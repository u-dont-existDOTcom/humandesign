"""Researcher feedback return path; no extra participant Action."""

from __future__ import annotations

from participant.question_feedback import collect_feedback, feedback_issue
from test_gpt_submission_action import auth, candidate_record, setup_submission, start_review


def test_explicit_objections_separate_from_behavior():
    record = {
        "consent": {"research_use_consented": True},
        "turns": [
            {
                "turn_id": "t1",
                "canonical_question_id": "G10",
                "question_text": "Group question?",
                "answer_text": "It depends on whether my work can fit their schedule.",
                "process_feedback": ["This is too vague; I already explained my availability."],
            },
            {
                "turn_id": "t2",
                "canonical_question_id": "D0",
                "question_text": "Practice?",
                "answer_text": "I would continue because practice matters.",
                "process_feedback": [],
            },
        ],
    }
    found = collect_feedback(record, source_type="review_record", source_id="review-test")
    assert len(found) == 1
    assert found[0]["route_id"] == "G10"
    assert "too vague" in found[0]["feedback_text"]
    assert found[0]["issue_hint"] == "unclear"  # Heuristic triage hint is not a final verdict.
    assert "It depends" not in found[0]["feedback_text"]
    record["consent"]["research_use_consented"] = False
    assert collect_feedback(record, source_type="review_record", source_id="review-test") == []


def test_untagged_clear_objection_is_flagged_but_plain_conditional_answer_is_not():
    record = {
        "consent": {"research_use_consented": True},
        "turns": [
            {
                "turn_id": "t1",
                "question_text": "Question A",
                "answer_text": "Why are you asking this? I already answered that.",
            },
            {
                "turn_id": "t2",
                "question_text": "Question B",
                "answer_text": "It depends on context.",
            },
            {
                "turn_id": "t3",
                "question_text": "Question C",
                "answer_text": "It depends on whether my supervisor trusts me.",
            },
        ],
    }
    found = collect_feedback(record, source_type="review_record", source_id="review-test")
    assert len(found) == 1
    assert found[0]["turn_id"] == "t1"
    assert found[0]["capture_method"] == "explicit_objection_in_answer"
    assert feedback_issue(found[0]["feedback_text"]) == "redundant"


def test_researcher_inbox_includes_queued_review_before_final_submission(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    candidate = candidate_record()
    candidate["turns"][0]["process_feedback"] = [
        "This question does not distinguish my preference from the obvious practical response."
    ]
    started = start_review(client, settings.submission_token, candidate)
    assert started.status_code == 200
    assert client.get("/api/admin/question-feedback").status_code == 401
    assert (
        client.get(
            "/api/admin/question-feedback", headers=auth(settings.submission_token)
        ).status_code
        == 401
    )
    response = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token))
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    item = payload["feedback"][0]
    assert item["route_id"] == "unmapped"
    assert "obvious practical response" in item["feedback_text"]
    assert item["source_type"] == "review_record"
    assert payload["auto_applies_question_changes"] is False
    assert started.json()["review_id"] == item["source_id"]
    assert client.app.state.store.gpt_submission_overview() == []


def test_review_clarification_objection_and_withdrawn_source(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    candidate = candidate_record()
    review_id = start_review(client, settings.submission_token, candidate).json()["review_id"]

    # A recorded clarification complaint is recoverable even before final storage.
    def inject(payload):
        payload["clarification_history"] = [
            {
                "route_id": "TF1-G10",
                "question_text": "What normally changes?",
                "answer_text": "You already asked this question; my answer was conditional.",
            },
        ]
        payload["status"] = "clarification_needed"

    with app.state.store.connection() as db:
        row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)).fetchone()
        state = app.state.store.decode(row[0])
        inject(state)
        db.execute(
            "UPDATE gpt_review_jobs SET status=?,payload=? WHERE id=?",
            (state["status"], app.state.store.encode(state), review_id),
        )
    info = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()
    assert info["total"] == 1
    assert info["feedback"][0]["route_id"] == "TF1-G10"
    assert info["feedback"][0]["issue_hint"] == "redundant"
    # Withdrawn reviews no longer expose source feedback.
    with app.state.store.connection() as db:
        state["status"] = "withdrawn"
        db.execute(
            "UPDATE gpt_review_jobs SET status=?,payload=? WHERE id=?",
            ("withdrawn", app.state.store.encode(state), review_id),
        )
    info = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()
    assert info["total"] == 0


