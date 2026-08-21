"""Deterministically compile the repository's V4/V3.2 symbolic mapping artifact."""

# The compiler intentionally preserves long normative rationales as single literals.
# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.model.dependencies import validate_dependency_control
from hdmatch.model.mapping_library import (
    MAPPING_DIRECTNESS,
    STRUCTURAL_SALIENCE,
    AnswerOption,
    ChartPredicate,
    ContradictionRule,
    ContradictionSeverity,
    DirectnessClass,
    MappingLibrary,
    MappingRule,
    MappingStatus,
    ModelConstants,
    PredicateOperator,
    PredictedResponse,
    QuestionAnswerSpec,
    SourceArtifact,
    SourceCitation,
    StructuralClass,
)
from hdmatch.questionnaire.bank import QuestionBank, load_question_bank
from hdmatch.questionnaire.response import normalize_answer_token

QUESTION_BANK = "reference/core/question_bank_v1.json"
V4_PROTOCOL = "reference/core/human_design_reverse_matching_protocol_v4_1.md"
V3_PROTOCOL = "reference/core/human_design_search_instructions_fixed_candidate_blind(6).md"
V32_PROFILE = "reference/core/updated_behavioral_profile_v3_2.md"
V32_DELTA = "reference/core/v3_2_scoring_delta.md"
MAPPING_TODO = "reference/core/MAPPING_LIBRARY_TODO.md"

NORMATIVE_SOURCES = (
    QUESTION_BANK,
    V4_PROTOCOL,
    V3_PROTOCOL,
    V32_PROFILE,
    V32_DELTA,
    MAPPING_TODO,
)


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class QuestionDisposition(FrozenModel):
    question_id: str
    status: MappingStatus
    mapping_ids: tuple[str, ...]
    reason: str


class UnresolvedMappingReport(FrozenModel):
    schema_version: Literal["unresolved-mapping-report-v1"] = "unresolved-mapping-report-v1"
    model_version: Literal["V4/V3.2-symbolic-v1"] = "V4/V3.2-symbolic-v1"
    mapping_model_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mapping_file_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mapping_counts: dict[str, int]
    question_counts: dict[str, int]
    question_dispositions: tuple[QuestionDisposition, ...]
    unresolved_scientific_limitations: tuple[str, ...]


class CompilationResult(FrozenModel):
    mapping_path: str
    report_path: str
    mapping_model_sha256: str
    mapping_file_sha256: str
    mapping_counts: dict[str, int]
    question_counts: dict[str, int]


_OPTION_LABELS: dict[str, tuple[tuple[str, Literal["prompt", "response_format"]], ...]] = {
    "D01": (
        ("an immediate quiet sense", "prompt"),
        ("a gut-like yes/no energy", "prompt"),
        ("clarity that changes over hours or days", "prompt"),
        ("hearing your own words reveal the answer", "prompt"),
        ("clarity from being in the right place or with the right listener", "prompt"),
        ("no stable pattern", "prompt"),
    ),
    "D02": (
        ("brief and nonrepeating", "prompt"),
        ("loud and energizing", "prompt"),
        ("persistent until acted upon", "prompt"),
        ("emotionally charged", "prompt"),
        ("mostly a later interpretation", "prompt"),
    ),
    "D03": (
        ("remain stable", "prompt"),
        ("fluctuate with emotional highs and lows", "prompt"),
        ("become clearer only after sleeping on it", "prompt"),
    ),
    "S02": (("very often", "response_format"),),
    "S03": (("extremely", "response_format"),),
    "S04": (
        (
            "function better after a clear mutual opening than after assigning yourself a role",
            "prompt",
        ),
    ),
    "S05": (
        ("sustain daily workforce energy indefinitely if sleep and health are adequate", "prompt"),
        ("even good projects eventually require disproportionate retreat", "prompt"),
    ),
    "D07": (
        ("feel a stable internal sense of who you are and where you are going", "prompt"),
        ("direction become clearer through the people and places around you", "prompt"),
    ),
    "C01": (("become amplified inside you", "prompt"),),
    "C02": (("wave-like", "prompt"),),
    "C03": (("very often", "response_format"),),
    "C07": (("feel a strong need to clear them quickly so pressure disappears", "prompt"),),
    "C08": (
        ("physical energy renew through doing the right work", "prompt"),
        ("prolonged work deplete you even when it is meaningful", "prompt"),
    ),
    "C09": (("extremely", "response_format"),),
    "P01": (("very often", "response_format"),),
    "P02": (("very often", "response_format"),),
    "P03": (("very often", "response_format"),),
    "P05": (("very often", "response_format"),),
    "P07": (("strongly", "response_format"),),
    "P09": (("relief and mobilization", "prompt"),),
    "P10": (("extremely", "response_format"),),
    "P11": (("treat it as data", "prompt"),),
    "P12": (("because of what you have lived through", "prompt"),),
}


