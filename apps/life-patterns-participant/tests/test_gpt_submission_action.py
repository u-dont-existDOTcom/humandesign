from __future__ import annotations

import copy
import importlib.util
import json
import secrets
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from participant.app import Settings, create_app
from participant.domain import bank
from test_participant import Fake, authority

ROOT = Path(__file__).resolve().parents[3]
WORKER_PATH = ROOT / "apps/life-patterns-participant/scripts/gpt_review_worker.py"


def load_worker_module():
    spec = importlib.util.spec_from_file_location("gpt_review_worker_test", WORKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup_submission(
    tmp_path,
    *,
    configured: bool = True,
    worker_configured: bool = True,
    live_enabled: bool = False,
):
    token = secrets.token_urlsafe(32) if configured else ""
    worker_token = secrets.token_urlsafe(32) if worker_configured else ""
    settings = Settings(
        database=tmp_path / "data.sqlite3",
        encryption_key=Fernet.generate_key().decode(),
        admin_token=secrets.token_urlsafe(32),
        join_token=secrets.token_urlsafe(32),
        authority=tmp_path,
        submission_token=token,
        review_worker_token=worker_token,
        secure_cookies=False,
        live_enabled=live_enabled,
    )
    fake = Fake()
    app = create_app(settings, provider=fake, instrument=authority())
    return settings, fake, app, TestClient(app)


def records():
    primary = {
        "schema": "life-patterns-full-survey-participant-export-v2",
        "collection_mode": "chatgpt_voice",
        "retrospective_questions_welcome": True,
        "consent": {"research_use_consented": True},
        "blinding": {
            "birth_or_chart_data_requested_by_interviewer": False,
            "target_predictions_used": False,
        },
        "turns": [
            {
                "turn_id": "t1",
                "question_text": "What do you usually do?",
                "answer_text": "I wait and think.",
                "canonical_question_id": None,
                "turn_role": "behavioral",
                "correction_of": None,
            }
        ],
        "participant_review": {"summary_shown": True, "confirmed": True},
        "freeze": {
            "record_state": "final",
            "frozen_before_birth_or_chart_reveal": True,
            "birth_or_chart_data_in_this_export": False,
        },
    }
    secondary = {
        "schema_version": "life-patterns-cf003-secondary-v0",
        "turns": [
            {
                "question_id": "CF003-ID-01",
                "question_text": "Continuity?",
                "answer_text": "I have stayed curious.",
                "turn_role": "behavioral",
            },
            {
                "question_id": "CF003-CENTRAL-01",
                "question_text": "Central patterns?",
                "answer_text": "Learning and freedom.",
                "turn_role": "behavioral",
            },
            {
                "question_id": "CF003-PERIPH-01",
                "question_text": "Peripheral patterns?",
                "answer_text": "Competition is situational.",
                "turn_role": "behavioral",
            },
        ],
    }
    return primary, secondary


def candidate_record():
    primary, _ = records()
    candidate = copy.deepcopy(primary)
    candidate["participant_review"] = {"summary_shown": False}
    candidate["freeze"] = {
        "record_state": "candidate",
        "frozen_before_birth_or_chart_reveal": False,
        "birth_or_chart_data_in_this_export": False,
    }
    return candidate


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def start_review(client, token, candidate, *, origin=None, request_id=None):
    headers = auth(token)
    if origin:
        headers["Origin"] = origin
    return client.post(
        "/api/gpt/reviews",
        headers=headers,
        json={
            "research_use_consented": True,
            "candidate_record": candidate,
            "request_id": request_id or secrets.token_hex(16),
        },
    )


def claim_review(client, worker_token):
    return client.get("/api/review-worker/jobs/next", headers=auth(worker_token))


def worker_result(
    client,
    worker_token,
    review_id,
    candidate_sha256,
    status,
    *,
    clarification=None,
    worker_state=None,
    error=None,
):
    return client.post(
        f"/api/review-worker/jobs/{review_id}/result",
        headers=auth(worker_token),
        json={
            "candidate_sha256": candidate_sha256,
            "claim_id": client.app.state.store.gpt_review_read(review_id)["claim_id"],
            "status": status,
            "worker_state": worker_state,
            "receipt": {
                "route": "test-worker",
                "instrument_version": client.app.state.store.gpt_review_read(review_id)[
                    "instrument_version"
                ],
                "paid_api": False,
                "production_backend": False,
            },
            "clarification": clarification,
            "error": error,
        },
    )


def ready_review(client, settings, candidate):
    started = start_review(client, settings.submission_token, candidate)
    assert started.status_code == 200
    review_id = started.json()["review_id"]
    job = claim_review(client, settings.review_worker_token)
    assert job.status_code == 200
    assert (
        worker_result(
            client,
            settings.review_worker_token,
            review_id,
            job.json()["candidate_sha256"],
            "ready",
            worker_state={"phase": "review"},
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"/api/gpt/reviews/{review_id}",
            headers=auth(settings.submission_token),
        ).json()["status"]
        == "ready"
    )
    return review_id


def submit(client, token, review_id, primary, secondary, *, origin=None):
    headers = auth(token)
    if origin:
        headers["Origin"] = origin
    return client.post(
        "/api/gpt/reviewed-submissions",
        headers=headers,
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record": primary,
            "cf003_record": secondary,
        },
    )


