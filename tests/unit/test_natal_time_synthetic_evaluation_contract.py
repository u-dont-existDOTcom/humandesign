from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

import hdmatch.natal_time.evaluation_contract as evaluation_contract_module
from hdmatch.natal_time.evaluation_contract import (
    ALLOWED_VIOLATION_CODES,
    BUILDER_PATH,
    METRIC_COMPONENT_IDS,
    MODULE_PATH,
    PREREGISTRATION_IDENTIFIER_SETS,
    PREREGISTRATION_REQUIRED_SINGLETONS,
    V1_CONTRACT_SHA256,
    V2_CONTRACT_SHA256,
    EvaluationSession,
    ReferenceBundle,
    VerificationError,
    fixture_digest,
    parse_preconstructed_output,
    parse_reference_bundle,
    validate_no_prohibited_fields,
    validate_preregistration_sections,
    verify_receipt,
    verify_receipt_self_hash,
    verify_synthetic_fixture,
)
from hdmatch.util import sha256_file, sha256_json
from scripts.build_natal_time_synthetic_evaluation_verifier import (
    STATE_DIRECTORY,
    build_bundle,
    build_fixtures,
)

PROJECT_ROOT = Path(__file__).parents[2]
STATE_ROOT = PROJECT_ROOT / STATE_DIRECTORY

VALID_FIXTURE_IDS = {
    "SYNTH-FIXTURE-FULL-C",
    "SYNTH-FIXTURE-ABSTENTION",
    "SYNTH-FIXTURE-BOUNDARY-TOUCH",
    "SYNTH-FIXTURE-REPEATED-STATE",
    "SYNTH-FIXTURE-MULTIPLE-DATES",
    "SYNTH-FIXTURE-WIDE-REFERENCE",
    "SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND",
    "SYNTH-FIXTURE-IDENTICAL-MULTIPLE-SOURCES",
}
REFERENCE_INAPPLICABLE_FIXTURE_IDS = {
    "SYNTH-FIXTURE-SOURCE-CONFLICT",
    "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE",
    "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE",
    "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED",
}
REJECTED_FIXTURE_CODES = {
    "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION": "invalid_output_empty_non_abstention",
    "SYNTH-FIXTURE-PARTIAL-INTERVAL": "partial_interval_not_allowed",
    "SYNTH-FIXTURE-DUPLICATE-INTERVAL": "duplicate_selected_interval",
    "SYNTH-FIXTURE-REORDERED-WITH-DUPLICATION": "duplicate_selected_interval",
    "SYNTH-FIXTURE-FOREIGN-INTERVAL": "foreign_or_manufactured_interval",
    "SYNTH-FIXTURE-MANUFACTURED-INTERVAL": "foreign_or_manufactured_interval",
    "SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS": "t_i_access_before_s_i_commitment",
    "SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION": "s_i_modified_after_t_i_exposure",
    "SYNTH-FIXTURE-CROSS-ROLE-COMPONENT": "cross_role_connected_component",
    "SYNTH-FIXTURE-CONTAMINATED-COMPONENT": "contaminated_connected_component",
}


def _by_id(values: tuple[dict[str, object], ...]) -> dict[str, dict[str, object]]:
    return {cast(str, item["fixture_id"]): item for item in values}


def _receipt_metrics(receipt: dict[str, object]) -> dict[str, dict[str, object]]:
    return cast(dict[str, dict[str, object]], receipt["metrics"])


def _recommit_fixture(value: dict[str, object]) -> dict[str, object]:
    value["fixture_sha256"] = fixture_digest(value)
    return value


def _valid_preregistration() -> dict[str, object]:
    return {
        "schema_version": "natal-time-preregistration-structure-v1",
        "required_singletons": list(PREREGISTRATION_REQUIRED_SINGLETONS),
        **{key: list(values) for key, values in PREREGISTRATION_IDENTIFIER_SETS.items()},
    }