def _source(path: str, locator: str, rationale: str) -> SourceCitation:
    return SourceCitation(path=path, locator=locator, rationale=rationale)


def _token(label: str) -> str:
    return normalize_answer_token(label)


def _frozen_rule(
    *,
    suffix: str,
    observation: str,
    statement: str,
    cluster: str,
    question_ids: tuple[str, ...],
    feature: Literal["type", "strategy", "authority", "profile", "defined_centers"],
    operator: PredicateOperator,
    values: tuple[str, ...],
    canonical_label: str,
    support_labels: tuple[str, ...] | None = None,
    structural_class: StructuralClass,
    directness: DirectnessClass,
    sources: tuple[SourceCitation, ...],
    contradiction_labels: tuple[str, ...] = (),
    contradiction_severity: ContradictionSeverity = ContradictionSeverity.NONE,
    contradiction_rationale: str = "",
) -> MappingRule:
    contradiction = None
    if contradiction_labels:
        contradiction = ContradictionRule(
            answer_tokens=tuple(_token(label) for label in contradiction_labels),
            severity=contradiction_severity,
            behavioral_rationale=contradiction_rationale,
        )
    return MappingRule(
        mapping_id=f"MAP-{suffix}",
        observation_id=f"OBS-{observation}",
        behavioral_statement=statement,
        dependency_cluster=cluster,
        question_ids=question_ids,
        status=MappingStatus.FROZEN,
        chart_feature_predicate=ChartPredicate(
            feature=feature,
            operator=operator,
            values=values,
        ),
        predicted_response=PredictedResponse(
            canonical_answer_token=_token(canonical_label),
            support_answer_tokens=tuple(
                _token(label) for label in (support_labels or (canonical_label,))
            ),
        ),
        structural_class=structural_class,
        structural_salience=STRUCTURAL_SALIENCE[structural_class],
        mapping_directness_class=directness,
        mapping_directness=MAPPING_DIRECTNESS[directness],
        contradiction_rule=contradiction,
        sources=sources,
    )


