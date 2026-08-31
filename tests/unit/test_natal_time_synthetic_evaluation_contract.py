from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

from hdmatch.natal_time.evaluation_contract import (
    ALLOWED_VIOLATION_CODES,
    BUILDER_PATH,
    METRIC_COMPONENT_IDS,
    MODULE_PATH,
    PREREGISTRATION_IDENTIFIER_SETS,
    PREREGISTRATION_REQUIRED_SINGLETONS,
    REFERENCE_OPERATION_CODES,
    V1_CONTRACT_SHA256,
    V2_CONTRACT_SHA256,
    V3_CONTRACT_SHA256,
    EvaluationSession,
    EvaluatorReferenceCustody,
    VerificationError,
    inference_visible_fixture_digest,
    parse_candidate_set,
    parse_component_assignments,
    parse_method_specification,
    parse_preconstructed_output,
    reference_custody_digest,
    validate_no_prohibited_fields,
    validate_preregistration_sections,
    verify_receipt,
    verify_receipt_self_hash,
    verify_separated_synthetic_fixture,
)
from hdmatch.util import canonical_json_bytes, sha256_file, sha256_json
from scripts.build_natal_time_synthetic_evaluation_verifier import (
    STATE_DIRECTORY,
    FixturePair,
    GeneratedBundle,
    build_bundle,
)

PROJECT_ROOT = Path(__file__).parents[2]
STATE_ROOT = PROJECT_ROOT / STATE_DIRECTORY

VALID_METRIC_FIXTURE_IDS = {
    "SYNTH-FIXTURE-FULL-C",
    "SYNTH-FIXTURE-ABSTENTION",
    "SYNTH-FIXTURE-BOUNDARY-TOUCH",
    "SYNTH-FIXTURE-REPEATED-STATE",
    "SYNTH-FIXTURE-DISCONNECTED-SAME-DATE",
    "SYNTH-FIXTURE-DISCONNECTED-REORDERED",
    "SYNTH-FIXTURE-MULTIPLE-DATES",
    "SYNTH-FIXTURE-WIDE-REFERENCE",
    "SYNTH-FIXTURE-REFERENCE-CONTAINED-ACROSS-ADJACENT",
    "SYNTH-FIXTURE-MULTIDATE-INCLUDED-DATE",
    "SYNTH-FIXTURE-IDENTICAL-MULTIPLE-SOURCES",
}
REFERENCE_NA_FIXTURE_IDS = {
    "SYNTH-FIXTURE-SOURCE-CONFLICT",
    "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE",
    "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED",
}
DOMAIN_DIAGNOSTIC_FIXTURE_STATUSES = {
    "SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND": ("reference_domain_partially_incompatible"),
    "SYNTH-FIXTURE-REFERENCE-EXTENDS-AFTER-DOMAIN": ("reference_domain_partially_incompatible"),
    "SYNTH-FIXTURE-REFERENCE-EXTENDS-BOTH-DOMAIN-ENDS": ("reference_domain_partially_incompatible"),
    "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE": "reference_domain_incompatible",
    "SYNTH-FIXTURE-MULTIDATE-EXCLUDED-DATE": "reference_domain_incompatible",
}
REJECTED_FIXTURE_CODES = {
    "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION": "invalid_output_empty_non_abstention",
    "SYNTH-FIXTURE-PARTIAL-INTERVAL": "partial_interval_not_allowed",
    "SYNTH-FIXTURE-DUPLICATE-INTERVAL": "duplicate_selected_interval",
    "SYNTH-FIXTURE-REORDERED-WITH-DUPLICATION": "duplicate_selected_interval",
    "SYNTH-FIXTURE-DISCONNECTED-DUPLICATE": "duplicate_selected_interval",
    "SYNTH-FIXTURE-FOREIGN-INTERVAL": "foreign_or_manufactured_interval",
    "SYNTH-FIXTURE-MANUFACTURED-INTERVAL": "manufactured_interval_not_allowed",
    "SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS": "t_i_access_before_s_i_commitment",
    "SYNTH-FIXTURE-EARLY-REFERENCE-RAW-BYTE": "early_reference_raw_byte_access",
    "SYNTH-FIXTURE-EARLY-REFERENCE-DIGEST": "early_reference_digest_access",
    "SYNTH-FIXTURE-EARLY-REFERENCE-METADATA": "early_reference_metadata_access",
    "SYNTH-FIXTURE-EARLY-REFERENCE-ALTERNATE-LOADER": ("early_reference_alternate_loader_access"),
    "SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION": "s_i_modified_after_t_i_exposure",
    "SYNTH-FIXTURE-POST-REFERENCE-T-MUTATION": "t_i_mutated_after_evaluator_access",
    "SYNTH-FIXTURE-CROSS-ROLE-COMPONENT": "cross_role_connected_component",
    "SYNTH-FIXTURE-CONTAMINATED-COMPONENT": "contaminated_connected_component",
}


