from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from fastapi import FastAPI
from starlette.types import Message, Scope

from hdmatch.api.life_patterns_app import LifePattern, LifePatternsFileStore, LifePatternsMap
from hdmatch.api.life_patterns_interview_app import (
    InterviewerResult,
    create_life_patterns_interview_app,
)
from hdmatch.api.life_patterns_recovery import (
    LifePatternsRecoveryService,
    LifePatternsRecoverySettings,
)


class FakeMapper:
    def build(self, episodes: list[dict[str, Any]]) -> tuple[LifePatternsMap, dict[str, str]]:
        if len(episodes) < 2:
            raise ValueError("at least two saved episodes are required before generating a map")
        return (
            LifePatternsMap(
                overall_summary="The episodes show both recurring and context-dependent patterns.",
                patterns=(
                    LifePattern(
                        pattern_id="P1",
                        title="Context changes the process",
                        summary="The participant uses different approaches in different settings.",
                        status="context_dependent",
                        confidence=0.8,
                        supporting_episode_ids=tuple(str(row["episode_id"]) for row in episodes),
                    ),
                ),
                strengths=("Supplies concrete examples.",),
                friction_points=("Broad summaries can hide context.",),
                transfer_opportunities=("Test one useful strategy in another low-stakes context.",),
                reversible_experiments=("Try one small cross-context experiment.",),
            ),
            {"model": "fake-map", "endpoint": "test", "raw_response_sha256": "a" * 64},
        )


class FakeInterviewer:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def respond(
        self,
        *,
        episodes: list[dict[str, Any]],
        turns: list[dict[str, Any]],
        progress: dict[str, Any],
    ) -> tuple[InterviewerResult, dict[str, str]]:
        self.calls.append({"episodes": episodes, "turns": turns, "progress": progress})
        completed = len(episodes) == 0
        return (
            InterviewerResult(
                reply=(
                    "That gives me a concrete starting point. What was different in a similar "
                    "situation where you did not respond that way?"
                ),
                episode_ready=completed,
                episode_domain="decisions" if completed else None,
                episode_title="A consequential decision" if completed else None,
                episode_narrative=(
                    "The participant described a consequential decision and how it unfolded."
                    if completed
                    else None
                ),
                episode_counterexample=None,
                provisional_insight="The process may change by context." if episodes else None,
                coverage_focus="counterexamples",
            ),
            {"model": "fake-interviewer", "endpoint": "test", "raw_response_sha256": "b" * 64},
        )


class FailingInterviewer:
    def respond(
        self,
        *,
        episodes: list[dict[str, Any]],
        turns: list[dict[str, Any]],
        progress: dict[str, Any],
    ) -> tuple[InterviewerResult, dict[str, str]]:
        del episodes, turns, progress
        raise RuntimeError("provider unavailable")


def _settings() -> LifePatternsRecoverySettings:
    return LifePatternsRecoverySettings(
        smtp_host="smtp.example.test",
        smtp_port=587,
        smtp_security="starttls",
        smtp_username="study@example.test",
        smtp_password="secret",
        from_address="study@example.test",
    )


def _recovery(
    store: LifePatternsFileStore,
    deliveries: list[tuple[str, str]],
) -> LifePatternsRecoveryService:
    def sender(settings: LifePatternsRecoverySettings, recipient: str, otp: str) -> None:
        assert settings.smtp_password == "secret"
        deliveries.append((recipient, otp))

    return LifePatternsRecoveryService(
        store,
        _settings(),
        sender=sender,
        clock=lambda: datetime(2026, 9, 3, 15, 0, tzinfo=UTC),
        otp_factory=lambda: "654321",
        resume_token_factory=lambda: "r" * 43,
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


def _create(app: FastAPI, email: str = "Person@Example.COM") -> tuple[str, str]:
    status, payload = _request(
        app,
        "POST",
        "/api/life-patterns/interview/sessions",
        body={
            "email": email,
            "consent_to_store_responses": True,
            "consent_to_llm_processing": True,
        },
    )
    assert status == 200
    return str(payload["session_id"]), str(payload["resume_token"])


def test_interview_stores_only_email_lookup_hash_and_stays_model_blind(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    interviewer = FakeInterviewer()
    deliveries: list[tuple[str, str]] = []
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=interviewer,
        mapper=FakeMapper(),
        recovery=_recovery(store, deliveries),
    )
    session_id, token = _create(app)
    raw = (tmp_path / "patterns" / f"{session_id}.json").read_text(encoding="utf-8")
    assert "person@example.com" not in raw.casefold()
    assert hashlib.sha256("person@example.com".encode()).hexdigest() in raw

    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={
            "token": token,
            "message": "I took weeks comparing two career options before choosing one.",
            "input_modality": "typed",
        },
    )
    assert status == 200
    assert payload["episode_saved"] is True
    assert len(interviewer.calls) == 1
    serialized = json.dumps(interviewer.calls[0]).casefold()
    for forbidden in (
        "birth",
        "astrology",
        "human design",
        "candidate_state",
        "chart",
        "model_fit",
        "rank",
    ):
        assert forbidden not in serialized


