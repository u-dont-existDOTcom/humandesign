from __future__ import annotations

from datetime import UTC, datetime

import pytest

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
from hdmatch.evaluation.theory_blind_authority import TheoryBlindContentAuthorityReceipt
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 4, 1, 0, tzinfo=UTC)


def _observable() -> ObservableDefinition:
    return ObservableDefinition(
        observable_id="STRUCTURAL_THEORY_BLIND_ALPHA",
        label="STRUCTURAL THEORY-BLIND TEST",
        definition="Software-gate fixture only; no substantive behavioral construct meaning.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO"),
        insufficient_semantics="Structural insufficient state.",
        not_applicable_semantics="Structural not-applicable state.",
        inclusion_criteria=("Structural inclusion only.",),
        exclusion_criteria=("Structural exclusion only.",),
        evidence_requirements=("One structural source turn.",),
        participant_review_policy="Structural software test only.",
        theory_contamination_policy="No target-theory content in this fixture.",
        origin_status="project_specific",
        validity_status="validation_candidate",
        reliability_status="automation_evaluated",
        release_notes="STRUCTURAL TEST ONLY; no scientific construct claim.",
    )


def _content_sha(observable: ObservableDefinition) -> str:
    return sha256_json(
        {
            "ontology_id": "life-patterns-theory-blind-structural-test",
            "ontology_version": "2026-09-04",
            "scope_statement": "STRUCTURAL SOFTWARE TEST ONLY.",
            "observables": (observable,),
        }
    )


def _theory_blind_receipt(
    observable: ObservableDefinition,
    *,
    stage: str = "validation_candidate",
    content_sha: str | None = None,
) -> TheoryBlindContentAuthorityReceipt:
    return TheoryBlindContentAuthorityReceipt(
        content_sha256=content_sha or _content_sha(observable),
        authority_id="LPTB-0123456789ABCDEF0123",
        authority_sha256="a" * 64,
        authority_stage=stage,  # type: ignore[arg-type]
        validation_route=(
            "statistically_justified_llm_substitution"
            if stage == "validation_candidate"
            else None
        ),
        authorized_at_utc=NOW,
    )


def _ontology():
    observable = _observable()
    return build_ontology_release(
        OntologyReleasePayload(
            ontology_id="life-patterns-theory-blind-structural-test",
            ontology_version="2026-09-04",
            release_status="frozen_for_validation",
            scope_statement="STRUCTURAL SOFTWARE TEST ONLY.",
            observables=(observable,),
            coding_procedure_id="structural-coding-v1",
            coding_procedure_sha256="1" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="2" * 64,
            theory_contamination_policy_id="structural-theory-v1",
            theory_contamination_policy_sha256="3" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=NOW,
            synthetic_fixture_only=False,
            theory_blind_content_authority=_theory_blind_receipt(observable),
        )
    )


def _evidence() -> FreezeEvidenceIndex:
    return FreezeEvidenceIndex(
        session_id="LP-THEORY-BLIND-STRUCTURAL",
        freeze_id="BPF-0123456789ABCDEF0123",
        freeze_sha256="4" * 64,
        episode_sha256={"EP-A": "5" * 64},
        source_turn_sha256={"TURN-A": "6" * 64},
        episode_source_turn_ids={"EP-A": ("TURN-A",)},
        episode_input_modality={"EP-A": "typed"},
        participant_revised_episode={"EP-A": False},
    )


def _record() -> CodedEpisodeRecord:
    return CodedEpisodeRecord(
        episode_id="EP-A",
        observable_id="STRUCTURAL_THEORY_BLIND_ALPHA",
        state="observed",
        coded_value="VALUE_ONE",
        supporting_source_turn_ids=("TURN-A",),
        input_modality="typed",
        theory_exposure="none_detected",
        source_episode_participant_revised=False,
    )


