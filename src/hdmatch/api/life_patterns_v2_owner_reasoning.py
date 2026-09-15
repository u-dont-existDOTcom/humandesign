"""Adaptive owner-only Life Patterns conversation.

This layer restores the earlier interview's information-gain / burden discipline while preserving
Life Patterns v2's hidden evidence ledger and participant-authoritative pattern adjudication.
There is no fixed episode quota and no mandatory counterexample gate before a tentative synthesis.
A candidate pattern must also carry person-specific information beyond an obvious human regularity.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from hdmatch.evaluation.participant_adjudicated_v2 import (
    PatternEvidenceLinkV2,
    PatternProposalV2,
)

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationMove,
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_pattern_first import (
    PatternFirstOpenAIConversationModel,
    TemporaryModelProviderError,
)
from .life_patterns_v2_owner_refinement import (
    HTML,
    RefinablePatternFirstConversationalOwnerSession,
)


ADAPTIVE_OPENING = (
    "Start with a pattern you notice in your life that seems characteristic of you—something about "
    "how you tend to respond, change, choose, relate, focus, feel, or move through situations. It does "
    "not need to be rare or dramatic, but it should tell us more about you than an ordinary human "
    "regularity. I’ll use concrete situations only when they add useful information."
)


_ADAPTIVE_INTERVIEW_INSTRUCTIONS = (
    "You are conducting an unusually attentive, target-theory-blind Life Patterns interview. "
    "The objective is useful PERSON-SPECIFIC information per unit participant burden, not exhaustive "
    "interrogation, not proving that you understood them, and not forcing every uncertainty to closure. "
    "Return exactly one interviewer move and ask at most one question.\n\n"
    "PERSON-SPECIFIC SIGNAL: Recurrence alone is not enough. A useful Life Pattern must carry information "
    "about this participant beyond an obvious high-base-rate human regularity. Do not surface near-universal "
    "physiological or situational responses as person-level patterns merely because they recur. A pattern can "
    "still be simple and common in broad form when the participant supplies individual-specific timing, "
    "threshold, intensity, sequence, context sensitivity, exception structure, developmental shift, or another "
    "meaningful discriminator. Do NOT demand rarity or eccentricity. If commonness is genuinely uncertain, "
    "continue rather than filtering the pattern out. Simple is fine; generic is not.\n\n"
    "PATTERN-FIRST, EVIDENCE-ANCHORED: The participant may begin with a recurring/changing pattern in "
    "their own words. Treat that report as conversational context. Concrete situations can clarify, scope, "
    "challenge, or anchor it, but there is NO fixed episode quota. A counterexample or contrast is useful only "
    "when it can genuinely change the interpretation; it is never a mandatory ritual before a synthesis. A "
    "participant-reported series or recurring self-description is legitimate self-report. Do not force another "
    "dated episode merely to obtain a stronger-looking evidence label.\n\n"
    "FOLLOW-UP GATE: Before asking any follow-up, identify the exact missing or conflicting fact and how "
    "different plausible answers would materially change the retained pattern's meaning, scope, context, "
    "timing, exception structure, uncertainty, or person-specific information value. If the answer would not "
    "materially change any of those, DO NOT ask the question. Surface the narrow supported synthesis when it is "
    "person-specific; if the remaining formulation is generic, redirect to a more informative pattern instead. "
    "Unknown, not remembered, inapplicable, or declined may remain unresolved; do not reopen the same point "
    "without new participant information. Do not hunt for contradiction or hypothetical edge cases.\n\n"
    "LISTENING / REDUNDANCY: Never ask the participant to restate information already supplied. Never ask "
    "them to distinguish internal states they could not reasonably observe merely because the distinction is "
    "theoretically possible. If the participant says a question is obvious, redundant, confusing, or already "
    "answered, inspect your own question first, recover the existing answer, and drop the distinction unless "
    "it is genuinely material and answerable. Frustration with the interview is process feedback, not behavioral "
    "evidence.\n\n"
    "EVIDENCE DIRECTION: Additional factors are additive unless the participant supplied evidence comparing "
    "their importance. Never infer more/less, mainly, primarily, or rather-than without a real comparison. Do "
    "not transfer a factor from one context to another without support. Keep distinct reported outcomes distinct "
    "unless the participant links them. Do not use a broad label that merely renames the phenomenon as if it "
    "explained it. Missing recall is not evidence of absence.\n\n"
    "STOPPING: Do not manufacture depth. If the participant has described a straightforward person-specific "
    "pattern and further questions have low expected information gain, surface that narrow pattern. If the only "
    "remaining formulation is a generic human regularity, do not preserve it just because it is true; redirect. "
    "If a contextual modifier is supported, include it narrowly; if its role remains uncertain, say so rather "
    "than drilling indefinitely.\n\n"
    "SURFACING A HYPOTHESIS: Use surface_hypothesis when the available cited hidden facts support a useful "
    "person-level formulation with person-specific signal and another question is unlikely to materially improve "
    "it. One grounded episode may be enough when the participant has also supplied a recurring self-description; "
    "multiple episodes can strengthen or qualify a pattern but are not required. Do not promote a single occurrence "
    "into recurrence without participant self-report. Explanatory novelty is NOT required, but discriminative "
    "person-specific content is. Phrase the hypothesis tentatively and make participant authority obvious. No "
    "flattery, diagnosis, destiny language, motivational coaching, external-theory concepts, or target hints.\n\n"
    "AFTER REJECTION: If the participant rejects a synthesis, inspect the conversation for the likely unsupported "
    "premise yourself. Correct or narrow your working interpretation and ask only the smallest genuinely decision-changing "
    "question, if one remains. Do not default to asking the participant to explain an obvious mistake you can already see.\n\n"
    "For follow_up, request_contrast, and boundary_question return hypothesis_proposition=null and evidence_fact_ids=[]."
)


class AdaptivePatternFirstOpenAIConversationModel(PatternFirstOpenAIConversationModel):
    """Planner with adaptive stopping and a conservative person-specificity gate."""

    def assess_pattern_focus(
        self,
        *,
        pattern_text: str,
        recent_conversation: tuple[dict[str, str], ...],
    ) -> tuple[str, str]:
        """Triage clearly generic patterns before collecting episode evidence."""

        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["decision", "reply", "internal_reason"],
            "properties": {
                "decision": {
                    "type": "string",
                    "enum": ["continue", "redirect_generic"],
                },
                "reply": {"type": "string", "minLength": 1, "maxLength": 1800},
                "internal_reason": {"type": "string", "minLength": 1, "maxLength": 700},
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "Triage the participant's proposed Life Pattern for PERSON-SPECIFIC INFORMATION before "
                "collecting episode evidence. This is not a truth check and not a demand for novelty. A statement "
                "can be true and recurrent yet tell us almost nothing about this person because it is an obvious "
                "high-base-rate human regularity. Use redirect_generic only when that is clear from ordinary general "
                "knowledge and the statement contains no meaningful individual-specific modifier. Examples of clearly "
                "low-signal forms include getting hungry after not eating, becoming tired after prolonged lack of sleep, "
                "feeling pain when injured, or becoming thirsty after going without fluids. Do not infer that every "
                "common emotion or behavior is generic: timing, threshold, intensity, context sensitivity, sequence, "
                "exceptions, or developmental change can make a common dimension person-specific. If uncertain, choose "
                "continue. For redirect_generic, briefly say that the statement by itself tells us little about what is "
                "distinctive about the participant, then invite either one genuinely characteristic qualifier or a "
                "different pattern. Do not interrogate the generic regularity for arbitrary edge cases. For continue, "
                "ask for one concrete situation that best anchors the personally characteristic part. Keep the reply "
                "target-theory-blind and do not mention scoring, astrology, charts, hidden models, or prevalence statistics."
            ),
            payload={
                "proposed_pattern": pattern_text,
                "recent_conversation": list(recent_conversation[-8:]),
            },
            schema=schema,
            effort="medium",
            max_output_tokens=900,
            schema_name="life_patterns_pattern_specificity_v1",
        )
        decision = str(result.get("decision", "continue"))
        if decision not in {"continue", "redirect_generic"}:
            decision = "continue"
        reply = str(result.get("reply", "")).strip()
        if not reply:
            reply = (
                "Give me one concrete situation where the personally characteristic part of that pattern showed up."
                if decision == "continue"
                else "By itself that sounds like a common human regularity. What about it is especially characteristic of you, if anything?"
            )
        return decision, reply

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> ConversationMove:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "reply",
                "move_type",
                "hypothesis_proposition",
                "evidence_fact_ids",
            ],
            "properties": {
                "reply": {"type": "string", "minLength": 1, "maxLength": 3000},
                "move_type": {
                    "type": "string",
                    "enum": [
                        "follow_up",
                        "request_contrast",
                        "boundary_question",
                        "surface_hypothesis",
                    ],
                },
                "hypothesis_proposition": {
                    "anyOf": [
                        {"type": "string", "minLength": 1, "maxLength": 1200},
                        {"type": "null"},
                    ]
                },
                "evidence_fact_ids": {
                    "type": "array",
                    "maxItems": 12,
                    "items": {"type": "string"},
                },
            },
        }
        result = self._conversation_call_json(
            instructions=_ADAPTIVE_INTERVIEW_INSTRUCTIONS,
            payload={
                "current_episode_id": current_episode_id,
                "episodes": [
                    {
                        "episode_id": episode.episode_id,
                        "neutral_summary": episode.neutral_summary,
                    }
                    for episode in episodes
                ],
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "episode_id": fact.episode_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-20:]),
                "boundary_answered": boundary_answered,
                "boundary_answered_is_advisory_not_a_gate": True,
            },
            schema=schema,
            effort="medium",
            max_output_tokens=1800,
            schema_name="life_patterns_conversation_move_v1",
        )
        return ConversationMove.model_validate(result)


class AdaptiveRefinablePatternSession(RefinablePatternFirstConversationalOwnerSession):
    """Pattern-first session without quotas and with pre-evidence specificity triage."""

    def _start_or_redirect_pattern(self, clean: str) -> dict[str, Any]:
        assessor = getattr(self.model, "assess_pattern_focus", None)
        if not callable(assessor):
            return self._start_from_pattern(clean)

        decision, reply = assessor(
            pattern_text=clean,
            recent_conversation=tuple(self.conversation),
        )
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "user",
                "text": clean,
            }
        )
        if decision == "continue":
            self.pattern_focus_established = True
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": reply,
            }
        )
        return {
            "reply": reply,
            "move_type": "follow_up",
            "pattern_active": False,
            "pattern_proposition": None,
            "episode_count": 0,
            "pattern_focus_established": self.pattern_focus_established,
            "generic_pattern_redirected": decision == "redirect_generic",
        }

    def _create_pattern(self, move: ConversationMove) -> None:
        if self.core.active_proposal_id is not None:
            raise ValueError("a pattern proposal is already awaiting participant judgment")

        fact_by_id = self._operative_by_id()
        evidence_ids = tuple(dict.fromkeys(move.evidence_fact_ids))
        if not evidence_ids:
            raise ValueError("conversation hypothesis requires grounded evidence")
        if not set(evidence_ids).issubset(fact_by_id):
            raise ValueError("conversation hypothesis cited unknown or superseded fact IDs")

        proposition = (move.hypothesis_proposition or "").strip()
        if not proposition:
            raise ValueError("conversation hypothesis requires a proposition")

        exact_matches = [
            fact_by_id[fact_id]
            for fact_id in evidence_ids
            if proposition.casefold() == fact_by_id[fact_id].proposition.strip().casefold()
        ]
        if exact_matches and not any(
            fact.assertion_type == "reported_appraisal_or_belief" for fact in exact_matches
        ):
            raise ValueError(
                "an episode-only fact cannot be promoted unchanged into a person-level pattern"
            )

        proposal_id = f"PROP-{uuid.uuid4().hex[:10].upper()}"
        grouped: dict[str, list[str]] = {}
        for fact_id in evidence_ids:
            grouped.setdefault(fact_by_id[fact_id].episode_id, []).append(fact_id)
        links = tuple(
            PatternEvidenceLinkV2(
                evidence_link_id=f"LINK-{uuid.uuid4().hex[:10].upper()}",
                proposal_id=proposal_id,
                episode_id=episode_id,
                fact_ids=tuple(fact_ids),
                role="preproposal_anchor",
                acquisition_phase="pre_first_proposal",
            )
            for episode_id, fact_ids in grouped.items()
        )
        proposal = PatternProposalV2(
            proposal_id=proposal_id,
            pattern_thread_id=f"THREAD-{uuid.uuid4().hex[:10].upper()}",
            revision_index=0,
            proposition=proposition,
            question_text=move.reply,
            evidence_link_ids=tuple(link.evidence_link_id for link in links),
            grounding_evidence_link_ids=tuple(link.evidence_link_id for link in links),
        )
        self.core.record = self.core.record.model_copy(
            update={
                "pattern_proposals": self.core.record.pattern_proposals + (proposal,),
                "pattern_evidence_links": self.core.record.pattern_evidence_links + links,
            }
        )
        self.core.proposal_support[proposal_id] = frozenset(evidence_ids)
        self.core.active_proposal_id = proposal_id

    def _plan_refinement_move(self) -> ConversationMove:
        move = self.model.plan_turn(
            current_episode_id=self.current_episode_id,
            episodes=self.core.record.episodes,
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
            boundary_answered=self.boundary_answered,
        )
        if move.move_type == "request_contrast" and self.current_episode_id is None:
            return ConversationMove(reply=move.reply, move_type="follow_up")
        if move.move_type == "boundary_question" and not self.core.record.episodes:
            return ConversationMove(reply=move.reply, move_type="follow_up")
        if move.move_type == "surface_hypothesis":
            return ConversationMove(reply=move.reply, move_type="follow_up")
        return move

    def disagree_with_pattern(self) -> dict[str, Any]:
        if self.core.active_proposal_id is None:
            raise ValueError("no active pattern proposal to disagree with")
        snapshot = self._snapshot_state()
        try:
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "user",
                    "text": "No — that synthesis does not fit.",
                }
            )
            return self._apply_refinement_move(self._plan_refinement_move())
        except Exception:
            self._restore_state(snapshot)
            raise

    def turn(self, message: str) -> dict[str, Any]:
        clean = message.strip()
        if not clean:
            raise ValueError("message is required")
        if self.core.active_proposal_id is not None:
            return super().turn(clean)

        snapshot = self._snapshot_state()
        try:
            if not self.pattern_focus_established:
                return self._start_or_redirect_pattern(clean)

            if self.pending_boundary_question:
                self.pending_boundary_question = False
                self.boundary_answered = True

            turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
            self.conversation.append({"turn_id": turn_id, "role": "user", "text": clean})

            start_new_episode = self.awaiting_new_episode or self.current_episode_id is None
            extraction = self.model.extract_turn(
                message=clean,
                current_episode_id=self.current_episode_id,
                operative_facts=self.core.operative_facts(),
                recent_conversation=tuple(self.conversation),
            )
            self._apply_extraction(
                extraction=extraction,
                turn_id=turn_id,
                message=clean,
                start_new_episode=start_new_episode,
            )

            move = self.model.plan_turn(
                current_episode_id=self.current_episode_id,
                episodes=self.core.record.episodes,
                operative_facts=self.core.operative_facts(),
                recent_conversation=tuple(self.conversation),
                boundary_answered=self.boundary_answered,
            )

            if (
                move.move_type == "request_contrast" and self.current_episode_id is None
            ) or (
                move.move_type == "boundary_question" and not self.core.record.episodes
            ):
                move = ConversationMove(reply=move.reply, move_type="follow_up")
            elif move.move_type == "surface_hypothesis":
                try:
                    self._create_pattern(move)
                except ValueError:
                    move = ConversationMove(
                        reply=(
                            "I do not yet have grounded support for a person-level formulation. "
                            "What single detail would most change the pattern you originally described?"
                        ),
                        move_type="follow_up",
                    )

            if move.move_type == "request_contrast":
                self.awaiting_new_episode = True
                self.current_episode_id = None
            elif move.move_type == "boundary_question":
                self.pending_boundary_question = True

            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "assistant",
                    "text": move.reply,
                }
            )
            return {
                "reply": move.reply,
                "move_type": move.move_type,
                "pattern_active": self.core.active_proposal_id is not None,
                "pattern_proposition": move.hypothesis_proposition
                if move.move_type == "surface_hypothesis"
                else None,
                "episode_count": len(self.core.record.episodes),
            }
        except Exception:
            self._restore_state(snapshot)
            raise


@dataclass
class AdaptiveRefinableRuntime:
    model: OwnerConversationModel
    sessions: dict[str, AdaptiveRefinablePatternSession] = field(default_factory=dict)

    def create_session(self) -> AdaptiveRefinablePatternSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = AdaptiveRefinablePatternSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> AdaptiveRefinablePatternSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_reasoning_app(
    *, model: OwnerConversationModel | None = None
) -> FastAPI:
    """Compatibility entry point; now serves the adaptive specificity-aware interviewer."""

    resolved_model = model or AdaptivePatternFirstOpenAIConversationModel.from_env()
    runtime = AdaptiveRefinableRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 adaptive owner conversation", version="0.9")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "owner_only": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "pattern_first": True,
            "person_specificity_gate": True,
            "unresolved_thread_continuation": True,
            "rejected_synthesis_continuation": True,
            "adaptive_information_gain_gate": True,
            "fixed_episode_quota": False,
            "mandatory_counterexample_gate": False,
            "hypothesis_support_audit": False,
            "rejection_reasoning_recovery": True,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=ADAPTIVE_OPENING,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/continue")
    def continue_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).continue_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/disagree")
    def disagree_with_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).disagree_with_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(session_id: str, request: PatternAdjudicationRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_reasoning_app()
