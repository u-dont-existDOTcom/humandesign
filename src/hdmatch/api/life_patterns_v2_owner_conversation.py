"""Hidden-ledger conversational owner probe for Life Patterns v2.

The participant sees an attentive conversation. Source-grounded episode facts and correction
lineage remain internal, while any person-level pattern still requires explicit participant
adjudication through the frozen v2 core.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.evaluation.participant_adjudicated_v2 import (
    EpisodeFactV2,
    EpisodeV2,
    PatternEvidenceLinkV2,
    PatternProposalV2,
)

from .life_patterns_v2_owner_app import (
    FactAssertionType,
    OpenAIOwnerV2Model,
    OwnerV2Model,
    OwnerV2Session,
    PatternAdjudicationRequest,
    _archive_sha,
    _parse_response_json,
    _source,
)
from .life_patterns_v2_owner_conversation_ui import HTML

MoveType = Literal["follow_up", "request_contrast", "boundary_question", "surface_hypothesis"]


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class HiddenFactCandidate(_FrozenModel):
    assertion_type: FactAssertionType
    proposition: str = Field(min_length=1, max_length=2000)


class HiddenFactCorrection(_FrozenModel):
    fact_id: str = Field(min_length=1)
    corrected_proposition: str = Field(min_length=1, max_length=2000)


class TurnExtraction(_FrozenModel):
    episode_summary: str = Field(min_length=1, max_length=500)
    facts: tuple[HiddenFactCandidate, ...] = Field(default=(), max_length=6)
    corrections: tuple[HiddenFactCorrection, ...] = Field(default=(), max_length=4)


class ConversationMove(_FrozenModel):
    reply: str = Field(min_length=1, max_length=3000)
    move_type: MoveType
    hypothesis_proposition: str | None = Field(default=None, max_length=1200)
    evidence_fact_ids: tuple[str, ...] = Field(default=(), max_length=12)

    @model_validator(mode="after")
    def hypothesis_fields_match_move(self) -> ConversationMove:
        if self.move_type == "surface_hypothesis":
            if not (self.hypothesis_proposition or "").strip():
                raise ValueError("surface_hypothesis requires hypothesis_proposition")
            if not self.evidence_fact_ids:
                raise ValueError("surface_hypothesis requires evidence_fact_ids")
        elif self.hypothesis_proposition is not None or self.evidence_fact_ids:
            raise ValueError("non-hypothesis moves cannot carry hypothesis fields")
        return self


class OwnerConversationModel(OwnerV2Model, Protocol):
    @property
    def configured(self) -> bool: ...

    def extract_turn(
        self,
        *,
        message: str,
        current_episode_id: str | None,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> TurnExtraction: ...

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[EpisodeV2, ...],
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> ConversationMove: ...


class OpenAIConversationModel(OpenAIOwnerV2Model):
    """OpenAI-compatible model with separate evidence and interviewer calls."""

    @classmethod
    def from_env(cls) -> OpenAIConversationModel:
        base = super().from_env()
        return cls(
            api_key=base.api_key,
            model=base.model,
            endpoint=base.endpoint,
            timeout_seconds=base.timeout_seconds,
        )

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
        if not self.api_key:
            raise RuntimeError(
                "The owner prototype needs HDMATCH_LLM_API_KEY or OPENAI_API_KEY in its runtime environment."
            )
        body = {
            "model": self.model,
            "instructions": instructions,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": effort},
            "max_output_tokens": max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                }
            },
        }
        request = URLRequest(
            self.endpoint,
            data=json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                raw = cast(bytes, response.read())
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:1000]
            raise RuntimeError(f"Owner Life Patterns model HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Owner Life Patterns model network error: {exc.reason}") from exc
        return _parse_response_json(raw)

    def extract_turn(
        self,
        *,
        message: str,
        current_episode_id: str | None,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> TurnExtraction:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["episode_summary", "facts", "corrections"],
            "properties": {
                "episode_summary": {"type": "string", "minLength": 1, "maxLength": 500},
                "facts": {
                    "type": "array",
                    "maxItems": 6,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["assertion_type", "proposition"],
                        "properties": {
                            "assertion_type": {
                                "type": "string",
                                "enum": [
                                    "positive_occurrence",
                                    "reported_appraisal_or_belief",
                                    "reported_outcome_or_resolution",
                                    "context",
                                    "temporal_relation",
                                ],
                            },
                            "proposition": {"type": "string", "minLength": 1, "maxLength": 2000},
                        },
                    },
                },
                "corrections": {
                    "type": "array",
                    "maxItems": 4,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["fact_id", "corrected_proposition"],
                        "properties": {
                            "fact_id": {"type": "string", "minLength": 1},
                            "corrected_proposition": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 2000,
                            },
                        },
                    },
                },
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "You maintain a hidden, target-theory-blind evidence ledger for an interview. "
                "Extract only literal or minimally normalized claims directly supported by the participant's latest message. "
                "Do not infer personality, recurrence, hidden motives, external theories, classifications, or information not supplied by the participant, "
                "or a preferred explanation. Do not turn silence or missingness into nonoccurrence. This bounded probe does not "
                "admit genuine absence facts; omit those rather than misclassify them. A participant may report a general belief "
                "or self-description; preserve that only as an attributed reported_appraisal_or_belief, not as independently "
                "established recurrence. Return a correction only when the latest participant message explicitly makes an existing "
                "operative fact materially wrong or too broad. Never silently rewrite a prior fact. Prefer fewer precise facts. "
                "episode_summary is a short neutral label for the current concrete situation, not a personality summary."
            ),
            payload={
                "latest_participant_message": message,
                "current_episode_id": current_episode_id,
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "episode_id": fact.episode_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-10:]),
            },
            schema=schema,
            effort="low",
            max_output_tokens=1600,
            schema_name="life_patterns_hidden_ledger_turn_v1",
        )
        return TurnExtraction.model_validate(result)

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[EpisodeV2, ...],
        operative_facts: tuple[EpisodeFactV2, ...],
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
            instructions=(
                "You are conducting an unusually attentive, target-theory-blind Life Patterns interview. "
                "The participant-facing objective is INFORMATION GAIN, not proving that you understood them. "
                "Return exactly one interviewer move. Ask at most one question. "
                "\n\nNEVER paraphrase or summarize the participant's last answer merely to show comprehension. "
                "A reflection is allowed only when a load-bearing ambiguity must be made explicit before the question. "
                "Do not ask the participant to certify obvious facts. Do not expose the hidden evidence ledger or fact IDs. "
                "\n\nChoose the next move that can most change the interpretation: mechanism, timing, realistic alternative, "
                "context, exception, developmental change, or a contrast between situations. If the current episode is sufficiently "
                "understood and there are not yet two distinct episodes, request a contrasting concrete episode rather than continuing "
                "to mine trivial detail. After multiple episodes, ask a boundary/counterexample question before surfacing a broad "
                "cross-episode hypothesis. "
                "\n\nUse surface_hypothesis only when boundary_answered=true and the cited hidden facts from at least two episodes "
                "support a nontrivial synthesis that adds explanatory compression beyond any single fact or restatement. The synthesis "
                "may identify a conditional, contrast, boundary, stable/context-dependent difference, or developmental change. "
                "Do not manufacture a pattern when the evidence is ordinary, thin, or incoherent; keep asking discriminating questions "
                "or request another contrasting example. "
                "\n\nWhen surfacing a hypothesis, phrase it tentatively and make the participant's authority obvious. No flattery, "
                "diagnosis, destiny language, motivational coaching, external-theory concepts, or model-targeting hints."
            ),
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
                "recent_conversation": list(recent_conversation[-16:]),
                "boundary_answered": boundary_answered,
            },
            schema=schema,
            effort="medium",
            max_output_tokens=1800,
            schema_name="life_patterns_conversation_move_v1",
        )
        return ConversationMove.model_validate(result)


@dataclass
class ConversationalOwnerSession:
    session_id: str
    model: OwnerConversationModel
    core: OwnerV2Session = field(init=False)
    conversation: list[dict[str, str]] = field(default_factory=list)
    current_episode_id: str | None = None
    awaiting_new_episode: bool = True
    pending_boundary_question: bool = False
    boundary_answered: bool = False

    def __post_init__(self) -> None:
        self.core = OwnerV2Session(session_id=self.session_id, model=self.model)

    def _operative_by_id(self) -> dict[str, EpisodeFactV2]:
        return {fact.fact_id: fact for fact in self.core.operative_facts()}

    def _episode_by_id(self, episode_id: str) -> EpisodeV2:
        for episode in self.core.record.episodes:
            if episode.episode_id == episode_id:
                return episode
        raise ValueError("episode not found")

    def _replace_episode(self, updated: EpisodeV2) -> None:
        episodes = tuple(
            updated if episode.episode_id == updated.episode_id else episode
            for episode in self.core.record.episodes
        )
        self.core.record = self.core.record.model_copy(update={"episodes": episodes})

    def _append_source(self, *, turn_id: str, text: str) -> str:
        source_id = f"SRC-{turn_id}"
        source = _source(
            source_id,
            self.session_id,
            f"runtime:conversation:{turn_id}",
            text,
        )
        sources = self.core.record.source_provenance + (source,)
        self.core.record = self.core.record.model_copy(
            update={
                "source_provenance": sources,
                "source_archive_sha256": _archive_sha(sources),
            }
        )
        return source_id

    def _apply_extraction(
        self,
        *,
        extraction: TurnExtraction,
        turn_id: str,
        message: str,
        start_new_episode: bool,
    ) -> None:
        if not extraction.facts and not extraction.corrections:
            return

        source_id = self._append_source(turn_id=turn_id, text=message)
        new_record_facts: list[EpisodeFactV2] = []
        affected_fact_ids: dict[str, list[str]] = {}

        episode_id = self.current_episode_id
        new_episode_id: str | None = None
        if extraction.facts and (start_new_episode or episode_id is None):
            episode_id = f"EP-{uuid.uuid4().hex[:10].upper()}"
            new_episode_id = episode_id
            self.current_episode_id = episode_id
            self.awaiting_new_episode = False

        if extraction.facts:
            assert episode_id is not None
            for candidate in extraction.facts:
                fact_id = f"{episode_id}-F-{uuid.uuid4().hex[:8].upper()}"
                fact = EpisodeFactV2(
                    fact_id=fact_id,
                    fact_lineage_id=f"LIN-{fact_id}",
                    revision_index=0,
                    episode_id=episode_id,
                    assertion_type=candidate.assertion_type,
                    actor="participant",
                    proposition=candidate.proposition,
                    source_provenance_ids=(source_id,),
                    temporal_relation_provenance_ids=(source_id,)
                    if candidate.assertion_type == "temporal_relation"
                    else (),
                )
                new_record_facts.append(fact)
                affected_fact_ids.setdefault(episode_id, []).append(fact.fact_id)

        operative = self._operative_by_id()
        for correction in extraction.corrections:
            predecessor = operative.get(correction.fact_id)
            if predecessor is None:
                raise ValueError("hidden correction cited unknown or superseded fact")
            revision_index = predecessor.revision_index + 1
            revised = predecessor.model_copy(
                update={
                    "fact_id": f"{predecessor.fact_id}-R{revision_index}",
                    "revision_index": revision_index,
                    "proposition": correction.corrected_proposition,
                    "supersedes_fact_id": predecessor.fact_id,
                    "participant_correction_provenance_ids": (source_id,),
                }
            )
            new_record_facts.append(revised)
            affected_fact_ids.setdefault(predecessor.episode_id, []).append(revised.fact_id)

        if new_record_facts:
            self.core.record = self.core.record.model_copy(
                update={"episode_facts": self.core.record.episode_facts + tuple(new_record_facts)}
            )

        if new_episode_id is not None:
            episode = EpisodeV2(
                episode_id=new_episode_id,
                neutral_summary=extraction.episode_summary,
                source_provenance_ids=(source_id,),
                fact_ids=tuple(affected_fact_ids[new_episode_id]),
            )
            self.core.record = self.core.record.model_copy(
                update={"episodes": self.core.record.episodes + (episode,)}
            )

        for affected_episode_id, new_ids in affected_fact_ids.items():
            if affected_episode_id == new_episode_id:
                continue
            episode = self._episode_by_id(affected_episode_id)
            source_ids = episode.source_provenance_ids
            if source_id not in source_ids:
                source_ids = source_ids + (source_id,)
            self._replace_episode(
                episode.model_copy(
                    update={
                        "source_provenance_ids": source_ids,
                        "fact_ids": episode.fact_ids + tuple(new_ids),
                    }
                )
            )

    def _create_pattern(self, move: ConversationMove) -> None:
        if self.core.active_proposal_id is not None:
            raise ValueError("a pattern proposal is already awaiting participant judgment")
        if not self.boundary_answered:
            raise ValueError("a cross-episode hypothesis requires a prior answered boundary check")

        fact_by_id = self._operative_by_id()
        evidence_ids = tuple(dict.fromkeys(move.evidence_fact_ids))
        if not set(evidence_ids).issubset(fact_by_id):
            raise ValueError("conversation hypothesis cited unknown or superseded fact IDs")
        episode_ids = {fact_by_id[fact_id].episode_id for fact_id in evidence_ids}
        if len(episode_ids) < 2:
            raise ValueError("conversation hypothesis must cite grounded facts from at least two episodes")

        proposition = (move.hypothesis_proposition or "").strip()
        if any(
            proposition.casefold() == fact_by_id[fact_id].proposition.strip().casefold()
            for fact_id in evidence_ids
        ):
            raise ValueError("conversation hypothesis cannot be an exact restatement of one cited fact")

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

    def turn(self, message: str) -> dict[str, Any]:
        clean = message.strip()
        if not clean:
            raise ValueError("message is required")
        if self.core.active_proposal_id is not None:
            raise ValueError("judge the current synthesis before continuing the interview")

        boundary_was_pending = self.pending_boundary_question
        if boundary_was_pending:
            self.pending_boundary_question = False
            self.boundary_answered = True

        turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
        user_turn = {"turn_id": turn_id, "role": "user", "text": clean}
        self.conversation.append(user_turn)

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

        if move.move_type == "request_contrast" and self.current_episode_id is None:
            move = ConversationMove(
                reply=(
                    "Stay with this situation for one more step: what happened next that most affected what you did?"
                ),
                move_type="follow_up",
            )
        elif move.move_type == "boundary_question" and len(self.core.record.episodes) < 2:
            move = ConversationMove(
                reply=(
                    "Give me a different real situation where you handled a similar kind of uncertainty differently."
                ),
                move_type="request_contrast",
            )
        elif move.move_type == "surface_hypothesis":
            if not self.boundary_answered or len(self.core.record.episodes) < 2:
                fallback_type: MoveType = (
                    "boundary_question" if len(self.core.record.episodes) >= 2 else "request_contrast"
                )
                fallback_reply = (
                    "Before I turn that into a pattern, what would be a real case where the apparent contrast does not hold?"
                    if fallback_type == "boundary_question"
                    else "I need a genuine contrast before that would mean anything. Tell me about another real situation where you handled it differently."
                )
                move = ConversationMove(reply=fallback_reply, move_type=fallback_type)
            else:
                try:
                    self._create_pattern(move)
                except ValueError:
                    move = ConversationMove(
                        reply=(
                            "I do not have enough clean cross-situation support for that synthesis yet. "
                            "Tell me about a case that would be most likely to break the pattern."
                        ),
                        move_type="boundary_question",
                    )

        if move.move_type == "request_contrast":
            self.awaiting_new_episode = True
            self.current_episode_id = None
        elif move.move_type == "boundary_question":
            self.pending_boundary_question = True

        assistant_turn = {
            "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
            "role": "assistant",
            "text": move.reply,
        }
        self.conversation.append(assistant_turn)

        return {
            "reply": move.reply,
            "move_type": move.move_type,
            "pattern_active": self.core.active_proposal_id is not None,
            "pattern_proposition": move.hypothesis_proposition
            if move.move_type == "surface_hypothesis"
            else None,
            "episode_count": len(self.core.record.episodes),
        }

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        return self.core.adjudicate_pattern(request)


@dataclass
class ConversationRuntime:
    model: OwnerConversationModel
    sessions: dict[str, ConversationalOwnerSession] = field(default_factory=dict)

    def create_session(self) -> ConversationalOwnerSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = ConversationalOwnerSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> ConversationalOwnerSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


class ConversationTurnRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)


class CreateConversationSessionResponse(_FrozenModel):
    session_id: str
    model_configured: bool
    opening: str


OPENING = (
    "Start with one specific situation from your life that feels representative, puzzling, or important. "
    "Tell me what happened in your own words. I’ll ask only the next question that seems capable of changing "
    "the picture, rather than making you approve a transcript of what you just said."
)


def create_life_patterns_v2_owner_conversation_app(
    *, model: OwnerConversationModel | None = None
) -> FastAPI:
    resolved_model = model or OpenAIConversationModel.from_env()
    runtime = ConversationRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 hidden-ledger owner conversation", version="0.2")

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
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=OPENING,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(
        session_id: str, request: ConversationTurnRequest
    ) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(
        session_id: str, request: PatternAdjudicationRequest
    ) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_conversation_app()
