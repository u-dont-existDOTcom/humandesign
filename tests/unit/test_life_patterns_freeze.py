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
from hdmatch.api.life_patterns_freeze import (
    _sha256_json,
    register_life_patterns_freeze_routes,
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


def _ready_session(tmp_path: Path) -> tuple[LifePatternsFileStore, FastAPI, str, str]:
    store = LifePatternsFileStore(tmp_path / "patterns")
    payload, token = store.create()
    now = datetime(2026, 9, 3, 16, 0, tzinfo=UTC).isoformat()
    payload["consent_to_llm_processing"] = True
    payload["conversation_turns"] = [
        {
            "turn_id": "TURN-A",
            "role": "user",
            "text": "In one career decision I gathered information for weeks before acting.",
            "input_modality": "typed",
            "created_at_utc": now,
        },
        {
            "turn_id": "TURN-B",
            "role": "user",
            "text": "In a relationship decision I acted quickly because the situation was urgent.",
            "input_modality": "voice",
            "created_at_utc": now,
        },
        {
            "turn_id": "TURN-AI",
            "role": "assistant",
            "text": "What was different between those situations?",
            "created_at_utc": now,
        },
    ]
    base = {
        "counterexample": None,
        "participant_revision": False,
        "reviewed_at_utc": now,
        "created_at_utc": now,
    }
    payload["episodes"] = [
        {
            **base,
            "episode_id": "EP-A",
            "domain": "work_projects",
            "title": "Career choice",
            "narrative": "The participant gathered information for weeks before committing.",
            "input_modality": "typed",
            "source_turn_ids": ["TURN-A"],
            "review_status": "approved",
        },
        {
            **base,
            "episode_id": "EP-B",
            "domain": "relationships",
            "title": "Urgent relationship choice",
            "narrative": "The participant acted quickly in an urgent relationship situation.",
            "input_modality": "voice",
            "source_turn_ids": ["TURN-B"],
            "review_status": "approved",
        },
        {
            **base,
            "episode_id": "EP-PENDING",
            "domain": "decisions",
            "title": "Pending summary",
            "narrative": "This has not been approved.",
            "input_modality": "typed",
            "source_turn_ids": [],
            "review_status": "pending",
            "reviewed_at_utc": None,
        },
        {
            **base,
            "episode_id": "EP-REJECTED",
            "domain": "other",
            "title": "Rejected summary",
            "narrative": "This was rejected.",
            "input_modality": "typed",
            "source_turn_ids": [],
            "review_status": "rejected",
        },
    ]
    life_map = LifePatternsMap(
        overall_summary="The examples differ by context.",
        patterns=(
            LifePattern(
                pattern_id="P1",
                title="Information gathering varies by context",
                summary="The participant sometimes gathers information extensively before commitment.",
                status="context_dependent",
                confidence=0.82,
                supporting_episode_ids=("EP-A",),
                counterexample_episode_ids=("EP-B",),
                contexts=("career", "relationship"),
                limits=("Urgency may change the process.",),
            ),
            LifePattern(
                pattern_id="P2",
                title="Urgency changes timing",
                summary="Urgent situations may shorten the time from first reaction to action.",
                status="tentative",
                confidence=0.65,
                supporting_episode_ids=("EP-B",),
                counterexample_episode_ids=(),
                contexts=("urgent situations",),
                limits=("Only one clear urgent example is currently available.",),
            ),
        ),
        strengths=("Can give detailed examples.",),
        friction_points=("Broad self-descriptions can hide context.",),
        transfer_opportunities=("Try career-style experiments in relationships.",),
        reversible_experiments=("Run a low-stakes timing experiment.",),
        important_unknowns=("Whether the urgency pattern repeats outside relationships.",),
    )
    payload["life_patterns_map"] = life_map.model_dump(mode="json")
    payload["map_provider_receipt"] = {
        "model": "fake-map",
        "endpoint": "test",
        "raw_response_sha256": "a" * 64,
    }
    payload["map_approved_episode_ids"] = ["EP-A", "EP-B"]
    store.save(payload)
    app = FastAPI()
    register_life_patterns_freeze_routes(app, store=store)
    return store, app, str(payload["session_id"]), token


def _candidate(app: FastAPI, session_id: str, token: str) -> dict[str, Any]:
    status, candidate = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/freeze-candidate",
        body={"token": token},
    )
    assert status == 200
    return candidate


def _review(
    app: FastAPI,
    session_id: str,
    token: str,
    candidate_id: str,
    claim_id: str,
    **body: Any,
) -> tuple[int, dict[str, Any]]:
    return _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/freeze-candidates/"
        f"{candidate_id}/claims/{claim_id}/review",
        body={"token": token, **body},
    )


