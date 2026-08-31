"""Acceptance tests for the B1 pre-content governance and AstroHD mapping firewall."""

import copy

import pytest

from tests.b1_precontent.acceptance import (
    ARTIFACT_MANIFEST,
    _canonical_json_digest,
    _expect_failure,
    _invalid_case,
    _validate_traceability_manifest_data,
    check_requirement,
)
from tests.b1_precontent.validator import load_fixture, load_json, validate_record


@pytest.mark.parametrize(
    "requirement_id",
    [f"B1-{index:02d}" for index in range(1, 65)],
)
def test_b1_precontent_acceptance(requirement_id: str) -> None:
    check_requirement(requirement_id)


def _traceability_manifest() -> dict[str, object]:
    return copy.deepcopy(load_json(ARTIFACT_MANIFEST))


def test_b1_traceability_has_exactly_one_primary_per_artifact() -> None:
    _validate_traceability_manifest_data(_traceability_manifest())


@pytest.mark.parametrize(
    "invalid_primary",
    [None, "", 62, "B1-65", "B1-1", ["B1-01", "B1-02"], ["B1-01", "B1-01"]],
)
def test_b1_traceability_invalid_primary_fails_closed(invalid_primary: object) -> None:
    manifest = _traceability_manifest()
    manifest["artifacts"][0]["primary_requirement_id"] = invalid_primary  # type: ignore[index]
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_missing_primary_fails_closed() -> None:
    manifest = _traceability_manifest()
    del manifest["artifacts"][0]["primary_requirement_id"]  # type: ignore[index]
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_duplicate_artifact_fails_closed() -> None:
    manifest = _traceability_manifest()
    manifest["artifacts"][1] = copy.deepcopy(manifest["artifacts"][0])  # type: ignore[index]
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_omitted_artifact_fails_closed() -> None:
    manifest = _traceability_manifest()
    manifest["artifacts"].pop()  # type: ignore[union-attr]
    manifest["artifact_count"] = 32
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_secondary_references_are_noncontrolling() -> None:
    manifest = _traceability_manifest()
    artifact = manifest["artifacts"][0]  # type: ignore[index]
    assert len(artifact["supports_requirement_ids"]) > 1  # type: ignore[arg-type,index]
    _validate_traceability_manifest_data(manifest)
    artifact["primary_requirement_ids"] = artifact["supports_requirement_ids"]  # type: ignore[index]
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_primary_cannot_be_repeated_as_support() -> None:
    manifest = _traceability_manifest()
    artifact = manifest["artifacts"][0]  # type: ignore[index]
    artifact["supports_requirement_ids"].append(artifact["primary_requirement_id"])  # type: ignore[union-attr,index]
    with pytest.raises(AssertionError):
        _validate_traceability_manifest_data(manifest)


def test_b1_traceability_primary_assignment_changes_manifest_digest() -> None:
    manifest = _traceability_manifest()
    before = _canonical_json_digest(manifest)
    artifact = manifest["artifacts"][0]  # type: ignore[index]
    artifact["primary_requirement_id"] = "B1-02"  # type: ignore[index]
    artifact["supports_requirement_ids"] = ["B1-01", "B1-03"]  # type: ignore[index]
    assert _canonical_json_digest(manifest) != before


@pytest.mark.parametrize(
    ("schema_name", "fixture_name"),
    [
        ("content_embargo", "content_embargo_valid.json"),
        ("candidate", "candidate_metadata_valid.json"),
        ("access", "access_event_valid.json"),
    ],
)
def test_b1_valid_synthetic_fixture(schema_name: str, fixture_name: str) -> None:
    validate_record(schema_name, load_fixture(fixture_name))


@pytest.mark.parametrize(
    "case_id",
    [
        "B1-INVALID-UNKNOWN-FIELD",
        "B1-INVALID-CONSTRUCT-NAME",
        "B1-INVALID-RESPONSE-CONTENT",
        "B1-INVALID-MEASUREMENT-MODEL",
        "B1-INVALID-COEFFICIENT",
        "B1-INVALID-POPULATION",
        "B1-INVALID-CHART-FIELD",
        "B1-INVALID-MAPPING-RULE",
        "B1-INVALID-REHASHED-MAPPING",
        "B1-INVALID-OPAQUE-ID",
        "B1-INVALID-UNKNOWN-PROVENANCE-CLEAN",
        "B1-INVALID-EXPOSURE-CLEAN",
        "B1-INVALID-APPEND-ONLY-FALSE",
        "B1-INVALID-ROLE-ERASES-EXPOSURE",
    ],
)
def test_b1_invalid_probe_controlled_rejection(case_id: str) -> None:
    schema, record, code = _invalid_case(case_id)
    _expect_failure(code, schema, record)
