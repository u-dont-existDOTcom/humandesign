"""Exact source-bound review-handle recovery and clarification process notes."""
from __future__ import annotations

import copy
import json

from test_gpt_submission_action import (
    auth,
    candidate_record,
    ready_review,
    records,
    setup_submission,
)


def _post(client, key, primary, secondary, review_id=None):
    request = {
        "research_use_consented": True,
        "primary_record_json": json.dumps(primary),
        "cf003_record_json": json.dumps(secondary),
    }
    if review_id is not None:
        request["review_id"] = review_id
    return client.post("/api/gpt/reviewed-submissions", headers=auth(key), json=request)


def test_exact_frozen_record_recovers_unique_ready_handle(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    ready = ready_review(client, settings, candidate_record())
    receipt = _post(client, settings.submission_token, primary, secondary)
    assert receipt.status_code == 200, receipt.json()
    assert receipt.json()["review_id"] == ready
    assert receipt.json()["independent_review_completed"] is True
    assert receipt.json()["stored_encrypted"] is True
    saved = app.state.store.gpt_submission_read(receipt.json()["submission_id"])
    assert saved["review_id"] == ready
    assert _post(client, settings.submission_token, primary, secondary).json()["duplicate"] is True


def test_no_partial_or_ambiguous_record_can_recover_another_review(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    ready_review(client, settings, candidate_record())
    wrong = copy.deepcopy(primary)
    wrong["turns"][0]["answer_text"] = "Different answer entirely"
    assert _post(client, settings.submission_token, wrong, secondary).status_code == 422
    missing = copy.deepcopy(primary)
    del missing["turns"]
    assert _post(client, settings.submission_token, missing, secondary).status_code == 422
    ready_review(client, settings, candidate_record())
    ambiguous = _post(client, settings.submission_token, primary, secondary)
    assert ambiguous.status_code == 422
    assert "uniquely match" in ambiguous.json()["detail"]
    assert app.state.store.gpt_submission_overview() == []


def _append_clarification(client, app, review_id, *, feedback=None):
    new_turn = {
        "turn_id": "clarification-1",
        "question_text": "What changes your usual response?",
        "answer_text": None,
        "canonical_question_id": "TF1-G17",
        "turn_role": "behavioral",
        "correction_of": None,
        "conditions": [],
        "corrections": [],
        "process_feedback": [] if feedback is None else feedback,
    }
    store = app.state.store
    with store.connection() as db:
        raw = db.execute(
            "SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)
        ).fetchone()[0]
        state = store.decode(raw)
        state["clarification_history"] = [
            {"question_text": new_turn["question_text"],
             "answer_text": new_turn["answer_text"],
             "route_id": new_turn["canonical_question_id"]}
        ]
        db.execute(
            "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
            (store.encode(state), review_id),
        )
    return new_turn


def test_clarification_process_feedback_preserved_without_changing_behavior(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    review = ready_review(client, settings, candidate_record())
    primary, secondary = records()
    correction = _append_clarification(
        client, app, review, feedback=["The question repeated an already answered condition."]
    )
    primary["turns"].append(correction)
    success = _post(client, settings.submission_token, primary, secondary)
    assert success.status_code == 200, success.json()
    stored = app.state.store.gpt_submission_read(success.json()["submission_id"])
    assert stored["primary_record"]["turns"][-1]["process_feedback"] == correction["process_feedback"]


def test_changed_earlier_behavior_remains_rejected_despite_process_feedback_exception(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    review = ready_review(client, settings, candidate_record())
    primary, secondary = records()
    correction = _append_clarification(client, app, review, feedback=["Already addressed."])
    primary["turns"].append(correction)
    primary["turns"][0]["process_feedback"] = ["Altered historical feedback"]
    assert _post(client, settings.submission_token, primary, secondary).status_code == 422
    primary["turns"][0].pop("process_feedback")
    primary["turns"][1]["answer_text"] = "Invented answer"
    assert _post(client, settings.submission_token, primary, secondary).status_code == 422
