"""HTTP transport for revision-bound Life Patterns operations; no private disk store."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .life_patterns_recoverability_domains import RECOVERABILITY_DOMAINS
from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_continuous_flow_ui import CONTINUOUS_FLOW_RECOVERABILITY_HTML
from .life_patterns_v2_owner_conversation import ConversationTurnRequest
from .life_patterns_v2_owner_coverage import COVERAGE_COMPLETE_STATUSES, COVERAGE_STATUSES
from .life_patterns_v2_owner_persistent import _canonical_sha
from .life_patterns_v2_owner_reasoning import ADAPTIVE_OPENING
from .life_patterns_v2_owner_recoverability import (
    RECOVERABILITY_BLUEPRINT_SHA256,
    RECOVERABILITY_BLUEPRINT_VERSION,
    _blueprint_payload,
)
from .life_patterns_v2_owner_workflow import InterviewOperation, WorkflowConflict, WorkflowSession

BUILD_VERSION = "survey-sol-xhigh-2026-09-18.5"


class RestoreRequest(BaseModel):
    snapshot: dict[str, Any]
    client_state: dict[str, Any] = Field(default_factory=dict)


class VisibleRequest(BaseModel):
    turns: list[dict[str, Any]] = Field(max_length=1000)


@dataclass
class WorkflowRuntime:
    model: Any
    sessions: dict[str, WorkflowSession] = field(default_factory=dict)
    lock: Any = field(default_factory=Lock)

    def create_session(self) -> WorkflowSession:
        sid = f"OWNER-{uuid.uuid4().hex}"
        session = WorkflowSession(session_id=sid, model=self.model)
        session.conversation.append(
            {"turn_id": f"TURN-{uuid.uuid4().hex}", "role": "assistant", "text": ADAPTIVE_OPENING}
        )
        with self.lock:
            self.sessions[sid] = session
        return session

    def get(self, session_id: str) -> WorkflowSession:
        try:
            return self.sessions[session_id]
        except KeyError as exc:
            raise HTTPException(
                404, "Session is no longer in server memory. Restore its browser checkpoint."
            ) from exc


def blueprint() -> dict[str, Any]:
    return {
        "version": RECOVERABILITY_BLUEPRINT_VERSION,
        "sha256": RECOVERABILITY_BLUEPRINT_SHA256,
        "domains": _blueprint_payload(),
        "statuses": list(COVERAGE_STATUSES),
        "complete_statuses": sorted(COVERAGE_COMPLETE_STATUSES),
    }


def measurement_package(session: WorkflowSession) -> dict[str, Any]:
    committed = session.read_committed()
    view = committed["view"]
    if view["recovery_quality"] != "exact_hidden_ledger":
        raise ValueError(
            "A reconstructed transcript is a recovery aid, not a clean research measurement."
        )
    result: dict[str, Any] = {
        "schema": "life-patterns-owner-measurement-bundle-v1",
        "evidence_archive_version": 2,
        "blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
        "blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
        "build_version": BUILD_VERSION,
        "build_commit": os.environ.get("RAILWAY_GIT_COMMIT_SHA"),
        "frozen_at": datetime.now(UTC).isoformat(),
        "session_revision": view["revision"],
        "completed_results": [
            {
                "status": p["status"]
                if p["status"] in {"accepted", "rejected", "unresolved"}
                else "unresolved",
                "wording": p["wording"],
                "origin": p["origin"],
                "proposal_id": p["proposal_id"],
                "corrections": p["corrections"],
            }
            for p in view["patterns"] if p["origin"] != "source_summary"
        ],
        "reported_summaries": [p for p in view["patterns"] if p["origin"] == "source_summary"],
        "aggregate_coverage": view["aggregate_coverage"],
        "evidence_archive": committed["snapshot"],
        "pending_inference": view["pattern_proposition"],
        "model_profile": view.get("model_profile", {}),
        "process_turn_exclusions": committed["snapshot"]["workflow"].get("process_turn_ids", []),
        "unresolved_corrections": [p for p in view["patterns"] if p["corrections"]],
        "measurement_scope": "development-only; incomplete and disputed material remains explicit",
        "scientifically_validated": False,
        "source_archive_role": "historical evidence plus append-only participant corrections; use current completed_results for current pattern status",
    }
    result["measurement_bundle_sha256"] = _canonical_sha(result)
    return result


def create_workflow_app(*, model: Any) -> FastAPI:
    app = FastAPI(title="Life Patterns owner development interview", version=BUILD_VERSION)
    runtime = WorkflowRuntime(model=model)
    app.state.recoverability_runtime = runtime
    app.state.continuous_interview_flow = True
    app.state.pre_send_question_admission = True
    app.state.same_session_cross_area_memory = True
    app.state.auto_continue_between_measurement_areas = True
    app.state.finish_for_now_always_visible = True
    app.state.question_admission_audit_in_recovery = True

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> HTMLResponse:
        return HTMLResponse(
            CONTINUOUS_FLOW_RECOVERABILITY_HTML, headers={"Cache-Control": "no-store"}
        )

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "development_surface": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "model_configured": bool(model.configured),
            "model_profile": getattr(model, "model_profile", lambda: {})(),
            "build_version": BUILD_VERSION,
            "build_commit": os.environ.get("RAILWAY_GIT_COMMIT_SHA"),
            "coverage_blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
            "coverage_blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
            "required_domain_count": len(RECOVERABILITY_DOMAINS),
            "explicit_workflow_phase": True,
            "revision_bound_operations": True,
            "fixed_episode_quota": False,
            "mandatory_counterexample_gate": False,
        }

    @app.get("/api/owner-v2/conversation/coverage/blueprint")
    def get_blueprint() -> dict[str, Any]:
        return {**blueprint(), "build_version": BUILD_VERSION}

    @app.post("/api/owner-v2/conversation/sessions")
    def create() -> dict[str, Any]:
        session = runtime.create_session()
        return {
            "session_id": session.session_id,
            "opening": ADAPTIVE_OPENING,
            "model_configured": bool(model.configured),
            **session.read_committed(),
        }

    @app.post("/api/owner-v2/conversation/sessions/restore")
    def restore(request: RestoreRequest) -> dict[str, Any]:
        sid = str(request.snapshot.get("session_id", ""))
        if not sid.startswith("OWNER-") or len(sid) > 100:
            raise HTTPException(
                422, "Invalid checkpoint session identity; original checkpoint remains unchanged."
            )
        candidate = WorkflowSession(session_id=sid, model=model)
        try:
            candidate.restore_recovery_snapshot(request.snapshot)
            if "workflow" not in request.snapshot:
                client = request.client_state
                candidate.legacy_patterns = list(client.get("completed_results", []))
                candidate.legacy_answer_memory = list(client.get("answer_memory", []))
                for key, row in dict(client.get("aggregate_coverage", {})).items():
                    candidate.coverage_aggregate.setdefault(key, row)
            with runtime.lock:
                existing = runtime.sessions.get(sid)
                # A restoration must never replace a live session. Its newest committed
                # state wins; explicit new interviews use separate random identities.
                if existing is None:
                    runtime.sessions[sid] = candidate
                session = existing or candidate
            return {**session.recovery_status(), **session.read_committed()}
        except WorkflowConflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except (ValueError, TypeError, KeyError) as exc:
            raise HTTPException(
                422, "The checkpoint could not be restored; keep the original backup."
            ) from exc

    @app.post("/api/owner-v2/conversation/sessions/restore-visible")
    def restore_visible(request: VisibleRequest) -> dict[str, Any]:
        session = runtime.create_session()
        session.visible_recovery_seed(request.turns)
        return {**session.recovery_status(), **session.read_committed()}

    @app.get("/api/owner-v2/conversation/sessions/{session_id}/recovery")
    def recovery(
        session_id: str, x_life_patterns_client: str | None = Header(default=None)
    ) -> dict[str, Any]:
        try:
            committed = runtime.get(session_id).read_committed()
            # Keep old open tabs' raw-snapshot backups compatible during the upgrade.
            return committed if x_life_patterns_client == "workflow-v1" else committed["snapshot"]
        except WorkflowConflict as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/operations")
    def operate(session_id: str, request: InterviewOperation) -> dict[str, Any]:
        try:
            return runtime.get(session_id).execute(request)
        except WorkflowConflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except (RuntimeError, TimeoutError, OSError) as exc:
            # Provider response bodies can contain sensitive text; never expose them.
            raise HTTPException(
                503, "Processing did not finish. Your response is preserved; retry this operation."
            ) from exc

    @app.get("/api/owner-v2/conversation/sessions/{session_id}/measurement")
    def measurement(session_id: str) -> dict[str, Any]:
        try:
            return measurement_package(runtime.get(session_id))
        except WorkflowConflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    # Old clients receive a recoverable upgrade boundary rather than mutating this
    # session outside the revision/operation contract. Their browser backup survives.
    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def legacy_turn(session_id: str, request: ConversationTurnRequest) -> None:
        raise HTTPException(
            409,
            "The interview has been updated. Refresh to restore your saved state before sending.",
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def legacy_adjudicate(session_id: str, request: PatternAdjudicationRequest) -> None:
        raise HTTPException(
            409, "Refresh to restore the current inference in the updated interview."
        )

    return app