def _compiled_frozen_rules() -> list[MappingRule]:
    authority_source = _source(
        V4_PROTOCOL,
        "V4.1 Addendum — Authority scope",
        "Splenic and Sacral processes are present-oriented; Emotional Authority requires waiting.",
    )
    immediate_source = _source(
        V3_PROTOCOL,
        "§23 Structural reuse rule",
        "The protocol explicitly links Splenic Authority with immediate non-repeating bodily knowing.",
    )
    emotional_source = _source(
        V3_PROTOCOL,
        "§16 Contradiction scale",
        "Waiting through an emotional wave is explicitly opposed to an immediate authority process.",
    )

    def question_source(question_id: str, rationale: str) -> SourceCitation:
        return _source(QUESTION_BANK, f"question {question_id}", rationale)

    return [
        _frozen_rule(
            suffix="AUTH-SPLENIC-D01",
            observation="AUTH-SPLENIC-IMMEDIATE",
            statement="Important decisions present as an immediate quiet sense.",
            cluster="AUTHORITY_DECISION",
            question_ids=("D01",),
            feature="authority",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Splenic",),
            canonical_label="an immediate quiet sense",
            structural_class=StructuralClass.AUTHORITY,
            directness=DirectnessClass.DIRECT,
            sources=(
                authority_source,
                immediate_source,
                question_source("D01", "Exact declared answer wording."),
            ),
            contradiction_labels=("clarity that changes over hours or days",),
            contradiction_severity=ContradictionSeverity.DIRECT,
            contradiction_rationale="Waiting across hours or days directly opposes the frozen immediate process.",
        ),
        _frozen_rule(
            suffix="AUTH-SACRAL-D01",
            observation="AUTH-SACRAL-RESPONSE",
            statement="Important decisions present as a gut-like yes/no energy.",
            cluster="AUTHORITY_DECISION",
            question_ids=("D01",),
            feature="authority",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Sacral",),
            canonical_label="a gut-like yes/no energy",
            structural_class=StructuralClass.AUTHORITY,
            directness=DirectnessClass.DIRECT,
            sources=(
                authority_source,
                question_source("D01", "Exact declared Sacral-like response wording."),
            ),
            contradiction_labels=("clarity that changes over hours or days",),
            contradiction_severity=ContradictionSeverity.DIRECT,
            contradiction_rationale="Waiting for an emotional wave directly opposes a present-oriented Sacral process.",
        ),
        _frozen_rule(
            suffix="AUTH-EMOTIONAL-D01",
            observation="AUTH-EMOTIONAL-WAIT",
            statement="Important-decision clarity changes over hours or days.",
            cluster="AUTHORITY_DECISION",
            question_ids=("D01",),
            feature="authority",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Emotional", "Emotional Solar Plexus", "Solar Plexus"),
            canonical_label="clarity that changes over hours or days",
            structural_class=StructuralClass.AUTHORITY,
            directness=DirectnessClass.DIRECT,
            sources=(
                authority_source,
                emotional_source,
                question_source("D01", "Exact declared delayed-clarity wording."),
            ),
            contradiction_labels=("an immediate quiet sense", "a gut-like yes/no energy"),
            contradiction_severity=ContradictionSeverity.DIRECT,
            contradiction_rationale="An explicitly immediate process directly opposes waiting through an emotional wave.",
        ),
        _frozen_rule(
            suffix="AUTH-SPLENIC-D02",
            observation="AUTH-SPLENIC-IMMEDIATE",
            statement="The immediate signal is brief and nonrepeating.",
            cluster="AUTHORITY_DECISION",
            question_ids=("D02",),
            feature="authority",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Splenic",),
            canonical_label="brief and nonrepeating",
            structural_class=StructuralClass.AUTHORITY,
            directness=DirectnessClass.DIRECT,
            sources=(
                immediate_source,
                question_source("D02", "Exact declared signal-quality wording."),
            ),
        ),
        _frozen_rule(
            suffix="AUTH-EMOTIONAL-D03",
            observation="AUTH-EMOTIONAL-WAIT",
            statement="Decision clarity fluctuates with emotional highs and lows or becomes clearer after sleep.",
            cluster="AUTHORITY_DECISION",
            question_ids=("D03",),
            feature="authority",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Emotional", "Emotional Solar Plexus", "Solar Plexus"),
            canonical_label="fluctuate with emotional highs and lows",
            support_labels=(
                "fluctuate with emotional highs and lows",
                "become clearer only after sleeping on it",
            ),
            structural_class=StructuralClass.AUTHORITY,
            directness=DirectnessClass.DIRECT,
            sources=(
                authority_source,
                emotional_source,
                question_source("D03", "Exact declared emotional-timing wording."),
            ),
        ),
        _frozen_rule(
            suffix="TYPE-PROJECTOR-S03",
            observation="TYPE-PROJECTOR-RECOGNITION",
            statement="Accurate recognition strongly changes willingness and effectiveness.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("S03",),
            feature="type",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Projector",),
            canonical_label="extremely",
            structural_class=StructuralClass.TYPE_STRATEGY,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§23 Structural reuse rule",
                    "Projector Type and waiting for recognition are explicitly one architecture.",
                ),
                question_source("S03", "The response scale is frozen in the question record."),
            ),
        ),
        _frozen_rule(
            suffix="TYPE-PROJECTOR-S04",
            observation="TYPE-PROJECTOR-RECOGNITION",
            statement="Major roles and collaborations function better after a clear mutual opening.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("S04",),
            feature="type",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Projector",),
            canonical_label="function better after a clear mutual opening than after assigning yourself a role",
            structural_class=StructuralClass.TYPE_STRATEGY,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V4_PROTOCOL,
                    "§8 Open autobiographical collection",
                    "The protocol explicitly uses Projector/invitation as the HD-labeled counterpart to a neutral opportunity-opening question.",
                ),
                question_source("S04", "Exact declared clear-opening wording."),
            ),
        ),
        _frozen_rule(
            suffix="TYPE-GENERATOR-S02",
            observation="TYPE-GENERATOR-RESPONSE",
            statement="Energy or interest commonly appears after a concrete option is present.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("S02",),
            feature="type",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Generator", "Manifesting Generator"),
            canonical_label="very often",
            structural_class=StructuralClass.TYPE_STRATEGY,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§8.1 Type + Strategy",
                    "Type and Strategy are a direct frozen architecture block.",
                ),
                question_source(
                    "S02",
                    "The question directly measures response after a concrete external stimulus.",
                ),
            ),
        ),
        _frozen_rule(
            suffix="TYPE-GENERATOR-S05",
            observation="TYPE-GENERATOR-SACRAL-ENERGY",
            statement="Meaningful work supports sustainable daily workforce energy.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("S05",),
            feature="type",
            operator=PredicateOperator.EQUALS_ANY,
            values=("Generator", "Manifesting Generator"),
            canonical_label="sustain daily workforce energy indefinitely if sleep and health are adequate",
            structural_class=StructuralClass.TYPE_STRATEGY,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§16 Contradiction scale",
                    "The protocol explicitly names sustainable Sacral-style workforce energy and its opposite architecture.",
                ),
                question_source("S05", "Exact declared sustainable-energy alternative."),
            ),
            contradiction_labels=(
                "even good projects eventually require disproportionate retreat",
            ),
            contradiction_severity=ContradictionSeverity.STRONG,
            contradiction_rationale="The frozen prompt presents disproportionate retreat as the opposing energy pattern.",
        ),
        _frozen_rule(
            suffix="CENTER-SOLARPLEXUS-UNDEFINED-C01",
            observation="CENTER-EMOTIONAL-AMPLIFICATION",
            statement="Another person's strong feelings become amplified internally.",
            cluster="CENTER_SOLAR_PLEXUS_STATE",
            question_ids=("C01",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("Solar Plexus",),
            canonical_label="become amplified inside you",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§20 Predeclared rarity anchors",
                    "The protocol's allowed example explicitly names open emotional amplification.",
                ),
                question_source("C01", "Exact declared amplification alternative."),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-SOLARPLEXUS-DEFINED-C02",
            observation="CENTER-EMOTIONAL-WAVE",
            statement="The safe-alone emotional baseline is wave-like.",
            cluster="AUTHORITY_DECISION",
            question_ids=("C02",),
            feature="defined_centers",
            operator=PredicateOperator.CONTAINS_ANY,
            values=("Solar Plexus",),
            canonical_label="wave-like",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V4_PROTOCOL,
                    "§9.2 Emotional wave versus mood instability",
                    "The protocol treats the emotional wave as a specific architecture-relevant process.",
                ),
                question_source("C02", "Exact declared emotional-baseline alternative."),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-EGO-UNDEFINED-C03",
            observation="CENTER-EGO-PROVING",
            statement="There is a recurring pressure to prove worth or promise beyond capacity.",
            cluster="CENTER_EGO_STATE",
            question_ids=("C03",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("Ego", "Heart", "Heart Ego", "Will"),
            canonical_label="very often",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.STRONG,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§16 Contradiction scale",
                    "The protocol permits a frozen distinction between reliable internally generated will and inconsistent/conditioned will.",
                ),
                question_source(
                    "C03",
                    "The item separates proving and overpromising from an externally required demand.",
                ),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-SACRAL-DEFINED-C08",
            observation="CENTER-SACRAL-ENERGY",
            statement="Physical energy renews through the right work.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("C08",),
            feature="defined_centers",
            operator=PredicateOperator.CONTAINS_ANY,
            values=("Sacral",),
            canonical_label="physical energy renew through doing the right work",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§16 Contradiction scale",
                    "The protocol explicitly contrasts sustainable Sacral-style workforce energy with the opposite architecture.",
                ),
                question_source("C08", "Exact declared energy-renewal alternative."),
            ),
            contradiction_labels=("prolonged work deplete you even when it is meaningful",),
            contradiction_severity=ContradictionSeverity.STRONG,
            contradiction_rationale="Meaningful work causing depletion is the declared opposing energy pattern.",
        ),
        _frozen_rule(
            suffix="CENTER-SACRAL-UNDEFINED-C08",
            observation="CENTER-NONSACRAL-DEPLETION",
            statement="Prolonged work depletes even when it is meaningful.",
            cluster="TYPE_STRATEGY_ARCHITECTURE",
            question_ids=("C08",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("Sacral",),
            canonical_label="prolonged work deplete you even when it is meaningful",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.DIRECT,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§16 Contradiction scale",
                    "The protocol explicitly permits the opposing non-Sacral energy prediction.",
                ),
                question_source("C08", "Exact declared depletion alternative."),
            ),
            contradiction_labels=("physical energy renew through doing the right work",),
            contradiction_severity=ContradictionSeverity.STRONG,
            contradiction_rationale="Renewal through work is the declared opposing energy pattern.",
        ),
        _frozen_rule(
            suffix="CENTER-G-DEFINED-D07",
            observation="CENTER-G-STABLE-DIRECTION",
            statement="Direction rests on a stable internal sense of identity.",
            cluster="CENTER_G_STATE",
            question_ids=("D07",),
            feature="defined_centers",
            operator=PredicateOperator.CONTAINS_ANY,
            values=("G", "Identity"),
            canonical_label="feel a stable internal sense of who you are and where you are going",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.STRONG,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§8.3 Diagnostic Centers",
                    "Strong center-state predictions may be frozen as a core architecture block.",
                ),
                question_source("D07", "Exact declared stable-identity alternative."),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-G-UNDEFINED-D07",
            observation="CENTER-G-ENVIRONMENTAL-DIRECTION",
            statement="Direction becomes clearer through surrounding people and places.",
            cluster="CENTER_G_STATE",
            question_ids=("D07",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("G", "Identity"),
            canonical_label="direction become clearer through the people and places around you",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.STRONG,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§8.3 Diagnostic Centers",
                    "Strong center-state predictions may be frozen as a core architecture block.",
                ),
                question_source("D07", "Exact declared environmental-direction alternative."),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-G-UNDEFINED-C09",
            observation="CENTER-G-ENVIRONMENTAL-DIRECTION",
            statement="Place and company strongly change felt direction or identity.",
            cluster="CENTER_G_STATE",
            question_ids=("C09",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("G", "Identity"),
            canonical_label="extremely",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.STRONG,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§8.3 Diagnostic Centers",
                    "Strong center-state predictions may be frozen as a core architecture block.",
                ),
                question_source("C09", "The response scale is frozen in the question record."),
            ),
        ),
        _frozen_rule(
            suffix="CENTER-ROOT-UNDEFINED-C07",
            observation="CENTER-ROOT-PRESSURE-CLEARING",
            statement="Pending tasks create pressure to clear them quickly so the pressure disappears.",
            cluster="CENTER_ROOT_STATE",
            question_ids=("C07",),
            feature="defined_centers",
            operator=PredicateOperator.NOT_CONTAINS_ANY,
            values=("Root",),
            canonical_label="feel a strong need to clear them quickly so pressure disappears",
            structural_class=StructuralClass.DIAGNOSTIC_CENTER,
            directness=DirectnessClass.STRONG,
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§8.3 Diagnostic Centers",
                    "Strong center-state predictions may be frozen as a core architecture block.",
                ),
                question_source("C07", "Exact declared pressure-clearing alternative."),
            ),
        ),
        *_profile_rules(),
    ]