@pytest.fixture(scope="module")
def bundle() -> GeneratedBundle:
    return build_bundle(PROJECT_ROOT)


def _pairs_by_id(bundle: GeneratedBundle) -> dict[str, FixturePair]:
    return {cast(str, pair.inference_visible["fixture_id"]): pair for pair in bundle.fixture_pairs}


def _receipts_by_id(bundle: GeneratedBundle) -> dict[str, dict[str, object]]:
    return {cast(str, item["fixture_id"]): item for item in bundle.receipts}


def _metrics(receipt: dict[str, object]) -> dict[str, dict[str, object]]:
    return cast(dict[str, dict[str, object]], receipt["metrics"])


def _evaluator_sha256(bundle: GeneratedBundle) -> str:
    version = cast(dict[str, object], bundle.evaluator_schema["evaluator_version"])
    return cast(str, version["evaluator_version_sha256"])


def _run(pair: FixturePair, evaluator_sha256: str) -> dict[str, object]:
    return verify_separated_synthetic_fixture(
        pair.inference_visible,
        EvaluatorReferenceCustody(lambda: deepcopy(pair.evaluator_reference)),
        evaluator_version_sha256=evaluator_sha256,
    )


def _rehash_fixture(value: dict[str, object]) -> None:
    value["inference_visible_fixture_digest"] = inference_visible_fixture_digest(value)


def _rehash_receipt(value: dict[str, object]) -> None:
    payload = dict(value)
    payload.pop("receipt_sha256", None)
    value["receipt_sha256"] = sha256_json(payload)


def _session_ready_for_reference(pair: FixturePair) -> EvaluationSession:
    fixture = pair.inference_visible
    session = EvaluationSession()
    session.freeze_candidate_domain(
        parse_candidate_set(fixture["candidate_set"]),
        parse_component_assignments(fixture["component_assignments"]),
        cast(str, fixture["contamination_status"]),
    )
    session.freeze_method_specification(parse_method_specification(fixture["method_specification"]))
    session.commit_preconstructed_output(
        parse_preconstructed_output(fixture["preconstructed_output"])
    )
    return session


def test_committed_split_bundle_matches_builder_and_hashes(bundle: GeneratedBundle) -> None:
    assert (
        json.loads((STATE_ROOT / "inference" / "schema.json").read_text())
        == bundle.inference_schema
    )
    assert (
        json.loads((STATE_ROOT / "evaluator" / "schema.json").read_text())
        == bundle.evaluator_schema
    )
    assert (
        json.loads((STATE_ROOT / "inference" / "manifest.json").read_text())
        == bundle.inference_manifest
    )
    assert (
        json.loads((STATE_ROOT / "evaluator" / "manifest.json").read_text())
        == bundle.evaluator_manifest
    )
    assert (
        json.loads((STATE_ROOT / "evaluation-manifest.json").read_text())
        == bundle.evaluation_manifest
    )
    for pair, receipt in zip(bundle.fixture_pairs, bundle.receipts, strict=True):
        fixture_id = cast(str, pair.inference_visible["fixture_id"])
        custody_id = cast(str, pair.evaluator_reference["custody_id"])
        assert (
            json.loads((STATE_ROOT / "inference" / "fixtures" / f"{fixture_id}.json").read_text())
            == pair.inference_visible
        )
        assert (
            json.loads((STATE_ROOT / "evaluator" / "references" / f"{custody_id}.json").read_text())
            == pair.evaluator_reference
        )
        stored = json.loads((STATE_ROOT / "receipts" / f"{fixture_id}.json").read_text())
        assert stored == receipt
        expected_bindings: dict[str, object] = {
            "inference_visible_fixture_digest": pair.inference_visible[
                "inference_visible_fixture_digest"
            ]
        }
        if stored["receipt_kind"] != "fail_closed_rejection":
            expected_bindings.update(
                {
                    "s_i_commitment_sha256": sha256_json(
                        parse_preconstructed_output(
                            pair.inference_visible["preconstructed_output"]
                        ).canonical_payload()
                    ),
                    "reference_custody_sha256": pair.evaluator_reference[
                        "reference_custody_sha256"
                    ],
                }
            )
        assert verify_receipt(
            stored,
            expected_evaluator_version_sha256=_evaluator_sha256(bundle),
            expected_binding_values=expected_bindings,
        )
    for manifest in (
        bundle.inference_manifest,
        bundle.evaluator_manifest,
        bundle.evaluation_manifest,
    ):
        payload = dict(manifest)
        embedded = payload.pop("manifest_sha256")
        assert embedded == sha256_json(payload)


