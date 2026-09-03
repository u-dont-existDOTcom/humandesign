"""Public launch surface for the confirmatory Relationship Pattern Lab."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import hdmatch.api.relationship_public_app as base_app
from hdmatch.api.life_patterns_interview_app import create_life_patterns_interview_app_from_env
from hdmatch.api.natal_pilot_app import create_natal_pilot_app_from_env
from hdmatch.api.relationship_full_study_app import create_relationship_full_study_app_from_env
from hdmatch.api.relationship_launch_ui import HTML as LAUNCH_HTML
from hdmatch.api.relationship_study_ui_enhanced import HTML as STUDY_HTML
from hdmatch.relationship.place_resolution import search_birthplaces


def create_relationship_launch_app_from_env() -> FastAPI:
    app = create_relationship_full_study_app_from_env()
    base_app._HTML = STUDY_HTML
    app.title = "Relationship Pattern Lab"
    app.version = "0.9.0"

    natal_enabled = os.environ.get("HDMATCH_NATAL_PILOT_ENABLED", "").strip() == "1"
    if natal_enabled:
        base_app._HTML = LAUNCH_HTML

        @app.get("/relationship", response_class=HTMLResponse, include_in_schema=False)
        def relationship_study() -> str:
            return STUDY_HTML

        app.mount("/astrohd", create_natal_pilot_app_from_env())

    life_patterns_enabled = os.environ.get("HDMATCH_LIFE_PATTERNS_ENABLED", "").strip() == "1"
    if life_patterns_enabled:
        app.mount("/patterns", create_life_patterns_interview_app_from_env())

    @app.get("/api/study/places")
    def search_places(q: str) -> dict[str, Any]:
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
            "privacy_note": (
                "Only the birthplace search text is sent to OpenStreetMap Nominatim. "
                "Birth date/time, email, relationship responses, and hidden predictions "
                "are not sent to the geocoder."
            ),
        }

    return app
