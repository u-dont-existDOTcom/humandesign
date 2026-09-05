"""Text-first, chart-blind Discover Your Unique Life Patterns MVP.

This surface intentionally has no birth/chart/model-scoring dependency. It captures
participant-authored episodes, shows descriptive evidence-area progress, and can build
an evidence-linked neutral Life Patterns Map from those episodes.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request as URLRequest
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from .life_patterns_ui import HTML

Area = Literal[
    "decisions",
    "work_projects",
    "relationships",
    "self_initiated_actions",
    "learning_adaptation",
    "conflict_stress",
    "life_transitions",
    "other",
]
InputModality = Literal["typed", "voice"]
PatternStatus = Literal["stable", "context_dependent", "mixed", "tentative"]

AREA_LABELS: dict[str, str] = {
    "decisions": "Major decisions",
    "work_projects": "Work & projects",
    "relationships": "Relationships",
    "self_initiated_actions": "Self-initiated actions",
    "learning_adaptation": "Learning & adaptation",
    "conflict_stress": "Conflict & stress",
    "life_transitions": "Life phases & transitions",
}


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CreateSessionRequest(BaseModel):
    consent_to_store_responses: bool


class AddEpisodeRequest(BaseModel):
    token: str = Field(min_length=16)
    domain: Area
    title: str = Field(min_length=1, max_length=160)
    narrative: str = Field(min_length=1, max_length=20000)
    counterexample: str | None = Field(default=None, max_length=12000)
    input_modality: InputModality = "typed"


class MapRequest(BaseModel):
    token: str = Field(min_length=16)


class LifePattern(_FrozenModel):
    pattern_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    status: PatternStatus
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_episode_ids: tuple[str, ...] = Field(min_length=1)
    counterexample_episode_ids: tuple[str, ...] = ()
    contexts: tuple[str, ...] = ()
    limits: tuple[str, ...] = ()


class LifePatternsMap(_FrozenModel):
    schema_version: Literal["life-patterns-map-v1"] = "life-patterns-map-v1"
    overall_summary: str = Field(min_length=1)
    patterns: tuple[LifePattern, ...]
    strengths: tuple[str, ...] = ()
    friction_points: tuple[str, ...] = ()
    transfer_opportunities: tuple[str, ...] = ()
    reversible_experiments: tuple[str, ...] = ()
    important_unknowns: tuple[str, ...] = ()


class LifePatternsFileStore:
    """Small private file store for the MVP; resume tokens are stored only as hashes."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)

    def create(self) -> tuple[dict[str, Any], str]:
        session_id = f"LP-{uuid.uuid4().hex[:16].upper()}"
        token = secrets.token_urlsafe(32)
        now = datetime.now(UTC).isoformat()
        payload: dict[str, Any] = {
            "schema_version": "life-patterns-session-v1",
            "session_id": session_id,
            "token_sha256": hashlib.sha256(token.encode()).hexdigest(),
            "created_at": now,
            "updated_at": now,
            "status": "in_progress",
            "episodes": [],
            "life_patterns_map": None,
            "map_provider_receipt": None,
        }
        self._write(payload)
        return payload, token

    def read(self, session_id: str, token: str) -> dict[str, Any]:
        payload = self.read_private(session_id)
        supplied = hashlib.sha256(token.encode()).hexdigest()
        if not secrets.compare_digest(str(payload.get("token_sha256", "")), supplied):
            raise HTTPException(status_code=403, detail="invalid resume token")
        return payload

    def read_private(self, session_id: str) -> dict[str, Any]:
        path = self._path(session_id)
        if not path.exists():
            raise HTTPException(status_code=404, detail="session not found")
        try:
            value: Any = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=500, detail="stored session is unreadable") from exc
        if not isinstance(value, dict) or value.get("session_id") != session_id:
            raise HTTPException(status_code=500, detail="stored session is invalid")
        return cast(dict[str, Any], value)

    def save(self, payload: dict[str, Any]) -> None:
        payload["updated_at"] = datetime.now(UTC).isoformat()
        self._write(payload)

    def _path(self, session_id: str) -> Path:
        safe = "".join(ch for ch in session_id if ch.isalnum() or ch in "-_")
        if safe != session_id or not session_id.startswith("LP-"):
            raise HTTPException(status_code=400, detail="invalid session id")
        return self.root / f"{safe}.json"

    def _write(self, payload: dict[str, Any]) -> None:
        path = self._path(str(payload["session_id"]))
        temporary = path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.chmod(temporary, 0o600)
        temporary.replace(path)
        os.chmod(path, 0o600)