def _automated_payload(ontology, *, calibrated: bool) -> CodingRunPayload:
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
            coder_id="LLM-STRUCTURAL-TEST",
            coder_type="llm",
            version="model-v1",
            implementation_sha256="7" * 64,
            automation_validation_receipt_sha256=("8" * 64 if calibrated else None),
        ),
        run_type="validation",
        records=(_record(),),
        created_at_utc=NOW,
    )


def test_theory_blind_llm_substitution_authority_can_replace_legacy_h1_gate() -> None:
    ontology = _ontology()
    assert ontology.payload.human_content_authority is None
    assert ontology.payload.theory_blind_content_authority is not None
    assert ontology.payload.theory_blind_content_authority.validation_route == (
        "statistically_justified_llm_substitution"
    )

    evidence = _evidence()
    blocked = build_coding_run_artifact(
        _automated_payload(ontology, calibrated=False),
        ontology,
        evidence,
    )
    assert blocked.scoreable_for_model_tournament is False
    assert "automated coder lacks a frozen calibration/validation receipt" in blocked.scoreability_blockers

    allowed = build_coding_run_artifact(
        _automated_payload(ontology, calibrated=True),
        ontology,
        evidence,
    )
    assert allowed.scoreable_for_model_tournament is True
    assert allowed.scoreability_blockers == ()


def test_frozen_theory_blind_ontology_requires_validation_stage_and_exact_content() -> None:
    observable = _observable()
    base = {
        "ontology_id": "life-patterns-theory-blind-structural-test",
        "ontology_version": "2026-09-04",
        "release_status": "frozen_for_validation",
        "scope_statement": "STRUCTURAL SOFTWARE TEST ONLY.",
        "observables": (observable,),
        "coding_procedure_id": "structural-coding-v1",
        "coding_procedure_sha256": "1" * 64,
        "aggregation_policy_id": "structural-aggregation-v1",
        "aggregation_policy_sha256": "2" * 64,
        "theory_contamination_policy_id": "structural-theory-v1",
        "theory_contamination_policy_sha256": "3" * 64,
        "source_commit": "abcdef0123456789abcdef0123456789abcdef01",
        "released_at_utc": NOW,
        "synthetic_fixture_only": False,
    }

    with pytest.raises(ValueError, match="validation-candidate theory-blind authority"):
        OntologyReleasePayload(
            **{
                **base,
                "theory_blind_content_authority": _theory_blind_receipt(
                    observable,
                    stage="development_candidate",
                ),
            }
        )

    tampered = OntologyReleasePayload(
        **{
            **base,
            "theory_blind_content_authority": _theory_blind_receipt(
                observable,
                content_sha="f" * 64,
            ),
        }
    )
    with pytest.raises(ValueError, match="theory-blind content authority does not bind"):
        build_ontology_release(tampered)


def test_ontology_rejects_simultaneous_legacy_and_theory_blind_authority() -> None:
    observable = _observable()
    content_sha = _content_sha(observable)
    legacy = HumanContentAuthorityReceipt(
        content_sha256=content_sha,
        human_authorship_receipt_sha256="b" * 64,
        exposure_adjudication_receipt_sha256="c" * 64,
        content_review_receipt_sha256="d" * 64,
        authorized_at_utc=NOW,
    )
    with pytest.raises(ValueError, match="exactly one content-authority path"):
        OntologyReleasePayload(
            ontology_id="life-patterns-theory-blind-structural-test",
            ontology_version="2026-09-04",
            release_status="frozen_for_validation",
            scope_statement="STRUCTURAL SOFTWARE TEST ONLY.",
            observables=(observable,),
            coding_procedure_id="structural-coding-v1",
            coding_procedure_sha256="1" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="2" * 64,
            theory_contamination_policy_id="structural-theory-v1",
            theory_contamination_policy_sha256="3" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=NOW,
            synthetic_fixture_only=False,
            human_content_authority=legacy,
            theory_blind_content_authority=_theory_blind_receipt(observable),
        )