def test_inference_bundle_has_no_reference_address_or_dependency(bundle: GeneratedBundle) -> None:
    exact_fields = set(cast(list[str], bundle.inference_schema["exact_fixture_fields"]))
    assert exact_fields == {
        "schema_version",
        "fixture_id",
        "synthetic_only",
        "preconstructed_s_i",
        "candidate_set",
        "method_specification",
        "preconstructed_output",
        "component_assignments",
        "contamination_status",
        "execution_plan",
        "inference_visible_fixture_digest",
    }
    prohibited_keys = {
        "hidden_reference",
        "reference_custody_sha256",
        "canonical_t_i_sha256",
        "reference_path",
        "reference_size",
        "custody_id",
    }
    for pair in bundle.fixture_pairs:
        assert set(pair.inference_visible) == exact_fields
        assert not (set(pair.inference_visible) & prohibited_keys)
    rendered_manifest = json.dumps(bundle.inference_manifest, sort_keys=True)
    rendered_schema = json.dumps(bundle.inference_schema, sort_keys=True)
    assert "custody_id" not in rendered_manifest
    assert "reference_path" not in rendered_manifest
    assert "evaluator_version" not in rendered_schema
    assert "source_files" not in rendered_schema
    assert BUILDER_PATH not in rendered_schema
    assert MODULE_PATH not in rendered_schema
    assert not any(
        isinstance(value, EvaluatorReferenceCustody) for value in vars(EvaluationSession()).values()
    )


def test_t_only_change_leaves_all_inference_visible_bytes_and_digests_unchanged(
    bundle: GeneratedBundle,
) -> None:
    pair = deepcopy(bundle.fixture_pairs[0])
    before_fixture = canonical_json_bytes(pair.inference_visible)
    before_digest = pair.inference_visible["inference_visible_fixture_digest"]
    reference = cast(dict[str, object], pair.evaluator_reference["reference"])
    sources = cast(list[dict[str, object]], reference["sources"])
    sources[0]["start_utc"] = "2099-01-01T03:00:00.000000Z"
    sources[0]["end_utc"] = "2099-01-01T04:00:00.000000Z"
    pair.evaluator_reference["reference_custody_sha256"] = reference_custody_digest(
        pair.evaluator_reference
    )
    assert canonical_json_bytes(pair.inference_visible) == before_fixture
    assert pair.inference_visible["inference_visible_fixture_digest"] == before_digest


def test_precommit_boundary_performs_zero_reference_operations(bundle: GeneratedBundle) -> None:
    pair = bundle.fixture_pairs[0]
    loader_calls = 0

    def loader() -> object:
        nonlocal loader_calls
        loader_calls += 1
        return deepcopy(pair.evaluator_reference)

    custody = EvaluatorReferenceCustody(loader)
    session = EvaluationSession()
    with pytest.raises(VerificationError, match="t_i_access_before_s_i_commitment"):
        session.release_reference_access_capability()
    assert loader_calls == 0
    assert custody.phase.value == "sealed"
    assert custody.operation_counts == {operation: 0 for operation in REFERENCE_OPERATION_CODES}


def test_evaluator_custody_rejects_an_unissued_capability_without_opening(
    bundle: GeneratedBundle,
) -> None:
    pair = bundle.fixture_pairs[0]
    loader_calls = 0

    def loader() -> object:
        nonlocal loader_calls
        loader_calls += 1
        return deepcopy(pair.evaluator_reference)

    custody = EvaluatorReferenceCustody(loader)
    assert not hasattr(custody, "_loader")
    with pytest.raises(VerificationError, match="invalid_reference_access_capability"):
        custody.open(object())
    assert loader_calls == 0
    assert custody.phase.value == "sealed"
    assert custody.operation_counts == {operation: 0 for operation in REFERENCE_OPERATION_CODES}


