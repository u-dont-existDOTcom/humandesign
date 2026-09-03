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
from hdmatch.api.life_patterns_interview_app import InterviewerResult, create_life_patterns_interview_app
from hdmatch.api.life_patterns_recovery import LifePatternsRecoveryService, LifePatternsRecoverySettings


class FakeMapper:
    def __init__(self) -> None:
        self.seen: list[dict[str, Any]] | None = None

    def build(self, episodes: list[dict[str, Any]]) -> tuple[LifePatternsMap, dict[str, str]]:
        self.seen = episodes
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
        first = not episodes
        return (
            InterviewerResult(
                reply="That gives me a concrete example. What was different in a similar case?",
                episode_ready=first,
                episode_domain="decisions" if first else None,
                episode_title="A consequential decision" if first else None,
                episode_narrative="The participant described how one decision unfolded." if first else None,
                episode_counterexample=None,
                provisional_insight="The process may change by context." if episodes else None,
                coverage_focus="counterexamples",
            ),
            {"model": "fake", "endpoint": "test", "raw_response_sha256": "b" * 64},
        )


class FailingInterviewer:
    def respond(self, **_: Any) -> tuple[InterviewerResult, dict[str, str]]:
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


def _recovery(store: LifePatternsFileStore, deliveries: list[tuple[str, str]]) -> LifePatternsRecoveryService:
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
        "/api/life-patterns/interview/sessions",
        body={
            "email": "Person@Example.COM",
            "consent_to_store_responses": True,
            "consent_to_llm_processing": True,
        },
    )
    assert status == 200
    return str(payload["session_id"]), str(payload["resume_token"])


def _approve(app: FastAPI, session_id: str, token: str, episode_id: str) -> dict[str, Any]:
    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/episodes/{episode_id}/review",
        body={"token": token, "action": "approve"},
    )
    assert status == 200
    return payload


def test_interviewer_is_model_blind_and_email_is_hash_only(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    interviewer = FakeInterviewer()
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=interviewer,
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    raw = (tmp_path / "patterns" / f"{session_id}.json").read_text(encoding="utf-8")
    assert "person@example.com" not in raw.casefold()
    assert hashlib.sha256(b"person@example.com").hexdigest() in raw

    status, payload = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={"token": token, "message": "I compared two careers for weeks.", "input_modality": "typed"},
    )
    assert status == 200
    assert payload["episode_saved"] is True
    assert payload["episode"]["review_status"] == "pending"
    assert payload["progress"]["episode_count"] == 0
    serialized = json.dumps(interviewer.calls[0]).casefold()
    for forbidden in ("birth", "astrology", "human design", "candidate_state", "chart", "model_fit", "rank"):
        assert forbidden not in serialized


def test_pending_episode_requires_participant_review_before_evidence_use(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    mapper = FakeMapper()
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=mapper,
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    status, turn = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={"token": token, "message": "A concrete decision episode.", "input_modality": "typed"},
    )
    assert status == 200
    episode_id = str(turn["episode"]["episode_id"])
    assert turn["progress"]["provisional_episode_count"] == 1
    assert turn["map_available"] is False

    status, _ = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/map",
        body={"token": token},
    )
    assert status == 409
    assert mapper.seen == []

    reviewed = _approve(app, session_id, token, episode_id)
    assert reviewed["episode"]["review_status"] == "approved"
    assert reviewed["progress"]["episode_count"] == 1
    assert reviewed["progress"]["provisional_episode_count"] == 0


def test_participant_can_edit_or_reject_ai_episode_summary(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=FakeMapper(),
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    status, turn = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/turns",
        body={"token": token, "message": "A story the AI may oversimplify.", "input_modality": "typed"},
    )
    assert status == 200
    episode_id = str(turn["episode"]["episode_id"])
    status, edited = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/episodes/{episode_id}/review",
        body={
            "token": token,
            "action": "edit",
            "domain": "work_projects",
            "title": "My corrected title",
            "narrative": "This is what I actually meant, preserving the context I care about.",
            "counterexample": "There was also a case where I acted differently.",
        },
    )
    assert status == 200
    episode = cast(dict[str, Any], edited["episode"])
    assert episode["review_status"] == "approved"
    assert episode["participant_revision"] is True
    assert episode["domain"] == "work_projects"
    assert episode["title"] == "My corrected title"

    payload = store.read(session_id, token)
    episodes = cast(list[dict[str, Any]], payload["episodes"])
    episodes.append(
        {
            "episode_id": "EP-REJECT",
            "domain": "other",
            "title": "Bad summary",
            "narrative": "Incorrect.",
            "counterexample": None,
            "input_modality": "typed",
            "source_turn_ids": [],
            "review_status": "pending",
            "participant_revision": False,
            "reviewed_at_utc": None,
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
    )
    store.save(payload)
    status, rejected = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/episodes/EP-REJECT/review",
        body={"token": token, "action": "reject"},
    )
    assert status == 200
    assert rejected["episode"]["review_status"] == "rejected"
    assert rejected["progress"]["rejected_episode_count"] == 1
    assert rejected["progress"]["episode_count"] == 1


