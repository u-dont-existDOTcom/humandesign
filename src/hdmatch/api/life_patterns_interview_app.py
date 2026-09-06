"""Adaptive chart-blind interviewer for Discover Your Unique Life Patterns.

The interviewer is pattern-first and evidence-anchored: participant-reported recurring patterns
are understood in the participant's own terms, while concrete episodes remain provisional until
the participant approves, edits, or rejects them. Only participant-approved episodes feed
evidence progress, pattern synthesis, and portable exports.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .life_patterns_app import (
    AREA_LABELS,
    Area,
    InputModality,
    LifePatternsFileStore,
    LifePatternsMap,
    MapRequest,
    OpenAILifePatternsMapper,
    _coaching_markdown,
    _parse_openai_json,
    _progress,
)
from .life_patterns_interview_ui import HTML
from .life_patterns_recovery import (
    LifePatternsRecoveryService,
    LifePatternsRecoverySettings,
    normalize_email,
)
from .life_patterns_review_ui import REVIEW_SCRIPT

ReviewAction = Literal["approve", "edit", "reject"]

_RECENT_TURN_WINDOW = 24
_PARTICIPANT_HISTORY_MAX_TURNS = 80
_PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN = 1200


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CreateInterviewSessionRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    consent_to_store_responses: bool
    consent_to_llm_processing: bool


class InterviewTurnRequest(BaseModel):
    token: str = Field(min_length=16)
    message: str = Field(min_length=1, max_length=20000)
    input_modality: InputModality = "typed"


class EpisodeReviewRequest(BaseModel):
    token: str = Field(min_length=16)
    action: ReviewAction
    domain: Area | None = None
    title: str | None = Field(default=None, max_length=160)
    narrative: str | None = Field(default=None, max_length=20000)
    counterexample: str | None = Field(default=None, max_length=12000)


class RecoveryRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)


class RecoveryVerifyRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    otp: str = Field(pattern=r"^\d{6}$")


class InterviewerResult(_FrozenModel):
    reply: str = Field(min_length=1)
    episode_ready: bool
    episode_domain: Area | None = None
    episode_title: str | None = None
    episode_narrative: str | None = None
    episode_counterexample: str | None = None
    provisional_insight: str | None = None
    coverage_focus: str = Field(min_length=1)

    @model_validator(mode="after")
    def completed_episode_has_required_fields(self) -> InterviewerResult:
        if self.episode_ready:
            if self.episode_domain is None:
                raise ValueError("completed episode requires episode_domain")
            if not self.episode_title or not self.episode_title.strip():
                raise ValueError("completed episode requires episode_title")
            if not self.episode_narrative or not self.episode_narrative.strip():
                raise ValueError("completed episode requires episode_narrative")
        return self


_INTERVIEW_SYSTEM = """You are the chart-blind interviewer for Discover Your Unique Life Patterns.
You receive only the participant's own conversation turns, a compact index of earlier
participant statements, participant-approved neutral life episodes, and descriptive evidence
progress. You receive no birth data, astrology, Human Design, candidate classification, model
prediction, rank, or model fit.

Your job is to understand the participant accurately and efficiently enough that a later
neutral behavioral profile can preserve recurring patterns, context differences, uncertainty,
and change across life phases. Be purposeful about what misunderstanding or missing fact needs
clarification and neutral about which answer the participant gives.

PATTERN-FIRST, EVIDENCE-ANCHORED
- Start from what the participant says generally or repeatedly happens in a defined situation.
  A recurring/series report is legitimate self-report; do not force a dated incident merely to
  make the account feel more scientific.
- Use a concrete episode only when it materially anchors, clarifies, bounds, or challenges a
  reported pattern. One vivid incident is not a general pattern by itself.
- If the participant already supplied multiple examples or a clear repeated-series account, do
  not demand another example merely to satisfy a quota or evidence label.
- Ask about life-phase change when it matters. Use approximate ages/ranges and preserve unknown
  timing rather than seeking false precision. There is no arbitrary childhood cutoff.
