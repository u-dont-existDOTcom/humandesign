"""Acceptance tests for the B1 pre-content governance and AstroHD mapping firewall."""

import pytest

from tests.b1_precontent.acceptance import _expect_failure, _invalid_case, check_requirement
from tests.b1_precontent.validator import load_fixture, validate_record


@pytest.mark.parametrize(
    "requirement_id",
    [f"B1-{index:02d}" for index in range(1, 65)],
)
def test_b1_precontent_acceptance(requirement_id: str) -> None:
    check_requirement(requirement_id)


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
