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

VERSION = "railway-participant-v2.2-cost-hybrid-20260928"
COLLECTION_MODES = {"railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"}
HISTORICAL_ROUTE_ALIASES = {
    "R07-retest": "R07",
    "R08-retest": "R08",
}


def _historical_route_from_record(raw: dict) -> str | None:
    source = raw.get("source")
    if not isinstance(source, dict):
        return None
    value = source.get("historical_question_id")
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    return HISTORICAL_ROUTE_ALIASES.get(value, value)


def resolved_turn_route_id(turn: dict, known_route_ids: set[str] | None = None) -> str | None:
    """Return verified route identity without rewriting historical source bytes."""

    value = turn.get("canonical_question_id")
    if isinstance(value, str) and value:
        route_id = HISTORICAL_ROUTE_ALIASES.get(value, value)
        if known_route_ids is None or route_id in known_route_ids:
            return route_id
    original = turn.get("original_record")
    if isinstance(original, dict):
        route_id = _historical_route_from_record(original)
        if route_id and (known_route_ids is None or route_id in known_route_ids):
            return route_id
    return None

def normalize_state_route_ids(state: dict, instrument: dict) -> list[str]:
    """Backfill only verified derived route metadata for old saved review states."""

    base = strict_json(instrument["interviewer-bank-v7.json"])
    known = {str(route["id"]) for route in base.get("questions", [])}
    changed: list[str] = []
    for turn in state.get("turns", []):
        resolved = resolved_turn_route_id(turn, known)
        if not resolved:
            continue
        if turn.get("canonical_question_id") == resolved:
            continue
        turn["canonical_question_id"] = resolved
        original = turn.get("original_record")
        historical = (
            original.get("source", {}).get("historical_question_id")
            if isinstance(original, dict) and isinstance(original.get("source"), dict)
            else None
        )
        if historical:
            turn["historical_question_id"] = historical
            turn["id_basis"] = "verified_historical_route"
        changed.append(str(turn.get("turn_id")))
    return changed

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
    controller = (root / "INTERVIEW-CONTROLLER-v2.md").read_bytes()
    controller_sha = hashlib.sha1(
        b"blob " + str(len(controller)).encode() + b"\0" + controller
    ).hexdigest()
    if controller_sha != "7b34c2b8711cbc5cfc1a2e7341f44366c1f0af4f":
        raise RuntimeError("Survey controller hash mismatch")
    result["controller"] = controller.decode()
    result["controller_blob_sha"] = controller_sha
    return result


def bank(instrument: dict, state: dict | None = None) -> dict:
    from .question_policy import view
    return view(strict_json(instrument["interviewer-bank-v7.json"]), state)


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
        "collection_mode": "railway_text",
        "collection_preferences": {"retrospective_questions_welcome": None},
        "evidence": [],
        "addressed_routes": {},
        "dispositions": {},
        "pending_question": None,
        "processing": None,
        "review": {"summary_shown": False, "confirmed": False, "confirmation_text": None},
        "operations": {},
        "lease": None,
        "calls": [],
        "error": None,
        "stop_reason": None,
        "final_export": None,
        "generation": 0,
        "recovery_markers": {},
        "contamination_notes": [],
        "quarantined_turns": [],
    }