@pytest.mark.parametrize(
    ("fixture_id", "code"),
    [
        ("SYNTH-FIXTURE-EARLY-REFERENCE-RAW-BYTE", "early_reference_raw_byte_access"),
        ("SYNTH-FIXTURE-EARLY-REFERENCE-DIGEST", "early_reference_digest_access"),
        ("SYNTH-FIXTURE-EARLY-REFERENCE-METADATA", "early_reference_metadata_access"),
        (
            "SYNTH-FIXTURE-EARLY-REFERENCE-ALTERNATE-LOADER",
            "early_reference_alternate_loader_access",
        ),
    ],
)
def test_early_probe_modes_fail_without_loader_or_reference_operations(
    bundle: GeneratedBundle, fixture_id: str, code: str
) -> None:
    pair = _pairs_by_id(bundle)[fixture_id]
    loader_calls = 0

    def loader() -> object:
        nonlocal loader_calls
        loader_calls += 1
        return deepcopy(pair.evaluator_reference)

    custody = EvaluatorReferenceCustody(loader)
    receipt = verify_separated_synthetic_fixture(
        pair.inference_visible,
        custody,
        evaluator_version_sha256=_evaluator_sha256(bundle),
    )
    assert receipt["receipt_kind"] == "fail_closed_rejection"
    assert receipt["violation_codes"] == [code]
    assert loader_calls == 0
    assert custody.operation_counts == {operation: 0 for operation in REFERENCE_OPERATION_CODES}


def test_authorized_reference_snapshot_is_version_locked_from_loader_alias(
    bundle: GeneratedBundle,
) -> None:
    pair = _pairs_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    shared = deepcopy(pair.evaluator_reference)
    custody = EvaluatorReferenceCustody(lambda: shared)
    session = _session_ready_for_reference(pair)
    opened = custody.open(session.release_reference_access_capability())
    session.accept_opened_reference(opened)
    reference = cast(dict[str, object], shared["reference"])
    sources = cast(list[dict[str, object]], reference["sources"])
    sources[0]["end_utc"] = "2099-01-01T02:00:00.000001Z"
    session.accept_preissue_reference_integrity_recheck(custody.verify_unchanged_after_access())
    receipt = session.issue_receipt(
        fixture_id=cast(str, pair.inference_visible["fixture_id"]),
        inference_visible_fixture_digest=cast(
            str, pair.inference_visible["inference_visible_fixture_digest"]
        ),
        evaluator_version_sha256=_evaluator_sha256(bundle),
    )
    assert (
        receipt["canonical_t_i_sha256"]
        == _receipts_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]["canonical_t_i_sha256"]
    )


def test_post_access_t_mutation_fixture_invalidates_custody(
    bundle: GeneratedBundle,
) -> None:
    receipt = _receipts_by_id(bundle)["SYNTH-FIXTURE-POST-REFERENCE-T-MUTATION"]
    assert receipt["receipt_kind"] == "fail_closed_rejection"
    assert receipt["valid_evaluation_receipt"] is False
    assert receipt["metrics_present"] is False
    assert receipt["violation_codes"] == ["t_i_mutated_after_evaluator_access"]


def test_valid_receipt_binds_final_custody_trace_after_preissue_recheck(
    bundle: GeneratedBundle,
) -> None:
    pair = _pairs_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    custody = EvaluatorReferenceCustody(lambda: deepcopy(pair.evaluator_reference))
    session = _session_ready_for_reference(pair)
    opened = custody.open(session.release_reference_access_capability())
    session.accept_opened_reference(opened)
    session.accept_preissue_reference_integrity_recheck(custody.verify_unchanged_after_access())
    receipt = session.issue_receipt(
        fixture_id=cast(str, pair.inference_visible["fixture_id"]),
        inference_visible_fixture_digest=cast(
            str, pair.inference_visible["inference_visible_fixture_digest"]
        ),
        evaluator_version_sha256=_evaluator_sha256(bundle),
    )
    assert receipt["reference_custody_access_state_sha256"] == custody.access_state_digest
    assert custody.operation_counts["addressability"] == 1
    assert custody.operation_counts["open"] == 1
    assert custody.operation_counts["read"] == 1
    assert custody.operation_counts["parse"] == 1
    assert custody.operation_counts["serialization"] == 3
    assert custody.operation_counts["hash"] == 3
    for operation in ("raw_byte", "stat", "path", "size", "listing"):
        assert custody.operation_counts[operation] == 0


