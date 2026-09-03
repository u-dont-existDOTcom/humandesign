from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.life_patterns_app import LifePattern, LifePatternsFileStore, LifePatternsMap
from hdmatch.api.life_patterns_coach import CoachResult, register_life_patterns_coach_routes


class FakeCoach:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def respond(
        self,
        *,
        life_patterns_map: LifePatternsMap,
        approved_episodes: list[dict[str, Any]],
        message: str,
    ) -> tuple[CoachResult, dict[str, str]]:
        self.calls.append(
            {
                "life_patterns_map": life_patterns_map.model_dump(mode="json"),
                "approved_episodes": approved_episodes,
                "message": message,
            }
        )
        return (
            CoachResult(
                reply="A strategy that helped in work may be worth testing here at low stakes.",
                referenced_pattern_ids=("P1",),
                suggested_experiment="Try the strategy once in a reversible situation and compare the result.",
                important_uncertainty="The profile has only two supporting episodes.",
            ),
            {"model": "fake-coach", "endpoint": "test", "raw_response_sha256": "c" * 64},
        )


async def _asgi_request(
    app: FastAPI,
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    parsed = urlsplit(url)
    encoded = b"" if body is None else json.dumps(body).encode()
    headers = [(b"accept", b"application/json")]
    if body is not None:
        headers.extend(
            [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(encoded)).encode()),
            ]
        )
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
            "headers": headers,
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
        return {"type": "http.request", "body": encoded, "more_body": False}

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
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    return asyncio.run(_asgi_request(app, method, url, body=body))


def _seed(store: LifePatternsFileStore) -> tuple[str, str, bytes]:
    payload, token = store.create()
    payload["consent_to_llm_processing"] = True
    now = datetime.now(UTC).isoformat()
    payload["episodes"] = [
        {"episode_id": "EP-1", "domain": "work_projects", "title": "Work", "narrative": "I ran a small test before committing.", "counterexample": None, "input_modality": "typed", "source_turn_ids": [], "review_status": "approved", "participant_revision": False, "reviewed_at_utc": now, "created_at_utc": now},
        {"episode_id": "EP-2", "domain": "relationships", "title": "Relationship", "narrative": "I moved faster and used less explicit testing.", "counterexample": None, "input_modality": "typed", "source_turn_ids": [], "review_status": "approved", "participant_revision": False, "reviewed_at_utc": now, "created_at_utc": now},
    ]
    payload["life_patterns_map"] = LifePatternsMap(
        overall_summary="Testing behavior differs by context.",
        patterns=(
            LifePattern(
                pattern_id="P1",
                title="Small tests help in uncertain work decisions",
                summary="The work episode used a low-cost experiment before commitment.",
                status="tentative",
                confidence=0.7,
                supporting_episode_ids=("EP-1",),
            ),
        ),
        transfer_opportunities=("Try a small reversible test in another domain.",),
    ).model_dump(mode="json")
    store.save(payload)
    path = store.root / f"{payload['session_id']}.json"
    return str(payload["session_id"]), token, path.read_bytes()


def test_coach_uses_only_approved_profile_and_cannot_mutate_research_record(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    coach = FakeCoach()
    app = FastAPI()
    register_life_patterns_coach_routes(app, store=store, coach=coach)
    session_id, token, before = _seed(store)

    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/coach",
        body={"token": token, "message": "How could I approach an uncertain personal project?"},
    )
    assert status == 200
    assert payload["research_evidence_mutated"] is False
    result = cast(dict[str, Any], payload["result"])
    assert result["boundary"] == "evidence_linked_coaching_not_fixed_identity_or_research_evidence"
    assert result["referenced_pattern_ids"] == ["P1"]
    assert (store.root / f"{session_id}.json").read_bytes() == before

    call = coach.calls[0]
    serialized = json.dumps(call).casefold()
    for forbidden in ("astrology", "human design", "birth chart", "candidate_state", "model_fit"):
        assert forbidden not in serialized
    assert {row["episode_id"] for row in call["approved_episodes"]} == {"EP-1", "EP-2"}


def test_coach_requires_existing_map(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    payload, token = store.create()
    payload["consent_to_llm_processing"] = True
    store.save(payload)
    app = FastAPI()
    register_life_patterns_coach_routes(app, store=store, coach=FakeCoach())
    status, _ = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{payload['session_id']}/coach",
        body={"token": token, "message": "Help me think."},
    )
    assert status == 409
