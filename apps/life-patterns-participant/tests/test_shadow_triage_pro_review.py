"""Contract regressions from the owner-authorized Pro review; synthetic source only."""

from __future__ import annotations

import copy

from participant.domain import bank
from participant.shadow_triage import (
    GapMatchAudit,
    GapMatchAuditResponse,
    GapMatchedRouteJudgment,
    GapMatchedRouteReview,
    GapQuestionReviewResponse,
    GapQuestionWordingJudgment,
    GapSpecAdmission,
    GapSpecAdmissionReview,
    _ordered_admitted_routes,
    bind_gap_match_audit,
    make_gap_match_audit_context,
    make_gap_spec_triage_context,
    make_gap_triage_context,
    privacy_safe_case_summary,
    run_shadow_fast_spec_path,
    run_shadow_triage,
)
from test_shadow_triage import (
    FastSpecOmissionRecoveryFake,
    FastSpecRetryWordingFake,
    ReadyFake,
    RejectedFake,
    authority,
    imported_state,
)


def append_route(state, instrument, route_id="G19", turn_id="scene"):
    route = next(r for r in bank(instrument)["questions"] if r["id"] == route_id)
    state["turns"].append(
        {
            "turn_id": turn_id,
            "turn_role": "behavioral",
            "canonical_question_id": route_id,
            "question_text": route["question"],
            "answer_text": "I would first ask the other person what they think.",
        }
    )


class AlwaysRejectWording(FastSpecRetryWordingFake):
    def call(self, system, payload, schema, model, effort):
        if schema is GapQuestionReviewResponse:
            self.calls.append((system, payload))
            self.review_count += 1
            return GapQuestionReviewResponse(
                reviews=[
                    GapQuestionWordingJudgment(
                        approved=False,
                        construct_discriminating=False,
                        one_response_task=True,
                        no_unsupported_extension=True,
                        failure_codes=["not_construct_discriminating"],
                    )
                    for _ in payload["items"]
                ]
            ), {"duration_seconds": 1.0}
        return super().call(system, payload, schema, model, effort)


def test_rejected_wording_is_not_reported_as_a_selected_usable_question():
    instrument = authority()
    state = imported_state(instrument)
    append_route(state, instrument)
    original = copy.deepcopy(state)
    fake = AlwaysRejectWording()
    result = run_shadow_fast_spec_path(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh")
    row = privacy_safe_case_summary("case-0001", state, result)
    assert fake.review_count == 2
    assert result["final_questions"] == {}
    assert state == original
    assert row["selected_route_id"] is None
    assert row["shadow_outcome"] == "question_generation_failed"


def test_an_omission_detector_cannot_overrule_independent_gap_rejection():
    instrument = authority()
    state = imported_state(instrument)
    result = run_shadow_triage(
        state, instrument, RejectedFake(), model="gpt-5.6-sol", effort="xhigh"
    )
    candidate = result["triage"].candidates[0]
    audit = GapMatchAudit(
        reviews=[
            GapMatchedRouteReview(
                route_id=candidate.question.route_id,
                source_turn_ids=candidate.source_anchor_turn_ids,
                status="preliminary_gap",
                independent_for_batch=True,
            )
        ]
    )
    admitted, _ = _ordered_admitted_routes(state, result["triage"], result["admission"], audit)
    assert admitted == [], "An omission hint is not an independent full-source admission."


class RecoveryWithAdmission(FastSpecOmissionRecoveryFake):
    def __init__(self):
        super().__init__()
        self.admission_payloads = []

    def call(self, system, payload, schema, model, effort):
        if schema is GapSpecAdmission:
            self.calls.append((system, payload))
            self.admission_payloads.append(payload)
            return GapSpecAdmission(
                source_review_complete=True,
                reviews=[
                    GapSpecAdmissionReview(
                        candidate_id=c["candidate_id"],
                        route_id=c["route_id"],
                        approved=True,
                        source_references_valid=True,
                        not_already_answered=True,
                        premise_supported=True,
                        antecedent_supported=True,
                        context_supported=True,
                        material_information_gain=True,
                        independent_for_batch=True,
                        failure_codes=[],
                    )
                    for c in payload["proposed_gap_specs"]
                ],
            ), {"duration_seconds": 1.0}
        return super().call(system, payload, schema, model, effort)


def test_recovered_gap_gets_independent_admission_over_all_source_before_rendering():
    instrument = authority()
    state = imported_state(instrument)
    append_route(state, instrument, "M09", "planning-scene")
    for n in range(8):
        state["turns"].append(
            {
                "turn_id": f"filler-{n}",
                "turn_role": "behavioral",
                "question_text": "An unrelated situation?",
                "answer_text": "No detail.",
            }
        )
    state["turns"].append(
        {
            "turn_id": "distant-answer",
            "turn_role": "behavioral",
            "question_text": "Anything to add about the software switch?",
            "answer_text": "I only care about reliable offline access, not the trial.",
        }
    )
    fake = RecoveryWithAdmission()
    result = run_shadow_fast_spec_path(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh")
    assert len(fake.admission_payloads) == 1
    assert "distant-answer" in {t["turn_id"] for t in fake.admission_payloads[0]["turns"]}
    stages = [c["shadow_stage"] for c in result["calls"]]
    assert stages.index("GapMatchAdmission") < stages.index("GapQuestionRender")


def test_deferred_audit_cannot_be_reported_as_completed_review():
    instrument = authority()
    state = imported_state(instrument)
    append_route(state, instrument, "M09")
    result = run_shadow_triage(
        state,
        instrument,
        ReadyFake(),
        model="gpt-5.6-sol",
        effort="xhigh",
        match_audit_mode="deferred",
    )
    assert result["match_audit_pending"]
    row = privacy_safe_case_summary("case-0001", state, result)
    assert row["shadow_outcome"] == "review_pending"


def test_match_audit_binds_all_presented_turns_without_four_turn_crash():
    instrument = authority()
    state = imported_state(instrument)
    for n in range(5):
        append_route(state, instrument, "G19", f"same-route-{n}")
    context = make_gap_triage_context(state, instrument)
    result = run_shadow_triage(
        imported_state(instrument), instrument, ReadyFake(), model="gpt-5.6-sol", effort="xhigh"
    )
    audit_context = make_gap_match_audit_context(state, instrument, context, result["triage"])
    response = GapMatchAuditResponse(
        reviews=[
            GapMatchedRouteJudgment(status="answered", independent_for_batch=True)
            for _ in audit_context["pairs"]
        ]
    )
    audit = bind_gap_match_audit(response, audit_context)
    review = next(r for r in audit.reviews if r.route_id == "G19")
    assert review.source_turn_ids == [f"same-route-{n}" for n in range(5)]


def test_paraphrased_antecedent_does_not_remove_unasked_dependent_route_from_fast_menu():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "supper-paraphrase",
            "turn_role": "behavioral",
            "canonical_question_id": None,
            "question_text": (
                "Imagine you've offered to cook a long dinner for you and one friend and "
                "asked them to pick up the groceries, but they tell you covering all of "
                "it would be too much for them. What do you say in response?"
            ),
            "answer_text": (
                "I'd ask about a smaller contribution. I cannot settle whether I usually "
                "want to keep working out a deal or abandon it at that point."
            ),
        }
    )
    context = make_gap_spec_triage_context(state, instrument)
    assert "PREFER-EXCHANGE" in {r["id"] for r in context["candidate_routes"]}