def test_committed_bundle_matches_builder_and_all_hashes() -> None:
    expected_schema, expected_fixtures, expected_receipts, expected_manifest = build_bundle(
        PROJECT_ROOT
    )
    assert json.loads((STATE_ROOT / "schema.json").read_text()) == expected_schema
    assert json.loads((STATE_ROOT / "manifest.json").read_text()) == expected_manifest
    assert expected_manifest["schema_file_sha256"] == sha256_file(STATE_ROOT / "schema.json")
    entries = {
        cast(str, entry["fixture_id"]): entry
        for entry in cast(list[dict[str, object]], expected_manifest["entries"])
    }
    for fixture, receipt in zip(expected_fixtures, expected_receipts, strict=True):
        fixture_id = cast(str, fixture["fixture_id"])
        fixture_path = STATE_ROOT / "fixtures" / f"{fixture_id}.json"
        receipt_path = STATE_ROOT / "receipts" / f"{fixture_id}.json"
        assert json.loads(fixture_path.read_text()) == fixture
        assert entries[fixture_id]["fixture_file_sha256"] == sha256_file(fixture_path)
        stored_receipt = json.loads(receipt_path.read_text())
        assert entries[fixture_id]["receipt_file_sha256"] == sha256_file(receipt_path)
        assert stored_receipt == receipt
        assert verify_receipt_self_hash(stored_receipt)
        assert verify_receipt(
            stored_receipt,
            expected_evaluator_version_sha256=cast(
                str, expected_manifest["evaluator_version_sha256"]
            ),
        )
        assert stored_receipt["fixture_sha256"] == fixture["fixture_sha256"]
        assert (
            stored_receipt["evaluator_version_sha256"]
            == expected_manifest["evaluator_version_sha256"]
        )
    manifest_without_hash = dict(expected_manifest)
    embedded_manifest_hash = manifest_without_hash.pop("manifest_sha256")
    assert embedded_manifest_hash == sha256_json(manifest_without_hash)
    schema_without_hash = dict(expected_schema)
    embedded_schema_hash = schema_without_hash.pop("schema_sha256")
    assert embedded_schema_hash == sha256_json(schema_without_hash)


def test_contract_and_evaluator_version_bind_logical_v2_and_exact_code_bytes() -> None:
    schema, _, receipts, manifest = build_bundle(PROJECT_ROOT)
    bindings = cast(dict[str, object], schema["contract_bindings"])
    assert bindings == {
        "preserved_v1_contract_sha256": V1_CONTRACT_SHA256,
        "metric_semantics_v2_contract_sha256": V2_CONTRACT_SHA256,
    }
    version = cast(dict[str, object], schema["evaluator_version"])
    source_files = cast(list[dict[str, str]], version["source_files"])
    assert source_files == [
        {"path": MODULE_PATH, "sha256": sha256_file(PROJECT_ROOT / MODULE_PATH)},
        {"path": BUILDER_PATH, "sha256": sha256_file(PROJECT_ROOT / BUILDER_PATH)},
    ]
    version_without_hash = dict(version)
    embedded = version_without_hash.pop("evaluator_version_sha256")
    assert embedded == sha256_json(version_without_hash)
    assert manifest["evaluator_version_sha256"] == embedded
    assert all(receipt["evaluator_version_sha256"] == embedded for receipt in receipts)


def test_every_acceptance_fixture_has_expected_receipt_kind_and_error_code() -> None:
    _, fixtures, receipts, _ = build_bundle(PROJECT_ROOT)
    fixture_ids = {cast(str, item["fixture_id"]) for item in fixtures}
    assert fixture_ids == (
        VALID_FIXTURE_IDS | REFERENCE_INAPPLICABLE_FIXTURE_IDS | set(REJECTED_FIXTURE_CODES)
    )
    by_receipt = _by_id(receipts)
    for fixture_id in VALID_FIXTURE_IDS:
        receipt = by_receipt[fixture_id]
        assert receipt["receipt_kind"] == "descriptive_metric_receipt"
        assert receipt["evaluation_eligible"] is True
    for fixture_id in REFERENCE_INAPPLICABLE_FIXTURE_IDS:
        receipt = by_receipt[fixture_id]
        assert receipt["receipt_kind"] == "descriptive_metric_receipt"
        assert receipt["evaluation_eligible"] is False
    for fixture_id, code in REJECTED_FIXTURE_CODES.items():
        receipt = by_receipt[fixture_id]
        assert receipt["receipt_kind"] == "fail_closed_rejection"
        assert receipt["valid_evaluation_receipt"] is False
        assert receipt["metrics_present"] is False
        assert code in cast(list[str], receipt["violation_codes"])
        assert set(cast(list[str], receipt["violation_codes"])) <= ALLOWED_VIOLATION_CODES


