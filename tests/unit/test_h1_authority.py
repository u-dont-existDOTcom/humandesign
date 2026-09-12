from __future__ import annotations

import stat
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.h1_authority import (
    EligibleH1AuthorReference,
    HumanAuthorshipProcessReceipt,
    HumanContentAuthorityBundlePayload,
    HumanContentReviewReceipt,
    SurveyV2H1SpecificationBinding,
    ValidatedH1AdjudicationPayload,
    authority_bundle_integrity_errors,
    build_human_content_authority_bundle,
    build_validated_h1_adjudication,
    h1_eligibility_errors,
    human_content_authority_receipt_from_bundle,
    load_h1_authority_bundle,
    write_h1_authority_bundle,
)
from hdmatch.evaluation.neutral_measurement import (
    ObservableDefinition,
    OntologyReleasePayload,
    build_ontology_release,
)
from hdmatch.experiments.canonical import sha256_json


CONTENT_SHA = "a" * 64
BASE_TIME = datetime(2026, 9, 3, 19, 0, tzinfo=UTC)


def _eligible_adjudication(
    *,
    content_sha: str = CONTENT_SHA,
    exposure_class: str = "shallow_or_incidental",
    semantic_overlap: str = "none_affirmatively_established",
    relevant_window: str = "no_exposure_in_relevant_window",
):
    return build_validated_h1_adjudication(
        ValidatedH1AdjudicationPayload(
            specification=SurveyV2H1SpecificationBinding(),
            h1_artifact_id="H1A-SYNTHETICARTIFACT01",
            h1_content_freeze_sha256=content_sha,
            request_id="H1R-SYNTHETICREQUEST01",
            request_sha256="1" * 64,
            evidence_packet_sha256="2" * 64,
            raw_response_sha256="3" * 64,
            parsed_output_sha256="4" * 64,
            top_level_status="completed",
            exposure_class=exposure_class,  # type: ignore[arg-type]
            decision="eligible",
            relevant_window_assessment=relevant_window,  # type: ignore[arg-type]
            semantic_overlap_assessment=semantic_overlap,  # type: ignore[arg-type]
            evidence_sufficiency="sufficient",
            missing_fact_codes=(),
            validator_id="SYNTHETIC-H1-VALIDATOR",
            validator_version="v1",
            validator_sha256="5" * 64,
            validated_at_utc=BASE_TIME,
        )
    )


def _reference(adjudication) -> EligibleH1AuthorReference:
    return EligibleH1AuthorReference(
        validation_receipt_id=adjudication.validation_receipt_id,
        validation_receipt_sha256=adjudication.validation_receipt_sha256,
        request_id=adjudication.payload.request_id,
    )


def _bundle_payload(
    *,
    content_sha: str = CONTENT_SHA,
    adjudication=None,
    review_outcome: str = "approved_for_validation",
    reviewer_influence: str = "method_only",
    reviewer_refs: tuple[EligibleH1AuthorReference, ...] = (),
    content_changed_during_review: bool = False,
) -> HumanContentAuthorityBundlePayload:
    adjudication = adjudication or _eligible_adjudication(content_sha=content_sha)
    ref = _reference(adjudication)
    return HumanContentAuthorityBundlePayload(
        content_sha256=content_sha,
        adjudications=(adjudication,),
        authorship=HumanAuthorshipProcessReceipt(
            h1_artifact_id=adjudication.payload.h1_artifact_id,
            content_sha256=content_sha,
            eligible_author_references=(ref,),
            authorship_started_at_utc=BASE_TIME - timedelta(days=3),
            content_frozen_at_utc=BASE_TIME + timedelta(minutes=1),
        ),
        content_review=HumanContentReviewReceipt(
            content_sha256=content_sha,
            review_protocol_sha256="6" * 64,
            review_outcome=review_outcome,  # type: ignore[arg-type]
            reviewer_influence=reviewer_influence,  # type: ignore[arg-type]
            content_changed_during_review=content_changed_during_review,
            content_influencing_reviewer_references=reviewer_refs,
            reviewed_at_utc=BASE_TIME + timedelta(minutes=2),
        ),
        authorized_at_utc=BASE_TIME + timedelta(minutes=3),
    )


