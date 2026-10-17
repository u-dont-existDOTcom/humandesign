"""Ready-only private browser finishing on the original encrypted GPT review."""

from __future__ import annotations

import copy
import secrets
from dataclasses import replace
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from participant.app import create_app
from participant.finish_portal import COOKIE_NAME
from participant.store import digest
from test_gpt_submission_action import (
    auth,
    candidate_record,
    ready_review,
    setup_submission,
)
from test_participant import authority

ROOT = Path(__file__).resolve().parents[3]
CF003 = ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
ORIGIN = "https://testserver"


@pytest.fixture
def flow(tmp_path):
    settings, fake, _, _ = setup_submission(tmp_path)
    source = tmp_path / "cf003_secondary_question_module_v0.json"
    source.write_bytes(CF003.read_bytes())
    settings = replace(settings, public_origin=ORIGIN, secure_cookies=True)
    app = create_app(settings, provider=fake, instrument=authority())
    client = TestClient(app, base_url=ORIGIN)
    return settings, fake, app, client


def issue(client, settings, review_id):
    response = client.post(
        f"/api/gpt/reviews/{review_id}/finish-link",
        headers=auth(settings.submission_token),
    )
    assert response.status_code == 200, response.text
    link = response.json()["finish_url"]
    assert link.startswith(ORIGIN + "/finish#token=")
    assert review_id not in link
    return link.split("#token=")[1]


def exchange(client, token):
    return client.post(
        "/api/finish/exchange",
        headers={"Origin": ORIGIN},
        json={"token": token},
    )


def finished_answers(questions):
    return {
        "confirmed_review": True,
        "submit_to_research": True,
        "answers": [
            {"question_id": item["question_id"], "answer_text": f"Original answer {i}."}
            for i, item in enumerate(questions)
        ],
        "metadata": {
            "rising_sign_previously_known": "unsure",
            "previous_natal_chart_reading": "no",
            "target_information_exposure": "prefer_not_to_say",
        },
    }


def test_complete_ready_review_to_secure_web_finish_without_reinterview(flow):
    s, fake, app, client = flow
    candidate = candidate_record()
    original = copy.deepcopy(candidate["turns"])
    rid = ready_review(client, s, candidate)
    assert fake.count == 0
    health = client.get("/healthz").json()
    assert not health["participant_enabled"]
    assert health["gpt_review_queue_enabled"]

    page = client.get("/finish")
    assert page.status_code == 200
    assert page.headers["cache-control"] == "no-store"
    assert "frame-ancestors 'none'" in page.headers["content-security-policy"]
    assert "Submit and finish" in page.text
    assert client.get("/assets/finish.js").status_code == 200
    assert client.get("/assets/finish.css").status_code == 200
    assert client.get("/api/finish/state").status_code == 401

    url = client.post(f"/api/gpt/reviews/{rid}/finish-link")
    assert url.status_code == 401
    token = issue(client, s, rid)
    assert not token.startswith(rid)
    assert exchange(client, token).status_code == 200
    cookie = client.cookies.get(COOKIE_NAME)
    assert cookie and len(cookie) >= 32
    assert exchange(client, token).status_code == 401  # one-time exchange

    ready = client.get("/api/finish/state")
    assert ready.status_code == 200, ready.text
    data = ready.json()
    assert data["status"] == "ready"
    assert data["original_turn_count"] == 1
    assert data["clarification_count"] == 0
    assert len(data["cf003_questions"]) == 3
    assert not any("purpose" in question for question in data["cf003_questions"])
    assert data["csrf_token"]
    final = finished_answers(data["cf003_questions"])
    assert (
        client.post("/api/finish/submit", headers={"Origin": ORIGIN}, json=final).status_code == 409
    )
    assert (
        client.post(
            "/api/finish/submit",
            headers={"Origin": "https://untrusted.invalid", "X-Finish-CSRF": data["csrf_token"]},
            json=final,
        ).status_code
        == 403
    )
    response = client.post(
        "/api/finish/submit",
        headers={"Origin": ORIGIN, "X-Finish-CSRF": data["csrf_token"]},
        json=final,
    )
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["stored_encrypted"] and receipt["independent_review_completed"]
    stored = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert stored["primary_record"]["turns"] == original
    assert stored["primary_record"]["participant_review"]["confirmed"] is True
    assert stored["primary_record"]["freeze"]["frozen_before_birth_or_chart_reveal"] is True
    assert stored["cf003_record"]["primary_record_sha256"] == receipt["primary_record_sha256"]
    assert [t["question_id"] for t in stored["cf003_record"]["turns"][:3]] == [
        "CF003-ID-01",
        "CF003-CENTRAL-01",
        "CF003-PERIPH-01",
    ]
    assert all(t["turn_role"] == "collection_metadata" for t in stored["cf003_record"]["turns"][3:])
    assert (
        client.get("/api/finish/state").json()["submission"]["submission_id"]
        == receipt["submission_id"]
    )

    retried = client.post(
        "/api/finish/submit",
        headers={"Origin": ORIGIN, "X-Finish-CSRF": data["csrf_token"]},
        json=final,
    )
    assert retried.status_code == 200
    assert retried.json()["duplicate"]
    changed = copy.deepcopy(final)
    changed["answers"][0]["answer_text"] = "Different final answer"
    assert (
        client.post(
            "/api/finish/submit",
            headers={"Origin": ORIGIN, "X-Finish-CSRF": data["csrf_token"]},
            json=changed,
        ).status_code
        == 409
    )
    assert (
        client.post(
            f"/api/gpt/reviews/{rid}/finish-link",
            headers=auth(s.submission_token),
        ).status_code
        == 409
    )
    assert fake.count == 0


