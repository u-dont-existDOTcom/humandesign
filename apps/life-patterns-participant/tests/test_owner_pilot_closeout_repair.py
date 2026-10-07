from __future__ import annotations

import json

import pytest
from participant.domain import Plan, new_state, validate_plan
from participant.review_timing import action_forecast
from test_gpt_submission_action import (
    auth,
    candidate_record,
    claim_review,
    ready_review,
    records,
    setup_submission,
    start_review,
    worker_result,
)
from test_participant import authority


def test_phase_local_action_forecast_is_explicit():
    clarification = action_forecast("clarification_needed")
    assert clarification["known_service_calls_before_next_stable_result"] == 2
    assert clarification["permission_cards_may_appear"] == {"low": 1, "high": 2}
    assert "first Allow does not finish" in clarification["participant_message"]
    ready = action_forecast("ready")
    assert ready["known_service_calls_before_next_stable_result"] == 1
    assert ready["permission_cards_may_appear"] == {"low": 1, "high": 1}


def test_ready_review_exposes_measurement_labels_and_splits_distinct_sources(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    candidate = candidate_record()
    started = start_review(client, settings.submission_token, candidate).json()
    review_id = started["review_id"]
    job = claim_review(client, settings.review_worker_token).json()
    worker_state = {
        "phase": "review",
        "turns": [
            {
                "turn_id": "status-source",
                "canonical_question_id": "TF1-STATUS",
                "question_text": "Recognition?",
                "answer_text": "Recognition depends on who it is from.",
                "turn_role": "behavioral",
            },
            {
                "turn_id": "ownership-source",
                "canonical_question_id": "OWNERSHIP",
                "question_text": "Ownership?",
                "answer_text": "The owner could feel awkward.",
                "turn_role": "behavioral",
            },
        ],
        "evidence": [
            {
                "evidence_id": "e-status-ownership",
                "observation": "Two separately scoped observations were retained.",
                "conditions": [],
                "time_frame": "current",
                "relationship_context": "mixed",
                "source_quotes": [
                    {"turn_id": "status-source", "quote": "Recognition depends on who it is from."},
                    {"turn_id": "ownership-source", "quote": "The owner could feel awkward."},
                ],
                "candidate_facet_ids": ["D19.status_ownership"],
                "supported_scope": "Recognition value and an ownership-context concern.",
                "review_status": "independent_semantic_admission_passed",
            }
        ],
    }
    result = worker_result(
        client,
        settings.review_worker_token,
        review_id,
        job["candidate_sha256"],
        "ready",
        worker_state=worker_state,
    )
    assert result.status_code == 200
    public = client.get(
        f"/api/gpt/reviews/{review_id}", headers=auth(settings.submission_token)
    ).json()
    item = public["review_summary"][0]
    assert item["split_for_display"] is True
    assert len(item["measurement_labels"]) == 2
    assert any("recognition" in label for label in item["measurement_labels"])
    assert any("ownership" in label for label in item["measurement_labels"])
    assert {row["turn_id"] for row in item["source_measurements"]} == {
        "status-source",
        "ownership-source",
    }


def test_final_submission_accepts_exact_json_string_transport(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    review_id = ready_review(client, settings, candidate_record())
    response = client.post(
        "/api/gpt/reviewed-submissions",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record_json": json.dumps(primary, ensure_ascii=False),
            "cf003_record_json": json.dumps(secondary, ensure_ascii=False),
        },
    )
    assert response.status_code == 200
    stored = app.state.store.gpt_submission_read(response.json()["submission_id"])
    assert stored["primary_record"] == primary
    assert stored["cf003_record"]["turns"] == secondary["turns"]


def test_malformed_json_string_is_rejected_before_storage(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, secondary = records()
    review_id = ready_review(client, settings, candidate_record())
    response = client.post(
        "/api/gpt/reviewed-submissions",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record_json": "{not-json",
            "cf003_record_json": json.dumps(secondary),
        },
    )
    assert response.status_code == 422
    assert response.json()["diagnostic_id"].startswith("V-")
    assert "raw JSON object string" in response.json()["errors"][0]["hint"]
    assert app.state.store.gpt_submission_overview() == []
    # The same review remains usable after correcting only the transport defect.
    valid = client.post(
        "/api/gpt/reviewed-submissions",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record_json": json.dumps(primary),
            "cf003_record_json": json.dumps(secondary),
        },
    )
    assert valid.status_code == 200


def test_nonobject_json_string_is_rejected_before_storage(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    _, secondary = records()
    review_id = ready_review(client, settings, candidate_record())
    response = client.post(
        "/api/gpt/reviewed-submissions",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record_json": "[]",
            "cf003_record_json": json.dumps(secondary),
        },
    )
    assert response.status_code == 422
    assert response.json()["diagnostic_id"].startswith("V-")
    assert response.json()["errors"][0]["code"] == "dict_type"
    assert "decode to one complete JSON object" in response.json()["errors"][0]["hint"]
    assert app.state.store.gpt_submission_overview() == []


def test_missing_record_string_gives_exact_recovery_hint(tmp_path):
    settings, _, app, client = setup_submission(tmp_path)
    primary, _ = records()
    review_id = ready_review(client, settings, candidate_record())
    response = client.post(
        "/api/gpt/reviewed-submissions",
        headers=auth(settings.submission_token),
        json={
            "research_use_consented": True,
            "review_id": review_id,
            "primary_record_json": json.dumps(primary),
        },
    )
    assert response.status_code == 422
    assert response.json()["errors"][0]["code"] == "missing"
    assert "exact frozen record JSON string is missing" in response.json()["errors"][0]["hint"]
    assert app.state.store.gpt_submission_overview() == []


def _turn(turn_id: str, route_id: str, answer: str) -> dict:
    return {
        "turn_id": turn_id,
        "turn_source": "chatgpt",
        "turn_role": "behavioral",
        "canonical_question_id": route_id,
        "question_text": route_id,
        "answer_text": answer,
    }


def _review_plan(route_ids: list[str], facets: list[str]) -> Plan:
    return Plan.model_validate(
        {
            "action": "review",
            "dispositions": [
                {
                    "turn_id": f"t-{i}",
                    "status": "answered",
                    "conditions": [],
                    "process_feedback_quotes": [],
                    "reason": "Synthetic.",
                }
                for i in range(len(route_ids))
            ],
            "evidence": [
                {
                    "evidence_id": "e-1",
                    "source_quotes": [
                        {"turn_id": f"t-{i}", "quote": f"answer-{i}"}
                        for i in range(len(route_ids))
                    ],
                    "observation": "Synthetic scoped observation.",
                    "evidence_type": "usual_response_self_report",
                    "conditions": [],
                    "time_frame": "current",
                    "relationship_context": "synthetic",
                    "candidate_facet_ids": facets,
                    "supported_scope": "Synthetic scope.",
                    "unsupported_extensions": [],
                }
            ],
            "question": None,
            "control_quote": None,
            "addressed_routes": [],
            "source_review_complete": False,
            "reason": "Review.",
        }
    )


def test_disconnected_constructs_cannot_be_fused_into_one_evidence_item():
    instrument = authority()
    state = new_state("v", "m", "xhigh")
    state["turns"] = [
        _turn("t-0", "STATUS", "answer-0"),
        _turn("t-1", "OWNERSHIP", "answer-1"),
    ]
    with pytest.raises(ValueError, match="disconnected measured distinctions"):
        validate_plan(
            _review_plan(["STATUS", "OWNERSHIP"], ["D19.status_ownership"]),
            state,
            instrument,
            ["t-0", "t-1"],
        )


def test_declared_stopping_and_recovery_facet_can_remain_coherent():
    instrument = authority()
    state = new_state("v", "m", "xhigh")
    state["turns"] = [
        _turn("t-0", "R09", "answer-0"),
        _turn("t-1", "WORK-RECOVERY", "answer-1"),
    ]
    validate_plan(
        _review_plan(
            ["R09", "WORK-RECOVERY"],
            ["D14.stopping_recovery"],
        ),
        state,
        instrument,
        ["t-0", "t-1"],
    )


def test_dependent_life_phase_routes_can_remain_one_coherent_item():
    instrument = authority()
    state = new_state("v", "m", "xhigh")
    state["turns"] = [
        _turn("t-0", "G24", "answer-0"),
        _turn("t-1", "LIFE-PHASE", "answer-1"),
    ]
    validate_plan(
        _review_plan(["G24", "LIFE-PHASE"], ["D20.continuity", "D20.phases"]),
        state,
        instrument,
        ["t-0", "t-1"],
    )


def test_semantic_prompts_protect_against_dumb_answer_pressure_and_scene_repetition():
    from participant.engine import PLANNER, REVIEWER
    from participant.shadow_triage import (
        GAP_QUESTION_RENDER_PROMPT,
        GAP_SPEC_ADMISSION_PROMPT,
        GAP_SPEC_TRIAGE_PROMPT,
    )

    assert "tautology/obvious inverse" in PLANNER
    assert "process feedback" in PLANNER
    assert "one coherent neutral construct" in PLANNER
    assert "fuses materially different measured distinctions" in REVIEWER
    assert "ordinary logic already supplied by the prompt" in GAP_SPEC_TRIAGE_PROMPT
    assert "obvious inverse" in GAP_SPEC_ADMISSION_PROMPT
    assert "ask only the single missing" in GAP_QUESTION_RENDER_PROMPT


def test_action_schema_exposes_string_records_and_phase_permission_help(tmp_path):
    _, _, _, client = setup_submission(tmp_path)
    schema = client.get("/action-openapi.yaml").json()
    submission = schema["components"]["schemas"]["Submission"]
    assert "primary_record" not in submission["properties"]
    assert "cf003_record" not in submission["properties"]
    assert {"primary_record_json", "cf003_record_json"}.issubset(submission["required"])
    operations = {
        op["operationId"]: op
        for verbs in schema["paths"].values()
        for op in verbs.values()
    }
    assert "one final storage call" in operations["submitLifePatternsRecords"]["description"]
    batch_description = operations["submitLifePatternsClarificationBatch"]["description"]
    assert "two calls" in batch_description
    assert "end the turn" in batch_description
    assert "do not call status automatically" in batch_description
    assert "Please click Allow on this tool call to continue." in operations[
        "submitLifePatternsRecords"
    ]["description"]
    review = schema["components"]["schemas"]["ReviewStatus"]
    assert "action_forecast" in review["required"]
    summary_item = review["properties"]["review_summary"]["anyOf"][0]["items"]
    assert {"measurement_labels", "split_for_display", "source_measurements"}.issubset(
        summary_item["required"]
    )