def _progress(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {area: 0 for area in AREA_LABELS}
    for episode in episodes:
        domain = str(episode.get("domain", ""))
        if domain in counts:
            counts[domain] += 1
    rows = []
    for area, label in AREA_LABELS.items():
        count = counts[area]
        status = "not_started" if count == 0 else "developing" if count == 1 else "strong"
        rows.append({"area": area, "label": label, "episode_count": count, "status": status})
    started = sum(row["status"] != "not_started" for row in rows)
    strong = sum(row["status"] == "strong" for row in rows)
    return {
        "status": "descriptive_evidence_coverage_not_completion_denominator",
        "areas": rows,
        "areas_started": started,
        "areas_strong": strong,
        "episode_count": len(episodes),
    }


def _public_session(payload: dict[str, Any]) -> dict[str, Any]:
    episodes = cast(list[dict[str, Any]], payload.get("episodes", []))
    return {
        "schema_version": payload.get("schema_version"),
        "session_id": payload["session_id"],
        "created_at": payload["created_at"],
        "updated_at": payload["updated_at"],
        "status": payload["status"],
        "episodes": episodes,
        "progress": _progress(episodes),
        "life_patterns_map": payload.get("life_patterns_map"),
        "map_provider_receipt": payload.get("map_provider_receipt"),
    }


def _map_schema() -> dict[str, Any]:
    pattern = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "pattern_id",
            "title",
            "summary",
            "status",
            "confidence",
            "supporting_episode_ids",
            "counterexample_episode_ids",
            "contexts",
            "limits",
        ],
        "properties": {
            "pattern_id": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "summary": {"type": "string", "minLength": 1},
            "status": {"type": "string", "enum": ["stable", "context_dependent", "mixed", "tentative"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "supporting_episode_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "counterexample_episode_ids": {"type": "array", "items": {"type": "string"}},
            "contexts": {"type": "array", "items": {"type": "string"}},
            "limits": {"type": "array", "items": {"type": "string"}},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "overall_summary",
            "patterns",
            "strengths",
            "friction_points",
            "transfer_opportunities",
            "reversible_experiments",
            "important_unknowns",
        ],
        "properties": {
            "schema_version": {"type": "string", "const": "life-patterns-map-v1"},
            "overall_summary": {"type": "string", "minLength": 1},
            "patterns": {"type": "array", "items": pattern},
            "strengths": {"type": "array", "items": {"type": "string"}},
            "friction_points": {"type": "array", "items": {"type": "string"}},
            "transfer_opportunities": {"type": "array", "items": {"type": "string"}},
            "reversible_experiments": {"type": "array", "items": {"type": "string"}},
            "important_unknowns": {"type": "array", "items": {"type": "string"}},
        },
    }


_MAP_SYSTEM = """You are a chart-blind behavioral synthesizer for Discover Your Unique Life Patterns.
You receive only participant-authored life episodes. You receive no birth data, astrology,
Human Design, candidate classification, hidden model output, rank, or model fit.

Build an evidence-linked behavioral map. Preserve context dependence, developmental change,
and counterexamples instead of forcing a coherent personality story. Do not diagnose mental
illness, infer hidden motives as facts, or tell the participant that a tendency is destiny.
Do not use astrology, Human Design, MBTI, Enneagram, attachment labels, or other personality
systems as explanatory shortcuts.

Every pattern must cite only supplied episode IDs. Confidence reflects the amount and
consistency of the supplied evidence, not certainty about the person. Use tentative or mixed
when evidence is sparse or contradictory. Transfer opportunities should identify strategies
that appear useful in one supplied context and might be worth testing elsewhere; phrase them
as hypotheses. Reversible experiments must be low-stakes, concrete tests, never medical,
legal, financial, or safety-critical directives. Return only the required JSON object."""


class OpenAILifePatternsMapper:
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
    def from_env(cls) -> OpenAILifePatternsMapper:
        return cls(
            api_key=os.environ.get("HDMATCH_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            model=os.environ.get("HDMATCH_LIFE_PATTERNS_MODEL", "gpt-5.6-luna").strip(),
            endpoint=os.environ.get("HDMATCH_LLM_API_URL", "https://api.openai.com/v1/responses").strip(),
            timeout_seconds=float(os.environ.get("HDMATCH_LIFE_PATTERNS_TIMEOUT_SECONDS", "90")),
        )

    def build(self, episodes: list[dict[str, Any]]) -> tuple[LifePatternsMap, dict[str, str]]:
        if not self.api_key:
            raise RuntimeError("Life Patterns mapper is not configured")
        if len(episodes) < 2:
            raise ValueError("at least two saved episodes are required before generating a map")
        body_obj = {
            "model": self.model,
            "instructions": _MAP_SYSTEM,
            "input": [{"role": "user", "content": json.dumps({"episodes": episodes}, ensure_ascii=False)}],
            "store": False,
            "reasoning": {"effort": "low"},
            "max_output_tokens": 8000,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "life_patterns_map_v1",
                    "strict": True,
                    "schema": _map_schema(),
                }
            },
        }
        request = URLRequest(
            self.endpoint,
            data=json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310 - fixed configured HTTPS API
                raw = cast(bytes, response.read())
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:1000]
            raise RuntimeError(f"Life Patterns mapper HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Life Patterns mapper network error: {exc.reason}") from exc
        parsed = LifePatternsMap.model_validate(_parse_openai_json(raw))
        known = {str(row["episode_id"]) for row in episodes}
        referenced = {
            episode_id
            for pattern in parsed.patterns
            for episode_id in (*pattern.supporting_episode_ids, *pattern.counterexample_episode_ids)
        }
        unknown = referenced - known
        if unknown:
            raise RuntimeError(f"Life Patterns mapper referenced unknown episodes: {sorted(unknown)}")
        return parsed, {
            "model": self.model,
            "endpoint": self.endpoint,
            "raw_response_sha256": hashlib.sha256(raw).hexdigest(),
        }


