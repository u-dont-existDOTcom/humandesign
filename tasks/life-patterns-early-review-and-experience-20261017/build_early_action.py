"""Cumulative read-only schema extension for early review handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = (
    ROOT / "tasks/life-patterns-railway-finishing-20261016/frozen_source/action-openapi-v1.7.0.json"
)
OUT = ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"


def build() -> bytes:
    data = json.loads(BASE.read_text())
    assert data["info"]["version"] == "1.7.0"
    assert len(data["paths"]) == 7
    data["info"]["version"] = "1.8.0"
    data["info"]["description"] = (
        "Saved reviews may continue on Railway before final independent readiness."
    )
    path = "/api/gpt/reviews/{review_id}/finish-link"
    op = data["paths"][path]["post"]
    assert op["operationId"] == "issueLifePatternsFinishLink"
    op["summary"] = "Continue an already saved review privately on Railway"
    op["description"] = (
        "For a saved consented review, offer a Railway link now. "
        "Issue it only with participant approval. Railway handles admitted "
        "questions, live review status, optional end of question intake with "
        "unknowns preserved, and ready-only final confirmation and storage. "
        "Do not continue that review in GPT."
    )
    op["responses"]["200"]["description"] = "One-time review link; not final storage."
    op["responses"]["409"]["description"] = "Review ended, withdrawn, or already submitted."
    data["components"]["schemas"]["FinishLink"]["properties"]["ready_review_required"][
        "description"
    ] = "False; independent ready is still required for final submission."
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()


if __name__ == "__main__":
    built = build()
    if "--check" in sys.argv:
        assert OUT.read_bytes() == built
    else:
        OUT.write_bytes(built)
    print("EARLY_REVIEW_SCHEMA", "CHECK" if "--check" in sys.argv else "BUILT")