def test_user_turn_is_durable_even_when_interviewer_provider_fails(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FailingInterviewer(),
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={
            "token": token,
            "message": "This matters and should not disappear if the AI call fails.",
            "input_modality": "typed",
        },
    )
    assert status == 502
    assert "saved" in str(payload["detail"]).casefold()
    stored = store.read(session_id, token)
    turns = cast(list[dict[str, Any]], stored["conversation_turns"])
    assert turns[-1]["role"] == "user"
    assert "should not disappear" in str(turns[-1]["text"])


def test_provisional_insight_waits_for_multiple_completed_episodes(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    interviewer = FakeInterviewer()
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=interviewer,
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    status, first = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={"token": token, "message": "First real decision episode.", "input_modality": "typed"},
    )
    assert status == 200
    assert first["provisional_insight"] is None

    payload = store.read(session_id, token)
    episodes = cast(list[dict[str, Any]], payload["episodes"])
    episodes.append(
        {
            "episode_id": "EP-SECOND",
            "domain": "relationships",
            "title": "Second episode",
            "narrative": "A contrasting relationship episode.",
            "counterexample": None,
            "input_modality": "typed",
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
    )
    store.save(payload)
    status, second = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={"token": token, "message": "Here is another contrast.", "input_modality": "typed"},
    )
    assert status == 200
    assert second["provisional_insight"] == "The process may change by context."


def test_email_otp_recovery_hashes_otp_and_rotates_resume_token(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    deliveries: list[tuple[str, str]] = []
    recovery = _recovery(store, deliveries)
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=FakeMapper(),
        recovery=recovery,
    )
    session_id, old_token = _create(app, "person@example.com")

    status, request_payload = _request(
        app,
        "POST",
        "/api/life-patterns/interview/recovery/request",
        body={"email": "person@example.com"},
    )
    assert status == 200
    assert request_payload["status"] == "accepted"
    assert deliveries == [("person@example.com", "654321")]
    raw = (tmp_path / "patterns" / f"{session_id}.json").read_text(encoding="utf-8")
    assert "654321" not in raw

    status, recovered = _request(
        app,
        "POST",
        "/api/life-patterns/interview/recovery/verify",
        body={"email": "person@example.com", "otp": "654321"},
    )
    assert status == 200
    assert recovered["resume_token"] == "r" * 43

    status, _ = _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}?token={old_token}",
    )
    assert status == 403
    status, _ = _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}?token={'r' * 43}",
    )
    assert status == 200


def test_export_declares_inner_signal_read_only_initial_policy(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    payload = store.read(session_id, token)
    payload["episodes"] = [
        {
            "episode_id": "EP-1",
            "domain": "decisions",
            "title": "One",
            "narrative": "First episode.",
            "counterexample": None,
            "input_modality": "typed",
            "created_at_utc": datetime.now(UTC).isoformat(),
        },
        {
            "episode_id": "EP-2",
            "domain": "relationships",
            "title": "Two",
            "narrative": "Second episode.",
            "counterexample": None,
            "input_modality": "typed",
            "created_at_utc": datetime.now(UTC).isoformat(),
        },
    ]
    mapped, _ = FakeMapper().build(cast(list[dict[str, Any]], payload["episodes"]))
    payload["life_patterns_map"] = mapped.model_dump(mode="json")
    store.save(payload)

    status, exported = _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}/export?token={token}",
    )
    assert status == 200
    policy = cast(dict[str, Any], exported["profile_json"])["integration_policy"]
    assert policy["readable_by_coaching_or_inner_signal_with_user_consent"] is True
    assert policy["downstream_apps_must_not_silently_rewrite_research_evidence"] is True
