from __future__ import annotations

import json
import secrets

from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from participant.app import Settings, create_app
from test_participant import Fake, authority


def setup_submission(tmp_path, *, configured: bool = True, live_enabled: bool = False):
    token = secrets.token_urlsafe(32) if configured else ""
    settings = Settings(
        database=tmp_path / "data.sqlite3",
        encryption_key=Fernet.generate_key().decode(),
        admin_token=secrets.token_urlsafe(32),
        join_token=secrets.token_urlsafe(32),
        authority=tmp_path,
        submission_token=token,
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
                "turn_role": "behavioral",
            }
        ],
        "freeze": {
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


def submit(client, token, primary, secondary, *, origin=None):
    headers = {"Authorization": f"Bearer {token}"}
    if origin:
        headers["Origin"] = origin
    return client.post(
        "/api/gpt/submissions",
        headers=headers,
        json={
            "research_use_consented": True,
            "primary_record": primary,
            "cf003_record": secondary,
        },
    )


def test_submission_requires_separate_action_key(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    primary, secondary = records()
    assert submit(client, "wrong-" + settings.submission_token, primary, secondary).status_code == 401
    assert fake.count == 0


def test_submission_is_available_while_inference_is_dark_and_is_idempotent(tmp_path):
    settings, fake, app, client = setup_submission(tmp_path, live_enabled=False)
    primary, secondary = records()
    first = submit(
        client,
        settings.submission_token,
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

    second = submit(client, settings.submission_token, primary, secondary)
    assert second.status_code == 200
    assert second.json()["submission_id"] == receipt["submission_id"]
    assert second.json()["duplicate"] is True
    assert fake.count == 0

    raw = settings.database.read_bytes()
    assert b"I wait and think." not in raw
    stored = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert stored["primary_record"]["turns"][0]["answer_text"] == "I wait and think."
    assert stored["cf003_record"]["primary_record_sha256"] == receipt["primary_record_sha256"]


def test_submission_fails_closed_on_consent_freeze_cf003_or_target_fields(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    primary, secondary = records()

    no_consent = json.loads(json.dumps(primary))
    no_consent["consent"]["research_use_consented"] = False
    assert submit(client, settings.submission_token, no_consent, secondary).status_code == 422

    not_frozen = json.loads(json.dumps(primary))
    not_frozen["freeze"]["frozen_before_birth_or_chart_reveal"] = False
    assert submit(client, settings.submission_token, not_frozen, secondary).status_code == 422

    missing_question = json.loads(json.dumps(secondary))
    missing_question["turns"] = missing_question["turns"][:2]
    assert submit(client, settings.submission_token, primary, missing_question).status_code == 422

    contaminated = json.loads(json.dumps(primary))
    contaminated["birth_date"] = "1900-01-01"
    assert submit(client, settings.submission_token, contaminated, secondary).status_code == 422
    assert fake.count == 0


def test_submission_hash_link_must_match_when_supplied(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    primary, secondary = records()
    secondary["primary_record_sha256"] = "0" * 64
    response = submit(client, settings.submission_token, primary, secondary)
    assert response.status_code == 422
    assert "primary_record_sha256" in response.json()["detail"]


def test_researcher_can_list_and_download_both_submitted_records(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    primary, secondary = records()
    receipt = submit(client, settings.submission_token, primary, secondary).json()
    headers = {"Authorization": f"Bearer {settings.admin_token}"}

    listing = client.get("/api/admin/gpt-submissions", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["submissions"][0]["submission_id"] == receipt["submission_id"]
    assert listing.json()["submissions"][0]["cf003_turn_count"] == 3

    primary_download = client.get(
        f"/api/admin/gpt-submissions/{receipt['submission_id']}/primary",
        headers=headers,
    )
    assert primary_download.status_code == 200
    assert primary_download.json()["schema"] == "life-patterns-full-survey-participant-export-v2"

    secondary_download = client.get(
        f"/api/admin/gpt-submissions/{receipt['submission_id']}/cf003",
        headers=headers,
    )
    assert secondary_download.status_code == 200
    assert secondary_download.json()["primary_record_sha256"] == receipt["primary_record_sha256"]


def test_submission_can_be_disabled_without_affecting_service(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path, configured=False)
    primary, secondary = records()
    response = submit(client, "x" * 40, primary, secondary)
    assert response.status_code == 503
    assert client.get("/healthz").json()["gpt_submission_enabled"] is False
    assert fake.count == 0


def test_action_schema_and_privacy_policy_are_public(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    assert settings.submission_token
    schema = client.get("/action-openapi.yaml")
    assert schema.status_code == 200
    assert "operationId: submitLifePatternsRecords" in schema.text
    assert "life-patterns-participant-production.up.railway.app" in schema.text
    privacy = client.get("/privacy")
    assert privacy.status_code == 200
    assert "does not run model inference" in privacy.text
