"""Frozen composite runtime for ``MODEL-B-DETAILED-V2-NEW``.

Claim-grade recovery needs only the compiled artifact, its freeze receipt, the
unchanged Model A mapping, public chart inputs/ephemeris, and writable output.
Source and preregistration files were validated before freeze and are bound by
hash, but are intentionally not runtime mount requirements.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from typing import Any

from hdmatch.model import MappingLibrary, load_mapping_library, score_symbolic
from hdmatch.model_b.scoring import score_detailed_symbolic
from hdmatch.schemas import BehavioralResponse, CandidateState, ChartFeatures, ScoredState
from hdmatch.util import sha256_file, sha256_json

from .artifacts import (
    MODEL_ID,
    ArtifactBinding,
    AssignmentScope,
    CompiledModelArtifact,
    ModelFreezeReceipt,
    canonical_bytes,
    load_compiled_artifact,
    load_freeze_receipt,
)
from .evaluator import (
    canonical_detailed_answers,
    detailed_question_clusters,
    evaluate_compiled_model,
)
from .prevalence import PreparedPrevalence, prepare_prevalence
from .selectors import structural_signature


class FrozenModelBV2New:
    """The separately identified prospective detailed model."""

    model_id = MODEL_ID
    detailed_scoring_status = "prospectively_frozen"
    assignment_scope = AssignmentScope.DISCOVERY

    def __init__(
        self,
        compiled_artifact_path: str | Path,
        freeze_receipt_path: str | Path,
        *,
        base_mapping_path: str | Path,
    ) -> None:
        self.compiled_artifact_path = Path(compiled_artifact_path)
        self.freeze_receipt_path = Path(freeze_receipt_path)
        self.base_mapping_path = Path(base_mapping_path)
        self.artifact: CompiledModelArtifact = load_compiled_artifact(self.compiled_artifact_path)
        self.freeze_receipt: ModelFreezeReceipt = load_freeze_receipt(self.freeze_receipt_path)
        self._verify_public_runtime_chain()
        self.base_library: MappingLibrary = load_mapping_library(self.base_mapping_path)
        if self.base_library.question_bank_sha256 != self.artifact.question_bank.sha256:
            raise ValueError("Model A and frozen V2 bind different question-bank bytes")
        self._compiled_file_sha256 = sha256_file(self.compiled_artifact_path)
        self._freeze_file_sha256 = sha256_file(self.freeze_receipt_path)
        self._selectors = tuple(
            pathway.selector
            for rule in self.artifact.rules_for_scope(self.assignment_scope)
            for pathway in (
                rule.primary,
                *rule.alternatives,
                *((rule.corroborator,) if rule.corroborator is not None else ()),
            )
        )

    @property
    def library(self) -> MappingLibrary:
        return self.base_library

    @property
    def model_sha256(self) -> str:
        return sha256_json(
            {
                "model_id": self.model_id,
                "compiled_file_sha256": self._compiled_file_sha256,
                "compiled_semantic_sha256": self.artifact.sha256(),
                "freeze_receipt_file_sha256": self._freeze_file_sha256,
                "base_model_semantic_sha256": self.base_library.sha256(),
                "assignment_scope": self.assignment_scope.value,
                "holdout_status": "frozen-withheld",
            }
        )

    @property
    def mapping_sha256(self) -> str:
        return self._compiled_file_sha256

    @property
    def question_bank_sha256(self) -> str:
        return self.artifact.question_bank.sha256

    @property
    def capability_metadata(self) -> Mapping[str, object]:
        return {
            "behavioral_scoring": "model-a-plus-prospective-detailed-v2-new",
            "detailed_behavioral_mappings": self.detailed_scoring_status,
            "assignment_scope": self.assignment_scope.value,
            "scientific_claim": "engineering-discovery-only-not-holdout-validation",
            "holdout": "frozen-withheld",
            "active_detailed_rule_count": len(self.artifact.rules_for_scope(self.assignment_scope)),
            "withheld_holdout_rule_count": sum(
                rule.assignment == "holdout" for rule in self.artifact.rules
            ),
            "unresolved_detailed_observation_count": len(self.artifact.unresolved_observations),
            "freeze_receipt_sha256": self._freeze_file_sha256,
        }

    def score_signature(self, chart: ChartFeatures) -> tuple[Any, ...]:
        return (
            self.assignment_scope.value,
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            chart.definition,
            tuple(sorted(chart.defined_centers)),
            tuple(sorted(chart.channels, key=_channel_sort_key)),
            structural_signature(chart, self._selectors),
        )

    def canonical_answers(self, chart: ChartFeatures) -> dict[str, str]:
        core = self.base_library.canonical_answers(chart)
        detailed = canonical_detailed_answers(self.artifact, chart, self.assignment_scope)
        overlap = set(core) & set(detailed)
        conflicts = {
            question_id
            for question_id in sorted(overlap)
            if detailed[question_id] != "unknown" and core[question_id] != detailed[question_id]
        }
        result = {**core, **detailed}
        for question_id in conflicts:
            result[question_id] = "unknown"
        return result

    def oracle_responses(self, chart: ChartFeatures) -> Sequence[BehavioralResponse]:
        canonical = self.canonical_answers(chart)
        clusters: dict[str, set[str]] = {}
        for mapping in self.base_library.frozen_mappings:
            for question_id in mapping.question_ids:
                clusters.setdefault(question_id, set()).add(mapping.dependency_cluster)
        for question_id, question_clusters in detailed_question_clusters(
            self.artifact, self.assignment_scope
        ).items():
            clusters.setdefault(question_id, set()).update(question_clusters)
        return tuple(
            BehavioralResponse(
                question_id=question_id,
                cluster_id="+".join(sorted(clusters[question_id])),
                answer=answer,
                behavioral_confidence=1.0,
                measurement_reliability=1.0,
            )
            for question_id, answer in sorted(canonical.items())
        )

    def answer_spaces(self) -> Mapping[str, Sequence[str]]:
        spaces: dict[str, list[str]] = {
            spec.question_id: [option.token for option in spec.options]
            for spec in self.base_library.answer_specs
        }
        scoped_questions = {
            rule.prediction.question_id
            for rule in self.artifact.rules_for_scope(self.assignment_scope)
        }
        for token_set in self.artifact.question_token_sets:
            if token_set.question_id not in scoped_questions:
                continue
            target = spaces.setdefault(token_set.question_id, [])
            target.extend(token.token for token in token_set.tokens)
        return {
            question_id: tuple(dict.fromkeys((*tokens, "unknown")))
            for question_id, tokens in sorted(spaces.items())
        }

    def prepare_prevalence(
        self,
        states: Sequence[CandidateState],
    ) -> PreparedPrevalence:
        return prepare_prevalence(states, self.base_library, self.artifact)

    def score(
        self,
        state: CandidateState,
        responses: Iterable[BehavioralResponse],
        prevalence: PreparedPrevalence,
    ) -> ScoredState:
        if not isinstance(prevalence, PreparedPrevalence):
            raise TypeError("MODEL-B-DETAILED-V2-NEW requires prepare_prevalence(states) output")
        response_tuple = tuple(responses)
        core = score_symbolic(
            state.chart_features,
            response_tuple,
            self.base_library,
            prevalence.base_flat,
        )
        pathways = evaluate_compiled_model(
            self.artifact,
            state.chart_features,
            response_tuple,
            self.assignment_scope,
        )
        detailed = score_detailed_symbolic(
            state.chart_features,
            pathways,
            prevalence.detailed_context,
        )
        evidence = core.evidence_rubric_bits + detailed.evidence_rubric_bits
        contradiction = core.contradiction_rubric_bits + detailed.contradiction_rubric_bits
        return ScoredState(
            state_id=state.state_id,
            net_rubric_bits=evidence - contradiction,
            evidence_rubric_bits=evidence,
            contradiction_rubric_bits=contradiction,
            detailed_support=(
                detailed.detailed_support if detailed.clusters else core.detailed_support
            ),
            core_fit=core.core_fit,
            meaningful_contradictions=(
                core.meaningful_contradictions + detailed.meaningful_contradictions
            ),
        )

    def _verify_public_runtime_chain(self) -> None:
        receipt = self.freeze_receipt
        artifact = self.artifact
        if sha256_file(self.compiled_artifact_path) != receipt.compiled_artifact.sha256:
            raise ValueError("compiled V2 bytes do not match the freeze receipt")
        if artifact.sha256() != receipt.compiled_semantic_sha256:
            raise ValueError("compiled V2 semantics do not match the freeze receipt")
        if artifact.preregistration_file_sha256 != receipt.preregistration.sha256:
            raise ValueError("compiled V2 and freeze receipt bind different preregistration bytes")
        if receipt.frozen_at_utc < artifact.preregistered_at_utc:
            raise ValueError("V2 freeze timestamp precedes preregistration")
        for label, compiled_binding, receipt_binding in (
            ("behavioral target", artifact.behavioral_target, receipt.behavioral_target),
            ("question bank", artifact.question_bank, receipt.question_bank),
            ("Model A base", artifact.model_a_base, receipt.model_a_base),
        ):
            if compiled_binding != receipt_binding:
                raise ValueError(f"compiled V2 and freeze receipt bind different {label}")
        if artifact.local_methods != receipt.local_methods:
            raise ValueError("compiled V2 and freeze receipt bind different local methods")
        expected_sources = tuple(
            ArtifactBinding(
                role=f"source_{source.source_id.removeprefix('SRC-').lower().replace('-', '_')}",
                path=source.local_path,
                sha256=source.local_sha256,
            )
            for source in artifact.source_catalog
        )
        if expected_sources != receipt.source_catalog:
            raise ValueError("compiled V2 and freeze receipt bind different source catalogs")
        if sha256_file(self.base_mapping_path) != receipt.model_a_base.sha256:
            raise ValueError("current Model A mapping bytes do not match the V2 freeze")
        # Ensure canonical serialization remains the committed semantic object.
        if sha256(canonical_bytes(artifact)).hexdigest() != artifact.sha256():
            raise AssertionError("compiled semantic hashing is inconsistent")


def _channel_sort_key(value: str) -> tuple[int, int]:
    left, right = value.split("-")
    return int(left), int(right)
