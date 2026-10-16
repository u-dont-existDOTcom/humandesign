"""Ready-only GPT -> one-time Railway browser finishing routes.

The shared GPT bearer is needed only when issuing the link. The participant
page has a completely separate short-lived HttpOnly cookie and CSRF token.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from .domain import target_exposure, utc
from .finish_portal import (
    COOKIE_NAME,
    SESSION_TTL_SECONDS,
    FinishSessions,
    cf003_secondary,
    frozen_primary,
)
from .store import Conflict, Store, canonical, digest

STATIC = Path(__file__).parent / "static"


class SourceBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LinkToken(SourceBody):
    token: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class FinalAnswer(SourceBody):
    question_id: Literal["CF003-ID-01", "CF003-CENTRAL-01", "CF003-PERIPH-01"]
    answer_text: str = Field(min_length=1, max_length=20000)


ResponseOption = Literal["yes", "no", "unsure", "prefer_not_to_say"]


class FinishMetadata(SourceBody):
    rising_sign_previously_known: ResponseOption
    previous_natal_chart_reading: ResponseOption
    target_information_exposure: ResponseOption


class FinishSubmit(SourceBody):
    confirmed_review: Literal[True]
    submit_to_research: Literal[True]
    answers: list[FinalAnswer] = Field(min_length=3, max_length=3)
    metadata: FinishMetadata


def mount_finish_routes(
    app,
    store: Store,
    settings,
    require_gpt_bearer,
    public_review,
    validate_submission,
    gpt_submission_type,
) -> None:
    """Attach a disabled-by-default-until-ready browser finish to existing service."""
    router = APIRouter()
    capabilities = FinishSessions(store)
    origin = settings.public_origin.rstrip("/")

    def require_origin(request: Request) -> None:
        if not origin.startswith("https://") and not (
            not settings.secure_cookies and origin.startswith("http://")
        ):
            raise HTTPException(503, "Finishing is not configured for a safe service origin.")
        if request.headers.get("origin", "").rstrip("/") != origin:
            raise HTTPException(403, "An ordinary same-origin browser request is required.")

    def cf003_questions() -> list[dict]:
        source = settings.authority / "cf003_secondary_question_module_v0.json"
        try:
            data = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise HTTPException(
                503, "The fixed three-question supplement is unavailable."
            ) from None
        expected = ["CF003-ID-01", "CF003-CENTRAL-01", "CF003-PERIPH-01"]
        items = data.get("questions")
        if (
            data.get("schema_version") != "cf003-secondary-question-module-v0"
            or not isinstance(items, list)
            or [x.get("question_id") for x in items] != expected
            or any(not isinstance(x.get("question"), str) or not x["question"] for x in items)
        ):
            raise HTTPException(503, "The fixed secondary questions did not verify.")
        # Only question wording and IDs; hidden measurement purposes stay private.
        return [
            {"question_id": item["question_id"], "question": item["question"]} for item in items
        ]

    def safe_json(data: dict) -> JSONResponse:
        return JSONResponse(
            data,
            headers={
                "Cache-Control": "no-store, private",
                "Pragma": "no-cache",
                "Referrer-Policy": "no-referrer",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
            },
        )

    def finish_session(request: Request):
        return capabilities.session(request.cookies.get(COOKIE_NAME, ""))

    @router.get("/finish")
    def finish_page():
        return FileResponse(
            STATIC / "finish.html",
            headers={
                "Cache-Control": "no-store",
                "Referrer-Policy": "no-referrer",
                "Content-Security-Policy": (
                    "default-src 'none'; script-src 'self'; style-src 'self'; "
                    "connect-src 'self'; base-uri 'none'; form-action 'none'; "
                    "frame-ancestors 'none'; object-src 'none'"
                ),
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
            },
        )

    @router.post("/api/gpt/reviews/{review_id}/finish-link")
    def issue_finish_link(request: Request, review_id: str):
        require_gpt_bearer(request)
        if not re.fullmatch(r"R-[a-f0-9]{32}", review_id):
            raise HTTPException(404, "Review unavailable.")
        # Validate canonical origin before issuing a secret.
        if not origin.startswith("https://") and not (
            not settings.secure_cookies and origin.startswith("http://127.0.0.1:")
        ):
            raise HTTPException(503, "A configured HTTPS finish origin is required.")
        token, seconds = capabilities.issue_link(review_id)
        return safe_json(
            {
                "schema": "life-patterns-finish-link-v1",
                "finish_url": origin + "/finish#token=" + token,
                "expires_in_seconds": seconds,
                "ready_review_required": True,
                "participant_action": "Open this link privately to confirm review and finish.",
            }
        )

    @router.post("/api/finish/exchange")
    def exchange(request: Request, body: LinkToken):
        require_origin(request)
        session, _csrf = capabilities.redeem(body.token)
        response = safe_json(
            {
                "status": "session_open",
                "session_expires_in_seconds": SESSION_TTL_SECONDS,
                "next": "Read your independent review and confirm or return for correction.",
            }
        )
        response.set_cookie(
            COOKIE_NAME,
            session,
            max_age=SESSION_TTL_SECONDS,
            path="/api/finish",
            httponly=True,
            secure=settings.secure_cookies,
            samesite="strict",
        )
        return response

    @router.get("/api/finish/state")
    def finish_state(request: Request):
        session = finish_session(request)
        saved = capabilities.submitted_receipt(session)
        if saved:
            return safe_json(
                {
                    "status": "stored",
                    "submission": saved,
                    "csrf_token": "",
                }
            )
        review = store.gpt_review_read(session.review_id)
        if review.get("status") != "ready":
            raise Conflict("Review is no longer ready; continue in the original conversation.")
        summary = public_review(review)
        if not summary.get("final_review_completed"):
            raise Conflict("Independent evidence synthesis is not finalized.")
        questions = cf003_questions()
        capabilities.mark_summary_shown(session)
        token = capabilities.rotate_csrf(session)
        original = review["candidate_record"].get("turns") or []
        return safe_json(
            {
                "status": "ready",
                "review_summary": summary.get("review_summary") or [],
                "original_turn_count": len(original),
                "clarification_count": len(review.get("clarification_history") or []),
                "cf003_questions": questions,
                "csrf_token": token,
                "submission": None,
            }
        )

    @router.post("/api/finish/submit")
    def submit_finish(request: Request, body: FinishSubmit):
        require_origin(request)
        session = finish_session(request)
        csrf = request.headers.get("x-finish-csrf", "")
        capabilities.require_csrf(session, csrf)
        input_hash = digest(canonical(body.model_dump()))
        previous = capabilities.submitted_receipt(session)
        if previous:
            if input_hash != session.final_input_hash:
                raise Conflict("This review has already been submitted with different answers.")
            return safe_json(previous)
        if not session.summary_shown:
            raise Conflict("Read the entire independent review before confirming.")
        review = store.gpt_review_read(session.review_id)
        if review.get("status") != "ready":
            raise Conflict("Independent review is no longer ready.")
        fixed = cf003_questions()
        entries = [answer.model_dump() for answer in body.answers]
        if any(target_exposure(item["answer_text"]) for item in entries):
            raise ValueError("Do not enter birth/chart information in your behavioral answers.")
        confirmed_at = utc()
        primary = frozen_primary(review, confirmed_at=confirmed_at)
        secondary = cf003_secondary(fixed, entries, body.metadata.model_dump())
        submitted = gpt_submission_type(
            research_use_consented=True,
            review_id=session.review_id,
            primary_record=primary,
            cf003_record=secondary,
        )
        validated_primary, linked_secondary, primary_hash = validate_submission(submitted)
        secondary_hash = digest(canonical(linked_secondary))
        submission_hash = digest(
            canonical(
                {
                    "review_id": session.review_id,
                    "primary_record": validated_primary,
                    "cf003_record": linked_secondary,
                }
            )
        )
        payload = {
            "schema": "life-patterns-gpt-submission-v1",
            "received_at_utc": confirmed_at,
            "review_id": session.review_id,
            "independent_review": {
                "receipts": review.get("worker_receipts", []),
                "worker_state_sha256": digest(canonical(review.get("worker_state"))),
                "evidence": (review.get("worker_state") or {}).get("evidence", []),
            },
            "submission_sha256": submission_hash,
            "primary_record_sha256": primary_hash,
            "cf003_record_sha256": secondary_hash,
            "primary_record": validated_primary,
            "cf003_record": linked_secondary,
        }
        submission_id, stored, duplicate = store.create_gpt_submission(
            payload,
            submission_hash,
            finish_session_hash=session.session_hash,
            finish_input_hash=input_hash,
        )
        return safe_json(
            {
                "schema": "life-patterns-gpt-submission-receipt-v1",
                "submission_id": submission_id,
                "stored_encrypted": True,
                "independent_review_completed": True,
                "primary_record_sha256": stored["primary_record_sha256"],
                "cf003_record_sha256": stored["cf003_record_sha256"],
                "duplicate": duplicate,
            }
        )

    app.include_router(router)