def import_record(
    state: dict,
    record: dict,
    source_type: str,
    instrument: dict,
    source_mode: str = "unknown",
) -> None:
    if state["phase"] != "consent" or state["turns"] or state["source_records"]:
        raise Conflict("Import is available only before this interview begins.")
    if source_mode == "unknown" and record.get("collection_mode") in COLLECTION_MODES:
        source_mode = str(record["collection_mode"])
    if source_mode not in COLLECTION_MODES:
        raise ValueError("Unknown collection mode.")
    turns = record.get("turns")
    if not isinstance(turns, list) or len(turns) > 1000:
        raise ValueError("An import needs a turns list with at most 1000 entries.")
    # Never expose an analyst assessment, chart fields, or predicted answers to the model.
    forbidden = {
        "birth_date",
        "birth_time",
        "birthplace",
        "date_of_birth",
        "dob",
        "birth_location",
        "birth_chart",
        "human_design_type",
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
    if record.get("question_policy") is not None:
        from .question_policy import active
        state["question_policy"] = copy.deepcopy(record["question_policy"])
        active(state)  # validate identity; do not infer it from a title or participant text
    questions = bank(instrument, state)["questions"]
    known = {q["id"] for q in questions}
    exact_question_ids = {
        str(q["question"]).strip(): q["id"] for q in questions if isinstance(q.get("question"), str)
    }
    state["source_records"].append(
        {
            "source_id": "import-1",
            "source_type": source_type,
            "source_mode": source_mode,
            "received_at": utc(),
            "original_wording_verified": None,
            "historical_blinding": "unknown",
            "source_fidelity": record.get("source_fidelity"),
            "upstream_evidence_authority": record.get("evidence_authority"),
            "upstream_evidence_admitted": False,
            "historical_interview_status": record.get("historical_interview_status"),
            "unrecovered_current_test_gap_present": bool(
                isinstance(record.get("unrecovered_current_test_gap"), dict)
                and record["unrecovered_current_test_gap"].get("present") is True
            ),
            "record_as_received": copy.deepcopy(record),
        }
    )
    state["collection_mode"] = source_mode
    retrospective = record.get("retrospective_questions_welcome")
    if not isinstance(retrospective, bool) and isinstance(
        record.get("collection_preferences"), dict
    ):
        retrospective = record["collection_preferences"].get("retrospective_questions_welcome")
    if isinstance(retrospective, bool):
        state.setdefault("collection_preferences", {})["retrospective_questions_welcome"] = (
            retrospective
        )

    upstream_turn_ids: dict[str, str] = {}
    for n, raw in enumerate(turns, 1):
        if not isinstance(raw, dict):
            continue
        upstream_id = raw.get("turn_id")
        if upstream_id is None:
            continue
        key = str(upstream_id)
        if key in upstream_turn_ids:
            raise ValueError("Imported turn identifiers must be unique.")
        upstream_turn_ids[key] = f"import-{n:04d}"

    for n, raw in enumerate(turns, 1):
        if not isinstance(raw, dict):
            raise ValueError("Every turn must be an object.")
        if source_mode in {"chatgpt_voice", "chatgpt_text", "mixed"} and (
            "question_text" not in raw or "answer_text" not in raw
        ):
            raise ValueError(
                "ChatGPT collection turns must explicitly contain question_text and answer_text."
            )
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
        historical_id = _historical_route_from_record(raw)
        historical_recorded = historical_id in known if historical_id else False
        exact_id = (
            exact_question_ids.get((q or "").strip())
            if not recorded and not historical_recorded
            else None
        )
        resolved_id = (
            str(old_id)
            if recorded
            else historical_id
            if historical_recorded
            else exact_id
        )
        turn_role = raw.get("turn_role", "behavioral")
        if turn_role not in {"behavioral", "collection_metadata"}:
            turn_role = "behavioral"
        turn_id = f"import-{n:04d}"
        raw_correction_of = raw.get("correction_of")
        correction_of = None
        if raw_correction_of is not None:
            correction_of = upstream_turn_ids.get(str(raw_correction_of))
            if correction_of is None:
                raise ValueError("Imported correction references an unknown source turn.")
        mapped_antecedents = [
            upstream_turn_ids[str(value)]
            for value in raw.get("antecedent_turn_ids", [])
            if str(value) in upstream_turn_ids
        ]
        state["turns"].append(
            {
                "turn_id": turn_id,
                "sequence": n,
                "turn_source": "import-1",
                "question_text": q,
                "answer_text": a,
                "canonical_question_id": resolved_id,
                "id_basis": (
                    "recorded"
                    if recorded
                    else "verified_historical_route"
                    if historical_recorded
                    else "exact_canonical_question_text"
                    if exact_id
                    else "unknown"
                ),
                "historical_question_id": (
                    raw.get("source", {}).get("historical_question_id")
                    if isinstance(raw.get("source"), dict)
                    else None
                ),
                "turn_role": turn_role,
                "route_type": "imported_unknown_route",
                "question_wording_status": "declared_original_unverified"
                if source_type == "raw_transcript"
                else "received_edited_or_unverified",
                "antecedent_turn_ids": mapped_antecedents,
                "conditions": copy.deepcopy(raw.get("conditions", [])),
                "corrections": copy.deepcopy(raw.get("corrections", []))
                if isinstance(raw.get("corrections", []), list)
                else [],
                "process_feedback": copy.deepcopy(raw.get("process_feedback", [])),
                "answer_status": "skipped" if raw.get("answer_status") == "skipped" else "unassessed",
                "recorded_at": raw.get("recorded_at"),
                "original_record": copy.deepcopy(raw),
                "correction_of": correction_of,
            }
        )
        if raw.get("answer_status") == "skipped":
            state["dispositions"][turn_id] = {
                "turn_id": turn_id,
                "status": "skipped",
                "conditions": [],
                "process_feedback_quotes": [],
                "reason": "Explicit skip preserved from the imported source record.",
            }
        if turn_role == "collection_metadata":
            state["dispositions"][turn_id] = {
                "turn_id": turn_id,
                "status": "process_only",
                "conditions": [],
                "process_feedback_quotes": [],
                "reason": "Collection metadata is preserved but excluded from behavioral evidence.",
            }


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Quote(StrictModel):
    turn_id: str
    quote: str = Field(min_length=1)


class ControlQuote(Quote):
    source_field: Literal["answer_text", "question_text"] = "answer_text"


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


class AddressedRoute(StrictModel):
    route_id: str
    source_turn_ids: list[str] = Field(min_length=1)


class Plan(StrictModel):
    action: Literal["ask", "process", "review", "pause", "stop", "hold"]
    dispositions: list[Disposition]
    evidence: list[Evidence]
    question: Question | None
    control_quote: ControlQuote | None
    addressed_routes: list[AddressedRoute] = Field(default_factory=list)
    source_review_complete: bool = False
    reason: str


class Admission(StrictModel):
    approved: bool
    errors: list[str]
    context_supported: bool
    no_redundant_question: bool
    no_unsupported_extension: bool
    control_is_participant_request: bool
    target_information_detected: bool = False
    bulk_source_review_supported: bool = False
    addressed_routes_supported: bool = False
    approved_evidence_ids: list[str] = Field(default_factory=list)
    approved_addressed_route_ids: list[str] = Field(default_factory=list)


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
                "historical_question_id",
                "question_wording_status",
                "antecedent_turn_ids",
                "correction_of",
            )
        }
        for t in state["turns"]
        if not t.get("quarantined") and t.get("turn_role", "behavioral") == "behavioral"
    ]


