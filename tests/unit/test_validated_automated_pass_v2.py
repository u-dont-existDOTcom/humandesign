from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

import pytest

from hdmatch.evaluation.automated_annotation_calibration import AutomatedCodingPassReceipt
from hdmatch.evaluation.neutral_measurement import (
    FreezeEvidenceIndex,
    ObservableDefinition,
    OntologyReleasePayload,
    build_ontology_release,
)
from hdmatch.evaluation.structured_annotation_normalization import (
    normalize_structured_annotation_responses_jsonl_v2,
)
from hdmatch.evaluation.structured_annotation_v2 import (
    ObservableProcedureExtensionV2,
    StructuredAnnotationResponseV2,
    StructuredAnnotationTaskV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)
from hdmatch.evaluation.validated_automated_pass_v2 import (
    build_validated_structured_automated_pass_v2,
    validated_structured_automated_pass_integrity_errors,
)

NOW = datetime(2026, 9, 4, 13, 10, tzinfo=UTC)


def _ontology():
    observable = ObservableDefinition(
        observable_id="STRUCTURAL_PASS_ALPHA",
        label="STRUCTURAL PASS TEST",
        definition="Software fixture only.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO", "OS"),
        insufficient_semantics="Structural insufficient.",
        not_applicable_semantics="Structural not applicable.",
        inclusion_criteria=("Structural inclusion.",),
        exclusion_criteria=("Structural exclusion.",),
        evidence_requirements=("Structural evidence.",),
        participant_review_policy="Structural test only.",
        theory_contamination_policy="No target theory in fixture.",
        origin_status="project_specific",
        release_notes="STRUCTURAL TEST ONLY.",
    )
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id="validated-automated-pass-v2-test",
            ontology_version="v1.0.0",
            release_status="development",
            scope_statement="STRUCTURAL SOFTWARE TEST ONLY.",
            observables=(observable,),
            coding_procedure_id="structural-manual",
            coding_procedure_sha256="1" * 64,
            aggregation_policy_id="structural-aggregation",
            aggregation_policy_sha256="2" * 64,
            theory_contamination_policy_id="structural-theory",
            theory_contamination_policy_sha256="3" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=NOW,
            synthetic_fixture_only=False,
        )
    )


def _procedure(ontology):
    return build_structured_coding_procedure_v2(
        StructuredCodingProcedurePayloadV2(
            ontology_artifact_id=ontology.artifact_id,
            ontology_sha256=ontology.ontology_sha256,
            reconciled_codebook_sha256="4" * 64,
            coding_manual_sha256="5" * 64,
            observable_extensions=(
                ObservableProcedureExtensionV2(
                    observable_id="STRUCTURAL_PASS_ALPHA",
                    other_specified_value="OS",
                ),
            ),
            created_at_utc=NOW,
        ),
        ontology,
    )


def _evidence() -> FreezeEvidenceIndex:
    return FreezeEvidenceIndex(
        session_id="LP-VALIDATED-PASS-V2",
        freeze_id="BPF-0123456789ABCDEF0123",
        freeze_sha256="6" * 64,
        episode_sha256={"EP-A": "7" * 64},
        source_turn_sha256={"TURN-A": "8" * 64},
        episode_source_turn_ids={"EP-A": ("TURN-A",)},
        episode_input_modality={"EP-A": "typed"},
        participant_revised_episode={"EP-A": False},
    )


def _task(ontology, procedure) -> StructuredAnnotationTaskV2:
    evidence = _evidence()
    return StructuredAnnotationTaskV2(
        task_id="TASK-A",
        freeze_id=evidence.freeze_id,
        freeze_sha256=evidence.freeze_sha256,
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        procedure_id=procedure.procedure_id,
        procedure_sha256=procedure.procedure_sha256,
        episode_id="EP-A",
        episode_title="Structural episode",
        episode_narrative="Structural narrative.",
        source_turns=({"turn_id": "TURN-A", "text": "STRUCTURAL SOURCE"},),
        observable_ids=("STRUCTURAL_PASS_ALPHA",),
    )


