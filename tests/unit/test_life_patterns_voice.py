from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.life_patterns_app import LifePatternsFileStore
from hdmatch.api.life_patterns_interview_app import InterviewerResult, create_life_patterns_interview_app
from hdmatch.api.life_patterns_recovery import LifePatternsRecoveryService
from hdmatch.api.life_patterns_voice import (
    _multipart_body,
    register_life_patterns_voice_routes,
)


class FakeMapper:
    def build(self, episodes: list[dict[str, Any]]) -> tuple[Any, dict[str, str]]:
        raise ValueError(f"not needed: {len(episodes)}")


class FakeInterviewer:
    def respond(self, **_: Any) -> tuple[InterviewerResult, dict[str, str]]:
        return (
            InterviewerResult(
                reply="Tell me more.",
                episode_ready=False,
                coverage_focus="concrete episode",
            ),
            {"model": "fake", "endpoint": "test", "raw_response_sha256": "a" * 64},
        )


class FakeTranscriber:
    def __init__(self) -> None:
        self.calls: list[tuple[bytes, str]] = []

    def transcribe(self, audio: bytes, content_type: str) -> dict[str, Any]:
        self.calls.append((audio, content_type))
        return {
            "text": "This is the visible advisory transcript.",
            "model": "fake-transcriber",
            "advisory_transcript_requires_user_review": True,
            "raw_audio_stored": False,
        }


async def _asgi_request(
    app: FastAPI,
    method: str,
    url: str,
    *,
    body: bytes = b"",
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any]]:
    parsed = urlsplit(url)
    raw_headers = [(b"accept", b"application/json")]
    raw_headers.extend(
        (name.lower().encode(), value.encode()) for name, value in (headers or {}).items()
    )
    if body:
        raw_headers.append((b"content-length", str(len(body)).encode()))
    scope = cast(
        Scope,
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "path": parsed.path,
            "raw_path": parsed.path.encode(),
            "query_string": parsed.query.encode(),
            "root_path": "",
            "headers": raw_headers,
            "client": ("test", 123),
            "server": ("test", 443),
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
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    await app(scope, receive, send)
    start = next(row for row in sent if row["type"] == "http.response.start")
    response_body = b"".join(
        cast(bytes, row.get("body", b"")) for row in sent if row["type"] == "http.response.body"
    )
    return int(start["status"]), cast(dict[str, Any], json.loads(response_body or b"{}"))


def _request(
    app: FastAPI,
    method: str,
    url: str,
    *,
    body: bytes = b"",
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any]]:
    return asyncio.run(_asgi_request(app, method, url, body=body, headers=headers))


def _app(tmp_path: Path, transcriber: FakeTranscriber) -> tuple[FastAPI, LifePatternsFileStore]:
    store = LifePatternsFileStore(tmp_path / "patterns")
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    register_life_patterns_voice_routes(app, store=store, transcriber=transcriber)
    return app, store


def _create(store: LifePatternsFileStore) -> tuple[str, str]:
    payload, token = store.create()
    payload["consent_to_llm_processing"] = True
    store.save(payload)
    return str(payload["session_id"]), token


def test_voice_transcription_requires_session_authorization_and_does_not_store_audio(
    tmp_path: Path,
) -> None:
    transcriber = FakeTranscriber()
    app, store = _app(tmp_path, transcriber)
    session_id, token = _create(store)
    audio = b"synthetic-webm-bytes"

    assert _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/transcribe",
        body=audio,
        headers={"content-type": "audio/webm"},
    )[0] == 401

    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/transcribe",
        body=audio,
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "audio/webm;codecs=opus",
        },
    )
    assert status == 200
    assert payload["text"] == "This is the visible advisory transcript."
    assert payload["advisory_transcript_requires_user_review"] is True
    assert payload["raw_audio_stored"] is False
    assert transcriber.calls == [(audio, "audio/webm")]

    stored = (tmp_path / "patterns" / f"{session_id}.json").read_bytes()
    assert audio not in stored
    assert b"visible advisory transcript" not in stored


def test_transcription_is_advisory_until_participant_sends_it(tmp_path: Path) -> None:
    transcriber = FakeTranscriber()
    app, store = _app(tmp_path, transcriber)
    session_id, token = _create(store)
    status, _ = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/transcribe",
        body=b"voice",
        headers={"authorization": f"Bearer {token}", "content-type": "audio/webm"},
    )
    assert status == 200
    payload = store.read(session_id, token)
    assert payload.get("conversation_turns", []) == []
    assert payload.get("episodes", []) == []


def test_openai_multipart_body_contains_model_file_and_exact_audio_bytes() -> None:
    audio = b"\x00\x01webm\xff"
    body = _multipart_body(
        "BOUNDARY",
        fields={"model": "gpt-4o-mini-transcribe", "response_format": "json"},
        filename="voice-turn.webm",
        media_type="audio/webm",
        audio=audio,
    )
    assert b'name="model"' in body
    assert b"gpt-4o-mini-transcribe" in body
    assert b'filename="voice-turn.webm"' in body
    assert b"Content-Type: audio/webm" in body
    assert audio in body
