from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.neutral_measurement import (
    ObservableDefinition,
    OntologyReleasePayload,
    build_ontology_release,
    freeze_evidence_index_from_artifact,
)
from hdmatch.evaluation.structured_annotation_v2 import (
    NonActionGateAssessmentV2,
    ObservableProcedureExtensionV2,
    StructuredAnnotationResponseV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_annotation_tasks_v2,
    build_structured_coding_procedure_v2,
    load_structured_annotation_responses_jsonl_v2,
    load_structured_coding_procedure_v2,
    structured_annotation_response_errors,
    structured_annotation_responses_jsonl_v2,
    write_structured_coding_procedure_v2,
)
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 4, 1, 30, tzinfo=UTC)


def _observable() -> ObservableDefinition:
    return ObservableDefinition(
        observable_id="STRUCTURED_ALPHA",
        label="STRUCTURED SOFTWARE TEST",
        definition="Software-only fixture with no substantive behavioral interpretation.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_START", "VALUE_STOP", "VALUE_NO_ACTION"),
        insufficient_semantics="Use when structural fixture evidence is insufficient.",
        not_applicable_semantics="Use when structural fixture prerequisite is absent.",
        inclusion_criteria=("Structural fixture inclusion.",),
        exclusion_criteria=("Structural fixture exclusion.",),
        evidence_requirements=("One structural source turn.",),
        participant_review_policy="Structural test only.",
        theory_contamination_policy="No target theory in structural fixture.",
        origin_status="project_specific",
        release_notes="STRUCTURAL TEST ONLY.",
    )


def _ontology():
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id="structured-annotation-v2-test",
            ontology_version="2026-09-04",
            release_status="development",
            scope_statement="STRUCTURAL SOFTWARE TEST ONLY.",
            observables=(_observable(),),
            coding_procedure_id="legacy-procedure-for-task-builder",
            coding_procedure_sha256="1" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="2" * 64,
            theory_contamination_policy_id="structural-theory-v1",
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
                    observable_id="STRUCTURED_ALPHA",
                    non_action_values=("VALUE_NO_ACTION",),
                ),
            ),
            created_at_utc=NOW,
        ),
        ontology,
    )


def _freeze_artifact() -> dict[str, object]:
    turn = {"turn_id": "TURN-A", "role": "user", "text": "STRUCTURAL SOURCE"}
    episode = {
        "episode_id": "EP-A",
        "title": "Structural episode",
        "narrative": "Structural narrative.",
        "source_turn_ids": ["TURN-A"],
        "input_modality": "typed",
        "participant_revision": False,
    }
    source = {
        "approved_episodes": [episode],
        "approved_episode_sha256": {"EP-A": sha256_json(episode)},
        "participant_source_turns": [turn],
        "participant_source_turn_sha256": {"TURN-A": sha256_json(turn)},
    }
    payload = {
        "schema_version": "life-patterns-behavioral-freeze-payload-v1",
        "session_id": "LP-STRUCTURED-V2-TEST",
        "behavioral_source": source,
    }
    digest = sha256_json(payload)
    return {
        "schema_version": "life-patterns-behavioral-freeze-artifact-v1",
        "freeze_id": f"BPF-{digest[:20].upper()}",
        "freeze_sha256": digest,
        "payload": payload,
    }


def _response(task, procedure, **overrides):
    values = {
        "task_id": task.task_id,
        "freeze_id": task.freeze_id,
        "freeze_sha256": task.freeze_sha256,
        "ontology_artifact_id": task.ontology_artifact_id,
        "ontology_sha256": task.ontology_sha256,
        "procedure_id": procedure.procedure_id,
        "procedure_sha256": procedure.procedure_sha256,
        "episode_id": task.episode_id,
        "observable_id": "STRUCTURED_ALPHA",
        "state": "observed",
        "coded_values": ("VALUE_START",),
        "value_relation": "single",
        "supporting_source_turn_ids": ("TURN-A",),
    }
    values.update(overrides)
    return StructuredAnnotationResponseV2(**values)


