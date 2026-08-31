"""Owner-only launch surface for the existing blind natal participant protocol."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, TypeVar

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse

from hdmatch.api.errors import ERROR_RESPONSES, install_error_handlers
from hdmatch.api.natal_pilot_ui import render_natal_pilot_html
from hdmatch.api.participant import _execute, register_participant_routes
from hdmatch.participant import ParticipantSessionService, ParticipantSessionStore
from hdmatch.participant.century_backend import CenturyCapableParticipantBackend
from hdmatch.participant.models import BirthIntake, SessionRecord
from hdmatch.relationship.place_resolution import search_birthplaces

T = TypeVar("T")
_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True, slots=True)
class NatalPilotConfig:
    invite_token_sha256: str
    invite_state_root: Path
    health_probe_root: Path
    public_base_url: str
    interviewer_url: str | None
    action_schema_template: str
    runtime_receipt: dict[str, str | int | bool]

    def __post_init__(self) -> None:
        if not _SHA256_RE.fullmatch(self.invite_token_sha256):
            raise ValueError("natal pilot invite token must be supplied as a SHA-256 digest")
        if not self.public_base_url.startswith(("https://", "http://localhost")):
            raise ValueError("HDMATCH_PUBLIC_BASE_URL must be HTTPS outside localhost")


class SingleUsePilotInvite:
    """Consume one hashed owner invitation without persisting the raw token."""

    def __init__(self, expected_sha256: str, root: Path) -> None:
        self.expected_sha256 = expected_sha256
        self.root = root

    def consume(
        self,
        supplied_token: str | None,
        operation: Callable[[], T],
        *,
        development_consent: bool,
    ) -> T:
        supplied_sha256 = hashlib.sha256((supplied_token or "").encode()).hexdigest()
        if not secrets.compare_digest(self.expected_sha256, supplied_sha256):
            raise HTTPException(status_code=403, detail="invalid or unavailable pilot access code")
        self.root.mkdir(parents=True, exist_ok=True)
        claim_path = self.root / f"{self.expected_sha256}.json"
        try:
            descriptor = os.open(
                claim_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
        except FileExistsError as exc:
            raise HTTPException(
                status_code=410,
                detail="this single-use pilot access code has already created a session",
            ) from exc
        created = False
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(
                    {"status": "reserved", "reserved_at_utc": datetime.now(UTC).isoformat()},
                    handle,
                    sort_keys=True,
                )
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            result = operation()
            created = True
            receipt = {
                "status": "consumed",
                "consumed_at_utc": datetime.now(UTC).isoformat(),
                "consent_to_private_research_storage": True,
                "consent_to_future_deidentified_model_development": development_consent,
            }
            session_id = getattr(result, "session_id", None)
            if isinstance(session_id, str):
                receipt["session_id"] = session_id
            temporary = claim_path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(receipt, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            os.chmod(temporary, 0o600)
            temporary.replace(claim_path)
            return result
        except BaseException:
            if not created:
                claim_path.unlink(missing_ok=True)
            raise


def create_natal_pilot_app(
    *,
    sessions: ParticipantSessionService,
    config: NatalPilotConfig,
) -> FastAPI:
    """Build the isolated natal pilot without exposing trusted birth intake to GPT."""

    app = FastAPI(
        title="AstroHD owner pilot",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    install_error_handlers(app)
    register_participant_routes(app, sessions, include_session_creation=False)
    invite = SingleUsePilotInvite(config.invite_token_sha256, config.invite_state_root)

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def home() -> str:
        return render_natal_pilot_html(config.interviewer_url)

    @app.get("/places", include_in_schema=False)
    async def search_places(q: str) -> dict[str, Any]:
        try:
            candidates = search_birthplaces(q)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except (OSError, RuntimeError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Birthplace search is temporarily unavailable; no intake was saved.",
            ) from exc
        return {
            "query": q,
            "candidates": [candidate.public_dict() for candidate in candidates],
        }

    @app.post(
        "/v1/participant-sessions",
        response_model=SessionRecord,
        responses=ERROR_RESPONSES,
        include_in_schema=False,
    )
    async def create_owner_pilot_session(
        request: BirthIntake,
        pilot_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Pilot-Token"),
        ] = None,
        storage_consent: Annotated[
            str | None,
            Header(alias="X-AstroHD-Storage-Consent"),
        ] = None,
        development_consent: Annotated[
            str | None,
            Header(alias="X-AstroHD-Development-Consent"),
        ] = None,
    ) -> SessionRecord:
        if storage_consent != "yes":
            raise HTTPException(status_code=400, detail="private-storage consent is required")
        return invite.consume(
            pilot_token,
            lambda: _execute(lambda: sessions.create_session(request)),
            development_consent=development_consent == "yes",
        )

    @app.get("/healthz", include_in_schema=False)
    async def healthz() -> dict[str, Any]:
        _verify_private_storage(config.health_probe_root)
        return {
            "status": "ok",
            "scope": "owner_only_exact_time_natal_pilot",
            "predictions_frozen_before_answers": True,
            "automatic_model_updates": False,
            **config.runtime_receipt,
        }

    @app.get(
        "/interviewer-action-openapi.yaml",
        response_class=PlainTextResponse,
        include_in_schema=False,
    )
    async def interviewer_action_openapi() -> str:
        server = config.public_base_url.rstrip("/") + "/astrohd"
        return config.action_schema_template.replace("https://YOUR_API_HOST", server)

    return app


def create_natal_pilot_app_from_env() -> FastAPI:
    """Construct the owner pilot from explicit immutable artifacts and private storage."""

    repo_root = Path(os.environ.get("HDMATCH_REPO_ROOT", "/app"))
    ephemeris_path = _required_env("HDMATCH_EPHEMERIS_PATH")
    mapping_path = os.environ.get(
        "HDMATCH_MAPPING_PATH",
        str(repo_root / "mappings/mapping_library_v1.json"),
    )
    question_bank_path = os.environ.get(
        "HDMATCH_QUESTION_BANK_PATH",
        str(repo_root / "reference/core/question_bank_v1.json"),
    )
    session_store = _required_env("HDMATCH_PARTICIPANT_STORE")
    invite_token_sha256 = _required_env("HDMATCH_NATAL_PILOT_TOKEN_SHA256")
    public_base_url = _required_env("HDMATCH_PUBLIC_BASE_URL")
    candidate_cache = os.environ.get("HDMATCH_CANDIDATE_CACHE") or None
    century_cache = _required_env("HDMATCH_CENTURY_CACHE")
    century_manifest_sha256 = _required_env("HDMATCH_CENTURY_MANIFEST_SHA256")
    century_canonical_rows_sha256 = _required_env("HDMATCH_CENTURY_CANONICAL_ROWS_SHA256")
    code_commit = os.environ.get("HDMATCH_CODE_COMMIT", "unknown")

    backend = CenturyCapableParticipantBackend(
        ephemeris_path=ephemeris_path,
        mapping_path=mapping_path,
        question_bank_path=question_bank_path,
        candidate_cache_dir=candidate_cache,
        century_cache_dir=century_cache,
        century_manifest_sha256=century_manifest_sha256,
        century_canonical_rows_sha256=century_canonical_rows_sha256,
        code_commit=code_commit,
    )
    backend.verify_pinned_month_cache_ready()
    sessions = ParticipantSessionService(
        store=ParticipantSessionStore(session_store),
        backend=backend,
    )
    schema_template = (
        repo_root / "reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml"
    ).read_text(encoding="utf-8")
    return create_natal_pilot_app(
        sessions=sessions,
        config=NatalPilotConfig(
            invite_token_sha256=invite_token_sha256,
            invite_state_root=Path(session_store) / ".pilot-invitations",
            health_probe_root=Path(session_store) / ".health",
            public_base_url=public_base_url,
            interviewer_url=os.environ.get("HDMATCH_NATAL_INTERVIEWER_URL") or None,
            action_schema_template=schema_template,
            runtime_receipt={
                "model_version": backend.model.library.model_version,
                "model_sha256": backend.model.model_sha256,
                "mapping_sha256": backend.model.mapping_sha256,
                "question_bank_version": backend.question_bank.version,
                "question_bank_sha256": backend.model.question_bank_sha256,
                "engine_fingerprint": backend.chart_engine.fingerprint,
                "code_commit": code_commit,
                "ranking_scope": "known_birth_month",
                "month_universe_source": "pinned_verified_century_cache_slice",
                "century_global_enabled": True,
            },
        ),
    )


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required environment variable is missing: {name}")
    return value


def _verify_private_storage(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=root, prefix="probe-", delete=False) as handle:
            path = Path(handle.name)
            handle.write(b"astrohd-private-store-ready\n")
            handle.flush()
            os.fsync(handle.fileno())
        if path.read_bytes() != b"astrohd-private-store-ready\n":
            raise OSError("private storage probe readback differed")
    finally:
        if path is not None:
            path.unlink(missing_ok=True)
