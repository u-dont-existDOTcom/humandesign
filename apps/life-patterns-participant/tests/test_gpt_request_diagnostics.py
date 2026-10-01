"""Regression at the same HTTP validation boundary the participant encountered."""

import copy
import json
import uuid
from pathlib import Path

from participant.validation_diagnostics import safe_validation_diagnostic
from test_gpt_submission_action import auth, candidate_record, setup_submission


def test_start_request_generated_from_exact_candidate_is_accepted(tmp_path):
    settings, fake, _, client = setup_submission(tmp_path)
    candidate = candidate_record()
    candidate["turns"][0]["answer_text"] = "  Exact wording, hedge … and\nnew line.  "
    original = copy.deepcopy(candidate)
    body = {
        "research_use_consented": True,
        "request_id": uuid.uuid4().hex,
        "candidate_record": candidate,
    }
    # This is the documented Data Analysis envelope, not a handcrafted alternate API.
    wire = json.dumps(body, ensure_ascii=False, allow_nan=False)
    response = client.post(
        "/api/gpt/reviews",
        headers={**auth(settings.submission_token), "Content-Type": "application/json"},
        content=wire.encode(),
    )
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "queued"
    assert candidate == original
    assert fake.count == 0


def test_missing_identifier_names_the_field_without_echoing_answers(tmp_path):
    settings, fake, app, client = setup_submission(tmp_path)
    candidate = candidate_record()
    candidate["turns"][0]["answer_text"] = "PRIVATE_ANSWER_CANARY"
    response = client.post(
        "/api/gpt/reviews",
        headers=auth(settings.submission_token),
        json={"research_use_consented": True, "candidate_record": candidate},
    )
    assert response.status_code == 422
    result = response.json()
    assert result["code"] == "request_validation_failed"
    assert result["errors"][0]["path"] == "body.request_id"
    assert result["errors"][0]["code"] == "missing"
    assert result["request_accepted"] is False
    assert "body.request_id: missing" in result["detail"]
    assert "PRIVATE_ANSWER_CANARY" not in response.text
    assert "candidate_record" not in result["errors"][0]["path"]
    with app.state.store.connection() as db:
        assert db.execute("SELECT COUNT(*) FROM gpt_review_jobs").fetchone()[0] == 0
    assert fake.count == 0


def test_short_id_and_stringified_candidate_are_actionable_without_coercion(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    response = client.post(
        "/api/gpt/reviews",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "request_id": "short",
            "candidate_record": json.dumps(candidate_record()),
        },
    )
    fields = {x["path"]: x for x in response.json()["errors"]}
    assert response.status_code == 422
    assert fields["body.request_id"]["code"] == "string_too_short"
    assert fields["body.candidate_record"]["code"] == "dict_type"


def test_diagnostics_never_echo_unknown_keys_values_context_or_messages():
    result = safe_validation_diagnostic(
        [
            {
                "loc": ("body", "SECRET_FIELD_NAME"),
                "type": "extra_forbidden",
                "input": "SECRET_VALUE",
                "msg": "SECRET_MESSAGE",
                "ctx": {"error": "SECRET_CONTEXT"},
            },
            {"loc": ("body", "turns", 999, "answer_text"), "type": "UNTRUSTED_TYPE"},
        ]
    )
    wire = json.dumps(result)
    assert "SECRET_" not in wire and "UNTRUSTED_TYPE" not in wire
    assert result["errors"][0]["path"] == "body.<unrecognized-field>"
    assert result["errors"][1]["path"] == "body.turns.[].answer_text"


def test_published_schema_has_a_complete_start_example():
    root = Path(__file__).resolve().parents[3]
    schema = json.loads(
        (root / "apps/life-patterns-participant/participant/static/action-openapi.yaml").read_text()
    )
    example = schema["components"]["schemas"]["ReviewStart"]["example"]
    required = schema["components"]["schemas"]["ReviewStart"]["required"]
    assert set(required) <= example.keys()
    assert len(example["request_id"]) >= 16
    assert isinstance(example["candidate_record"], dict)
    assert example["candidate_record"]["freeze"]["record_state"] == "candidate"
    assert example["candidate_record"]["consent"]["research_use_consented"] is True