def _profile_rules() -> list[MappingRule]:
    # The P-series wording follows the V3 single-line scoring rule. Only the clearest
    # line constructs are frozen; multi-line/role interpretations remain unresolved.
    source = _source(
        V3_PROTOCOL,
        "§8.4 Profile",
        "The protocol permits scoring one genuinely predicted line without forcing a second line.",
    )
    specs = (
        (
            "P01",
            "1",
            "very often",
            "FOUNDATION",
            "Foundation investigation precedes action in unfamiliar domains.",
        ),
        (
            "P02",
            "2",
            "very often",
            "NATURAL",
            "Strong abilities develop privately and are recognized by others.",
        ),
        (
            "P03",
            "3",
            "very often",
            "TRIAL-ERROR",
            "Learning proceeds primarily through trial, error, and adaptation.",
        ),
        (
            "P10",
            "4",
            "extremely",
            "NETWORK",
            "Network reputation strongly affects later opportunities.",
        ),
        (
            "P05",
            "5",
            "very often",
            "PROJECTION",
            "Others project a larger practical role and later encounter its limits.",
        ),
        (
            "P07",
            "6",
            "strongly",
            "DEVELOPMENT",
            "Life follows experimentation, observation, and later role-modeling phases.",
        ),
        (
            "P09",
            "2",
            "relief and mobilization",
            "NATURAL",
            "Accurate calling-out of natural ability produces relief and mobilization.",
        ),
        ("P11", "3", "treat it as data", "TRIAL-ERROR", "Failed experiments are treated as data."),
        (
            "P12",
            "6",
            "because of what you have lived through",
            "DEVELOPMENT",
            "Perspective is sought because of lived experience.",
        ),
    )
    result: list[MappingRule] = []
    for question_id, line, label, name, statement in specs:
        # Kept local to prevent the question-bank source from being treated as a
        # server-side mapping on its own; V3 §8.4 is the controlling mapping rule.
        result.append(
            _frozen_rule(
                suffix=f"PROFILE-LINE{line}-{question_id}",
                observation=f"PROFILE-LINE{line}-{name}",
                statement=statement,
                cluster="PROFILE_ARCHITECTURE",
                question_ids=(question_id,),
                feature="profile",
                operator=PredicateOperator.PROFILE_HAS_LINE,
                values=(line,),
                canonical_label=label,
                structural_class=StructuralClass.PROFILE,
                directness=DirectnessClass.DIRECT,
                sources=(
                    source,
                    _source(
                        QUESTION_BANK,
                        f"question {question_id}",
                        "Frozen P-series line-behavior wording.",
                    ),
                ),
            )
        )
    return result


