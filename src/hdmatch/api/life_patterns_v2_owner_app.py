"""Owner-only real-data browser prototype for Life Patterns v2.

This is a bounded development surface. It accepts the owner's own episode narratives,
uses a target-theory-blind model to extract literal facts and propose at most one tentative
cross-episode pattern, and routes all accepted person-level claims through the frozen v2
participant-adjudication core. Runtime narratives live in memory only.
"""

from __future__ import annotations

import hashlib
import json
import os
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
    LifePatternsRecordV2,
    ParticipantAdjudicationV2,
    PatternEvidenceLinkV2,
    PatternProposalV2,
    SemanticCallbackProvenanceV2,
    SourceProvenanceV2,
    TheoryBlindSemanticCallbacksV2,
    build_adapter_projection_v2,
    freeze_life_patterns_record_v2,
    validate_life_patterns_record_v2,
)

from .life_patterns_v2_owner_ui import HTML

FactAssertionType = Literal[
    "positive_occurrence",
    "reported_appraisal_or_belief",
    "reported_outcome_or_resolution",
    "context",
    "temporal_relation",
]
FactReviewAction = Literal["accept", "correct", "not_supported"]
PatternDecision = Literal["accept", "revise", "reject", "unresolved"]
GroundingSource = Literal["examples", "other_situations", "unsure"]
FinalDecision = Literal["accept", "reject", "unresolved"]

_CONTRACT_SHA256 = hashlib.sha256(b"life-patterns-v2-owner-development-contract").hexdigest()
_CALLBACK_SHA256 = hashlib.sha256(b"life-patterns-v2-owner-development-grounding-v1").hexdigest()


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ExtractedFact(_FrozenModel):
    fact_id: str = Field(min_length=1)
    assertion_type: FactAssertionType
    proposition: str = Field(min_length=1)


class ExtractedEpisode(_FrozenModel):
    neutral_summary: str = Field(min_length=1)
    facts: tuple[ExtractedFact, ...] = Field(min_length=1, max_length=6)


class PatternSuggestion(_FrozenModel):
    has_candidate: bool
    proposition: str | None = None
    question_text: str | None = None
    evidence_fact_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def candidate_fields_match_flag(self) -> PatternSuggestion:
        if self.has_candidate:
            if not (self.proposition or "").strip() or not (self.question_text or "").strip():
                raise ValueError("candidate requires proposition and question_text")
            if not self.evidence_fact_ids:
                raise ValueError("candidate requires evidence_fact_ids")
        return self


class OwnerV2Model(Protocol):
    def extract_episode(self, episode_text: str, episode_id: str) -> ExtractedEpisode: ...

    def propose_pattern(self, facts: tuple[EpisodeFactV2, ...]) -> PatternSuggestion: ...