def validate_plan(plan: Plan, state: dict, instrument: dict, pending: list[str]) -> None:
    turns = {t["turn_id"]: t for t in state["turns"]}
    routes = {q["id"]: q for q in bank(instrument, state)["questions"]}
    facets = {g["facet_id"] for g in guide(instrument)}
    disposition_ids = [x.turn_id for x in plan.dispositions]
    if len(disposition_ids) != len(set(disposition_ids)) or any(
        i not in pending for i in disposition_ids
    ):
        raise ValueError("Disposition identifiers must be unique pending source turns.")
    bulk_import_review = bool(pending) and all(
        str(turns[i].get("turn_source", "")).startswith("import-") for i in pending
    )
    if plan.addressed_routes:
        if not bulk_import_review:
            raise ValueError(
                "Cross-route addressed metadata is only admitted during complete import review."
            )
        seen_addressed: set[str] = set()
        for addressed in plan.addressed_routes:
            if addressed.route_id not in routes:
                raise ValueError("Unknown addressed route.")
            if addressed.route_id in seen_addressed:
                raise ValueError("Addressed route identifiers must be unique.")
            seen_addressed.add(addressed.route_id)
            if any(turn_id not in pending for turn_id in addressed.source_turn_ids):
                raise ValueError(
                    "Addressed-route support must come from pending imported source turns."
                )
            if not any(
                (turns[turn_id].get("answer_text") or "").strip()
                for turn_id in addressed.source_turn_ids
            ):
                raise ValueError("Addressed route needs at least one answered source turn.")

    if plan.source_review_complete:
        if not bulk_import_review:
            raise ValueError(
                "Bulk source-review completion is only valid for imported source turns."
            )
    elif sorted(disposition_ids) != sorted(pending):
        raise ValueError("Each pending non-bulk source turn needs exactly one disposition.")
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
    process_ids.update(
        turn_id for turn_id, disposition in state.get("dispositions", {}).items()
        if disposition.get("status") in {"process_only", "skipped"}
    )
    if any(q.turn_id in process_ids for e in plan.evidence for q in e.source_quotes):
        raise ValueError("Process-only feedback and skipped answers are not personality evidence.")
    if plan.action in {"pause", "stop", "hold"}:
        q = plan.control_quote
        if (
            q is None
            or q.turn_id not in pending
            or q.quote
            not in (turns[q.turn_id].get(getattr(q, "source_field", "answer_text")) or "")
            or (
                plan.action != "hold" and getattr(q, "source_field", "answer_text") != "answer_text"
            )
        ):
            raise ValueError(
                "A control action needs an exact current source quote in its permitted field."
            )
    if plan.action in {"pause", "stop"} and "gpt_review_answers_processed" in state:
        source = turns[plan.control_quote.turn_id]
        if source.get("turn_source") == "import-1":
            raise ValueError(
                "Historical imported text cannot pause or stop the current queued review."
            )
        if source.get("answer_status") == "skipped":
            raise ValueError("An item skip cannot pause or stop the entire review.")
    if plan.action == "hold" and plan.evidence:
        raise ValueError("A target-information hold must not emit behavioral evidence.")
    if any(turns[q.turn_id].get("quarantined") for e in plan.evidence for q in e.source_quotes):
        raise ValueError("Quarantined sources cannot support evidence.")
    if plan.action == "ask":
        q = plan.question
        if q is None or q.route_id not in routes:
            raise ValueError("A question must belong to the full canonical bank.")
        route = routes[q.route_id]
        from .question_policy import selectable
        if not selectable(route, state):
            raise ValueError("This retired or skipped route is not available for new elicitation.")
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
    routes = bank(instrument, state)["questions"]
    answered = {
        t.get("canonical_question_id")
        for t in state["turns"]
        if t.get("canonical_question_id")
        and t.get("answer_text") is not None
        and not t.get("quarantined")
        and t.get("turn_role", "behavioral") == "behavioral"
    }
    reviewed = bool(state["review"].get("confirmed"))
    return {
        "schema": "life-patterns-full-survey-participant-export-v2",
        **({"question_policy": copy.deepcopy(state["question_policy"])}
           if state.get("question_policy") else {}),
        "session_id": state["session_id"],
        "survey_authority": {
            "engine_version": VERSION,
            "instrument_version": state["instrument_version"],
            "controller_blob_sha": instrument.get("controller_blob_sha"),
            "protocol_blob_sha": SOURCES["INTERVIEW-PROTOCOL-v6.md"],
            "bank_blob_sha": SOURCES["interviewer-bank-v7.json"],
            "evidence_guide_blob_sha": SOURCES["EVIDENCE-GUIDE-v7.json"],
        },
        "source_records": copy.deepcopy(state["source_records"]),
        "collection_mode": state.get("collection_mode", "unknown"),
        "collection_preferences": copy.deepcopy(state.get("collection_preferences", {})),
        "consent": {
            "research_use_consented": state["consent"] is True,
            "recorded_at": state.get("consented_at"),
        },
        "blinding": {
            "birth_or_chart_data_requested_by_interviewer": False,
            "birth_or_chart_data_used_by_interviewer": None,
            "target_predictions_used": False,
            "contamination_notes": copy.deepcopy(state["contamination_notes"]),
            "target_check_result": "exposure_detected"
            if state["contamination_notes"]
            else "not_detected_by_conservative_check",
            "target_use_policy": "prohibited; absence and non-use are not independently certified",
        },
        "interview_status": "complete"
        if state["phase"] == "complete"
        else "stopped_by_participant"
        if state["phase"] == "stopped"
        else "partial",
        "stop_reason": state["stop_reason"],
        "turns": copy.deepcopy(state["turns"]),
        "neutral_evidence": copy.deepcopy(state["evidence"]),
        "evidence_authority": "railway_independent_semantic_admission",
        "addressed_routes": copy.deepcopy(state.get("addressed_routes", {})),
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
            "frozen_before_birth_or_chart_reveal": None,
            "birth_or_chart_data_in_this_export": None,
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
        "model_call_telemetry_scope": "Recorded completions/attempts at export time; an in-flight call may finish after a stopped record was frozen.",
        "turn_dispositions": copy.deepcopy(state["dispositions"]),
        "scientifically_validated": False,
        "review_status": "reviewed_for_development_fitting"
        if reviewed
        else "not_participant_reviewed",
    }


def freeze(state: dict, instrument: dict) -> None:
    state["final_export"] = canonical(export_record(state, instrument, final=True))