def _non_frozen_rules(bank: QuestionBank, frozen_rules: Iterable[MappingRule]) -> list[MappingRule]:
    covered = {question_id for rule in frozen_rules for question_id in rule.question_ids}
    empirical_groups = (
        (
            "V32-MASTERY-EXCLUDED",
            "OBS-V32-MASTERY-EXCLUDED",
            "MASTERY_MOTIVE",
            ("A05", "T02", "T03"),
            "V3.2 invalidates expertise or polished output as positive symbolic evidence of an independent mastery drive; only a separately learned human model may re-establish it.",
        ),
        (
            "V32-SYSTEM-IDENTIFICATION-EXCLUDED",
            "OBS-V32-SYSTEM-IDENTIFICATION-EXCLUDED",
            "SYSTEM_IDENTIFICATION",
            ("A06",),
            "V3.2 states that institutional participation does not imply motivational identification or imitation; no replacement chart predicate is supplied.",
        ),
        (
            "V32-ADVANCEMENT-EXCLUDED",
            "OBS-V32-ADVANCEMENT-EXCLUDED",
            "HIERARCHICAL_ADVANCEMENT",
            ("A07", "T10"),
            "V3.2 removes material or hierarchical advancement as positive symbolic evidence and keeps resource competence separate; only empirical refitting may restore it.",
        ),
    )
    result: list[MappingRule] = []
    empirical_source = _source(
        V32_DELTA,
        "Behavioral corrections",
        "The V3.2 delta explicitly removes mastery and advancement shortcuts from positive scoring.",
    )
    for suffix, observation, cluster, question_ids, reason in empirical_groups:
        result.append(
            MappingRule(
                mapping_id=f"MAP-{suffix}",
                observation_id=observation,
                behavioral_statement=reason,
                dependency_cluster=cluster,
                question_ids=question_ids,
                status=MappingStatus.EMPIRICAL_ONLY,
                sources=(empirical_source,),
                unresolved_reason=reason,
            )
        )
        covered.update(question_ids)

    for question in bank.questions:
        if question.id in covered:
            continue
        reason = (
            "The normative repository supplies no predeclared chart-feature predicate and "
            "contradiction rule for this question. It remains non-scoring until a sourced "
            "symbolic mapping or separately versioned empirical mapping exists."
        )
        result.append(
            MappingRule(
                mapping_id=f"MAP-UNRESOLVED-{question.id}",
                observation_id=f"OBS-UNRESOLVED-{question.id}",
                behavioral_statement=(
                    f"Unresolved mapping for {question.domain}: {question.prompt}"
                ),
                dependency_cluster=f"UNRESOLVED_{question.id}",
                question_ids=(question.id,),
                status=MappingStatus.UNRESOLVED,
                sources=(
                    _source(
                        QUESTION_BANK,
                        f"question {question.id}",
                        "Normative frozen question wording.",
                    ),
                    _source(
                        MAPPING_TODO,
                        "Mapping Library Formalization TODO",
                        "Unsupported mappings must remain unresolved rather than being invented.",
                    ),
                ),
                unresolved_reason=reason,
            )
        )
    return result