def test_saved_queued_review_has_private_portal_but_unknown_review_does_not(flow):
    s, _, app, c = flow
    start = c.post(
        "/api/gpt/reviews",
        headers=auth(s.submission_token),
        json={
            "research_use_consented": True,
            "candidate_record": candidate_record(),
            "request_id": secrets.token_hex(16),
        },
    )
    assert start.status_code == 200
    rid = start.json()["review_id"]
    token = issue(c, s, rid)
    assert exchange(c, token).status_code == 200
    state = c.get("/api/finish/state").json()
    assert state["status"] == "queued"
    assert state["clarification_count"] == 0
    assert "cf003_questions" not in state
    assert (
        c.post(
            "/api/gpt/reviews/R-" + "f" * 32 + "/finish-link",
            headers=auth(s.submission_token),
        ).status_code
        == 409
    )


def test_expiration_replay_and_independent_browser_cookie_isolation(flow):
    s, _, app, c = flow
    rid = ready_review(c, s, candidate_record())
    token = issue(c, s, rid)
    assert exchange(c, token).status_code == 200
    assert c.cookies.get(COOKIE_NAME)
    other = TestClient(app, base_url=ORIGIN)
    assert other.get("/api/finish/state").status_code == 401
    with app.state.store.connection() as db:
        db.execute("UPDATE gpt_finish_sessions SET expires_at=0 WHERE review_id=?", (rid,))
    assert c.get("/api/finish/state").status_code == 401
    token2 = issue(c, s, rid)
    with app.state.store.connection() as db:
        db.execute("UPDATE gpt_finish_links SET expires_at=0 WHERE token_hash=?", (digest(token2),))
    assert exchange(c, token2).status_code == 401
    assert c.get("/api/finish/state").status_code == 401


def test_reloaded_page_rotates_csrf_and_old_page_cannot_submit(flow):
    s, _, app, c = flow
    rid = ready_review(c, s, candidate_record())
    assert exchange(c, issue(c, s, rid)).status_code == 200
    previous = c.get("/api/finish/state").json()
    later = c.get("/api/finish/state").json()
    assert previous["csrf_token"] != later["csrf_token"]
    payload = finished_answers(later["cf003_questions"])
    wrong = c.post(
        "/api/finish/submit",
        headers={"Origin": ORIGIN, "X-Finish-CSRF": previous["csrf_token"]},
        json=payload,
    )
    assert wrong.status_code == 409
    assert (
        c.post(
            "/api/finish/submit",
            headers={"Origin": ORIGIN, "X-Finish-CSRF": later["csrf_token"]},
            json=payload,
        ).status_code
        == 200
    )