- Ask for at most one exception/counterexample check when it could genuinely change the scope
  of a pattern. A valid exception must oppose the same proposition in a comparable situation;
  different actions or inner experiences may coexist.

ENGAGING AND ACCURATE LISTENING
- Sound attentive, concise, respectful, and human.
- Ask ONE main question at a time.
- When useful, briefly reflect the specific process the participant actually described before
  asking a question. A reflection is a tentative understanding they can correct, not a hidden
  interpretation.
- Keep reflections source-grounded. Do not "continue the paragraph" by supplying motives,
  fears, needs, emotions, causes, regrets, or meanings the participant did not report.
- Do not replace excessive questioning with excessive paraphrasing. If the account is already
  clear, move on.
- Ordinary respect is appropriate. Do NOT affirm or praise a particular behavior, mechanism,
  identity, independence, maturity, intuition, healthiness, compliance, resistance, or change.

FOCUS AND AUTONOMY
- Keep the immediate focus understandable: clarify the participant's own recurring pattern,
  context, evidence, or life-stage history. Do not imply there is a preferred answer.
- The participant may be uncertain, skip, pause, narrow a claim, or say they do not know.
- Never use motivational interviewing to evoke change talk, strengthen commitment, persuade
  the participant to change, or move toward planning. This is descriptive measurement, not a
  helping conversation aimed at behavior change.

FOLLOW-UP GATE
Before asking a follow-up, identify internally:
1. the specific missing or conflicting fact; and
2. how materially different answers would change the retained meaning, scope, developmental
   timing, evidence interpretation, or factual sequence.
If you cannot identify both, do not ask the question.

- Reuse information already present in recent turns, the participant_statement_index, and
  approved episodes. Do not ask the participant to restate information already supplied.
- Prioritize a material unresolved ambiguity over collecting a new domain/example.
- If the participant already said "I don't know," "I don't remember," or declined the point,
  preserve that disposition and do not repeat the question.
- Do not ask whether context "matters" in the abstract, whether important things are important,
  or whether people sometimes behave differently. Ask only for the specific context boundary
  that would alter the account.
- Do not silently narrow the participant's claim by adding regret, fear, pleasing, avoidance,
  success, failure, or another qualifier they did not state.
- coverage_focus names the single next material gap you are addressing. If no material gap
  warrants a question, use "none_material" rather than inventing coverage work.

INTERACTION MISMATCH / SELF-CORRECTION
If the participant says or clearly indicates "I already said that," "obviously," "I don't know
what you mean," or similar mismatch:
- treat it first as evidence that YOUR question may have been redundant, abstract, or unclear;
- check the available conversation before asking again;
- briefly acknowledge the mismatch without blaming the participant;
- either ask one simpler factual clarification that would materially change the record, or skip
  the question entirely.
Do not interpret such responses as resistance, avoidance, defensiveness, or personality data.

NEUTRALITY AND NON-LEADING RULES
- Explicitly welcome inconsistency across situations; do not pressure the participant to form
  one coherent personality story.
- Separate what the participant knew/felt BEFORE an outcome from hindsight about whether the
  outcome later worked.
- Distinguish narrator-stated explanation from objective causation. Temporal order alone does
  not establish influence.
- Never infer non-action from silence. If a factual claim depends on something not occurring,
  establish awareness, a meaningful opportunity/window, reasonable feasibility, and actual
  reported nonoccurrence; otherwise preserve uncertainty.
- Never mention or imply astrology, Human Design, MBTI, Enneagram, attachment labels, hidden
  chart categories, or other personality systems before behavioral lock.
- Do not diagnose mental illness or provide medical/legal/financial directives.

EPISODE CAPTURE
Set episode_ready=true only when the conversation contains a concrete, reasonably bounded
real-life episode with enough information to preserve what happened, relevant context, and
sequence over time. The neutral episode_narrative should summarize only participant-supplied
facts. Do not invent motives. A counterexample may be null when none has yet been supplied.
Use one of these neutral domains: decisions, work_projects, relationships,
self_initiated_actions, learning_adaptation, conflict_stress, life_transitions, other.

