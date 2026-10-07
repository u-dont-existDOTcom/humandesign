"""HTTP/worker seam tests; no real participants or provider calls."""

from __future__ import annotations

import copy
import secrets
from dataclasses import replace
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient
from participant.app import create_app
from participant.domain import new_state
from participant.fast_review import PROTOCOL, source_revision
from participant.question_policy import activate
from participant.review_timing import review_guidance
from participant.shadow_triage import (
    GapMatchAuditResponse,
    GapQuestionRenderResponse,
    GapQuestionReviewResponse,
    GapSpecAdmission,
    GapSpecTriage,
)
from test_gpt_submission_action import (
    auth,
    candidate_record,
    claim_review,
    load_worker_module,
    records,
    setup_submission,
    submit,
)
from test_participant import Fake, authority


class FastFake(Fake):
    def __init__(self):
        super().__init__()
        self.triages = 0
        self.seen_sources = []
        self.review = True

    def call(self, system, payload, schema, model, effort):
        meta = {"duration_seconds": 0.01, "prompt_tokens": 100, "completion_tokens": 10}
        if schema is GapSpecTriage:
            self.triages += 1
            self.seen_sources.append(copy.deepcopy(payload["turns"]))
            if self.triages > 1:
                return GapSpecTriage(decision="review_ready", candidates=[]), meta
            return GapSpecTriage.model_validate(
                {
                    "decision": "clarification_needed",
                    "candidates": [
                        {
                            "candidate_id": f"C{i}",
                            "rank": i,
                            "route_id": rid,
                            "source_anchor_turn_ids": [payload["turns"][0]["turn_id"]],
                            "antecedent_turn_ids": [],
                            "equivalent_context": False,
                            "missing_distinction": "Synthetic material missing factor.",
                        }
                        for i, rid in enumerate(["TF1-M11", "TF1-G19"], 1)
                    ],
                }
            ), meta
        if schema is GapSpecAdmission:
            return GapSpecAdmission.model_validate(
                {
                    "source_review_complete": True,
                    "reviews": [
                        {
                            "candidate_id": item["candidate_id"],
                            "route_id": item["route_id"],
                            "approved": True,
                            "source_references_valid": True,
                            "not_already_answered": True,
                            "premise_supported": True,
                            "antecedent_supported": True,
                            "context_supported": True,
                            "material_information_gain": True,
                            "independent_for_batch": True,
                            "failure_codes": [],
                        }
                        for item in payload["proposed_gap_specs"]
                    ],
                }
            ), meta
        if schema is GapMatchAuditResponse:
            return schema.model_validate(
                {
                    "reviews": [
                        {"status": "answered", "independent_for_batch": True}
                        for _ in payload["pairs"]
                    ]
                }
            ), meta
        if schema is GapQuestionRenderResponse:
            return schema.model_validate(
                {
                    "questions": [
                        {"text": row["route_authority"]["question"]}
                        for row in payload["render_specs"]
                    ]
                }
            ), meta
        if schema is GapQuestionReviewResponse:
            return schema.model_validate(
                {
                    "reviews": [
                        {
                            "approved": True,
                            "construct_discriminating": True,
                            "one_response_task": True,
                            "no_unsupported_extension": True,
                            "failure_codes": [],
                        }
                        for _ in payload["items"]
                    ]
                }
            ), meta
        return super().call(system, payload, schema, model, effort)


def setup_fast(tmp_path, monkeypatch):
    settings, _, _, _ = setup_submission(tmp_path)
    settings = replace(settings, fast_review_enabled=True)
    fake = FastFake()
    app = create_app(settings, provider=fake, instrument=authority())
    client = TestClient(app)
    worker = load_worker_module()
    monkeypatch.setattr(worker, "CodexCliProvider", lambda **kw: fake)
    stages = []

    def transport(method, url, token, body=None, **kwargs):
        if body and body.get("review_stage"):
            stages.append(body["review_stage"])
        r = client.request(method, urlparse(url).path, headers=auth(token), json=body)
        if r.status_code >= 400:
            raise worker.TransportError(r.status_code)
        return r.status_code, r.json() if r.content else None

    monkeypatch.setattr(worker, "http_json", transport)
    box = worker.EncryptedOutbox(tmp_path / "outbox")
    return settings, fake, app, client, worker, box, stages


def start_fast(client, settings):
    r = client.post(
        "/api/gpt/reviews",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "candidate_record": candidate_record(),
            "request_id": secrets.token_hex(16),
            "review_protocol": PROTOCOL,
        },
    )
    assert r.status_code == 200, r.text
    return r.json()


def view(client, settings, rid):
    return client.get(f"/api/gpt/reviews/{rid}", headers=auth(settings.submission_token)).json()