def test_session_rejects_forged_or_nonrechecked_reference_handoffs(
    bundle: GeneratedBundle,
) -> None:
    pair = _pairs_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    forged_session = _session_ready_for_reference(pair)
    with pytest.raises(VerificationError, match="invalid_reference_access_capability"):
        forged_session.accept_opened_reference(object())

    custody = EvaluatorReferenceCustody(lambda: deepcopy(pair.evaluator_reference))
    session = _session_ready_for_reference(pair)
    opened = custody.open(session.release_reference_access_capability())
    session.accept_opened_reference(opened)
    with pytest.raises(VerificationError, match="invalid_reference_access_capability"):
        session.compute_metrics()

    custody = EvaluatorReferenceCustody(lambda: deepcopy(pair.evaluator_reference))
    session = _session_ready_for_reference(pair)
    opened = custody.open(session.release_reference_access_capability())
    session.accept_opened_reference(opened)
    with pytest.raises(VerificationError, match="invalid_reference_access_capability"):
        session.issue_receipt(
            fixture_id=cast(str, pair.inference_visible["fixture_id"]),
            inference_visible_fixture_digest=cast(
                str, pair.inference_visible["inference_visible_fixture_digest"]
            ),
            evaluator_version_sha256=_evaluator_sha256(bundle),
        )


def test_valid_receipts_bind_s_t_custody_access_evaluator_and_v1_v2_v3(
    bundle: GeneratedBundle,
) -> None:
    receipt = _receipts_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    assert receipt["contract_bindings"] == {
        "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
        "preserved_v2_contract_sha256": V2_CONTRACT_SHA256,
        "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
    }
    for field in (
        "inference_visible_fixture_digest",
        "candidate_domain_freeze_sha256",
        "study_method_specification_sha256",
        "s_i_commitment_sha256",
        "canonical_t_i_sha256",
        "reference_custody_sha256",
        "reference_custody_access_state_sha256",
        "access_state_sha256",
        "evaluator_version_sha256",
        "metrics_sha256",
    ):
        assert isinstance(receipt[field], str) and len(cast(str, receipt[field])) == 64
    version = cast(dict[str, object], bundle.evaluator_schema["evaluator_version"])
    assert cast(list[dict[str, str]], version["source_files"]) == [
        {"path": MODULE_PATH, "sha256": sha256_file(PROJECT_ROOT / MODULE_PATH)},
        {"path": BUILDER_PATH, "sha256": sha256_file(PROJECT_ROOT / BUILDER_PATH)},
    ]


def test_every_postcommit_artifact_binds_access_state_and_evaluator(
    bundle: GeneratedBundle,
) -> None:
    evaluator_sha256 = _evaluator_sha256(bundle)
    for receipt in bundle.receipts:
        assert verify_receipt(
            receipt,
            expected_evaluator_version_sha256=evaluator_sha256,
        )
        assert receipt["evaluator_version_sha256"] == evaluator_sha256
        for field in ("inference_visible_fixture_digest", "access_state_sha256"):
            assert isinstance(receipt[field], str)
            assert len(cast(str, receipt[field])) == 64
        if receipt["receipt_kind"] != "fail_closed_rejection":
            assert isinstance(receipt["reference_custody_access_state_sha256"], str)
            assert len(cast(str, receipt["reference_custody_access_state_sha256"])) == 64


def test_contextual_receipt_validation_rejects_a_rehashed_wrong_s_commitment(
    bundle: GeneratedBundle,
) -> None:
    receipt = deepcopy(_receipts_by_id(bundle)["SYNTH-FIXTURE-FULL-C"])
    expected_s = receipt["s_i_commitment_sha256"]
    receipt["s_i_commitment_sha256"] = "0" * 64
    _rehash_receipt(receipt)
    assert verify_receipt_self_hash(receipt)
    assert not verify_receipt(
        receipt,
        expected_evaluator_version_sha256=_evaluator_sha256(bundle),
        expected_binding_values={"s_i_commitment_sha256": expected_s},
    )