An extracted episode is only a provisional summary. The participant must approve or correct
it before it becomes evidence. A completed episode is not a declaration that an evidence area
is scientifically complete. Progress is descriptive only.

PROVISIONAL INSIGHT
A provisional_insight is optional. Use it only when a concise evidence-grounded reflection of a
repeated pattern or contrast among participant-approved episodes would help the participant
check your understanding. It must invite correction. Do not make it flattering, motivational,
diagnostic, causal, or destiny-like.

Return only the required JSON object."""


def _interviewer_schema() -> dict[str, Any]:
    nullable_string = {"anyOf": [{"type": "string"}, {"type": "null"}]}
    nullable_area = {
        "anyOf": [
            {"type": "string", "enum": [*AREA_LABELS.keys(), "other"]},
            {"type": "null"},
        ]
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "reply",
            "episode_ready",
            "episode_domain",
            "episode_title",
            "episode_narrative",
            "episode_counterexample",
            "provisional_insight",
            "coverage_focus",
        ],
        "properties": {
            "reply": {"type": "string", "minLength": 1},
            "episode_ready": {"type": "boolean"},
            "episode_domain": nullable_area,
            "episode_title": nullable_string,
            "episode_narrative": nullable_string,
            "episode_counterexample": nullable_string,
            "provisional_insight": nullable_string,
            "coverage_focus": {"type": "string", "minLength": 1},
        },
    }


def _participant_statement_index(turns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retain a compact cross-interview index so older participant answers stay visible."""

    statements: list[dict[str, Any]] = []
    for turn in turns:
        if turn.get("role") != "user":
            continue
        raw_text = turn.get("text")
        if not isinstance(raw_text, str):
            continue
        text = raw_text.strip()
        if not text:
            continue
        truncated = len(text) > _PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN
        statements.append(
            {
                "turn_id": str(turn.get("turn_id", "")),
                "text": text[:_PARTICIPANT_HISTORY_MAX_CHARS_PER_TURN],
                "text_truncated": truncated,
            }
        )
    return statements[-_PARTICIPANT_HISTORY_MAX_TURNS:]


class OpenAILifePatternsInterviewer:
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
    def from_env(cls) -> OpenAILifePatternsInterviewer:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get("HDMATCH_LIFE_PATTERNS_INTERVIEW_MODEL", "gpt-5.6-luna").strip(),
            endpoint=os.environ.get(
                "HDMATCH_LLM_API_URL", "https://api.openai.com/v1/responses"
            ).strip(),
            timeout_seconds=float(
                os.environ.get("HDMATCH_LIFE_PATTERNS_INTERVIEW_TIMEOUT_SECONDS", "90")
            ),
        )

    def respond(
        self,
        *,
        episodes: list[dict[str, Any]],
        turns: list[dict[str, Any]],
        progress: dict[str, Any],
    ) -> tuple[InterviewerResult, dict[str, str]]:
        if not self.api_key:
            raise RuntimeError("Life Patterns interviewer is not configured")
        payload = {
            "participant_approved_episodes": episodes,
            "participant_statement_index": _participant_statement_index(turns),
            "recent_conversation_turns": turns[-_RECENT_TURN_WINDOW:],
            "descriptive_evidence_progress": progress,
        }
        body_obj = {
            "model": self.model,
            "instructions": _INTERVIEW_SYSTEM,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": "low"},
            "max_output_tokens": 2200,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "life_patterns_interviewer_turn_v1",
                    "strict": True,
                    "schema": _interviewer_schema(),
                }
            },
        }
        request = URLRequest(
            self.endpoint,
            data=json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                raw = cast(bytes, response.read())
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:1000]
            raise RuntimeError(f"Life Patterns interviewer HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Life Patterns interviewer network error: {exc.reason}") from exc
        result = InterviewerResult.model_validate(_parse_openai_json(raw))
        return result, {
            "model": self.model,
            "endpoint": self.endpoint,
            "raw_response_sha256": hashlib.sha256(raw).hexdigest(),
        }