class OpenAIOwnerV2Model:
    """Small OpenAI-compatible client used only when the owner runs the local prototype."""

    def __init__(
        self,
        *,
        api_key: str | None,
        model: str = "gpt-5.6-luna",
        endpoint: str = "https://api.openai.com/v1/responses",
        timeout_seconds: float = 90.0,
    ) -> None:
        self.api_key = api_key.strip() if api_key else None
        self.model = model
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> OpenAIOwnerV2Model:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get("HDMATCH_LIFE_PATTERNS_OWNER_MODEL", "gpt-5.6-luna").strip(),
            endpoint=os.environ.get(
                "HDMATCH_LLM_API_URL", "https://api.openai.com/v1/responses"
            ).strip(),
            timeout_seconds=float(os.environ.get("HDMATCH_LIFE_PATTERNS_OWNER_TIMEOUT", "90")),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def _call_json(
        self, *, instructions: str, payload: dict[str, Any], schema: dict[str, Any]
    ) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError(
                "The owner prototype needs HDMATCH_LLM_API_KEY or OPENAI_"
                "API_KEY in its runtime environment."
            )
        body = {
            "model": self.model,
            "instructions": instructions,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": "low"},
            "max_output_tokens": 1800,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "life_patterns_owner_v2",
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

    def extract_episode(self, episode_text: str, episode_id: str) -> ExtractedEpisode:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["neutral_summary", "facts"],
            "properties": {
                "neutral_summary": {"type": "string", "minLength": 1},
                "facts": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 6,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["fact_id", "assertion_type", "proposition"],
                        "properties": {
                            "fact_id": {"type": "string", "minLength": 1},
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
                            "proposition": {"type": "string", "minLength": 1},
                        },
                    },
                },
            },
        }
        result = self._call_json(
            instructions=(
                "You are a target-theory-blind evidence extractor. Read o"
                "ne first-person episode and "
                "extract only literal or minimally normalized facts direc"
                "tly supported by that episode. "
                "Do not infer personality, recurrence, hidden motives, Hu"
                "man Design, astrology, or a person-level pattern. "
                "Do not turn silence into absence. Prefer fewer precise f"
                "acts. Use fact_id values F1, F2, ... ."
            ),
            payload={"episode_id": episode_id, "episode_text": episode_text},
            schema=schema,
        )
        return ExtractedEpisode.model_validate(result)

    def propose_pattern(self, facts: tuple[EpisodeFactV2, ...]) -> PatternSuggestion:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["has_candidate", "proposition", "question_text", "evidence_fact_ids"],
            "properties": {
                "has_candidate": {"type": "boolean"},
                "proposition": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "question_text": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "evidence_fact_ids": {"type": "array", "items": {"type": "string"}},
            },
        }
        result = self._call_json(
            instructions=(
                "You are a target-theory-blind pattern-hypothesis generat"
                "or. You receive only participant-reviewed "
                "episode facts from multiple episodes. If a useful cross-"
                "episode hypothesis is supported, propose at most "
                "one tentative person-level pattern as a question. Cite o"
                "nly the fact IDs that actually support it. "
                "Do not call it true, do not infer from missingness, and "
                "do not use any birth/chart/model concepts. "
                "If the evidence does not support a coherent cross-episod"
                "e hypothesis, return has_candidate=false."
            ),
            payload={
                "facts": [
                    {
                        "fact_id": fact.fact_id,
                        "episode_id": fact.episode_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in facts
                ]
            },
            schema=schema,
        )
        return PatternSuggestion.model_validate(result)


def _parse_response_json(raw: bytes) -> dict[str, Any]:
    payload = json.loads(raw)
    texts: list[str] = []
    if isinstance(payload, dict) and isinstance(payload.get("output_text"), str):
        texts.append(payload["output_text"])
    for item in payload.get("output", []) if isinstance(payload, dict) else []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                texts.append(content["text"])
    if not texts:
        raise RuntimeError("model response did not contain output text")
    try:
        parsed = json.loads(texts[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError("model output was not valid JSON") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("model output must be a JSON object")
    return parsed


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _source(source_id: str, record_id: str, locator: str, text: str) -> SourceProvenanceV2:
    return SourceProvenanceV2(
        source_provenance_id=source_id,
        source_record_id=record_id,
        locator=locator,
        content_sha256=_sha(text),
        exact_text_available=True,
    )


def _archive_sha(sources: tuple[SourceProvenanceV2, ...]) -> str:
    material = "|".join(sorted(row.content_sha256 for row in sources)) or "empty"
    return _sha(material)


@dataclass
class PendingEpisode:
    episode_id: str
    text: str
    extracted: ExtractedEpisode


@dataclass
class OwnerV2Session:
    session_id: str
    model: OwnerV2Model
    record: LifePatternsRecordV2 = field(
        default_factory=lambda: LifePatternsRecordV2(
            contract_sha256=_CONTRACT_SHA256,
            source_archive_sha256=_sha("empty"),
            source_provenance=(),
            episodes=(),
            episode_facts=(),
        )
    )
    pending_episodes: dict[str, PendingEpisode] = field(default_factory=dict)
    proposal_support: dict[str, frozenset[str]] = field(default_factory=dict)
    active_proposal_id: str | None = None

    def add_episode(self, text: str) -> PendingEpisode:
        clean = text.strip()
        if not clean:
            raise ValueError("episode text is required")
        episode_id = f"EP-{uuid.uuid4().hex[:10].upper()}"
        extracted = self.model.extract_episode(clean, episode_id)
        normalized_facts = tuple(
            fact.model_copy(update={"fact_id": f"{episode_id}-{fact.fact_id}"})
            for fact in extracted.facts
        )
        pending = PendingEpisode(
            episode_id=episode_id,
            text=clean,
            extracted=extracted.model_copy(update={"facts": normalized_facts}),
        )
        self.pending_episodes[episode_id] = pending
        return pending

    def review_episode(self, episode_id: str, reviews: tuple[FactReview, ...]) -> dict[str, Any]:
        pending = self.pending_episodes.get(episode_id)
        if pending is None:
            raise ValueError("pending episode not found")
        by_id = {fact.fact_id: fact for fact in pending.extracted.facts}
        if {row.fact_id for row in reviews} != set(by_id):
            raise ValueError("every proposed fact must receive exactly one review")

        episode_source_id = f"SRC-{episode_id}"
        new_sources: list[SourceProvenanceV2] = [
            _source(episode_source_id, episode_id, f"runtime:{episode_id}", pending.text)
        ]
        new_facts: list[EpisodeFactV2] = []
        episode_fact_ids: list[str] = []
        for review in reviews:
            draft = by_id[review.fact_id]
            if review.action == "not_supported":
                continue
            base = EpisodeFactV2(
                fact_id=draft.fact_id,
                fact_lineage_id=f"LIN-{draft.fact_id}",
                revision_index=0,
                episode_id=episode_id,
                assertion_type=draft.assertion_type,
                actor="participant",
                proposition=draft.proposition,
                source_provenance_ids=(episode_source_id,),
                temporal_relation_provenance_ids=(episode_source_id,)
                if draft.assertion_type == "temporal_relation"
                else (),
            )
            new_facts.append(base)
            episode_fact_ids.append(base.fact_id)
            if review.action == "correct":
                corrected = (review.corrected_proposition or "").strip()
                if not corrected:
                    raise ValueError("correct requires corrected_proposition")
                correction_source_id = f"SRC-CORR-{uuid.uuid4().hex[:10].upper()}"
                new_sources.append(
                    _source(
                        correction_source_id,
                        episode_id,
                        f"runtime:{episode_id}:correction",
                        corrected,
                    )
                )
                revision = base.model_copy(
                    update={
                        "fact_id": f"{base.fact_id}-R1",
                        "revision_index": 1,
                        "proposition": corrected,
                        "supersedes_fact_id": base.fact_id,
                        "participant_correction_provenance_ids": (correction_source_id,),
                    }
                )
                new_facts.append(revision)
                episode_fact_ids.append(revision.fact_id)

        if not episode_fact_ids:
            del self.pending_episodes[episode_id]
            return {"episode_saved": False, "reason": "no_supported_facts"}

        episode = EpisodeV2(
            episode_id=episode_id,
            neutral_summary=pending.extracted.neutral_summary,
            source_provenance_ids=(episode_source_id,),
            fact_ids=tuple(episode_fact_ids),
        )
        sources = self.record.source_provenance + tuple(new_sources)
        self.record = self.record.model_copy(
            update={
                "source_provenance": sources,
                "source_archive_sha256": _archive_sha(sources),
                "episodes": self.record.episodes + (episode,),
                "episode_facts": self.record.episode_facts + tuple(new_facts),
            }
        )
        del self.pending_episodes[episode_id]
        return {
            "episode_saved": True,
            "episode_id": episode_id,
            "operative_fact_ids": [
                fact.fact_id for fact in self.operative_facts() if fact.episode_id == episode_id
            ],
        }

    def operative_facts(self) -> tuple[EpisodeFactV2, ...]:
        latest: dict[str, EpisodeFactV2] = {}
        for fact in self.record.episode_facts:
            current = latest.get(fact.fact_lineage_id)
            if current is None or fact.revision_index > current.revision_index:
                latest[fact.fact_lineage_id] = fact
        return tuple(latest.values())

    def propose_pattern(self) -> PatternSuggestion:
        facts = self.operative_facts()
        episode_ids = {fact.episode_id for fact in facts}
        if len(episode_ids) < 2:
            raise ValueError(
                "This development probe waits for two reviewed episodes b"
                "efore asking for a cross-episode pattern."
            )
        suggestion = self.model.propose_pattern(facts)
        if not suggestion.has_candidate:
            return suggestion
        fact_by_id = {fact.fact_id: fact for fact in facts}
        evidence_ids = tuple(dict.fromkeys(suggestion.evidence_fact_ids))
        if not set(evidence_ids).issubset(fact_by_id):
            raise ValueError("pattern proposer cited unknown or superseded fact IDs")
        if len({fact_by_id[fact_id].episode_id for fact_id in evidence_ids}) < 2:
            raise ValueError(
                "cross-episode candidate must cite reviewed facts from at least two episodes"
            )

        proposal_id = f"PROP-{uuid.uuid4().hex[:10].upper()}"
        links: list[PatternEvidenceLinkV2] = []
        grouped: dict[str, list[str]] = {}
        for fact_id in evidence_ids:
            grouped.setdefault(fact_by_id[fact_id].episode_id, []).append(fact_id)
        for episode_id, grouped_fact_ids in grouped.items():
            links.append(
                PatternEvidenceLinkV2(
                    evidence_link_id=f"LINK-{uuid.uuid4().hex[:10].upper()}",
                    proposal_id=proposal_id,
                    episode_id=episode_id,
                    fact_ids=tuple(grouped_fact_ids),
                    role="preproposal_anchor",
                    acquisition_phase="pre_first_proposal",
                )
            )
        proposal = PatternProposalV2(
            proposal_id=proposal_id,
            pattern_thread_id=f"THREAD-{uuid.uuid4().hex[:10].upper()}",
            revision_index=0,
            proposition=cast(str, suggestion.proposition),
            question_text=cast(str, suggestion.question_text),
            evidence_link_ids=tuple(link.evidence_link_id for link in links),
            grounding_evidence_link_ids=tuple(link.evidence_link_id for link in links),
        )
        self.record = self.record.model_copy(
            update={
                "pattern_proposals": self.record.pattern_proposals + (proposal,),
                "pattern_evidence_links": self.record.pattern_evidence_links + tuple(links),
            }
        )
        self.proposal_support[proposal_id] = frozenset(evidence_ids)
        self.active_proposal_id = proposal_id
        return suggestion.model_copy(
            update={
                "proposition": proposal.proposition,
                "question_text": proposal.question_text,
                "evidence_fact_ids": evidence_ids,
            }
        )

    def adjudicate_pattern(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        if self.active_proposal_id is None:
            raise ValueError("no active pattern proposal")
        proposal = next(
            row
            for row in self.record.pattern_proposals
            if row.proposal_id == self.active_proposal_id
        )
        if request.decision != "revise":
            wording = proposal.proposition if request.decision == "accept" else None
            self._append_adjudication(proposal, request.decision, wording)
            return self._final_result()

        revised_wording = (request.revised_wording or "").strip()
        if not revised_wording:
            raise ValueError("revise requires revised_wording")
        if request.grounding_source != "examples":
            self._append_adjudication(proposal, "unresolved", revised_wording)
            result = self._final_result()
            result.update(
                {
                    "wording": revised_wording,
                    "needs_more_evidence": True,
                    "message": (
                        "That wording may still fit you, but these examples do no"
                        "t establish the added claim. "
                        "Add another real episode if you want to test it."
                    ),
                }
            )
            return result
        final_decision = request.final_decision
        if final_decision is None:
            raise ValueError("revised pattern grounded in examples requires final_decision")

        response_source_id = self._add_runtime_source(
            f"pattern revise: {revised_wording}", "participant-pattern-revision"
        )
        revise_adjudication = ParticipantAdjudicationV2(
            adjudication_id=f"ADJ-{uuid.uuid4().hex[:10].upper()}",
            proposal_id=proposal.proposal_id,
            decision="revise",
            participant_response_provenance_ids=(response_source_id,),
            participant_approved_wording=revised_wording,
        )
        revised_id = f"PROP-{uuid.uuid4().hex[:10].upper()}"
        old_links = [
            link
            for link in self.record.pattern_evidence_links
            if link.proposal_id == proposal.proposal_id
        ]
        revised_links = tuple(
            link.model_copy(
                update={
                    "evidence_link_id": f"LINK-{uuid.uuid4().hex[:10].upper()}",
                    "proposal_id": revised_id,
                }
            )
            for link in old_links
        )
        revised_proposal = PatternProposalV2(
            proposal_id=revised_id,
            pattern_thread_id=proposal.pattern_thread_id,
            revision_index=proposal.revision_index + 1,
            proposition=revised_wording,
            question_text=f"Does this version fit better: {revised_wording}",
            evidence_link_ids=tuple(link.evidence_link_id for link in revised_links),
            grounding_evidence_link_ids=tuple(link.evidence_link_id for link in revised_links),
            previous_proposal_id=proposal.proposal_id,
        )
        self.record = self.record.model_copy(
            update={
                "participant_adjudications": self.record.participant_adjudications
                + (revise_adjudication,),
                "pattern_proposals": self.record.pattern_proposals + (revised_proposal,),
                "pattern_evidence_links": self.record.pattern_evidence_links + revised_links,
            }
        )
        self.proposal_support[revised_id] = self.proposal_support[proposal.proposal_id]
        self.active_proposal_id = revised_id
        final_wording = revised_wording if final_decision == "accept" else None
        self._append_adjudication(revised_proposal, final_decision, final_wording)
        return self._final_result()

    def _add_runtime_source(self, text: str, locator: str) -> str:
        source_id = f"SRC-{uuid.uuid4().hex[:10].upper()}"
        source = _source(source_id, self.session_id, f"runtime:{locator}", text)
        sources = self.record.source_provenance + (source,)
        self.record = self.record.model_copy(
            update={"source_provenance": sources, "source_archive_sha256": _archive_sha(sources)}
        )
        return source_id

    def _append_adjudication(
        self,
        proposal: PatternProposalV2,
        decision: FinalDecision | PatternDecision,
        wording: str | None,
    ) -> None:
        source_id = self._add_runtime_source(
            f"pattern decision={decision}; wording={wording or ''}", "participant-pattern-decision"
        )
        adjudication = ParticipantAdjudicationV2(
            adjudication_id=f"ADJ-{uuid.uuid4().hex[:10].upper()}",
            proposal_id=proposal.proposal_id,
            decision=decision,
            participant_response_provenance_ids=(source_id,),
            participant_approved_wording=wording,
        )
        self.record = self.record.model_copy(
            update={
                "participant_adjudications": self.record.participant_adjudications + (adjudication,)
            }
        )

    def _callbacks(self) -> TheoryBlindSemanticCallbacksV2:
        return TheoryBlindSemanticCallbacksV2(
            provenance=SemanticCallbackProvenanceV2(
                validator_id="owner-v2-development-grounding",
                validator_version="1",
                validator_sha256=_CALLBACK_SHA256,
            ),
            asserts_real_world_nonoccurrence=lambda _fact: False,
            grounding_supports_current_proposition=lambda proposal, link, _facts: set(
                link.fact_ids
            ).issubset(self.proposal_support.get(proposal.proposal_id, frozenset())),
        )

    def _final_result(self) -> dict[str, Any]:
        callbacks = self._callbacks()
        validate_life_patterns_record_v2(self.record, callbacks=callbacks)
        frozen = freeze_life_patterns_record_v2(self.record, callbacks=callbacks)
        projection = build_adapter_projection_v2(frozen, callbacks=callbacks)
        terminal = frozen.payload.resolved_patterns[-1]
        return {
            "status": terminal.status,
            "wording": terminal.participant_approved_wording,
            "scope_note": terminal.scope_note,
            "exception_note": terminal.exception_note,
            "accepted_pattern_count": len(projection.accepted_patterns),
            "freeze_payload_sha256": frozen.freeze_payload_sha256,
            "needs_more_evidence": False,
        }


class CreateSessionResponse(_FrozenModel):
    session_id: str
    model_configured: bool


class EpisodeInput(BaseModel):
    text: str = Field(min_length=1, max_length=12000)


class FactReview(BaseModel):
    fact_id: str = Field(min_length=1)
    action: FactReviewAction
    corrected_proposition: str | None = Field(default=None, max_length=2000)


class EpisodeReviewRequest(BaseModel):
    reviews: tuple[FactReview, ...] = Field(min_length=1)


class PatternAdjudicationRequest(BaseModel):
    decision: PatternDecision
    revised_wording: str | None = Field(default=None, max_length=2000)
    grounding_source: GroundingSource | None = None
    final_decision: FinalDecision | None = None


@dataclass
class OwnerV2Runtime:
    model: OwnerV2Model
    sessions: dict[str, OwnerV2Session] = field(default_factory=dict)

    def create_session(self) -> OwnerV2Session:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = OwnerV2Session(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> OwnerV2Session:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_app(*, model: OwnerV2Model | None = None) -> FastAPI:
    resolved_model = model or OpenAIOwnerV2Model.from_env()
    runtime = OwnerV2Runtime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 owner development", version="0.1")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "owner_only": True,
            "target_theory_blind": True,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.post("/api/owner-v2/sessions")
    def create_session() -> CreateSessionResponse:
        session = runtime.create_session()
        return CreateSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
        )

    @app.post("/api/owner-v2/sessions/{session_id}/episodes")
    def add_episode(session_id: str, request: EpisodeInput) -> dict[str, Any]:
        try:
            pending = runtime.get(session_id).add_episode(request.text)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {
            "episode_id": pending.episode_id,
            "neutral_summary": pending.extracted.neutral_summary,
            "proposed_facts": [fact.model_dump(mode="json") for fact in pending.extracted.facts],
        }

    @app.post("/api/owner-v2/sessions/{session_id}/episodes/{episode_id}/review")
    def review_episode(
        session_id: str, episode_id: str, request: EpisodeReviewRequest
    ) -> dict[str, Any]:
        try:
            session = runtime.get(session_id)
            result = session.review_episode(episode_id, request.reviews)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        result["reviewed_episode_count"] = len(session.record.episodes)
        result["can_look_for_pattern"] = len(session.record.episodes) >= 2
        return result

    @app.post("/api/owner-v2/sessions/{session_id}/patterns/propose")
    def propose_pattern(session_id: str) -> dict[str, Any]:
        try:
            suggestion = runtime.get(session_id).propose_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return suggestion.model_dump(mode="json")

    @app.post("/api/owner-v2/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(session_id: str, request: PatternAdjudicationRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate_pattern(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_app()
