from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.annotation_exchange import (
    AnnotationResponse,
    annotation_responses_jsonl,
    annotation_tasks_jsonl,
    coded_record_from_annotation_response,
    load_annotation_responses_jsonl,
)
from hdmatch.evaluation.neutral_measurement import (
    CodedEpisodeRecord,
    CoderIdentity,
    CodingRunPayload,
    ConfusionCell,
    ExternalConceptReference,
    HumanContentAuthorityReceipt,
    ObservableDefinition,
    ObservableReliabilityResult,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
    ReliabilityReportPayload,
    aggregate_person_observables,
    build_annotation_tasks,
    build_coding_run_artifact,
    build_ontology_release,
    build_reliability_report,
    coding_run_artifact_integrity_errors,
    freeze_evidence_index_from_artifact,
    load_coding_run_artifact,
    load_ontology_release,
    load_reliability_report,
    ontology_successor_errors,
    reliability_report_integrity_errors,
    write_coding_run_artifact,
    write_ontology_release,
    write_reliability_report,
)
from hdmatch.experiments.canonical import sha256_json


def _synthetic_observable(
    observable_id: str = "OBSERVABLE_ALPHA",
    *,
    definition: str = "Synthetic observable definition with no substantive behavioral meaning.",
    supersedes: str | None = None,
) -> ObservableDefinition:
    return ObservableDefinition(
        observable_id=observable_id,
        label="Synthetic placeholder",
        definition=definition,
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO"),
        insufficient_semantics="Use when the synthetic source does not support a code.",
        not_applicable_semantics="Use when the synthetic observable does not apply to the fixture.",
        inclusion_criteria=("Synthetic inclusion criterion only.",),
        exclusion_criteria=("Synthetic exclusion criterion only.",),
        evidence_requirements=("At least one synthetic source-turn reference for informative codes.",),
        positive_examples=("SYNTHETIC_POSITIVE_EXAMPLE",),
        negative_or_near_miss_examples=("SYNTHETIC_NEAR_MISS",),
        ambiguity_examples=("SYNTHETIC_AMBIGUITY",),
        participant_review_policy="Synthetic fixture policy only.",
        theory_contamination_policy="No theory content exists in this synthetic fixture.",
        external_references=(),
        origin_status="synthetic_placeholder",
        supersedes_observable_id=supersedes,
        release_notes="SYNTHETIC FIXTURE ONLY; no construct authority.",
    )


def _synthetic_ontology(
    *,
    version: str = "2026-09-03",
    observables: tuple[ObservableDefinition, ...] | None = None,
) -> OntologyReleaseArtifact:
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id="life-patterns-neutral-synthetic-test",
            ontology_version=version,
            release_status="development",
            scope_statement="SYNTHETIC SOFTWARE FIXTURE ONLY; no substantive construct content.",
            observables=observables or (_synthetic_observable(),),
            coding_procedure_id="synthetic-coding-procedure-v1",
            coding_procedure_sha256="1" * 64,
            aggregation_policy_id="synthetic-aggregation-v1",
            aggregation_policy_sha256="2" * 64,
            theory_contamination_policy_id="synthetic-theory-policy-v1",
            theory_contamination_policy_sha256="3" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=datetime(2026, 9, 3, 17, 45, tzinfo=UTC),
            synthetic_fixture_only=True,
        )
    )


def _structural_test_observable() -> ObservableDefinition:
    return ObservableDefinition(
        observable_id="STRUCTURAL_TEST_ALPHA",
        label="STRUCTURAL TEST PLACEHOLDER",
        definition="Software-gate fixture only; this string has no intended behavioral construct meaning.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO"),
        insufficient_semantics="Structural test insufficient state.",
        not_applicable_semantics="Structural test not-applicable state.",
        inclusion_criteria=("Structural test criterion only.",),
        exclusion_criteria=("Structural test exclusion only.",),
        evidence_requirements=("One structural test source turn.",),
        participant_review_policy="Structural software test only.",
        theory_contamination_policy="Structural software test contains no target-theory content.",
        external_references=(
            ExternalConceptReference(
                source_name="STRUCTURAL_TEST_SOURCE",
                external_id="TEST:0001",
                relation="adapted_from",
                citation="Synthetic test citation; not a scientific source.",
            ),
        ),
        origin_status="project_specific",
        validity_status="validation_candidate",
        reliability_status="human_baseline_evaluated",
        release_notes="STRUCTURAL TEST ONLY; fake authority hashes exercise software gates.",
    )


