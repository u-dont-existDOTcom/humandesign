from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.life_patterns_app import (
    LifePattern,
    LifePatternsFileStore,
    LifePatternsMap,
    create_life_patterns_app,
)


class FakeMapper:
    def __init__(self) -> None:
        self.seen_episodes: list[dict[str, Any]] | None = None

    def build(self, episodes: list[dict[str, Any]]) -> tuple[LifePatternsMap, dict[str, str]]:
        self.seen_episodes = episodes
        return (
            LifePatternsMap(
                overall_summary="The supplied episodes show both recurring and context-dependent patterns.",
                patterns=(
                    LifePattern(
                        pattern_id="P1",
                        title="Context changes the decision process",
                        summary=(
                            "Relationship and work episodes used meaningfully different processes; "
                            "the evidence does not support one universal style."
                        ),
                        status="context_dependent",
                        confidence=0.8,
                        supporting_episode_ids=tuple(row["episode_id"] for row in episodes),
                        contexts=("relationships", "work_projects"),
                    ),
                ),
                strengths=("The participant supplies concrete counterexamples.",),
                friction_points=("Broad self-descriptions can hide domain differences.",),
                transfer_opportunities=(
                    "Test whether a successful work-planning strategy helps in another low-stakes domain.",
                ),
                reversible_experiments=("Try one low-stakes cross-domain planning experiment.",),
                important_unknowns=("More conflict/stress evidence would improve the map.",),
            ),
            {"model": "fake-map-model", "endpoint": "test", "raw_response_sha256": "a" * 64},
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


def _create(app: FastAPI) -> tuple[str, str]:
    status, payload = _request(
        app,
        "POST",
        "/api/life-patterns/sessions",
        body={"consent_to_store_responses": True},
    )
    assert status == 200
    return str(payload["session_id"]), str(payload["resume_token"])


def test_session_token_is_hash_only_and_wrong_token_fails(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    app = create_life_patterns_app(store=store, mapper=FakeMapper())
    session_id, token = _create(app)

    saved = (tmp_path / "patterns" / f"{session_id}.json").read_text(encoding="utf-8")
    assert token not in saved
    assert "token_sha256" in saved

    status, _ = _request(
        app,
        "GET",
        f"/api/life-patterns/sessions/{session_id}?token=definitely-not-the-token",
    )
    assert status == 403


def test_episode_progress_is_descriptive_not_question_completion(tmp_path: Path) -> None:
    app = create_life_patterns_app(
        store=LifePatternsFileStore(tmp_path / "patterns"),
        mapper=FakeMapper(),
    )
    session_id, token = _create(app)

    for title in ("Work choice one", "Work choice two"):
        status, _ = _request(
            app,
            "POST",
            f"/api/life-patterns/sessions/{session_id}/episodes",
            body={
                "token": token,
                "domain": "work_projects",
                "title": title,
                "narrative": "A concrete work episode with enough detail to preserve context.",
                "counterexample": None,
                "input_modality": "typed",
            },
        )
        assert status == 200

    status, payload = _request(
        app,
        "GET",
        f"/api/life-patterns/sessions/{session_id}?token={token}",
    )
    assert status == 200
    progress = cast(dict[str, Any], payload["progress"])
    assert progress["status"] == "descriptive_evidence_coverage_not_completion_denominator"
    rows = {row["area"]: row for row in cast(list[dict[str, Any]], progress["areas"])}
    assert rows["work_projects"]["status"] == "strong"
    assert rows["relationships"]["status"] == "not_started"
    assert "question" not in json.dumps(progress).lower()


def test_map_and_portable_exports_use_only_saved_episode_evidence(tmp_path: Path) -> None:
    mapper = FakeMapper()
    app = create_life_patterns_app(
        store=LifePatternsFileStore(tmp_path / "patterns"),
        mapper=mapper,
    )
    session_id, token = _create(app)

    episodes = (
        (
            "relationships",
            "Starting a relationship",
            "I felt an immediate pull but still took time to see how we handled conflict.",
            "In another relationship I felt no immediate pull and closeness developed slowly.",
        ),
        (
            "work_projects",
            "Starting a business",
            "I compared costs, talked to experienced people, and ran a small test before committing.",
            "One side project began impulsively and worked anyway.",
        ),
    )
    for domain, title, narrative, counterexample in episodes:
        status, _ = _request(
            app,
            "POST",
            f"/api/life-patterns/sessions/{session_id}/episodes",
            body={
                "token": token,
                "domain": domain,
                "title": title,
                "narrative": narrative,
                "counterexample": counterexample,
                "input_modality": "typed",
            },
        )
        assert status == 200

    status, mapped = _request(
        app,
        "POST",
        f"/api/life-patterns/sessions/{session_id}/map",
        body={"token": token},
    )
    assert status == 200
    assert mapper.seen_episodes is not None
    serialized_input = json.dumps(mapper.seen_episodes).lower()
    assert "birth" not in serialized_input
    assert "astrology" not in serialized_input
    assert "human design" not in serialized_input

    status, exported = _request(
        app,
        "GET",
        f"/api/life-patterns/sessions/{session_id}/export?token={token}",
    )
    assert status == 200
    profile = cast(dict[str, Any], exported["profile_json"])
    assert profile["interpretation_boundary"] == "historical_tendencies_not_fixed_traits"
    markdown = str(exported["coaching_markdown"])
    assert "Treat these as evidence-linked historical tendencies" in markdown
    assert "Reversible experiments" in markdown
    assert mapped["life_patterns_map"]["patterns"][0]["status"] == "context_dependent"


def test_map_requires_more_than_one_episode(tmp_path: Path) -> None:
    app = create_life_patterns_app(
        store=LifePatternsFileStore(tmp_path / "patterns"),
        mapper=FakeMapper(),
    )
    session_id, token = _create(app)
    status, _ = _request(
        app,
        "POST",
        f"/api/life-patterns/sessions/{session_id}/episodes",
        body={
            "token": token,
            "domain": "decisions",
            "title": "One decision",
            "narrative": "One episode is not enough evidence for a recurring pattern.",
            "counterexample": None,
            "input_modality": "typed",
        },
    )
    assert status == 200
    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/sessions/{session_id}/map",
        body={"token": token},
    )
    assert status == 409
    assert "at least two" in str(payload["detail"])
