"""Public launch surface for the confirmatory Relationship Pattern Lab."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException

import hdmatch.api.relationship_public_app as base_app
from hdmatch.api.relationship_full_study_app import create_relationship_full_study_app_from_env
from hdmatch.api.relationship_study_ui_enhanced import HTML as STUDY_HTML
from hdmatch.relationship.place_resolution import search_birthplaces


def create_relationship_launch_app_from_env() -> FastAPI:
    app = create_relationship_full_study_app_from_env()
    base_app._HTML = STUDY_HTML
    app.title = "Relationship Pattern Lab"
    app.version = "0.8.1"

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
