"""Standalone natal-first intake API; never mounted in relationship routes."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import Field

from hdmatch.natal_time.models import (
    DocumentaryVerification,
    EvidenceAssessment,
    EvidenceLineage,
    EvidenceSource,
    NatalTimeModel,
    Weekday,
    WeekdayAnswerStatus,
)
from hdmatch.natal_time.service import NatalTimeIntakeService, WeekdayLockReceipt
from hdmatch.natal_time.store import NatalTimePrivateStore


class NatalTimeIntakeRequest(NatalTimeModel):
    asserted_date: date
    date_source: Literal[EvidenceSource.DOCUMENTARY, EvidenceSource.MEMORY]
    documentary_verification: DocumentaryVerification
    remembered_weekday_status: WeekdayAnswerStatus
    remembered_weekday: Weekday | None = None
    entered_how: str = Field(default="participant_api", min_length=1, max_length=120)


class NatalTimeIntakeResponse(NatalTimeModel):
    schema_version: Literal["natal-time-intake-lock-response-v1"] = (
        "natal-time-intake-lock-response-v1"
    )
    lock: WeekdayLockReceipt


class NatalTimeAssessmentResponse(NatalTimeModel):
    schema_version: Literal["natal-time-assessment-response-v1"] = (
        "natal-time-assessment-response-v1"
    )
    assessment: EvidenceAssessment


class ConfirmCandidateDatesRequest(NatalTimeModel):
    candidate_dates: tuple[date, ...] = Field(min_length=1)
    confirmed_how: str = Field(default="participant_api", min_length=1, max_length=120)


class ConfirmCandidateDatesResponse(NatalTimeModel):
    schema_version: Literal["natal-time-candidate-dates-response-v1"] = (
        "natal-time-candidate-dates-response-v1"
    )
    lineage: EvidenceLineage
    assessment: EvidenceAssessment


def create_natal_time_app(store_root: str | Path) -> FastAPI:
    """Create a non-production natal-time API with its own private namespace."""

    service = NatalTimeIntakeService(NatalTimePrivateStore(store_root))
    app = FastAPI(title="Natal Time Foundation", version="0.1.0")

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "service": "natal-time-foundation"}

    @app.post("/v1/natal-time/intakes", response_model=NatalTimeIntakeResponse)
    async def capture_intake(request: NatalTimeIntakeRequest) -> NatalTimeIntakeResponse:
        try:
            receipt = service.capture_initial_evidence(
                asserted_date=request.asserted_date,
                date_source=request.date_source,
                documentary_verification=request.documentary_verification,
                weekday_answer_status=request.remembered_weekday_status,
                asserted_weekday=request.remembered_weekday,
                entered_how=request.entered_how,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return NatalTimeIntakeResponse(lock=receipt)

    @app.post(
        "/v1/natal-time/intakes/{lineage_id}/assessment",
        response_model=NatalTimeAssessmentResponse,
    )
    async def assess_intake(lineage_id: str) -> NatalTimeAssessmentResponse:
        try:
            assessment = service.assess_locked_evidence(lineage_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return NatalTimeAssessmentResponse(assessment=assessment)

    @app.post(
        "/v1/natal-time/intakes/{lineage_id}/candidate-dates",
        response_model=ConfirmCandidateDatesResponse,
    )
    async def confirm_candidate_dates(
        lineage_id: str,
        request: ConfirmCandidateDatesRequest,
    ) -> ConfirmCandidateDatesResponse:
        try:
            lineage = service.confirm_candidate_dates(
                lineage_id,
                candidate_dates=request.candidate_dates,
                confirmed_how=request.confirmed_how,
            )
            assessment = service.assess_locked_evidence(lineage_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return ConfirmCandidateDatesResponse(lineage=lineage, assessment=assessment)

    return app
