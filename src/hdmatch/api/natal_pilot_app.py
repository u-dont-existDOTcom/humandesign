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
from typing import Annotated, Any, Literal, TypeVar
from urllib.parse import urlsplit

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import Field

from hdmatch.api.errors import ERROR_RESPONSES, install_error_handlers
from hdmatch.api.natal_pilot_ui import render_natal_pilot_html, render_natal_result_html
from hdmatch.api.participant import _execute, register_participant_routes
from hdmatch.participant import ParticipantSessionService, ParticipantSessionStore
from hdmatch.participant.century_backend import CenturyCapableParticipantBackend
from hdmatch.participant.models import (
    BirthIntake,
    EvidenceInput,
    ExploratoryRankingReport,
    FinalParticipantReport,
    NextInterviewQuestion,
    ParticipantModel,
    ParticipantModelReceipt,
    PredictionComparison,
    PublicConfirmatoryLock,
    PublicEvidenceRecord,
    PublicProgress,
    RankingSnapshot,
    RankScope,
    ResearchLayer,
    RevealReport,
    SessionMode,
    SessionRecord,
)
from hdmatch.relationship.place_resolution import search_birthplaces

T = TypeVar("T")
_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
_SOURCE_COMMIT_RE = re.compile(r"^[a-f0-9]{40,64}$")
_SESSION_ID_RE = re.compile(r"^HD-[A-F0-9]{32}$")


class NatalPilotSessionCreated(SessionRecord):
    session_token: str


class InterviewerSessionAccess(ParticipantModel):
    """Per-session bearer capability carried in an Action request body, never a URL."""

    session_id: str = Field(pattern=r"^HD-[A-F0-9]{32}$")
    session_token: str = Field(min_length=32)


class InterviewerEvidenceAccess(InterviewerSessionAccess):
    evidence: EvidenceInput


class InterviewerRevealReport(ParticipantModel):
    """Chart- and birth-redacted reveal safe for the external interviewer."""

    schema_version: str = "participant-interviewer-reveal-v1"
    protocol_status: Literal["policy_bound_conforming", "historical_diagnostic"]
    session_id: str
    revealed_at_utc: datetime
    confirmatory_ranking: RankingSnapshot
    prediction_comparisons: tuple[PredictionComparison, ...]
    model_receipt: ParticipantModelReceipt
    primary_test_statement: str
    trusted_result_url: str
    interviewer_model_receipt: str
    interviewer_instructions_sha256: str
    interviewer_action_schema_sha256: str


class InterviewerFinalReport(ParticipantModel):
    """Final report with the sensitive birth and raw chart retained server-side."""

    schema_version: str = "participant-interviewer-final-report-v1"
    session_id: str
    mode: SessionMode
    confirmatory: InterviewerRevealReport
    exploratory: ExploratoryRankingReport
    retained_secondary_evidence: tuple[PublicEvidenceRecord, ...]
    research_layers: tuple[ResearchLayer, ...]


