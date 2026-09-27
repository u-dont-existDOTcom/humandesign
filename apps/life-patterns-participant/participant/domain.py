"""Source-bound survey records. No birth/chart/scoring code is imported here."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .store import Conflict, canonical

VERSION = "railway-participant-v2.1-20260927"
SOURCES = {
    "INTERVIEW-PROTOCOL-v6.md": "5dc95763f65441d67c87b21116e00d7f2df04223",
    "interviewer-bank-v7.json": "cf6c60ec7206e07ee62b6148549e6d755bef8ac1",
    "EVIDENCE-GUIDE-v7.json": "29309f2341e2a8c91e578b683058e360ded8e420",
}


def utc() -> str:
    return datetime.now(UTC).isoformat()


def strict_json(raw: str) -> dict:
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError("Duplicate JSON key")
            out[k] = v
        return out

    def invalid(value):
        raise ValueError("Non-finite JSON number")

    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    if not isinstance(value, dict):
        raise ValueError("JSON must contain one object")
    return value


def load_instrument(root: Path) -> dict:
    result = {"version": VERSION}
    for name, expected in SOURCES.items():
        raw = (root / name).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if actual != expected:
            raise RuntimeError("Survey source hash mismatch: " + name)
        result[name] = raw.decode()
    result["controller"] = (root / "INTERVIEW-CONTROLLER-v2.md").read_text()
    return result


def bank(instrument: dict) -> dict:
    return strict_json(instrument["interviewer-bank-v7.json"])


def guide(instrument: dict) -> list[dict]:
    return json.loads(instrument["EVIDENCE-GUIDE-v7.json"])


def target_exposure(text: str) -> bool:
    # A conservative ingestion guard, not a claim of perfect semantic detection.
    return bool(
        re.search(
            r"\b(?:I was born|my (?:birth date|date of birth|birth time|birthplace|natal chart))\b",
            text,
            re.I,
        )
        or (
            re.search(r"\b\d{1,4}[-/]\d{1,2}[-/]\d{1,4}\b", text)
            and re.search(r"\b\d{1,2}:\d{2}\b", text)
        )
    )


def new_state(instrument_version: str, model: str, effort: str) -> dict:
    return {
        "created_at": utc(),
        "instrument_version": instrument_version,
        "model": model,
        "effort": effort,
        "phase": "consent",
        "consent": None,
        "turns": [],
        "source_records": [],
        "evidence": [],
        "dispositions": {},
        "pending_question": None,
        "review": {"summary_shown": False, "confirmed": False, "confirmation_text": None},
        "operations": {},
        "lease": None,
        "calls": [],
        "error": None,
        "stop_reason": None,
        "final_export": None,
        "generation": 0,
        "contamination_notes": [],
        "quarantined_turns": [],
    }


def import_record(state: dict, record: dict, source_type: str, instrument: dict) -> None:
    if state["phase"] != "consent" or state["turns"]:
        raise Conflict("Import is available only before this interview begins.")
    turns = record.get("turns")
    if not isinstance(turns, list) or len(turns) > 1000:
        raise ValueError("An import needs a turns list with at most 1000 entries.")
    # Never expose an analyst assessment, chart fields, or predicted answers to the model.
    forbidden = {
        "birth_date",
        "birth_time",
        "birthplace",
        "date_of_birth",
        "natal_chart",
        "chart",
        "rankings",
        "target_predictions",
    }

    def walk(obj):
        if isinstance(obj, dict):
            if forbidden.intersection(k.lower() for k in obj):
                raise ValueError("Remove birth/chart/ranking fields from the interview input.")
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    walk(record)
    known = {q["id"] for q in bank(instrument)["questions"]}
    state["source_records"].append(
        {
            "source_id": "import-1",
            "source_type": source_type,
            "received_at": utc(),
            "original_wording_verified": source_type == "raw_transcript",
            "historical_blinding": "unknown",
            "record_as_received": copy.deepcopy(record),
        }
    )
    for n, raw in enumerate(turns, 1):
        if not isinstance(raw, dict):
            raise ValueError("Every turn must be an object.")
        q = raw.get("question_text")
        a = raw.get("answer_text")
        if q is not None and not isinstance(q, str):
            raise ValueError("Question text must be text or null.")
        if a is not None and not isinstance(a, str):
            raise ValueError("Answer text must be text or null.")
        if target_exposure((q or "") + "\n" + (a or "")):
            raise ValueError(
                "A prior turn appears to contain birth information. Keep it out of the interview import."
            )
        old_id = raw.get("canonical_question_id", raw.get("question_id"))
        recorded = old_id in known
        state["turns"].append(
            {
                "turn_id": f"import-{n:04d}",
                "sequence": n,
                "turn_source": "import-1",
                "question_text": q,
                "answer_text": a,
                "canonical_question_id": old_id if recorded else None,
                "id_basis": "recorded" if recorded else "unknown",
                "route_type": "imported_unknown_route",
                "question_wording_status": "verified_original"
                if source_type == "raw_transcript"
                else "received_edited_or_unverified",
                "antecedent_turn_ids": [],
                "conditions": copy.deepcopy(raw.get("conditions", [])),
                "corrections": copy.deepcopy(raw.get("corrections", []))
                if isinstance(raw.get("corrections", []), list)
                else [],
                "process_feedback": copy.deepcopy(raw.get("process_feedback", [])),
                "answer_status": "unassessed",
                "recorded_at": raw.get("recorded_at"),
                "original_record": copy.deepcopy(raw),
                "correction_of": None,
            }
        )


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Quote(StrictModel):
    turn_id: str
    quote: str = Field(min_length=1)


class Evidence(StrictModel):
    evidence_id: str
    source_quotes: list[Quote] = Field(min_length=1)
    observation: str = Field(min_length=1, max_length=1500)
    evidence_type: Literal[
        "usual_response_self_report",
        "retrospective_recollection",
        "normative_view",
        "supplementary_self_report",
    ]
    conditions: list[str]
    time_frame: str
    relationship_context: str
    candidate_facet_ids: list[str]
    supported_scope: str
    unsupported_extensions: list[str]
    amends_evidence_ids: list[str] = Field(default_factory=list)


class Disposition(StrictModel):
    turn_id: str
    status: Literal["answered", "conditional", "unclear", "process_only", "skipped", "unassessed"]
    conditions: list[str]
    process_feedback_quotes: list[str]
    reason: str


class Question(StrictModel):
    route_id: str
    route_type: Literal["canonical", "context_repair", "missing_piece_followup"]
    text: str = Field(min_length=1, max_length=3000)
    antecedent_turn_ids: list[str]
    equivalent_context: bool
    missing_distinction: str
    why_useful: str


class Plan(StrictModel):
    action: Literal["ask", "process", "review", "pause", "stop", "hold"]
    dispositions: list[Disposition]
    evidence: list[Evidence]
    question: Question | None
    control_quote: Quote | None
    reason: str


class Admission(StrictModel):
    approved: bool
    errors: list[str]
    context_supported: bool
    no_redundant_question: bool
    no_unsupported_extension: bool
    control_is_participant_request: bool


def semantic_turns(state: dict) -> list[dict]:
    # Exact respondent words and visible questions only; no imported analyst assessment.
    return [
        {
            k: t.get(k)
            for k in (
                "turn_id",
                "question_text",
                "answer_text",
                "canonical_question_id",
                "question_wording_status",
                "antecedent_turn_ids",
                "correction_of",
            )
        }
        for t in state["turns"]
    ]


def validate_plan(plan: Plan, state: dict, instrument: dict, pending: list[str]) -> None:
    turns = {t["turn_id"]: t for t in state["turns"]}
    routes = {q["id"]: q for q in bank(instrument)["questions"]}
    facets = {g["facet_id"] for g in guide(instrument)}
    if sorted(x.turn_id for x in plan.dispositions) != sorted(pending):
        raise ValueError("Each pending source turn needs exactly one disposition.")
    for d in plan.dispositions:
        for quote in d.process_feedback_quotes:
            if not quote or quote not in (turns[d.turn_id].get("answer_text") or ""):
                raise ValueError("Process feedback must quote the respondent exactly.")
    seen = {e["evidence_id"] for e in state["evidence"]}
    for e in plan.evidence:
        if e.evidence_id in seen:
            raise ValueError("Evidence identifiers must be unique.")
        if any(
            i not in {old["evidence_id"] for old in state["evidence"]}
            for i in e.amends_evidence_ids
        ):
            raise ValueError("An amendment must name existing evidence.")
        if e.amends_evidence_ids and not any(
            turns[i].get("correction_of") or turns[i].get("is_review_correction") for i in pending
        ):
            raise ValueError("Amendment requires a pending participant correction.")
        seen.add(e.evidence_id)
        if any(f not in facets for f in e.candidate_facet_ids):
            raise ValueError("Unknown neutral facet.")
        if not any(q.turn_id in pending for q in e.source_quotes):
            raise ValueError("New evidence must involve a pending source, not duplicate old votes.")
        for q in e.source_quotes:
            if q.turn_id not in turns or q.quote not in (turns[q.turn_id].get("answer_text") or ""):
                raise ValueError("Evidence quote not found in exact respondent answer.")
    if plan.action == "process" and not pending:
        raise ValueError("No pending import batch remains to process.")
    if plan.action == "review" and not state["turns"]:
        raise ValueError("A new interview needs an admissible first question.")
    process_ids = {d.turn_id for d in plan.dispositions if d.status in {"process_only", "skipped"}}
    if any(q.turn_id in process_ids for e in plan.evidence for q in e.source_quotes):
        raise ValueError("Process-only feedback and skipped answers are not personality evidence.")
    if plan.action in {"pause", "stop", "hold"}:
        q = plan.control_quote
        if (
            q is None
            or q.turn_id not in pending
            or q.quote not in (turns[q.turn_id].get("answer_text") or "")
        ):
            raise ValueError("A control action needs an exact current participant-request quote.")
    if plan.action == "ask":
        q = plan.question
        if q is None or q.route_id not in routes:
            raise ValueError("A question must belong to the full canonical bank.")
        route = routes[q.route_id]
        if q.route_type == "canonical" and q.text != route["question"]:
            raise ValueError("Canonical wording must match the bank exactly.")
        if target_exposure(q.text):
            raise ValueError("Birth-related questions are excluded.")
        if any(i not in turns for i in q.antecedent_turn_ids):
            raise ValueError("Invented antecedent identifier.")
        if not route["context_requirement"].startswith("Self-contained"):
            usable = [turns[i] for i in q.antecedent_turn_ids if turns[i].get("answer_text")]
            if not usable:
                raise ValueError("A dependent route needs an actual answered antecedent.")
            if not q.equivalent_context and not any(
                t.get("canonical_question_id") in route.get("context_sources", []) for t in usable
            ):
                raise ValueError(
                    "The antecedent must match the route or require explicit contextual-equivalence review."
                )
        for t in state["turns"]:
            if t.get("canonical_question_id") == q.route_id and q.route_type == "canonical":
                raise ValueError("Do not repeat an already presented canonical question.")
    elif plan.question is not None:
        raise ValueError("Non-question actions must not carry a question.")


def export_record(state: dict, instrument: dict, final: bool = False) -> dict:
    routes = bank(instrument)["questions"]
    answered = {
        t.get("canonical_question_id") for t in state["turns"] if t.get("answer_text") is not None
    }
    reviewed = bool(state["review"].get("confirmed"))
    return {
        "schema": "life-patterns-full-survey-participant-export-v2",
        "session_id": state["session_id"],
        "survey_authority": {
            "engine_version": VERSION,
            "instrument_version": state["instrument_version"],
            "protocol_blob_sha": SOURCES["INTERVIEW-PROTOCOL-v6.md"],
            "bank_blob_sha": SOURCES["interviewer-bank-v7.json"],
            "evidence_guide_blob_sha": SOURCES["EVIDENCE-GUIDE-v7.json"],
        },
        "source_records": copy.deepcopy(state["source_records"]),
        "consent": {
            "research_use_consented": state["consent"] is True,
            "recorded_at": state.get("consented_at"),
        },
        "blinding": {
            "birth_or_chart_data_requested_by_interviewer": False,
            "birth_or_chart_data_used_by_interviewer": False,
            "target_predictions_used": False,
            "contamination_notes": copy.deepcopy(state["contamination_notes"]),
        },
        "interview_status": "complete"
        if state["phase"] == "complete"
        else "stopped_by_participant"
        if state["phase"] == "stopped"
        else "partial",
        "stop_reason": state["stop_reason"],
        "turns": copy.deepcopy(state["turns"]),
        "neutral_evidence": copy.deepcopy(state["evidence"]),
        "coverage": [
            {
                "question_id": q["id"],
                "status": "partial" if q["id"] in answered else "unassessed",
                "reason": "An answer is present; credit remains source- and context-specific."
                if q["id"] in answered
                else "No canonical route answer established; not a negative trait.",
            }
            for q in routes
        ],
        "participant_review": copy.deepcopy(state["review"]),
        "freeze": {
            "record_state": "final" if final else "checkpoint",
            "versioned_at": utc(),
            "frozen_before_birth_or_chart_reveal": None
            if state["source_records"] or state["contamination_notes"]
            else True,
            "birth_or_chart_data_in_this_export": False,
            "do_not_recode_after_target_reveal_without_versioning": True,
        },
        "handoff_method": "json_file",
        "model_profile": {
            "provider": "venice",
            "model": state["model"],
            "reasoning_effort": state["effort"],
            "automatic_fallback": False,
        },
        "model_call_telemetry": copy.deepcopy(state["calls"]),
        "scientifically_validated": False,
        "review_status": "reviewed_for_development_fitting"
        if reviewed
        else "not_participant_reviewed",
    }


def freeze(state: dict, instrument: dict) -> None:
    state["final_export"] = canonical(export_record(state, instrument, final=True))