def _authorized_structural_ontology() -> OntologyReleaseArtifact:
    observable = _structural_test_observable()
    scope = "STRUCTURAL SOFTWARE TEST ONLY; not a substantive measurement instrument."
    content_sha = sha256_json(
        {
            "ontology_id": "life-patterns-structural-test",
            "ontology_version": "2026-09-03",
            "scope_statement": scope,
            "observables": (observable,),
        }
    )
    authority = HumanContentAuthorityReceipt(
        content_sha256=content_sha,
        human_authorship_receipt_sha256="a" * 64,
        exposure_adjudication_receipt_sha256="b" * 64,
        content_review_receipt_sha256="c" * 64,
        authorized_at_utc=datetime(2026, 9, 3, 17, 46, tzinfo=UTC),
    )
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id="life-patterns-structural-test",
            ontology_version="2026-09-03",
            release_status="frozen_for_validation",
            scope_statement=scope,
            observables=(observable,),
            coding_procedure_id="structural-coding-procedure-v1",
            coding_procedure_sha256="4" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="5" * 64,
            theory_contamination_policy_id="structural-theory-policy-v1",
            theory_contamination_policy_sha256="6" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=datetime(2026, 9, 3, 17, 47, tzinfo=UTC),
            synthetic_fixture_only=False,
            human_content_authority=authority,
        )
    )


def _freeze_artifact() -> dict[str, object]:
    turns = [
        {"turn_id": "TURN-A", "role": "user", "text": "SYNTHETIC SOURCE A"},
        {"turn_id": "TURN-B", "role": "user", "text": "SYNTHETIC SOURCE B"},
        {"turn_id": "TURN-C", "role": "user", "text": "SYNTHETIC SOURCE C"},
    ]
    episodes = [
        {
            "episode_id": "EP-A",
            "title": "Synthetic episode A",
            "narrative": "Synthetic narrative A.",
            "source_turn_ids": ["TURN-A"],
            "input_modality": "typed",
            "participant_revision": False,
        },
        {
            "episode_id": "EP-B",
            "title": "Synthetic episode B",
            "narrative": "Synthetic narrative B.",
            "source_turn_ids": ["TURN-B"],
            "input_modality": "voice",
            "participant_revision": True,
        },
        {
            "episode_id": "EP-C",
            "title": "Synthetic episode C",
            "narrative": "Synthetic narrative C.",
            "source_turn_ids": ["TURN-C"],
            "input_modality": "typed",
            "participant_revision": False,
        },
    ]
    source = {
        "approved_episodes": episodes,
        "approved_episode_sha256": {
            str(row["episode_id"]): sha256_json(row) for row in episodes
        },
        "participant_source_turns": turns,
        "participant_source_turn_sha256": {
            str(row["turn_id"]): sha256_json(row) for row in turns
        },
    }
    payload = {
        "schema_version": "life-patterns-behavioral-freeze-payload-v1",
        "session_id": "LP-SYNTHETIC0001",
        "behavioral_source": source,
    }
    digest = sha256_json(payload)
    return {
        "schema_version": "life-patterns-behavioral-freeze-artifact-v1",
        "freeze_id": f"BPF-{digest[:20].upper()}",
        "freeze_sha256": digest,
        "payload": payload,
    }


def _rebind_outer_freeze_identity(artifact: dict[str, object]) -> None:
    payload = artifact["payload"]
    assert isinstance(payload, dict)
    digest = sha256_json(payload)
    artifact["freeze_sha256"] = digest
    artifact["freeze_id"] = f"BPF-{digest[:20].upper()}"


