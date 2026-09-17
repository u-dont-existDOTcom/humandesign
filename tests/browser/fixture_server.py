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
from hdmatch.api.life_patterns_v2_owner_workflow_api import create_workflow_app


class SyntheticModel:
    configured = True

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