def _response(task, *, value: str = "VALUE_ONE") -> StructuredAnnotationResponseV2:
    return StructuredAnnotationResponseV2(
        task_id=task.task_id,
        freeze_id=task.freeze_id,
        freeze_sha256=task.freeze_sha256,
        ontology_artifact_id=task.ontology_artifact_id,
        ontology_sha256=task.ontology_sha256,
        procedure_id=task.procedure_id,
        procedure_sha256=task.procedure_sha256,
        episode_id=task.episode_id,
        observable_id="STRUCTURAL_PASS_ALPHA",
        state="observed",
        coded_values=(value,),
        value_relation="single",
        supporting_source_turn_ids=("TURN-A",),
    )


def _raw(response: StructuredAnnotationResponseV2) -> bytes:
    return (json.dumps(response.model_dump(mode="json"), indent=2) + "\n").encode()


def _pass(procedure, normalized: bytes) -> AutomatedCodingPassReceipt:
    return AutomatedCodingPassReceipt(
        pass_id="PASS-ONE",
        corpus_sha256="9" * 64,
        codebook_sha256=procedure.payload.reconciled_codebook_sha256,
        coding_procedure_sha256=procedure.procedure_sha256,
        prompt_sha256="a" * 64,
        model_identity="STRUCTURAL-MODEL",
        model_version="STRUCTURAL-VERSION",
        output_sha256=hashlib.sha256(normalized).hexdigest(),
        created_at_utc=NOW,
    )


def test_complete_pass_binds_raw_normalized_tasks_and_response_structure() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    task = _task(ontology, procedure)
    raw = _raw(_response(task))
    normalized = normalize_structured_annotation_responses_jsonl_v2(raw)
    artifact = build_validated_structured_automated_pass_v2(
        raw_output=raw,
        normalized_output=normalized,
        automated_pass=_pass(procedure, normalized),
        tasks=(task,),
        evidence=_evidence(),
        ontology=ontology,
        procedure=procedure,
        expected_corpus_sha256="9" * 64,
        normalization_implementation_sha256="b" * 64,
        created_at_utc=NOW,
    )
    assert artifact.payload.expected_unit_count == 1
    assert artifact.payload.validated_unit_count == 1
    assert artifact.payload.raw_output_sha256 == hashlib.sha256(raw).hexdigest()
    assert validated_structured_automated_pass_integrity_errors(artifact) == ()


def test_missing_unit_and_out_of_codebook_value_fail_closed() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    task = _task(ontology, procedure)

    empty = b""
    with pytest.raises(ValueError, match="missing frozen annotation units"):
        build_validated_structured_automated_pass_v2(
            raw_output=empty,
            normalized_output=empty,
            automated_pass=_pass(procedure, empty),
            tasks=(task,),
            evidence=_evidence(),
            ontology=ontology,
            procedure=procedure,
            expected_corpus_sha256="9" * 64,
            normalization_implementation_sha256="b" * 64,
            created_at_utc=NOW,
        )

    raw = _raw(_response(task, value="VALUE_OUTSIDE_CODEBOOK"))
    normalized = normalize_structured_annotation_responses_jsonl_v2(raw)
    with pytest.raises(ValueError, match="value outside codebook"):
        build_validated_structured_automated_pass_v2(
            raw_output=raw,
            normalized_output=normalized,
            automated_pass=_pass(procedure, normalized),
            tasks=(task,),
            evidence=_evidence(),
            ontology=ontology,
            procedure=procedure,
            expected_corpus_sha256="9" * 64,
            normalization_implementation_sha256="b" * 64,
            created_at_utc=NOW,
        )


def test_canonical_output_must_be_exact_normalization_of_raw_output() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    task = _task(ontology, procedure)
    raw = _raw(_response(task))
    normalized = normalize_structured_annotation_responses_jsonl_v2(raw)
    altered = normalized + b"\n"
    with pytest.raises(ValueError, match="not deterministic normalization"):
        build_validated_structured_automated_pass_v2(
            raw_output=raw,
            normalized_output=altered,
            automated_pass=_pass(procedure, altered),
            tasks=(task,),
            evidence=_evidence(),
            ontology=ontology,
            procedure=procedure,
            expected_corpus_sha256="9" * 64,
            normalization_implementation_sha256="b" * 64,
            created_at_utc=NOW,
        )