def test_ordered_sequence_is_preserved_without_mislabeling_as_mixed() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    freeze = _freeze_artifact()
    evidence = freeze_evidence_index_from_artifact(freeze)
    task = build_structured_annotation_tasks_v2(freeze, ontology, procedure)[0]
    response = _response(
        task,
        procedure,
        coded_values=("VALUE_START", "VALUE_STOP"),
        value_relation="ordered_sequence",
    )
    assert response.state == "observed"
    assert response.coded_values == ("VALUE_START", "VALUE_STOP")
    assert structured_annotation_response_errors(
        response,
        task=task,
        evidence=evidence,
        ontology=ontology,
        procedure=procedure,
    ) == ()


def test_non_action_registry_requires_all_four_prerequisites() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    freeze = _freeze_artifact()
    evidence = freeze_evidence_index_from_artifact(freeze)
    task = build_structured_annotation_tasks_v2(freeze, ontology, procedure)[0]

    with pytest.raises(ValueError, match="all four gate elements"):
        _response(
            task,
            procedure,
            coded_values=("VALUE_NO_ACTION",),
            asserts_non_action=True,
            non_action_gate=NonActionGateAssessmentV2(
                awareness="established",
                opportunity="established",
                feasibility="unclear",
                established_non_action="established",
            ),
        )

    gate = NonActionGateAssessmentV2(
        awareness="established",
        opportunity="established",
        feasibility="established",
        established_non_action="established",
    )
    response = _response(
        task,
        procedure,
        coded_values=("VALUE_NO_ACTION",),
        asserts_non_action=True,
        non_action_gate=gate,
    )
    assert structured_annotation_response_errors(
        response,
        task=task,
        evidence=evidence,
        ontology=ontology,
        procedure=procedure,
    ) == ()

    false_flag = _response(
        task,
        procedure,
        coded_values=("VALUE_NO_ACTION",),
        asserts_non_action=False,
        non_action_gate=gate,
    )
    assert "structured annotation non-action flag disagrees with frozen procedure registry" in (
        structured_annotation_response_errors(
            false_flag,
            task=task,
            evidence=evidence,
            ontology=ontology,
            procedure=procedure,
        )
    )


def test_influence_and_source_provenance_are_explicit_and_task_bound() -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    freeze = _freeze_artifact()
    evidence = freeze_evidence_index_from_artifact(freeze)
    task = build_structured_annotation_tasks_v2(freeze, ontology, procedure)[0]
    response = _response(
        task,
        procedure,
        influence_relation="temporal_precedence_only",
        influence_source_turn_ids=("TURN-A",),
    )
    assert structured_annotation_response_errors(
        response,
        task=task,
        evidence=evidence,
        ontology=ontology,
        procedure=procedure,
    ) == ()

    outside = response.model_copy(update={"influence_source_turn_ids": ("TURN-OUTSIDE",)})
    errors = structured_annotation_response_errors(
        outside,
        task=task,
        evidence=evidence,
        ontology=ontology,
        procedure=procedure,
    )
    assert "structured annotation cites source turns outside supplied task" in errors


def test_v2_procedure_and_jsonl_are_content_addressed_and_canonical(tmp_path: Path) -> None:
    ontology = _ontology()
    procedure = _procedure(ontology)
    path = tmp_path / "procedure-v2.json"
    write_structured_coding_procedure_v2(path, procedure, ontology)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_structured_coding_procedure_v2(path, ontology) == procedure
    with pytest.raises(FileExistsError):
        write_structured_coding_procedure_v2(path, procedure, ontology)

    freeze = _freeze_artifact()
    task = build_structured_annotation_tasks_v2(freeze, ontology, procedure)[0]
    response = _response(task, procedure)
    encoded = structured_annotation_responses_jsonl_v2((response,))
    assert encoded.endswith(b"\n")
    assert load_structured_annotation_responses_jsonl_v2(encoded) == (response,)
