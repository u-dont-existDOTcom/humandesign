"""Closed validator for conspicuously synthetic B1 pre-content metadata.

This module is test-only. Production code must never import it or the state schemas it reads.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "b1-precontent-synthetic-validator-v1"
ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
FIXTURES = ROOT / "tests" / "fixtures" / "b1_precontent"
ALLOWED_SOURCE = "CONSPICUOUSLY_SYNTHETIC_B1_FIXTURE"

SCHEMA_PATHS = {
    "content_embargo": STATE / "NATAL-TIME-B1-CONTENT-EMBARGO-SCHEMA-V1.json",
    "candidate": STATE / "NATAL-TIME-B1-CONSTRUCT-CANDIDATE-METADATA-SCHEMA-V1.json",
    "access": STATE / "NATAL-TIME-B1-ACCESS-AND-CONTAMINATION-SCHEMA-V1.json",
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
        raise ValidationFailure("B1_FIXTURE_PATH_REJECTED", "$", name)
    value = load_json(FIXTURES / name)
    if not isinstance(value, dict):
        raise ValidationFailure("B1_TYPE_MISMATCH", "$", "fixture must be an object")
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


def _prohibited_field_names() -> set[str]:
    schema = load_json(SCHEMA_PATHS["content_embargo"])
    return set(schema["x-prohibited-field-names"])


def _check_prohibited_fields(record: dict[str, Any]) -> None:
    prohibited = _prohibited_field_names()
    for key in _all_keys(record):
        if key in prohibited:
            raise ValidationFailure(
                "B1_PROHIBITED_FIELD", f"$.{key}", "content-bearing field is prohibited"
            )


def _check_synthetic_boundary(record: dict[str, Any], source: str) -> None:
    if source != ALLOWED_SOURCE:
        raise ValidationFailure("B1_NON_SYNTHETIC_INPUT", "$", "source is not synthetic")
    record_class = record.get("record_class")
    if not isinstance(record_class, str) or not record_class.startswith(
        "CONSPICUOUSLY_SYNTHETIC_B1_"
    ):
        raise ValidationFailure(
            "B1_NON_SYNTHETIC_INPUT",
            "$.record_class",
            "conspicuous synthetic record class required",
        )


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
        raise ValidationFailure("B1_TYPE_MISMATCH", path, f"expected {expected_type}")

    if "const" in schema and value != schema["const"]:
        raise ValidationFailure("B1_CONST_VIOLATION", path, "value differs from closed constant")

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationFailure("B1_ENUM_VIOLATION", path, "value outside closed vocabulary")

    if (
        isinstance(value, str)
        and "pattern" in schema
        and re.fullmatch(schema["pattern"], value) is None
    ):
        raise ValidationFailure("B1_PATTERN_VIOLATION", path, "pattern mismatch")

    if (
        isinstance(value, int)
        and not isinstance(value, bool)
        and "minimum" in schema
        and value < schema["minimum"]
    ):
        raise ValidationFailure("B1_RANGE_VIOLATION", path, "below minimum")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                raise ValidationFailure(
                    "B1_REQUIRED_FIELD_MISSING", f"{path}.{field}", "required field missing"
                )
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise ValidationFailure("B1_UNKNOWN_FIELD", f"{path}.{unknown[0]}", "closed schema")
        for field, nested in value.items():
            if field in properties:
                _validate_schema(nested, properties[field], f"{path}.{field}")

    if isinstance(value, list):
        if schema.get("uniqueItems") and len(
            {json.dumps(item, sort_keys=True) for item in value}
        ) != len(value):
            raise ValidationFailure("B1_DUPLICATE_ITEM", path, "items must be unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, nested in enumerate(value):
                _validate_schema(nested, item_schema, f"{path}[{index}]")


def _check_semantics(schema_name: str, record: dict[str, Any]) -> None:
    contamination = record.get("contamination_state")
    exposure = record.get("astrohd_exposure_state")
    if exposure in {"UNKNOWN_FAIL_CLOSED", "EXPOSED_CONTAMINATED"} and contamination == (
        "CLEAN_SYNTHETIC_METADATA_ONLY"
    ):
        raise ValidationFailure(
            "B1_EXPOSURE_CONTAMINATION_REQUIRED",
            "$.contamination_state",
            "unknown or positive exposure cannot remain clean",
        )

    if (
        schema_name == "candidate"
        and record["source_provenance_status"] == "UNKNOWN_FAIL_CLOSED"
        and contamination == "CLEAN_SYNTHETIC_METADATA_ONLY"
    ):
        raise ValidationFailure(
            "B1_UNKNOWN_PROVENANCE",
            "$.source_provenance_status",
            "unknown provenance fails closed",
        )

    if schema_name == "access":
        if record["event_sequence"] == 0 and record["previous_event_digest"] != "GENESIS":
            raise ValidationFailure(
                "B1_HISTORY_CHAIN_INVALID",
                "$.previous_event_digest",
                "first event requires GENESIS",
            )
        if record["event_sequence"] > 0 and record["previous_event_digest"] == "GENESIS":
            raise ValidationFailure(
                "B1_HISTORY_CHAIN_INVALID",
                "$.previous_event_digest",
                "later event requires prior digest",
            )
        mapping_roles = {"MAPPING", "MAPPING_EVALUATION", "INCREMENTAL_VALUE_EVALUATION"}
        if record["actor_role_id"] in mapping_roles and contamination == (
            "CLEAN_SYNTHETIC_METADATA_ONLY"
        ):
            raise ValidationFailure(
                "B1_PRE_FREEZE_MAPPING_ACCESS",
                "$.actor_role_id",
                "mapping-role access cannot remain clean in the pre-content slice",
            )


def validate_record(
    schema_name: str,
    record: dict[str, Any],
    *,
    source: str = ALLOWED_SOURCE,
) -> None:
    """Validate one conspicuously synthetic record against a closed schema."""

    if schema_name not in SCHEMA_PATHS:
        raise ValidationFailure("B1_SCHEMA_REJECTED", "$", schema_name)
    _check_synthetic_boundary(record, source)
    _check_prohibited_fields(record)
    schema = load_json(SCHEMA_PATHS[schema_name])
    _validate_schema(record, schema)
    _check_semantics(schema_name, record)


def validate_access_history(records: list[dict[str, Any]]) -> None:
    """Validate append-only order, hash linkage, monotonic contamination, and role crossings."""

    if not records:
        raise ValidationFailure("B1_HISTORY_EMPTY", "$", "at least one synthetic event required")
    for record in records:
        validate_record("access", record)

    ordered = sorted(records, key=lambda item: item["event_sequence"])
    if [item["event_sequence"] for item in ordered] != list(range(len(ordered))):
        raise ValidationFailure("B1_HISTORY_SEQUENCE_INVALID", "$", "sequence must be contiguous")

    candidate_ids = {item["synthetic_candidate_id"] for item in ordered}
    if len(candidate_ids) != 1:
        raise ValidationFailure("B1_HISTORY_CANDIDATE_MISMATCH", "$", "one candidate required")

    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current["previous_event_digest"] != previous["access_event_digest"]:
            raise ValidationFailure(
                "B1_HISTORY_CHAIN_INVALID",
                "$.previous_event_digest",
                "event chain digest mismatch",
            )

    contamination_rank = {
        "CLEAN_SYNTHETIC_METADATA_ONLY": 0,
        "UNKNOWN_FAIL_CLOSED": 1,
        "CONTAMINATED_INELIGIBLE": 2,
    }
    ranks = [contamination_rank[item["contamination_state"]] for item in ordered]
    if ranks != sorted(ranks):
        raise ValidationFailure(
            "B1_CONTAMINATION_NOT_MONOTONIC",
            "$.contamination_state",
            "history cannot become cleaner",
        )

    development_roles = {
        "CHART_BLIND_AUTHORSHIP",
        "CONSTRUCT_SOURCE_REVIEW",
        "MEASUREMENT_DEVELOPMENT",
        "RELIABILITY_ANALYSIS",
    }
    mapping_roles = {"MAPPING", "MAPPING_EVALUATION", "INCREMENTAL_VALUE_EVALUATION"}
    roles = {item["actor_role_id"] for item in ordered}
    if roles & development_roles and roles & mapping_roles and ranks[-1] == 0:
        raise ValidationFailure(
            "B1_CROSS_ROLE_CONTAMINATION_REQUIRED",
            "$.actor_role_id",
            "incompatible role crossing requires contamination",
        )
