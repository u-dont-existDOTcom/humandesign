"""Isolated participant HTTP surface: no astrology or owner-app imports."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from .domain import (
    VERSION,
    export_record,
    import_record,
    load_instrument,
    new_state,
    strict_json,
    utc,
)
from .engine import PAYMENT_ERROR, Engine, ProviderError, Venice
from .store import Conflict, Missing, Store, canonical, digest

STATIC = Path(__file__).parent / "static"


@dataclass(frozen=True)
class Settings:
    database: Path
    encryption_key: str
    admin_token: str
    join_token: str
    authority: Path
    submission_token: str = ""
    gateway_url: str = "https://venice-model-gateway-production.up.railway.app/v1"
    gateway_token: str = ""
    model: str = "openai-gpt-56-sol"
    effort: str = "xhigh"
    secure_cookies: bool = True
    maximum_sessions: int = 50
    maximum_calls: int = 12
    live_enabled: bool = False
    public_origin: str = ""

    @classmethod
    def from_env(cls):
        required = ("PARTICIPANT_DATA_KEY", "PARTICIPANT_ADMIN_TOKEN", "PARTICIPANT_JOIN_TOKEN")
        if any(not os.environ.get(k) for k in required):
            raise RuntimeError("Participant storage and access secrets must be configured.")
        path = Path(os.environ.get("PARTICIPANT_DB", "/data/survey.sqlite3"))
        if os.environ.get("RAILWAY_ENVIRONMENT_ID"):
            volume_path = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
            if not volume_path or not path.resolve().is_relative_to(Path(volume_path).resolve()):
                raise RuntimeError("A persistent Railway volume is required.")
        return cls(
            database=path,
            encryption_key=os.environ[required[0]],
            admin_token=os.environ[required[1]],
            join_token=os.environ[required[2]],
            authority=Path(os.environ.get("SURVEY_AUTHORITY_DIR", "/app/authority")),
            submission_token=os.environ.get("PARTICIPANT_GPT_SUBMISSION_TOKEN", ""),
            gateway_url=os.environ.get(
                "UDA_MODEL_GATEWAY_URL", "https://venice-model-gateway-production.up.railway.app"
            ).rstrip("/")
            + "/v1",
            gateway_token=os.environ.get("UDA_MODEL_GATEWAY_TOKEN", ""),
            model=os.environ.get("PARTICIPANT_MODEL", "openai-gpt-56-sol"),
            effort=os.environ.get("PARTICIPANT_REASONING", "xhigh"),
            live_enabled=os.environ.get("PARTICIPANT_LIVE_ENABLED") == "1",
            public_origin=os.environ.get("PARTICIPANT_PUBLIC_ORIGIN", "").rstrip("/"),
            maximum_sessions=int(os.environ.get("PARTICIPANT_MAX_SESSIONS", "50")),
            maximum_calls=int(os.environ.get("PARTICIPANT_MAX_MODEL_CALLS", "12")),
        )


class Body(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Access(Body):
    token: str = Field(min_length=32, max_length=128)


class Operation(Body):
    revision: int = Field(ge=0)
    operation_id: str = Field(min_length=12, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    action: Literal[
        "consent",
        "decline",
        "answer",
        "skip",
        "pause",
        "resume",
        "stop",
        "confirm",
        "correct",
        "review_correction",
        "review_seen",
        "set_retrospective_preference",
    ]
    text: str = Field(default="", max_length=20000)
    target: str | None = Field(default=None, max_length=100)
    retrospective_questions_welcome: bool | None = None


class Import(Body):
    source_type: Literal[
        "edited_response_record", "raw_transcript", "prior_json", "answer_only_notes"
    ] = "edited_response_record"
    source_mode: Literal["railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"] = (
        "unknown"
    )
    record: dict | None = None
    record_text: str | None = Field(default=None, max_length=1_500_000)

    def parsed_record(self):
        if self.record is not None and self.record_text is not None:
            raise ValueError("Provide one source record representation, not two.")
        return strict_json(self.record_text) if self.record_text is not None else self.record


class ProviderRecovery(Body):
    billing_issue_resolved: Literal[True]


class GptSubmission(Body):
    research_use_consented: Literal[True]
    primary_record: dict
    cf003_record: dict


class BodyLimit:
    def __init__(self, app, limit=2_000_000):
        self.app, self.limit = app, limit

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        messages, size = [], 0
        while True:
            message = await receive()
            messages.append(message)
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > self.limit:
                return await JSONResponse({"detail": "Request too large."}, status_code=413)(
                    scope, receive, send
                )
            if not message.get("more_body"):
                break
        position = 0

        async def replay():
            nonlocal position
            if position < len(messages):
                message = messages[position]
                position += 1
                return message
            return await receive()

        await self.app(scope, replay, send)


def create_app(settings: Settings, provider=None, instrument=None) -> FastAPI:
    if min(len(settings.admin_token), len(settings.join_token)) < 32:
        raise RuntimeError("Strong participant access secrets are required.")
    store = Store(settings.database, settings.encryption_key)
    instrument = instrument or load_instrument(settings.authority)
    version = store.pin_instrument(instrument)
    provider = provider or Venice(settings.gateway_url, settings.gateway_token)
    engine = Engine(store, provider, settings.maximum_calls)
    app = FastAPI(
        title="Life Patterns", version=VERSION, docs_url=None, redoc_url=None, openapi_url=None
    )
    app.state.store, app.state.engine = store, engine
    app.add_middleware(BodyLimit)

    def ready():
        if not settings.live_enabled or not provider.configured:
            raise ProviderError("venice_not_activated")

    def token(request):
        value = request.cookies.get("lp_session", "")
        current = store.read(value)
        header_id = request.headers.get("x-life-patterns-session")
        query_id = request.query_params.get("session_id")
        if header_id and query_id and header_id != query_id:
            raise Conflict("Conflicting session identifiers.")
        expected = header_id or query_id
        if request.method not in {"GET", "HEAD"} or request.url.path == "/api/export":
            if not expected:
                raise Conflict(
                    "A session-bound request is required. Reload your private resume link."
                )
        if expected and expected != current["session_id"]:
            raise Conflict(
                "Another session is open in this browser. Reload this tab's private resume link."
            )
        return value

    def admin(request):
        header = request.headers.get("authorization", "")
        value = header[7:] if header.startswith("Bearer ") else ""
        if not secrets.compare_digest(value, settings.admin_token):
            raise HTTPException(401, "Researcher access required.")

    def gpt_submitter(request):
        if not settings.submission_token:
            raise HTTPException(503, "GPT submission is not configured.")
        header = request.headers.get("authorization", "")
        value = header[7:] if header.startswith("Bearer ") else ""
        if not secrets.compare_digest(value, settings.submission_token):
            raise HTTPException(401, "GPT submission access required.")

    def reject_target_fields(record):
        forbidden = {
            "birth_date",
            "birth_time",
            "birthplace",
            "date_of_birth",
            "dob",
            "birth_location",
            "birth_chart",
            "human_design_type",
            "natal_chart",
            "chart",
            "rankings",
            "target_predictions",
        }

        def walk(value):
            if isinstance(value, dict):
                if forbidden.intersection(str(key).lower() for key in value):
                    raise ValueError("Remove birth/chart/ranking fields before submission.")
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(record)

    def validate_gpt_submission(body):
        primary = body.primary_record
        secondary = body.cf003_record
        if primary.get("schema") != "life-patterns-full-survey-participant-export-v2":
            raise ValueError("Primary record schema is not the current Life Patterns export.")
        if (primary.get("consent") or {}).get("research_use_consented") is not True:
            raise ValueError("Research-use consent must be frozen in the primary record.")
        freeze = primary.get("freeze") or {}
        if freeze.get("frozen_before_birth_or_chart_reveal") is not True:
            raise ValueError("Primary record must be frozen before any birth/chart reveal.")
        if not isinstance(primary.get("turns"), list) or not isinstance(secondary.get("turns"), list):
            raise ValueError("Both submitted records need a turns list.")
        required = {"CF003-ID-01", "CF003-CENTRAL-01", "CF003-PERIPH-01"}
        present = {
            turn.get("question_id") or turn.get("canonical_question_id")
            for turn in secondary["turns"]
            if isinstance(turn, dict) and turn.get("turn_role", "behavioral") == "behavioral"
        }
        if not required.issubset(present):
            raise ValueError("CF-003 record must contain all three required behavioral questions.")
        reject_target_fields(primary)
        reject_target_fields(secondary)
        primary_sha256 = digest(canonical(primary))
        declared = secondary.get("primary_record_sha256")
        if declared not in {None, primary_sha256}:
            raise ValueError("CF-003 primary_record_sha256 does not match the submitted primary record.")
        linked_secondary = dict(secondary)
        linked_secondary["primary_record_sha256"] = primary_sha256
        return primary, linked_secondary, primary_sha256

    def public(state):
        return {
            "session_id": state["session_id"],
            "revision": state["revision"],
            "phase": state["phase"],
            "server_time": utc(),
            "error_code": state.get("error"),
            "error": "The AI service needs API credit. Your saved answers are safe; the study organizer must resolve this before retrying."
            if state.get("error") == PAYMENT_ERROR
            else state["error"],
            "provider_issue": {
                "code": "payment_required",
                "http_status": 402,
                "title": "Interview paused — AI service needs credit",
                "detail": "Venice returned a payment-required response. This is a study service issue, not a problem with your answers. Please return after the organizer checks the API balance. Retrying now will not help.",
                "automatic_retry": False,
                "requires_organizer": True,
            }
            if state.get("error") == PAYMENT_ERROR
            else None,
            "question": {k: state["pending_question"].get(k) for k in ("text", "question_id")}
            if state["pending_question"]
            else None,
            "review": state["review"],
            "collection_preferences": state.get("collection_preferences", {}),
            "processing": state.get("processing") if state["phase"] == "planning" else None,
            "turns": [
                {
                    k: t.get(k)
                    for k in (
                        "turn_id",
                        "question_text",
                        "answer_text",
                        "turn_source",
                        "correction_of",
                    )
                }
                for t in state["turns"]
            ],
            "evidence": state["evidence"]
            if state["phase"] in {"review", "complete", "stopped"}
            else [],
            "processed_turn_count": len(state["dispositions"]),
            "ready": settings.live_enabled and provider.configured,
        }

    def with_cookie(state, value, disclose=False):
        response = JSONResponse(public(state) | ({"resume_token": value} if disclose else {}))
        response.set_cookie(
            "lp_session",
            value,
            secure=settings.secure_cookies,
            httponly=True,
            samesite="strict",
            max_age=180 * 24 * 3600,
            path="/",
        )
        return response

    @app.middleware("http")
    async def privacy_headers(request, call_next):
        origin = request.headers.get("origin")
        if (
            request.method not in {"GET", "HEAD"}
            and request.url.path != "/api/gpt/submissions"
            and origin
            and origin.rstrip("/") != (settings.public_origin or str(request.base_url).rstrip("/"))
        ):
            return JSONResponse({"detail": "Cross-origin writes are not allowed."}, status_code=403)
        response = await call_next(request)
        response.headers.update(
            {
                "Cache-Control": "no-store",
                "Referrer-Policy": "no-referrer",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            }
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return JSONResponse(
            {"detail": "Invalid fields. Your saved record has not been replaced."}, status_code=422
        )

    @app.exception_handler(Conflict)
    async def conflict_error(request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=409)

    @app.exception_handler(Missing)
    async def missing_error(request, exc):
        return JSONResponse({"detail": "Session access required."}, status_code=401)

    @app.exception_handler(ProviderError)
    async def provider_error(request, exc):
        return JSONResponse(
            {
                "detail": "Venice is unavailable or not activated. Saved answers remain available.",
                "code": str(exc),
            },
            status_code=503,
        )

    @app.exception_handler(ValueError)
    async def value_error(request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=422)

    @app.get("/healthz")
    def health():
        return {
            "status": "ok",
            "version": VERSION,
            "provider": "venice",
            "provider_configured": provider.configured,
            "participant_enabled": settings.live_enabled,
            "gpt_submission_enabled": bool(settings.submission_token),
            "persistence": "encrypted_sqlite",
            "instrument_version": version,
        }

    @app.get("/")
    def home():
        return FileResponse(STATIC / "index.html")

    @app.get("/admin")
    def admin_home():
        return FileResponse(STATIC / "admin.html")

    @app.get("/privacy")
    def privacy():
        return FileResponse(STATIC / "privacy.html")

    @app.get("/action-openapi.yaml")
    def action_openapi():
        return FileResponse(STATIC / "action-openapi.yaml", media_type="application/yaml")

    @app.get("/assets/{name}")
    def assets(name: str):
        if name not in {"app.js", "style.css", "admin.js"}:
            raise HTTPException(404)
        return FileResponse(STATIC / name)

    @app.post("/api/join")
    def join(body: Access):
        if not secrets.compare_digest(body.token, settings.join_token):
            raise HTTPException(401, "Study invitation required.")
        ready()
        value, state = store.create(
            new_state(version, settings.model, settings.effort), settings.maximum_sessions
        )
        return with_cookie(state, value, True)

    @app.post("/api/resume")
    def resume(body: Access):
        return with_cookie(store.read(body.token), body.token)

    @app.get("/api/session")
    def session(request: Request):
        value = token(request)
        return public(engine.recover_interrupted(value))

    @app.post("/api/operations")
    def operation(request: Request, body: Operation):
        value = token(request)
        if body.action == "consent":
            ready()
        if body.action == "review_seen":

            def mark(s):
                if body.operation_id in s["operations"]:
                    return
                Engine._revision(s, body.revision)
                if s["phase"] != "review":
                    raise Conflict("No review is being shown.")
                s["review"].update(summary_shown=True, shown_at=utc())
                s["operations"][body.operation_id] = {"action": "review_seen", "at": utc()}

            return public(store.change(value, mark))
        return public(
            engine.command(
                value,
                body.revision,
                body.operation_id,
                body.action,
                body.text,
                body.target,
                body.retrospective_questions_welcome,
            )
        )

    @app.post("/api/next")
    def next_question(request: Request):
        ready()
        return public(engine.launch_advance(token(request)))

    def download_response(state):
        if state["consent"] is not True:
            raise HTTPException(403, "Research consent is not recorded.")
        text = state["final_export"] or canonical(
            export_record(state, store.instrument(state["instrument_version"]))
        )
        return Response(
            text,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="life-patterns-participant-export.json"'
            },
        )

    @app.get("/api/export")
    def download(request: Request):
        return download_response(store.read(token(request)))

    @app.post("/api/import")
    def participant_import(request: Request, body: Import):
        value = token(request)
        record = body.parsed_record()
        if record is None:
            raise ValueError("Select a source record.")

        def apply(s):
            import_record(
                s,
                record,
                body.source_type,
                store.instrument(s["instrument_version"]),
                body.source_mode,
            )

        return public(store.change(value, apply))

    @app.post("/api/gpt/submissions")
    def gpt_submission(request: Request, body: GptSubmission):
        gpt_submitter(request)
        primary, secondary, primary_sha256 = validate_gpt_submission(body)
        cf003_sha256 = digest(canonical(secondary))
        submission_sha256 = digest(
            canonical({"primary_record": primary, "cf003_record": secondary})
        )
        payload = {
            "schema": "life-patterns-gpt-submission-v1",
            "received_at_utc": utc(),
            "submission_sha256": submission_sha256,
            "primary_record_sha256": primary_sha256,
            "cf003_record_sha256": cf003_sha256,
            "primary_record": primary,
            "cf003_record": secondary,
        }
        submission_id, stored, duplicate = store.create_gpt_submission(
            payload, submission_sha256
        )
        return {
            "schema": "life-patterns-gpt-submission-receipt-v1",
            "submission_id": submission_id,
            "received_at_utc": stored["received_at_utc"],
            "duplicate": duplicate,
            "primary_record_sha256": stored["primary_record_sha256"],
            "cf003_record_sha256": stored["cf003_record_sha256"],
            "stored_encrypted": True,
            "inference_started": False,
        }

    @app.get("/api/admin/sessions")
    def sessions(request: Request):
        admin(request)
        return {"sessions": store.overview()}

    @app.get("/api/admin/gpt-submissions")
    def gpt_submissions(request: Request):
        admin(request)
        return {"submissions": store.gpt_submission_overview()}

    @app.get("/api/admin/gpt-submissions/{submission_id}/primary")
    def gpt_submission_primary(request: Request, submission_id: str):
        admin(request)
        payload = store.gpt_submission_read(submission_id)
        return Response(
            canonical(payload["primary_record"]),
            media_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="life-patterns-participant-export.json"'},
        )

    @app.get("/api/admin/gpt-submissions/{submission_id}/cf003")
    def gpt_submission_cf003(request: Request, submission_id: str):
        admin(request)
        payload = store.gpt_submission_read(submission_id)
        return Response(
            canonical(payload["cf003_record"]),
            media_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="life-patterns-cf003-secondary-v0.json"'},
        )

    @app.post("/api/admin/invitations")
    def invitation(request: Request, body: Import):
        admin(request)
        state = new_state(version, settings.model, settings.effort)
        record = body.parsed_record()
        if record is not None:
            import_record(state, record, body.source_type, instrument, body.source_mode)
        value, state = store.create(state, settings.maximum_sessions)
        return {
            "session_id": state["session_id"],
            "resume_path": "/#resume=" + value,
            "turn_count": len(state["turns"]),
            "consent_required": True,
        }

    @app.post("/api/admin/sessions/{session_id}/resume-provider")
    def resume_provider(request: Request, session_id: str, body: ProviderRecovery):
        admin(request)

        def unblock(state):
            if state.get("error") != PAYMENT_ERROR or state["phase"] not in {
                "error",
                "provider_blocked",
            }:
                raise Conflict("This session is not blocked by the provider payment response.")
            state.setdefault("provider_recovery", []).append(
                {"at": utc(), "action": "organizer_acknowledged_billing_repair"}
            )
            state["phase"], state["error"], state["stop_reason"] = "ready", None, None
            state["processing"], state["lease"] = None, None
            state["generation"] += 1

        changed = store.admin_change(session_id, unblock)
        return {"session_id": session_id, "phase": changed["phase"], "inference_started": False}

    @app.get("/api/admin/exports/{session_id}")
    def researcher_export(request: Request, session_id: str):
        admin(request)
        return download_response(store.admin_read(session_id))

    return app


def factory():
    app = create_app(Settings.from_env())
    if not isinstance(app.state.engine.provider, Venice):
        raise RuntimeError("Production participant inference must use the Venice provider.")
    return app