def answer_batch(client, settings, state, *, count=None, skip=False):
    qs = state["clarifications"][:count]
    body = {
        "batch_id": state["batch_id"],
        "operation_id": secrets.token_hex(16),
        "answers": [
            {
                "clarification_id": q["clarification_id"],
                "answer_text": "" if skip else f"Exact answer {i}.",
                "skipped": skip,
            }
            for i, q in enumerate(qs)
        ],
    }
    return client.post(
        f"/api/gpt/reviews/{state['review_id']}/clarification-batches",
        headers=auth(settings.submission_token),
        json=body,
    ), body


def test_fast_http_worker_batch_final_review_and_submission(tmp_path, monkeypatch):
    s, fake, app, c, worker, box, stages = setup_fast(tmp_path, monkeypatch)
    started = start_fast(c, s)
    rid = started["review_id"]
    assert started["recommended_check_after_seconds"] == 180
    assert started["final_review_completed"] is False
    assert worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    questions = view(c, s, rid)
    assert questions["status"] == "clarification_needed"
    assert len(questions["clarifications"]) == 2
    assert "gap_admission" in stages
    assert "source_revision" not in questions
    r, body = answer_batch(c, s, questions)
    assert r.status_code == 200, r.text
    retry = c.post(
        f"/api/gpt/reviews/{rid}/clarification-batches", headers=auth(s.submission_token), json=body
    )
    assert retry.status_code == 200
    assert len(app.state.store.gpt_review_read(rid)["clarification_history"]) == 2
    assert worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    intermediate = view(c, s, rid)
    assert intermediate["status"] == "queued"
    assert intermediate["review_stage"] == "final_synthesis"
    assert intermediate["review_summary"] is None
    assert not intermediate["final_review_completed"]
    assert len(fake.seen_sources[-1]) == 3
    assert [t["answer_text"] for t in fake.seen_sources[-1][-2:]] == [
        "Exact answer 0.",
        "Exact answer 1.",
    ]
    assert worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    ready = view(c, s, rid)
    assert ready["status"] == "ready", ready
    assert ready["final_review_completed"]
    assert "final_synthesis" in stages and "final_admission" in stages
    primary, secondary = records()
    for q, a in zip(questions["clarifications"], body["answers"], strict=True):
        primary["turns"].append(
            {
                "question_text": q["question_text"],
                "answer_text": a["answer_text"],
                "canonical_question_id": q["route_id"],
                "turn_role": "behavioral",
            }
        )
    sent = submit(c, s.submission_token, rid, primary, secondary)
    assert sent.status_code == 200, sent.text
    assert sent.json()["independent_review_completed"]
    assert box.read() is None


@pytest.mark.parametrize("skip", [False, True])
def test_partial_batch_invalidates_unasked_remainder_without_fabricated_skips(
    tmp_path, monkeypatch, skip
):
    s, fake, app, c, worker, box, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(c, s)["review_id"]
    worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    before = view(c, s, rid)
    r, _ = answer_batch(c, s, before, count=1, skip=skip)
    assert r.status_code == 200
    saved = app.state.store.gpt_review_read(rid)
    assert len(saved["clarification_history"]) == 1
    assert saved["clarification_history"][0]["answer_status"] == ("skipped" if skip else "answered")
    assert saved["pending_clarifications"] == []
    assert answer_batch(c, s, before, count=1)[0].status_code == 409
    worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    assert len(fake.seen_sources[-1]) == 2


def test_bad_order_has_no_partial_commit_and_withdraw_clears_batch(tmp_path, monkeypatch):
    s, _, app, c, worker, box, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(c, s)["review_id"]
    worker.process_one("https://testserver", s.review_worker_token, outbox=box)
    state = view(c, s, rid)
    qs = state["clarifications"]
    body = {
        "batch_id": state["batch_id"],
        "operation_id": secrets.token_hex(16),
        "answers": [
            {"clarification_id": q["clarification_id"], "answer_text": "Exact."}
            for q in reversed(qs)
        ],
    }
    assert (
        c.post(
            f"/api/gpt/reviews/{rid}/clarification-batches",
            headers=auth(s.submission_token),
            json=body,
        ).status_code
        == 409
    )
    assert app.state.store.gpt_review_read(rid)["clarification_history"] == []
    for action in ["pause", "resume", "withdraw"]:
        r = c.post(
            f"/api/gpt/reviews/{rid}/control",
            headers=auth(s.submission_token),
            json={"action": action, "operation_id": secrets.token_hex(16)},
        )
        assert r.status_code == 200
    saved = app.state.store.gpt_review_read(rid)
    assert saved["candidate_record"] == {} and not saved["pending_clarifications"]
    assert saved["worker_state"] is None
    assert answer_batch(c, s, state)[0].status_code == 409


