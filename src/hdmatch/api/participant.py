"""FastAPI routes for participant interview sessions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, TypeVar

from fastapi import FastAPI, Header

from hdmatch.api.errors import ERROR_RESPONSES, ApiProblem
from hdmatch.chart.timezone import TimezoneResolutionError
from hdmatch.participant.backend import FrozenRuntimeMismatchError, UnsupportedRankScopeError
from hdmatch.participant.models import (
    BirthIntake,
    ConfirmatoryLock,
    EvidenceInput,
    EvidenceRecord,
    FinalParticipantReport,
    NextInterviewQuestion,
    PublicProgress,
    RevealReport,
    SessionRecord,
)
from hdmatch.participant.service import ParticipantSessionService, ParticipantStateError
from hdmatch.participant.store import SessionStorageError

T = TypeVar("T")


def _execute(operation: Callable[[], T]) -> T:
    try:
        return operation()
    except SessionStorageError as exc:
        raise ApiProblem(404, "PARTICIPANT_SESSION_NOT_FOUND", str(exc)) from exc
    except ParticipantStateError as exc:
        raise ApiProblem(409, "PARTICIPANT_PHASE_CONFLICT", str(exc)) from exc
    except UnsupportedRankScopeError as exc:
        raise ApiProblem(501, "PARTICIPANT_RANK_SCOPE_UNAVAILABLE", str(exc)) from exc
    except FrozenRuntimeMismatchError as exc:
        raise ApiProblem(503, "PARTICIPANT_FROZEN_RUNTIME_UNAVAILABLE", str(exc)) from exc
    except TimezoneResolutionError as exc:
        raise ApiProblem(400, "BIRTH_TIME_RESOLUTION_FAILED", str(exc)) from exc
    except ValueError as exc:
        raise ApiProblem(400, "INVALID_PARTICIPANT_REQUEST", str(exc)) from exc


def register_participant_routes(
    service: FastAPI,
    sessions: ParticipantSessionService,
    *,
    include_session_creation: bool = True,
    include_result_routes: bool = True,
    authorize_session: Callable[[str, str | None], None] | None = None,
) -> None:
    """Register only participant-safe orchestration routes."""

    if include_session_creation:

        @service.post(
            "/v1/participant-sessions",
            response_model=SessionRecord,
            responses=ERROR_RESPONSES,
            operation_id="createParticipantSession",
        )
        async def create_participant_session(request: BirthIntake) -> SessionRecord:
            return _execute(lambda: sessions.create_session(request))

    def require_access(session_id: str, session_token: str | None) -> None:
        if authorize_session is not None:
            authorize_session(session_id, session_token)

    @service.get(
        "/v1/participant-sessions/{session_id}/progress",
        response_model=PublicProgress,
        responses=ERROR_RESPONSES,
        operation_id="getParticipantProgress",
    )
    async def participant_progress(
        session_id: str,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> PublicProgress:
        require_access(session_id, session_token)
        return _execute(lambda: sessions.public_progress(session_id))

    @service.get(
        "/v1/participant-sessions/{session_id}/next-question",
        response_model=NextInterviewQuestion,
        responses=ERROR_RESPONSES,
        operation_id="getParticipantNextQuestion",
    )
    async def participant_next_question(
        session_id: str,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> NextInterviewQuestion:
        require_access(session_id, session_token)
        return _execute(lambda: sessions.next_question(session_id))

    @service.post(
        "/v1/participant-sessions/{session_id}/evidence",
        response_model=EvidenceRecord,
        responses=ERROR_RESPONSES,
        operation_id="appendParticipantEvidence",
    )
    async def append_participant_evidence(
        session_id: str,
        request: EvidenceInput,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> EvidenceRecord:
        require_access(session_id, session_token)
        return _execute(lambda: sessions.append_evidence(session_id, request))

    @service.post(
        "/v1/participant-sessions/{session_id}/lock",
        response_model=ConfirmatoryLock,
        responses=ERROR_RESPONSES,
        operation_id="lockParticipantConfirmatoryEvidence",
    )
    async def lock_participant_evidence(
        session_id: str,
        session_token: Annotated[
            str | None,
            Header(alias="X-AstroHD-Session-Token"),
        ] = None,
    ) -> ConfirmatoryLock:
        require_access(session_id, session_token)
        return _execute(lambda: sessions.lock_confirmatory(session_id))

    if include_result_routes:

        @service.post(
            "/v1/participant-sessions/{session_id}/reveal",
            response_model=RevealReport,
            responses=ERROR_RESPONSES,
            operation_id="revealParticipantResult",
        )
        async def reveal_participant_result(
            session_id: str,
            session_token: Annotated[
                str | None,
                Header(alias="X-AstroHD-Session-Token"),
            ] = None,
        ) -> RevealReport:
            require_access(session_id, session_token)
            return _execute(lambda: sessions.reveal(session_id))

        @service.post(
            "/v1/participant-sessions/{session_id}/finalize-exploratory",
            response_model=FinalParticipantReport,
            responses=ERROR_RESPONSES,
            operation_id="finalizeParticipantExploratoryProfile",
        )
        async def finalize_participant_exploratory(
            session_id: str,
            session_token: Annotated[
                str | None,
                Header(alias="X-AstroHD-Session-Token"),
            ] = None,
        ) -> FinalParticipantReport:
            require_access(session_id, session_token)
            return _execute(lambda: sessions.finalize_exploratory(session_id))

        @service.get(
            "/v1/participant-sessions/{session_id}/final-report",
            response_model=FinalParticipantReport,
            responses=ERROR_RESPONSES,
            operation_id="getParticipantFinalReport",
        )
        async def participant_final_report(
            session_id: str,
            session_token: Annotated[
                str | None,
                Header(alias="X-AstroHD-Session-Token"),
            ] = None,
        ) -> FinalParticipantReport:
            require_access(session_id, session_token)

            def load() -> FinalParticipantReport:
                report = sessions.store.load_final_report(session_id)
                if report is None:
                    raise ParticipantStateError("exploratory profile has not been finalized")
                return report

            return _execute(load)
