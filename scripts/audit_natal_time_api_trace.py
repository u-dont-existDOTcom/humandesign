"""Emit a reproducible synthetic trace of the server-side weekday lock."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.natal_time_app import create_natal_time_app
from hdmatch.util import canonical_json_bytes, sha256_json

CREATED_AT = datetime(2026, 8, 30, 3, 15, tzinfo=UTC)
SYNTHETIC_DATE = "2000-01-03"
SYNTHETIC_REMEMBERED_WEEKDAY = "tuesday"
SYNTHETIC_IMPLIED_WEEKDAY = "monday"


def _deterministic_id_factory() -> Callable[[str], str]:
    counts: dict[str, int] = {}

    def create(prefix: str) -> str:
        counts[prefix] = counts.get(prefix, 0) + 1
        return f"{prefix}-{counts[prefix]:024X}"

    return create


def _request_json(
    app: FastAPI,
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    parsed = urlsplit(url)
    encoded = b"" if body is None else json.dumps(body).encode()
    headers = [(b"accept", b"application/json")]
    if body is not None:
        headers.extend(
            (
                (b"content-type", b"application/json"),
                (b"content-length", str(len(encoded)).encode()),
            )
        )
    scope: Scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": parsed.path,
        "raw_path": parsed.path.encode(),
        "query_string": parsed.query.encode(),
        "root_path": "",
        "headers": headers,
        "client": ("synthetic-audit", 123),
        "server": ("synthetic-audit", 80),
        "state": {},
    }
    sent: list[Message] = []
    delivered = False

    async def receive() -> Message:
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": encoded, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    start = next(message for message in sent if message["type"] == "http.response.start")
    payload = b"".join(
        message.get("body", b"")
        for message in sent
        if message["type"] == "http.response.body"
    )
    return start["status"], json.loads(payload)


def build_trace(repository_commit: str) -> dict[str, object]:
    with TemporaryDirectory(prefix="natal-time-synthetic-api-trace-") as directory:
        app = create_natal_time_app(
            Path(directory),
            clock=lambda: CREATED_AT,
            id_factory=_deterministic_id_factory(),
        )
        intake_request = {
            "asserted_date": SYNTHETIC_DATE,
            "date_source": "memory",
            "documentary_verification": "not_applicable",
            "remembered_weekday_status": "remembered",
            "remembered_weekday": SYNTHETIC_REMEMBERED_WEEKDAY,
            "entered_how": "conspicuously_synthetic_api_trace",
        }
        intake_status, intake_response = _request_json(
            app,
            "POST",
            "/v1/natal-time/intakes",
            intake_request,
        )
        intake_text = json.dumps(intake_response, sort_keys=True)
        lineage_id = intake_response["lock"]["lineage_id"]
        assessment_path = f"/v1/natal-time/intakes/{lineage_id}/assessment"
        assessment_status, assessment_response = _request_json(
            app,
            "POST",
            assessment_path,
        )

    pre_reveal_assertions = {
        "status_200": intake_status == 200,
        "weekday_locked": intake_response["lock"]["weekday_locked"] is True,
        "implied_weekday_revealed_false": (
            intake_response["lock"]["implied_weekday_revealed"] is False
        ),
        "asserted_date_absent_from_lock_response": SYNTHETIC_DATE not in intake_text,
        "implied_weekday_absent_from_lock_response": (
            SYNTHETIC_IMPLIED_WEEKDAY not in intake_text
        ),
    }
    post_lock_assertions = {
        "status_200": assessment_status == 200,
        "conflict_fails_closed": (
            assessment_response["assessment"]["state"] == "birth_date_uncertain"
        ),
        "enumeration_disallowed": (
            assessment_response["assessment"]["enumeration_allowed"] is False
        ),
        "implied_weekday_revealed_after_lock": (
            assessment_response["assessment"]["date_weekday_facts"][0][
                "implied_weekday"
            ]
            == SYNTHETIC_IMPLIED_WEEKDAY
        ),
    }
    if not all((*pre_reveal_assertions.values(), *post_lock_assertions.values())):
        raise RuntimeError("synthetic weekday-lock API trace failed its assertions")

    payload: dict[str, object] = {
        "schema_version": "natal-time-weekday-lock-api-trace-v1",
        "synthetic_only": True,
        "claim_scope": (
            "server-side sequence and response non-disclosure only; no human calibration"
        ),
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "sequence": [
            {
                "sequence": 1,
                "event": "client_submits_date_and_independent_weekday_memory",
                "method": "POST",
                "path": "/v1/natal-time/intakes",
                "request": intake_request,
                "status_code": intake_status,
                "response": intake_response,
                "assertions": pre_reveal_assertions,
            },
            {
                "sequence": 2,
                "event": "client_requests_assessment_after_server_lock",
                "method": "POST",
                "path": assessment_path,
                "status_code": assessment_status,
                "response": assessment_response,
                "assertions": post_lock_assertions,
            },
        ],
    }
    payload["trace_sha256"] = sha256_json(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-commit", required=True)
    args = parser.parse_args()
    sys.stdout.buffer.write(canonical_json_bytes(build_trace(args.repository_commit)) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
