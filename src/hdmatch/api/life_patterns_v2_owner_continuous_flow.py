"""Continuous natural-flow owner interview with a pre-send question-admission gate.

The fixed recoverability surface remains target-theory-blind and standardized, but the
participant should experience one continuous interview rather than a sequence of category
checkpoints. This layer keeps the current server session alive across measurement areas,
feeds prior participant answers into continuation planning, and runs a separate low-cost
admission pass before any model-generated question is shown.
"""

from __future__ import annotations

import uuid
import os
from typing import Any, Literal, cast

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .life_patterns_v2_owner_dialogue import ParticipantInput, ROUTING_POLICY, QUESTION_POLICY, INTERVIEW_POLICY
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

    def __init__(self, *, api_key: str | None, model: str = "gpt-5.6-sol",
                 endpoint: str = "https://api.openai.com/v1/responses",
                 timeout_seconds: float = 180.0) -> None:
        super().__init__(api_key=api_key, model=model, endpoint=endpoint,
                         timeout_seconds=timeout_seconds)
        self._question_admission_by_reply: dict[str, list[dict[str, Any]]] = {}

    @classmethod
    def from_env(cls) -> ContinuousFlowRecoverabilityOpenAIModel:
        return cls(api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
                   model=os.environ.get("HDMATCH_LIFE_PATTERNS_OWNER_MODEL", "gpt-5.6-sol").strip(),
                   endpoint=os.environ.get("HDMATCH_LLM_API_URL", "https://api.openai.com/v1/responses").strip(),
                   timeout_seconds=float(os.environ.get("HDMATCH_LIFE_PATTERNS_OWNER_TIMEOUT", "180")))

    def model_profile(self) -> dict[str, Any]:
        return {"interviewer_model": self.model, "interviewer_reasoning": "xhigh",
                "extraction_model": "gpt-5.6-luna", "extraction_reasoning": "low",
                "semantic_max_output_tokens": 25000, "automatic_model_fallback": False}

    def _request_settings(self, schema_name: str, effort: str, maximum: int) -> dict[str, Any]:
        extraction = schema_name == "life_patterns_hidden_ledger_turn_v1"
        return {"model": "gpt-5.6-luna" if extraction else self.model,
                "reasoning": {"effort": "low" if extraction else "xhigh"},
                "max_output_tokens": max(maximum, 2500 if extraction else 25000)}

    def _observe_model_response(self, schema_name: str, settings: dict[str, Any],
                                response: dict[str, Any], elapsed: float) -> None:
        context = current_interview_context()
        sink = context.get("model_call_sink") if context else None
        if isinstance(sink, list):
            usage = response.get("usage") or {}
            sink.append({"schema": schema_name, "requested_model": settings["model"],
                         "returned_model": response.get("model"),
                         "reasoning_effort": settings["reasoning"]["effort"],
                         "status": response.get("status"), "duration_seconds": round(elapsed, 3),
                         "input_tokens": usage.get("input_tokens"),
                         "output_tokens": usage.get("output_tokens"),
                         "reasoning_tokens": (usage.get("output_tokens_details") or {}).get("reasoning_tokens")})

    def route_participant_turn(self, *, message: str, evidence_context: dict[str, Any]) -> ParticipantInput:
        result = self._conversation_call_json(
            instructions=ROUTING_POLICY,
            payload={"latest_participant_message": message},
            schema=ParticipantInput.model_json_schema(), effort="medium", max_output_tokens=1800,
            schema_name="life_patterns_participant_input_v1")
        route = ParticipantInput.model_validate(result)
        route.check_source(message)
        return route

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
                key: value for key, value in context.items() if key not in {"admission_sink", "model_call_sink", "conversation", "evidence_conversation"}
            }
            payload = {
                **payload,
                "recent_conversation": context["conversation"],
                "shared_evidence_context": source_context,
            }
        if schema_name == "life_patterns_hidden_ledger_turn_v1" and context is not None:
            payload = {**payload,
                       "recent_conversation": context.get("evidence_conversation", context["conversation"]),
                       "shared_evidence_context": {"operative_facts": context.get("operative_facts", [])}}
            instructions += " Extract ONLY the latest approved evidence excerpts; do not extract process feedback from the surrounding conversation."
        if schema_name in {"life_patterns_conversation_move_v1", "life_patterns_refinement_move_v1"}:
            instructions = INTERVIEW_POLICY
        elif schema_name != "life_patterns_hidden_ledger_turn_v1":
            instructions += "\n\n" + QUESTION_POLICY
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
                "Review ONLY the actual candidate proposition, not a previous formulation. Compare its meaning "
                "with saved/accepted/rejected patterns and exact participant sources. Return duplicate when it "
                "only repeats a recorded idea without a material new relationship, scope or correction; identify "
                "the existing proposal. A paraphrase or extra evidence for the same unchanged idea is still a "
                "duplicate, but shared evidence alone does not make genuinely different claims duplicates. "
                "Return direct for an endorsed person-specific report already explicitly stated with all "
                "qualifiers, attribution, negation and time intact. Familiarity or conditionality is not a defect. "
                "A substring of quoted, negated or no-longer-endorsed text is not automatically endorsed. "
                "Return inference only for a genuinely added plausible relation to judge. inference_quote must "
                "be an exact substring of THIS candidate containing what was added; inference_added explains "
                "that actual addition. Do not describe additions absent from the candidate. Return context_only "
                "for unsupported motives, causal/directional additions or generic/contextual material, not for "
                "an unfamiliar but supported direct statement. A rejected or disputed claim is not settled truth. "
                "Output new_information briefly; never manufacture novelty. This is fallible product judgment."
            ),
            payload={"candidate": move.model_dump(mode="json")},
            schema={"type": "object", "additionalProperties": False,
                    "required": ["decision", "inference_added", "inference_quote", "source_reason",
                                 "related_proposal_id", "new_information"],
                    "properties": {
                        "decision": {"type": "string", "enum": ["direct", "inference", "context_only", "duplicate"]},
                        **{key: {"type": "string", "maxLength": 1000} for key in
                           ["inference_added", "inference_quote", "source_reason", "related_proposal_id", "new_information"]}}},
            effort="medium", max_output_tokens=1800, schema_name="life_patterns_formulation_fidelity_v2")

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
                "premises_supported", "scope_preserved", "contrast_answerable",
            ],
            "properties": {
                "decision": {"type": "string", "enum": ["admit", "replace", "stop"]},
                **{key: {"type": "boolean"} for key in ["premises_supported", "scope_preserved", "contrast_answerable"]},
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
                "already answered. Set the three logic-check booleans for the FINAL emitted question (a replacement when selected). A non-contrast open question can have contrast_answerable=true."
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
        if not all(result.get(key, False) for key in ("premises_supported", "scope_preserved", "contrast_answerable")):
            decision = "stop"
        evidence: dict[str, Any] = {
            "stage": "in_thread_pre_send",
            "decision": decision,
            "candidate_question": candidate.reply,
            "logic_checks": {key: result.get(key) for key in ["premises_supported", "scope_preserved", "contrast_answerable"]},
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

    def plan_refinement_turn(self, **kwargs: Any) -> Any:
        schema = self._move_schema()
        schema["properties"]["move_type"]["enum"].append("topic_complete")
        payload = {k: v for k, v in kwargs.items() if k not in {"episodes", "operative_facts"}}
        result = self._conversation_call_json(
            instructions=INTERVIEW_POLICY, payload=payload, schema=schema,
            effort="medium", max_output_tokens=1800, schema_name="life_patterns_refinement_move_v1")
        if result.get("move_type") == "topic_complete":
            return TopicCompleteMove(reply="I do not see a useful further question about that interpretation.")
        return ConversationMove.model_validate(result)

    def plan_turn(self, **kwargs: Any) -> Any:
        return super().plan_turn(**kwargs)

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
                "premises_supported", "scope_preserved", "contrast_answerable",
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
                **{key: {"type": "boolean"} for key in ["premises_supported", "scope_preserved", "contrast_answerable"]},
                "missing_discriminator": {"type": "string", "minLength": 1, "maxLength": 600},
                "decision_impact": {"type": "string", "minLength": 1, "maxLength": 700},
                "redundancy_check": {"type": "string", "minLength": 1, "maxLength": 700},
                "changed_candidate": {"type": "boolean"},
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "You are the FINAL PRE-SEND ADMISSION GATE for the next question in a continuous, target-theory-blind "
                "Life Patterns interview. This is an authorized cross-area transition after completion/deferment, not an in-thread repair; choose a new useful open focus. The first-pass candidate is only a draft. Inspect the participant's prior "
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
                "answers would change interpretation, and why the question is not already answered. Report all three logic booleans for the FINAL question; open questions without a contrast are contrast_answerable=true. Consult legacy planning knowledge without claiming lost source evidence is recovered. Prefer another genuinely unknown area over restarting a covered one."
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
        stopped = bool(result.get("no_useful_question")) or not all(
            result.get(key, False) for key in ("premises_supported", "scope_preserved", "contrast_answerable"))
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
            "logic_checks": {key: result.get(key) for key in ["premises_supported", "scope_preserved", "contrast_answerable"]},
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
