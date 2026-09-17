"""Continuous natural-flow owner interview with a pre-send question-admission gate.

The fixed recoverability surface remains target-theory-blind and standardized, but the
participant should experience one continuous interview rather than a sequence of category
checkpoints. This layer keeps the current server session alive across measurement areas,
feeds prior participant answers into continuation planning, and runs a separate low-cost
admission pass before any model-generated question is shown.
"""

from __future__ import annotations

import uuid
from typing import Any, cast

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .life_patterns_v2_owner_conversation import ConversationMove, ConversationTurnRequest
from .life_patterns_v2_owner_continuous_flow_ui import CONTINUOUS_FLOW_RECOVERABILITY_HTML
from .life_patterns_v2_owner_natural_flow import (
    NaturalFlowRecoverabilityOpenAIModel,
    NaturalFlowRecoverabilitySession,
    TopicCompleteMove,
    create_life_patterns_v2_owner_natural_flow_app,
)
from .life_patterns_v2_owner_pattern_first import TemporaryModelProviderError
from .life_patterns_v2_owner_recoverability import _open_domains

_QUESTION_MOVES = frozenset({"follow_up", "request_contrast", "boundary_question"})


class ContinuousAdvanceRequest(BaseModel):
    aggregate_coverage: list[dict[str, Any]] = Field(default_factory=list, max_length=64)
    completed_results: list[dict[str, Any]] = Field(default_factory=list, max_length=64)
    answer_memory: list[str] = Field(default_factory=list, max_length=400)