def test_exact_frozen_survey_v2_h1_specification_is_structurally_pinned() -> None:
    lock = SurveyV2H1SpecificationBinding()
    assert lock.contract_version == "survey-v2-h1-exposure-adjudication-contract-v1.0.0"
    assert lock.required_model_family == "gpt-5.6-sol"
    assert lock.contract_sha256 == (
        "b26e8ca398eb805125ed4ea475243e1d0cb5134bee4c509dd29223355ff1b070"
    )
    with pytest.raises(ValidationError):
        SurveyV2H1SpecificationBinding(contract_sha256="f" * 64)  # type: ignore[arg-type]


def test_eligible_h1_receipt_requires_frozen_eligible_branch_semantics() -> None:
    shallow = _eligible_adjudication()
    assert h1_eligibility_errors(shallow) == ()

    substantial = _eligible_adjudication(
        exposure_class="substantial_semantic_or_technical",
        semantic_overlap="disjoint_technical_only",
        relevant_window="before_or_during_h1_authorship",
    )
    assert h1_eligibility_errors(substantial) == ()

    bad_overlap = _eligible_adjudication(
        exposure_class="substantial_semantic_or_technical",
        semantic_overlap="material_or_foreseeable_overlap",
        relevant_window="before_or_during_h1_authorship",
    )
    assert "substantial exposure is eligible only under disjoint technical quarantine" in (
        h1_eligibility_errors(bad_overlap)
    )


def test_ineligible_or_ambiguous_h1_result_cannot_become_authority() -> None:
    ineligible = build_validated_h1_adjudication(
        ValidatedH1AdjudicationPayload(
            specification=SurveyV2H1SpecificationBinding(),
            h1_artifact_id="H1A-SYNTHETICARTIFACT01",
            h1_content_freeze_sha256=CONTENT_SHA,
            request_id="H1R-SYNTHETICREQUEST02",
            request_sha256="1" * 64,
            evidence_packet_sha256="2" * 64,
            raw_response_sha256="3" * 64,
            parsed_output_sha256="4" * 64,
            top_level_status="completed",
            exposure_class="identity_defining_or_comprehensive",
            decision="ineligible",
            relevant_window_assessment="before_or_during_h1_authorship",
            semantic_overlap_assessment="material_or_foreseeable_overlap",
            evidence_sufficiency="sufficient",
            validator_id="SYNTHETIC-H1-VALIDATOR",
            validator_version="v1",
            validator_sha256="5" * 64,
            validated_at_utc=BASE_TIME,
        )
    )
    errors = h1_eligibility_errors(ineligible)
    assert "H1 adjudication did not return eligible" in errors
    with pytest.raises(ValueError, match="invalid H1 authority bundle"):
        build_human_content_authority_bundle(
            _bundle_payload(adjudication=ineligible)
        )


def test_authority_bundle_binds_exact_content_and_all_referenced_h1_receipts() -> None:
    adjudication = _eligible_adjudication()
    payload = _bundle_payload(adjudication=adjudication)
    bundle = build_human_content_authority_bundle(payload)
    assert authority_bundle_integrity_errors(bundle) == ()
    assert bundle.authority_bundle_id == f"LPH1-{bundle.authority_bundle_sha256[:20].upper()}"

    wrong_content = payload.model_copy(update={"content_sha256": "b" * 64})
    with pytest.raises(ValueError, match="does not bind authority content hash"):
        build_human_content_authority_bundle(wrong_content)

    bad_ref = EligibleH1AuthorReference(
        validation_receipt_id=adjudication.validation_receipt_id,
        validation_receipt_sha256="f" * 64,
        request_id=adjudication.payload.request_id,
    )
    bad_authorship = payload.authorship.model_copy(
        update={"eligible_author_references": (bad_ref,)}
    )
    with pytest.raises(ValueError, match="does not match its receipt"):
        build_human_content_authority_bundle(
            payload.model_copy(update={"authorship": bad_authorship})
        )


