"""Closed test-only validator for conspicuously synthetic P1 metadata.

This validates schema shape and the content embargo. It deliberately contains no rule that
derives a substantive outcome for a human or synthetic case.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "state" / "NATAL-TIME-P1-EVIDENCE-CLASSIFICATION-SCHEMA-V1.json"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "p1_adjudication"
ALLOWED_SOURCE = "CONSPICUOUSLY_SYNTHETIC_P1_FIXTURE"
VALIDATOR_VERSION = "p1-adjudication-schema-only-validator-v1"


@dataclass(frozen=True)
class ValidationFailure(Exception):
    """A controlled fail-closed result."""

    code: str
    path: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}:{self.path}:{self.detail}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture(name: str) -> dict[str, Any]:
    if Path(name).name != name or not name.endswith(".json"):
        raise ValidationFailure("P1_FIXTURE_PATH_REJECTED", "$", name)
    value = load_json(FIXTURE_ROOT / name)
    if not isinstance(value, dict):
        raise ValidationFailure("P1_TYPE_MISMATCH", "$", "fixture must be object")
    return value


def _type_matches(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "oneOf" in schema:
        matches = 0
        for candidate in schema["oneOf"]:
            try:
                _validate_schema(value, candidate, path)
            except ValidationFailure:
                continue
            matches += 1
        if matches != 1:
            raise ValidationFailure("P1_ONE_OF_VIOLATION", path, "expected exactly one match")
        return
    expected = schema.get("type")
    if expected is not None and not _type_matches(expected, value):
        raise ValidationFailure("P1_TYPE_MISMATCH", path, f"expected {expected}")
    if "const" in schema and value != schema["const"]:
        raise ValidationFailure("P1_CONST_VIOLATION", path, "closed constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise ValidationFailure("P1_ENUM_VIOLATION", path, "outside closed vocabulary")
    if (
        isinstance(value, str)
        and "pattern" in schema
        and re.fullmatch(schema["pattern"], value) is None
    ):
        raise ValidationFailure("P1_PATTERN_VIOLATION", path, "pattern mismatch")
    if (
        isinstance(value, int)
        and not isinstance(value, bool)
        and "minimum" in schema
        and value < schema["minimum"]
    ):
        raise ValidationFailure("P1_MINIMUM_VIOLATION", path, "below minimum")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for field in schema.get("required", []):
            if field not in value:
                raise ValidationFailure("P1_REQUIRED_FIELD_MISSING", f"{path}.{field}", "required")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise ValidationFailure("P1_UNKNOWN_FIELD", f"{path}.{unknown[0]}", "closed schema")
        for field, nested in value.items():
            if field in properties:
                _validate_schema(nested, properties[field], f"{path}.{field}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValidationFailure("P1_MIN_ITEMS_VIOLATION", path, "too few items")
        distinct_items = {json.dumps(item, sort_keys=True) for item in value}
        if schema.get("uniqueItems") and len(distinct_items) != len(value):
            raise ValidationFailure("P1_UNIQUE_ITEMS_VIOLATION", path, "duplicate items")
        if "items" in schema:
            for index, nested in enumerate(value):
                _validate_schema(nested, schema["items"], f"{path}[{index}]")


def _all_items(value: Any, path: str = "$") -> list[tuple[str, str, Any]]:
    items: list[tuple[str, str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            items.append((nested_path, key, nested))
            items.extend(_all_items(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            items.extend(_all_items(nested, f"{path}[{index}]"))
    return items


def _check_content_embargo(schema: dict[str, Any], record: dict[str, Any]) -> None:
    prohibited_fields = set(schema["x-prohibited-field-names"])
    prohibited_value = re.compile(
        r"(?:astrohd|human[ _-]?design|birth[ _-]?time|candidate[ _-]?interval|"
        r"relationship[ _-]?datum|construct[ _-]?description|screening[ _-]?question)",
        re.IGNORECASE,
    )
    email_value = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    for path, key, value in _all_items(record):
        if key in prohibited_fields:
            raise ValidationFailure("P1_PROHIBITED_FIELD", path, "content embargo")
        if isinstance(value, str) and prohibited_value.search(value):
            raise ValidationFailure("P1_PROHIBITED_VALUE", path, "content embargo")
        if isinstance(value, str) and email_value.fullmatch(value):
            raise ValidationFailure("P1_PERSONAL_VALUE", path, "contact data prohibited")


def validate_record(record: dict[str, Any], *, source: str = ALLOWED_SOURCE) -> None:
    """Validate synthetic metadata without deriving or checking an outcome algorithm."""

    if source != ALLOWED_SOURCE:
        raise ValidationFailure("P1_NON_SYNTHETIC_INPUT", "$", "source boundary")
    if record.get("record_class") != "CONSPICUOUSLY_SYNTHETIC_P1_EVIDENCE_PACKAGE":
        raise ValidationFailure(
            "P1_NON_SYNTHETIC_INPUT", "$.record_class", "synthetic class required"
        )
    schema = load_json(SCHEMA_PATH)
    _check_content_embargo(schema, record)
    _validate_schema(record, schema)
