from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.life_patterns_product import create_life_patterns_product_app_from_env


async def _asgi_get(app: FastAPI, url: str) -> tuple[int, dict[str, Any]]:
    parsed = urlsplit(url)
    scope = cast(
        Scope,
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "https",
            "path": parsed.path,
            "raw_path": parsed.path.encode(),
            "query_string": parsed.query.encode(),
            "root_path": "",
            "headers": [(b"accept", b"application/json")],
            "client": ("test", 123),
            "server": ("testserver", 443),
            "state": {},
        },
    )
    sent: list[Message] = []
    delivered = False

    async def receive() -> Message:
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    await app(scope, receive, send)
    start = next(row for row in sent if row["type"] == "http.response.start")
    response_body = b"".join(
        cast(bytes, row.get("body", b"")) for row in sent if row["type"] == "http.response.body"
    )
    return int(start["status"]), cast(dict[str, Any], json.loads(response_body or b"{}"))


def test_product_health_reports_voice_freeze_and_coach(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    monkeypatch.setenv("HDMATCH_LIFE_PATTERNS_STORE", str(tmp_path / "patterns"))
    monkeypatch.delenv("HDMATCH_SMTP_PASSWORD", raising=False)
    app = create_life_patterns_product_app_from_env()
    status, payload = asyncio.run(_asgi_get(app, "/healthz"))
    assert status == 200
    assert payload == {
        "status": "ok",
        "product": "discover-your-unique-life-patterns",
        "email_recovery_configured": False,
        "participant_review_required": True,
        "voice_enabled": True,
        "behavioral_freeze_enabled": True,
        "coach_enabled": True,
    }