def test_full_candidate_set_has_unit_fractions_without_success_semantics(
    bundle: GeneratedBundle,
) -> None:
    receipt = _receipts_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    metrics = _metrics(receipt)
    for component in (
        "temporal_width_retained",
        "canonical_interval_count_retained",
        "unique_state_identity_count_retained",
        "date_coverage",
    ):
        assert metrics[component]["fraction"] == "1/1"
    assert "success" not in json.dumps(receipt, sort_keys=True).lower()
    assert receipt["inference_or_selection_performed"] is False


def test_endpoint_only_contact_does_not_count_as_reference_intersection(
    bundle: GeneratedBundle,
) -> None:
    metrics = _metrics(_receipts_by_id(bundle)["SYNTH-FIXTURE-BOUNDARY-TOUCH"])
    assert metrics["reference_intersection"] == {"status": "applicable", "value": False}


def test_repeated_state_interval_and_unique_state_counts_diverge(
    bundle: GeneratedBundle,
) -> None:
    metrics = _metrics(_receipts_by_id(bundle)["SYNTH-FIXTURE-REPEATED-STATE"])
    assert metrics["canonical_interval_count_retained"]["fraction"] == "1/3"
    assert metrics["unique_state_identity_count_retained"]["fraction"] == "1/4"
    assert metrics["canonical_interval_count_retained"]["selected_interval_count"] == 2
    assert (
        metrics["unique_state_identity_count_retained"]["selected_unique_state_identity_count"] == 1
    )


def test_fixed_fixture_kinds_and_controlled_rejections(bundle: GeneratedBundle) -> None:
    receipts = _receipts_by_id(bundle)
    assert set(receipts) == (
        VALID_METRIC_FIXTURE_IDS
        | REFERENCE_NA_FIXTURE_IDS
        | set(DOMAIN_DIAGNOSTIC_FIXTURE_STATUSES)
        | set(REJECTED_FIXTURE_CODES)
    )
    for fixture_id in VALID_METRIC_FIXTURE_IDS:
        assert receipts[fixture_id]["receipt_kind"] == "descriptive_metric_receipt"
        assert receipts[fixture_id]["evaluation_eligible"] is True
    for fixture_id in REFERENCE_NA_FIXTURE_IDS:
        assert receipts[fixture_id]["receipt_kind"] == "descriptive_metric_receipt"
        assert receipts[fixture_id]["evaluation_eligible"] is False
    for fixture_id, code in REJECTED_FIXTURE_CODES.items():
        receipt = receipts[fixture_id]
        assert receipt["receipt_kind"] == "fail_closed_rejection"
        assert code in cast(list[str], receipt["violation_codes"])
        assert set(cast(list[str], receipt["violation_codes"])) <= ALLOWED_VIOLATION_CODES


def test_disconnected_first_and_third_same_date_has_exact_components_and_no_gap_fill(
    bundle: GeneratedBundle,
) -> None:
    pair = _pairs_by_id(bundle)["SYNTH-FIXTURE-DISCONNECTED-SAME-DATE"]
    candidate = cast(dict[str, object], pair.inference_visible["candidate_set"])
    assert len(cast(list[object], candidate["intervals"])) == 4
    output = cast(dict[str, object], pair.inference_visible["preconstructed_output"])
    selected = cast(list[dict[str, object]], output["selected_intervals"])
    assert [item["interval_id"] for item in selected] == ["SYNTH-INTERVAL-A", "SYNTH-INTERVAL-C"]
    metrics = _metrics(_receipts_by_id(bundle)["SYNTH-FIXTURE-DISCONNECTED-SAME-DATE"])
    assert metrics["temporal_width_retained"]["fraction"] == "1/2"
    assert metrics["canonical_interval_count_retained"]["fraction"] == "1/2"
    assert metrics["unique_state_identity_count_retained"]["fraction"] == "1/3"
    assert metrics["date_coverage"]["fraction"] == "1/1"


def test_disconnected_reordering_preserves_commitment_and_complete_receipt(
    bundle: GeneratedBundle,
) -> None:
    pair = deepcopy(_pairs_by_id(bundle)["SYNTH-FIXTURE-DISCONNECTED-SAME-DATE"])
    original = _run(pair, _evaluator_sha256(bundle))
    output = cast(dict[str, object], pair.inference_visible["preconstructed_output"])
    cast(list[object], output["selected_intervals"]).reverse()
    _rehash_fixture(pair.inference_visible)
    reordered = _run(pair, _evaluator_sha256(bundle))
    assert reordered == original


