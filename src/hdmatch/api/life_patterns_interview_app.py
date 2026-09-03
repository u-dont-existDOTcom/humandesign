"""Adaptive chart-blind interviewer for Discover Your Unique Life Patterns.

The interviewer receives only participant-authored conversation turns, completed neutral
episodes, and descriptive evidence coverage. It never receives birth data, chart data,
model predictions, candidate states, or model fit.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
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
You receive only the participant's own conversation turns, previously completed neutral life
episodes, and descriptive evidence-area progress. You receive no birth data, astrology,
Human Design, candidate classification, model prediction, rank, or model fit.

Your job is to understand the participant accurately enough that a later neutral behavioral
profile can preserve both recurring patterns and context differences.

INTERVIEW STYLE
- Sound attentive, curious, concise, and human.
- Ask ONE main question at a time.
- Prefer concrete episodes over global personality claims.
- When the participant makes a broad claim, ask for real examples and counterexamples.
- Explicitly welcome inconsistency across situations; do not pressure the participant to form
  one coherent personality story.
- Periodically reflect a tentative pattern and invite correction, especially when two episodes
  differ. Phrase reflections as observations from supplied evidence, never as diagnoses.
- Validate specificity, nuance, difficulty, or emotional significance. Do NOT praise a
  particular mechanism as wise, correct, intuitive, healthy, or theory-consistent.
- Separate what the participant knew/felt BEFORE an outcome from hindsight about whether the
  outcome later worked.
- Distinguish advice from hearing oneself speak, permission from informing, self-initiation
  from response to an opportunity, and situational urgency from a stable disposition when the
  participant's story makes those distinctions relevant.
- Ask how patterns changed across life phases when useful.
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

A completed episode is not a declaration that an evidence area is scientifically complete.
The progress object is descriptive only.

PROVISIONAL INSIGHT
A provisional_insight is optional. Use it only when there is a useful evidence-grounded
contrast or repeated pattern that could make the interview rewarding. It must invite revision,
for example: 'Across these two episodes, X seems different when Y changes. I may be making
that too simple.' Never state that the pattern is destiny or that a mechanism is correct.

Return only the required JSON object."""


def _interviewer_schema() -> dict[str, Any]:
    nullable_string = {"anyOf": [{"type": "string"}, {"type": "null"}]}
    nullable_area = {
        "anyOf": [
            {
                "type": "string",
                "enum": [*AREA_LABELS.keys(), "other"],
            },
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
            "completed_episodes": episodes,
            "recent_conversation_turns": turns[-18:],
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
        "progress": _progress(episodes),
        "life_patterns_map": payload.get("life_patterns_map"),
        "map_provider_receipt": payload.get("map_provider_receipt"),
    }


def create_life_patterns_interview_app(
    *,
    store: LifePatternsFileStore,
    interviewer: OpenAILifePatternsInterviewer | Any,
    mapper: OpenAILifePatternsMapper | Any,
    recovery: LifePatternsRecoveryService,
) -> FastAPI:
    app = FastAPI(title="Discover Your Unique Life Patterns", version="0.2.0")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "product": "discover-your-unique-life-patterns",
            "email_recovery_configured": recovery.configured,
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
        payload["interview_schema_version"] = "life-patterns-conversation-v1"
        payload["consent_to_llm_processing"] = True
        payload["contact_email_lookup_sha256"] = hashlib.sha256(email.encode()).hexdigest()
        payload["conversation_turns"] = []
        payload["last_completed_turn_index"] = 0
        store.save(payload)
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "email_recovery_configured": recovery.configured,
            "privacy_note": "The research record stores only a one-way email lookup hash, not the plaintext address.",
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
                episodes=episodes,
                turns=turns,
                progress=_progress(episodes),
            )
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail="Your message was saved, but the interviewer could not respond. You can safely try again.",
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
                "created_at_utc": datetime.now(UTC).isoformat(),
            }
            episodes.append(episode)
            payload["life_patterns_map"] = None
            payload["map_provider_receipt"] = None

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
        provisional = result.provisional_insight if len(episodes) >= 2 else None
        return {
            "reply": result.reply,
            "provisional_insight": provisional,
            "coverage_focus": result.coverage_focus,
            "episode_saved": episode is not None,
            "episode": episode,
            "progress": _progress(episodes),
            "map_available": len(episodes) >= 2,
        }

    @app.post("/api/life-patterns/interview/sessions/{session_id}/map")
    def build_map(session_id: str, request: MapRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
        try:
            result, receipt = mapper.build(episodes)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail="The Life Patterns Map could not be generated. Your saved interview was not changed.",
            ) from exc
        payload["life_patterns_map"] = result.model_dump(mode="json")
        payload["map_provider_receipt"] = receipt
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
        return {
            "profile_json": {
                "schema_version": "life-patterns-portable-profile-v1",
                "session_id": session_id,
                "life_patterns_map": result.model_dump(mode="json"),
                "evidence_episode_ids": [str(row["episode_id"]) for row in episodes],
                "interpretation_boundary": "historical_tendencies_not_fixed_traits",
                "integration_policy": {
                    "readable_by_coaching_or_inner_signal_with_user_consent": True,
                    "downstream_apps_must_not_silently_rewrite_research_evidence": True,
                },
            },
            "coaching_markdown": _coaching_markdown(payload, result),
        }

    @app.post("/api/life-patterns/interview/recovery/request")
    def request_recovery(request: RecoveryRequest) -> dict[str, str]:
        try:
            recovery.request(request.email)
        except ValueError:
            pass
        return {
            "status": "accepted",
            "message": "If a matching interview exists and recovery is configured, a one-time code has been sent.",
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
