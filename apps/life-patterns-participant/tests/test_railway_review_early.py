"""Participant-controlled early Railway review: no GPT check-in loops."""

from __future__ import annotations

import copy
import secrets
from dataclasses import replace

from fastapi.testclient import TestClient
from participant.app import create_app
from participant.fast_review import PROTOCOL, run_fast_review
from test_gpt_submission_action import (
    auth,
    candidate_record,
    setup_submission,
)
from test_participant import Fake, authority

ORIGIN = "https://testserver"


def setup_early(tmp_path):
    settings, _, _, _ = setup_submission(tmp_path)
    settings = replace(
        settings,
        fast_review_enabled=True,
        public_origin=ORIGIN,
        secure_cookies=True,
    )
    app = create_app(settings, provider=Fake(), instrument=authority())
    client = TestClient(app, base_url=ORIGIN)
    candidate = candidate_record()
    started = client.post(
        "/api/gpt/reviews",
        headers=auth(settings.submission_token),
        json={
            "candidate_record": candidate,
            "research_use_consented": True,
            "request_id": secrets.token_hex(16),
            "review_protocol": PROTOCOL,
        },
    )
    assert started.status_code == 200, started.text
    return settings, app, client, candidate, started.json()["review_id"]


def portal(client, settings, rid):
    url = client.post(
        f"/api/gpt/reviews/{rid}/finish-link",
        headers=auth(settings.submission_token),
    )
    assert url.status_code == 200, url.text
    assert url.json()["ready_review_required"] is False
    token = url.json()["finish_url"].split("#token=")[1]
    exchange = client.post(
        "/api/finish/exchange",
        headers={"Origin": ORIGIN},
        json={"token": token},
    )
    assert exchange.status_code == 200
    state = client.get("/api/finish/state")
    assert state.status_code == 200, state.text
    return state.json()


def fake_question(app, rid, route="TF1-M11"):
    store = app.state.store
    batch_id = "B-" + secrets.token_hex(16)
    question = {
        "clarification_id": "Q-" + secrets.token_hex(16),
        "route_id": route,
        "route_type": "missing_piece_followup",
        "question_text": "When you hesitate, what, if anything, determines the next action?",
        "participant_purpose": "a synthetic unresolved difference",
        "antecedent_turn_ids": ["t1"],
    }
    with store.connection() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)).fetchone()
        job = store.decode(row[0])
        job.update(
            status="clarification_needed",
            pending_clarification=question,
            pending_clarifications=[question],
            pending_batch_id=batch_id,
        )
        db.execute(
            "UPDATE gpt_review_jobs SET payload=?,status=? WHERE id=?",
            (store.encode(job), "clarification_needed", rid),
        )
        db.commit()
    return batch_id, question


def post(client, path, csrf, body):
    return client.post(
        path,
        headers={
            "Origin": ORIGIN,
            "X-Finish-CSRF": csrf,
        },
        json=body,
    )


def test_queued_review_redeems_early_and_requires_no_gpt_checkins(tmp_path):
    settings, app, c, candidate, rid = setup_early(tmp_path)
    first = portal(c, settings, rid)
    assert first["status"] == "queued"
    assert first["clarifications"] == []
    assert first["clarification_count"] == 0
    assert first["clarification_progress"]["overall_clarifications_remaining"] is None
    assert not first["clarification_intake_closed"]
    assert "cf003_questions" not in first
    assert c.get("/api/finish/state").status_code == 200
    assert post(c, "/api/finish/submit", first["csrf_token"], {}).status_code == 422
    assert app.state.store.gpt_submission_overview() == []