def _parse_openai_json(raw: bytes) -> dict[str, Any]:
    try:
        envelope_raw: Any = json.loads(raw.decode())
        envelope = cast(dict[str, Any], envelope_raw)
        texts: list[str] = []
        for item in cast(list[dict[str, Any]], envelope.get("output", [])):
            if item.get("type") != "message":
                continue
            for content in cast(list[dict[str, Any]], item.get("content", [])):
                if content.get("type") == "refusal":
                    raise RuntimeError("OpenAI refused the Life Patterns mapping request")
                if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                    texts.append(str(content["text"]))
        if not texts and isinstance(envelope.get("output_text"), str):
            texts.append(str(envelope["output_text"]))
        if not texts:
            raise ValueError("no output text")
        value: Any = json.loads("".join(texts))
        if not isinstance(value, dict):
            raise ValueError("output is not an object")
        return cast(dict[str, Any], value)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("OpenAI returned an invalid Life Patterns map") from exc


def _coaching_markdown(payload: dict[str, Any], result: LifePatternsMap) -> str:
    lines = [
        "# Life Patterns Coaching Context",
        "",
        "> Treat these as evidence-linked historical tendencies, not fixed traits or destiny.",
        "> Prefer reversible experiments and ask for current context before applying an old pattern.",
        "",
        "## Overall summary",
        "",
        result.overall_summary,
        "",
        "## Patterns",
        "",
    ]
    for pattern in result.patterns:
        lines.extend(
            [
                f"### {pattern.title}",
                "",
                pattern.summary,
                "",
                f"- Status: {pattern.status}",
                f"- Confidence: {pattern.confidence:.2f}",
                f"- Supporting episodes: {', '.join(pattern.supporting_episode_ids)}",
                f"- Counterexample episodes: {', '.join(pattern.counterexample_episode_ids) or 'none recorded'}",
                f"- Contexts: {', '.join(pattern.contexts) or 'not specified'}",
                f"- Limits: {', '.join(pattern.limits) or 'none specified'}",
                "",
            ]
        )
    for heading, values in (
        ("Strengths", result.strengths),
        ("Friction points", result.friction_points),
        ("Transfer opportunities", result.transfer_opportunities),
        ("Reversible experiments", result.reversible_experiments),
        ("Important unknowns", result.important_unknowns),
    ):
        lines.extend([f"## {heading}", ""])
        lines.extend(f"- {value}" for value in values)
        lines.append("")
    lines.extend(
        [
            "## Evidence provenance",
            "",
            f"- Session: {payload['session_id']}",
            f"- Saved episodes: {len(cast(list[dict[str, Any]], payload.get('episodes', [])))}",
            "- The map generator received no birth data, astrology, Human Design, candidate rank, or model fit.",
        ]
    )
    return "\n".join(lines).rstrip()


