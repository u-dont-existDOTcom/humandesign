"""Separate, optional source addendum; never primary evidence or chart scoring.

The runtime contains only a neutral projection of existing question wording.
Validation verifies shape and source references, not the semantic adequacy of an
answer, true blinding, a trait, or a scientific measurement claim.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

BANK_PATH = Path(__file__).parent / "static/shared-life-topics-v3.json"
INSTRUMENT = "shared-life-topics-v3-20261026"
RECORD_SCHEMA = "life-patterns-shared-evidence-addendum-v1"
MAX_SERIALIZED_BYTES = 250_000
STATES = {
    "ANSWERED",
    "CONTEXT_DEPENDENT",
    "NO_OPPORTUNITIES",
    "NEVER",
    "NOT_APPLICABLE",
    "UNCERTAIN",
    "SKIPPED",
    "ALREADY_COVERED",
    "NOT_ASKED",
    "FUTURE_PENDING",
}
ELABORATABLE = {"ANSWERED", "CONTEXT_DEPENDENT", "UNCERTAIN"}
NO_ANSWER = {"NOT_ASKED", "SKIPPED", "FUTURE_PENDING", "ALREADY_COVERED"}
RECORD_KEYS = {
    "schema",
    "instrument",
    "research_use_consented",
    "collection_mode",
    "status",
    "sittings",
}
SITTING_KEYS = {"sitting_id", "topics_selected", "probe_admissions", "responses"}
ADMISSION_KEYS = {"probe_id", "parent_topic_id", "unresolved_distinction"}
RESPONSE_KEYS = {
    "question_id",
    "prompt_kind",
    "state",
    "question_text",
    "answer_text",
    "source_ref",
    "source_quote",
    "unresolved_distinction",
    "process_feedback",
}


def public_instrument() -> dict[str, Any]:
    """Return the explicitly whitelisted participant bank, with fresh objects."""
    data = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if (
        data.get("version") != INSTRUMENT
        or len(data.get("questions", [])) != 23
        or len(data.get("optional_microprobes", [])) != 7
    ):
        raise ValueError("The optional shared question bank did not verify.")
    return data


def explicit_target_exposure(text: str) -> bool:
    """Conservative explicit-language guard; ordinary event dates are allowed.

    A numeric date beside a clock time does not establish birth/chart exposure.
    This is not a semantic classifier and does not certify source blinding.
    """
    return bool(
        re.search(
            r"\b(?:I was born|my (?:birth date|date of birth|birth time|birthplace|"
            r"natal chart|birth chart|rising sign)|date of birth|birth[ -]?date|"
            r"birth[ -]?time|birthplace|natal chart|birth chart|human design|DOB)\b",
            text,
            re.I,
        )
    )


def experience_source_catalog(record: dict | None) -> list[dict[str, str]]:
    """Expose exact eligible notes from a valid, separately consented record.

    Structured choices are not converted into prose. Skips, unasked items and
    prior-source references are not new notes and never create reuse chains.
    """
    if record is None:
        return []
    from .experience import public_instrument as experience_instrument
    from .experience import validate_experience_record

    try:
        validated = validate_experience_record(record)
    except (TypeError, KeyError) as exc:
        raise ValueError("The optional experience source record is malformed.") from exc
    questions = {item["id"]: item["question"] for item in experience_instrument()["items"]}
    result: list[dict[str, str]] = []
    for index, response in enumerate(validated["responses"]):
        note = response.get("note")
        if (
            response["state"] not in {"ANSWERED", "NEVER", "UNKNOWN"}
            or not isinstance(note, str)
            or not note.strip()
            or explicit_target_exposure(note)
        ):
            continue
        result.append(
            {
                "source_ref": f"/experience/responses/{index}/note",
                "question_text": questions[response["question_id"]],
                "answer_text": note,
            }
        )
    return result


def source_catalog(
    primary: dict | None,
    cf003: dict | None = None,
    experience_record: dict | None = None,
) -> list[dict[str, str]]:
    """Enumerate exact usable source text; never metadata or inferred summaries.

    Explicitly superseded originals remain in their frozen records but cannot be
    selected as sole reuse support. A correction's exact text may be selected.
    """
    result: list[dict[str, str]] = []
    for label, record in (("primary", primary), ("cf003", cf003)):
        if not isinstance(record, dict) or not isinstance(record.get("turns"), list):
            continue
        turns = record["turns"]
        superseded = {
            str(row["correction_of"])
            for row in turns
            if isinstance(row, dict) and row.get("correction_of") is not None
        }
        for index, row in enumerate(turns):
            if not isinstance(row, dict):
                continue
            answer = row.get("answer_text")
            if (
                row.get("turn_role", "behavioral") != "behavioral"
                or row.get("quarantined")
                or row.get("answer_status") in ("skipped", "process_only")
                or (row.get("turn_id") is not None and str(row["turn_id"]) in superseded)
                or not isinstance(answer, str)
                or not answer.strip()
                or explicit_target_exposure(answer)
                or (
                    isinstance(row.get("question_text"), str)
                    and explicit_target_exposure(row["question_text"])
                )
            ):
                continue
            question = row.get("question_text")
            result.append(
                {
                    "source_ref": f"/{label}/turns/{index}/answer_text",
                    "question_text": question if isinstance(question, str) else "",
                    "answer_text": answer,
                }
            )
    return result + experience_source_catalog(experience_record)


def _object(value: Any, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) - keys:
        raise ValueError(f"Unexpected {label} fields.")
    return value


def _text(value: Any, label: str, maximum: int = 20_000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{label} must be nonempty bounded source text.")
    if explicit_target_exposure(value):
        raise ValueError("Keep explicit birth/chart information out of this addendum.")
    return value


def validate_shared_evidence_record(
    record: Any,
    *,
    primary_record: dict | None = None,
    cf003_record: dict | None = None,
    experience_record: dict | None = None,
) -> dict[str, Any]:
    """Validate and return the exact received object without rewriting evidence."""
    _object(record, RECORD_KEYS, "shared evidence record")
    if (
        record.get("schema") != RECORD_SCHEMA
        or record.get("instrument") != INSTRUMENT
        or record.get("research_use_consented") is not True
        or record.get("collection_mode") not in ("gpt_optional", "railway_finish")
        or record.get("status") != "post_review_development_not_scored"
    ):
        raise ValueError("Shared evidence requires its own opt-in and development version.")
    try:
        size = len(json.dumps(record, ensure_ascii=False, allow_nan=False).encode("utf-8"))
    except (ValueError, TypeError) as exc:
        raise ValueError("Shared evidence must be ordinary JSON.") from exc
    if size > MAX_SERIALIZED_BYTES:
        raise ValueError("The shared evidence record exceeds its transport size limit.")
    bank = public_instrument()
    topics = {row["id"]: row for row in bank["questions"]}
    probes = {row["id"]: row for row in bank["optional_microprobes"]}
    items = {**topics, **probes}
    sources = {
        row["source_ref"]: row["answer_text"]
        for row in source_catalog(
            primary_record,
            cf003_record,
            experience_record,
        )
    }
    sittings = record.get("sittings")
    if not isinstance(sittings, list) or not sittings:
        raise ValueError("An opted-in addendum needs at least one voluntary sitting.")
    sitting_ids: set[str] = set()
    prior_main: dict[str, str] = {}
    for sitting_index, sitting in enumerate(sittings):
        _object(sitting, SITTING_KEYS, "sitting")
        sid = sitting.get("sitting_id")
        if (
            not isinstance(sid, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", sid)
            or sid in sitting_ids
        ):
            raise ValueError("Every sitting needs its own stable identifier.")
        sitting_ids.add(sid)
        selected = sitting.get("topics_selected")
        if (
            not isinstance(selected, list)
            or not 1 <= len(selected) <= 5
            or any(not isinstance(qid, str) or qid not in topics for qid in selected)
            or len(set(selected)) != len(selected)
        ):
            raise ValueError("Choose one to five distinct optional topics per sitting.")
        if any(prior_main.get(qid) not in {None, "NOT_ASKED"} for qid in selected):
            raise ValueError(
                "Answered, covered or skipped topics cannot reopen in another sitting."
            )
        admitted = sitting.get("probe_admissions", [])
        if not isinstance(admitted, list) or len(admitted) > 2:
            raise ValueError("At most two conditional probes may be admitted per sitting.")
        admissions: dict[str, dict] = {}
        for admission in admitted:
            _object(admission, ADMISSION_KEYS, "probe admission")
            pid, parent = admission.get("probe_id"), admission.get("parent_topic_id")
            if (
                not isinstance(pid, str)
                or pid not in probes
                or pid in admissions
                or not isinstance(parent, str)
                or parent not in selected
                or parent not in probes[pid]["related_topics"]
                or pid not in topics[parent]["conditional_new_probe_ids"]
                or prior_main.get(pid) not in {None, "NOT_ASKED"}
            ):
                raise ValueError("A probe needs an eligible selected parent and unique identity.")
            _text(admission.get("unresolved_distinction"), "Unresolved distinction", 1000)
            admissions[pid] = admission
        responses = sitting.get("responses")
        if not isinstance(responses, list) or len(responses) > 2 * (
            len(selected) + len(admissions)
        ):
            raise ValueError("Responses must fit this sitting's selected questions and followups.")
        seen: set[tuple[str, str]] = set()
        main_states: dict[str, str] = {}
        skipped_variants: set[str] = set()
        for response_index, response in enumerate(responses):
            _object(response, RESPONSE_KEYS, "shared response")
            qid, kind, state = (
                response.get(key) for key in ("question_id", "prompt_kind", "state")
            )
            if (
                not isinstance(qid, str)
                or qid not in selected + list(admissions)
                or not isinstance(kind, str)
                or kind not in {"main", "followup"}
                or not isinstance(state, str)
                or state not in STATES
                or (qid, kind) in seen
            ):
                raise ValueError("Unknown, duplicate or unselected shared question response.")
            seen.add((qid, kind))
            if qid in admissions:
                parent = admissions[qid]["parent_topic_id"]
                if main_states.get(parent) not in ELABORATABLE or parent in skipped_variants:
                    raise ValueError(
                        "A conditional probe requires a preceding unresolved parent answer."
                    )
            if kind == "followup":
                if main_states.get(qid) not in ELABORATABLE or qid in skipped_variants:
                    raise ValueError("A followup requires a preceding unresolved answer.")
                _text(response.get("unresolved_distinction"), "Unresolved distinction", 1000)
            elif "unresolved_distinction" in response:
                raise ValueError("A main response does not carry a followup admission.")
            item = items[qid]
            exact = (
                item["question"]
                if kind == "main"
                else item.get("optional_followup", item.get("followup"))
            )
            prompt = response.get("question_text")
            if state in {"ALREADY_COVERED", "NOT_ASKED", "FUTURE_PENDING"}:
                if prompt is not None:
                    raise ValueError("Unasked/reused evidence must not claim a new elicitation.")
            elif state == "SKIPPED":
                if prompt is not None and prompt != exact:
                    raise ValueError("A shown skipped question must preserve the exact wording.")
            elif prompt != exact:
                raise ValueError("Shared question wording must match the existing bank exactly.")
            answer = response.get("answer_text")
            if state in NO_ANSWER:
                if answer is not None:
                    raise ValueError(
                        "Missing, skipped and reused states cannot invent new answers."
                    )
            else:
                _text(answer, "Answer")
            if state == "ALREADY_COVERED":
                ref, quote = response.get("source_ref"), response.get("source_quote")
                if not isinstance(ref, str) or ref not in sources:
                    raise ValueError("Covered evidence needs an actual earlier source reference.")
                _text(quote, "Exact earlier-source quote")
                if quote not in sources[ref]:
                    raise ValueError(
                        "The reuse quote must be exact contiguous earlier-source text."
                    )
            elif "source_ref" in response or "source_quote" in response:
                raise ValueError("Source reuse fields belong only to ALREADY_COVERED.")
            feedback = response.get("process_feedback", [])
            if not isinstance(feedback, list) or len(feedback) > 20:
                raise ValueError("Process feedback must be a bounded list of exact comments.")
            for comment in feedback:
                _text(comment, "Process feedback", 4000)
            if kind == "main":
                main_states[qid] = state
            if state == "SKIPPED":
                skipped_variants.add(qid)
            # Register only after this answer has passed every check. This
            # permits exact reuse across topics/sittings without forward/self
            # references, reuse chains, or process feedback becoming evidence.
            if state not in NO_ANSWER:
                ref = f"/shared/sittings/{sitting_index}/responses/{response_index}/answer_text"
                sources[ref] = answer
        for admission in admissions.values():
            if main_states.get(admission["parent_topic_id"]) not in ELABORATABLE:
                raise ValueError("Admitted probes cannot bypass a skipped or absent parent answer.")
        # Every selected topic has an explicit state; unvisited ones stay NOT_ASKED.
        if not set(selected).issubset(main_states):
            raise ValueError("Include a main state for every selected topic; unasked is NOT_ASKED.")
        prior_main.update(main_states)
    return record