def first_route():
    return bank(authority())["questions"][0]


def test_review_and_submission_use_separate_action_and_worker_keys(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    candidate = candidate_record()
    assert (
        start_review(
            client,
            "wrong-" + settings.submission_token,
            candidate,
        ).status_code
        == 401
    )
    assert claim_review(client, "wrong-" + settings.review_worker_token).status_code == 401
    assert fake.count == 0


def test_review_queue_works_while_public_inference_is_dark(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path, live_enabled=False)
    candidate = candidate_record()
    started = start_review(
        client,
        settings.submission_token,
        candidate,
        origin="https://chatgpt.com",
    )
    assert started.status_code == 200
    assert started.json()["status"] == "queued"
    assert 840 <= started.json()["recommended_check_after_seconds"] <= 900
    health = client.get("/healthz").json()
    assert health["participant_enabled"] is False
    assert health["gpt_review_queue_enabled"] is True
    assert health["review_worker_configured"] is True
    assert fake.count == 0

    job = claim_review(client, settings.review_worker_token)
    assert job.status_code == 200
    assert job.json()["candidate_record"]["turns"][0]["answer_text"] == "I wait and think."
    assert fake.count == 0


def test_review_candidate_must_be_consented_unfrozen_and_chart_blind(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    candidate = candidate_record()

    frozen = copy.deepcopy(candidate)
    frozen["freeze"]["frozen_before_birth_or_chart_reveal"] = True
    assert start_review(client, settings.submission_token, frozen).status_code == 422

    no_consent = copy.deepcopy(candidate)
    no_consent["consent"]["research_use_consented"] = False
    assert start_review(client, settings.submission_token, no_consent).status_code == 422

    contaminated = copy.deepcopy(candidate)
    contaminated["birth_date"] = "1900-01-01"
    assert start_review(client, settings.submission_token, contaminated).status_code == 422
    assert fake.count == 0


def test_clarification_round_trip_and_final_turn_binding(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    candidate = candidate_record()
    started = start_review(client, settings.submission_token, candidate).json()
    review_id = started["review_id"]
    job = claim_review(client, settings.review_worker_token).json()
    route = first_route()
    clarification = {
        "route_id": route["id"],
        "route_type": "canonical",
        "question_text": route["question"],
        "antecedent_turn_ids": [],
    }
    result = worker_result(
        client,
        settings.review_worker_token,
        review_id,
        job["candidate_sha256"],
        "clarification_needed",
        clarification=clarification,
        worker_state={"phase": "awaiting_answer"},
    )
    assert result.status_code == 200
    status = client.get(
        f"/api/gpt/reviews/{review_id}",
        headers=auth(settings.submission_token),
    ).json()
    assert status["status"] == "clarification_needed"
    assert status["recommended_check_after_seconds"] == 0
    assert status["clarification"]["question_text"] == route["question"]

    answer = client.post(
        f"/api/gpt/reviews/{review_id}/clarifications",
        headers=auth(settings.submission_token),
        json={
            "answer_text": "I usually pause and compare the options.",
            "clarification_id": status["clarification"]["clarification_id"],
            "operation_id": secrets.token_hex(16),
        },
    )
    assert answer.status_code == 200
    assert answer.json()["status"] == "queued"
    assert 840 <= answer.json()["recommended_check_after_seconds"] <= 900

    second_job = claim_review(client, settings.review_worker_token).json()
    assert second_job["clarification_history"][-1]["answer_text"].startswith("I usually pause")
    assert (
        worker_result(
            client,
            settings.review_worker_token,
            review_id,
            second_job["candidate_sha256"],
            "ready",
            worker_state={"phase": "review"},
        ).status_code
        == 200
    )

    primary, secondary = records()
    mismatch = submit(
        client,
        settings.submission_token,
        review_id,
        primary,
        secondary,
    )
    assert mismatch.status_code == 422
    assert "reviewed record" in mismatch.json()["detail"]

    primary["turns"].append(
        {
            "turn_id": "clarification-1",
            "question_text": route["question"],
            "answer_text": "I usually pause and compare the options.",
            "canonical_question_id": route["id"],
            "turn_role": "behavioral",
            "correction_of": None,
        }
    )
    accepted = submit(
        client,
        settings.submission_token,
        review_id,
        primary,
        secondary,
    )
    assert accepted.status_code == 200
    assert accepted.json()["independent_review_completed"] is True
    assert accepted.json()["review_id"] == review_id
    assert fake.count == 0


def test_final_submission_requires_ready_review_and_is_idempotent(tmp_path):
    settings, fake, app, client = setup_submission(tmp_path, live_enabled=False)
    primary, secondary = records()
    candidate = candidate_record()

    queued = start_review(client, settings.submission_token, candidate).json()
    assert (
        submit(
            client,
            settings.submission_token,
            queued["review_id"],
            primary,
            secondary,
        ).status_code
        == 422
    )

    job = claim_review(client, settings.review_worker_token).json()
    assert (
        worker_result(
            client,
            settings.review_worker_token,
            queued["review_id"],
            job["candidate_sha256"],
            "ready",
            worker_state={"phase": "review"},
        ).status_code
        == 200
    )
    first = submit(
        client,
        settings.submission_token,
        queued["review_id"],
        primary,
        secondary,
        origin="https://chatgpt.com",
    )
    assert first.status_code == 200
    receipt = first.json()
    assert receipt["stored_encrypted"] is True
    assert receipt["inference_started"] is False
    assert receipt["duplicate"] is False
    assert fake.count == 0

    second = submit(
        client,
        settings.submission_token,
        queued["review_id"],
        primary,
        secondary,
    )
    assert second.status_code == 200
    assert second.json()["submission_id"] == receipt["submission_id"]
    assert second.json()["duplicate"] is True

    raw = settings.database.read_bytes()
    assert b"I wait and think." not in raw
    stored = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert stored["review_id"] == queued["review_id"]
    assert stored["primary_record"]["turns"][0]["answer_text"] == "I wait and think."


def test_final_submission_still_enforces_freeze_cf003_hash_and_target_fields(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    primary, secondary = records()
    review_id = ready_review(client, settings, candidate_record())

    not_frozen = copy.deepcopy(primary)
    not_frozen["freeze"]["frozen_before_birth_or_chart_reveal"] = False
    assert (
        submit(
            client,
            settings.submission_token,
            review_id,
            not_frozen,
            secondary,
        ).status_code
        == 422
    )

    missing_question = copy.deepcopy(secondary)
    missing_question["turns"] = missing_question["turns"][:2]
    assert (
        submit(
            client,
            settings.submission_token,
            review_id,
            primary,
            missing_question,
        ).status_code
        == 422
    )

    bad_hash = copy.deepcopy(secondary)
    bad_hash["primary_record_sha256"] = "0" * 64
    response = submit(
        client,
        settings.submission_token,
        review_id,
        primary,
        bad_hash,
    )
    assert response.status_code == 422
    assert "primary_record_sha256" in response.json()["detail"]

    contaminated = copy.deepcopy(primary)
    contaminated["birth_date"] = "1900-01-01"
    assert (
        submit(
            client,
            settings.submission_token,
            review_id,
            contaminated,
            secondary,
        ).status_code
        == 422
    )
    assert fake.count == 0


def test_researcher_can_list_and_download_reviewed_submission(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    primary, secondary = records()
    review_id = ready_review(client, settings, candidate_record())
    receipt = submit(
        client,
        settings.submission_token,
        review_id,
        primary,
        secondary,
    ).json()
    headers = auth(settings.admin_token)

    listing = client.get("/api/admin/gpt-submissions", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["submissions"][0]["submission_id"] == receipt["submission_id"]
    assert listing.json()["submissions"][0]["cf003_turn_count"] == 3

    primary_download = client.get(
        f"/api/admin/gpt-submissions/{receipt['submission_id']}/primary",
        headers=headers,
    )
    assert primary_download.status_code == 200

    secondary_download = client.get(
        f"/api/admin/gpt-submissions/{receipt['submission_id']}/cf003",
        headers=headers,
    )
    assert secondary_download.status_code == 200
    assert secondary_download.json()["primary_record_sha256"] == receipt["primary_record_sha256"]


def test_submission_and_review_can_be_disabled_independently(tmp_path):
    settings, fake, _, client = setup_submission(
        tmp_path, configured=False, worker_configured=False
    )
    candidate = candidate_record()
    assert start_review(client, "x" * 40, candidate).status_code == 503
    health = client.get("/healthz").json()
    assert health["gpt_submission_enabled"] is False
    assert health["gpt_review_queue_enabled"] is False
    assert health["review_worker_configured"] is False
    assert fake.count == 0


def test_local_worker_reuses_existing_engine_with_fake_model():
    worker = load_worker_module()
    candidate = candidate_record()
    job = {
        "review_id": "R-" + "a" * 32,
        "candidate_sha256": "b" * 64,
        "candidate_record": candidate,
        "worker_state": None,
        "clarification_history": [],
        "round": 1,
        "model": "gpt-5.6-sol",
        "effort": "xhigh",
    }
    fake = Fake()
    status, receipt, worker_state, clarification = worker.run_review(job, provider=fake)
    assert status == "clarification_needed"
    assert clarification
    assert worker_state["phase"] == "awaiting_answer"
    assert fake.count == 2
    assert receipt["paid_api"] is False

    continued = copy.deepcopy(job)
    continued["worker_state"] = worker_state
    continued["round"] = 2
    continued["clarification_history"] = [
        {
            "route_id": clarification["route_id"],
            "question_text": clarification["question_text"],
            "answer_text": "I would pause and think first.",
        }
    ]
    second_fake = Fake()
    second_fake.review = True
    status, _, next_state, clarification2 = worker.run_review(continued, provider=second_fake)
    assert status == "ready"
    assert clarification2 is None
    assert next_state["phase"] == "review"
    assert next_state["review_only"] is True
    assert next_state["review_finalization_after_clarification"] is True
    assert second_fake.count == 2


def test_action_schema_privacy_and_description_limits(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    response = client.get("/action-openapi.yaml")
    assert response.status_code == 200
    schema = response.json()
    operations = [op for verbs in schema["paths"].values() for op in verbs.values()]
    assert {op["operationId"] for op in operations} == {
        "startLifePatternsReview",
        "getLifePatternsReview",
        "submitLifePatternsClarification",
        "controlLifePatternsReview",
        "submitLifePatternsRecords",
    }
    assert "/api/gpt/reviewed-submissions" in schema["paths"]
    assert all(len(op["description"]) <= 300 and len(op["summary"]) <= 300 for op in operations)
    assert "claim_id" not in json.dumps(schema)
    assert "review_worker_token" not in json.dumps(schema)
    privacy = client.get("/privacy")
    assert privacy.status_code == 200
    assert "researcher's ChatGPT-authenticated Codex CLI" in privacy.text