def create_life_patterns_app(
    *,
    store: LifePatternsFileStore,
    mapper: OpenAILifePatternsMapper | Any,
) -> FastAPI:
    app = FastAPI(title="Discover Your Unique Life Patterns", version="0.1.0")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok", "product": "discover-your-unique-life-patterns"}

    @app.post("/api/life-patterns/sessions")
    def create_session(request: CreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="private-storage consent is required")
        payload, token = store.create()
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "recovery_note": "Save the recovery file until durable email recovery is enabled.",
        }

    @app.get("/api/life-patterns/sessions/{session_id}")
    def get_session(session_id: str, token: str) -> dict[str, Any]:
        return _public_session(store.read(session_id, token))

    @app.post("/api/life-patterns/sessions/{session_id}/episodes")
    def add_episode(session_id: str, request: AddEpisodeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        episodes = cast(list[dict[str, Any]], payload.setdefault("episodes", []))
        episode = {
            "episode_id": f"EP-{uuid.uuid4().hex[:12].upper()}",
            "domain": request.domain,
            "title": request.title.strip(),
            "narrative": request.narrative.strip(),
            "counterexample": request.counterexample.strip() if request.counterexample else None,
            "input_modality": request.input_modality,
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
        episodes.append(episode)
        payload["life_patterns_map"] = None
        payload["map_provider_receipt"] = None
        store.save(payload)
        return {"episode": episode, "progress": _progress(episodes)}

    @app.post("/api/life-patterns/sessions/{session_id}/map")
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
                detail="The Life Patterns Map could not be generated. Your saved episodes were not changed.",
            ) from exc
        payload["life_patterns_map"] = result.model_dump(mode="json")
        payload["map_provider_receipt"] = receipt
        store.save(payload)
        return {"life_patterns_map": payload["life_patterns_map"], "provider_receipt": receipt}

    @app.get("/api/life-patterns/sessions/{session_id}/export")
    def export_profile(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        raw_map = payload.get("life_patterns_map")
        if not isinstance(raw_map, dict):
            raise HTTPException(status_code=409, detail="generate a Life Patterns Map before exporting")
        result = LifePatternsMap.model_validate(raw_map)
        return {
            "profile_json": {
                "schema_version": "life-patterns-portable-profile-v1",
                "session_id": session_id,
                "life_patterns_map": result.model_dump(mode="json"),
                "evidence_episode_ids": [row["episode_id"] for row in cast(list[dict[str, Any]], payload.get("episodes", []))],
                "interpretation_boundary": "historical_tendencies_not_fixed_traits",
            },
            "coaching_markdown": _coaching_markdown(payload, result),
        }

    return app


def create_life_patterns_app_from_env() -> FastAPI:
    root_value = os.environ.get("HDMATCH_LIFE_PATTERNS_STORE", "").strip()
    if not root_value:
        raise RuntimeError("HDMATCH_LIFE_PATTERNS_STORE is required")
    return create_life_patterns_app(
        store=LifePatternsFileStore(Path(root_value)),
        mapper=OpenAILifePatternsMapper.from_env(),
    )