def test_content_review_cannot_silently_change_or_select_content_without_h1_reference() -> None:
    with pytest.raises(ValidationError, match="changed content requires a new content hash"):
        HumanContentReviewReceipt(
            content_sha256=CONTENT_SHA,
            review_protocol_sha256="6" * 64,
            review_outcome="approved_for_validation",
            reviewer_influence="method_only",
            content_changed_during_review=True,
            reviewed_at_utc=BASE_TIME,
        )

    with pytest.raises(ValidationError, match="content-influencing reviewers require"):
        HumanContentReviewReceipt(
            content_sha256=CONTENT_SHA,
            review_protocol_sha256="6" * 64,
            review_outcome="approved_for_validation",
            reviewer_influence="content_influencing",
            content_changed_during_review=False,
            reviewed_at_utc=BASE_TIME,
        )

    payload = _bundle_payload(review_outcome="approved_for_development_only")
    with pytest.raises(ValueError, match="not approved for validation"):
        build_human_content_authority_bundle(payload)


def test_authority_bundle_derives_existing_neutral_measurement_authority_receipt() -> None:
    bundle = build_human_content_authority_bundle(_bundle_payload())
    receipt = human_content_authority_receipt_from_bundle(bundle)
    assert receipt.content_sha256 == CONTENT_SHA
    assert receipt.human_authorship_receipt_sha256 == sha256_json(bundle.payload.authorship)
    assert receipt.exposure_adjudication_receipt_sha256 == sha256_json(
        bundle.payload.adjudications
    )
    assert receipt.content_review_receipt_sha256 == sha256_json(bundle.payload.content_review)


def test_derived_authority_receipt_binds_exact_ontology_content_hash() -> None:
    observable = ObservableDefinition(
        observable_id="STRUCTURAL_AUTHORITY_TEST",
        label="STRUCTURAL TEST PLACEHOLDER",
        definition="Software authority-binding fixture only; no behavioral construct meaning.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("VALUE_ONE", "VALUE_TWO"),
        insufficient_semantics="Structural insufficient state.",
        not_applicable_semantics="Structural not-applicable state.",
        inclusion_criteria=("Structural criterion only.",),
        exclusion_criteria=("Structural exclusion only.",),
        evidence_requirements=("One structural evidence reference.",),
        participant_review_policy="Structural software test only.",
        theory_contamination_policy="No target-theory content in this structural fixture.",
        origin_status="project_specific",
        validity_status="validation_candidate",
        reliability_status="human_baseline_evaluated",
        release_notes="STRUCTURAL TEST ONLY; not scientific content.",
    )
    ontology_id = "life-patterns-h1-authority-structural-test"
    ontology_version = "2026-09-03"
    scope = "STRUCTURAL SOFTWARE TEST ONLY; not a substantive ontology."
    content_sha = sha256_json(
        {
            "ontology_id": ontology_id,
            "ontology_version": ontology_version,
            "scope_statement": scope,
            "observables": (observable,),
        }
    )
    adjudication = _eligible_adjudication(content_sha=content_sha)
    bundle = build_human_content_authority_bundle(
        _bundle_payload(content_sha=content_sha, adjudication=adjudication)
    )
    authority = human_content_authority_receipt_from_bundle(bundle)
    ontology = build_ontology_release(
        OntologyReleasePayload(
            ontology_id=ontology_id,
            ontology_version=ontology_version,
            release_status="frozen_for_validation",
            scope_statement=scope,
            observables=(observable,),
            coding_procedure_id="structural-procedure-v1",
            coding_procedure_sha256="7" * 64,
            aggregation_policy_id="structural-aggregation-v1",
            aggregation_policy_sha256="8" * 64,
            theory_contamination_policy_id="structural-theory-policy-v1",
            theory_contamination_policy_sha256="9" * 64,
            source_commit="abcdef0123456789abcdef0123456789abcdef01",
            released_at_utc=BASE_TIME + timedelta(minutes=4),
            synthetic_fixture_only=False,
            human_content_authority=authority,
        )
    )
    assert ontology.payload.human_content_authority == authority

    wrong_authority = authority.model_copy(update={"content_sha256": "f" * 64})
    with pytest.raises(ValueError, match="does not bind this ontology content"):
        build_ontology_release(
            ontology.payload.model_copy(update={"human_content_authority": wrong_authority})
        )


def test_h1_authority_bundle_is_immutable_and_canonical(tmp_path: Path) -> None:
    bundle = build_human_content_authority_bundle(_bundle_payload())
    path = tmp_path / "authority.json"
    write_h1_authority_bundle(path, bundle)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_h1_authority_bundle(path) == bundle
    with pytest.raises(FileExistsError):
        write_h1_authority_bundle(path, bundle)
