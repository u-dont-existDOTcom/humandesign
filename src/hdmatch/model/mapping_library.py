"""Typed, versioned symbolic mapping-library schema and deterministic hashing."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from enum import Enum, StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.questionnaire.bank import QuestionBank
from hdmatch.questionnaire.response import normalize_answer_token


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class MappingStatus(StrEnum):
    FROZEN = "frozen"
    UNRESOLVED = "unresolved"
    EMPIRICAL_ONLY = "empirical_only"


class StructuralClass(StrEnum):
    TYPE_STRATEGY = "type_strategy"
    AUTHORITY = "authority"
    DIAGNOSTIC_CENTER = "diagnostic_center"
    PROFILE = "profile"
    COMPLETE_CHANNEL = "complete_channel"
    CARDINAL_ACTIVATION = "cardinal_activation"
    DEFINITION = "definition"
    REPEATED_GATE_OR_NODE = "repeated_gate_or_node"
    PROMINENT_ACTIVATION = "prominent_activation"
    HANGING_GATE = "hanging_gate"
    GENERIC_SYMBOLISM = "generic_symbolism"


STRUCTURAL_SALIENCE: Mapping[StructuralClass, float] = {
    StructuralClass.TYPE_STRATEGY: 1.00,
    StructuralClass.AUTHORITY: 1.00,
    StructuralClass.DIAGNOSTIC_CENTER: 0.90,
    StructuralClass.PROFILE: 0.85,
    StructuralClass.COMPLETE_CHANNEL: 0.80,
    StructuralClass.CARDINAL_ACTIVATION: 0.75,
    StructuralClass.DEFINITION: 0.65,
    StructuralClass.REPEATED_GATE_OR_NODE: 0.55,
    StructuralClass.PROMINENT_ACTIVATION: 0.45,
    StructuralClass.HANGING_GATE: 0.35,
    StructuralClass.GENERIC_SYMBOLISM: 0.15,
}


class DirectnessClass(StrEnum):
    DIRECT = "direct"
    STRONG = "strong"
    PLAUSIBLE = "plausible"
    NONE = "none"


MAPPING_DIRECTNESS: Mapping[DirectnessClass, float] = {
    DirectnessClass.DIRECT: 1.00,
    DirectnessClass.STRONG: 0.75,
    DirectnessClass.PLAUSIBLE: 0.50,
    DirectnessClass.NONE: 0.00,
}


class ContradictionSeverity(float, Enum):
    NONE = 0.00
    MILD = 0.25
    MEANINGFUL = 0.50
    STRONG = 0.75
    DIRECT = 1.00


class PredicateOperator(StrEnum):
    EQUALS_ANY = "equals_any"
    CONTAINS_ANY = "contains_any"
    NOT_CONTAINS_ANY = "not_contains_any"
    PROFILE_HAS_LINE = "profile_has_line"


class SourceCitation(FrozenModel):
    path: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class SourceArtifact(FrozenModel):
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class AnswerOption(FrozenModel):
    """A mechanical token for wording already present in the frozen question record."""

    token: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    label: str = Field(min_length=1)
    source: Literal["prompt", "response_format"]

    @model_validator(mode="after")
    def token_matches_label(self) -> AnswerOption:
        if self.token != normalize_answer_token(self.label):
            raise ValueError("answer token must be the mechanical normalization of its label")
        return self


class QuestionAnswerSpec(FrozenModel):
    question_id: str = Field(min_length=1)
    options: tuple[AnswerOption, ...] = Field(min_length=1)
    unmapped_answer_policy: Literal["neutral"] = "neutral"

    @model_validator(mode="after")
    def unique_tokens(self) -> QuestionAnswerSpec:
        tokens = [option.token for option in self.options]
        if len(tokens) != len(set(tokens)):
            raise ValueError(f"duplicate answer token for {self.question_id}")
        return self


class ChartPredicate(FrozenModel):
    """Small declarative predicate over chart features; no candidate-specific logic."""

    feature: Literal["type", "strategy", "authority", "profile", "defined_centers"]
    operator: PredicateOperator
    values: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def compatible_operator(self) -> ChartPredicate:
        if self.operator is PredicateOperator.PROFILE_HAS_LINE:
            if self.feature != "profile" or len(self.values) != 1:
                raise ValueError("profile_has_line requires one profile-line value")
            if self.values[0] not in {"1", "2", "3", "4", "5", "6"}:
                raise ValueError("profile line must be 1 through 6")
        elif self.feature == "profile":
            raise ValueError("profile predicates must use profile_has_line")
        return self

    def matches(self, chart: Mapping[str, Any] | object) -> bool:
        """Evaluate against a mapping or typed chart-feature record."""

        if isinstance(chart, Mapping):
            raw_value = chart.get(self.feature)
        else:
            raw_value = getattr(chart, self.feature, None)

        if self.operator is PredicateOperator.PROFILE_HAS_LINE:
            if raw_value is None:
                return False
            lines = re.findall(r"[1-6]", str(raw_value))
            return self.values[0] in lines[:2]

        expected = {_normalize_feature(value) for value in self.values}
        if self.operator is PredicateOperator.EQUALS_ANY:
            return _normalize_feature(raw_value) in expected

        if raw_value is None:
            present: set[str] = set()
        elif isinstance(raw_value, str):
            present = {_normalize_feature(raw_value)}
        else:
            try:
                present = {_normalize_feature(value) for value in raw_value}
            except TypeError:
                present = {_normalize_feature(raw_value)}
        intersects = bool(expected & present)
        if self.operator is PredicateOperator.CONTAINS_ANY:
            return intersects
        if self.operator is PredicateOperator.NOT_CONTAINS_ANY:
            return not intersects
        raise AssertionError(f"unsupported operator: {self.operator}")


class PredictedResponse(FrozenModel):
    canonical_answer_token: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    support_answer_tokens: tuple[str, ...] = Field(min_length=1)
    rule: Literal["symbolic_support"] = "symbolic_support"

    @model_validator(mode="after")
    def canonical_is_supported(self) -> PredictedResponse:
        if self.canonical_answer_token not in self.support_answer_tokens:
            raise ValueError("canonical answer must also be a support answer")
        if len(self.support_answer_tokens) != len(set(self.support_answer_tokens)):
            raise ValueError("support answer tokens must be unique")
        return self


class ContradictionRule(FrozenModel):
    answer_tokens: tuple[str, ...] = Field(min_length=1)
    severity: ContradictionSeverity
    behavioral_rationale: str = Field(min_length=1)

    @field_validator("severity")
    @classmethod
    def nonzero_severity(cls, value: ContradictionSeverity) -> ContradictionSeverity:
        if value is ContradictionSeverity.NONE:
            raise ValueError("stored contradiction rules must have nonzero severity")
        return value


class MappingRule(FrozenModel):
    mapping_id: str = Field(pattern=r"^MAP-[A-Z0-9-]+$")
    observation_id: str = Field(pattern=r"^OBS-[A-Z0-9-]+$")
    behavioral_statement: str = Field(min_length=1)
    dependency_cluster: str = Field(pattern=r"^[A-Z0-9_]+$")
    question_ids: tuple[str, ...] = Field(min_length=1)
    status: MappingStatus
    chart_feature_predicate: ChartPredicate | None = None
    predicted_response: PredictedResponse | None = None
    structural_class: StructuralClass | None = None
    structural_salience: float | None = Field(default=None, ge=0.0, le=1.0)
    mapping_directness_class: DirectnessClass | None = None
    mapping_directness: float | None = Field(default=None, ge=0.0, le=1.0)
    contradiction_rule: ContradictionRule | None = None
    sources: tuple[SourceCitation, ...] = Field(min_length=1)
    unresolved_reason: str | None = None

    @model_validator(mode="after")
    def status_controls_scoring_fields(self) -> MappingRule:
        scoring_fields = (
            self.chart_feature_predicate,
            self.predicted_response,
            self.structural_class,
            self.structural_salience,
            self.mapping_directness_class,
            self.mapping_directness,
        )
        if self.status is MappingStatus.FROZEN:
            if any(value is None for value in scoring_fields):
                raise ValueError("frozen mappings require every scoring field")
            assert self.structural_class is not None
            assert self.mapping_directness_class is not None
            if self.structural_salience != STRUCTURAL_SALIENCE[self.structural_class]:
                raise ValueError("structural salience must equal the frozen V3 constant")
            if self.mapping_directness != MAPPING_DIRECTNESS[self.mapping_directness_class]:
                raise ValueError("mapping directness must equal the frozen V3 constant")
            if self.unresolved_reason is not None:
                raise ValueError("frozen mappings cannot have an unresolved reason")
        else:
            if any(value is not None for value in scoring_fields):
                raise ValueError("non-frozen mappings cannot carry scoring fields")
            if self.contradiction_rule is not None:
                raise ValueError("non-frozen mappings cannot carry contradiction rules")
            if not self.unresolved_reason:
                raise ValueError("non-frozen mappings require an explicit reason")
        return self

    @property
    def anchor_id(self) -> str:
        """Stable prevalence/dependency key for this exact chart predicate."""

        if self.chart_feature_predicate is None:
            raise ValueError("unresolved mappings have no structural anchor")
        predicate = self.chart_feature_predicate
        values = ",".join(sorted(_normalize_feature(value) for value in predicate.values))
        return f"{predicate.feature}:{predicate.operator.value}:{values}"


class ModelConstants(FrozenModel):
    information_cap_rubric_bits: float = 6.0
    contradiction_cap_rubric_bits: float = 4.0
    independent_corroboration_cap: float = 0.15
    core_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "type_strategy": 30.0,
            "authority": 30.0,
            "diagnostic_centers": 25.0,
            "profile": 15.0,
        }
    )

    @model_validator(mode="after")
    def frozen_values(self) -> ModelConstants:
        if self.information_cap_rubric_bits != 6.0:
            raise ValueError("V3 information cap is frozen at 6 rubric bits")
        if self.contradiction_cap_rubric_bits != 4.0:
            raise ValueError("V3 contradiction cap is frozen at 4 rubric bits")
        if self.independent_corroboration_cap != 0.15:
            raise ValueError("V3 corroboration cap is frozen at 15%")
        if self.core_weights != {
            "type_strategy": 30.0,
            "authority": 30.0,
            "diagnostic_centers": 25.0,
            "profile": 15.0,
        }:
            raise ValueError("V3 core weights are frozen at 30/30/25/15")
        return self


class MappingLibrary(FrozenModel):
    schema_version: Literal["mapping-library-v1"] = "mapping-library-v1"
    model_version: Literal["V4/V3.2-symbolic-v1"] = "V4/V3.2-symbolic-v1"
    question_bank_version: str = Field(min_length=1)
    question_bank_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    source_artifacts: tuple[SourceArtifact, ...] = Field(min_length=1)
    constants: ModelConstants = Field(default_factory=ModelConstants)
    answer_specs: tuple[QuestionAnswerSpec, ...]
    mappings: tuple[MappingRule, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_identifiers_and_valid_answer_references(self) -> MappingLibrary:
        mapping_ids = [mapping.mapping_id for mapping in self.mappings]
        if len(mapping_ids) != len(set(mapping_ids)):
            raise ValueError("mapping IDs must be unique")
        answer_specs = {spec.question_id: spec for spec in self.answer_specs}
        if len(answer_specs) != len(self.answer_specs):
            raise ValueError("question answer specs must be unique")
        available_tokens = {
            question_id: {option.token for option in spec.options}
            for question_id, spec in answer_specs.items()
        }
        for mapping in self.frozen_mappings:
            assert mapping.predicted_response is not None
            for question_id in mapping.question_ids:
                if question_id not in available_tokens:
                    raise ValueError(
                        f"missing answer spec for frozen mapping question {question_id}"
                    )
                referenced = set(mapping.predicted_response.support_answer_tokens)
                if mapping.contradiction_rule is not None:
                    referenced.update(mapping.contradiction_rule.answer_tokens)
                unknown = referenced - available_tokens[question_id]
                if unknown:
                    raise ValueError(
                        f"mapping {mapping.mapping_id} references undeclared tokens: "
                        f"{sorted(unknown)}"
                    )
        return self

    @property
    def frozen_mappings(self) -> tuple[MappingRule, ...]:
        return tuple(mapping for mapping in self.mappings if mapping.status is MappingStatus.FROZEN)

    def answer_spec(self, question_id: str) -> QuestionAnswerSpec:
        for spec in self.answer_specs:
            if spec.question_id == question_id:
                return spec
        raise KeyError(question_id)

    def validate_against_question_bank(self, bank: QuestionBank) -> None:
        """Check question coverage and prove that every token comes from frozen wording."""

        referenced_questions = {
            question_id for mapping in self.mappings for question_id in mapping.question_ids
        }
        missing = bank.question_ids - referenced_questions
        unknown = referenced_questions - bank.question_ids
        if missing:
            raise ValueError(f"mapping library omits question IDs: {sorted(missing)}")
        if unknown:
            raise ValueError(f"mapping library has unknown question IDs: {sorted(unknown)}")

        for spec in self.answer_specs:
            question = bank.by_id(spec.question_id)
            for option in spec.options:
                if option.source == "prompt":
                    if option.label.casefold() not in question.prompt.casefold():
                        raise ValueError(
                            f"{spec.question_id} token label is not verbatim prompt wording: "
                            f"{option.label!r}"
                        )
                elif option.label not in question.response_format_options:
                    raise ValueError(
                        f"{spec.question_id} token label is not a declared response-format option: "
                        f"{option.label!r}"
                    )

    def canonical_bytes(self) -> bytes:
        payload = self.model_dump(mode="json", exclude_none=False)
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def matching_mappings(
        self, chart: Mapping[str, Any] | object, *, question_id: str | None = None
    ) -> tuple[MappingRule, ...]:
        matches: list[MappingRule] = []
        for mapping in self.frozen_mappings:
            if question_id is not None and question_id not in mapping.question_ids:
                continue
            assert mapping.chart_feature_predicate is not None
            if mapping.chart_feature_predicate.matches(chart):
                matches.append(mapping)
        return tuple(matches)

    def canonical_answers(self, chart: Mapping[str, Any] | object) -> dict[str, str]:
        """Return deterministic model-predicted answers, omitting unresolved conflicts."""

        predictions: dict[str, set[str]] = {}
        for mapping in self.matching_mappings(chart):
            assert mapping.predicted_response is not None
            for question_id in mapping.question_ids:
                predictions.setdefault(question_id, set()).add(
                    mapping.predicted_response.canonical_answer_token
                )
        return {
            question_id: next(iter(tokens))
            for question_id, tokens in sorted(predictions.items())
            if len(tokens) == 1
        }


def _normalize_feature(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).casefold())


def load_mapping_library(path: str | Path) -> MappingLibrary:
    source = Path(path)
    return MappingLibrary.model_validate(json.loads(source.read_text(encoding="utf-8")))


def mapping_library_sha256(library: MappingLibrary) -> str:
    return library.sha256()


def ensure_unique_question_ids(question_ids: Sequence[str]) -> tuple[str, ...]:
    """Small helper for compiler code that preserves declaration order."""

    result = tuple(question_ids)
    if len(result) != len(set(result)):
        raise ValueError("question IDs must be unique")
    return result
