"""Browser-persistent audit/recovery checkpoints for the Life Patterns development interview.

The live development service deliberately does not persist private interview narratives on
Railway. Instead, this layer exposes a JSON snapshot of the exact in-memory *working* hidden
ledger so the participant's browser can preserve it for audit and crash recovery after each
successful turn. A later server process can restore that snapshot without re-running the
interview or reconstructing facts from prose.

Exact recovery means lossless state preservation, not scientific correctness. The snapshot is
explicitly an unvalidated working/audit checkpoint and never becomes a canonical measurement or
scientific freeze merely because it can be restored.

A transcript-only import seam is also provided for older recovery files that predate exact
hidden-ledger snapshots. Those imports restore conversational context only and are explicitly
not eligible to masquerade as an exact scientific recovery.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from types import MethodType
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from hdmatch.evaluation.participant_adjudicated_v2 import LifePatternsRecordV2

from .life_patterns_v2_owner_app import ExtractedEpisode, PendingEpisode
from .life_patterns_v2_owner_conversation import ConversationMove
from .life_patterns_v2_owner_persistent_ui import PERSISTENT_RECOVERABILITY_HTML
from .life_patterns_v2_owner_recoverability import RecoverabilityCoverageRuntime
from .life_patterns_v2_owner_resilient import (
    ResilientRecoverabilityCoverageSession,
    create_life_patterns_v2_owner_resilient_app,
)

_RECOVERY_SCHEMA = "life-patterns-hidden-ledger-session-v2"


class RecoveryRestoreRequest(BaseModel):
    snapshot: dict[str, Any]


class VisibleRecoveryRestoreRequest(BaseModel):
    turns: list[dict[str, Any]] = Field(default_factory=list, max_length=300)


def _canonical_sha(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
    ).hexdigest()


class PersistentRecoverabilityCoverageSession(ResilientRecoverabilityCoverageSession):
    """Resilient session with exact JSON audit/recovery snapshots of the working ledger."""

    recovery_quality: str = "exact_hidden_ledger"

    def recovery_snapshot(self) -> dict[str, Any]:
        pending = {
            episode_id: {
                "episode_id": row.episode_id,
                "text": row.text,
                "extracted": row.extracted.model_dump(mode="json"),
            }
            for episode_id, row in self.core.pending_episodes.items()
        }
        body: dict[str, Any] = {
            "schema": _RECOVERY_SCHEMA,
            "session_id": self.session_id,
            "recovery_quality": self.recovery_quality,
            "snapshot_role": "unvalidated_working_audit_checkpoint",
            "canonical_measurement": False,
            "scientific_freeze": False,
            "conversation": [dict(row) for row in self.conversation],
            "current_episode_id": self.current_episode_id,
            "awaiting_new_episode": self.awaiting_new_episode,
            "pending_boundary_question": self.pending_boundary_question,
            "boundary_answered": self.boundary_answered,
            "pattern_focus_established": self.pattern_focus_established,
            "record": self.core.record.model_dump(mode="json"),
            "pending_episodes": pending,
            "proposal_support": {
                proposal_id: sorted(fact_ids)
                for proposal_id, fact_ids in self.core.proposal_support.items()
            },
            "active_proposal_id": self.core.active_proposal_id,
            "draft_move": (
                self._draft_move.model_dump(mode="json") if self._draft_move is not None else None
            ),
            "last_progress_user_turn_count": self._last_progress_user_turn_count,
            "last_progress_report": self._last_progress_report,
        }
        body["recovery_sha256"] = _canonical_sha(body)
        return body

    def restore_recovery_snapshot(self, snapshot: dict[str, Any]) -> None:
        if snapshot.get("schema") != _RECOVERY_SCHEMA:
            raise ValueError("unsupported hidden-ledger recovery schema")
        supplied_sha = str(snapshot.get("recovery_sha256", ""))
        unsigned = dict(snapshot)
        unsigned.pop("recovery_sha256", None)
        expected_sha = _canonical_sha(unsigned)
        if not supplied_sha or supplied_sha != expected_sha:
            raise ValueError("recovery JSON checksum does not match its contents")

        record = LifePatternsRecordV2.model_validate(snapshot.get("record", {}))
        conversation: list[dict[str, str]] = []
        for index, row in enumerate(snapshot.get("conversation", [])):
            if not isinstance(row, dict):
                continue
            role = str(row.get("role", ""))
            text = str(row.get("text", ""))
            if role not in {"user", "assistant"} or not text:
                continue
            turn_id = str(row.get("turn_id", "")) or f"RECOVERED-{index:04d}"
            conversation.append({"turn_id": turn_id, "role": role, "text": text})

        pending: dict[str, PendingEpisode] = {}
        for episode_id, raw in dict(snapshot.get("pending_episodes", {})).items():
            if not isinstance(raw, dict):
                continue
            recovered_id = str(raw.get("episode_id", episode_id))
            pending[recovered_id] = PendingEpisode(
                episode_id=recovered_id,
                text=str(raw.get("text", "")),
                extracted=ExtractedEpisode.model_validate(raw.get("extracted", {})),
            )

        proposal_support: dict[str, frozenset[str]] = {}
        for proposal_id, fact_ids in dict(snapshot.get("proposal_support", {})).items():
            if isinstance(fact_ids, list):
                proposal_support[str(proposal_id)] = frozenset(str(item) for item in fact_ids)

        draft_raw = snapshot.get("draft_move")
        draft = ConversationMove.model_validate(draft_raw) if isinstance(draft_raw, dict) else None

        self.conversation = conversation
        self.current_episode_id = (
            str(snapshot["current_episode_id"])
            if snapshot.get("current_episode_id") is not None
            else None
        )
        self.awaiting_new_episode = bool(snapshot.get("awaiting_new_episode", True))
        self.pending_boundary_question = bool(snapshot.get("pending_boundary_question", False))
        self.boundary_answered = bool(snapshot.get("boundary_answered", False))
        self.pattern_focus_established = bool(snapshot.get("pattern_focus_established", False))
        self.core.record = record
        self.core.pending_episodes = pending
        self.core.proposal_support = proposal_support
        self.core.active_proposal_id = (
            str(snapshot["active_proposal_id"])
            if snapshot.get("active_proposal_id") is not None
            else None
        )
        self._draft_move = draft
        self._last_progress_user_turn_count = int(
            snapshot.get("last_progress_user_turn_count", 0)
        )
        progress = snapshot.get("last_progress_report")
        self._last_progress_report = progress if isinstance(progress, dict) else None
        quality = str(snapshot.get("recovery_quality", "exact_hidden_ledger"))
        self.recovery_quality = (
            quality
            if quality in {"exact_hidden_ledger", "visible_transcript_only"}
            else "exact_hidden_ledger"
        )

    def visible_recovery_seed(self, turns: list[dict[str, Any]]) -> None:
        """Restore old visible transcript context without pretending the old ledger exists."""

        conversation: list[dict[str, str]] = []
        for index, row in enumerate(turns[:300]):
            if not isinstance(row, dict):
                continue
            role = str(row.get("role", ""))
            text = str(row.get("text", ""))
            if role not in {"user", "assistant"} or not text:
                continue
            conversation.append(
                {"turn_id": f"VISIBLE-RECOVERY-{index:04d}", "role": role, "text": text}
            )
        if not conversation:
            raise ValueError("visible recovery file contains no usable interview turns")
        self.conversation = conversation
        self.pattern_focus_established = any(row["role"] == "user" for row in conversation)
        self.current_episode_id = None
        self.awaiting_new_episode = True
        self.pending_boundary_question = False
        self.boundary_answered = False
        self._draft_move = None
        self._last_progress_report = None
        self._last_progress_user_turn_count = 0
        self.recovery_quality = "visible_transcript_only"

    def recovery_status(self) -> dict[str, Any]:
        proposition = self._active_proposition() if self._draft_move is not None else None
        exact = self.recovery_quality == "exact_hidden_ledger"
        return {
            "session_id": self.session_id,
            "recovery_quality": self.recovery_quality,
            "conversation": [dict(row) for row in self.conversation],
            "pattern_active": self._draft_move is not None,
            "pattern_proposition": proposition,
            "coverage": self._last_progress_report,
            "exact_hidden_ledger_restored": exact,
            "resume_capable": exact,
            "working_ledger_validation_status": "unvalidated",
            "requires_audit_before_scientific_use": True,
            "scientific_freeze_eligible": False,
        }


def _create_persistent_session(
    runtime: RecoverabilityCoverageRuntime,
) -> PersistentRecoverabilityCoverageSession:
    session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
    session = PersistentRecoverabilityCoverageSession(session_id=session_id, model=runtime.model)
    runtime.sessions[session_id] = session
    return session


def create_life_patterns_v2_owner_persistent_app() -> FastAPI:
    """Serve the owner interview with browser-local working-ledger audit/recovery snapshots."""

    app = create_life_patterns_v2_owner_resilient_app()
    runtime = app.state.recoverability_runtime
    runtime.create_session = MethodType(_create_persistent_session, runtime)

    app.router.routes[:] = [
        route for route in app.router.routes if getattr(route, "path", None) != "/"
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return PERSISTENT_RECOVERABILITY_HTML

    @app.get("/api/owner-v2/conversation/sessions/{session_id}/recovery")
    def export_recovery(session_id: str) -> dict[str, Any]:
        try:
            session = runtime.get(session_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        if not isinstance(session, PersistentRecoverabilityCoverageSession):
            raise HTTPException(status_code=409, detail="session predates exact recovery support")
        return session.recovery_snapshot()

    @app.post("/api/owner-v2/conversation/sessions/restore")
    def restore_recovery(request: RecoveryRestoreRequest) -> dict[str, Any]:
        raw_id = str(request.snapshot.get("session_id", "")).strip()
        session_id = (
            raw_id if raw_id.startswith("OWNER-") else f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        )
        session = PersistentRecoverabilityCoverageSession(session_id=session_id, model=runtime.model)
        try:
            session.restore_recovery_snapshot(request.snapshot)
        except (TypeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        runtime.sessions[session_id] = session
        return session.recovery_status()

    @app.post("/api/owner-v2/conversation/sessions/restore-visible")
    def restore_visible(request: VisibleRecoveryRestoreRequest) -> dict[str, Any]:
        session = _create_persistent_session(runtime)
        try:
            session.visible_recovery_seed(request.turns)
        except ValueError as exc:
            runtime.sessions.pop(session.session_id, None)
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return session.recovery_status()

    app.state.exact_hidden_ledger_browser_recovery = True
    app.state.working_ledger_snapshots_are_unvalidated = True
    app.state.recovery_import = True
    app.state.visible_transcript_import_is_non_scientific = True
    return app
