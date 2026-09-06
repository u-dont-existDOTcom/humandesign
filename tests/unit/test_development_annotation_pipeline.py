from __future__ import annotations

import hashlib
from datetime import UTC, datetime

import pytest

from hdmatch.evaluation.automated_annotation_calibration import AutomatedCodingPassReceipt
from hdmatch.evaluation.development_annotation_pipeline import (
    build_development_consensus,
    build_validated_development_episode_pass,
    build_validated_development_series_pass,
    normalize_development_episode_responses_jsonl,
    normalize_development_series_responses_jsonl,
)
from hdmatch.evaluation.development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from hdmatch.evaluation.development_series_evidence import (
    DevelopmentSeriesAnnotationResponse,
    DevelopmentSeriesCodingTask,
)
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentSourceSegment,
)
from hdmatch.evaluation.neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
)
from hdmatch.evaluation.structured_annotation_v2 import (
    ObservableProcedureExtensionV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json


NOW = datetime(2026, 9, 6, 22, 30, tzinfo=UTC)
PROMPT_SHA = "4" * 64
NORMALIZER_SHA = "5" * 64
CORPUS_SHA = "1" * 64
ZERO = "0" * 64


def _segment(prefix: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=f"{prefix}-SEG-01",
        exact_text="Synthetic exact participant evidence.",
        provenance_refs=("T01",),
    )


def _episode_task() -> DevelopmentEpisodeCodingTask:
    return DevelopmentEpisodeCodingTask(
        task_id="LPDT-00000000000000000001",
        corpus_id="LPDC-00000000000000000001",
        corpus_sha256=CORPUS_SHA,
        episode_id="EP-001",
        domain_id="P01",
        approximate_age_life_phase="adult",
        episode_narrative="Synthetic transfer summary.",
        exact_source_segments=(_segment("EP-001"),),
        source_completeness="partial_exact_segments_plus_transfer_summary",
        observable_ids=("NBM-R01",),
        participant_theory_exposure="prior_exposure_possible",
    )


def _series_task() -> DevelopmentSeriesCodingTask:
    return DevelopmentSeriesCodingTask(
        task_id="LPST-00000000000000000001",
        corpus_id="LPDC-00000000000000000001",
        corpus_sha256=CORPUS_SHA,
        series_id="SER-001",
        domain_id="P01",
        bounded_period_context="Synthetic repeated period.",
        approximate_age_life_phase="adult",
        recurrence_language="many times",
        rough_opportunity_count="at least 3",
        behavior_reportedly_recurred="Synthetic repeated behavior.",
        exact_source_segments=(_segment("SER-001"),),
        observable_ids=("NBM-R01",),
        participant_theory_exposure="prior_exposure_possible",
    )


def _ontology() -> OntologyReleaseArtifact:
    observable = ObservableDefinition(
        observable_id="NBM-R01",
        label="Synthetic observable",
        definition="Synthetic definition.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("R01-a", "R01-b", "OS"),
        insufficient_semantics="Missing information.",
        not_applicable_semantics="Prerequisite absent.",
        inclusion_criteria=("Synthetic inclusion.",),
        exclusion_criteria=("Synthetic exclusion.",),
        evidence_requirements=("Synthetic evidence.",),
        participant_review_policy="Synthetic review.",
        theory_contamination_policy="No target information.",
        origin_status="synthetic_placeholder",
        release_notes="Synthetic only.",
    )
    payload = OntologyReleasePayload(
        ontology_id="development-pipeline-test",
        ontology_version="v1",
        release_status="development",
        scope_statement="Synthetic pipeline test.",
        observables=(observable,),
        coding_procedure_id="synthetic",
        coding_procedure_sha256=ZERO,
        aggregation_policy_id="synthetic",
        aggregation_policy_sha256=ZERO,
        theory_contamination_policy_id="synthetic",
        theory_contamination_policy_sha256=ZERO,
        source_commit="abcdef0",
        released_at_utc=NOW,
        synthetic_fixture_only=True,
    )
    digest = sha256_json(payload)
    return OntologyReleaseArtifact(
        artifact_id=f"LPO-{digest[:20].upper()}",
        ontology_sha256=digest,
        payload=payload,
    )


def _procedure(ontology: OntologyReleaseArtifact):
    payload = StructuredCodingProcedurePayloadV2(
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        reconciled_codebook_sha256="2" * 64,
        coding_manual_sha256="3" * 64,
        observable_extensions=(
            ObservableProcedureExtensionV2(
                observable_id="NBM-R01",
                non_action_values=(),
                other_specified_value="OS",
            ),
        ),
        created_at_utc=NOW,
    )
    return build_structured_coding_procedure_v2(payload, ontology)


def _episode_response(value: str = "R01-a") -> DevelopmentEpisodeAnnotationResponse:
    task = _episode_task()
    return DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=(value,),
        value_relation="single",
        supporting_source_segment_ids=("EP-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )


def _series_response(value: str = "R01-a") -> DevelopmentSeriesAnnotationResponse:
    task = _series_task()
    return DevelopmentSeriesAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=(value,),
        value_relation="single",
        minimum_reported_occurrences=3,
        supporting_source_segment_ids=("SER-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )


def _receipt(
    pass_id: str,
    normalized: bytes,
    procedure_sha: str,
    *,
    prompt_sha: str = PROMPT_SHA,
) -> AutomatedCodingPassReceipt:
    return AutomatedCodingPassReceipt(
        pass_id=pass_id,
        corpus_sha256=CORPUS_SHA,
        codebook_sha256="2" * 64,
        coding_procedure_sha256=procedure_sha,
        prompt_sha256=prompt_sha,
        model_identity="SYNTHETIC-CODER",
        model_version="test",
        output_sha256=hashlib.sha256(normalized).hexdigest(),
        created_at_utc=NOW,
    )


def _validated_episode(pass_id: str, value: str = "R01-a"):
    ontology = _ontology()
    procedure = _procedure(ontology)
    raw = b"\n  " + canonical_json_bytes(_episode_response(value)) + b"\n"
    normalized = normalize_development_episode_responses_jsonl(raw)
    artifact = build_validated_development_episode_pass(
        raw_output=raw,
        normalized_output=normalized,
        automated_pass=_receipt(pass_id, normalized, procedure.procedure_sha256),
        tasks=(_episode_task(),),
        ontology=ontology,
        procedure=procedure,
        expected_prompt_sha256=PROMPT_SHA,
        normalization_implementation_sha256=NORMALIZER_SHA,
        created_at_utc=NOW,
    )
    return artifact, normalized


def _validated_series(pass_id: str, value: str = "R01-a"):
    ontology = _ontology()
    procedure = _procedure(ontology)
    raw = canonical_json_bytes(_series_response(value)) + b"\n"
    normalized = normalize_development_series_responses_jsonl(raw)
    artifact = build_validated_development_series_pass(
        raw_output=raw,
        normalized_output=normalized,
        automated_pass=_receipt(pass_id, normalized, procedure.procedure_sha256),
        tasks=(_series_task(),),
        ontology=ontology,
        procedure=procedure,
        expected_prompt_sha256=PROMPT_SHA,
        normalization_implementation_sha256=NORMALIZER_SHA,
        created_at_utc=NOW,
    )
    return artifact, normalized


def test_normalization_accepts_whitespace_separated_objects_and_is_canonical() -> None:
    raw = b"  " + canonical_json_bytes(_episode_response()) + b"\n\n"
    normalized = normalize_development_episode_responses_jsonl(raw)
    assert normalized == canonical_json_bytes(_episode_response()) + b"\n"


def test_validated_episode_pass_requires_complete_exact_task_coverage() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    normalized = b""
    with pytest.raises(ValueError, match="missing units"):
        build_validated_development_episode_pass(
            raw_output=b"",
            normalized_output=normalized,
            automated_pass=_receipt("PASS-1", normalized, procedure.procedure_sha256),
            tasks=(_episode_task(),),
            ontology=ontology,
            procedure=procedure,
            expected_prompt_sha256=PROMPT_SHA,
            normalization_implementation_sha256=NORMALIZER_SHA,
            created_at_utc=NOW,
        )


def test_validated_pass_rejects_wrong_transport_prompt_binding() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    raw = canonical_json_bytes(_episode_response())
    normalized = normalize_development_episode_responses_jsonl(raw)
    with pytest.raises(ValueError, match="transport prompt"):
        build_validated_development_episode_pass(
            raw_output=raw,
            normalized_output=normalized,
            automated_pass=_receipt(
                "PASS-1",
                normalized,
                procedure.procedure_sha256,
                prompt_sha="9" * 64,
            ),
            tasks=(_episode_task(),),
            ontology=ontology,
            procedure=procedure,
            expected_prompt_sha256=PROMPT_SHA,
            normalization_implementation_sha256=NORMALIZER_SHA,
            created_at_utc=NOW,
        )


def test_three_episode_passes_produce_strict_majority_consensus() -> None:
    passes = (
        _validated_episode("PASS-A", "R01-a"),
        _validated_episode("PASS-B", "R01-a"),
        _validated_episode("PASS-C", "R01-b"),
    )
    consensus = build_development_consensus(passes)
    assert consensus.payload.evidence_kind == "episode"
    assert consensus.payload.total_units == 1
    assert consensus.payload.majority_units == 1
    assert consensus.payload.unresolved_units == 0
    unit = consensus.payload.units[0]
    assert unit.status == "majority"
    assert unit.agreeing_pass_ids == ("PASS-A", "PASS-B")
    assert unit.dissenting_pass_ids == ("PASS-C",)
    assert unit.consensus_response is not None
    assert unit.consensus_response.coded_values == ("R01-a",)
    assert consensus.payload.self_consistency_does_not_establish_correctness is True
    assert consensus.payload.validation_use_forbidden is True


def test_consensus_requires_at_least_three_validated_passes() -> None:
    with pytest.raises(ValueError, match="at least three"):
        build_development_consensus(
            (
                _validated_episode("PASS-A"),
                _validated_episode("PASS-B"),
            )
        )


def test_episode_and_series_passes_cannot_be_pooled() -> None:
    with pytest.raises(ValueError, match="cannot be pooled"):
        build_development_consensus(
            (
                _validated_episode("PASS-A"),
                _validated_episode("PASS-B"),
                _validated_series("PASS-C"),
            )
        )


def test_three_series_passes_can_form_separate_consensus() -> None:
    consensus = build_development_consensus(
        (
            _validated_series("PASS-A"),
            _validated_series("PASS-B"),
            _validated_series("PASS-C"),
        )
    )
    assert consensus.payload.evidence_kind == "series"
    assert consensus.payload.unanimous_units == 1
    unit = consensus.payload.units[0]
    assert unit.consensus_response is not None
    assert isinstance(unit.consensus_response, DevelopmentSeriesAnnotationResponse)
    assert unit.consensus_response.minimum_reported_occurrences == 3