def test_fast_start_disabled_and_legacy_compatible(tmp_path):
    s, _, _, c = setup_submission(tmp_path)
    body = {
        "research_use_consented": True,
        "candidate_record": candidate_record(),
        "request_id": secrets.token_hex(16),
        "review_protocol": PROTOCOL,
    }
    assert (
        c.post("/api/gpt/reviews", headers=auth(s.submission_token), json=body).status_code == 409
    )
    body.pop("review_protocol")
    assert (
        c.post("/api/gpt/reviews", headers=auth(s.submission_token), json=body).status_code == 200
    )


def test_stale_and_fake_ready_results_are_rejected(tmp_path, monkeypatch):
    s, _, _, c, _, _, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(c, s)["review_id"]
    job = claim_review(c, s.review_worker_token).json()
    body = {
        "candidate_sha256": job["candidate_sha256"],
        "claim_id": job["claim_id"],
        "status": "ready",
        "worker_state": {"phase": "review"},
        "receipt": {"instrument_version": job["instrument_version"], "source_revision": "0" * 64},
    }
    url = f"/api/review-worker/jobs/{rid}/result"
    assert c.post(url, headers=auth(s.review_worker_token), json=body).status_code == 409
    body["receipt"]["source_revision"] = source_revision(job["candidate_sha256"], [])
    assert c.post(url, headers=auth(s.review_worker_token), json=body).status_code == 422


def test_timing_honest_ranges_stale_and_overdue():
    base = {
        "status": "processing",
        "review_protocol": PROTOCOL,
        "review_stage": "initial_triage",
        "stage_started_at_unix": 1000,
        "worker_heartbeat_at_unix": 1040,
    }
    normal = review_guidance(base, now=1060)
    assert normal["estimated_stage_seconds"] == {"low": 60, "high": 180}
    assert normal["estimated_remaining_seconds"]["high"] == 120
    overdue = review_guidance(dict(base, worker_heartbeat_at_unix=1250), now=1260)
    assert overdue["estimate_exceeded"] and overdue["estimated_remaining_seconds"] is None
    stale = review_guidance(base, now=1150)
    assert stale["worker_status_uncertain"] and stale["estimated_remaining_seconds"] is None
    final = review_guidance(dict(base, review_stage="final_synthesis"), now=1045)
    assert final["estimated_stage_seconds"]["low"] == 300
    blocked = review_guidance(dict(base, status="error"), now=1100)
    assert blocked["recommended_check_after_seconds"] == 0
    assert "Waiting alone" in blocked["wait_guidance"]


def test_heartbeat_does_not_restart_same_stage_clock(tmp_path, monkeypatch):
    s, _, app, c, _, _, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(c, s)["review_id"]
    job = claim_review(c, s.review_worker_token).json()
    url = f"/api/review-worker/jobs/{rid}/heartbeat"
    previous = None
    for stage in ["final_synthesis", "final_synthesis"]:
        r = c.post(
            url,
            headers=auth(s.review_worker_token),
            json={"claim_id": job["claim_id"], "review_stage": stage},
        )
        assert r.status_code == 200
        current = app.state.store.gpt_review_read(rid)["stage_started_at_unix"]
        if previous is not None:
            assert current == previous
        previous = current


def test_persisted_retired_question_requeues_without_fake_answer_and_rebuilds(
    tmp_path, monkeypatch
):
    settings, _, app, client, worker, box, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(client, settings)["review_id"]
    store = app.state.store
    payload = store.gpt_review_read(rid)
    stale_question = {
        "route_id": "G15",
        "route_type": "canonical",
        "question_text": (
            "Imagine an ordinary day where you do about six hours of mentally demanding "
            "computer work that you find worthwhile. What would your energy usually be like?"
        ),
        "antecedent_turn_ids": [],
        "clarification_id": "Q-stale-synthetic",
    }
    state = new_state(payload["instrument_version"], payload["model"], payload["effort"])
    activate(state)
    state.update(
        phase="awaiting_answer",
        gpt_review_answers_processed=0,
        pending_question={
            "route_id": "G15",
            "route_type": "canonical",
            "text": stale_question["question_text"],
            "antecedent_turn_ids": [],
        },
    )
    state["fast_review"] = {
        "protocol": PROTOCOL,
        "stage": "triage",
        "pending_questions": [
            {
                "route_id": "G15",
                "route_type": "canonical",
                "text": stale_question["question_text"],
                "antecedent_turn_ids": [],
            }
        ],
        "source_revision": source_revision(payload["candidate_sha256"], []),
        "deferred_audit_pending": False,
        "final_review_completed": False,
    }
    with store.connection() as db:
        row = db.execute(
            "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
        ).fetchone()
        current = store.decode(row[0])
        current.update(
            status="clarification_needed",
            worker_state=state,
            pending_clarification=stale_question,
            pending_clarifications=[stale_question],
            pending_batch_id="B-stale-synthetic",
        )
        store._save_review(db, current)
        db.commit()

    assert store.requeue_stale_gpt_review_questions({"G15"}) == 1
    refreshed = store.gpt_review_read(rid)
    assert refreshed["status"] == "queued"
    assert refreshed["clarification_history"] == []
    assert refreshed["pending_clarifications"] == []
    assert refreshed["worker_state"]["fast_review"]["policy_refresh_required"] is True
    assert refreshed["worker_state"]["phase"] == "ready"

    assert worker.process_one("https://testserver", settings.review_worker_token, outbox=box)
    after = view(client, settings, rid)
    assert after["status"] == "clarification_needed"
    assert all(q["route_id"] != "G15" for q in after["clarifications"])
    assert store.gpt_review_read(rid)["clarification_history"] == []