@pytest.mark.parametrize(
    "problem",
    [
        "missing_question",
        "duplicate_question",
        "empty_answer",
        "source_birth_leak",
        "unknown_metadata",
    ],
)
def test_malformed_final_answers_do_not_insert_any_submission(flow, problem):
    s, _, app, c = flow
    rid = ready_review(c, s, candidate_record())
    assert exchange(c, issue(c, s, rid)).status_code == 200
    view = c.get("/api/finish/state").json()
    payload = finished_answers(view["cf003_questions"])
    if problem == "missing_question":
        payload["answers"].pop()
    elif problem == "duplicate_question":
        payload["answers"][1]["question_id"] = payload["answers"][0]["question_id"]
    elif problem == "empty_answer":
        payload["answers"][2]["answer_text"] = ""
    elif problem == "source_birth_leak":
        payload["answers"][0]["answer_text"] = "My date of birth is 1980-01-01."
    elif problem == "unknown_metadata":
        payload["metadata"]["rising_sign_previously_known"] = "maybe"
    r = c.post(
        "/api/finish/submit",
        headers={"Origin": ORIGIN, "X-Finish-CSRF": view["csrf_token"]},
        json=payload,
    )
    assert r.status_code == 422, (problem, r.status_code, r.text)
    assert app.state.store.gpt_submission_overview() == []


def test_existing_clarification_history_and_skips_preserved_through_final_storage(flow):
    s, _, app, c = flow
    candidate = candidate_record()
    old_turns = copy.deepcopy(candidate["turns"])
    rid = ready_review(c, s, candidate)
    stored = app.state.store
    history = [
        {
            "question_text": "When is it easier to make a commitment?",
            "route_id": "TF1-G19",
            "route_type": "missing_piece_followup",
            "answer_text": "When I can keep my options open.",
            "answer_status": "answered",
        },
        {
            "question_text": "What changes in a different context?",
            "route_id": "TF1-M11",
            "route_type": "missing_piece_followup",
            "answer_text": None,
            "answer_status": "skipped",
        },
    ]
    with stored.connection() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)).fetchone()
        job = stored.decode(row[0])
        job["clarification_history"] = history
        db.execute("UPDATE gpt_review_jobs SET payload=? WHERE id=?", (stored.encode(job), rid))
        db.commit()
    assert exchange(c, issue(c, s, rid)).status_code == 200
    view = c.get("/api/finish/state").json()
    assert view["clarification_count"] == 2
    form = finished_answers(view["cf003_questions"])
    response = c.post(
        "/api/finish/submit",
        headers={
            "Origin": ORIGIN,
            "X-Finish-CSRF": view["csrf_token"],
        },
        json=form,
    )
    assert response.status_code == 200, response.text
    final = stored.gpt_submission_read(response.json()["submission_id"])
    turns = final["primary_record"]["turns"]
    assert turns[: len(old_turns)] == old_turns
    assert len(turns) == len(old_turns) + 2
    assert turns[-2]["answer_text"] == history[0]["answer_text"]
    assert turns[-2]["question_text"] == history[0]["question_text"]
    assert turns[-1]["answer_text"] is None
    assert turns[-1]["canonical_question_id"] == history[1]["route_id"]
    assert (
        final["cf003_record"]["primary_record_sha256"] == response.json()["primary_record_sha256"]
    )


def test_issue_link_rechecks_terminal_review_after_creation(flow):
    s, _, app, c = flow
    rid = ready_review(c, s, candidate_record())
    raw = issue(c, s, rid)
    with app.state.store.connection() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)).fetchone()
        job = app.state.store.decode(row[0])
        job["status"] = "withdrawn"
        db.execute(
            "UPDATE gpt_review_jobs SET status=?,payload=? WHERE id=?",
            ("withdrawn", app.state.store.encode(job), rid),
        )
        db.commit()
    assert exchange(c, raw).status_code == 409
    assert c.get("/api/finish/state").status_code == 401
    assert (
        c.post(
            f"/api/gpt/reviews/{rid}/finish-link",
            headers=auth(s.submission_token),
        ).status_code
        == 409
    )
