"""Closed, standard-library-only validator for conspicuously synthetic Option B fixtures.

This module is test-only. Production code must never import it or the schemas it reads.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "option-b-synthetic-validator-v1"
ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
FIXTURES = ROOT / "tests" / "fixtures" / "option_b"

SCHEMA_PATHS = {
    "administration": STATE / "NATAL-TIME-MEASUREMENT-RELIABILITY-ADMINISTRATION-SCHEMA-V1.json",
    "coding": STATE / "NATAL-TIME-MEASUREMENT-RELIABILITY-CODING-SCHEMA-V1.json",
    "property_plan": STATE / "NATAL-TIME-MEASUREMENT-RELIABILITY-PROPERTY-PLAN-SCHEMA-V1.json",
}
CONTRACT_PATH = STATE / "NATAL-TIME-MEASUREMENT-RELIABILITY-CONTRACT-V1.json"
ALLOWED_SOURCE = "CONSPICUOUSLY_SYNTHETIC_FIXTURE"


@dataclass(frozen=True)
class ValidationFailure(Exception):
    """A controlled fail-closed synthetic validation result."""

    code: str
    path: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}:{self.path}:{self.detail}"


def load_json(path: Path) -> Any:
    """Read one committed test or state artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture(name: str) -> dict[str, Any]:
    """Load a fixture only from the dedicated synthetic fixture directory."""

    if Path(name).name != name or not name.endswith(".json"):
        raise ValidationFailure("OB_FIXTURE_PATH_REJECTED", "$", name)
    value = load_json(FIXTURES / name)
    if not isinstance(value, dict):
        raise ValidationFailure("OB_TYPE_MISMATCH", "$", "fixture must be an object")
    return value


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


def _check_synthetic_boundary(record: dict[str, Any], source: str) -> None:
    if source != ALLOWED_SOURCE:
        raise ValidationFailure("OB_NON_SYNTHETIC_INPUT", "$", "source is not synthetic")
    record_class = record.get("record_class")
    if not isinstance(record_class, str) or not record_class.startswith("CONSPICUOUSLY_SYNTHETIC_"):
        raise ValidationFailure(
            "OB_NON_SYNTHETIC_INPUT", "$.record_class", "synthetic record class required"
        )

    for field in ("synthetic_participant_id", "synthetic_component_id", "synthetic_coder_id"):
        value = record.get(field)
        if value is not None and (not isinstance(value, str) or not value.startswith("SYNTH-")):
            raise ValidationFailure(
                "OB_SYNTHETIC_ID_REQUIRED", f"$.{field}", "conspicuous synthetic ID required"
            )


def _check_prohibited_fields(record: dict[str, Any]) -> None:
    contract = load_json(CONTRACT_PATH)
    prohibited = set(contract["prohibited_fields"])
    for key in _all_keys(record):
        if key in prohibited:
            raise ValidationFailure("OB_PROHIBITED_FIELD", f"$.{key}", "field is prohibited")


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
    expected_type = schema.get("type")
    if expected_type is not None and not _type_matches(expected_type, value):
        raise ValidationFailure("OB_TYPE_MISMATCH", path, f"expected {expected_type}")

    if "const" in schema and value != schema["const"]:
        raise ValidationFailure("OB_CONST_VIOLATION", path, "value differs from closed constant")

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationFailure("OB_ENUM_VIOLATION", path, "value is outside closed vocabulary")

    if (
        isinstance(value, str)
        and "pattern" in schema
        and re.fullmatch(schema["pattern"], value) is None
    ):
        raise ValidationFailure("OB_PATTERN_VIOLATION", path, "pattern mismatch")

    if (
        isinstance(value, int)
        and not isinstance(value, bool)
        and "minimum" in schema
        and value < schema["minimum"]
    ):
        raise ValidationFailure("OB_RANGE_VIOLATION", path, "below minimum")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                raise ValidationFailure(
                    "OB_REQUIRED_FIELD_MISSING", f"{path}.{field}", "required field missing"
                )
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise ValidationFailure("OB_UNKNOWN_FIELD", f"{path}.{unknown[0]}", "closed schema")
        for field, nested in value.items():
            if field in properties:
                _validate_schema(nested, properties[field], f"{path}.{field}")

    if isinstance(value, list):
        if schema.get("uniqueItems") and len(
            {json.dumps(item, sort_keys=True) for item in value}
        ) != len(value):
            raise ValidationFailure("OB_DUPLICATE_ITEM", path, "items must be unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, nested in enumerate(value):
                _validate_schema(nested, item_schema, f"{path}[{index}]")


def _check_semantics(schema_name: str, record: dict[str, Any]) -> None:
    if schema_name == "coding":
        if record["prior_code_visibility"] and record["contamination_status"] == "CLEAN_SYNTHETIC":
            raise ValidationFailure(
                "OB_VISIBILITY_CONTAMINATION_REQUIRED",
                "$.contamination_status",
                "prior-code visibility cannot remain clean",
            )
        if record["adjudication_status"] == "PROHIBITED_REWRITE_ATTEMPT":
            raise ValidationFailure(
                "OB_ORIGINAL_COMMITMENT_REWRITE",
                "$.adjudication_status",
                "adjudication cannot rewrite original commitments",
            )

    if schema_name == "administration":
        contaminated = record["contamination_status"] != "CLEAN_SYNTHETIC"
        exposed = record["prior_feedback_or_chart_exposure"] != "NONE_RECORDED"
        if (record["prior_response_visibility"] or exposed) and not contaminated:
            raise ValidationFailure(
                "OB_VISIBILITY_CONTAMINATION_REQUIRED",
                "$.contamination_status",
                "exposure cannot remain clean",
            )
        missing = record["missingness_class"] != "NOT_MISSING"
        if missing and record["missingness_reason_provenance"] == "NOT_APPLICABLE":
            raise ValidationFailure(
                "OB_MISSINGNESS_PROVENANCE_REQUIRED",
                "$.missingness_reason_provenance",
                "missingness requires reason provenance",
            )


def validate_record(
    schema_name: str,
    record: dict[str, Any],
    *,
    source: str = ALLOWED_SOURCE,
) -> None:
    """Validate one conspicuously synthetic record against a closed test-only schema."""

    if schema_name not in SCHEMA_PATHS:
        raise ValidationFailure("OB_SCHEMA_REJECTED", "$", schema_name)
    _check_synthetic_boundary(record, source)
    _check_prohibited_fields(record)
    schema = load_json(SCHEMA_PATHS[schema_name])
    _validate_schema(record, schema)
    _check_semantics(schema_name, record)
