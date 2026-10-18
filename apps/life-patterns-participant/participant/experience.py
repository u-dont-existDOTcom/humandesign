"""Separate, opt-in lived-experience evidence for GPT/Railway completion.

Never merge into primary interview / CF003, never change chart prediction scores.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .domain import target_exposure

BANK_PATH = Path(__file__).parent / "static/experience-meaning-v2.json"
RECORD_SCHEMA = "life-patterns-experience-meaning-addendum-v2"
INSTRUMENT = "experience-meaning-v2-20261017"
STATES = {"ANSWERED", "NEVER", "UNKNOWN", "SKIPPED", "NOT_ASKED", "ALREADY_COVERED"}
RESPONSE_KEYS = {
    "question_id", "state", "value", "values", "typical_intensity",
    "peak_intensity", "note", "source_ref",
}
RECORD_KEYS = {
    "schema", "instrument", "research_use_consented", "collection_mode",
    "status", "topics_selected", "responses",
}


def instrument() -> dict[str, Any]:
    data = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    assert data["version"] == INSTRUMENT
    assert [item["id"] for item in data["items"]] == [
        "EM01", "EM02", "EM03", "EM04", "EM05", "EM06", "EM07", "EM08"
    ]
    return data


def public_instrument() -> dict[str, Any]:
    bank = instrument()
    return {
        key: bank[key] for key in (
            "schema", "version", "consent_text", "core_ids", "optional_ids",
            "items", "frequency_options", "intensity_options",
            "predictability_options", "meaning_options", "context_note",
        )
    }


def _choice(value: Any, options: list, *, allow_none: bool = False) -> bool:
    if value is None:
        return allow_none
    return type(value) is str and value in {row[0] for row in options}


def validate_experience_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) - RECORD_KEYS:
        raise ValueError("Unexpected experience record fields.")
    if (
        record.get("schema") != RECORD_SCHEMA
        or record.get("instrument") != INSTRUMENT
        or record.get("research_use_consented") is not True
        or record.get("collection_mode") not in ("railway_finish", "gpt_optional")
        or record.get("status") != "post_review_exploratory_not_scored"
    ):
        raise ValueError("Experience answers require their own opt-in and version.")
    bank = instrument()
    ids = {item["id"] for item in bank["items"]}
    items = {item["id"]: item for item in bank["items"]}
    selected = record.get("topics_selected")
    if (
        not isinstance(selected, list)
        or any(type(s) is not str or s not in bank["optional_ids"] for s in selected)
        or len(selected) != len(set(selected))
    ):
        raise ValueError("Unexpected experience topic selection.")
    responses = record.get("responses")
    if not isinstance(responses, list) or not (1 <= len(responses) <= 8):
        raise ValueError("Experience responses must be a bounded list.")
    found: set[str] = set()
    for response in responses:
        if not isinstance(response, dict) or set(response) - RESPONSE_KEYS:
            raise ValueError("Unexpected experience answer fields.")
        qid, state = response.get("question_id"), response.get("state")
        if type(qid) is not str or qid not in ids or qid in found:
            raise ValueError("Unknown or duplicate experience question.")
        found.add(qid)
        if state not in STATES:
            raise ValueError("Invalid experience evidence state.")
        mode = items[qid]["mode"]
        if qid in bank["optional_ids"] and qid not in selected and state != "NOT_ASKED":
            raise ValueError("Unselected experience topics must remain NOT_ASKED.")
        if state != "ANSWERED":
            allowed = {"question_id", "state"}
            if state in {"NEVER", "UNKNOWN", "SKIPPED"} and "note" in response:
                note = response["note"]
                if not isinstance(note, str) or len(note) > 4000 or target_exposure(note):
                    raise ValueError("Invalid contextual note.")
                allowed.add("note")
            if state == "ALREADY_COVERED":
                allowed.add("source_ref")
                if (
                    not isinstance(response.get("source_ref"), str)
                    or not response["source_ref"].strip()
                    or len(response["source_ref"]) > 500
                ):
                    raise ValueError("A covered experience needs an exact earlier source.")
            if set(response) - allowed:
                raise ValueError("Skipped, unknown and never responses cannot imply intensity.")
            if state == "NEVER" and mode != "frequency":
                raise ValueError("Never is a frequency outcome, not a meaning score.")
            continue
        note = response.get("note")
        if note is not None and (
            not isinstance(note, str) or len(note) > 4000 or target_exposure(note)
        ):
            raise ValueError("Experience context cannot contain birth/chart data.")
        allowed = {"question_id", "state", "note"}
        if mode == "frequency":
            allowed |= {"value", "typical_intensity", "peak_intensity"}
            if not _choice(response.get("value"), bank["frequency_options"]):
                raise ValueError("Missing/invalid experience frequency.")
            if response["value"] in ("never", "unknown", "skip"):
                raise ValueError("Use NEVER, UNKNOWN or SKIPPED as separate evidence states.")
            for key in ("typical_intensity", "peak_intensity"):
                if key in response and not _choice(
                    response[key], bank["intensity_options"]
                ):
                    raise ValueError(f"Invalid {key}.")
        elif mode == "predictability":
            allowed.add("value")
            if not _choice(response.get("value"), bank["predictability_options"]):
                raise ValueError("Missing/invalid predictability.")
            if response["value"] in ("unknown", "skip"):
                raise ValueError("Unknown and skipped require their separate evidence state.")
        elif mode == "dual_meaning":
            allowed.add("values")
            values = response.get("values")
            if (
                not isinstance(values, dict)
                or set(values) != {"personal_meaning", "perceived_contribution"}
                or not all(_choice(v, bank["meaning_options"]) for v in values.values())
                or all(value == "not_answered" for value in values.values())
            ):
                raise ValueError("Meaning and contribution require distinct responses.")
        if set(response) - allowed:
            raise ValueError("Question response contains incompatible dimensions.")
    # Canonical presentation requires every item; never invent a negative answer.
    if found != ids:
        raise ValueError("Include all eight IDs, with NOT_ASKED for unanswered topics.")
    return record
