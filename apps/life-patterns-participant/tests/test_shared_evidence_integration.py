"""Real API/storage seams for the optional, unscored shared addendum."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from participant.shared_evidence import INSTRUMENT, RECORD_SCHEMA, public_instrument
from participant.store import canonical, digest
from test_experience_finish_v2 import example as experience_example
from test_experience_finish_v2 import experience_flow as experience_flow
from test_experience_finish_v2 import headers
from test_gpt_submission_action import (
    auth,
    candidate_record,
    ready_review,
    records,
    setup_submission,
)
from test_railway_finish_handoff import exchange, finished_answers, issue

STATIC = Path(__file__).resolve().parents[1] / "participant/static"


def shared_example(mode="gpt_optional"):
    question = next(item for item in public_instrument()["questions"] if item["id"] == "TIMELINE")
    return {
        "schema": RECORD_SCHEMA,
        "instrument": INSTRUMENT,
        "research_use_consented": True,
        "collection_mode": mode,
        "status": "post_review_development_not_scored",
        "sittings": [
            {
                "sitting_id": "synthetic-sitting-0001",
                "topics_selected": ["TIMELINE"],
                "probe_admissions": [],
                "responses": [
                    {
                        "question_id": "TIMELINE",
                        "prompt_kind": "main",
                        "state": "ANSWERED",
                        "question_text": question["question"],
                        "answer_text": ("  I moved on 2018-09-14 at about 08:30.\n"
                            "That is one selected event.  "),
                        "process_feedback": ["Please keep that date approximate."],
                    }
                ],
            }
        ],
    }


def gpt_body(review_id, shared=None):
    primary, secondary = records()
    body = {
        "research_use_consented": True,
        "review_id": review_id,
        "primary_record_json": json.dumps(primary),
        "cf003_record_json": json.dumps(secondary),
    }
    if shared is not None:
        body["shared_evidence_record_json"] = json.dumps(shared)
    return body


def test_gpt_shared_addendum_round_trip_without_reopening_review(tmp_path):
    settings, fake, app, client = setup_submission(tmp_path)
    rid = ready_review(client, settings, candidate_record())
    before = copy.deepcopy(app.state.store.gpt_review_read(rid))
    record = shared_example()
    body = gpt_body(rid, record)
    result = client.post(
        "/api/gpt/reviewed-submissions", json=body, headers=auth(settings.submission_token)
    )
    assert result.status_code == 200, result.text
    receipt = result.json()
    assert receipt["shared_evidence_record_sha256"] == digest(canonical(record))
    saved = app.state.store.gpt_submission_read(receipt["submission_id"])
    assert saved["shared_evidence_record"] == record
    assert saved["primary_record"]["turns"] == records()[0]["turns"]
    assert saved["cf003_record"]["turns"] == records()[1]["turns"]
    assert "shared_evidence_record" not in saved["primary_record"]
    assert "shared_evidence_record" not in saved["cf003_record"]
    after = app.state.store.gpt_review_read(rid)
    assert after["candidate_record"] == before["candidate_record"]
    assert after["worker_state"] == before["worker_state"]
    assert after["clarification_history"] == before["clarification_history"]
    assert fake.count == 0
    duplicate = client.post(
        "/api/gpt/reviewed-submissions", json=body, headers=auth(settings.submission_token)
    )
    assert duplicate.status_code == 200 and duplicate.json()["duplicate"]
    assert (
        duplicate.json()["shared_evidence_record_sha256"]
        == receipt["shared_evidence_record_sha256"]
    )
    path = f"/api/admin/gpt-submissions/{receipt['submission_id']}/shared-evidence"
    assert client.get(path).status_code == 401
    download = client.get(path, headers=auth(settings.admin_token))
    assert download.json() == record
    assert "no-store" in download.headers["cache-control"]


@pytest.mark.parametrize("change", ["consent", "channel", "mismatch", "birth", "forged_reuse"])
def test_invalid_shared_addendum_writes_no_submission(tmp_path, change):
    settings, _, app, client = setup_submission(tmp_path)
    rid = ready_review(client, settings, candidate_record())
    value = shared_example()
    if change == "consent":
        value["research_use_consented"] = False
    elif change == "channel":
        value["collection_mode"] = "railway_finish"
    elif change == "birth":
        value["sittings"][0]["responses"][0]["answer_text"] = "My natal chart said this."
    elif change == "forged_reuse":
        value["sittings"][0]["responses"][0] = {
            "question_id": "TIMELINE",
            "prompt_kind": "main",
            "state": "ALREADY_COVERED",
            "source_ref": "/primary/turns/0/answer_text",
            "source_quote": "words never supplied",
        }
    body = gpt_body(rid, value)
    if change == "mismatch":
        body["shared_evidence_record"] = copy.deepcopy(value)
        body["shared_evidence_record"]["sittings"][0]["sitting_id"] = "different-sitting-id"
    result = client.post(
        "/api/gpt/reviewed-submissions", json=body, headers=auth(settings.submission_token)
    )
    assert result.status_code == 422
    assert app.state.store.gpt_submission_overview() == []


def test_shared_addendum_needs_ready_review_and_can_reuse_actual_source(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    body = gpt_body(None, shared_example())
    rejected = client.post(
        "/api/gpt/submissions", json=body, headers=auth(settings.submission_token)
    )
    assert rejected.status_code == 422
    assert app.state.store.gpt_submission_overview() == []
    rid = ready_review(client, settings, candidate_record())
    value = shared_example()
    value["sittings"][0]["responses"][0] = {
        "question_id": "TIMELINE",
        "prompt_kind": "main",
        "state": "ALREADY_COVERED",
        "source_ref": "/primary/turns/0/answer_text",
        "source_quote": "I wait and think.",
    }
    result = client.post(
        "/api/gpt/reviewed-submissions",
        json=gpt_body(rid, value),
        headers=auth(settings.submission_token),
    )
    assert result.status_code == 200, result.text


def test_railway_finish_preserves_both_optional_hashes_on_retry_and_reload(experience_flow):
    settings, _, app, client = experience_flow
    rid = ready_review(client, settings, candidate_record())
    assert exchange(client, issue(client, settings, rid)).status_code == 200
    state = client.get("/api/finish/state").json()
    assert state["shared_evidence_instrument"]["version"] == INSTRUMENT
    assert state["shared_evidence_sources"][0]["answer_text"] == "I wait and think."
    assert len(state["shared_evidence_instrument"]["questions"]) == 23
    assert client.get("/assets/shared-evidence.js").status_code == 200
    original = copy.deepcopy(app.state.store.gpt_review_read(rid)["candidate_record"])
    body = finished_answers(state["cf003_questions"])
    body["shared_evidence_record"] = shared_example("railway_finish")
    body["experience_record"] = experience_example()
    assert client.post("/api/finish/submit", json=body).status_code == 403
    result = client.post("/api/finish/submit", json=body, headers=headers(state))
    assert result.status_code == 200, result.text
    first = result.json()
    retried = client.post("/api/finish/submit", json=body, headers=headers(state)).json()
    reloaded = client.get("/api/finish/state").json()["submission"]
    for key in [
        "primary_record_sha256",
        "cf003_record_sha256",
        "experience_record_sha256",
        "shared_evidence_record_sha256",
    ]:
        assert first[key] == retried[key] == reloaded[key]
    saved = app.state.store.gpt_submission_read(first["submission_id"])
    assert saved["shared_evidence_record"] == body["shared_evidence_record"]
    assert saved["experience_record"] == body["experience_record"]
    assert saved["primary_record"]["turns"] == original["turns"]
    body["shared_evidence_record"]["sittings"][0]["responses"][0]["answer_text"] = (
        "Changed after storing."
    )
    assert client.post("/api/finish/submit", json=body, headers=headers(state)).status_code == 409


def test_old_clients_need_no_shared_record(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    rid = ready_review(client, settings, candidate_record())
    response = client.post(
        "/api/gpt/reviewed-submissions", json=gpt_body(rid), headers=auth(settings.submission_token)
    )
    assert response.status_code == 200
    assert "shared_evidence_record_sha256" not in response.json()
    saved = app.state.store.gpt_submission_read(response.json()["submission_id"])
    assert "shared_evidence_record" not in saved


@pytest.mark.parametrize("channel", ["gpt_optional", "railway_finish"])
def test_both_finish_channels_reuse_exact_experience_note(experience_flow, channel):
    settings, _, app, client = experience_flow
    rid = ready_review(client, settings, candidate_record())
    note = "  Not in the last year.\nEarlier experiences were different.  "
    experience = experience_example(channel)
    experience["responses"][2]["note"] = note
    shared = shared_example(channel)
    shared["sittings"][0]["responses"][0] = {
        "question_id": "TIMELINE",
        "prompt_kind": "main",
        "state": "ALREADY_COVERED",
        "source_ref": "/experience/responses/2/note",
        "source_quote": note,
    }
    if channel == "gpt_optional":
        url = "/api/gpt/reviewed-submissions"
        request_headers = auth(settings.submission_token)
        body = gpt_body(rid, shared)
        experience_key = "experience_record_json"
        serialize = json.dumps
    else:
        assert exchange(client, issue(client, settings, rid)).status_code == 200
        state = client.get("/api/finish/state").json()
        url = "/api/finish/submit"
        request_headers = headers(state)
        body = finished_answers(state["cf003_questions"])
        body["shared_evidence_record"] = shared
        experience_key = "experience_record"
        serialize = copy.deepcopy
    assert client.post(url, json=body, headers=request_headers).status_code == 422
    stale = copy.deepcopy(experience)
    stale["responses"][2]["note"] = "A correction removes the quoted words."
    body[experience_key] = serialize(stale)
    assert client.post(url, json=body, headers=request_headers).status_code == 422
    assert app.state.store.gpt_submission_overview() == []
    body[experience_key] = serialize(experience)
    result = client.post(url, json=body, headers=request_headers)
    assert result.status_code == 200, result.text
    saved = app.state.store.gpt_submission_read(result.json()["submission_id"])
    assert saved["experience_record"]["responses"][2]["note"] == note
    assert saved["shared_evidence_record"] == shared


def test_action_upgrade_is_strictly_additive_for_existing_clients(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    previous = json.loads((STATIC / "action-openapi-v1.9.yaml").read_text())
    current = client.get("/action-openapi.yaml").json()
    assert current["info"]["version"] == "1.10.0"
    for schema, field in [
        ("Submission", "shared_evidence_record_json"),
        ("Receipt", "shared_evidence_record_sha256"),
        ("ReviewStatus", "shared_evidence_available"),
    ]:
        assert field in current["components"]["schemas"][schema]["properties"]
        del current["components"]["schemas"][schema]["properties"][field]
    current["paths"]["/api/gpt/reviews/{review_id}"]["get"]["parameters"].pop()
    current["info"]["version"] = previous["info"]["version"]
    assert current == previous
    rid = ready_review(client, settings, candidate_record())
    legacy = client.get(f"/api/gpt/reviews/{rid}", headers=auth(settings.submission_token))
    assert "shared_evidence_available" not in legacy.json()
    state = client.get(
        f"/api/gpt/reviews/{rid}?include_shared_evidence=true",
        headers=auth(settings.submission_token),
    )
    assert state.json()["shared_evidence_available"] is True


def test_finalized_review_does_not_offer_new_shared_answers(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    rid = ready_review(client, settings, candidate_record())
    stored = client.post(
        "/api/gpt/reviewed-submissions", json=gpt_body(rid), headers=auth(settings.submission_token)
    )
    assert stored.status_code == 200
    status = client.get(
        f"/api/gpt/reviews/{rid}?include_shared_evidence=true",
        headers=auth(settings.submission_token),
    ).json()
    assert status["status"] == "ready"
    assert status["shared_evidence_available"] is False
