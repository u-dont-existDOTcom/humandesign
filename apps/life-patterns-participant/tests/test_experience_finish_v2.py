"""Opt-in experience evidence remains distinct from the frozen questionnaire."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from participant.app import create_app
from participant.experience import (
    INSTRUMENT,
    RECORD_SCHEMA,
    instrument,
    public_instrument,
    validate_experience_record,
)
from test_gpt_submission_action import (
    auth,
    candidate_record,
    ready_review,
    records,
    setup_submission,
)
from test_participant import authority
from test_railway_finish_handoff import exchange, finished_answers, issue

ROOT = Path(__file__).resolve().parents[3]
ORIGIN = "https://testserver"


@pytest.fixture
def experience_flow(tmp_path):
    settings, fake, _, _ = setup_submission(tmp_path)
    source = ROOT / "reference/empirical_astrology/cf003_secondary_question_module_v0.json"
    (tmp_path / source.name).write_bytes(source.read_bytes())
    settings = replace(settings, public_origin=ORIGIN, secure_cookies=True)
    app = create_app(settings, provider=fake, instrument=authority())
    return settings, fake, app, TestClient(app, base_url=ORIGIN)


def example(mode="railway_finish"):
    return {
        "schema": RECORD_SCHEMA,
        "instrument": INSTRUMENT,
        "research_use_consented": True,
        "collection_mode": mode,
        "status": "post_review_exploratory_not_scored",
        "topics_selected": ["EM06"],
        "responses": [
            {
                "question_id": "EM01",
                "state": "ANSWERED",
                "value": "most_days",
                "typical_intensity": "strong",
                "peak_intensity": "overwhelming",
            },
            {"question_id": "EM02", "state": "NOT_ASKED"},
            {"question_id": "EM03", "state": "NEVER", "note": "Not in the last year"},
            {"question_id": "EM04", "state": "UNKNOWN"},
            {"question_id": "EM05", "state": "NOT_ASKED"},
            {"question_id": "EM06", "state": "ANSWERED", "value": "weekly"},
            {"question_id": "EM07", "state": "NOT_ASKED"},
            {
                "question_id": "EM08",
                "state": "ANSWERED",
                "values": {
                    "personal_meaning": "varies",
                    "perceived_contribution": "strong",
                },
            },
        ],
    }


def test_instrument_is_optional_and_has_two_distinct_intensity_fields():
    bank = instrument()
    assert bank["version"] == INSTRUMENT
    assert len(bank["core_ids"]) == len(bank["optional_ids"]) == 4
    assert len({item["id"] for item in bank["items"]}) == 8
    assert "typical" in bank["context_note"]
    assert "maximum" in bank["context_note"]
    assert public_instrument()["items"] == bank["items"]
    assert validate_experience_record(example()) == example()


@pytest.mark.parametrize(
    "change",
    [
        "consent",
        "duplicate",
        "peak",
        "unselected",
        "legacy_intensity",
        "missing",
        "target_leak",
        "meaning_dimensions",
        "unknown_with_intensity",
    ],
)
def test_invalid_experience_records_rejected(change):
    value = example()
    if change == "consent":
        value["research_use_consented"] = False
    elif change == "duplicate":
        value["responses"][-1]["question_id"] = "EM01"
    elif change == "peak":
        value["responses"][0]["peak_intensity"] = "invalid"
    elif change == "unselected":
        value["responses"][1].update(state="NEVER")
    elif change == "legacy_intensity":
        value["responses"][0]["intensity"] = "overwhelming"
    elif change == "missing":
        value["responses"].pop()
    elif change == "target_leak":
        value["responses"][0]["note"] = "My natal chart predicted this."
    elif change == "meaning_dimensions":
        value["responses"][7]["values"] = {"personal_meaning": "strong"}
    elif change == "unknown_with_intensity":
        value["responses"][3]["typical_intensity"] = "strong"
    with pytest.raises(ValueError):
        validate_experience_record(value)


def headers(state):
    return {"Origin": ORIGIN, "X-Finish-CSRF": state["csrf_token"]}


def test_ready_railway_finish_stores_separate_experience(experience_flow):
    settings, _, app, client = experience_flow
    initial = candidate_record()
    review_id = ready_review(client, settings, initial)
    assert exchange(client, issue(client, settings, review_id)).status_code == 200
    ready = client.get("/api/finish/state")
    assert ready.status_code == 200
    state = ready.json()
    assert state["status"] == "ready"
    assert state["experience_instrument"]["version"] == INSTRUMENT
    assert client.get("/assets/experience.js").status_code == 200
    payload = finished_answers(state["cf003_questions"])
    payload["experience_record"] = example()
    assert client.post("/api/finish/submit", json=payload).status_code == 403
    response = client.post("/api/finish/submit", json=payload, headers=headers(state))
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["stored_encrypted"] and receipt["experience_record_sha256"]
    stored = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert stored["experience_record"] == example()
    assert stored["experience_record_sha256"] == receipt["experience_record_sha256"]
    assert stored["primary_record"]["turns"] == initial["turns"]
    assert "experience_record" not in stored["primary_record"]
    assert "experience_record" not in stored["cf003_record"]
    assert client.post("/api/finish/submit", json=payload, headers=headers(state)).json()[
        "duplicate"
    ]
    changed = copy.deepcopy(payload)
    changed["experience_record"]["responses"][0]["peak_intensity"] = "faint"
    assert (
        client.post("/api/finish/submit", json=changed, headers=headers(state)).status_code == 409
    )
    direct = client.get(f"/api/admin/gpt-submissions/{receipt['submission_id']}/experience")
    assert direct.status_code == 401
    download = client.get(
        f"/api/admin/gpt-submissions/{receipt['submission_id']}/experience",
        headers=auth(settings.admin_token),
    )
    assert download.status_code == 200
    assert json.loads(download.text) == example()
    assert "no-store" in download.headers["cache-control"]


def test_no_opt_in_preserves_existing_two_records(experience_flow):
    settings, _, app, client = experience_flow
    rid = ready_review(client, settings, candidate_record())
    assert exchange(client, issue(client, settings, rid)).status_code == 200
    state = client.get("/api/finish/state").json()
    body = finished_answers(state["cf003_questions"])
    response = client.post("/api/finish/submit", json=body, headers=headers(state))
    assert response.status_code == 200
    assert "experience_record_sha256" not in response.json()
    saved = app.state.store.gpt_submission_read(response.json()["submission_id"])
    assert "experience_record" not in saved
    assert saved["primary_record"] and saved["cf003_record"]


def test_wrong_collection_channel_rejected_before_storage(experience_flow):
    settings, _, app, client = experience_flow
    rid = ready_review(client, settings, candidate_record())
    assert exchange(client, issue(client, settings, rid)).status_code == 200
    state = client.get("/api/finish/state").json()
    body = finished_answers(state["cf003_questions"])
    body["experience_record"] = example("gpt_optional")
    result = client.post("/api/finish/submit", json=body, headers=headers(state))
    assert result.status_code == 422
    assert app.state.store.gpt_submission_overview() == []


def test_action_v19_retains_old_required_fields_and_adds_optional_json(experience_flow):
    _, _, _, client = experience_flow
    action = json.loads(client.get("/action-openapi.yaml").text)
    assert action["info"]["version"] == "1.10.0"
    props = action["components"]["schemas"]["Submission"]
    assert props["required"] == [
        "research_use_consented",
        "primary_record_json",
        "cf003_record_json",
    ]
    assert props["properties"]["experience_record_json"]["maxLength"] == 50000
    assert action["components"]["schemas"]["Receipt"]["properties"].get("experience_record_sha256")


def test_existing_gpt_action_accepts_only_reviewed_optional_addendum(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    optional = example("gpt_optional")
    base = {
        "research_use_consented": True,
        "primary_record_json": json.dumps(primary),
        "cf003_record_json": json.dumps(secondary),
        "experience_record_json": json.dumps(optional),
    }
    before_review = client.post(
        "/api/gpt/submissions",
        json=base,
        headers=auth(settings.submission_token),
    )
    assert before_review.status_code == 422
    assert app.state.store.gpt_submission_overview() == []
    rid = ready_review(client, settings, candidate_record())
    accepted = client.post(
        "/api/gpt/reviewed-submissions",
        json={**base, "review_id": rid},
        headers=auth(settings.submission_token),
    )
    assert accepted.status_code == 200, accepted.text
    receipt = accepted.json()
    assert receipt["stored_encrypted"] and receipt["independent_review_completed"]
    assert receipt["experience_record_sha256"]
    saved = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert saved["experience_record"] == optional
    assert "experience_record" not in saved["primary_record"]
    assert "experience_record" not in saved["cf003_record"]
    retried = client.post(
        "/api/gpt/reviewed-submissions",
        json={**base, "review_id": rid},
        headers=auth(settings.submission_token),
    )
    assert retried.status_code == 200 and retried.json()["duplicate"]
    altered = copy.deepcopy(optional)
    altered["responses"][0]["peak_intensity"] = "faint"
    second = client.post(
        "/api/gpt/reviewed-submissions",
        json={**base, "review_id": rid, "experience_record_json": json.dumps(altered)},
        headers=auth(settings.submission_token),
    )
    assert second.status_code == 409
    assert len(app.state.store.gpt_submission_overview()) == 1


def test_gpt_experience_requires_auth_and_matching_transport(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    rid = ready_review(client, settings, candidate_record())
    data = {
        "research_use_consented": True,
        "review_id": rid,
        "primary_record": primary,
        "cf003_record": secondary,
        "experience_record": example("gpt_optional"),
    }
    no_auth = client.post("/api/gpt/reviewed-submissions", json=data)
    assert no_auth.status_code == 401
    other = copy.deepcopy(data["experience_record"])
    other["responses"][0]["typical_intensity"] = "faint"
    response = client.post(
        "/api/gpt/reviewed-submissions",
        json={**data, "experience_record_json": json.dumps(other)},
        headers=auth(settings.submission_token),
    )
    assert response.status_code == 422
    assert app.state.store.gpt_submission_overview() == []