def _human_coder() -> CoderIdentity:
    return CoderIdentity(
        coder_id="HUMAN-CODER-SYNTHETIC",
        coder_type="human",
        version="training-v1",
        training_receipt_sha256="7" * 64,
    )


def _observed_record(
    observable_id: str,
    episode_id: str,
    turn_id: str,
    value: str = "VALUE_ONE",
    *,
    modality: str = "typed",
    revised: bool = False,
    context: str = "CONTEXT_ALPHA",
) -> CodedEpisodeRecord:
    return CodedEpisodeRecord(
        episode_id=episode_id,
        observable_id=observable_id,
        state="observed",
        coded_value=value,
        supporting_source_turn_ids=(turn_id,),
        context_qualifiers=(context,),
        input_modality=modality,  # type: ignore[arg-type]
        theory_exposure="none_detected",
        source_episode_participant_revised=revised,
    )


def _coding_payload(
    ontology: OntologyReleaseArtifact,
    *,
    records: tuple[CodedEpisodeRecord, ...],
    run_type: str,
    coder: CoderIdentity | None = None,
) -> CodingRunPayload:
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    return CodingRunPayload(
        session_id=evidence.session_id,
        freeze_id=evidence.freeze_id,
        freeze_sha256=evidence.freeze_sha256,
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        coding_procedure_id=ontology.payload.coding_procedure_id,
        coding_procedure_sha256=ontology.payload.coding_procedure_sha256,
        coder=coder or _human_coder(),
        run_type=run_type,  # type: ignore[arg-type]
        records=records,
        created_at_utc=datetime(2026, 9, 3, 17, 50, tzinfo=UTC),
    )


def test_synthetic_ontology_is_content_addressed_read_only_and_not_validation_authority(
    tmp_path: Path,
) -> None:
    ontology = _synthetic_ontology()
    assert ontology.artifact_id == f"LPO-{ontology.ontology_sha256[:20].upper()}"
    assert ontology.payload.synthetic_fixture_only is True
    assert ontology.payload.human_content_authority is None

    path = tmp_path / "ontology.json"
    write_ontology_release(path, ontology)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_ontology_release(path) == ontology
    with pytest.raises(FileExistsError):
        write_ontology_release(path, ontology)

    with pytest.raises(ValueError, match="synthetic ontology releases cannot be frozen"):
        OntologyReleasePayload(
            **{
                **ontology.payload.model_dump(),
                "release_status": "frozen_for_validation",
            }
        )


def test_validation_authority_is_required_and_legacy_h1_binds_exact_content() -> None:
    observable = _structural_test_observable()
    base = {
        "ontology_id": "life-patterns-structural-test",
        "ontology_version": "2026-09-03",
        "release_status": "frozen_for_validation",
        "scope_statement": "STRUCTURAL SOFTWARE TEST ONLY; not substantive content.",
        "observables": (observable,),
        "coding_procedure_id": "structural-coding-procedure-v1",
        "coding_procedure_sha256": "4" * 64,
        "aggregation_policy_id": "structural-aggregation-v1",
        "aggregation_policy_sha256": "5" * 64,
        "theory_contamination_policy_id": "structural-theory-policy-v1",
        "theory_contamination_policy_sha256": "6" * 64,
        "source_commit": "abcdef0123456789abcdef0123456789abcdef01",
        "released_at_utc": datetime(2026, 9, 3, 17, 47, tzinfo=UTC),
        "synthetic_fixture_only": False,
    }
    with pytest.raises(ValueError, match="requires a validation content-authority receipt"):
        OntologyReleasePayload(**base)

    valid = _authorized_structural_ontology()
    assert valid.payload.release_status == "frozen_for_validation"
    bad_authority = HumanContentAuthorityReceipt(
        content_sha256="f" * 64,
        human_authorship_receipt_sha256="a" * 64,
        exposure_adjudication_receipt_sha256="b" * 64,
        content_review_receipt_sha256="c" * 64,
        authorized_at_utc=datetime(2026, 9, 3, 17, 46, tzinfo=UTC),
    )
    tampered = OntologyReleasePayload(**{**base, "human_content_authority": bad_authority})
    with pytest.raises(ValueError, match="does not bind this ontology content"):
        build_ontology_release(tampered)


