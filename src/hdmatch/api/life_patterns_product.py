"""Compose the current Life Patterns participant-value product surface."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI

from .life_patterns_app import LifePatternsFileStore
from .life_patterns_coach import OpenAILifePatternsCoach, register_life_patterns_coach_routes
from .life_patterns_voice import create_life_patterns_voice_app_from_env


def create_life_patterns_product_app_from_env() -> FastAPI:
    app = create_life_patterns_voice_app_from_env()
    root_value = os.environ.get("HDMATCH_LIFE_PATTERNS_STORE", "").strip()
    if not root_value:
        raise RuntimeError("HDMATCH_LIFE_PATTERNS_STORE is required")
    # This store is read-only in the coaching route, so it cannot race with interview writes.
    coach_store = LifePatternsFileStore(Path(root_value))
    register_life_patterns_coach_routes(
        app,
        store=coach_store,
        coach=OpenAILifePatternsCoach.from_env(),
    )
    return app
