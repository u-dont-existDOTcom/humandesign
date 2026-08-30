"""Closed validator for conspicuously synthetic S6/H1 pre-human metadata.

This module is test-only. Production code must never import it or the state schemas it reads.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "s6-h1-prehuman-synthetic-validator-v1"
ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
FIXTURES = ROOT / "tests" / "fixtures" / "s6_h1_prehuman"
ALLOWED_SOURCE = "CONSPICUOUSLY_SYNTHETIC_S6_H1_FIXTURE"

SCHEMA_PATHS = {
    "screening": STATE / "NATAL-TIME-S6-H1-SCREENING-METADATA-SCHEMA-V1.json",
    "isolation": STATE / "NATAL-TIME-S6-H1-ISOLATION-PROVENANCE-SCHEMA-V1.json",
}


@dataclass(frozen=True)
class ValidationFailure(Exception):
    """A controlled fail-closed result for test-only metadata."""

    code: str
    path: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}:{self.path}:{self.detail}"


def load_json(path: Path) -> Any:
    """Read one committed JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture(name: str) -> dict[str, Any]:
    """Load an object only from the dedicated synthetic fixture directory."""

    if Path(name).name != name or not name.endswith(".json"):
        raise ValidationFailure("S6H1_FIXTURE_PATH_REJECTED", "$", name)
    value = load_json(FIXTURES / name)
    if not isinstance(value, dict):
        raise ValidationFailure("S6H1_TYPE_MISMATCH", "$", "fixture must be an object")
    return value


def _type_matches(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return False


def _validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    if expected is not None and not _type_matches(expected, value):
        raise ValidationFailure("S6H1_TYPE_MISMATCH", path, f"expected {expected}")
    if "const" in schema and value != schema["const"]:
        raise ValidationFailure("S6H1_CONST_VIOLATION", path, "closed constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise ValidationFailure("S6H1_ENUM_VIOLATION", path, "outside closed vocabulary")
    if (
        isinstance(value, str)
        and "pattern" in schema
        and re.fullmatch(schema["pattern"], value) is None
    ):
        raise ValidationFailure("S6H1_PATTERN_VIOLATION", path, "pattern mismatch")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for field in schema.get("required", []):
            if field not in value:
                raise ValidationFailure(
                    "S6H1_REQUIRED_FIELD_MISSING", f"{path}.{field}", "required"
                )
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise ValidationFailure(
                    "S6H1_UNKNOWN_FIELD", f"{path}.{unknown[0]}", "closed schema"
                )
        for field, nested in value.items():
            if field in properties:
                _validate_schema(nested, properties[field], f"{path}.{field}")
    if isinstance(value, list) and "items" in schema:
        for index, nested in enumerate(value):
            _validate_schema(nested, schema["items"], f"{path}[{index}]")


def _all_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        keys = list(value)
        for nested in value.values():
            keys.extend(_all_keys(nested))
        return keys
    if isinstance(value, list):
        keys: list[str] = []
        for nested in value:
            keys.extend(_all_keys(nested))
        return keys
    return []


def _check_prohibited_fields(schema: dict[str, Any], record: dict[str, Any]) -> None:
    prohibited = set(schema["x-prohibited-field-names"])
    for key in _all_keys(record):
        if key in prohibited:
            raise ValidationFailure(
                "S6H1_PROHIBITED_FIELD", f"$.{key}", "human/content field prohibited"
            )


def _check_synthetic_boundary(record: dict[str, Any], source: str) -> None:
    if source != ALLOWED_SOURCE:
        raise ValidationFailure("S6H1_NON_SYNTHETIC_INPUT", "$", "source is not synthetic")
    record_class = record.get("record_class")
    if not isinstance(record_class, str) or not record_class.startswith(
        "CONSPICUOUSLY_SYNTHETIC_S6_H1_"
    ):
        raise ValidationFailure(
            "S6H1_NON_SYNTHETIC_INPUT", "$.record_class", "synthetic class required"
        )


def _check_screening_semantics(record: dict[str, Any]) -> None:
    exposures = set(record["exposure_states"].values())
    conflict = record["conflict_provenance"]
    eligibility = record["eligibility_state"]
    if (
        "DISCLOSED_EXPOSURE_CONTAMINATED" in exposures
        and eligibility != "CONTAMINATED_INELIGIBLE"
    ):
        raise ValidationFailure(
            "S6H1_CONTAMINATION_NOT_INELIGIBLE",
            "$.eligibility_state",
            "positive exposure must be ineligible",
        )
    if (
        "NOT_ASSESSED_FAIL_CLOSED" in exposures
        or conflict == "UNKNOWN_FAIL_CLOSED"
    ) and eligibility != "NOT_ASSESSED_FAIL_CLOSED":
        raise ValidationFailure(
            "S6H1_UNKNOWN_NOT_FAIL_CLOSED",
            "$.eligibility_state",
            "unknown exposure or conflict must fail closed",
        )
    if (
        conflict == "DISCLOSED_CONFLICT_CONTAMINATED"
        and eligibility != "CONTAMINATED_INELIGIBLE"
    ):
        raise ValidationFailure(
            "S6H1_CONFLICT_NOT_INELIGIBLE",
            "$.eligibility_state",
            "disclosed conflict must be ineligible",
        )


def _check_isolation_semantics(record: dict[str, Any]) -> None:
    if record["fresh_isolation_state"] != "ESTABLISHED_SYNTHETIC_TEST_ONLY":
        return
    checks = [
        record["environment"]["provenance_state"] == "COMPLETE_SYNTHETIC_TEST_PROVENANCE",
        record["session"]["history_state"] == "EMPTY_SYNTHETIC_TEST_HISTORY",
        record["retrieval"]["state"] == "DISABLED",
        record["actor"]["exposure_state"] == "DISCLOSED_NO_EXPOSURE",
        record["access"]["event_state"] == "NO_ACCESS_EVENTS",
    ]
    if not all(checks):
        raise ValidationFailure(
            "S6H1_ISOLATION_EVIDENCE_INCOMPLETE",
            "$.fresh_isolation_state",
            "isolation cannot be established with unknown provenance",
        )


def validate_record(
    schema_name: str,
    record: dict[str, Any],
    *,
    source: str = ALLOWED_SOURCE,
) -> None:
    """Validate one conspicuously synthetic record against a closed schema."""

    if schema_name not in SCHEMA_PATHS:
        raise ValidationFailure("S6H1_SCHEMA_REJECTED", "$", schema_name)
    _check_synthetic_boundary(record, source)
    schema = load_json(SCHEMA_PATHS[schema_name])
    _check_prohibited_fields(schema, record)
    _validate_schema(record, schema)
    if schema_name == "screening":
        _check_screening_semantics(record)
    else:
        _check_isolation_semantics(record)