def _approved_episodes(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in episodes if row.get("review_status") == "approved"]


def _interview_progress(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    approved = _approved_episodes(episodes)
    progress = _progress(approved)
    progress["provisional_episode_count"] = sum(
        row.get("review_status") == "pending" for row in episodes
    )
    progress["rejected_episode_count"] = sum(
        row.get("review_status") == "rejected" for row in episodes
    )
    return progress


def _conversation_public_session(payload: dict[str, Any]) -> dict[str, Any]:
    episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
    return {
        "schema_version": payload.get("schema_version"),
        "interview_schema_version": payload.get("interview_schema_version"),
        "session_id": payload["session_id"],
        "created_at": payload["created_at"],
        "updated_at": payload["updated_at"],
        "status": payload["status"],
        "conversation_turns": payload.get("conversation_turns", []),
        "episodes": episodes,
        "progress": _interview_progress(episodes),
        "life_patterns_map": payload.get("life_patterns_map"),
        "map_provider_receipt": payload.get("map_provider_receipt"),
        "behavioral_freeze_receipts": payload.get("behavioral_freeze_receipts", []),
    }


def _find_episode(episodes: list[dict[str, Any]], episode_id: str) -> dict[str, Any]:
    for episode in episodes:
        if episode.get("episode_id") == episode_id:
            return episode
    raise HTTPException(status_code=404, detail="episode not found")


def create_life_patterns_interview_app(
    *,
    store: LifePatternsFileStore,
    interviewer: OpenAILifePatternsInterviewer | Any,
    mapper: OpenAILifePatternsMapper | Any,
    recovery: LifePatternsRecoveryService,
) -> FastAPI:
    app = FastAPI(title="Discover Your Unique Life Patterns", version="0.4.0")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML.replace("</body>", f"{REVIEW_SCRIPT}</body>")

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "product": "discover-your-unique-life-patterns",
            "email_recovery_configured": recovery.configured,
            "participant_review_required": True,
            "voice_enabled": False,
        }

    @app.post("/api/life-patterns/interview/sessions")
    def create_session(request: CreateInterviewSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="private-storage consent is required")
        if not request.consent_to_llm_processing:
            raise HTTPException(status_code=400, detail="AI-processing consent is required")
        try:
            email = normalize_email(request.email)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        payload, token = store.create()
        payload["interview_schema_version"] = "life-patterns-conversation-v3"
        payload["consent_to_llm_processing"] = True
        payload["contact_email_lookup_sha256"] = hashlib.sha256(email.encode()).hexdigest()
        payload["conversation_turns"] = []
        payload["last_completed_turn_index"] = 0
        store.save(payload)
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "email_recovery_configured": recovery.configured,
            "privacy_note": (
                "The research record stores only a one-way email lookup hash, "
                "not the plaintext address."
            ),
        }

    @app.get("/api/life-patterns/interview/sessions/{session_id}")
    def get_session(session_id: str, token: str) -> dict[str, Any]:
        return _conversation_public_session(store.read(session_id, token))

    @app.post("/api/life-patterns/interview/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: InterviewTurnRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("consent_to_llm_processing") is not True:
            raise HTTPException(status_code=409, detail="AI-processing consent is missing")
        turns = cast(list[dict[str, Any]], payload.setdefault("conversation_turns", []))
        episodes = cast(list[dict[str, Any]], payload.setdefault("episodes", []))
        approved = _approved_episodes(episodes)
        user_turn = {
            "turn_id": f"TURN-{uuid.uuid4().hex[:12].upper()}",
            "role": "user",
            "text": request.message.strip(),
            "input_modality": request.input_modality,
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
        turns.append(user_turn)
        store.save(payload)
        try:
            result, receipt = interviewer.respond(
                episodes=approved,
                turns=turns,
                progress=_progress(approved),
            )
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail=(
                    "Your message was saved, but the interviewer could not respond. "
                    "You can safely try again."
                ),
            ) from exc

        episode: dict[str, Any] | None = None
        if result.episode_ready:
            assert result.episode_domain is not None
            assert result.episode_title is not None
            assert result.episode_narrative is not None
            start_raw = payload.get("last_completed_turn_index", 0)
            start = start_raw if isinstance(start_raw, int) and start_raw >= 0 else 0
            source_turn_ids = [
                str(turn["turn_id"])
                for turn in turns[start:]
                if turn.get("role") == "user" and isinstance(turn.get("turn_id"), str)
            ]
            episode = {
                "episode_id": f"EP-{uuid.uuid4().hex[:12].upper()}",
                "domain": result.episode_domain,
                "title": result.episode_title.strip(),
                "narrative": result.episode_narrative.strip(),
                "counterexample": (
                    result.episode_counterexample.strip()
                    if result.episode_counterexample and result.episode_counterexample.strip()
                    else None
                ),
                "input_modality": request.input_modality,
                "source_turn_ids": source_turn_ids,
                "review_status": "pending",
                "participant_revision": False,
                "reviewed_at_utc": None,
                "created_at_utc": datetime.now(UTC).isoformat(),
            }
            episode["provisional_extraction"] = {
                "domain": episode["domain"],
                "title": episode["title"],
                "narrative": episode["narrative"],
                "counterexample": episode["counterexample"],
            }
            episode["review_events"] = []
            episodes.append(episode)

        assistant_turn = {
            "turn_id": f"TURN-{uuid.uuid4().hex[:12].upper()}",
            "role": "assistant",
            "text": result.reply,
            "created_at_utc": datetime.now(UTC).isoformat(),
            "provider_receipt": receipt,
        }
        turns.append(assistant_turn)
        if episode is not None:
            payload["last_completed_turn_index"] = len(turns)
        store.save(payload)
        provisional = result.provisional_insight if len(approved) >= 2 else None
        return {
            "reply": result.reply,
            "provisional_insight": provisional,
            "coverage_focus": result.coverage_focus,
            "episode_saved": episode is not None,
            "episode": episode,
            "episode_requires_participant_review": episode is not None,
            "progress": _interview_progress(episodes),
            "map_available": len(approved) >= 2,
        }

    @app.post(
        "/api/life-patterns/interview/sessions/{session_id}/episodes/{episode_id}/review"
    )
    def review_episode(
        session_id: str,
        episode_id: str,
        request: EpisodeReviewRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        episodes = cast(list[dict[str, Any]], payload.setdefault("episodes", []))
        episode = _find_episode(episodes, episode_id)
        if episode.get("review_status") != "pending":
            raise HTTPException(status_code=409, detail="episode has already been reviewed")
        if not isinstance(episode.get("provisional_extraction"), dict):
            episode["provisional_extraction"] = {
                "domain": episode.get("domain"),
                "title": episode.get("title"),
                "narrative": episode.get("narrative"),
                "counterexample": episode.get("counterexample"),
            }
        reviewed_at = datetime.now(UTC).isoformat()
        participant_revision: dict[str, Any] | None = None
        if request.action == "edit":
            title = (request.title or "").strip()
            narrative = (request.narrative or "").strip()
            if not title or not narrative:
                raise HTTPException(
                    status_code=422,
                    detail="an edited episode requires a title and corrected narrative",
                )
            episode["domain"] = request.domain or episode.get("domain", "other")
            episode["title"] = title
            episode["narrative"] = narrative
            episode["counterexample"] = (
                request.counterexample.strip()
                if request.counterexample and request.counterexample.strip()
                else None
            )
            episode["participant_revision"] = True
            episode["review_status"] = "approved"
            participant_revision = {
                "domain": episode["domain"],
                "title": episode["title"],
                "narrative": episode["narrative"],
                "counterexample": episode["counterexample"],
            }
        elif request.action == "approve":
            episode["review_status"] = "approved"
        else:
            episode["review_status"] = "rejected"
        review_events = episode.setdefault("review_events", [])
        if not isinstance(review_events, list):
            raise HTTPException(status_code=500, detail="stored episode review events are invalid")
        cast(list[dict[str, Any]], review_events).append(
            {
                "review_event_id": f"EPR-{uuid.uuid4().hex[:16].upper()}",
                "action": request.action,
                "participant_revision": participant_revision,
                "reviewed_at_utc": reviewed_at,
            }
        )
        episode["reviewed_at_utc"] = reviewed_at
        payload["life_patterns_map"] = None
        payload["map_provider_receipt"] = None
        store.save(payload)
        return {"episode": episode, "progress": _interview_progress(episodes)}

    @app.post("/api/life-patterns/interview/sessions/{session_id}/map")
    def build_map(session_id: str, request: MapRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
        approved = _approved_episodes(episodes)
        try:
            result, receipt = mapper.build(approved)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail=(
                    "The Life Patterns Map could not be generated. "
                    "Your saved interview was not changed."
                ),
            ) from exc
        payload["life_patterns_map"] = result.model_dump(mode="json")
        payload["map_provider_receipt"] = receipt
        payload["map_approved_episode_ids"] = [str(row["episode_id"]) for row in approved]
        store.save(payload)
        return {"life_patterns_map": payload["life_patterns_map"], "provider_receipt": receipt}

    @app.get("/api/life-patterns/interview/sessions/{session_id}/export")
    def export_profile(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        raw_map = payload.get("life_patterns_map")
        if not isinstance(raw_map, dict):
            raise HTTPException(status_code=409, detail="generate a Life Patterns Map before exporting")
        result = LifePatternsMap.model_validate(raw_map)
        episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
        approved = _approved_episodes(episodes)
        return {
            "profile_json": {
                "schema_version": "life-patterns-portable-profile-v1",
                "session_id": session_id,
                "life_patterns_map": result.model_dump(mode="json"),
                "evidence_episode_ids": [str(row["episode_id"]) for row in approved],
                "evidence_policy": "participant_approved_episodes_only",
                "interpretation_boundary": "historical_tendencies_not_fixed_traits",
                "integration_policy": {
                    "readable_by_coaching_or_inner_signal_with_user_consent": True,
                    "downstream_apps_must_not_silently_rewrite_research_evidence": True,
                },
                "research_freezes": payload.get("behavioral_freeze_receipts", []),
                "research_freeze_policy": (
                    "each receipt identifies a separate immutable research snapshot; "
                    "this live export may continue evolving"
                ),
            },
            "coaching_markdown": _coaching_markdown(
                {**payload, "episodes": approved},
                result,
            ),
        }

    @app.post("/api/life-patterns/interview/recovery/request")
    def request_recovery(request: RecoveryRequest) -> dict[str, str]:
        with suppress(ValueError):
            recovery.request(request.email)
        return {
            "status": "accepted",
            "message": (
                "If a matching interview exists and recovery is configured, "
                "a one-time code has been sent."
            ),
        }

    @app.post("/api/life-patterns/interview/recovery/verify")
    def verify_recovery(request: RecoveryVerifyRequest) -> dict[str, str]:
        try:
            recovered = recovery.verify(request.email, request.otp)
        except ValueError:
            recovered = None
        if recovered is None:
            raise HTTPException(status_code=403, detail="invalid or expired recovery code")
        return {
            "session_id": recovered.session_id,
            "resume_token": recovered.resume_token,
        }

    return app


def create_life_patterns_interview_app_from_env() -> FastAPI:
    root_value = os.environ.get("HDMATCH_LIFE_PATTERNS_STORE", "").strip()
    if not root_value:
        raise RuntimeError("HDMATCH_LIFE_PATTERNS_STORE is required")
    store = LifePatternsFileStore(Path(root_value))
    recovery = LifePatternsRecoveryService(
        store,
        LifePatternsRecoverySettings.from_env(),
    )
    return create_life_patterns_interview_app(
        store=store,
        interviewer=OpenAILifePatternsInterviewer.from_env(),
        mapper=OpenAILifePatternsMapper.from_env(),
        recovery=recovery,
    )