def build_mapping_library(project_root: str | Path) -> MappingLibrary:
    root = Path(project_root)
    bank_path = root / QUESTION_BANK
    bank = load_question_bank(bank_path)
    frozen_rules = _compiled_frozen_rules()
    rules = tuple(frozen_rules + _non_frozen_rules(bank, frozen_rules))
    answer_specs = tuple(
        QuestionAnswerSpec(
            question_id=question_id,
            options=tuple(
                AnswerOption(token=_token(label), label=label, source=source)
                for label, source in options
            ),
        )
        for question_id, options in sorted(_OPTION_LABELS.items())
    )
    library = MappingLibrary(
        question_bank_version=bank.version,
        question_bank_sha256=_sha256_file(bank_path),
        source_artifacts=tuple(
            SourceArtifact(path=path, sha256=_sha256_file(root / path))
            for path in NORMATIVE_SOURCES
        ),
        constants=ModelConstants(),
        answer_specs=answer_specs,
        mappings=rules,
    )
    library.validate_against_question_bank(bank)
    validate_dependency_control(library)
    return library


def compile_mapping_artifacts(
    project_root: str | Path,
    *,
    mapping_path: str | Path | None = None,
    report_path: str | Path | None = None,
) -> CompilationResult:
    """Write deterministic mapping and unresolved-report JSON artifacts."""

    root = Path(project_root)
    target_mapping = (
        Path(mapping_path) if mapping_path else root / "mappings/mapping_library_v1.json"
    )
    target_report = (
        Path(report_path) if report_path else root / "mappings/unresolved_mapping_report_v1.json"
    )
    library = build_mapping_library(root)
    _write_json(target_mapping, library.model_dump(mode="json", exclude_none=False))
    mapping_file_sha256 = _sha256_file(target_mapping)
    report = build_unresolved_report(
        library,
        mapping_file_sha256=mapping_file_sha256,
    )
    _write_json(target_report, report.model_dump(mode="json", exclude_none=False))
    return CompilationResult(
        mapping_path=str(target_mapping),
        report_path=str(target_report),
        mapping_model_sha256=library.sha256(),
        mapping_file_sha256=mapping_file_sha256,
        mapping_counts=report.mapping_counts,
        question_counts=report.question_counts,
    )