def test_service_startup_migrates_persisted_retired_question(tmp_path):
    settings, _, _, _ = setup_submission(tmp_path)
    settings = replace(settings, fast_review_enabled=True)
    first_app = create_app(settings, provider=FastFake(), instrument=authority())
    first_client = TestClient(first_app)
    rid = start_fast(first_client, settings)["review_id"]
    store = first_app.state.store
    payload = store.gpt_review_read(rid)
    stale_question = {
        "route_id": "G15",
        "route_type": "canonical",
        "question_text": "Synthetic legacy G15 question.",
        "antecedent_turn_ids": [],
        "clarification_id": "Q-startup-stale",
    }
    state = new_state(payload["instrument_version"], payload["model"], payload["effort"])
    activate(state)
    state.update(phase="awaiting_answer", gpt_review_answers_processed=0)
    state["fast_review"] = {
        "protocol": PROTOCOL,
        "stage": "triage",
        "pending_questions": [{"route_id": "G15"}],
        "source_revision": source_revision(payload["candidate_sha256"], []),
        "deferred_audit_pending": False,
        "final_review_completed": False,
    }
    with store.connection() as db:
        row = db.execute(
            "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
        ).fetchone()
        current = store.decode(row[0])
        current.update(
            status="clarification_needed",
            worker_state=state,
            pending_clarification=stale_question,
            pending_clarifications=[stale_question],
            pending_batch_id="B-startup-stale",
        )
        store._save_review(db, current)
        db.commit()

    second_app = create_app(settings, provider=FastFake(), instrument=authority())
    assert second_app.state.policy_refresh_count == 1
    refreshed = second_app.state.store.gpt_review_read(rid)
    assert refreshed["status"] == "queued"
    assert refreshed["clarification_history"] == []
    assert refreshed["pending_clarifications"] == []
    assert refreshed["worker_state"]["fast_review"]["policy_refresh_required"] is True


def test_app_startup_requeues_persisted_retired_fast_question(tmp_path, monkeypatch):
    settings, _, app, client, _, _, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(client, settings)["review_id"]
    store = app.state.store
    payload = store.gpt_review_read(rid)
    stale_question = {
        "route_id": "G15",
        "route_type": "canonical",
        "question_text": "Synthetic stale G15 question.",
        "antecedent_turn_ids": [],
        "clarification_id": "Q-startup-stale",
    }
    state = new_state(payload["instrument_version"], payload["model"], payload["effort"])
    activate(state)
    state.update(phase="awaiting_answer", gpt_review_answers_processed=0)
    state["fast_review"] = {
        "protocol": PROTOCOL,
        "stage": "triage",
        "pending_questions": [],
        "source_revision": source_revision(payload["candidate_sha256"], []),
        "deferred_audit_pending": False,
        "final_review_completed": False,
    }
    with store.connection() as db:
        row = db.execute(
            "SELECT payload FROM gpt_review_jobs WHERE id=?", (rid,)
        ).fetchone()
        current = store.decode(row[0])
        current.update(
            status="clarification_needed",
            worker_state=state,
            pending_clarification=stale_question,
            pending_clarifications=[stale_question],
            pending_batch_id="B-startup-stale",
        )
        store._save_review(db, current)
        db.commit()

    restarted = create_app(settings, provider=FastFake(), instrument=authority())
    assert restarted.state.policy_refresh_count == 1
    refreshed = restarted.state.store.gpt_review_read(rid)
    assert refreshed["status"] == "queued"
    assert refreshed["clarification_history"] == []
    assert refreshed["pending_clarifications"] == []
    assert refreshed["worker_state"]["fast_review"]["policy_refresh_required"] is True
