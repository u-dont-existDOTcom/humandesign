from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_episode_evidence import (
    DevelopmentEpisodeAnnotationResponse,
    development_episode_response_errors,
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
    NonActionGateAssessmentV2,
    ObservableProcedureExtensionV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)
from hdmatch.experiments.canonical import sha256_json


NOW = datetime(2026, 9, 6, 22, 0, tzinfo=UTC)
ZERO = "0" * 64


def _task() -> DevelopmentEpisodeCodingTask:
    return DevelopmentEpisodeCodingTask(
        task_id="LPDT-00000000000000000001",
        corpus_id="LPDC-00000000000000000001",
        corpus_sha256="1" * 64,
        episode_id="EP-001",
        domain_id="P01",
        approximate_age_life_phase="adult",
        episode_narrative="Transfer summary only.",
        exact_source_segments=(
            DevelopmentSourceSegment(
                segment_id="EP-001-SEG-01",
                exact_text="I accepted the invitation after thinking about it.",
                provenance_refs=("T01",),
            ),
        ),
        source_completeness="partial_exact_segments_plus_transfer_summary",
        observable_ids=("NBM-R01",),
        participant_theory_exposure="prior_exposure_possible",
    )


def _ontology() -> OntologyReleaseArtifact:
    observable = ObservableDefinition(
        observable_id="NBM-R01",
        label="Synthetic optional response",
        definition="Synthetic development observable.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("R01-a", "R01-h", "OS"),
        insufficient_semantics="Missing required information.",
        not_applicable_semantics="Prerequisite absent.",
        inclusion_criteria=("Synthetic prerequisite.",),
        exclusion_criteria=("Synthetic exclusion.",),
        evidence_requirements=("Synthetic evidence requirement.",),
        participant_review_policy="Synthetic participant review.",
        theory_contamination_policy="No target-model information.",
        origin_status="synthetic_placeholder",
        release_notes="Synthetic test only.",
    )
    payload = OntologyReleasePayload(
        ontology_id="synthetic-development-episode-test",
        ontology_version="v1.0",
        release_status="development",
        scope_statement="Synthetic development episode test ontology.",
        observables=(observable,),
        coding_procedure_id="synthetic-procedure",
        coding_procedure_sha256=ZERO,
        aggregation_policy_id="synthetic-aggregation",
        aggregation_policy_sha256=ZERO,
        theory_contamination_policy_id="synthetic-theory-policy",
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
                non_action_values=("R01-h",),
                other_specified_value="OS",
            ),
        ),
        created_at_utc=NOW,
    )
    return build_structured_coding_procedure_v2(payload, ontology)


def test_observed_episode_requires_exact_source_segment_support() -> None:
    task = _task()
    with pytest.raises(ValidationError, match="exact source-segment support"):
        DevelopmentEpisodeAnnotationResponse(
            task_id=task.task_id,
            corpus_id=task.corpus_id,
            corpus_sha256=task.corpus_sha256,
            episode_id=task.episode_id,
            observable_id="NBM-R01",
            state="observed",
            coded_values=("R01-a",),
            value_relation="single",
            theory_exposure="prior_exposure_possible",
        )


def test_valid_observed_episode_binds_task_source_ontology_and_procedure() -> None:
    task = _task()
    ontology = _ontology()
    procedure = _procedure(ontology)
    response = DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        supporting_source_segment_ids=("EP-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )
    assert development_episode_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    ) == ()
    assert response.transfer_summary_is_not_primary_source is True
    assert response.validation_use_forbidden is True


def test_response_rejects_source_segment_outside_task() -> None:
    task = _task()
    ontology = _ontology()
    procedure = _procedure(ontology)
    response = DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        supporting_source_segment_ids=("NOT-IN-TASK",),
    )
    errors = development_episode_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    )
    assert "development episode response cites supporting source outside supplied task" in errors


def test_non_action_requires_registry_match_and_full_gate() -> None:
    task = _task()
    ontology = _ontology()
    procedure = _procedure(ontology)
    gate = NonActionGateAssessmentV2(
        awareness="established",
        opportunity="established",
        feasibility="established",
        established_non_action="established",
    )
    response = DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-h",),
        value_relation="single",
        asserts_non_action=True,
        non_action_gate=gate,
        supporting_source_segment_ids=("EP-001-SEG-01",),
    )
    assert development_episode_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    ) == ()


def test_other_specified_contract_is_checked_against_procedure() -> None:
    task = _task()
    ontology = _ontology()
    procedure = _procedure(ontology)
    response = DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("OS",),
        value_relation="single",
        other_specified_description="Concrete synthetic behavior not represented by listed values.",
        supporting_source_segment_ids=("EP-001-SEG-01",),
    )
    assert development_episode_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    ) == ()


def test_influence_relation_requires_exact_source_provenance() -> None:
    task = _task()
    with pytest.raises(ValidationError, match="requires exact source-segment provenance"):
        DevelopmentEpisodeAnnotationResponse(
            task_id=task.task_id,
            corpus_id=task.corpus_id,
            corpus_sha256=task.corpus_sha256,
            episode_id=task.episode_id,
            observable_id="NBM-R01",
            state="insufficient",
            influence_relation="narrator_explicit_influence",
        )


def test_development_response_has_no_canonical_freeze_fields() -> None:
    fields = set(DevelopmentEpisodeAnnotationResponse.model_fields)
    assert "freeze_id" not in fields
    assert "freeze_sha256" not in fields
    assert "ontology_artifact_id" not in fields
    assert "procedure_id" not in fields
    assert "corpus_id" in fields
    assert "development_only" in fields
