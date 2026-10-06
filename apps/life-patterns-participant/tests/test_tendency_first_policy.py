"""New-selection policy at actual producer, admission, HTTP and source boundaries."""

import copy
import json

import pytest
from participant.domain import Plan, Question, bank, import_record, new_state, validate_plan
from participant.inference_context import make_context, make_review_context
from participant.question_policy import PolicyProvider, activate, identity
from participant.shadow_triage import make_gap_spec_triage_context
from test_fast_review_integration import setup_fast, start_fast, view
from test_participant import authority

MEAL_PATTERN = (
    "When sharing work or costs with someone, how do you usually work out an arrangement?"
)


def state_for_policy():
    state = new_state("test", "model", "xhigh")
    activate(state)
    return state


def test_legacy_bank_bytes_and_hash_contract_unchanged():
    instrument = authority()
    before = copy.deepcopy(instrument)
    legacy = bank(instrument)
    state = state_for_policy()
    revised = bank(instrument, state)
    assert instrument == before
    assert legacy["questions"] == json.loads(instrument["interviewer-bank-v7.json"])["questions"]
    assert len(legacy["questions"]) == 79
    assert len(revised["questions"]) == 104
    old = next(q for q in revised["questions"] if q["id"] == "M11")
    assert old["question"] == next(q for q in legacy["questions"] if q["id"] == "M11")["question"]
    assert old["elicitation_retired"] is True


def test_fast_and_full_fallback_select_direct_patterns_not_retired_scenarios():
    state = state_for_policy()
    state["turns"] = [
        {
            "turn_id": "t1",
            "turn_source": "import-1",
            "question_text": "Q",
            "answer_text": "A",
            "canonical_question_id": None,
        }
    ]
    instrument = authority()
    fast = make_gap_spec_triage_context(state, instrument)
    full = make_context(state, instrument, ["t1"], bulk_import=True)
    for context in (fast, full):
        routes = {q["id"]: q for q in context["candidate_routes"]}
        assert "M11" not in routes and "M09" not in routes
        assert routes["TF1-M11"]["question"] == MEAL_PATTERN
        assert routes["TF1-M11"].get("planning_targets", []) == []
    reviewed = make_review_context(
        state,
        instrument,
        full,
        {"question": {"route_id": "TF1-M11"}, "evidence": [], "addressed_routes": []},
        bulk_import=True,
    )
    assert any(q["id"] == "TF1-M11" for q in reviewed["selected_routes"])


@pytest.mark.parametrize("skipped_id", ["M11", "TF1-M11"])
def test_skip_survives_replacement_and_dependent_variant(skipped_id):
    state = state_for_policy()
    state["turns"] = [
        {
            "turn_id": "t1",
            "question_text": "Old exact question.",
            "answer_text": None,
            "canonical_question_id": skipped_id,
            "answer_status": "skipped",
        }
    ]
    routes = {q["id"] for q in make_gap_spec_triage_context(state, authority())["candidate_routes"]}
    assert not {"M11", "TF1-M11", "PREFER-EXCHANGE", "TF1-PREFER-EXCHANGE"}.intersection(routes)
    assert "TF1-G15" in routes  # a skip is not a global stop or coverage veto


def test_exact_import_keeps_new_source_identity_and_original_words():
    state = state_for_policy()
    record = {
        "turns": [
            {
                "turn_id": "old",
                "question_text": MEAL_PATTERN,
                "answer_text": "it depends, especially with family...",
                "canonical_question_id": "TF1-M11",
            }
        ]
    }
    original = copy.deepcopy(record)
    import_record(state, record, "prior_json", authority())
    assert record == original
    assert state["turns"][0]["answer_text"] == original["turns"][0]["answer_text"]
    assert state["turns"][0]["canonical_question_id"] == "TF1-M11"
    assert state["question_policy"] == identity()


