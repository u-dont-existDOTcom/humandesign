"""Add one ready-only GPT Action for secure Railway browser finishing.

All previously frozen six Action request/response contracts are unchanged.
"""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = (
    ROOT
    / "reference/custom_gpt/releases"
    / "Life-Patterns-GPT-honest-review-progress-2026-10-16.zip"
)
OUT = ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"
NAME = "ACTION-life-patterns-submission-openapi.yaml"


def generate() -> bytes:
    with zipfile.ZipFile(BASE) as archive:
        original = json.loads(archive.read(NAME))
    if original["info"]["version"] != "1.6.1":
        raise ValueError("Expected cumulative Oct16 progress-contract baseline")
    assert len(original["paths"]) == 6
    if "FinishLink" in original["components"]["schemas"]:
        raise ValueError("A finish-link implementation already exists")
    original["info"]["version"] = "1.7.0"
    original["info"]["description"] = (
        "Independent review, encrypted final submission and a participant-approved "
        "single-use finishing link, available only when review is ready."
    )
    original["components"]["schemas"]["FinishLink"] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "schema": {"type": "string"},
            "finish_url": {
                "type": "string",
                "format": "uri",
                "description": (
                    "A single-use secret browser link valid briefly; share only "
                    "with the participant in their current private conversation."
                ),
            },
            "expires_in_seconds": {"type": "integer", "minimum": 1},
            "ready_review_required": {"type": "boolean"},
            "participant_action": {"type": "string"},
        },
        "required": [
            "schema",
            "finish_url",
            "expires_in_seconds",
            "ready_review_required",
            "participant_action",
        ],
    }
    original["paths"]["/api/gpt/reviews/{review_id}/finish-link"] = {
        "post": {
            "operationId": "issueLifePatternsFinishLink",
            "summary": "Create a one-time private Railway finishing link for a ready review",
            "description": (
                "Only after status ready and participant opts for Railway finish. "
                "Say: Please click Allow on this tool call to continue. "
                "Keep the one-time link private; use only this saved review_id. "
                "Railway collects confirmation, the three CF003 answers and "
                "encrypted submission. This call does not submit anything."
            ),
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "review_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "pattern": "^R-[a-f0-9]{32}$"},
                    "description": "Opaque current review ID already saved in this conversation.",
                }
            ],
            "responses": {
                "200": {
                    "description": "One-time link generated; not submitted.",
                    "content": {
                        "application/json": {"schema": {"$ref": "#/components/schemas/FinishLink"}}
                    },
                },
                "401": {"description": "GPT Action credential not accepted."},
                "409": {"description": "Review not yet ready or already submitted."},
                "503": {"description": "Private HTTPS finishing origin unavailable."},
            },
            "x-openai-isConsequential": True,
        }
    }
    return (json.dumps(original, indent=2, ensure_ascii=False) + "\n").encode()


def main() -> None:
    data = generate()
    if "--check" in sys.argv:
        if OUT.read_bytes() != data:
            raise ValueError("OpenAPI generation is not reproducible")
    else:
        OUT.write_bytes(data)
    print("OPENAPI_FINISH", "CHECKED" if "--check" in sys.argv else "BUILT", len(data))


if __name__ == "__main__":
    main()
