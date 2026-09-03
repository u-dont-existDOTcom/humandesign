from __future__ import annotations

from datetime import UTC, datetime

from hdmatch.evaluation.neutral_measurement import (
    CodedEpisodeRecord,
    CoderIdentity,
    CodingRunPayload,
    FreezeEvidenceIndex,
    HumanContentAuthorityReceipt,
    ObservableDefinition,
    OntologyReleasePayload,
    build_coding_run_artifact,
    build_ontology_release,
)
from hdmatch.experiments.canonical import sha256_json


NOW = datetime(2026, 9, 3, 19, 10, tzinfo=UTC)


def _evidence() -> FreezeEvidenceIndex:
    return FreezeEvidenceIndex(
        session_id="LP-STRUCTURAL-READINESS-TEST",
        freeze_id="BPF-0123456789ABCDEF0123",
        freeze_sha256="0" * 64,
        episode_sha256={"EP-A": "1" * 64},
        source_turn_sha256={"TURN-A": "2" * 64},
        episode_source_turn_ids={"EP-A": ("TURN-A",)},
        episode_input_modality={"EP-A": "typed"},
        participant_revised_episode={"EP-A": False},
    )


def _observable(*, validity: str, reliability: str) -> ObservableDefinition:
    return ObservableDefinition(
        observable_id="STRUCTURAL_READINESS_ALPHA",
        label="STRUCTURAL READINESS TEST",
        definition="Software readiness fixture only; no behavioral construct meaning.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO"),
        insufficient_semantics="Structural insufficient state.",
        not_applicable_semantics="Structural not-applicable state.",
        inclusion_criteria=("Structural inclusion criterion only.",),
        exclusion_criteria=("Structural exclusion criterion only.",),
        evidence_requirements=("One structural evidence reference.",),
        participant_review_policy="Structural software test only.",
        theory_contamination_policy="No target-theory content in this fixture.",
        origin_status="project_specific",
        validity_status=validity,  # type: ignore[arg-type]
        reliability_status=reliability,  # type: ignore[arg-type]
        release_notes="STRUCTURAL SOFTWARE TEST ONLY; not scientific content.",
    )


def _ontology(*, validity: str, reliability: str):
    observable = _observable(validity=validity, reliability=reliability)
    ontology_id = "life-patterns-structural-readiness-test"
    ontology_version = "2026-09-03"
    scope = "STRUCTURAL SOFTWARE READINESS TEST ONLY; not a substantive ontology."
    content_sha = sha256_json(
        {
            "ontology_id": ontology_id,
            "ontology_version": ontology_version,
            "scope_statement": scope,
            "observables": (observable,),
        }
    )
    authority = HumanContentAuthorityReceipt(
        content_sha256=content_sha,
        human_authorship_receipt_sha256="3" * 64,
        exposure_adjudication_receipt_sha256="4" * 64,
        content_review_receipt_sha256="5" * 64,
        authorized_at_utc=NOW,
    )
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id=ontology_id,
            ontology_version=ontology_version,
            release_status="frozen_for_validation",
            scope_statement=scope,
            observables=(observable,),
            coding_procedure_id="structural-coding-v1",
            coding_procedure_sha256="6" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="7" * 64,
            theory_contamination_policy_id="structural-theory-v1",
            theory_contamination_policy_sha256="8" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=NOW,
            synthetic_fixture_only=False,
            human_content_authority=authority,
        )
    )


def _record() -> CodedEpisodeRecord:
    return CodedEpisodeRecord(
        episode_id="EP-A",
        observable_id="STRUCTURAL_READINESS_ALPHA",
        state="observed",
        coded_value="VALUE_ONE",
        supporting_source_turn_ids=("TURN-A",),
        input_modality="typed",
        theory_exposure="none_detected",
        source_episode_participant_revised=False,
    )


def _payload(ontology, *, records: tuple[CodedEpisodeRecord, ...]) -> CodingRunPayload:
    evidence = _evidence()
    return CodingRunPayload(
        session_id=evidence.session_id,
        freeze_id=evidence.freeze_id,
        freeze_sha256=evidence.freeze_sha256,
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        coding_procedure_id=ontology.payload.coding_procedure_id,
        coding_procedure_sha256=ontology.payload.coding_procedure_sha256,
        coder=CoderIdentity(
            coder_id="STRUCTURAL-HUMAN-CODER",
            coder_type="human",
            version="training-v1",
            training_receipt_sha256="9" * 64,
        ),
        run_type="validation",
        records=records,
        created_at_utc=NOW,
    )


def test_validation_run_blocks_observable_without_validation_candidate_status() -> None:
    ontology = _ontology(
        validity="content_reviewed",
        reliability="human_baseline_evaluated",
    )
    artifact = build_coding_run_artifact(
        _payload(ontology, records=(_record(),)),
        ontology,
        _evidence(),
    )
    assert artifact.scoreable_for_model_tournament is False
    assert (
        "coded observables are not validation candidates: STRUCTURAL_READINESS_ALPHA"
        in artifact.scoreability_blockers
    )


def test_validation_run_blocks_observable_without_human_reliability_baseline() -> None:
    ontology = _ontology(
        validity="validation_candidate",
        reliability="not_evaluated",
    )
    artifact = build_coding_run_artifact(
        _payload(ontology, records=(_record(),)),
        ontology,
        _evidence(),
    )
    assert artifact.scoreable_for_model_tournament is False
    assert (
        "coded observables lack a human reliability baseline: STRUCTURAL_READINESS_ALPHA"
        in artifact.scoreability_blockers
    )


def test_validation_run_is_scoreable_only_after_declared_measurement_readiness() -> None:
    ontology = _ontology(
        validity="validation_candidate",
        reliability="human_baseline_evaluated",
    )
    artifact = build_coding_run_artifact(
        _payload(ontology, records=(_record(),)),
        ontology,
        _evidence(),
    )
    assert artifact.scoreable_for_model_tournament is True
    assert artifact.scoreability_blockers == ()


def test_empty_validation_coding_run_is_never_scoreable() -> None:
    ontology = _ontology(
        validity="validation_candidate",
        reliability="human_baseline_evaluated",
    )
    artifact = build_coding_run_artifact(
        _payload(ontology, records=()),
        ontology,
        _evidence(),
    )
    assert artifact.scoreable_for_model_tournament is False
    assert "coding run contains no coded episode records" in artifact.scoreability_blockers