@dataclass(frozen=True, slots=True)
class NatalPilotConfig:
    invite_token_sha256: str
    invite_state_root: Path
    health_probe_root: Path
    public_base_url: str
    interviewer_url: str | None
    interviewer_model_receipt: str | None
    action_schema_template: str
    runtime_receipt: dict[str, str | int | bool]

    def __post_init__(self) -> None:
        if not _SHA256_RE.fullmatch(self.invite_token_sha256):
            raise ValueError("natal pilot invite token must be supplied as a SHA-256 digest")
        public = urlsplit(self.public_base_url)
        if not (
            public.scheme == "https"
            or (public.scheme == "http" and public.hostname in {"localhost", "127.0.0.1"})
        ):
            raise ValueError("HDMATCH_PUBLIC_BASE_URL must be HTTPS outside localhost")
        if (self.interviewer_url is None) != (self.interviewer_model_receipt is None):
            raise ValueError("interviewer URL and model receipt must be configured together")
        if self.interviewer_url is not None:
            parsed = urlsplit(self.interviewer_url)
            if (
                parsed.scheme != "https"
                or parsed.hostname != "chatgpt.com"
                or parsed.username is not None
                or parsed.password is not None
                or parsed.port is not None
                or not parsed.path.startswith("/g/")
            ):
                raise ValueError("interviewer URL must be an HTTPS chatgpt.com Custom GPT link")


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
        openai_consent: bool,
    ) -> T:
        supplied_sha256 = hashlib.sha256((supplied_token or "").encode()).hexdigest()
        if not secrets.compare_digest(self.expected_sha256, supplied_sha256):
            raise HTTPException(status_code=403, detail="invalid or unavailable pilot access code")
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)
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
                "consent_to_openai_redacted_interview_processing": openai_consent,
            }
            session_id = getattr(result, "session_id", None)
            if isinstance(session_id, str):
                receipt["session_id"] = session_id
            session_token = getattr(result, "session_token", None)
            if isinstance(session_token, str) and session_token:
                receipt["session_token_sha256"] = hashlib.sha256(session_token.encode()).hexdigest()
            if isinstance(session_id, str) and isinstance(session_token, str) and session_token:
                self._write_session_access(
                    session_id,
                    hashlib.sha256(session_token.encode()).hexdigest(),
                )
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

    def authorize_session(self, session_id: str, supplied_token: str | None) -> None:
        """Require the separate session bearer secret without storing it in plaintext."""

        if not _SESSION_ID_RE.fullmatch(session_id):
            raise HTTPException(status_code=403, detail="invalid session access")
        expected_token_sha256 = self._session_token_sha256(session_id)
        observed = hashlib.sha256((supplied_token or "").encode()).hexdigest()
        if expected_token_sha256 is None or not secrets.compare_digest(
            expected_token_sha256,
            observed,
        ):
            raise HTTPException(status_code=403, detail="invalid session access")

    def _session_token_sha256(self, session_id: str) -> str | None:
        access_path = self.root / "session-access" / f"{session_id}.json"
        try:
            receipt = json.loads(access_path.read_text(encoding="utf-8"))
            if (
                isinstance(receipt, dict)
                and receipt.get("session_id") == session_id
                and _SHA256_RE.fullmatch(str(receipt.get("session_token_sha256", "")))
            ):
                return str(receipt["session_token_sha256"])
        except (OSError, TypeError, ValueError):
            pass

        # Compatibility for the already-deployed one-receipt owner session. A later
        # invite rotation must not strand that session merely because its invitation
        # hash is no longer the process's active creation gate.
        try:
            claim_paths = tuple(self.root.glob("*.json"))
        except OSError:
            return None
        for claim_path in claim_paths:
            try:
                receipt = json.loads(claim_path.read_text(encoding="utf-8"))
                if not isinstance(receipt, dict):
                    continue
                token_sha256 = str(receipt.get("session_token_sha256", ""))
            except (OSError, TypeError, ValueError):
                continue
            if receipt.get("session_id") != session_id or not _SHA256_RE.fullmatch(token_sha256):
                continue
            self._write_session_access(session_id, token_sha256)
            return token_sha256
        return None

    def _write_session_access(self, session_id: str, token_sha256: str) -> None:
        access_root = self.root / "session-access"
        access_root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(access_root, 0o700)
        target = access_root / f"{session_id}.json"
        temporary = access_root / f".{session_id}.{secrets.token_hex(8)}.tmp"
        temporary.write_text(
            json.dumps(
                {
                    "session_id": session_id,
                    "session_token_sha256": token_sha256,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        os.chmod(temporary, 0o600)
        temporary.replace(target)


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
    invite = SingleUsePilotInvite(config.invite_token_sha256, config.invite_state_root)
    register_participant_routes(
        app,
        sessions,
        include_session_creation=False,
        include_result_routes=False,
        authorize_session=invite.authorize_session,
    )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def home() -> str:
        return render_natal_pilot_html(config.interviewer_url)

    @app.get("/result", response_class=HTMLResponse, include_in_schema=False)
    async def trusted_result_page() -> str:
        return render_natal_result_html()

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
        response_model=NatalPilotSessionCreated,
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
        openai_consent: Annotated[
            str | None,
            Header(alias="X-AstroHD-OpenAI-Consent"),
        ] = None,
    ) -> NatalPilotSessionCreated:
        if request.mode is not SessionMode.SCIENTIFIC_BLIND:
            raise HTTPException(status_code=400, detail="owner pilot requires scientific_blind")
        if request.ranking_scope is not RankScope.KNOWN_BIRTH_MONTH:
            raise HTTPException(status_code=400, detail="owner pilot requires known_birth_month")
        if storage_consent != "yes":
            raise HTTPException(status_code=400, detail="private-storage consent is required")
        if openai_consent != "yes":
            raise HTTPException(status_code=400, detail="OpenAI interview consent is required")
        session_token = secrets.token_urlsafe(32)

        def create() -> NatalPilotSessionCreated:
            record = _execute(lambda: sessions.create_session(request))
            return NatalPilotSessionCreated(
                **record.model_dump(mode="python"),
                session_token=session_token,
            )

        return invite.consume(
            pilot_token,
            create,
            development_consent=development_consent == "yes",
            openai_consent=True,
        )

    @app.post(
        "/v1/interviewer/progress",
        response_model=PublicProgress,
        responses=ERROR_RESPONSES,
        operation_id="getParticipantProgress",
    )
    async def progress_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> PublicProgress:
        invite.authorize_session(request.session_id, request.session_token)
        return _execute(lambda: sessions.public_progress(request.session_id))

    @app.post(
        "/v1/interviewer/next-question",
        response_model=NextInterviewQuestion,
        responses=ERROR_RESPONSES,
        operation_id="getParticipantNextQuestion",
    )
    async def next_question_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> NextInterviewQuestion:
        invite.authorize_session(request.session_id, request.session_token)
        return _execute(lambda: sessions.next_question(request.session_id))

    @app.post(
        "/v1/interviewer/evidence",
        response_model=PublicEvidenceRecord,
        responses=ERROR_RESPONSES,
        operation_id="appendParticipantEvidence",
    )
    async def evidence_for_interviewer(
        request: InterviewerEvidenceAccess,
    ) -> PublicEvidenceRecord:
        invite.authorize_session(request.session_id, request.session_token)
        record = _execute(lambda: sessions.append_evidence(request.session_id, request.evidence))
        return record.public_view()

    @app.post(
        "/v1/interviewer/lock",
        response_model=PublicConfirmatoryLock,
        responses=ERROR_RESPONSES,
        operation_id="lockParticipantConfirmatoryEvidence",
    )
    async def lock_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> PublicConfirmatoryLock:
        invite.authorize_session(request.session_id, request.session_token)
        lock = _execute(lambda: sessions.lock_confirmatory(request.session_id))
        return lock.public_view()

    @app.post(
        "/v1/interviewer/reveal",
        response_model=InterviewerRevealReport,
        responses=ERROR_RESPONSES,
        operation_id="revealParticipantResult",
    )
    async def reveal_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> InterviewerRevealReport:
        invite.authorize_session(request.session_id, request.session_token)
        report = _execute(lambda: sessions.reveal(request.session_id))
        return _interviewer_reveal(report, config, protocol_status="policy_bound_conforming")

    @app.post(
        "/v1/interviewer/diagnostic-reveal",
        response_model=InterviewerRevealReport,
        responses=ERROR_RESPONSES,
        operation_id="getHistoricalDiagnosticReveal",
    )
    async def diagnostic_reveal_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> InterviewerRevealReport:
        invite.authorize_session(request.session_id, request.session_token)
        report = _execute(lambda: sessions.load_historical_diagnostic_reveal(request.session_id))
        return _interviewer_reveal(report, config, protocol_status="historical_diagnostic")

    @app.post(
        "/v1/interviewer/finalize-exploratory",
        response_model=InterviewerFinalReport,
        responses=ERROR_RESPONSES,
        operation_id="finalizeParticipantExploratoryProfile",
    )
    async def finalize_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> InterviewerFinalReport:
        invite.authorize_session(request.session_id, request.session_token)
        report = _execute(lambda: sessions.finalize_exploratory(request.session_id))
        return _interviewer_final(report, config)

    @app.post(
        "/v1/interviewer/final-report",
        response_model=InterviewerFinalReport,
        responses=ERROR_RESPONSES,
        operation_id="getParticipantFinalReport",
    )
    async def final_report_for_interviewer(
        request: InterviewerSessionAccess,
    ) -> InterviewerFinalReport:
        invite.authorize_session(request.session_id, request.session_token)
        report = sessions.store.load_final_report(request.session_id)
        if report is None:
            raise HTTPException(status_code=409, detail="exploratory profile is not finalized")
        return _interviewer_final(report, config)

    @app.post(
        "/trusted/v1/participant-sessions/{session_id}/reveal",
        response_model=RevealReport,
        responses=ERROR_RESPONSES,
        include_in_schema=False,
    )
    async def trusted_sensitive_reveal(
        session_id: str,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> RevealReport:
        invite.authorize_session(session_id, session_token)
        return _execute(lambda: sessions.reveal(session_id))

    @app.post(
        "/trusted/v1/participant-sessions/{session_id}/diagnostic-reveal",
        response_model=RevealReport,
        responses=ERROR_RESPONSES,
        include_in_schema=False,
    )
    async def trusted_historical_diagnostic_reveal(
        session_id: str,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> RevealReport:
        invite.authorize_session(session_id, session_token)
        return _execute(lambda: sessions.load_historical_diagnostic_reveal(session_id))

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


def _interviewer_reveal(
    report: RevealReport,
    config: NatalPilotConfig,
    *,
    protocol_status: Literal[
        "policy_bound_conforming", "historical_diagnostic"
    ] = "historical_diagnostic",
) -> InterviewerRevealReport:
    if report.model_receipt is None:
        raise RuntimeError("legacy reveal has no model receipt for interviewer display")
    return InterviewerRevealReport(
        session_id=report.session_id,
        protocol_status=protocol_status,
        revealed_at_utc=report.revealed_at_utc,
        confirmatory_ranking=report.confirmatory_ranking,
        prediction_comparisons=report.prediction_comparisons,
        model_receipt=report.model_receipt,
        primary_test_statement=report.primary_test_statement,
        trusted_result_url=config.public_base_url.rstrip("/") + "/astrohd/result",
        interviewer_model_receipt=config.interviewer_model_receipt or "not_configured",
        interviewer_instructions_sha256=str(
            config.runtime_receipt.get("interviewer_instructions_sha256", "not_configured")
        ),
        interviewer_action_schema_sha256=str(
            config.runtime_receipt.get("interviewer_action_schema_sha256", "not_configured")
        ),
    )


def _interviewer_final(
    report: FinalParticipantReport,
    config: NatalPilotConfig,
) -> InterviewerFinalReport:
    return InterviewerFinalReport(
        session_id=report.session_id,
        mode=report.mode,
        confirmatory=_interviewer_reveal(
            report.confirmatory,
            config,
            protocol_status="historical_diagnostic",
        ),
        exploratory=report.exploratory,
        retained_secondary_evidence=tuple(
            record.public_view() for record in report.retained_secondary_evidence
        ),
        research_layers=report.research_layers,
    )


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
    code_commit = (
        os.environ.get("RAILWAY_GIT_COMMIT_SHA") or os.environ.get("HDMATCH_CODE_COMMIT") or ""
    ).strip()
    if not _SOURCE_COMMIT_RE.fullmatch(code_commit):
        raise RuntimeError("an exact deployed source commit is required for the natal pilot")
    interviewer_url = os.environ.get("HDMATCH_NATAL_INTERVIEWER_URL") or None
    interviewer_model_receipt = (
        _required_env("HDMATCH_NATAL_INTERVIEWER_MODEL_RECEIPT")
        if interviewer_url is not None
        else None
    )

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
            interviewer_url=interviewer_url,
            interviewer_model_receipt=interviewer_model_receipt,
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
                "interviewer_model_receipt": interviewer_model_receipt or "not_configured",
                "interviewer_instructions_sha256": hashlib.sha256(
                    (
                        repo_root / "reference/custom_gpt/"
                        "participant_interviewer_instructions_under_8000_v1.md"
                    ).read_bytes()
                ).hexdigest(),
                "interviewer_action_schema_sha256": hashlib.sha256(
                    schema_template.encode()
                ).hexdigest(),
            },
        ),
    )


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required environment variable is missing: {name}")
    return value


def _verify_private_storage(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
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