def test_old_meal_prompt_fails_new_selection_even_with_syntactically_valid_plan():
    state = state_for_policy()
    original = next(q for q in bank(authority())["questions"] if q["id"] == "M11")
    plan = Plan(
        action="ask",
        dispositions=[],
        evidence=[],
        addressed_routes=[],
        source_review_complete=False,
        question=Question(
            route_id="M11",
            route_type="canonical",
            text=original["question"],
            antecedent_turn_ids=[],
            equivalent_context=False,
            missing_distinction="Scene completion",
            why_useful="Claimed useful",
        ),
        control_quote=None,
        reason="Synthetic test",
    )
    with pytest.raises(ValueError, match="retired or skipped"):
        validate_plan(plan, state, authority(), [])


def test_policy_reaches_every_semantic_provider_stage_without_duplicate_injection():
    seen = []

    class Capture:
        def call(self, system, payload, schema, model, effort, **kwargs):
            seen.append(system)
            return {}, {}

    state = state_for_policy()
    wrapped = PolicyProvider(PolicyProvider(Capture(), state), state)
    wrapped.call("Original role", {}, dict, "model", "xhigh")
    assert seen[0].count("ACTIVE ELICITATION POLICY") == 1
    assert "Completing a hypothetical scene" in seen[0]
    assert "Independently admit a facet only if exact answer content" in seen[0]


def test_http_worker_delivers_policy_question_and_retains_policy_in_saved_state(
    tmp_path, monkeypatch
):
    settings, _, app, client, worker, box, _ = setup_fast(tmp_path, monkeypatch)
    rid = start_fast(client, settings)["review_id"]
    assert worker.process_one("https://testserver", settings.review_worker_token, outbox=box)
    result = view(client, settings, rid)
    assert result["status"] == "clarification_needed", result
    assert result["clarifications"][0]["route_id"].startswith("TF1-")
    assert "usually" in result["clarifications"][0]["question_text"]
    assert app.state.store.gpt_review_read(rid)["worker_state"]["question_policy"] == identity()


def test_imported_skip_keeps_status_and_blocks_successor():
    state = state_for_policy()
    record = {
        "turns": [
            {
                "turn_id": "old",
                "question_text": "Original meal question.",
                "answer_text": None,
                "canonical_question_id": "M11",
                "answer_status": "skipped",
            }
        ]
    }
    original = copy.deepcopy(record)
    import_record(state, record, "prior_json", authority())
    assert record == original
    assert state["turns"][0]["answer_status"] == "skipped"
    routes = {
        row["id"] for row in make_gap_spec_triage_context(state, authority())["candidate_routes"]
    }
    assert not {"M11", "TF1-M11", "PREFER-EXCHANGE", "TF1-PREFER-EXCHANGE"} & routes


def test_historical_import_control_cannot_stop_current_queued_review():
    state = state_for_policy()
    record = {
        "turns": [
            {
                "turn_id": "old",
                "question_text": "Earlier interview item",
                "answer_text": "Please leave it unknown rather than repeat it.",
            }
        ]
    }
    import_record(state, record, "prior_json", authority())
    state["gpt_review_answers_processed"] = 0
    tid = state["turns"][0]["turn_id"]
    plan = Plan(
        action="stop",
        dispositions=[],
        evidence=[],
        question=None,
        control_quote={"turn_id": tid, "quote": "Please leave it unknown rather than repeat it."},
        source_review_complete=True,
        reason="Incorrectly promoted historical item skip",
    )
    with pytest.raises(ValueError, match="Historical imported"):
        validate_plan(plan, state, authority(), [tid])


def test_current_explicit_review_stop_is_still_valid():
    state = state_for_policy()
    state["gpt_review_answers_processed"] = 1
    state["turns"] = [
        {
            "turn_id": "review-answer-0001",
            "turn_source": "import-fast-review-clarification",
            "question_text": "Current clarification",
            "answer_text": "Stop this interview now.",
        }
    ]
    plan = Plan(
        action="stop",
        dispositions=[],
        evidence=[],
        question=None,
        control_quote={"turn_id": "review-answer-0001", "quote": "Stop this interview now."},
        source_review_complete=True,
        reason="Current explicit stop",
    )
    validate_plan(plan, state, authority(), ["review-answer-0001"])
