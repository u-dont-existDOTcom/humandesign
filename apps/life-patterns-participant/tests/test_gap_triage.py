import pytest
from participant.domain import Plan
from participant.gap_triage import (
    GapAdmission,
    GapTriage,
    admitted_candidates,
    make_admission_context,
    make_triage_context,
    validate_admission,
    validate_triage,
)
from participant.store import canonical
from test_inference_context import imported_state
from test_participant import authority


def test_gap_triage_context_keeps_full_source_but_omits_evidence_work():
    state = imported_state(turn_count=96)
    instrument = authority()
    context = make_triage_context(state, instrument)

    assert len(context["turns"]) == 96
    assert len(context["candidate_routes"]) >= 70
    assert "candidate_evidence_guide" not in context
    assert "existing_evidence" not in context
    assert "dispositions" not in context


def test_gap_triage_output_schema_is_much_smaller_than_full_plan_schema():
    triage_schema_chars = len(canonical(GapTriage.model_json_schema()))
    plan_schema_chars = len(canonical(Plan.model_json_schema()))

    assert triage_schema_chars < plan_schema_chars * 0.45


def test_gap_triage_enforces_decision_and_canonical_wording():
    state = imported_state(turn_count=12)
    instrument = authority()
    route = make_triage_context(state, instrument)["candidate_routes"][0]

    ready = GapTriage(decision="review_ready", candidates=[])
    assert validate_triage(ready, state, instrument) == ready

    with pytest.raises(ValueError, match="review_ready"):
        validate_triage(
            GapTriage(
                decision="review_ready",
                candidates=[
                    {
                        "route_id": route["id"],
                        "route_type": "canonical",
                        "text": route["question"],
                        "antecedent_turn_ids": [],
                        "equivalent_context": False,
                        "missing_distinction": "fixture",
                        "why_useful": "fixture",
                    }
                ],
            ),
            state,
            instrument,
        )

    with pytest.raises(ValueError, match="canonical triage wording"):
        validate_triage(
            GapTriage(
                decision="clarification_needed",
                candidates=[
                    {
                        "route_id": route["id"],
                        "route_type": "canonical",
                        "text": "Wrong wording",
                        "antecedent_turn_ids": [],
                        "equivalent_context": False,
                        "missing_distinction": "fixture",
                        "why_useful": "fixture",
                    }
                ],
            ),
            state,
            instrument,
        )


def test_gap_admission_only_keeps_independently_approved_candidates():
    state = imported_state(turn_count=12)
    instrument = authority()
    routes = make_triage_context(state, instrument)["candidate_routes"][:2]
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            {
                "route_id": route["id"],
                "route_type": "canonical",
                "text": route["question"],
                "antecedent_turn_ids": [],
                "equivalent_context": False,
                "missing_distinction": "fixture",
                "why_useful": "fixture",
            }
            for route in routes
        ],
    )
    validate_triage(triage, state, instrument)
    context = make_admission_context(state, instrument, triage)

    assert len(context["turns"]) == 12
    assert {r["id"] for r in context["selected_routes"]} == {
        r["id"] for r in routes
    }
    admission = GapAdmission(
        approved_route_ids=[routes[0]["id"]],
        missed_material_gap=None,
        review_ready_supported=False,
        errors=[],
    )
    validate_admission(admission, triage, state, instrument)
    kept = admitted_candidates(triage, admission)
    assert [item.route_id for item in kept] == [routes[0]["id"]]

    missed_admission = GapAdmission(
        approved_route_ids=[routes[0]["id"]],
        missed_material_gap=triage.candidates[1],
        review_ready_supported=False,
        errors=[],
    )
    validate_admission(missed_admission, triage, state, instrument)
    combined = admitted_candidates(triage, missed_admission)
    assert [item.route_id for item in combined] == [routes[0]["id"], routes[1]["id"]]
