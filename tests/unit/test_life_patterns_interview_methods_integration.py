"""No external services: exercise the actual ASGI routes and mocked provider boundary."""
from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

import pytest
from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api import life_patterns_interview_app as module
from hdmatch.api.life_patterns_app import LifePatternsFileStore
from hdmatch.api.life_patterns_freeze import _source_turns
from hdmatch.api.life_patterns_interview_methods import (
    INTERVIEW_OPENING, METHODS_VERSION, PROCESS_POLICY, ClarificationNote,
)
from hdmatch.api.life_patterns_recovery import LifePatternsRecoveryService


class NotesInterviewer:
    def __init__(self, *, invalid_reference: bool = False) -> None:
        self.invalid_reference = invalid_reference

    def respond(self, *, turns: list[dict[str, Any]], **_: Any) -> tuple[module.InterviewerResult, dict[str, str]]:
        source_id = "missing" if self.invalid_reference else str(turns[-1]["turn_id"])
        return module.InterviewerResult(
            reply="We can leave the date uncertain.", episode_ready=False,
            coverage_focus="none_material", clarification_notes=(ClarificationNote(
                gap_id="GAP-date", issue="The date is not remembered.", status="unknown",
                source_turn_ids=(source_id,),
            ),),
        ), {"model": "synthetic", "raw_response_sha256": "f" * 64}


async def _asgi(app: FastAPI, method: str, url: str, body: dict[str, Any] | None) -> tuple[int, dict[str, Any]]:
    parsed = urlsplit(url)
    data = b"" if body is None else json.dumps(body).encode()
    scope = cast(Scope, {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1", "method": method, "scheme": "https",
        "path": parsed.path, "raw_path": parsed.path.encode(), "query_string": parsed.query.encode(),
        "root_path": "", "headers": [(b"content-type", b"application/json"),
                                        (b"content-length", str(len(data)).encode())],
        "client": ("test", 1), "server": ("test", 443), "state": {},
    })
    sent: list[Message] = []
    delivered = False

    async def receive() -> Message:
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": data, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    await app(scope, receive, send)
    status = next(r["status"] for r in sent if r["type"] == "http.response.start")
    raw = b"".join(cast(bytes, r.get("body", b"")) for r in sent if r["type"] == "http.response.body")
    return int(status), cast(dict[str, Any], json.loads(raw or b"{}"))


