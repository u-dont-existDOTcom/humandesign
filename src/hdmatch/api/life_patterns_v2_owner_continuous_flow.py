"""Continuous natural-flow owner interview with a pre-send question-admission gate.

The fixed recoverability surface remains target-theory-blind and standardized, but the
participant should experience one continuous interview rather than a sequence of category
checkpoints. This layer keeps the current server session alive across measurement areas,
feeds prior participant answers into continuation planning, and runs a separate low-cost
admission pass before any model-generated question is shown.
"""

from __future__ import annotations

import uuid
from typing import Any, Literal, cast

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .life_patterns_v2_owner_context import current_interview_context
from .life_patterns_v2_owner_conversation import ConversationMove
from .life_patterns_v2_owner_natural_flow import (
    NaturalFlowRecoverabilityOpenAIModel,
    NaturalFlowRecoverabilitySession,
    TopicCompleteMove,
)
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

    def _conversation_call_json(
        self,
        *,
        instructions: str,
        payload: dict[str, Any],
        schema: dict[str, Any],
        effort: Literal["low", "medium"],
        max_output_tokens: int,
        schema_name: str,
    ) -> dict[str, Any]:
        context = current_interview_context()
        if context is not None:
            source_context = {
                key: value for key, value in context.items() if key != "admission_sink"
            }
            payload = {
                **payload,
                "recent_conversation": context["conversation"],
                "shared_evidence_context": source_context,
            }
        instructions += (
            "\n\nSOURCE FIDELITY: Consult the shared source-bound interview context before asking or "
            "formulating anything. Older relevant answers and later corrections matter, not just recent turns. "
            "Do not convert needed duration/amount into benefit, correlation into cause, an example into a "
            "universal claim, a quoted belief into endorsement, or a past/negated/qualified statement into a "
            "present unqualified assertion. A familiar direct self-report can be useful without being surprising "
            "or rare. Never assert population rarity without evidence. 'It depends' can identify the meaningful "
            "condition; ask only for a condition or distinction not already known. Preserve broad intended scope. "
            "Participant correction annotations dispute the linked historical pattern; do not present that "
            "pattern as settled or silently erase the correction. Process feedback is not personality evidence. "
            "A new inference must state the actual added relationship tentatively, not hide it in a recap. "
            "When reviewing an existing inference, no worthwhile further question is a legitimate outcome; "
            "do not invent a new synthesis merely to fill a section boundary."
        )
        return super()._conversation_call_json(
            instructions=instructions,
            payload=payload,
            schema=schema,
            effort=effort,
            max_output_tokens=max_output_tokens,
            schema_name=schema_name,
        )

    def review_pattern_candidate(
        self, *, move: ConversationMove, evidence_context: dict[str, Any]
    ) -> dict[str, Any]:
        return self._conversation_call_json(
            instructions=(
                "Check the proposed person-level formulation against the EXACT participant sources and "
                "operative evidence before recording or showing it. This is a fallible product-quality "
                "review, not scientific validation. Return direct only for an endorsed, person-specific "
                "self-report already explicitly stated, with its original scope, polarity, speaker, time, "
                "uncertainty and conditions intact. A verbatim substring is NOT sufficient if its surrounding "
                "text negates it, attributes it to somebody else, limits it or says it no longer applies. "
                "Direct statements need not be surprising, rare, sophisticated, or discoveries. Return "
                "inference only for a genuinely added, plausibly supported relationship that should be "
                "judged by the participant; identify precisely what is added. Do not confuse the amount "
                "of something needed with how beneficial it is. Return context_only for generic filler, "
                "misquoted context, unsupported causal/directional/scope additions, or no person-level "
                "claim. Context-only material can remain episode or measurement evidence. Do not demand "
                "a quota of examples or invalidate useful conditional answers."
            ),
            payload={
                "candidate": move.model_dump(mode="json"),
                "source_context": {
                    k: v for k, v in evidence_context.items() if k != "admission_sink"
                },
            },
            schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["decision", "inference_added", "source_reason"],
                "properties": {
                    "decision": {"type": "string", "enum": ["direct", "inference", "context_only"]},
                    "inference_added": {"type": "string", "maxLength": 800},
                    "source_reason": {"type": "string", "minLength": 1, "maxLength": 1000},
                },
            },
            effort="low",
            max_output_tokens=900,
            schema_name="life_patterns_formulation_fidelity_v1",
        )

    def _remember_question_admission(self, reply: str, evidence: dict[str, Any]) -> None:
        context = current_interview_context()
        if context is not None:
            # The evidence provider exposes an operation-local audit sink.
            sink = context.get("admission_sink")
            if isinstance(sink, list):
                sink.append({"reply": reply, "evidence": evidence})
                return
        self._question_admission_by_reply.setdefault(reply, []).append(evidence)

    def pop_question_admission(self, reply: str) -> dict[str, Any] | None:
        context = current_interview_context()
        if context is not None:
            sink = context.get("admission_sink")
            if isinstance(sink, list):
                for index, item in enumerate(sink):
                    if item["reply"] == reply:
                        return cast(dict[str, Any], sink.pop(index)["evidence"])
                return None
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
        evidence: dict[str, Any] = {
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
        reply = "I do not see another useful question for this point right now."
        evidence["final_question"] = None
        self._remember_question_admission(reply, evidence)
        return TopicCompleteMove(reply=reply)

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
        # WorkflowSession admits the final emitted question, after refinement and
        # runtime fallback transformations. Do not gate a draft twice here.
        return move

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
                "no_useful_question",
            ],
            "properties": {
                "primary_domain_id": {
                    "anyOf": [{"type": "string", "enum": open_ids}, {"type": "null"}]
                },
                "opening": {
                    "anyOf": [
                        {"type": "string", "minLength": 1, "maxLength": 1800},
                        {"type": "null"},
                    ]
                },
                "no_useful_question": {"type": "boolean"},
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
                "one admitted question, OR return no_useful_question=true and opening/primary_domain_id=null when none is worth asking. An open category does not force a question and does not become complete when you stop. The internal fields must state the missing discriminator, how materially different "
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
        stopped = bool(result.get("no_useful_question"))
        opening = None if stopped else str(result.get("opening") or "").strip()
        if not stopped and not opening:
            raise ValueError("admission returned neither a question nor an explicit stop")
        admission = {
            "stage": "cross_area_pre_send",
            "decision": "stop"
            if stopped
            else "replace"
            if bool(result["changed_candidate"])
            else "admit",
            "candidate_question": str(candidate.get("opening", "")),
            "final_question": opening,
            "missing_discriminator": str(result["missing_discriminator"]),
            "decision_impact": str(result["decision_impact"]),
            "redundancy_check": str(result["redundancy_check"]),
        }
        return {
            "primary_domain_id": None if stopped else str(result["primary_domain_id"]),
            "opening": opening,
            "no_useful_question": stopped,
            "question_admission": admission,
        }


def _advance_existing_session(
    *,
    session: NaturalFlowRecoverabilitySession,
    model: ContinuousFlowRecoverabilityOpenAIModel,
    request: ContinuousAdvanceRequest,
) -> dict[str, Any]:
    if (
        getattr(session, "_draft_move", None) is not None
        or session.core.active_proposal_id is not None
    ):
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
    """One workflow controller and one client for the existing scientific substrate."""
    from .life_patterns_v2_owner_workflow_api import create_workflow_app

    return create_workflow_app(model=ContinuousFlowRecoverabilityOpenAIModel.from_env())


app = create_life_patterns_v2_owner_continuous_flow_app()
