"""Local-only synthetic consumer fixture. Never imports provider credentials."""

from __future__ import annotations

from types import MethodType
from typing import Any

from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_natural_flow import TopicCompleteMove
from hdmatch.api.life_patterns_v2_owner_context import current_interview_context
from hdmatch.api.life_patterns_v2_owner_persistent import _canonical_sha
from hdmatch.api.life_patterns_v2_owner_workflow_api import create_workflow_app


class SyntheticModel:
    configured = True

    def route_participant_turn(self, **kwargs: Any) -> dict[str, Any]:
        message = kwargs["message"]
        if message == "That is not a new connection.":
            return {"kind": "repair", "evidence_quotes": [], "repair_reply": "I have withdrawn the misleading draft.",
                    "withdraw_pending_inference": True, "historical_process_turn_ids": [],
                    "repair_frontier": {"next_action": "continue_interview", "question": ""}}
        if message == "Answer with a stale routing reference.":
            return {"kind": "answer", "evidence_quotes": [message], "repair_reply": "",
                    "withdraw_pending_inference": False,
                    "historical_process_turn_ids": ["TURN-NOT-IN-THIS-SESSION"],
                    "repair_frontier": None}
        repair = message == "Please clarify your question."
        return {"kind": "repair" if repair else "answer",
                "evidence_quotes": [] if repair else [message],
                "repair_reply": "My alternatives can coexist; that contrast was not justified." if repair else "",
                "withdraw_pending_inference": False, "historical_process_turn_ids": [],
                "repair_frontier": {"next_action": "await_answer", "question": "What happened next in that same situation?"} if repair else None}

    def extract_turn(self, **kwargs: Any) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Synthetic browser fixture",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief", proposition=kwargs["message"]
                ),
            ),
            corrections=(),
        )

    def plan_turn(self, **kwargs: Any) -> Any:
        text = next(
            r["text"] for r in reversed(kwargs["recent_conversation"]) if r["role"] == "user"
        )
        if "summary second" in text and not any(p.get("origin") == "source_summary" for p in (current_interview_context() or {}).get("patterns", [])):
            return ConversationMove(reply="A connection?", move_type="surface_hypothesis",
                hypothesis_proposition="The participant walks on weekdays and cycles on weekends.",
                evidence_fact_ids=tuple(f.fact_id for f in kwargs["operative_facts"]))
        if "end this area" in text or "no useful" in text:
            return TopicCompleteMove(reply="Moving to the next useful distinction.")
        if "direct pattern" in text:
            return ConversationMove(
                reply="Saved from your words.",
                move_type="surface_hypothesis",
                hypothesis_proposition=text,
                evidence_fact_ids=(kwargs["operative_facts"][-1].fact_id,),
            )
        if "inference" in text:
            return ConversationMove(
                reply="Could context explain that difference?",
                move_type="surface_hypothesis",
                hypothesis_proposition="The difference may depend on context.",
                evidence_fact_ids=(kwargs["operative_facts"][-1].fact_id,),
            )
        return ConversationMove(
            reply="What tells you that a different response is needed?", move_type="follow_up"
        )

    def review_pattern_candidate(self, **kwargs: Any) -> dict[str, Any]:
        wording = kwargs["move"].hypothesis_proposition or ""
        return ({"decision": "inference", "inference_added": "Context may account for the difference.",
                 "inference_quote": "depend on context"} if "may depend on context" in wording
                else {"decision": "direct", "inference_added": "", "inference_quote": ""})

    def recover_repair_frontier(self, **kwargs: Any) -> dict[str, str]:
        return {"next_action": "continue_interview", "question": ""}

    def plan_refinement_turn(self, **kwargs: Any) -> ConversationMove:
        return ConversationMove(reply="Which condition is still unclear?", move_type="follow_up")

    def plan_continuation_question(self, **kwargs: Any) -> dict[str, Any]:
        stop = any("no useful" in r["text"] for r in kwargs["recent_conversation"])
        return {
            "opening": None if stop else "What tends to change when you work with somebody new?",
            "primary_domain_id": None if stop else kwargs["open_domains"][0].domain_id,
            "no_useful_question": stop,
            "question_admission": {"decision": "stop" if stop else "admit"},
        }


app = create_workflow_app(model=SyntheticModel())
runtime = app.state.recoverability_runtime
original_create = runtime.create_session


def create_ready(_self: Any) -> Any:
    session = original_create()
    session.pattern_focus_established = True
    return session


runtime.create_session = MethodType(create_ready, runtime)


@app.post("/__test/drop/{session_id}")
def drop(session_id: str) -> dict[str, bool]:
    runtime.sessions.pop(session_id, None)
    return {"dropped": True}


@app.post("/__test/legacy-repair/{session_id}")
def legacy_repair(session_id: str) -> dict[str, Any]:
    """Only synthetic loopback tests use this old-state migration fixture."""
    session = runtime.get(session_id)
    session._append_reply("The old draft has been withdrawn.", "conversation_repair")
    session.repair_pending = True
    snapshot = session.recovery_snapshot()
    snapshot["workflow"]["semantic_policy_version"] = 3
    snapshot["workflow"].pop("repair_frontier", None)
    snapshot["workflow"].pop("repair_needs_review", None)
    snapshot.pop("recovery_sha256")
    snapshot["recovery_sha256"] = _canonical_sha(snapshot)
    runtime.sessions.pop(session_id)
    return snapshot