def test_map_and_export_use_only_participant_approved_episodes(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    mapper = FakeMapper()
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=mapper,
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    payload = store.read(session_id, token)
    base = {
        "counterexample": None,
        "input_modality": "typed",
        "source_turn_ids": [],
        "participant_revision": False,
        "reviewed_at_utc": datetime.now(UTC).isoformat(),
        "created_at_utc": datetime.now(UTC).isoformat(),
    }
    payload["episodes"] = [
        {**base, "episode_id": "EP-A", "domain": "decisions", "title": "Approved A", "narrative": "First approved episode.", "review_status": "approved"},
        {**base, "episode_id": "EP-B", "domain": "relationships", "title": "Approved B", "narrative": "Second approved episode.", "review_status": "approved"},
        {**base, "episode_id": "EP-P", "domain": "work_projects", "title": "Pending", "narrative": "Not yet accepted.", "review_status": "pending", "reviewed_at_utc": None},
        {**base, "episode_id": "EP-R", "domain": "other", "title": "Rejected", "narrative": "Rejected evidence.", "review_status": "rejected"},
    ]
    store.save(payload)

    status, _ = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/map",
        body={"token": token},
    )
    assert status == 200
    assert mapper.seen is not None
    assert [row["episode_id"] for row in mapper.seen] == ["EP-A", "EP-B"]

    status, exported = _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}/export?token={token}",
    )
    assert status == 200
    profile = cast(dict[str, Any], exported["profile_json"])
    assert profile["evidence_episode_ids"] == ["EP-A", "EP-B"]
    assert profile["evidence_policy"] == "participant_approved_episodes_only"


def test_user_turn_survives_provider_failure(tmp_path: Path) -> None:
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
        body={"token": token, "message": "Do not lose this turn.", "input_modality": "typed"},
    )
    assert status == 502
    assert "saved" in str(payload["detail"]).casefold()
    turns = cast(list[dict[str, Any]], store.read(session_id, token)["conversation_turns"])
    assert turns[-1]["role"] == "user"
    assert turns[-1]["text"] == "Do not lose this turn."


def test_otp_recovery_hashes_code_and_rotates_token(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    deliveries: list[tuple[str, str]] = []
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=FakeMapper(),
        recovery=_recovery(store, deliveries),
    )
    session_id, old_token = _create(app)
    status, _ = _request(
        app,
        "POST",
        "/api/life-patterns/interview/recovery/request",
        body={"email": "person@example.com"},
    )
    assert status == 200
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
    new_token = str(recovered["resume_token"])
    assert new_token == "r" * 43
    assert _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}?token={old_token}",
    )[0] == 403
    assert _request(
        app,
        "GET",
        f"/api/life-patterns/interview/sessions/{session_id}?token={new_token}",
    )[0] == 200


def test_inner_signal_export_is_consent_read_only_policy(tmp_path: Path) -> None:
    store = LifePatternsFileStore(tmp_path / "patterns")
    mapper = FakeMapper()
    app = create_life_patterns_interview_app(
        store=store,
        interviewer=FakeInterviewer(),
        mapper=mapper,
        recovery=LifePatternsRecoveryService(store, None),
    )
    session_id, token = _create(app)
    payload = store.read(session_id, token)
    now = datetime.now(UTC).isoformat()
    payload["episodes"] = [
        {"episode_id": "EP-1", "domain": "decisions", "title": "One", "narrative": "First.", "counterexample": None, "input_modality": "typed", "source_turn_ids": [], "review_status": "approved", "participant_revision": False, "reviewed_at_utc": now, "created_at_utc": now},
        {"episode_id": "EP-2", "domain": "relationships", "title": "Two", "narrative": "Second.", "counterexample": None, "input_modality": "typed", "source_turn_ids": [], "review_status": "approved", "participant_revision": False, "reviewed_at_utc": now, "created_at_utc": now},
    ]
    mapped, _ = mapper.build(cast(list[dict[str, Any]], payload["episodes"]))
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