def request(app: FastAPI, method: str, url: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    return asyncio.run(_asgi(app, method, url, body))


def setup(tmp_path: Path, *, invalid_reference: bool = False) -> tuple[FastAPI, LifePatternsFileStore, str, str]:
    store = LifePatternsFileStore(tmp_path / "private")
    app = module.create_life_patterns_interview_app(
        store=store, interviewer=NotesInterviewer(invalid_reference=invalid_reference),
        mapper=object(), recovery=LifePatternsRecoveryService(store, None),
    )
    status, created = request(app, "POST", "/api/life-patterns/interview/sessions", {
        "email": "synthetic@example.test", "consent_to_store_responses": True,
        "consent_to_llm_processing": True,
    })
    assert status == 200
    return app, store, str(created["session_id"]), str(created["resume_token"])


def test_new_session_persists_exact_opener_not_just_ui_text(tmp_path: Path) -> None:
    app, store, sid, token = setup(tmp_path)
    payload = store.read(sid, token)
    assert payload["interview_schema_version"] == "life-patterns-conversation-v4"
    first = payload["conversation_turns"][0]
    assert first["role"] == "assistant"
    assert first["text"] == INTERVIEW_OPENING
    assert first["source_kind"] == "fixed_interview_opening"
    status, public = request(app, "GET", f"/api/life-patterns/interview/sessions/{sid}?token={token}")
    assert status == 200
    assert public["conversation_turns"][0]["text"] == first["text"]
    assert public["progress"]["episode_count"] == 0


def test_notes_persist_but_do_not_count_as_evidence(tmp_path: Path) -> None:
    app, store, sid, token = setup(tmp_path)
    status, response = request(app, "POST", f"/api/life-patterns/interview/sessions/{sid}/turns", {
        "token": token, "message": "I do not remember the date.",
    })
    assert status == 200
    assert response["clarification_log"]["policy"] == PROCESS_POLICY
    assert response["clarification_log"]["items"][0]["status"] == "unknown"
    assert response["episode_saved"] is False
    assert response["progress"]["episode_count"] == 0
    assert response["map_available"] is False
    saved = store.read(sid, token)
    assert saved["episodes"] == []
    turns = saved["conversation_turns"]
    assert turns[-1]["interview_methods_version"] == METHODS_VERSION
    assert turns[-1]["clarification_notes"][0]["source_turn_ids"] == [turns[-2]["turn_id"]]


def test_invalid_source_rejected_after_user_message_is_saved(tmp_path: Path) -> None:
    app, store, sid, token = setup(tmp_path, invalid_reference=True)
    status, response = request(app, "POST", f"/api/life-patterns/interview/sessions/{sid}/turns", {
        "token": token, "message": "This message must survive invalid AI output.",
    })
    assert status == 502
    assert "saved" in response["detail"]
    saved = store.read(sid, token)
    assert saved["conversation_turns"][-1]["role"] == "user"
    assert len(saved["conversation_turns"]) == 2
    assert saved["episodes"] == []


def test_legacy_record_not_backfilled_or_relabeled(tmp_path: Path) -> None:
    app, store, sid, token = setup(tmp_path)
    payload = store.read(sid, token)
    payload["interview_schema_version"] = "life-patterns-conversation-v2"
    original = {"turn_id": "old-user", "role": "user", "text": "Earlier answer."}
    payload["conversation_turns"] = [original]
    store.save(payload)
    status, _ = request(app, "POST", f"/api/life-patterns/interview/sessions/{sid}/turns", {
        "token": token, "message": "I still cannot remember the date.",
    })
    assert status == 200
    saved = store.read(sid, token)
    assert saved["interview_schema_version"] == "life-patterns-conversation-v2"
    assert saved["conversation_turns"][0] == original
    assert all(t.get("source_kind") != "fixed_interview_opening" for t in saved["conversation_turns"])


def test_freeze_evidence_sources_do_not_include_process_notes() -> None:
    payload = {"conversation_turns": [
        {"turn_id": "A0", "role": "assistant", "text": INTERVIEW_OPENING},
        {"turn_id": "U1", "role": "user", "text": "A real event was reported."},
        {"turn_id": "A1", "role": "assistant", "text": "Reply", "clarification_notes": []},
    ]}
    sources = _source_turns(payload, [{"source_turn_ids": ["U1"]}])
    assert sources == [payload["conversation_turns"][1]]


def test_provider_receives_paired_sources_and_gap_log_without_external_call(monkeypatch: pytest.MonkeyPatch) -> None:
    requests: list[dict[str, Any]] = []
    turns = [
        {"turn_id": "A0", "role": "assistant", "text": "Which period?"},
        {"turn_id": "U1", "role": "user", "text": "During college."},
    ]
    result = module.InterviewerResult(reply="Understood.", episode_ready=False, coverage_focus="none_material")

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: Any) -> None:
            return None

        def read(self) -> bytes:
            return b"synthetic-response"

    def opener(req: Any, **_: Any) -> Response:
        requests.append(json.loads(req.data))
        return Response()

    monkeypatch.setattr(module, "urlopen", opener)
    monkeypatch.setattr(module, "_parse_openai_json", lambda _: result.model_dump(mode="json"))
    _, receipt = module.OpenAILifePatternsInterviewer(api_key="fake", model="mock").respond(
        episodes=[], turns=turns, progress={},
    )
    body = requests[0]
    supplied = json.loads(body["input"][0]["content"])
    assert supplied["participant_statement_index"][0]["preceding_interviewer_turn"]["turn_id"] == "A0"
    assert supplied["context_coverage"]["participant_turns_omitted"] == 0
    assert supplied["clarification_log"]["policy"] == PROCESS_POLICY
    assert "clarification_notes" in body["text"]["format"]["schema"]["required"]
    assert body["store"] is False
    assert receipt["interview_methods_version"] == METHODS_VERSION
    assert receipt["interview_prompt_sha256"] == hashlib.sha256(body["instructions"].encode()).hexdigest()
    for name in ("astrology", "human design", "astrohd"):
        assert name not in body["instructions"].casefold()