def _finalize(
    app: FastAPI,
    session_id: str,
    token: str,
    candidate_id: str,
    *,
    reviewed: bool = True,
    immutable: bool = True,
) -> tuple[int, dict[str, Any]]:
    return _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/freeze-candidates/"
        f"{candidate_id}/finalize",
        body={
            "token": token,
            "attest_profile_reviewed": reviewed,
            "attest_snapshot_immutable": immutable,
        },
    )


def test_candidate_is_current_neutral_and_idempotent(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    first = _candidate(app, session_id, token)
    second = _candidate(app, session_id, token)
    assert first["candidate_id"] == second["candidate_id"]
    assert first["candidate_sha256"] == second["candidate_sha256"]
    assert first["claim_count"] == 2
    assert first["review_complete"] is False

    stored = store.read(session_id, token)
    candidates = cast(list[dict[str, Any]], stored["behavioral_freeze_candidates"])
    assert len(candidates) == 1
    source = cast(dict[str, Any], candidates[0]["source"])
    assert [row["episode_id"] for row in source["approved_episodes"]] == ["EP-A", "EP-B"]
    assert [row["turn_id"] for row in source["participant_source_turns"]] == ["TURN-A", "TURN-B"]
    assert source["evidence_coverage"]["semantics"] == "descriptive_evidence_coverage_not_completion_denominator"
    serialized = json.dumps(source, ensure_ascii=False)
    assert "Try career-style experiments in relationships" not in serialized
    assert "Run a low-stakes timing experiment" not in serialized
    assert "Can give detailed examples" not in serialized
    assert "Broad self-descriptions can hide context" not in serialized


def test_candidate_fails_closed_when_map_is_stale(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    payload = store.read(session_id, token)
    payload["map_approved_episode_ids"] = ["EP-A"]
    store.save(payload)
    status, response = _request(
        app,
        "POST",
        f"/api/life-patterns/interview/sessions/{session_id}/freeze-candidate",
        body={"token": token},
    )
    assert status == 409
    assert "older than the approved evidence" in response["detail"]


def test_review_events_are_append_only_and_edits_are_new_review_data(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    candidate = _candidate(app, session_id, token)
    candidate_id = str(candidate["candidate_id"])

    status, _ = _review(
        app,
        session_id,
        token,
        candidate_id,
        "P1",
        action="approve",
    )
    assert status == 200
    status, updated = _review(
        app,
        session_id,
        token,
        candidate_id,
        "P1",
        action="edit",
        title="My corrected pattern",
        summary="I gather information extensively when I have time, but urgency changes the process.",
        status="mixed",
    )
    assert status == 200
    p1 = next(row for row in updated["claims"] if row["claim_id"] == "P1")
    assert p1["latest_review"]["action"] == "edit"
    assert p1["latest_review"]["new_data_during_review"] is True

    stored = store.read(session_id, token)
    record = cast(list[dict[str, Any]], stored["behavioral_freeze_candidates"])[0]
    events = cast(list[dict[str, Any]], record["review_events"])
    assert [row["action"] for row in events] == ["approve", "edit"]
    original = cast(dict[str, Any], record["source"])["claims"][0]
    assert original["title"] == "Information gathering varies by context"
    assert original["summary"].startswith("The participant sometimes")


def test_finalization_requires_complete_review_and_explicit_attestation(tmp_path: Path) -> None:
    _, app, session_id, token = _ready_session(tmp_path)
    candidate = _candidate(app, session_id, token)
    candidate_id = str(candidate["candidate_id"])
    status, _ = _review(app, session_id, token, candidate_id, "P1", action="approve")
    assert status == 200

    status, response = _finalize(app, session_id, token, candidate_id)
    assert status == 409
    assert response["detail"] == "review every claim before freezing"

    status, _ = _review(app, session_id, token, candidate_id, "P2", action="uncertain")
    assert status == 200
    status, response = _finalize(
        app,
        session_id,
        token,
        candidate_id,
        reviewed=True,
        immutable=False,
    )
    assert status == 400
    assert "explicit participant review" in response["detail"]


def test_freeze_hash_is_reproducible_and_artifact_never_changes(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    candidate = _candidate(app, session_id, token)
    candidate_id = str(candidate["candidate_id"])
    status, _ = _review(app, session_id, token, candidate_id, "P1", action="approve")
    assert status == 200
    status, _ = _review(
        app,
        session_id,
        token,
        candidate_id,
        "P2",
        action="edit",
        summary="When a situation is truly urgent, I may move quickly even if I usually gather more information.",
        status="context_dependent",
    )
    assert status == 200
    status, frozen = _finalize(app, session_id, token, candidate_id)
    assert status == 200
    receipt = cast(dict[str, Any], frozen["freeze_receipt"])
    artifact_path = store.root / str(receipt["artifact_relpath"])
    before = artifact_path.read_bytes()
    artifact = cast(dict[str, Any], json.loads(before))
    assert artifact["freeze_id"] == receipt["freeze_id"]
    assert artifact["freeze_sha256"] == receipt["freeze_sha256"]
    assert _sha256_json(artifact["payload"]) == receipt["freeze_sha256"]

    review = cast(dict[str, Any], artifact["payload"])["participant_review"]
    assert review["admissible_claim_ids"] == ["P1", "P2"]
    p2 = next(row for row in review["effective_claims"] if row["claim_id"] == "P2")
    assert p2["original_synthesis"]["title"] == "Urgency changes timing"
    assert p2["effective_review"]["new_data_during_review"] is True
    assert p2["final_participant_claim"]["participant_revision"] is True
    assert p2["final_participant_claim"]["status"] == "context_dependent"
    source = artifact["payload"]["behavioral_source"]
    assert [row["episode_id"] for row in source["approved_episodes"]] == ["EP-A", "EP-B"]
    assert artifact["payload"]["future_model_binding"]["separate_model_analysis_authorization_required"] is True

    status, response = _review(app, session_id, token, candidate_id, "P1", action="reject")
    assert status == 409
    assert response["detail"] == "this behavioral freeze is already final"

    live = store.read(session_id, token)
    cast(list[dict[str, Any]], live["episodes"]).append(
        {
            "episode_id": "EP-LATER",
            "domain": "decisions",
            "title": "Later evidence",
            "narrative": "This happened after the frozen research snapshot.",
            "counterexample": None,
            "input_modality": "typed",
            "source_turn_ids": [],
            "review_status": "approved",
            "participant_revision": False,
            "reviewed_at_utc": datetime.now(UTC).isoformat(),
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
    )
    live["life_patterns_map"] = None
    live["map_provider_receipt"] = None
    live["map_approved_episode_ids"] = []
    store.save(live)
    assert artifact_path.read_bytes() == before


def test_rejected_and_uncertain_claims_are_audited_but_not_admissible(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    candidate = _candidate(app, session_id, token)
    candidate_id = str(candidate["candidate_id"])
    status, _ = _review(
        app,
        session_id,
        token,
        candidate_id,
        "P1",
        action="reject",
        note="This overgeneralizes the work example.",
    )
    assert status == 200
    status, _ = _review(
        app,
        session_id,
        token,
        candidate_id,
        "P2",
        action="uncertain",
        note="I need more examples before calling this a pattern.",
    )
    assert status == 200
    status, frozen = _finalize(app, session_id, token, candidate_id)
    assert status == 200
    receipt = cast(dict[str, Any], frozen["freeze_receipt"])
    artifact = json.loads((store.root / receipt["artifact_relpath"]).read_text(encoding="utf-8"))
    review = artifact["payload"]["participant_review"]
    assert review["admissible_claim_ids"] == []
    assert [row["effective_review"]["action"] for row in review["effective_claims"]] == [
        "reject",
        "uncertain",
    ]
    assert all(row["final_participant_claim"] is None for row in review["effective_claims"])


def test_finalization_rejects_candidate_after_live_evidence_changes(tmp_path: Path) -> None:
    store, app, session_id, token = _ready_session(tmp_path)
    candidate = _candidate(app, session_id, token)
    candidate_id = str(candidate["candidate_id"])
    for claim_id in ("P1", "P2"):
        status, _ = _review(app, session_id, token, candidate_id, claim_id, action="approve")
        assert status == 200

    payload = store.read(session_id, token)
    cast(list[dict[str, Any]], payload["episodes"]).append(
        {
            "episode_id": "EP-NEW",
            "domain": "decisions",
            "title": "New approved episode",
            "narrative": "New evidence arrived while the candidate was being reviewed.",
            "counterexample": None,
            "input_modality": "typed",
            "source_turn_ids": [],
            "review_status": "approved",
            "participant_revision": False,
            "reviewed_at_utc": datetime.now(UTC).isoformat(),
            "created_at_utc": datetime.now(UTC).isoformat(),
        }
    )
    payload["map_approved_episode_ids"] = ["EP-A", "EP-B", "EP-NEW"]
    store.save(payload)

    status, response = _finalize(app, session_id, token, candidate_id)
    assert status == 409
    assert "live evidence changed" in response["detail"] or "older than the approved evidence" in response["detail"]