class ContinuousFlowRecoverabilityOpenAIModel(NaturalFlowRecoverabilityOpenAIModel):
    """Natural-flow planner with an explicit pre-send usefulness/redundancy check."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._question_admission_by_reply: dict[str, list[dict[str, Any]]] = {}

    def _remember_question_admission(self, reply: str, evidence: dict[str, Any]) -> None:
        self._question_admission_by_reply.setdefault(reply, []).append(evidence)

    def pop_question_admission(self, reply: str) -> dict[str, Any] | None:
        rows = self._question_admission_by_reply.get(reply)
        if not rows:
            return None
        evidence = rows.pop(0)
        if not rows:
            self._question_admission_by_reply.pop(reply, None)
        return evidence

    def _admit_in_thread_question(
        self,
        *,
        candidate: ConversationMove,
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> ConversationMove | TopicCompleteMove:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "decision",
                "reply",
                "move_type",
                "missing_discriminator",
                "decision_impact",
                "redundancy_check",
            ],
            "properties": {
                "decision": {"type": "string", "enum": ["admit", "replace", "stop"]},
                "reply": {
                    "anyOf": [
                        {"type": "string", "minLength": 1, "maxLength": 1800},
                        {"type": "null"},
                    ]
                },
                "move_type": {
                    "anyOf": [
                        {
                            "type": "string",
                            "enum": ["follow_up", "request_contrast", "boundary_question"],
                        },
                        {"type": "null"},
                    ]
                },
                "missing_discriminator": {"type": "string", "minLength": 1, "maxLength": 600},
                "decision_impact": {"type": "string", "minLength": 1, "maxLength": 700},
                "redundancy_check": {"type": "string", "minLength": 1, "maxLength": 700},
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "You are the PRE-SEND QUESTION ADMISSION GATE for a target-theory-blind Life Patterns interview. "
                "The candidate question has NOT been shown to the participant yet. Do not rubber-stamp it. ADMIT only "
                "when all of these are true: (1) the participant has not already answered the same substantive question, "
                "including under different wording; (2) at least two plausible answers would materially change the "
                "person-specific characterization, scope, boundary, timing, mechanism, or a still-open measurement "
                "distinction; (3) the question is answerable from ordinary lived experience; and (4) the expected "
                "information gain is worth another participant turn. REPLACE when the candidate fails but one clearly "
                "better question remains in the current thread. STOP when no genuinely useful question remains in this "
                "thread. Reject semantic restatements, questionnaire-for-its-own-sake prompts, generic questions whose "
                "likely answers are ordinary human defaults, and questions whose answer is already present in the "
                "conversation. Process feedback about the interview is not personality evidence. For admit, return the "
                "candidate unchanged. For replace, return exactly one concise replacement question and its move type. "
                "For stop, return reply=null and move_type=null. The three explanation fields are internal admission "
                "evidence and must name the exact missing distinction, how different answers matter, and why this is not "
                "already answered."
            ),
            payload={
                "candidate": {
                    "reply": candidate.reply,
                    "move_type": candidate.move_type,
                },
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-120:]),
            },
            schema=schema,
            effort="low",
            max_output_tokens=950,
            schema_name="life_patterns_question_admission_v1",
        )
        decision = str(result.get("decision", "stop"))
        evidence = {
            "stage": "in_thread_pre_send",
            "decision": decision,
            "candidate_question": candidate.reply,
            "missing_discriminator": str(result.get("missing_discriminator", "")),
            "decision_impact": str(result.get("decision_impact", "")),
            "redundancy_check": str(result.get("redundancy_check", "")),
        }
        if decision == "admit":
            evidence["final_question"] = candidate.reply
            self._remember_question_admission(candidate.reply, evidence)
            return candidate
        if decision == "replace":
            reply = str(result.get("reply") or "").strip()
            move_type = str(result.get("move_type") or "")
            if reply and move_type in _QUESTION_MOVES:
                evidence["final_question"] = reply
                self._remember_question_admission(reply, evidence)
                return ConversationMove(reply=reply, move_type=move_type)  # type: ignore[arg-type]
        return TopicCompleteMove(
            reply="That gives me enough useful information for this area; I’ll move on."
        )

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> Any:
        move = super().plan_turn(
            current_episode_id=current_episode_id,
            episodes=episodes,
            operative_facts=operative_facts,
            recent_conversation=recent_conversation,
            boundary_answered=boundary_answered,
        )
        if getattr(move, "move_type", None) not in _QUESTION_MOVES:
            return move
        return self._admit_in_thread_question(
            candidate=move,
            operative_facts=operative_facts,
            recent_conversation=recent_conversation,
        )

    def plan_continuation_question(
        self,
        *,
        open_domains: tuple[Any, ...],
        aggregate_coverage: list[dict[str, Any]],
        completed_results: list[dict[str, Any]],
        answer_memory: list[str],
        recent_conversation: tuple[dict[str, str], ...],
        operative_facts: tuple[Any, ...],
    ) -> dict[str, Any]:
        """Generate, then independently admit/replace, the next cross-area question."""

        candidate = super().plan_next_coverage_question(
            open_domains=open_domains,
            aggregate_coverage=aggregate_coverage,
            completed_results=completed_results,
        )
        open_ids = [domain.domain_id for domain in open_domains]
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "primary_domain_id",
                "opening",
                "missing_discriminator",
                "decision_impact",
                "redundancy_check",
                "changed_candidate",
            ],
            "properties": {
                "primary_domain_id": {"type": "string", "enum": open_ids},
                "opening": {"type": "string", "minLength": 1, "maxLength": 1800},
                "missing_discriminator": {"type": "string", "minLength": 1, "maxLength": 600},
                "decision_impact": {"type": "string", "minLength": 1, "maxLength": 700},
                "redundancy_check": {"type": "string", "minLength": 1, "maxLength": 700},
                "changed_candidate": {"type": "boolean"},
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "You are the FINAL PRE-SEND ADMISSION GATE for the next question in a continuous, target-theory-blind "
                "Life Patterns interview. The first-pass candidate is only a draft. Inspect the participant's prior "
                "answer memory, the current continuous conversation, accepted pattern wording, and coverage metadata. "
                "Return the candidate only if it targets a genuinely missing discriminator and different plausible "
                "answers would materially change a person-specific characterization or close/advance a still-open "
                "measurement area. If the participant has already answered the substantive question—even with different "
                "wording—replace it. If the candidate is vague, generic, normative, or likely to elicit an ordinary "
                "human default rather than discriminating information, replace it with a more concrete behavioral "
                "contrast from another open dimension. For PARTIAL dimensions ask only the missing distinction, never "
                "restart the topic. For UNASSESSED dimensions prefer high expected information gain and a natural bridge "
                "from what is already known. Do not ask a question merely because a category remains open. Output exactly "
                "one admitted question. The internal fields must state the missing discriminator, how materially different "
                "answers would change interpretation, and why the question is not already answered."
            ),
            payload={
                "first_pass_candidate": candidate,
                "open_dimensions": [
                    {
                        "domain_id": domain.domain_id,
                        "title": domain.title,
                        "definition": domain.definition,
                    }
                    for domain in open_domains
                ],
                "aggregate_coverage": aggregate_coverage[-64:],
                "completed_results": [
                    {
                        "status": str(row.get("status", "")),
                        "wording": str(row.get("wording", ""))[:1400],
                    }
                    for row in completed_results[-64:]
                    if isinstance(row, dict)
                ],
                "participant_answer_memory": answer_memory[-300:],
                "recent_conversation": list(recent_conversation[-120:]),
                "operative_facts": [
                    {
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts[-160:]
                ],
            },
            schema=schema,
            effort="low",
            max_output_tokens=1100,
            schema_name="life_patterns_continuation_question_admission_v1",
        )
        opening = str(result["opening"]).strip()
        admission = {
            "stage": "cross_area_pre_send",
            "decision": "replace" if bool(result["changed_candidate"]) else "admit",
            "candidate_question": str(candidate.get("opening", "")),
            "final_question": opening,
            "missing_discriminator": str(result["missing_discriminator"]),
            "decision_impact": str(result["decision_impact"]),
            "redundancy_check": str(result["redundancy_check"]),
        }
        return {
            "primary_domain_id": str(result["primary_domain_id"]),
            "opening": opening,
            "question_admission": admission,
        }


def _advance_existing_session(
    *,
    session: NaturalFlowRecoverabilitySession,
    model: ContinuousFlowRecoverabilityOpenAIModel,
    request: ContinuousAdvanceRequest,
) -> dict[str, Any]:
    if getattr(session, "_draft_move", None) is not None or session.core.active_proposal_id is not None:
        raise ValueError("judge the current inferred synthesis before advancing")

    open_domains = _open_domains(request.aggregate_coverage)
    if not open_domains:
        return {
            "session_id": session.session_id,
            "complete": True,
            "opening": None,
            "primary_domain_id": None,
        }

    plan = model.plan_continuation_question(
        open_domains=open_domains,
        aggregate_coverage=request.aggregate_coverage,
        completed_results=request.completed_results,
        answer_memory=request.answer_memory,
        recent_conversation=tuple(session.conversation),
        operative_facts=session.core.operative_facts(),
    )
    opening = str(plan["opening"]).strip()
    if not opening:
        raise ValueError("next-question admission returned no question")

    session.current_episode_id = None
    session.awaiting_new_episode = True
    session.pending_boundary_question = False
    session.boundary_answered = False
    session.pattern_focus_established = True
    if hasattr(session, "_topic_complete_ready"):
        session._topic_complete_ready = False
    session.conversation.append(
        {
            "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
            "role": "assistant",
            "text": opening,
        }
    )
    return {
        "session_id": session.session_id,
        "complete": False,
        "opening": opening,
        "primary_domain_id": str(plan["primary_domain_id"]),
        "question_admission": plan["question_admission"],
    }


def create_life_patterns_v2_owner_continuous_flow_app() -> FastAPI:
    """Serve automatic continuation on one recoverable session with admitted questions only."""

    app = create_life_patterns_v2_owner_natural_flow_app()
    runtime = app.state.recoverability_runtime
    runtime.model = ContinuousFlowRecoverabilityOpenAIModel.from_env()

    app.router.routes[:] = [
        route
        for route in app.router.routes
        if getattr(route, "path", None)
        not in {"/", "/api/owner-v2/conversation/sessions/{session_id}/turns"}
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return CONTINUOUS_FLOW_RECOVERABILITY_HTML

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            result = cast(dict[str, Any], runtime.get(session_id).turn(request.message))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        reply = str(result.get("reply", ""))
        admission = runtime.model.pop_question_admission(reply)
        if admission is not None:
            result["question_admission"] = admission
        return result

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/advance")
    def advance_interview(session_id: str, request: ContinuousAdvanceRequest) -> dict[str, Any]:
        try:
            session = runtime.get(session_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        if not isinstance(session, NaturalFlowRecoverabilitySession):
            raise HTTPException(status_code=409, detail="session does not support continuous interview flow")
        try:
            return _advance_existing_session(session=session, model=runtime.model, request=request)
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    app.state.continuous_interview_flow = True
    app.state.auto_continue_between_measurement_areas = True
    app.state.finish_for_now_always_visible = True
    app.state.pre_send_question_admission = True
    app.state.same_session_cross_area_memory = True
    app.state.question_admission_audit_in_recovery = True
    return app


app = create_life_patterns_v2_owner_continuous_flow_app()