def test_reference_supplier_is_not_invoked_before_output_commitment() -> None:
    session = EvaluationSession()
    calls = 0

    def supplier() -> ReferenceBundle:
        nonlocal calls
        calls += 1
        return parse_reference_bundle(
            {"canonicalization_status": "no_eligible_reference", "sources": []}
        )

    with pytest.raises(VerificationError, match="t_i_access_before_s_i_commitment"):
        session.expose_reference(supplier)
    assert calls == 0
    assert session.phase.value == "invalidated"
    assert session.violations == ("t_i_access_before_s_i_commitment",)


def test_precommit_fixture_digest_excludes_hidden_reference_semantics() -> None:
    fixture = deepcopy(build_fixtures()[0])
    original_digest = fixture_digest(fixture)
    reference = cast(dict[str, object], fixture["hidden_reference"])
    sources = cast(list[dict[str, object]], reference["sources"])
    sources[0]["start_utc"] = "2099-01-01T03:00:00.000000Z"
    sources[0]["end_utc"] = "2099-01-01T04:00:00.000000Z"
    assert fixture_digest(fixture) == original_digest


def test_early_access_fixture_never_parses_hidden_reference(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schema, fixtures, _, _ = build_bundle(PROJECT_ROOT)
    evaluator = cast(dict[str, object], schema["evaluator_version"])
    calls = 0
    original = evaluation_contract_module.parse_reference_bundle

    def probe(value: object) -> ReferenceBundle:
        nonlocal calls
        calls += 1
        return original(value)

    monkeypatch.setattr(evaluation_contract_module, "parse_reference_bundle", probe)
    fixture = _by_id(fixtures)["SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS"]
    receipt = verify_synthetic_fixture(
        fixture,
        evaluator_version_sha256=cast(str, evaluator["evaluator_version_sha256"]),
    )
    assert receipt["violation_codes"] == ["t_i_access_before_s_i_commitment"]
    assert calls == 0


def test_post_reference_output_change_is_fail_closed_and_has_no_valid_receipt() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    receipt = _by_id(receipts)["SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION"]
    assert receipt["valid_evaluation_receipt"] is False
    assert receipt["metrics_present"] is False
    assert receipt["violation_codes"] == ["s_i_modified_after_t_i_exposure"]


def test_full_candidate_set_has_unit_retention_without_success_semantics() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    receipt = _by_id(receipts)["SYNTH-FIXTURE-FULL-C"]
    metrics = _receipt_metrics(receipt)
    for component in (
        "temporal_width_retained",
        "canonical_interval_count_retained",
        "unique_state_identity_count_retained",
        "date_coverage",
    ):
        assert metrics[component]["fraction"] == "1/1"
    assert metrics["reference_intersection"] == {"status": "applicable", "value": True}
    assert "success" not in json.dumps(receipt).lower()
    assert receipt["inference_or_selection_performed"] is False
    assert receipt["metrics_sha256"] == sha256_json(metrics)


def test_abstention_uses_typed_null_na_components_not_zero_or_false() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    metrics = _receipt_metrics(_by_id(receipts)["SYNTH-FIXTURE-ABSTENTION"])
    assert metrics["abstention"] == {"status": "applicable", "value": True}
    assert metrics["documentary_reference_width"] == {
        "status": "applicable",
        "microseconds": 3_600_000_000,
    }
    assert metrics["reference_intersection"] == {
        "status": "not_applicable_abstention",
        "value": None,
    }
    for component in (
        "temporal_width_retained",
        "canonical_interval_count_retained",
        "unique_state_identity_count_retained",
        "date_coverage",
    ):
        item = metrics[component]
        assert item["status"] == "not_applicable_abstention"
        assert item["fraction"] is None
        assert all(value is None for key, value in item.items() if key != "status")


def test_endpoint_repeated_state_multiple_date_wide_and_partial_reference_metrics() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    by_receipt = _by_id(receipts)
    boundary = _receipt_metrics(by_receipt["SYNTH-FIXTURE-BOUNDARY-TOUCH"])
    assert boundary["reference_intersection"] == {"status": "applicable", "value": False}

    repeated = _receipt_metrics(by_receipt["SYNTH-FIXTURE-REPEATED-STATE"])
    assert repeated["canonical_interval_count_retained"]["fraction"] == "2/5"
    assert repeated["unique_state_identity_count_retained"]["fraction"] == "1/3"
    assert repeated["temporal_width_retained"]["fraction"] == "1/3"

    multiple_dates = _receipt_metrics(by_receipt["SYNTH-FIXTURE-MULTIPLE-DATES"])
    assert multiple_dates["date_coverage"]["fraction"] == "1/1"
    assert multiple_dates["temporal_width_retained"]["fraction"] == "5/12"

    wide = _receipt_metrics(by_receipt["SYNTH-FIXTURE-WIDE-REFERENCE"])
    assert wide["documentary_reference_width"]["microseconds"] == 79_200_000_000

    partial = _receipt_metrics(by_receipt["SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND"])
    assert partial["reference_intersection"] == {"status": "applicable", "value": True}
    assert partial["documentary_reference_width"]["microseconds"] == 60_000_001

    corroborated = _receipt_metrics(by_receipt["SYNTH-FIXTURE-IDENTICAL-MULTIPLE-SOURCES"])
    assert corroborated["reference_intersection"] == {"status": "applicable", "value": True}
    assert corroborated["documentary_reference_width"]["microseconds"] == 3_600_000_000


def test_reference_failure_modes_are_distinct_typed_na_and_never_inference_misses() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    by_receipt = _by_id(receipts)
    expected = {
        "SYNTH-FIXTURE-SOURCE-CONFLICT": "not_applicable_conflicting_eligible_sources",
        "SYNTH-FIXTURE-DOMAIN-INCOMPATIBLE": ("not_applicable_reference_domain_incompatible"),
        "SYNTH-FIXTURE-NO-ELIGIBLE-REFERENCE": "not_applicable_no_eligible_reference",
        "SYNTH-FIXTURE-REFERENCE-CANONICALIZATION-FAILED": (
            "not_applicable_reference_canonicalization_failed"
        ),
    }
    for fixture_id, status in expected.items():
        receipt = by_receipt[fixture_id]
        metrics = _receipt_metrics(receipt)
        assert receipt["evaluation_eligible"] is False
        assert set(metrics) == set(METRIC_COMPONENT_IDS)
        for name, component in metrics.items():
            if name == "abstention":
                assert component == {"status": "applicable", "value": False}
                continue
            assert component["status"] == status
            assert all(value is None for key, value in component.items() if key != "status")
        assert "miss" not in json.dumps(receipt).lower()


def test_canonical_reordering_preserves_fixture_output_and_receipt_digests() -> None:
    schema, fixtures, receipts, _ = build_bundle(PROJECT_ROOT)
    fixture = deepcopy(_by_id(fixtures)["SYNTH-FIXTURE-FULL-C"])
    receipt = _by_id(receipts)["SYNTH-FIXTURE-FULL-C"]
    original_digest = fixture_digest(fixture)
    candidate = cast(dict[str, object], fixture["candidate_set"])
    cast(list[object], candidate["intervals"]).reverse()
    cast(list[object], candidate["declared_dates"]).reverse()
    output = cast(dict[str, object], fixture["preconstructed_output"])
    cast(list[object], output["selected_intervals"]).reverse()
    assert fixture_digest(fixture) == original_digest
    evaluator = cast(dict[str, object], schema["evaluator_version"])
    reordered_receipt = verify_synthetic_fixture(
        fixture,
        evaluator_version_sha256=cast(str, evaluator["evaluator_version_sha256"]),
    )
    assert reordered_receipt == receipt


def test_duplicate_detection_precedes_canonical_reordering() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    receipt = _by_id(receipts)["SYNTH-FIXTURE-REORDERED-WITH-DUPLICATION"]
    assert receipt["violation_codes"] == ["duplicate_selected_interval"]
    assert receipt["metrics_present"] is False


def test_exact_membership_includes_civil_date_and_state_provenance() -> None:
    schema, fixtures, _, _ = build_bundle(PROJECT_ROOT)
    evaluator = cast(dict[str, object], schema["evaluator_version"])
    evaluator_sha256 = cast(str, evaluator["evaluator_version_sha256"])
    base = _by_id(fixtures)["SYNTH-FIXTURE-BOUNDARY-TOUCH"]
    for field, value in (
        ("civil_date", "2099-01-03"),
        ("full_state_sha256", "f" * 64),
        ("candidate_manifest_sha256", "e" * 64),
    ):
        mutant = deepcopy(base)
        output = cast(dict[str, object], mutant["preconstructed_output"])
        selected = cast(list[dict[str, object]], output["selected_intervals"])
        selected[0][field] = value
        _recommit_fixture(mutant)
        receipt = verify_synthetic_fixture(mutant, evaluator_version_sha256=evaluator_sha256)
        assert receipt["violation_codes"] == ["foreign_or_manufactured_interval"]
        assert "partial_interval_not_allowed" not in cast(list[str], receipt["violation_codes"])


def test_recursive_extra_prohibited_and_invalid_date_mutants_fail_closed() -> None:
    schema, fixtures, _, _ = build_bundle(PROJECT_ROOT)
    evaluator = cast(dict[str, object], schema["evaluator_version"])
    evaluator_sha256 = cast(str, evaluator["evaluator_version_sha256"])
    base = _by_id(fixtures)["SYNTH-FIXTURE-FULL-C"]

    prohibited_mutants: list[dict[str, object]] = []
    for container_name, key in (
        ("candidate_set", "free_text"),
        ("hidden_reference", "relationship_code"),
        ("preconstructed_output", "score"),
    ):
        mutant = deepcopy(base)
        cast(dict[str, object], mutant[container_name])[key] = "SYNTHETIC-ONLY"
        prohibited_mutants.append(mutant)
    participant_mutant = deepcopy(base)
    participant_mutant["participant_id"] = "SYNTHETIC-ONLY"
    prohibited_mutants.append(participant_mutant)
    for mutant in prohibited_mutants:
        _recommit_fixture(mutant)
        receipt = verify_synthetic_fixture(mutant, evaluator_version_sha256=evaluator_sha256)
        assert receipt["receipt_kind"] == "fail_closed_rejection"
        assert receipt["valid_evaluation_receipt"] is False
        assert cast(list[str], receipt["violation_codes"])[0].startswith("prohibited_")

    nested_extra = deepcopy(base)
    cast(dict[str, object], nested_extra["hidden_reference"])["note"] = "SYNTHETIC-ONLY"
    _recommit_fixture(nested_extra)
    extra_receipt = verify_synthetic_fixture(
        nested_extra, evaluator_version_sha256=evaluator_sha256
    )
    assert extra_receipt["violation_codes"] == ["invalid_reference_fields"]

    invalid_date = deepcopy(base)
    candidate = cast(dict[str, object], invalid_date["candidate_set"])
    cast(list[object], candidate["declared_dates"])[0] = "2099-02-30"
    _recommit_fixture(invalid_date)
    date_receipt = verify_synthetic_fixture(invalid_date, evaluator_version_sha256=evaluator_sha256)
    assert date_receipt["violation_codes"] == ["invalid_synthetic_date"]


def test_preregistration_requires_every_exact_controlled_identifier_set() -> None:
    valid = _valid_preregistration()
    assert validate_preregistration_sections(valid).valid is True
    assert len(cast(list[object], valid["baseline_ids"])) == 15
    assert len(cast(list[object], valid["measurement_requirement_ids"])) == 11
    for field in ("required_singletons", *PREREGISTRATION_IDENTIFIER_SETS):
        missing = deepcopy(valid)
        cast(list[object], missing[field]).pop()
        assert validate_preregistration_sections(missing).valid is False

        duplicate = deepcopy(valid)
        values = cast(list[object], duplicate[field])
        values.append(values[0])
        result = validate_preregistration_sections(duplicate)
        assert result.valid is False
        assert result.duplicate_sections

        unknown = deepcopy(valid)
        cast(list[object], unknown[field]).append("heading-only-or-unknown")
        result = validate_preregistration_sections(unknown)
        assert result.valid is False
        assert result.unexpected_sections

    headings_only = {
        "schema_version": "natal-time-preregistration-structure-v1",
        "required_singletons": list(PREREGISTRATION_REQUIRED_SINGLETONS),
    }
    assert validate_preregistration_sections(headings_only).valid is False


def test_receipts_expose_only_separate_components_and_no_prohibited_semantics() -> None:
    schema, _, receipts, _ = build_bundle(PROJECT_ROOT)
    receipt_contract = cast(dict[str, object], schema["receipt_contract"])
    assert receipt_contract["component_metrics"] == list(METRIC_COMPONENT_IDS)
    assert receipt_contract["scalar_summary_present"] is False
    for receipt in receipts:
        validate_no_prohibited_fields(receipt)
        rendered = json.dumps(receipt, sort_keys=True).lower()
        for forbidden in (
            '"rank"',
            '"best',
            '"score',
            '"weight',
            '"probability',
            '"confidence',
            '"utility',
            '"threshold',
            '"recommendation',
        ):
            assert forbidden not in rendered
        assert receipt["inference_or_selection_performed"] is False


def test_rehashed_unknown_receipt_fields_fail_closed_at_every_shape() -> None:
    _, _, receipts, _ = build_bundle(PROJECT_ROOT)
    by_receipt = _by_id(receipts)
    valid = by_receipt["SYNTH-FIXTURE-FULL-C"]
    rejection = by_receipt["SYNTH-FIXTURE-EMPTY-NON-ABSTENTION"]

    top_level = deepcopy(valid)
    top_level["metadata"] = "SYNTHETIC-ONLY"
    unhashed = dict(top_level)
    unhashed.pop("receipt_sha256")
    top_level["receipt_sha256"] = sha256_json(unhashed)
    assert verify_receipt_self_hash(top_level)
    assert verify_receipt(top_level) is False

    nested_metric = deepcopy(valid)
    metrics = cast(dict[str, dict[str, object]], nested_metric["metrics"])
    metrics["reference_intersection"]["metadata"] = "SYNTHETIC-ONLY"
    nested_metric["metrics_sha256"] = sha256_json(metrics)
    unhashed = dict(nested_metric)
    unhashed.pop("receipt_sha256")
    nested_metric["receipt_sha256"] = sha256_json(unhashed)
    assert verify_receipt_self_hash(nested_metric)
    assert verify_receipt(nested_metric) is False

    nested_binding = deepcopy(valid)
    bindings = cast(dict[str, object], nested_binding["contract_bindings"])
    bindings["metadata"] = "SYNTHETIC-ONLY"
    unhashed = dict(nested_binding)
    unhashed.pop("receipt_sha256")
    nested_binding["receipt_sha256"] = sha256_json(unhashed)
    assert verify_receipt_self_hash(nested_binding)
    assert verify_receipt(nested_binding) is False

    rejection_extra = deepcopy(rejection)
    rejection_extra["metadata"] = "SYNTHETIC-ONLY"
    unhashed = dict(rejection_extra)
    unhashed.pop("receipt_sha256")
    rejection_extra["receipt_sha256"] = sha256_json(unhashed)
    assert verify_receipt_self_hash(rejection_extra)
    assert verify_receipt(rejection_extra) is False

    inconsistent_eligibility = deepcopy(valid)
    inconsistent_eligibility["evaluation_eligible"] = False
    unhashed = dict(inconsistent_eligibility)
    unhashed.pop("receipt_sha256")
    inconsistent_eligibility["receipt_sha256"] = sha256_json(unhashed)
    assert verify_receipt_self_hash(inconsistent_eligibility)
    assert verify_receipt(inconsistent_eligibility) is False


def test_invalid_evaluator_digest_emits_no_artifact() -> None:
    fixture = build_fixtures()[0]
    for invalid in ("not-a-digest", "0" * 64):
        with pytest.raises(VerificationError, match="invalid_evaluator_version_digest"):
            verify_synthetic_fixture(fixture, evaluator_version_sha256=invalid)


def test_output_commitment_digest_is_order_insensitive_but_duplicate_preserving() -> None:
    fixture = deepcopy(build_fixtures()[0])
    output = cast(dict[str, object], fixture["preconstructed_output"])
    original = parse_preconstructed_output(output)
    cast(list[object], output["selected_intervals"]).reverse()
    reordered = parse_preconstructed_output(output)
    assert sha256_json(original.canonical_payload()) == sha256_json(reordered.canonical_payload())
    cast(list[object], output["selected_intervals"]).append(
        deepcopy(cast(list[object], output["selected_intervals"])[0])
    )
    duplicated = parse_preconstructed_output(output)
    assert sha256_json(duplicated.canonical_payload()) != sha256_json(original.canonical_payload())