def test_stable_observable_id_cannot_silently_change_core_meaning() -> None:
    previous = _synthetic_ontology()
    changed = _synthetic_ontology(
        version="2026-09-04",
        observables=(
            _synthetic_observable(definition="Changed synthetic core meaning under same ID."),
        ),
    )
    errors = ontology_successor_errors(previous, changed)
    assert any("changed core meaning" in error for error in errors)

    successor = _synthetic_ontology(
        version="2026-09-04",
        observables=(
            _synthetic_observable("OBSERVABLE_BETA", supersedes="OBSERVABLE_ALPHA"),
        ),
    )
    assert ontology_successor_errors(previous, successor) == ()


def test_freeze_evidence_index_binds_episode_hashes_and_provenance() -> None:
    artifact = _freeze_artifact()
    evidence = freeze_evidence_index_from_artifact(artifact)
    assert evidence.session_id == "LP-SYNTHETIC0001"
    assert evidence.episode_source_turn_ids["EP-B"] == ("TURN-B",)
    assert evidence.episode_input_modality["EP-B"] == "voice"
    assert evidence.participant_revised_episode["EP-B"] is True

    payload = artifact["payload"]
    assert isinstance(payload, dict)
    source = payload["behavioral_source"]
    assert isinstance(source, dict)
    episodes = source["approved_episodes"]
    assert isinstance(episodes, list)
    episodes[0]["narrative"] = "TAMPERED"
    with pytest.raises(ValueError, match="content-address verification"):
        freeze_evidence_index_from_artifact(artifact)

    _rebind_outer_freeze_identity(artifact)
    with pytest.raises(ValueError, match="episode hash"):
        freeze_evidence_index_from_artifact(artifact)


def test_freeze_evidence_index_binds_source_turn_hashes() -> None:
    artifact = _freeze_artifact()
    payload = artifact["payload"]
    assert isinstance(payload, dict)
    source = payload["behavioral_source"]
    assert isinstance(source, dict)
    turns = source["participant_source_turns"]
    assert isinstance(turns, list)
    turns[0]["text"] = "TAMPERED SOURCE TURN"
    with pytest.raises(ValueError, match="content-address verification"):
        freeze_evidence_index_from_artifact(artifact)

    _rebind_outer_freeze_identity(artifact)
    with pytest.raises(ValueError, match="source-turn hash"):
        freeze_evidence_index_from_artifact(artifact)


def test_synthetic_coding_run_is_valid_but_never_scoreable(tmp_path: Path) -> None:
    ontology = _synthetic_ontology()
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    record = _observed_record("OBSERVABLE_ALPHA", "EP-A", "TURN-A")
    payload = _coding_payload(
        ontology,
        records=(record,),
        run_type="synthetic_fixture",
    )
    artifact = build_coding_run_artifact(payload, ontology, evidence)
    assert artifact.scoreable_for_model_tournament is False
    assert "synthetic ontology cannot produce scoreable research evidence" in artifact.scoreability_blockers
    assert coding_run_artifact_integrity_errors(artifact, ontology, evidence) == ()

    path = tmp_path / "coding.json"
    write_coding_run_artifact(path, artifact, ontology, evidence)
    assert load_coding_run_artifact(path, ontology, evidence) == artifact


def test_structurally_authorized_human_validation_path_can_be_scoreable() -> None:
    ontology = _authorized_structural_ontology()
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    record = _observed_record("STRUCTURAL_TEST_ALPHA", "EP-A", "TURN-A")
    payload = _coding_payload(
        ontology,
        records=(record,),
        run_type="validation",
    )
    artifact = build_coding_run_artifact(payload, ontology, evidence)
    assert artifact.scoreable_for_model_tournament is True
    assert artifact.scoreability_blockers == ()