def test_three_way_domain_union_and_diagnostic_only_artifacts(bundle: GeneratedBundle) -> None:
    receipts = _receipts_by_id(bundle)
    spanning = receipts["SYNTH-FIXTURE-REFERENCE-CONTAINED-ACROSS-ADJACENT"]
    assert spanning["receipt_kind"] == "descriptive_metric_receipt"
    assert _metrics(spanning)["reference_intersection"] == {"status": "applicable", "value": True}
    assert (
        receipts["SYNTH-FIXTURE-MULTIDATE-INCLUDED-DATE"]["receipt_kind"]
        == "descriptive_metric_receipt"
    )
    for fixture_id, status in DOMAIN_DIAGNOSTIC_FIXTURE_STATUSES.items():
        diagnostic = receipts[fixture_id]
        assert diagnostic["receipt_kind"] == "reference_domain_diagnostic"
        assert diagnostic["valid_reference_evaluation_receipt"] is False
        assert diagnostic["reference_domain_status"] == status
        assert diagnostic["reference_intersection"] == {
            "status": f"not_applicable_{status}",
            "value": None,
        }
        width = cast(dict[str, object], diagnostic["documentary_reference_width"])
        assert width["status"] == "applicable"
        assert isinstance(width["microseconds"], int) and cast(int, width["microseconds"]) > 0
        assert "metrics" not in diagnostic
        assert verify_receipt(diagnostic)


def test_diagnostic_rejects_typed_na_documentary_width_even_when_rehashed(
    bundle: GeneratedBundle,
) -> None:
    diagnostic = deepcopy(_receipts_by_id(bundle)["SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE"])
    diagnostic["documentary_reference_width"] = {
        "status": "not_applicable_reference_domain_incompatible",
        "microseconds": None,
    }
    _rehash_receipt(diagnostic)
    assert verify_receipt_self_hash(diagnostic)
    assert verify_receipt(diagnostic) is False


def test_reference_na_abstention_and_separate_metric_components(bundle: GeneratedBundle) -> None:
    receipts = _receipts_by_id(bundle)
    abstention = _metrics(receipts["SYNTH-FIXTURE-ABSTENTION"])
    assert abstention["abstention"] == {"status": "applicable", "value": True}
    assert abstention["reference_intersection"] == {
        "status": "not_applicable_abstention",
        "value": None,
    }
    for fixture_id, status in {
        "SYNTH-FIXTURE-SOURCE-CONFLICT": "not_applicable_conflicting_eligible_sources",
        "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE": "not_applicable_no_eligible_reference",
        "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED": (
            "not_applicable_reference_canonicalization_failed"
        ),
    }.items():
        metrics = _metrics(receipts[fixture_id])
        assert set(metrics) == set(METRIC_COMPONENT_IDS)
        assert metrics["reference_intersection"] == {"status": status, "value": None}
    validate_no_prohibited_fields(receipts)


def test_receipt_schema_is_closed_for_valid_diagnostic_and_rejection(
    bundle: GeneratedBundle,
) -> None:
    receipts = _receipts_by_id(bundle)
    for fixture_id in (
        "SYNTH-FIXTURE-FULL-C",
        "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",
        "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION",
    ):
        mutant = deepcopy(receipts[fixture_id])
        mutant["metadata"] = "SYNTHETIC-ONLY"
        _rehash_receipt(mutant)
        assert verify_receipt_self_hash(mutant)
        assert verify_receipt(mutant) is False

    valid_nested = deepcopy(receipts["SYNTH-FIXTURE-FULL-C"])
    metrics = cast(dict[str, dict[str, object]], valid_nested["metrics"])
    metrics["reference_intersection"]["metadata"] = "SYNTHETIC-ONLY"
    valid_nested["metrics_sha256"] = sha256_json(metrics)
    _rehash_receipt(valid_nested)
    assert verify_receipt(valid_nested) is False

    binding_nested = deepcopy(receipts["SYNTH-FIXTURE-FULL-C"])
    bindings = cast(dict[str, object], binding_nested["contract_bindings"])
    bindings["metadata"] = "SYNTHETIC-ONLY"
    _rehash_receipt(binding_nested)
    assert verify_receipt(binding_nested) is False

    diagnostic_nested = deepcopy(receipts["SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE"])
    intersection = cast(dict[str, object], diagnostic_nested["reference_intersection"])
    intersection["metadata"] = "SYNTHETIC-ONLY"
    _rehash_receipt(diagnostic_nested)
    assert verify_receipt(diagnostic_nested) is False


