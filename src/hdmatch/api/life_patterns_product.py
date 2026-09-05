"""Compose the current Life Patterns participant-value product surface."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from .life_patterns_app import LifePatternsFileStore
from .life_patterns_coach import OpenAILifePatternsCoach, register_life_patterns_coach_routes
from .life_patterns_freeze import register_life_patterns_freeze_routes
from .life_patterns_voice import create_life_patterns_voice_app_from_env


def create_life_patterns_product_app_from_env() -> FastAPI:
    app = create_life_patterns_voice_app_from_env()
    root_value = os.environ.get("HDMATCH_LIFE_PATTERNS_STORE", "").strip()
    if not root_value:
        raise RuntimeError("HDMATCH_LIFE_PATTERNS_STORE is required")
    product_store = LifePatternsFileStore(Path(root_value))
    register_life_patterns_freeze_routes(app, store=product_store)
    # Coaching reads the same private store but is explicitly checked not to mutate it.
    register_life_patterns_coach_routes(
        app,
        store=product_store,
        coach=OpenAILifePatternsCoach.from_env(),
    )

    # Replace the lower-level interview health response with the capabilities of this
    # composed product surface so operations do not falsely report voice as disabled.
    app.router.routes[:] = [
        route for route in app.router.routes if getattr(route, "path", None) != "/healthz"
    ]

    @app.get("/healthz")
    def product_health() -> dict[str, Any]:
        return {
            "status": "ok",
            "product": "discover-your-unique-life-patterns",
            "email_recovery_configured": bool(os.environ.get("HDMATCH_SMTP_PASSWORD", "").strip()),
            "participant_review_required": True,
            "voice_enabled": True,
            "behavioral_freeze_enabled": True,
            "coach_enabled": True,
        }

    return app
