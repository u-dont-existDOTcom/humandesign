"""Deterministic consent/coverage admission for the OPTIONAL experience pilot.

Never interpret missing topics as low scores. Source equivalence must be evidenced,
not guessed from nearby chart or decision-making constructs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
BANK = HERE / "EXPERIENCE-MEANING-PILOT-v1.json"
ANSWER_STATES = frozenset(
    {"ANSWERED", "NEVER", "UNKNOWN", "SKIPPED", "ALREADY_COVERED", "NOT_ASKED"}
)


def instrument() -> dict[str, Any]:
    return json.loads(BANK.read_text(encoding="utf-8"))


def plan_questions(
    *,
    consent: bool,
    requested_optional_ids: list[str] | None = None,
    covered_sources: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return planned prompts and separately recorded sourced skips.

    covered_sources is supplied by a human/source-audited interviewer.
    A blank citation never counts as equivalent coverage. No NLP guess is made.
    """
    bank = instrument()
    items = {item["id"] for item in bank["items"]}
    optional = set(bank["other_prompt_order"])
    requested = requested_optional_ids or []
    covered = covered_sources or {}
    if len(requested) != len(set(requested)) or not set(requested) <= optional:
        raise ValueError("Unexpected or duplicate optional question ID")
    if len(requested) > bank["max_additional_topics"]:
        raise ValueError("Too many optional pilot topics")
    if any(key not in items for key in covered):
        raise ValueError("Unknown covered-source question ID")
    if not consent:
        return {
            "consent": False,
            "queue": [],
            "covered": {},
            "not_asked": sorted(items),
        }
    proposed = bank["prompt_order"] + [x for x in bank["other_prompt_order"] if x in requested]
    verified = {k: v.strip() for k, v in covered.items() if isinstance(v, str) and v.strip()}
    return {
        "consent": True,
        "queue": [q for q in proposed if q not in verified],
        "covered": {q: verified[q] for q in proposed if q in verified},
        "not_asked": sorted(items - set(proposed)),
    }


def normalize_answer(question_id: str, answer: dict[str, Any]) -> dict[str, Any]:
    """Retain epistemic distinctions. Do not auto-score or impute intensity."""
    bank = instrument()
    item = next((i for i in bank["items"] if i["id"] == question_id), None)
    if item is None:
        raise ValueError("Unknown question")
    state = answer.get("state")
    if state not in ANSWER_STATES - {"NOT_ASKED"}:
        raise ValueError("Invalid recorded answer state")
    if state == "ALREADY_COVERED":
        if not isinstance(answer.get("source_ref"), str) or not answer["source_ref"].strip():
            raise ValueError("Already-covered needs an actual source reference")
        return {
            "question_id": question_id,
            "state": state,
            "source_ref": answer["source_ref"].strip(),
        }
    if state in {"SKIPPED", "UNKNOWN", "NEVER"}:
        return {"question_id": question_id, "state": state}
    result: dict[str, Any] = {"question_id": question_id, "state": "ANSWERED"}
    if item["mode"] == "dual_meaning":
        allowed = {choice[0] for choice in bank["meaning_options"]}
        values = answer.get("values") or {}
        if (
            not isinstance(values, dict)
            or set(values) != {"personal_meaning", "perceived_contribution"}
        ):
            raise ValueError("Meaning and contribution need two separate responses")
        if any(v not in allowed for v in values.values()):
            raise ValueError("Invalid meaning option")
        result["values"] = values.copy()
    else:
        choices = (
            bank["frequency_options"]
            if item["mode"] == "frequency"
            else bank["predictability_options"]
        )
        allowed = {choice[0] for choice in choices} - {"skip", "unknown"}
        value = answer.get("value")
        if value not in allowed:
            raise ValueError("Missing/invalid main response (use UNKNOWN or SKIPPED state)")
        if item["mode"] == "frequency" and value == "never":
            return {"question_id": question_id, "state": "NEVER"}
        result["value"] = value
        if item["mode"] == "frequency" and answer.get("intensity"):
            options = {x[0] for x in bank["intensity_options"]}
            if answer["intensity"] not in options:
                raise ValueError("Invalid intensity")
            result["intensity"] = answer["intensity"]
    if answer.get("note"):
        if not isinstance(answer["note"], str):
            raise ValueError("Notes must be free text")
        result["note"] = answer["note"]
    return result


def could_ask_followup(answer: dict[str, Any]) -> bool:
    """The follow-up remains optional; never/unknown/skip is a complete response."""
    return answer.get("state") == "ANSWERED"