def test_rehash_added_forbidden_scalar_field_is_rejected(
    bundle: GeneratedBundle,
) -> None:
    mutant = deepcopy(_receipts_by_id(bundle)["SYNTH-FIXTURE-FULL-C"])
    mutant["score"] = 1
    _rehash_receipt(mutant)
    assert verify_receipt_self_hash(mutant)
    with pytest.raises(
        VerificationError,
        match="prohibited_inferential_or_scalar_output_field",
    ):
        validate_no_prohibited_fields(mutant)
    assert verify_receipt(mutant) is False


def test_evaluator_custody_schema_is_closed_recursively(bundle: GeneratedBundle) -> None:
    pair = deepcopy(_pairs_by_id(bundle)["SYNTH-FIXTURE-FULL-C"])
    reference = cast(dict[str, object], pair.evaluator_reference["reference"])
    reference["metadata"] = "SYNTHETIC-ONLY"
    pair.evaluator_reference["reference_custody_sha256"] = reference_custody_digest(
        pair.evaluator_reference
    )
    receipt = _run(pair, _evaluator_sha256(bundle))
    assert receipt["receipt_kind"] == "fail_closed_rejection"
    assert receipt["violation_codes"] == ["invalid_reference_fields"]


def test_recursive_prohibited_and_exact_membership_mutants_fail_closed(
    bundle: GeneratedBundle,
) -> None:
    pair = _pairs_by_id(bundle)["SYNTH-FIXTURE-FULL-C"]
    evaluator_sha256 = _evaluator_sha256(bundle)
    for container, key in (
        ("candidate_set", "free_text"),
        ("preconstructed_output", "score"),
    ):
        mutant = deepcopy(pair)
        cast(dict[str, object], mutant.inference_visible[container])[key] = "SYNTHETIC-ONLY"
        _rehash_fixture(mutant.inference_visible)
        receipt = _run(mutant, evaluator_sha256)
        assert receipt["receipt_kind"] == "fail_closed_rejection"
        assert cast(list[str], receipt["violation_codes"])[0].startswith("prohibited_")
    for field, value in (
        ("civil_date", "2099-01-03"),
        ("full_state_sha256", "f" * 64),
        ("candidate_manifest_sha256", "e" * 64),
    ):
        mutant = deepcopy(pair)
        output = cast(dict[str, object], mutant.inference_visible["preconstructed_output"])
        cast(list[dict[str, object]], output["selected_intervals"])[0][field] = value
        _rehash_fixture(mutant.inference_visible)
        receipt = _run(mutant, evaluator_sha256)
        assert receipt["violation_codes"] == ["foreign_or_manufactured_interval"]


def test_preregistration_requires_every_exact_controlled_identifier_set() -> None:
    valid: dict[str, object] = {
        "schema_version": "natal-time-preregistration-structure-v1",
        "required_singletons": list(PREREGISTRATION_REQUIRED_SINGLETONS),
        **{key: list(values) for key, values in PREREGISTRATION_IDENTIFIER_SETS.items()},
    }
    assert validate_preregistration_sections(valid).valid
    for field in ("required_singletons", *PREREGISTRATION_IDENTIFIER_SETS):
        missing = deepcopy(valid)
        cast(list[object], missing[field]).pop()
        assert not validate_preregistration_sections(missing).valid
        duplicate = deepcopy(valid)
        values = cast(list[object], duplicate[field])
        values.append(values[0])
        assert validate_preregistration_sections(duplicate).duplicate_sections
        unknown = deepcopy(valid)
        cast(list[object], unknown[field]).append("heading-only-or-unknown")
        assert validate_preregistration_sections(unknown).unexpected_sections


def test_invalid_evaluator_digest_emits_no_artifact(bundle: GeneratedBundle) -> None:
    pair = bundle.fixture_pairs[0]
    for invalid in ("not-a-digest", "0" * 64):
        with pytest.raises(VerificationError, match="invalid_evaluator_version_digest"):
            verify_separated_synthetic_fixture(
                pair.inference_visible,
                EvaluatorReferenceCustody(lambda: deepcopy(pair.evaluator_reference)),
                evaluator_version_sha256=invalid,
            )