def test_automated_validation_requires_frozen_calibration_receipt() -> None:
    ontology = _authorized_structural_ontology()
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    record = _observed_record("STRUCTURAL_TEST_ALPHA", "EP-A", "TURN-A")
    coder = CoderIdentity(
        coder_id="LLM-STRUCTURAL-TEST",
        coder_type="llm",
        version="model-v1",
        implementation_sha256="8" * 64,
    )
    blocked = build_coding_run_artifact(
        _coding_payload(
            ontology,
            records=(record,),
            run_type="validation",
            coder=coder,
        ),
        ontology,
        evidence,
    )
    assert "automated coder lacks a frozen calibration/validation receipt" in blocked.scoreability_blockers

    validated_coder = CoderIdentity(
        coder_id="LLM-STRUCTURAL-TEST",
        coder_type="llm",
        version="model-v1",
        implementation_sha256="8" * 64,
        automation_validation_receipt_sha256="9" * 64,
    )
    allowed = build_coding_run_artifact(
        _coding_payload(
            ontology,
            records=(record,),
            run_type="validation",
            coder=validated_coder,
        ),
        ontology,
        evidence,
    )
    assert allowed.scoreable_for_model_tournament is True


def test_coding_fails_closed_on_unknown_turn_and_out_of_codebook_value() -> None:
    ontology = _synthetic_ontology()
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    bad_turn = _observed_record("OBSERVABLE_ALPHA", "EP-A", "TURN-NOT-FROZEN")
    bad_value = _observed_record(
        "OBSERVABLE_ALPHA",
        "EP-B",
        "TURN-B",
        value="VALUE_NOT_ALLOWED",
        modality="voice",
        revised=True,
    )
    artifact = build_coding_run_artifact(
        _coding_payload(
            ontology,
            records=(bad_turn, bad_value),
            run_type="synthetic_fixture",
        ),
        ontology,
        evidence,
    )
    assert any("outside that episode" in error for error in artifact.scoreability_blockers)
    assert any("outside its categorical codebook" in error for error in artifact.scoreability_blockers)
    assert coding_run_artifact_integrity_errors(artifact, ontology, evidence)


def test_missingness_and_distribution_preserving_aggregation_are_explicit() -> None:
    ontology = _synthetic_ontology()
    evidence = freeze_evidence_index_from_artifact(_freeze_artifact())
    records = (
        _observed_record(
            "OBSERVABLE_ALPHA",
            "EP-A",
            "TURN-A",
            value="VALUE_ONE",
            context="CONTEXT_ALPHA",
        ),
        CodedEpisodeRecord(
            episode_id="EP-B",
            observable_id="OBSERVABLE_ALPHA",
            state="mixed",
            mixed_values=("VALUE_ONE", "VALUE_TWO"),
            supporting_source_turn_ids=("TURN-B",),
            context_qualifiers=("CONTEXT_BETA",),
            input_modality="voice",
            theory_exposure="unknown",
            source_episode_participant_revised=True,
        ),
        CodedEpisodeRecord(
            episode_id="EP-C",
            observable_id="OBSERVABLE_ALPHA",
            state="insufficient",
            input_modality="typed",
            theory_exposure="unknown",
            source_episode_participant_revised=False,
        ),
    )
    artifact = build_coding_run_artifact(
        _coding_payload(
            ontology,
            records=records,
            run_type="synthetic_fixture",
        ),
        ontology,
        evidence,
    )
    summary = aggregate_person_observables(artifact)[0]
    assert summary.episode_record_count == 3
    assert summary.applicable_episode_count == 3
    assert summary.informative_episode_count == 2
    assert summary.insufficient_episode_count == 1
    assert summary.coverage_fraction == pytest.approx(2 / 3)
    assert summary.distinct_observed_values == 2
    counts = {str(row.value): row.count for row in summary.value_counts}
    assert counts == {"VALUE_ONE": 2, "VALUE_TWO": 1}
    assert summary.aggregation_semantics == "descriptive_distribution_preserving_no_trait_collapse"