def test_synthetic_pilot_is_never_added_to_feedback_counts():
    fake = {
        "consent": {"research_use_consented": True},
        "evidence_authority": "synthetic_release_canary_not_participant",
        "turns": [
            {"turn_id": "test", "question_text": "A", "answer_text": "I already answered this"}
        ],
    }
    assert collect_feedback(fake, source_type="review_record", source_id="syn") == []


def test_private_admin_page_has_feedback_panel_and_escaped_rendering(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    page = client.get("/admin")
    assert page.status_code == 200
    assert "Question feedback" in page.text
    assert "feedback-refresh" in page.text
    assert "feedback-download" in page.text
    script = client.get("/assets/admin.js")
    assert script.status_code == 200
    assert "refreshQuestionFeedback" in script.text
    assert "textContent=item.feedback_text" in script.text
    assert "innerHTML" not in script.text


def test_only_consenting_nonsynthetic_reviews_expose_derived_process_feedback(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    candidate = candidate_record()
    review_id = start_review(client, settings.submission_token, candidate).json()["review_id"]
    store = app.state.store
    with store.connection() as db:
        raw = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)).fetchone()[
            0
        ]
        payload = store.decode(raw)
        payload["worker_state"] = {
            "turns": [
                {
                    "turn_id": "t1",
                    "canonical_question_id": "G10",
                    "question_text": "A group scheduling question",
                    "answer_text": "I would try to fit the schedule.",
                    "derived_process_feedback": [
                        "The question repeats a distinction I already answered."
                    ],
                }
            ]
        }
        db.execute(
            "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
            (store.encode(payload), review_id),
        )
    response = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()
    assert response["total"] == 1
    assert response["feedback"][0]["capture_method"] == "process_feedback"
    assert response["feedback"][0]["route_id"] == "G10"
    with store.connection() as db:
        payload["candidate_record"]["evidence_authority"] = "synthetic_release_canary"
        db.execute(
            "UPDATE gpt_review_jobs SET payload=? WHERE id=?",
            (store.encode(payload), review_id),
        )
    response = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()
    assert response["total"] == 0


def test_researcher_can_track_feedback_to_a_versioned_revision(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    candidate = candidate_record()
    candidate["turns"][0]["process_feedback"] = [
        "This question is too vague to distinguish anything about me."
    ]
    start = start_review(client, settings.submission_token, candidate)
    assert start.status_code == 200
    public_review = client.get(
        f"/api/gpt/reviews/{start.json()['review_id']}",
        headers=auth(settings.submission_token),
    ).json()
    before = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()[
        "feedback"
    ][0]
    route = f"/api/admin/question-feedback/{before['feedback_id']}/disposition"
    body = {"status": "revision_proposed", "revision_id": "TF2-development-20261008"}
    assert client.post(route, json=body).status_code == 401
    assert client.post(route, headers=auth(settings.submission_token), json=body).status_code == 401
    assert (
        client.post(
            route,
            headers=auth(settings.admin_token),
            json={"status": "revision_proposed", "revision_id": ""},
        ).status_code
        == 422
    )
    assert (
        client.post(
            route,
            headers=auth(settings.admin_token),
            json={"status": "revision_proposed", "revision_id": "<script>"},
        ).status_code
        == 422
    )
    changed = client.post(route, headers=auth(settings.admin_token), json=body)
    assert changed.status_code == 200
    assert changed.json()["status"] == "revision_proposed"
    after = client.get("/api/admin/question-feedback", headers=auth(settings.admin_token)).json()[
        "feedback"
    ][0]
    assert after["revision_id"] == body["revision_id"]
    assert after["status"] == "revision_proposed"
    with app.state.store.connection() as db:
        stored = db.execute(
            "SELECT status,revision_id FROM question_feedback_dispositions"
        ).fetchall()
    assert stored == [("revision_proposed", "TF2-development-20261008")]
    assert (
        client.get(
            f"/api/gpt/reviews/{start.json()['review_id']}",
            headers=auth(settings.submission_token),
        ).json()
        == public_review
    )
    assert (
        client.post(
            "/api/admin/question-feedback/F-" + "0" * 24 + "/disposition",
            headers=auth(settings.admin_token),
            json=body,
        ).status_code
        == 404
    )
