"""Final participant-facing liveness wrapper for the Life Patterns development interview."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_import_resume import create_life_patterns_v2_owner_import_resume_app
from .life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def create_life_patterns_v2_owner_liveness_app() -> FastAPI:
    app = create_life_patterns_v2_owner_import_resume_app()
    app.router.routes[:] = [
        route for route in app.router.routes if getattr(route, "path", None) != "/"
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return LIVENESS_RECOVERABILITY_HTML

    app.state.long_operation_feedback = True
    app.state.recovery_restores_coverage_blueprint = True
    app.state.progress_false_complete_guard = True
    return app
