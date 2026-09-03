"""Read-only coaching over a participant-approved Life Patterns Map.

Coaching is downstream utility, not research evidence. It cannot edit episodes, the map,
or any future behavioral freeze.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .life_patterns_app import LifePatternsFileStore, LifePatternsMap, _parse_openai_json


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CoachRequest(BaseModel):
    token: str = Field(min_length=16)
    message: str = Field(min_length=1, max_length=12000)


class CoachResult(_FrozenModel):
    reply: str = Field(min_length=1)
    referenced_pattern_ids: tuple[str, ...] = ()
    suggested_experiment: str | None = None
    important_uncertainty: str | None = None
    boundary: str = "evidence_linked_coaching_not_fixed_identity_or_research_evidence"


_COACH_SYSTEM = """You are the optional Life Patterns Coach.
You receive a participant-approved neutral Life Patterns Map, its approved evidence episodes,
and one current user question. You receive no birth chart, astrology, Human Design, hidden
candidate, prediction rank, or model fit.

Use the map as evidence-linked historical tendencies, not destiny or identity. Distinguish:
1) what the participant's prior evidence actually supports;
2) a plausible interpretation of the current situation;
3) a low-stakes reversible experiment or question that could test the interpretation.

Look for Pattern Transfer: strategies that worked in one domain but may be underused in another.
Point out context differences and counterexamples instead of forcing consistency. When evidence
is insufficient, say so. Do not claim causation from correlation in the participant's history.
Do not diagnose mental illness. Do not give medical, legal, or financial directives. For high
stakes, focus on reflection, questions, and appropriate professional support.

The coach is downstream utility. Nothing said here becomes research evidence or changes the
participant's Life Patterns Map unless they separately return to the evidence-review flow.

Return only the required JSON object."""


def _coach_schema() -> dict[str, Any]:
    nullable_string = {"anyOf": [{"type": "string"}, {"type": "null"}]}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "reply",
            "referenced_pattern_ids",
            "suggested_experiment",
            "important_uncertainty",
            "boundary",
        ],
        "properties": {
            "reply": {"type": "string", "minLength": 1},
            "referenced_pattern_ids": {"type": "array", "items": {"type": "string"}},
            "suggested_experiment": nullable_string,
            "important_uncertainty": nullable_string,
            "boundary": {
                "type": "string",
                "const": "evidence_linked_coaching_not_fixed_identity_or_research_evidence",
            },
        },
    }


class OpenAILifePatternsCoach:
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
    def from_env(cls) -> OpenAILifePatternsCoach:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get("HDMATCH_LIFE_PATTERNS_COACH_MODEL", "gpt-5.6-luna").strip(),
            endpoint=os.environ.get(
                "HDMATCH_LLM_API_URL", "https://api.openai.com/v1/responses"
            ).strip(),
            timeout_seconds=float(os.environ.get("HDMATCH_LIFE_PATTERNS_COACH_TIMEOUT_SECONDS", "90")),
        )

    def respond(
        self,
        *,
        life_patterns_map: LifePatternsMap,
        approved_episodes: list[dict[str, Any]],
        message: str,
    ) -> tuple[CoachResult, dict[str, str]]:
        if not self.api_key:
            raise RuntimeError("Life Patterns coach is not configured")
        allowed_pattern_ids = {pattern.pattern_id for pattern in life_patterns_map.patterns}
        payload = {
            "life_patterns_map": life_patterns_map.model_dump(mode="json"),
            "approved_evidence_episodes": approved_episodes,
            "current_user_question": message,
        }
        body_obj = {
            "model": self.model,
            "instructions": _COACH_SYSTEM,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": "low"},
            "max_output_tokens": 1800,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "life_patterns_coach_v1",
                    "strict": True,
                    "schema": _coach_schema(),
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
            raise RuntimeError(f"Life Patterns coach HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Life Patterns coach network error: {exc.reason}") from exc
        result = CoachResult.model_validate(_parse_openai_json(raw))
        unknown = set(result.referenced_pattern_ids) - allowed_pattern_ids
        if unknown:
            raise RuntimeError(f"Life Patterns coach referenced unknown pattern IDs: {sorted(unknown)}")
        return result, {
            "model": self.model,
            "endpoint": self.endpoint,
            "raw_response_sha256": hashlib.sha256(raw).hexdigest(),
        }


def register_life_patterns_coach_routes(
    app: FastAPI,
    *,
    store: LifePatternsFileStore,
    coach: OpenAILifePatternsCoach | Any,
) -> None:
    @app.post("/api/life-patterns/interview/sessions/{session_id}/coach")
    def coach_turn(session_id: str, request: CoachRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("consent_to_llm_processing") is not True:
            raise HTTPException(status_code=409, detail="AI-processing consent is missing")
        raw_map = payload.get("life_patterns_map")
        if not isinstance(raw_map, dict):
            raise HTTPException(status_code=409, detail="build your Life Patterns Map before using Coach")
        life_map = LifePatternsMap.model_validate(raw_map)
        episodes_raw = cast(list[dict[str, Any]], payload.get("episodes", []))
        approved = [row for row in episodes_raw if row.get("review_status") == "approved"]
        before = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        try:
            result, receipt = coach.respond(
                life_patterns_map=life_map,
                approved_episodes=approved,
                message=request.message.strip(),
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail="Life Patterns Coach is temporarily unavailable") from exc
        after = json.dumps(store.read(session_id, request.token), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if before != after:
            raise RuntimeError("read-only Life Patterns coaching unexpectedly mutated the research record")
        return {
            "result": result.model_dump(mode="json"),
            "provider_receipt": receipt,
            "research_evidence_mutated": False,
        }