def test_railway_accepts_exact_admitted_batch_then_preserves_answer(tmp_path):
    settings, app, c, source, rid = setup_early(tmp_path)
    portal(c, settings, rid)
    batch_id, q = fake_question(app, rid)
    data = c.get("/api/finish/state").json()
    assert data["status"] == "clarification_needed"
    assert data["batch_id"] == batch_id
    assert data["clarifications"][0]["question_text"] == q["question_text"]
    assert data["clarification_progress"]["current_batch_only"]
    body = {
        "batch_id": batch_id,
        "operation_id": secrets.token_hex(16),
        "answers": [
            {
                "clarification_id": q["clarification_id"],
                "answer_text": "I follow up when I understand the details.",
                "skipped": False,
            }
        ],
    }
    out = post(c, "/api/finish/clarification-batches", data["csrf_token"], body)
    assert out.status_code == 200, out.text
    assert out.json()["status"] == "queued"
    saved = app.state.store.gpt_review_read(rid)
    assert saved["candidate_record"] == source
    assert len(saved["clarification_history"]) == 1
    assert saved["clarification_history"][0]["answer_text"] == body["answers"][0]["answer_text"]
    # Exact retry is idempotent even after the review is requeued.
    again = post(c, "/api/finish/clarification-batches", data["csrf_token"], body)
    assert again.status_code == 200
    assert len(app.state.store.gpt_review_read(rid)["clarification_history"]) == 1
    assert c.get("/api/finish/state").json()["clarification_count"] == 1


def test_close_intake_saves_all_prior_source_and_declines_unanswered_questions(tmp_path):
    settings, app, c, candidate, rid = setup_early(tmp_path)
    portal(c, settings, rid)
    batch_id, q = fake_question(app, rid)
    data = c.get("/api/finish/state").json()
    original = copy.deepcopy(app.state.store.gpt_review_read(rid)["candidate_record"])
    assert (
        post(
            c,
            "/api/finish/close-clarifications",
            "no-csrf",
            {
                "confirm_no_more_questions": True,
            },
        ).status_code
        == 409
    )
    closed = post(
        c,
        "/api/finish/close-clarifications",
        data["csrf_token"],
        {
            "confirm_no_more_questions": True,
        },
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["clarification_intake_closed"]
    review = app.state.store.gpt_review_read(rid)
    assert review["candidate_record"] == original
    assert review["status"] == "queued"
    assert review["clarification_intake_closed"] is True
    assert len(review["clarification_history"]) == 1
    item = review["clarification_history"][0]
    assert item["answer_status"] == "skipped"
    assert item["answer_text"] is None
    assert item["question_text"] == q["question_text"]
    assert item["skip_reason"] == "participant_declined_further_clarifications"
    assert review.get("pending_clarifications") == []
    summary = c.get("/api/finish/state").json()
    assert summary["clarifications"] == []
    assert summary["clarification_intake_closed"]
    assert summary["status"] != "ready"
    assert (
        post(
            c,
            "/api/finish/clarification-batches",
            summary["csrf_token"],
            {
                "batch_id": batch_id,
                "operation_id": secrets.token_hex(16),
                "answers": [
                    {
                        "clarification_id": q["clarification_id"],
                        "answer_text": "I changed my mind",
                        "skipped": False,
                    }
                ],
            },
        ).status_code
        == 409
    )


def test_close_intake_invalidates_running_worker_lease(tmp_path):
    s, app, c, _, rid = setup_early(tmp_path)
    portal(c, s, rid)
    claimed = app.state.store.claim_gpt_review()
    assert claimed["status"] == "processing"
    token = claimed["claim_id"]
    data = c.get("/api/finish/state").json()
    close = post(
        c,
        "/api/finish/close-clarifications",
        data["csrf_token"],
        {"confirm_no_more_questions": True},
    )
    assert close.status_code == 200
    assert app.state.store.gpt_review_read(rid)["status"] == "queued"
    from participant.store import Conflict

    try:
        app.state.store.renew_gpt_review(rid, token)
    except Conflict:
        pass
    else:
        raise AssertionError("Old worker claim remained valid after participant stopped questions")


def test_closed_intake_bypasses_fast_gap_generation_and_forbids_new_questions(tmp_path):
    s, app, c, original, rid = setup_early(tmp_path)
    portal(c, s, rid)
    data = c.get("/api/finish/state").json()
    assert (
        post(
            c,
            "/api/finish/close-clarifications",
            data["csrf_token"],
            {"confirm_no_more_questions": True},
        ).status_code
        == 200
    )
    job = app.state.store.gpt_review_read(rid)
    instrument = authority()
    version = app.state.store.pin_instrument(instrument)
    calls = []

    def final_only(prepared, provider):
        state = prepared["worker_state"]
        calls.append(state)
        assert state["review_only"] is True
        assert state["phase"] == "ready"
        assert state["pending_question"] is None
        assert state["turns"][0]["answer_text"] == original["turns"][0]["answer_text"]
        return "ready", {"instrument_version": version}, state, None

    status, receipt, saved, question = run_fast_review(job, Fake(), instrument, version, final_only)
    assert status == "ready"
    assert receipt["participant_declined_further_clarifications"] is True
    assert receipt["final_review_completed"] is True
    assert saved["fast_review"]["participant_declined_further_clarifications"]
    assert question is None
    assert len(calls) == 1

    def illegal_question(prepared, provider):
        return "clarification_needed", {}, prepared["worker_state"], {"question_text": "again"}

    import pytest

    with pytest.raises(RuntimeError, match="cannot_produce_new_question"):
        run_fast_review(job, Fake(), instrument, version, illegal_question)


def test_real_synthetic_independent_full_review_after_participant_ends_questions(tmp_path):
    """No fake ready state: the existing Engine still performs evidence admission."""
    from test_gpt_submission_action import load_worker_module

    settings, app, client, source, rid = setup_early(tmp_path)
    portal(client, settings, rid)
    state = client.get("/api/finish/state").json()
    assert (
        post(
            client,
            "/api/finish/close-clarifications",
            state["csrf_token"],
            {"confirm_no_more_questions": True},
        ).status_code
        == 200
    )
    job = app.state.store.gpt_review_read(rid)
    worker = load_worker_module()
    instrument = authority()
    version = app.state.store.pin_instrument(instrument)

    def actual_legacy(prepared, provider):
        return worker.run_legacy_review(prepared, provider=provider)

    status, receipt, saved, question = run_fast_review(
        job, Fake(), instrument, version, actual_legacy
    )
    assert status == "ready", (status, receipt)
    assert receipt["participant_declined_further_clarifications"]
    assert saved["review_only"] is True
    assert question is None
    assert saved["phase"] == "review"


def test_legacy_saved_review_can_decline_further_questions_without_fake_ready(tmp_path):
    from test_gpt_submission_action import load_worker_module

    settings, app, c, candidate, rid = setup_early(tmp_path)
    # This existing record predates the fast-batch-v1 protocol.
    with app.state.store.connection() as db:
        db.execute("BEGIN IMMEDIATE")
        raw = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)).fetchone()[0]
        job = app.state.store.decode(raw)
        job["review_protocol"] = "legacy-v1"
        db.execute(
            "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
            (app.state.store.encode(job), rid),
        )
        db.commit()
    portal(c, settings, rid)
    state = c.get("/api/finish/state").json()
    closed = post(
        c,
        "/api/finish/close-clarifications",
        state["csrf_token"],
        {
            "confirm_no_more_questions": True,
        },
    )
    assert closed.status_code == 200, closed.text
    pending = app.state.store.gpt_review_read(rid)
    assert pending["status"] == "queued"
    worker = load_worker_module()
    status, receipt, saved, question = worker.run_legacy_review(pending, provider=Fake())
    assert status == "ready", (status, receipt)
    assert question is None
    assert saved["review_only"] is True
    assert saved["turns"][0]["answer_text"] == candidate["turns"][0]["answer_text"]


