"""Acceptance tests for the construct-neutral Option B reliability architecture."""

import pytest

from tests.option_b.acceptance import _expect_failure, _invalid_case, check_requirement
from tests.option_b.validator import load_fixture, validate_record


@pytest.mark.parametrize(
    "requirement_id",
    [f"OB-{index:02d}" for index in range(1, 73)],
)
def test_option_b_acceptance(requirement_id: str) -> None:
    check_requirement(requirement_id)


@pytest.mark.parametrize(
    ("schema_name", "fixture_name"),
    [
        ("administration", "administration_valid.json"),
        ("coding", "coding_valid.json"),
        ("property_plan", "property_plan_valid.json"),
    ],
)
def test_option_b_valid_synthetic_fixture(schema_name: str, fixture_name: str) -> None:
    validate_record(schema_name, load_fixture(fixture_name))


@pytest.mark.parametrize(
    "case_id",
    [
        "SYNTH-INVALID-UNKNOWN-FIELD",
        "SYNTH-INVALID-CONSTRUCT-FIELD",
        "SYNTH-INVALID-REHASHED-CONSTRUCT",
        "SYNTH-INVALID-PRODUCTION-CLASS",
        "SYNTH-INVALID-PARTICIPANT-ID",
        "SYNTH-INVALID-CHART-FIELD",
        "SYNTH-INVALID-REFERENCE-SET-FIELD",
        "SYNTH-INVALID-SCORE-FIELD",
        "SYNTH-INVALID-THRESHOLD-FIELD",
        "SYNTH-INVALID-CODING-CATEGORY",
        "SYNTH-INVALID-PRIOR-CODE-CLEAN",
        "SYNTH-INVALID-ADJUDICATION-REWRITE",
        "SYNTH-INVALID-RETEST-RESOLVED",
        "SYNTH-INVALID-MISSING-AS-ZERO",
        "SYNTH-INVALID-RESPONSE-CONTENT",
    ],
)
def test_option_b_invalid_probe_controlled_rejection(case_id: str) -> None:
    schema, record, code = _invalid_case(case_id)
    _expect_failure(code, schema, record)
