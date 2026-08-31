"""Closed test-only validator for conspicuously synthetic A1/GPT-heavy metadata.

This module validates custody, authority, role, and isolation invariants. It contains no
human-facing process, semantic content, real eligibility classifier, or production import.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "state" / "NATAL-TIME-A1-GPT-HEAVY-CUSTODY-SCHEMA-V1.json"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "a1_gpt_heavy"
ALLOWED_SOURCE = "CONSPICUOUSLY_SYNTHETIC_A1_GPT_HEAVY_FIXTURE"
VALIDATOR_VERSION = "a1-gpt-heavy-custody-test-validator-v1"


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
        raise ValidationFailure("A1G_FIXTURE_PATH_REJECTED", "$", name)
    value = load_json(FIXTURE_ROOT / name)
    if not isinstance(value, dict):
        raise ValidationFailure("A1G_TYPE_MISMATCH", "$", "fixture must be object")
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
            raise ValidationFailure("A1G_ONE_OF_VIOLATION", path, "expected exactly one match")
        return
    expected = schema.get("type")
    if expected is not None and not _type_matches(expected, value):
        raise ValidationFailure("A1G_TYPE_MISMATCH", path, f"expected {expected}")
    if "const" in schema and value != schema["const"]:
        raise ValidationFailure("A1G_CONST_VIOLATION", path, "closed constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise ValidationFailure("A1G_ENUM_VIOLATION", path, "outside closed vocabulary")
    if (
        isinstance(value, str)
        and "pattern" in schema
        and re.fullmatch(schema["pattern"], value) is None
    ):
        raise ValidationFailure("A1G_PATTERN_VIOLATION", path, "pattern mismatch")
    if (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value < schema.get("minimum", value)
    ):
        raise ValidationFailure("A1G_MINIMUM_VIOLATION", path, "below minimum")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for field in schema.get("required", []):
            if field not in value:
                raise ValidationFailure("A1G_REQUIRED_FIELD_MISSING", f"{path}.{field}", "required")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise ValidationFailure(
                    "A1G_UNKNOWN_FIELD", f"{path}.{unknown[0]}", "closed schema"
                )
        for field, nested in value.items():
            if field in properties:
                _validate_schema(nested, properties[field], f"{path}.{field}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValidationFailure("A1G_MIN_ITEMS_VIOLATION", path, "too few items")
        distinct = {json.dumps(item, sort_keys=True) for item in value}
        if schema.get("uniqueItems") and len(distinct) != len(value):
            raise ValidationFailure("A1G_UNIQUE_ITEMS_VIOLATION", path, "duplicate items")
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
        r"(?:astrohd|human[ _-]?design|birth[ _-]?chart|relationship[ _-]?chart|"
        r"construct[ _-]?description|screening[ _-]?question|mapping[ _-]?(?:hypothesis|result))",
        re.IGNORECASE,
    )
    email_value = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    for path, key, value in _all_items(record):
        if key in prohibited_fields:
            raise ValidationFailure("A1G_PROHIBITED_FIELD", path, "content embargo")
        if isinstance(value, str) and prohibited_value.search(value):
            raise ValidationFailure("A1G_PROHIBITED_VALUE", path, "content embargo")
        if isinstance(value, str) and email_value.fullmatch(value):
            raise ValidationFailure("A1G_PERSONAL_VALUE", path, "contact data prohibited")


def _check_authority_invariants(record: dict[str, Any]) -> None:
    transformations = record["transformations"]
    decision_events = {item["event_id"]: item for item in record["decision_events"]}
    clean_units = {item["unit_id"]: item for item in record["clean_units"]}
    semantic_kinds = {
        "GPT_PARAPHRASE_CANDIDATE",
        "GPT_CATEGORY_CANDIDATE",
        "GPT_LABEL_CANDIDATE",
        "GPT_SYNTHESIS_CANDIDATE",
    }
    for index, item in enumerate(transformations):
        path = f"$.transformations[{index}]"
        if item["kind"] == "EXACT_QUOTE_EXTRACTION" and item["source_offsets"] is None:
            raise ValidationFailure(
                "A1G_QUOTE_OFFSET_REQUIRED", f"{path}.source_offsets", "exact quote"
            )
        if (
            item["kind"] in {"EXACT_DUPLICATE_FLAG", "NEAR_DUPLICATE_FLAG"}
            and item["record_action"] != "FLAG_ONLY_PRESERVE_ALL"
        ):
            raise ValidationFailure(
                "A1G_DUPLICATE_FLAG_ONLY", f"{path}.record_action", "source deletion prohibited"
            )
        if item["kind"] in semantic_kinds:
            if not item["human_source_ids"]:
                raise ValidationFailure(
                    "A1G_HUMAN_SOURCE_REQUIRED", f"{path}.human_source_ids", "semantic derivative"
                )
            if item["authority_state"] == "JOEL_ACCEPTED_SOURCE_LINKED":
                event_id = item["decision_event_id"]
                if event_id is None or event_id not in decision_events:
                    raise ValidationFailure(
                        "A1G_ACCEPTANCE_EVENT_REQUIRED",
                        f"{path}.decision_event_id",
                        "accepted derivative",
                    )
                event = decision_events[event_id]
                if (
                    event["event_type"] != "JOEL_AUTHOR_SEMANTIC_DECISION"
                    or event["actor_role"] != "JOEL_AUTHOR"
                    or event["target_derivative_id"] != item["derivative_id"]
                    or event["decision"] != "ACCEPT"
                ):
                    raise ValidationFailure(
                        "A1G_ACCEPTANCE_EVENT_INVALID",
                        f"{path}.decision_event_id",
                        "wrong role or target",
                    )
            elif item["authority_state"] != "NONAUTHORITATIVE_PENDING_JOEL":
                raise ValidationFailure(
                    "A1G_SEMANTIC_AUTHORITY_INVALID",
                    f"{path}.authority_state",
                    "semantic derivative",
                )
        if item["kind"] == "GPT_SYNTHESIS_CANDIDATE":
            if not item["preserves_conflict"]:
                raise ValidationFailure(
                    "A1G_SYNTHESIS_CONFLICT_OMITTED",
                    f"{path}.preserves_conflict",
                    "conflict must remain",
                )
            if not item["accepted_unit_ids"] or not set(item["accepted_unit_ids"]).issubset(
                clean_units
            ):
                raise ValidationFailure(
                    "A1G_SYNTHESIS_UNIT_INVALID",
                    f"{path}.accepted_unit_ids",
                    "accepted unit required",
                )

    for index, event in enumerate(record["decision_events"]):
        path = f"$.decision_events[{index}]"
        if event["event_type"].startswith("JOEL_AUTHOR_") and event["actor_role"] != "JOEL_AUTHOR":
            raise ValidationFailure("A1G_ROLE_EVENT_MISMATCH", f"{path}.actor_role", "author event")
        if event["event_type"] == "JOEL_OWNER_GOVERNANCE_DECISION" and (
            event["actor_role"] != "JOEL_OWNER"
            or event["decision"] != "GOVERNANCE_ONLY"
            or event["target_derivative_id"] is not None
        ):
            raise ValidationFailure("A1G_ROLE_EVENT_MISMATCH", path, "owner event")

    for index, unit in enumerate(record["clean_units"]):
        event = decision_events.get(unit["decision_event_id"])
        if (
            event is None
            or event["actor_role"] != "JOEL_AUTHOR"
            or event["target_derivative_id"] != unit["derivative_id"]
            or event["decision"] != "ACCEPT"
        ):
            raise ValidationFailure(
                "A1G_CLEAN_UNIT_DECISION_INVALID", f"$.clean_units[{index}]", "human decision link"
            )

    attestation = decision_events.get(record["clean_freeze"]["final_fidelity_attestation_event_id"])
    if (
        attestation is None
        or attestation["event_type"] != "JOEL_AUTHOR_FINAL_FIDELITY_ATTESTATION"
        or attestation["actor_role"] != "JOEL_AUTHOR"
        or attestation["decision"] != "ATTEST_FIDELITY"
    ):
        raise ValidationFailure(
            "A1G_FINAL_ATTESTATION_INVALID",
            "$.clean_freeze.final_fidelity_attestation_event_id",
            "author attestation",
        )


def _check_adjudication_invariants(record: dict[str, Any]) -> None:
    adjudication = record["adjudication"]
    slots = adjudication["initial_slots"]
    if (
        len(slots) != 2
        or {item["slot_id"] for item in slots}
        != {"GPT_INITIAL_RUN_SLOT_A", "GPT_INITIAL_RUN_SLOT_B"}
        or len({item["run_id"] for item in slots}) != 2
        or len({item["context_id"] for item in slots}) != 2
    ):
        raise ValidationFailure(
            "A1G_RUN_CONTEXT_NOT_DISTINCT",
            "$.adjudication.initial_slots",
            "two distinct initial runs",
        )
    if len({item["access_event_id"] for item in slots}) != 2:
        raise ValidationFailure(
            "A1G_ACCESS_EVENT_NOT_DISTINCT",
            "$.adjudication.initial_slots",
            "separate access events",
        )
    outputs = {item["output_id"]: item for item in adjudication["outputs"]}
    packet_id = adjudication["evidence_packet"]["packet_id"]
    for item in slots:
        output = outputs.get(item["output_id"])
        if output is None or output["run_id"] != item["run_id"] or output["packet_id"] != packet_id:
            raise ValidationFailure(
                "A1G_OUTPUT_BINDING_INVALID", "$.adjudication.outputs", "run and packet binding"
            )
    reconciliation = adjudication["reconciliation"]
    if set(reconciliation["input_output_ids"]) != set(outputs):
        raise ValidationFailure(
            "A1G_RECONCILIATION_INPUT_INVALID",
            "$.adjudication.reconciliation.input_output_ids",
            "sealed outputs",
        )


def validate_record(record: dict[str, Any], *, source: str = ALLOWED_SOURCE) -> None:
    """Validate only synthetic metadata and fail closed on content or authority bypass."""

    if source != ALLOWED_SOURCE:
        raise ValidationFailure("A1G_NON_SYNTHETIC_INPUT", "$", "source boundary")
    if record.get("record_class") != "CONSPICUOUSLY_SYNTHETIC_A1_GPT_HEAVY_PACKAGE":
        raise ValidationFailure(
            "A1G_NON_SYNTHETIC_INPUT", "$.record_class", "synthetic class required"
        )
    schema = load_json(SCHEMA_PATH)
    _check_content_embargo(schema, record)
    _validate_schema(record, schema)
    _check_authority_invariants(record)
    _check_adjudication_invariants(record)