def test_legacy_single_question_saved_to_original_review(tmp_path):
    settings, app, client, candidate, rid = setup_early(tmp_path)
    portal(client, settings, rid)
    _, question = fake_question(app, rid)
    with app.state.store.connection() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)).fetchone()
        record = app.state.store.decode(row[0])
        record["review_protocol"] = "legacy-v1"
        record["pending_batch_id"] = None
        record["pending_clarifications"] = []
        db.execute(
            "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
            (app.state.store.encode(record), rid),
        )
        db.commit()
    pending = client.get("/api/finish/state").json()
    assert pending["status"] == "clarification_needed"
    assert pending["batch_id"] is None
    assert pending["clarifications"][0]["clarification_id"] == question["clarification_id"]
    body = {
        "clarification_id": question["clarification_id"],
        "answer_text": "I check the situation first.",
        "operation_id": secrets.token_hex(16),
        "skipped": False,
    }
    reply = post(client, "/api/finish/clarifications", pending["csrf_token"], body)
    assert reply.status_code == 200, reply.text
    assert reply.json()["status"] == "queued"
    assert (
        post(client, "/api/finish/clarifications", pending["csrf_token"], body).status_code == 200
    )
    recorded = app.state.store.gpt_review_read(rid)
    assert recorded["candidate_record"] == candidate
    assert len(recorded["clarification_history"]) == 1
