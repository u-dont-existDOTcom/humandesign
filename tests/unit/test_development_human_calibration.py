from __future__ import annotations

import hashlib
from datetime import UTC, datetime

import pytest

from hdmatch.evaluation.development_annotation_pipeline import (
    DevelopmentConsensusArtifact,
    DevelopmentConsensusPayload,
    DevelopmentConsensusUnit,
    DevelopmentPassUnitConsensusTrace,
    normalize_development_episode_responses_jsonl,
    normalize_development_series_responses_jsonl,
)
from hdmatch.evaluation.development_calibration_sampling import (
    build_development_calibration_sample,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from hdmatch.evaluation.development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from hdmatch.evaluation.development_human_calibration import (
    build_development_human_consensus_comparison,
    build_development_human_episode_first_pass,
    build_development_human_series_first_pass,
)
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


NOW = datetime(2026, 9, 6, 23, 30, tzinfo=UTC)
CORPUS_ID = "LPDC-00000000000000000001"
CORPUS_SHA = "1" * 64
CODEBOOK_SHA = "2" * 64
MANUAL_SHA = "3" * 64
HUMAN_PROMPT_SHA = "4" * 64
SEED = "5" * 64
ZERO = "0" * 64


def _segment(prefix: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=f"{prefix}-SEG-01",
        exact_text="Synthetic exact participant statement.",
        provenance_refs=("T01",),
    )


def _episode_task() -> DevelopmentEpisodeCodingTask:
    return DevelopmentEpisodeCodingTask(
        task_id="LPDT-00000000000000000001",
        corpus_id=CORPUS_ID,
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
        corpus_id=CORPUS_ID,
        corpus_sha256=CORPUS_SHA,
        series_id="SER-001",
        domain_id="P01",
        bounded_period_context="Synthetic repeated context.",
        approximate_age_life_phase="adult",
        recurrence_language="many times",
        rough_opportunity_count="at least 3",
        behavior_reportedly_recurred="Synthetic behavior recurred.",
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
        insufficient_semantics="Missing.",
        not_applicable_semantics="Absent prerequisite.",
        inclusion_criteria=("Synthetic inclusion.",),
        exclusion_criteria=("Synthetic exclusion.",),
        evidence_requirements=("Synthetic evidence.",),
        participant_review_policy="Synthetic review.",
        theory_contamination_policy="No target theory.",
        origin_status="synthetic_placeholder",
        release_notes="Synthetic only.",
    )
    payload = OntologyReleasePayload(
        ontology_id="development-human-calibration-test",
        ontology_version="v1.0",
        release_status="development",
        scope_statement="Synthetic human calibration ontology.",
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
    return build_structured_coding_procedure_v2(
        StructuredCodingProcedurePayloadV2(
            ontology_artifact_id=ontology.artifact_id,
            ontology_sha256=ontology.ontology_sha256,
            reconciled_codebook_sha256=CODEBOOK_SHA,
            coding_manual_sha256=MANUAL_SHA,
            observable_extensions=(
                ObservableProcedureExtensionV2(
                    observable_id="NBM-R01",
                    non_action_values=(),
                    other_specified_value="OS",
                ),
            ),
            created_at_utc=NOW,
        ),
        ontology,
    )


def _calibration():
    return build_development_calibration_sample(
        episode_tasks=(_episode_task(),),
        series_tasks=(_series_task(),),
        episode_sample_size=1,
        series_sample_size=1,
        seed_sha256=SEED,
        created_at_utc=NOW,
    )


def _episode_response(value: str = "R01-a") -> DevelopmentEpisodeAnnotationResponse:
    task = human_episode_calibration_tasks((_episode_task(),), _calibration())[0]
    return DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id=task.observable_ids[0],
        state="observed",
        coded_values=(value,),
        value_relation="single",
        supporting_source_segment_ids=("EP-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )


def _series_response(value: str = "R01-a") -> DevelopmentSeriesAnnotationResponse:
    task = human_series_calibration_tasks(
        (_episode_task(),),
        (_series_task(),),
        _calibration(),
    )[0]
    return DevelopmentSeriesAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id=task.observable_ids[0],
        state="observed",
        coded_values=(value,),
        value_relation="single",
        minimum_reported_occurrences=3,
        supporting_source_segment_ids=("SER-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )


def _consensus(response: DevelopmentEpisodeAnnotationResponse) -> DevelopmentConsensusArtifact:
    traces = tuple(
        DevelopmentPassUnitConsensusTrace(
            pass_id=f"PASS-{index}",
            response_sha256=str(index) * 64,
            semantic_sha256="a" * 64,
        )
        for index in (1, 2, 3)
    )
    unit = DevelopmentConsensusUnit(
        evidence_kind="episode",
        task_id=response.task_id,
        evidence_id=response.episode_id,
        observable_id=response.observable_id,
        status="unanimous",
        agreeing_pass_ids=("PASS-1", "PASS-2", "PASS-3"),
        dissenting_pass_ids=(),
        consensus_response=response,
        pass_trace=traces,
    )
    payload = DevelopmentConsensusPayload(
        evidence_kind="episode",
        validated_pass_artifact_sha256=("b" * 64, "c" * 64, "d" * 64),
        pass_ids=("PASS-1", "PASS-2", "PASS-3"),
        corpus_sha256=CORPUS_SHA,
        codebook_sha256=CODEBOOK_SHA,
        coding_procedure_sha256=_procedure(_ontology()).procedure_sha256,
        prompt_sha256="e" * 64,
        task_set_sha256="f" * 64,
        units=(unit,),
        total_units=1,
        unanimous_units=1,
        majority_units=0,
        unresolved_units=0,
    )
    digest = sha256_json(payload)
    return DevelopmentConsensusArtifact(
        artifact_id=f"LPDCN-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def test_human_episode_first_pass_is_complete_blind_and_content_addressed() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    raw = b"  " + canonical_json_bytes(_episode_response()) + b"\n"
    normalized = normalize_development_episode_responses_jsonl(raw)
    artifact = build_development_human_episode_first_pass(
        auditor_id="AUDITOR-01",
        raw_output=raw,
        normalized_output=normalized,
        calibration=_calibration(),
        episode_tasks=(_episode_task(),),
        series_tasks=(_series_task(),),
        ontology=ontology,
        procedure=procedure,
        coding_manual_sha256=MANUAL_SHA,
        human_prompt_sha256=HUMAN_PROMPT_SHA,
        created_at_utc=NOW,
    )
    assert artifact.payload.expected_unit_count == 1
    assert artifact.payload.validated_unit_count == 1
    assert artifact.payload.llm_outputs_available_before_first_pass is False
    assert artifact.payload.automated_consensus_available_before_first_pass is False
    assert artifact.payload.target_theory_blind is True
    assert artifact.payload.validation_use_forbidden is True
    assert artifact.payload.raw_output_sha256 == hashlib.sha256(raw).hexdigest()


def test_human_first_pass_rejects_missing_preselected_unit() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    with pytest.raises(ValueError, match="does not exactly cover selected units"):
        build_development_human_episode_first_pass(
            auditor_id="AUDITOR-01",
            raw_output=b"",
            normalized_output=b"",
            calibration=_calibration(),
            episode_tasks=(_episode_task(),),
            series_tasks=(_series_task(),),
            ontology=ontology,
            procedure=procedure,
            coding_manual_sha256=MANUAL_SHA,
            human_prompt_sha256=HUMAN_PROMPT_SHA,
            created_at_utc=NOW,
        )


def test_human_series_first_pass_validates_separate_series_stratum() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    raw = canonical_json_bytes(_series_response()) + b"\n"
    normalized = normalize_development_series_responses_jsonl(raw)
    artifact = build_development_human_series_first_pass(
        auditor_id="AUDITOR-01",
        raw_output=raw,
        normalized_output=normalized,
        calibration=_calibration(),
        episode_tasks=(_episode_task(),),
        series_tasks=(_series_task(),),
        ontology=ontology,
        procedure=procedure,
        coding_manual_sha256=MANUAL_SHA,
        human_prompt_sha256=HUMAN_PROMPT_SHA,
        created_at_utc=NOW,
    )
    assert artifact.payload.evidence_kind == "series"
    assert artifact.payload.expected_unit_count == 1


def test_later_consensus_comparison_reports_agreement_without_pass_fail_threshold() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    human_response = _episode_response("R01-a")
    raw = canonical_json_bytes(human_response) + b"\n"
    normalized = normalize_development_episode_responses_jsonl(raw)
    first_pass = build_development_human_episode_first_pass(
        auditor_id="AUDITOR-01",
        raw_output=raw,
        normalized_output=normalized,
        calibration=_calibration(),
        episode_tasks=(_episode_task(),),
        series_tasks=(_series_task(),),
        ontology=ontology,
        procedure=procedure,
        coding_manual_sha256=MANUAL_SHA,
        human_prompt_sha256=HUMAN_PROMPT_SHA,
        created_at_utc=NOW,
    )
    comparison = build_development_human_consensus_comparison(
        human_first_pass=first_pass,
        human_normalized_output=normalized,
        consensus=_consensus(_episode_response("R01-a")),
        created_at_utc=NOW,
    )
    assert comparison.payload.sampled_units == 1
    assert comparison.payload.state_agreement_rate_on_resolved_consensus == 1.0
    assert comparison.payload.value_agreement_rate_when_both_observed == 1.0
    assert comparison.payload.no_pass_fail_threshold_applied is True
    assert comparison.payload.calibration_does_not_establish_construct_validity is True
