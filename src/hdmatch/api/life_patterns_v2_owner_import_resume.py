"""Actionable continuation for transcript-only Life Patterns recovery imports.

Older recovery JSON can preserve the visible conversation without the original hidden ledger.
Importing that transcript should not strand the participant at a generic text box. This overlay
provides an explicit development-only reconstruction path: exact participant utterances are
re-encoded conservatively as attributed self-report facts, then the target-blind interviewer
chooses either a current tentative synthesis or one genuinely necessary next question.

The reconstructed ledger is an audit/development convenience only. It is not the original
hidden ledger, is not a canonical measurement, and remains ineligible for the scientific freeze.
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import OwnerV2Session
from .life_patterns_v2_owner_conversation import HiddenFactCandidate, TurnExtraction
from .life_patterns_v2_owner_import_resume_ui import IMPORT_RESUME_RECOVERABILITY_HTML
from .life_patterns_v2_owner_pattern_first import TemporaryModelProviderError
from .life_patterns_v2_owner_persistent import (
    PersistentRecoverabilityCoverageSession,
    create_life_patterns_v2_owner_persistent_app,
)


def _participant_turns(session: PersistentRecoverabilityCoverageSession) -> list[dict[str, str]]:
    return [
        row
        for row in session.conversation
        if row.get("role") == "user" and str(row.get("text", "")).strip()
    ]


def _rebuild_visible_transcript_working_ledger(
    session: PersistentRecoverabilityCoverageSession,
) -> dict[str, Any]:
    """Create an explicitly reconstructed, non-scientific working ledger and continue.

    The original fact IDs/extraction decisions are unrecoverable. Each recovered participant
    utterance therefore becomes one attributed self-report fact with its exact source text and a
    fresh episode. This maximizes auditability and avoids pretending to recreate the lost model
    extraction. The target-blind planner may then surface a working synthesis or ask one further
    question. The result remains recovery/development state only.
    """

    if session.recovery_quality not in {
        "visible_transcript_only",
        "reconstructed_visible_transcript",
    }:
        raise ValueError("this action is only for transcript-only recovery sessions")

    turns = _participant_turns(session)
    if not turns:
        raise ValueError("recovered transcript contains no participant answers")

    # Rebuild from source utterances rather than trying to repair an empty/partial old ledger.
    session.core = OwnerV2Session(session_id=session.session_id, model=session.model)
    session.current_episode_id = None
    session.awaiting_new_episode = True
    session.pending_boundary_question = False
    session.boundary_answered = True
    session.pattern_focus_established = True
    session._draft_move = None
    session._last_progress_report = None
    session._last_progress_user_turn_count = 0

    for index, row in enumerate(turns, start=1):
        text = str(row["text"]).strip()
        proposition = f"Participant reported in recovered transcript: {text}"
        if len(proposition) > 2000:
            proposition = proposition[:1997] + "..."
        extraction = TurnExtraction(
            episode_summary=f"Recovered participant statement {index}",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition=proposition,
                ),
            ),
            corrections=(),
        )
        session.current_episode_id = None
        session.awaiting_new_episode = True
        session._apply_extraction(
            extraction=extraction,
            turn_id=f"RECOVERED-SOURCE-{index:04d}-{uuid.uuid4().hex[:6].upper()}",
            message=text,
            start_new_episode=True,
        )

    session.recovery_quality = "reconstructed_visible_transcript"

    move = session.model.plan_turn(
        current_episode_id=session.current_episode_id,
        episodes=session.core.record.episodes,
        operative_facts=session.core.operative_facts(),
        recent_conversation=tuple(session.conversation),
        boundary_answered=True,
    )

    if move.move_type == "surface_hypothesis":
        session._create_pattern(move)
    elif move.move_type == "request_contrast":
        session.awaiting_new_episode = True
        session.current_episode_id = None
    elif move.move_type == "boundary_question":
        session.pending_boundary_question = True

    session.conversation.append(
        {
            "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
            "role": "assistant",
            "text": move.reply,
        }
    )
    result: dict[str, Any] = {
        "reply": move.reply,
        "move_type": move.move_type,
        "pattern_active": session._draft_move is not None,
        "pattern_proposition": (
            session._draft_move.hypothesis_proposition if session._draft_move is not None else None
        ),
        "episode_count": len(session.core.record.episodes),
        "recovery_quality": session.recovery_quality,
        "reconstructed_from_visible_transcript": True,
        "scientific_freeze_eligible": False,
        "working_ledger_validation_status": "reconstructed_unvalidated",
    }
    return session._attach_periodic_progress(result, force=True)


def create_life_patterns_v2_owner_import_resume_app() -> FastAPI:
    """Serve persistent recovery plus an actionable transcript-only continuation seam."""

    app = create_life_patterns_v2_owner_persistent_app()
    runtime = app.state.recoverability_runtime

    # Replace only the root UI. Existing exact audit/recovery endpoints remain unchanged.
    app.router.routes[:] = [
        route for route in app.router.routes if getattr(route, "path", None) != "/"
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return IMPORT_RESUME_RECOVERABILITY_HTML

    @app.post(
        "/api/owner-v2/conversation/sessions/{session_id}/reconstruct-visible"
    )
    def reconstruct_visible(session_id: str) -> dict[str, Any]:
        try:
            session = runtime.get(session_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        if not isinstance(session, PersistentRecoverabilityCoverageSession):
            raise HTTPException(status_code=409, detail="session does not support recovery reconstruction")
        try:
            return _rebuild_visible_transcript_working_ledger(session)
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    app.state.transcript_only_import_has_explicit_continuation = True
    app.state.transcript_reconstruction_is_non_scientific = True
    return app
