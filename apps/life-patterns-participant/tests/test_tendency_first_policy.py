"""New-selection policy at actual producer, admission, HTTP and source boundaries."""

import copy
import json

import pytest
from participant.domain import Plan, Question, bank, import_record, new_state, validate_plan
from participant.inference_context import make_context, make_review_context, presented_route_ids
from participant.question_policy import PolicyProvider, activate, identity
from participant.shadow_triage import (
    GapSpecCandidate,
    GapSpecTriage,
    make_gap_spec_triage_context,
    normalize_gap_spec_bindings,
    validate_gap_spec_triage,
)
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


def completed_work_energy_record():
    return {
        "historical_interview_status": "completed_under_then_current_protocol",
        "unrecovered_current_test_gap": {
            "present": True,
            "note": "Synthetic provenance gap; earlier distinctions stay authoritative.",
        },
        "turns": [
            {
                "turn_id": "old-g15",
                "question_text": "Earlier ordinary worthwhile-work energy baseline.",
                "answer_text": "Generally good unless tired.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "G15"},
            },
            {
                "turn_id": "old-r07",
                "question_text": "Earlier two-day longer-work comparison.",
                "answer_text": "Probably fine.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "R07"},
            },
            {
                "turn_id": "old-r08",
                "question_text": "Earlier prolonged-work comparison.",
                "answer_text": "Pretty good.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "R08"},
            },
            {
                "turn_id": "old-r09",
                "question_text": "Earlier stopping-cue question.",
                "answer_text": "I stop when too tired or getting nowhere.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "R09"},
            },
            {
                "turn_id": "old-recovery",
                "question_text": "Earlier recovery question.",
                "answer_text": "Rest usually raises my energy.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "WORK-RECOVERY"},
            },
            {
                "turn_id": "later-r07",
                "question_text": "Later matched two-day work retest.",
                "answer_text": "Probably good.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "R07-retest"},
            },
            {
                "turn_id": "later-r08",
                "question_text": "Later matched prolonged-work retest.",
                "answer_text": "Same as before.",
                "canonical_question_id": None,
                "source": {"historical_question_id": "R08-retest"},
            },
        ],
    }


def test_import_resolves_nested_historical_route_ids_and_retest_aliases():
    state = state_for_policy()
    record = completed_work_energy_record()
    original = copy.deepcopy(record)
    import_record(state, record, "prior_json", authority())
    assert record == original
    route_ids = [turn["canonical_question_id"] for turn in state["turns"]]
    assert route_ids == ["G15", "R07", "R08", "R09", "WORK-RECOVERY", "R07", "R08"]
    assert all(turn["id_basis"] == "verified_historical_route" for turn in state["turns"])
    assert state["source_records"][0]["historical_interview_status"].startswith("completed")
    assert state["source_records"][0]["unrecovered_current_test_gap_present"] is True


def test_completed_historical_g15_marks_tendency_successor_presented_and_repair_only():
    state = state_for_policy()
    import_record(state, completed_work_energy_record(), "prior_json", authority())
    presented = presented_route_ids(state, authority())
    assert {"G15", "TF1-G15", "R07", "R08"} <= presented
    context = make_gap_spec_triage_context(state, authority())
    routes = {row["id"]: row for row in context["candidate_routes"]}
    assert "G15" not in routes
    assert routes["TF1-G15"]["candidate_mode"] == "repair_only"
    assert routes["TF1-G15"]["presented_turn_ids"] == ["import-0001"]
    assert set(routes["TF1-G15"]["historical_family_turn_ids"]) >= {
        "import-0001",
        "import-0002",
        "import-0003",
        "import-0004",
        "import-0005",
        "import-0006",
        "import-0007",
    }
    assert context["historical_source_completed"] is True
    assert context["unrecovered_current_test_gap_present"] is True


def test_completed_source_rejects_g15_gap_anchored_outside_relevant_family():
    state = state_for_policy()
    record = completed_work_energy_record()
    record["turns"].append(
        {
            "turn_id": "other",
            "question_text": "An unrelated social question.",
            "answer_text": "An unrelated answer.",
            "canonical_question_id": None,
            "source": {"historical_question_id": "G23"},
        }
    )
    import_record(state, record, "prior_json", authority())
    context = make_gap_spec_triage_context(state, authority())
    triage = GapSpecTriage(
        decision="clarification_needed",
        candidates=[
            GapSpecCandidate(
                candidate_id="C1",
                rank=1,
                route_id="TF1-G15",
                source_anchor_turn_ids=["import-0008"],
                antecedent_turn_ids=["import-0001"],
                equivalent_context=False,
                missing_distinction="Synthetic version-only gap.",
            )
        ],
    )
    with pytest.raises(ValueError, match="relevant historical route family"):
        validate_gap_spec_triage(triage, context)


def test_completed_g15_repair_binds_actual_historical_baseline_not_empty_antecedent():
    state = state_for_policy()
    import_record(state, completed_work_energy_record(), "prior_json", authority())
    context = make_gap_spec_triage_context(state, authority())
    triage = GapSpecTriage(
        decision="clarification_needed",
        candidates=[
            GapSpecCandidate(
                candidate_id="C1",
                rank=1,
                route_id="TF1-G15",
                source_anchor_turn_ids=["import-0001"],
                missing_distinction="A genuinely unresolved synthetic condition.",
            )
        ],
    )
    normalized = normalize_gap_spec_bindings(triage, context)
    assert normalized == ["C1"]
    assert triage.candidates[0].antecedent_turn_ids == ["import-0001"]
    validate_gap_spec_triage(triage, context)