def build_unresolved_report(
    library: MappingLibrary, *, mapping_file_sha256: str
) -> UnresolvedMappingReport:
    mappings_by_question: dict[str, list[MappingRule]] = defaultdict(list)
    for mapping in library.mappings:
        for question_id in mapping.question_ids:
            mappings_by_question[question_id].append(mapping)

    dispositions: list[QuestionDisposition] = []
    for question_id, mappings in sorted(mappings_by_question.items()):
        statuses = {mapping.status for mapping in mappings}
        if MappingStatus.FROZEN in statuses:
            status = MappingStatus.FROZEN
            reason = "At least one conservative, sourced symbolic rule is frozen; unlisted answers remain neutral."
        elif MappingStatus.EMPIRICAL_ONLY in statuses:
            status = MappingStatus.EMPIRICAL_ONLY
            reason = next(mapping.unresolved_reason or "" for mapping in mappings)
        else:
            status = MappingStatus.UNRESOLVED
            reason = next(mapping.unresolved_reason or "" for mapping in mappings)
        dispositions.append(
            QuestionDisposition(
                question_id=question_id,
                status=status,
                mapping_ids=tuple(sorted(mapping.mapping_id for mapping in mappings)),
                reason=reason,
            )
        )

    mapping_counts = Counter(mapping.status.value for mapping in library.mappings)
    question_counts = Counter(disposition.status.value for disposition in dispositions)
    return UnresolvedMappingReport(
        mapping_model_sha256=library.sha256(),
        mapping_file_sha256=mapping_file_sha256,
        mapping_counts={
            key: mapping_counts.get(key, 0)
            for key in sorted(status.value for status in MappingStatus)
        },
        question_counts={
            key: question_counts.get(key, 0)
            for key in sorted(status.value for status in MappingStatus)
        },
        question_dispositions=tuple(dispositions),
        unresolved_scientific_limitations=(
            "The question bank intentionally contains no complete server-side HD key; this artifact freezes only the direct architecture links recoverable from the normative repository.",
            "No gate, channel, definition, cardinal-activation, Color, Tone, Base, Incarnation Cross, or variable-level behavioral mappings are sufficiently specified to freeze.",
            "Self-Projected, Ego, Environmental/No-Inner, and Lunar Authority response keys are not sufficiently specified in the normative text and therefore remain unresolved.",
            "Manifestor and Reflector Type/Strategy response keys and all four Not-Self signature alternatives lack an explicit normative mapping table and remain unresolved.",
            "Profile entries encode only the clearest single-line constructs; personality/design role order and exact two-line Profile predictions remain unresolved.",
            "Symbolic rarity weights are rubric bits, not probabilities; candidate-universe prevalence must be supplied independently at scoring time.",
            "V3.2 exclusions prevent mastery, institutional participation, and material competence from acting as positive shortcuts; future human-learned versions must be separate artifacts.",
        ),
    )


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