def test_annotation_exchange_is_canonical_tool_neutral_and_provenance_bound() -> None:
    ontology = _synthetic_ontology()
    freeze = _freeze_artifact()
    evidence = freeze_evidence_index_from_artifact(freeze)
    tasks = build_annotation_tasks(freeze, ontology)
    assert len(tasks) == 3
    assert all(task.birth_chart_model_blind is True for task in tasks)
    assert annotation_tasks_jsonl(tasks).endswith(b"\n")

    task = next(row for row in tasks if row.episode_id == "EP-B")
    response = AnnotationResponse(
        task_id=task.task_id,
        freeze_id=task.freeze_id,
        freeze_sha256=task.freeze_sha256,
        ontology_artifact_id=task.ontology_artifact_id,
        ontology_sha256=task.ontology_sha256,
        episode_id="EP-B",
        observable_id="OBSERVABLE_ALPHA",
        state="observed",
        coded_value="VALUE_TWO",
        supporting_source_turn_ids=("TURN-B",),
        context_qualifiers=("CONTEXT_BETA",),
        theory_exposure="unknown",
    )
    encoded = annotation_responses_jsonl((response,))
    assert load_annotation_responses_jsonl(encoded) == (response,)
    record = coded_record_from_annotation_response(response, task=task, evidence=evidence)
    assert record.input_modality == "voice"
    assert record.source_episode_participant_revised is True

    bad = response.model_copy(update={"supporting_source_turn_ids": ("TURN-A",)})
    with pytest.raises(ValueError, match="outside the annotation task"):
        coded_record_from_annotation_response(bad, task=task, evidence=evidence)


def test_reliability_report_is_auditable_but_not_construct_validity(tmp_path: Path) -> None:
    ontology = _synthetic_ontology()
    result = ObservableReliabilityResult(
        observable_id="OBSERVABLE_ALPHA",
        n_double_coded=10,
        class_distribution={"VALUE_ONE": 6, "VALUE_TWO": 4},
        raw_agreement=0.8,
        krippendorff_alpha=0.7,
        gwet_ac=0.82,
        abstention_rate=0.1,
        adjudication_rate=0.2,
        confusion_matrix=(
            ConfusionCell(reference_label="VALUE_ONE", comparison_label="VALUE_ONE", count=5),
            ConfusionCell(reference_label="VALUE_ONE", comparison_label="VALUE_TWO", count=1),
            ConfusionCell(reference_label="VALUE_TWO", comparison_label="VALUE_ONE", count=1),
            ConfusionCell(reference_label="VALUE_TWO", comparison_label="VALUE_TWO", count=3),
        ),
        error_categories={"SYNTHETIC_BOUNDARY_CONFUSION": 2},
    )
    report = build_reliability_report(
        ReliabilityReportPayload(
            ontology_artifact_id=ontology.artifact_id,
            ontology_sha256=ontology.ontology_sha256,
            coding_procedure_sha256=ontology.payload.coding_procedure_sha256,
            development_corpus_sha256="d" * 64,
            comparison_type="human_human",
            reference_coder_ids=("HUMAN-A",),
            comparison_coder_ids=("HUMAN-B",),
            observable_results=(result,),
            created_at_utc=datetime(2026, 9, 3, 18, 0, tzinfo=UTC),
        )
    )
    assert report.payload.does_not_establish_construct_validity is True
    assert reliability_report_integrity_errors(report, ontology) == ()
    path = tmp_path / "reliability.json"
    write_reliability_report(path, report, ontology)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_reliability_report(path, ontology) == report

    unknown = ObservableReliabilityResult(
        **{
            **result.model_dump(),
            "observable_id": "OBSERVABLE_UNKNOWN",
        }
    )
    bad = build_reliability_report(
        ReliabilityReportPayload(
            **{
                **report.payload.model_dump(),
                "observable_results": (unknown,),
            }
        )
    )
    assert any("unknown observables" in error for error in reliability_report_integrity_errors(bad, ontology))
