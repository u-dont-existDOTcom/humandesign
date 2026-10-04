"""Shadow-only clarification triage tests; no external model calls."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from importlib import util
from pathlib import Path
from types import SimpleNamespace

import pytest
from participant.domain import Question, import_record, load_instrument, new_state
from participant.shadow_triage import (
    GAP_ADMISSION_PROMPT,
    GAP_TRIAGE_PROMPT,
    GapAdmission,
    GapCandidate,
    GapCandidateAdmission,
    GapMatchAudit,
    GapMatchedRouteReview,
    GapTriage,
    make_gap_match_audit_context,
    make_gap_triage_context,
    privacy_safe_case_summary,
    run_shadow_triage,
    validate_gap_admission,
    validate_gap_triage,
)

ROOT = Path(__file__).resolve().parents[3]
SURVEY = ROOT / "tasks/scenario-survey-v7-redesign-20260922"
CONTROLLER = ROOT / "tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md"
BENCHMARK = ROOT / "apps/life-patterns-participant/scripts/benchmark_shadow_triage.py"
PRIVATE_SENTINEL = "PRIVATE-SOURCE-SENTINEL-DO-NOT-LOG"


def authority() -> dict:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        for name in (
            "INTERVIEW-PROTOCOL-v6.md",
            "interviewer-bank-v7.json",
            "EVIDENCE-GUIDE-v7.json",
        ):
            (root / name).write_bytes((SURVEY / name).read_bytes())
        (root / CONTROLLER.name).write_bytes(CONTROLLER.read_bytes())
        return load_instrument(root)


def source_record() -> dict:
    return {
        "schema": "life-patterns-full-survey-participant-export-v2",
        "collection_mode": "chatgpt_text",
        "turns": [
            {
                "turn_id": "private-upstream-id",
                "question_text": "Describe a recent decision.",
                "answer_text": PRIVATE_SENTINEL + " I paused before deciding.",
            },
            {
                "turn_id": "metadata-id",
                "turn_role": "collection_metadata",
                "question_text": "Collection mode?",
                "answer_text": "typed",
            },
        ],
    }


def imported_state(instrument: dict) -> dict:
    state = new_state("shadow-test", "gpt-5.6-sol", "xhigh")
    import_record(state, source_record(), "prior_json", instrument, "chatgpt_text")
    state["consent"] = True
    state["phase"] = "ready"
    return state


class ApprovedFake:
    configured = True

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.selected_route: dict | None = None

    def call(self, system, payload, schema, model, effort):
        self.calls.append((system, payload))
        if schema is GapTriage:
            route = next(
                row
                for row in payload["candidate_routes"]
                if row["candidate_mode"] == "unasked" and row["self_contained"]
            )
            self.selected_route = route
            return (
                GapTriage(
                    decision="clarification_needed",
                    candidates=[
                        GapCandidate(
                            candidate_id="C1",
                            rank=1,
                            source_anchor_turn_ids=[payload["turns"][0]["turn_id"]],
                            question=Question(
                                route_id=route["id"],
                                route_type="canonical",
                                text=route["question"],
                                antecedent_turn_ids=[],
                                equivalent_context=False,
                                missing_distinction="A material contrast remains unresolved.",
                                why_useful="The answer could change the route interpretation.",
                            ),
                        )
                    ],
                ),
                {
                    "duration_seconds": 40.0,
                    "prompt_tokens": 12000,
                    "completion_tokens": 900,
                },
            )
        assert schema is GapAdmission
        assert self.selected_route is not None
        return (
            GapAdmission(
                source_review_complete=True,
                reviews=[
                    GapCandidateAdmission(
                        candidate_id="C1",
                        route_id=self.selected_route["id"],
                        approved=True,
                        source_references_valid=True,
                        not_already_answered=True,
                        premise_supported=True,
                        antecedent_supported=True,
                        context_supported=True,
                        construct_discriminating=True,
                        one_response_task=True,
                        material_information_gain=True,
                        independent_for_batch=True,
                        no_unsupported_extension=True,
                        failure_codes=[],
                    )
                ],
            ),
            {
                "duration_seconds": 20.0,
                "prompt_tokens": 12500,
                "completion_tokens": 250,
            },
        )


class RejectedFake(ApprovedFake):
    def call(self, system, payload, schema, model, effort):
        if schema is GapTriage:
            return super().call(system, payload, schema, model, effort)
        self.calls.append((system, payload))
        assert self.selected_route is not None
        return (
            GapAdmission(
                source_review_complete=True,
                reviews=[
                    GapCandidateAdmission(
                        candidate_id="C1",
                        route_id=self.selected_route["id"],
                        approved=False,
                        source_references_valid=True,
                        not_already_answered=False,
                        premise_supported=True,
                        antecedent_supported=True,
                        context_supported=True,
                        construct_discriminating=True,
                        one_response_task=True,
                        material_information_gain=False,
                        independent_for_batch=True,
                        no_unsupported_extension=True,
                        failure_codes=["already_answered", "low_information_gain"],
                    )
                ],
            ),
            {"duration_seconds": 12.0, "prompt_tokens": 12300, "completion_tokens": 180},
        )


class ReadyFake:
    def __init__(self) -> None:
        self.count = 0

    def call(self, system, payload, schema, model, effort):
        self.count += 1
        assert schema is GapTriage
        return (
            GapTriage(
                decision="review_ready",
                candidates=[],
            ),
            {"duration_seconds": 10.0, "prompt_tokens": 10000, "completion_tokens": 80},
        )


class OmissionRecoveryFake:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, system, payload, schema, model, effort):
        self.calls.append((system, payload))
        if schema is GapTriage:
            return (
                GapTriage(decision="review_ready", candidates=[]),
                {"duration_seconds": 8.0, "prompt_tokens": 10000, "completion_tokens": 80},
            )

        assert schema is GapMatchAudit
        matched = []
        for pair in payload["pairs"]:
            route_id = pair["route_id"]
            matched.append(
                GapMatchedRouteReview(
                    route_id=route_id,
                    source_turn_ids=list(pair["source_turn_ids"]),
                    status="preliminary_gap" if route_id == "M09" else "answered",
                    independent_for_batch=True,
                )
            )
        return (
            GapMatchAudit(reviews=matched),
            {"duration_seconds": 12.0, "prompt_tokens": 11000, "completion_tokens": 220},
        )


class TwoCandidateFake(ApprovedFake):
    def call(self, system, payload, schema, model, effort):
        self.calls.append((system, payload))
        if schema is GapTriage:
            routes = [
                row
                for row in payload["candidate_routes"]
                if row["candidate_mode"] == "unasked" and row["self_contained"]
            ][:2]
            self.selected_route = routes[0]
            candidates = []
            for index, route in enumerate(routes, 1):
                candidates.append(
                    GapCandidate(
                        candidate_id=f"C{index}",
                        rank=index,
                        source_anchor_turn_ids=[payload["turns"][0]["turn_id"]],
                        question=Question(
                            route_id=route["id"],
                            route_type="canonical",
                            text=route["question"],
                            antecedent_turn_ids=[],
                            equivalent_context=False,
                            missing_distinction="A material contrast remains unresolved.",
                            why_useful="The answer could change the route interpretation.",
                        ),
                    )
                )
            return (
                GapTriage(
                    decision="clarification_needed",
                    candidates=candidates,
                ),
                {"duration_seconds": 30.0, "prompt_tokens": 11000, "completion_tokens": 700},
            )

        reviews = []
        for candidate in reversed(payload["proposed_candidates"]):
            reviews.append(
                GapCandidateAdmission(
                    candidate_id=candidate["candidate_id"],
                    route_id=candidate["question"]["route_id"],
                    approved=True,
                    source_references_valid=True,
                    not_already_answered=True,
                    premise_supported=True,
                    antecedent_supported=True,
                    context_supported=True,
                    construct_discriminating=True,
                    one_response_task=True,
                    material_information_gain=True,
                    independent_for_batch=True,
                    no_unsupported_extension=True,
                    failure_codes=[],
                )
            )
        return (
            GapAdmission(source_review_complete=True, reviews=reviews),
            {"duration_seconds": 15.0, "prompt_tokens": 11500, "completion_tokens": 300},
        )


def test_triage_context_adds_conservative_source_question_route_hints():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].extend(
        [
            {
                "turn_id": "near-m09",
                "turn_role": "behavioral",
                "question_text": (
                    "You have a familiar simple offline planning app and could move to a more "
                    "complex one with shared reminders and better search, which would take about "
                    "an hour to migrate. What matters in deciding whether to switch?"
                ),
                "answer_text": "I would begin by reading reviews and checking the import tool.",
            },
            {
                "turn_id": "near-g19",
                "turn_role": "behavioral",
                "question_text": (
                    "You promised to help a friend move, and it is running long into your own "
                    "personal time. What matters in deciding what to do?"
                ),
                "answer_text": "I would first ask how much is left.",
            },
        ]
    )
    context = make_gap_triage_context(state, instrument)
    routes = {route["id"]: route for route in context["candidate_routes"]}
    assert routes["M09"]["source_question_match_turn_ids"] == ["near-m09"]
    assert routes["G19"]["source_question_match_turn_ids"] == ["near-g19"]
    assert [
        (match["route_id"], match["turn_ids"])
        for match in context["source_question_matches"][:2]
    ] == [
        ("M09", ["near-m09"]),
        ("G19", ["near-g19"]),
    ]
    for match in context["source_question_matches"][:2]:
        assert {"near-m09", "near-g19"}.issubset(set(match["context_turn_ids"]))


def test_triage_context_audits_presented_route_as_exact_source_question_match():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "presented-g19",
            "turn_role": "behavioral",
            "canonical_question_id": "G19",
            "question_text": (
                "You promised to help a friend move, but it is taking longer than expected "
                "and using your personal time. What would matter most in deciding what to do?"
            ),
            "answer_text": "I would talk it through with my friend first and see how they feel.",
        }
    )
    context = make_gap_triage_context(state, instrument)
    route = next(row for row in context["candidate_routes"] if row["id"] == "G19")
    assert route["candidate_mode"] == "repair_only"
    assert route["source_question_match_turn_ids"] == ["presented-g19"]
    match = next(
        item for item in context["source_question_matches"] if item["route_id"] == "G19"
    )
    assert match["turn_ids"] == ["presented-g19"]
    assert "presented-g19" in match["context_turn_ids"]


def test_match_audit_context_includes_nearby_route_contradiction():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].extend(
        [
            {
                "turn_id": "meal-match",
                "turn_role": "behavioral",
                "question_text": (
                    "You arrive at a relaxed dinner with friends and nobody assigned you "
                    "anything. What do you notice first?"
                ),
                "answer_text": "I head toward the kitchen and see what is missing.",
            },
            {
                "turn_id": "intervening-planner",
                "turn_role": "behavioral",
                "question_text": "How would you test a new planning app?",
                "answer_text": "I would try it briefly.",
            },
            {
                "turn_id": "meal-contradiction",
                "turn_role": "behavioral",
                "question_text": (
                    "At a gathering like that, where does your attention usually go?"
                ),
                "answer_text": (
                    "Mostly the people. I do not really look at the kitchen or what needs doing."
                ),
            },
        ]
    )
    triage_context = make_gap_triage_context(state, instrument)
    match = next(
        item for item in triage_context["source_question_matches"] if item["route_id"] == "G23"
    )
    assert match["turn_ids"] == ["meal-match"]
    assert "meal-contradiction" in match["context_turn_ids"]

    audit_context = make_gap_match_audit_context(
        state,
        instrument,
        triage_context,
        GapTriage(decision="review_ready", candidates=[]),
    )
    pair = next(item for item in audit_context["pairs"] if item["route_id"] == "G23")
    assert "meal-contradiction" in pair["context_turn_ids"]
    source_ids = {turn["turn_id"] for turn in audit_context["source_turns"]}
    assert {"meal-match", "meal-contradiction"}.issubset(source_ids)


def test_contradictory_match_audit_recovers_route():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "meal-match",
            "turn_role": "behavioral",
            "question_text": "At a casual meal, what catches your attention first?",
            "answer_text": "I notice the kitchen and what is missing.",
        }
    )
    triage = GapTriage(decision="review_ready", candidates=[])
    admission = GapAdmission(source_review_complete=True, reviews=[])
    audit = GapMatchAudit(
        reviews=[
            GapMatchedRouteReview(
                route_id="G23",
                source_turn_ids=["meal-match"],
                status="contradictory_gap",
                independent_for_batch=True,
            )
        ]
    )
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        {
            "triage": triage,
            "admission": admission,
            "match_audit": audit,
            "calls": [],
            "triage_context_chars": 0,
            "admission_context_chars": 0,
            "match_audit_context_chars": 0,
            "eligible_route_count": 1,
        },
    )
    assert summary["admitted_route_ids"] == ["G23"]
    assert summary["recovered_omission_route_ids"] == ["G23"]


def test_triage_context_has_complete_source_and_no_evidence_deliverables():
    instrument = authority()
    context = make_gap_triage_context(imported_state(instrument), instrument)
    assert context["shadow_only"] is True
    assert len(context["turns"]) == 1
    assert PRIVATE_SENTINEL in context["turns"][0]["answer_text"]
    assert context["candidate_routes"]
    assert "existing_evidence" not in context
    assert "candidate_evidence_guide" not in context
    assert "addressed_routes" not in context
    assert all("interpretation_limit" not in route for route in context["candidate_routes"])


def test_shadow_pipeline_uses_separate_triage_and_admission_without_mutating_state():
    instrument = authority()
    state = imported_state(instrument)
    before = json.dumps(state, sort_keys=True)
    fake = ApprovedFake()
    result = run_shadow_triage(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh")
    assert json.dumps(state, sort_keys=True) == before
    assert [call["shadow_stage"] for call in result["calls"]] == [
        "GapTriage",
        "GapAdmission",
    ]
    assert fake.calls[0][0] == GAP_TRIAGE_PROMPT
    assert fake.calls[1][0] == GAP_ADMISSION_PROMPT
    assert fake.calls[1][1]["turns"] == fake.calls[0][1]["turns"]
    assert fake.calls[1][1]["selected_routes"]
    assert "proposed_triage" not in fake.calls[1][1]
    assert "decision" not in fake.calls[1][1]["proposed_candidates"][0]
    assert "defect_flags" not in fake.calls[1][1]["proposed_candidates"][0]
    assert "material_change" not in fake.calls[1][1]["proposed_candidates"][0]
    assert fake.calls[1][1]["proposed_candidates"][0]["source_anchor_turn_ids"] == [
        fake.calls[0][1]["turns"][0]["turn_id"]
    ]
    summary = privacy_safe_case_summary("case-0001", state, result)
    encoded = json.dumps(summary)
    assert summary["shadow_outcome"] == "clarification_recommended"
    assert summary["selected_route_id"] == fake.selected_route["id"]
    assert summary["semantic_duration_seconds"] == 60.0
    assert PRIVATE_SENTINEL not in encoded
    assert "import-0001" not in encoded
    assert "question_text" not in encoded


def test_all_rejected_candidates_remain_unresolved_not_review_ready():
    instrument = authority()
    state = imported_state(instrument)
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        run_shadow_triage(state, instrument, RejectedFake(), model="gpt-5.6-sol", effort="xhigh"),
    )
    assert summary["triage_decision"] == "clarification_needed"
    assert summary["shadow_outcome"] == "no_admitted_candidate"
    assert summary["selected_route_id"] is None
    assert summary["rejection_code_counts"] == {
        "already_answered": 1,
        "low_information_gain": 1,
    }


def test_review_ready_skips_empty_admission_round_trip():
    instrument = authority()
    state = imported_state(instrument)
    fake = ReadyFake()
    result = run_shadow_triage(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh")
    assert fake.count == 1
    assert len(result["calls"]) == 1
    assert result["admission_context_chars"] == 0
    assert privacy_safe_case_summary("case-0001", state, result)["shadow_outcome"] == (
        "review_ready"
    )


def test_admission_recovers_source_matched_gap_omitted_by_triage():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "near-m09",
            "turn_role": "behavioral",
            "question_text": (
                "You have a familiar simple offline planning app and could move to a more "
                "complex one with shared reminders and better search, which would take about "
                "an hour to migrate. What matters in deciding whether to switch?"
            ),
            "answer_text": "I would begin by reading reviews and checking the import tool.",
        }
    )
    fake = OmissionRecoveryFake()
    result = run_shadow_triage(
        state, instrument, fake, model="gpt-5.6-sol", effort="xhigh"
    )
    summary = privacy_safe_case_summary("case-0001", state, result)
    assert len(fake.calls) == 2
    assert fake.calls[1][1]["pairs"]
    assert summary["triage_decision"] == "review_ready"
    assert summary["shadow_outcome"] == "clarification_recommended"
    assert summary["admitted_route_ids"] == ["M09"]
    assert summary["recovered_omission_route_ids"] == ["M09"]


def test_match_audit_can_recover_proposed_route_rejected_only_on_answer_completeness():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "near-g19",
            "turn_role": "behavioral",
            "question_text": (
                "You promised to help a friend move, and it is running long into your own "
                "personal time. They are open to changing the arrangement. What matters most "
                "when deciding what to do?"
            ),
            "answer_text": "I would talk it through with my friend first and see how they feel.",
        }
    )
    triage_context = make_gap_triage_context(state, instrument)
    route = next(row for row in triage_context["candidate_routes"] if row["id"] == "G19")
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=["near-g19"],
                question=Question(
                    route_id="G19",
                    route_type="canonical",
                    text=route["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="The deciding factor remains unstated.",
                    why_useful="It could change interpretation of the response.",
                ),
            )
        ],
    )
    match_context = make_gap_match_audit_context(
        state, instrument, triage_context, triage
    )
    pair = next(item for item in match_context["pairs"] if item["route_id"] == "G19")
    assert pair["source_turn_ids"] == ["near-g19"]

    admission = GapAdmission(
        source_review_complete=True,
        reviews=[
            GapCandidateAdmission(
                candidate_id="C1",
                route_id="G19",
                approved=False,
                source_references_valid=True,
                not_already_answered=False,
                premise_supported=True,
                antecedent_supported=True,
                context_supported=True,
                construct_discriminating=True,
                one_response_task=True,
                material_information_gain=False,
                independent_for_batch=True,
                no_unsupported_extension=True,
                failure_codes=["already_answered", "low_information_gain"],
            )
        ],
    )
    audit = GapMatchAudit(
        reviews=[
            GapMatchedRouteReview(
                route_id="G19",
                source_turn_ids=["near-g19"],
                status="preliminary_gap",
                independent_for_batch=True,
            )
        ]
    )
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        {
            "triage": triage,
            "admission": admission,
            "match_audit": audit,
            "calls": [],
            "triage_context_chars": 0,
            "admission_context_chars": 0,
            "match_audit_context_chars": 0,
            "eligible_route_count": len(triage_context["candidate_routes"]),
        },
    )
    assert summary["admitted_route_ids"] == ["G19"]
    assert summary["recovered_omission_route_ids"] == ["G19"]


def test_match_audit_does_not_override_non_answer_admission_failure():
    instrument = authority()
    state = imported_state(instrument)
    state["turns"].append(
        {
            "turn_id": "near-g19",
            "turn_role": "behavioral",
            "question_text": (
                "You promised to help a friend move, and it is running long into your own "
                "personal time. They are open to changing the arrangement. What matters most "
                "when deciding what to do?"
            ),
            "answer_text": "I would talk it through with my friend first and see how they feel.",
        }
    )
    triage_context = make_gap_triage_context(state, instrument)
    route = next(row for row in triage_context["candidate_routes"] if row["id"] == "G19")
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=["near-g19"],
                question=Question(
                    route_id="G19",
                    route_type="canonical",
                    text=route["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="The deciding factor remains unstated.",
                    why_useful="It could change interpretation of the response.",
                ),
            )
        ],
    )
    admission = GapAdmission(
        source_review_complete=True,
        reviews=[
            GapCandidateAdmission(
                candidate_id="C1",
                route_id="G19",
                approved=False,
                source_references_valid=True,
                not_already_answered=False,
                premise_supported=False,
                antecedent_supported=True,
                context_supported=True,
                construct_discriminating=True,
                one_response_task=True,
                material_information_gain=False,
                independent_for_batch=True,
                no_unsupported_extension=True,
                failure_codes=[
                    "already_answered",
                    "unsupported_premise",
                    "low_information_gain",
                ],
            )
        ],
    )
    audit = GapMatchAudit(
        reviews=[
            GapMatchedRouteReview(
                route_id="G19",
                source_turn_ids=["near-g19"],
                status="preliminary_gap",
                independent_for_batch=True,
            )
        ]
    )
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        {
            "triage": triage,
            "admission": admission,
            "match_audit": audit,
            "calls": [],
            "triage_context_chars": 0,
            "admission_context_chars": 0,
            "match_audit_context_chars": 0,
            "eligible_route_count": len(triage_context["candidate_routes"]),
        },
    )
    assert summary["admitted_route_ids"] == []
    assert summary["recovered_omission_route_ids"] == []


def test_selected_candidate_follows_triage_rank_not_admission_review_order():
    instrument = authority()
    state = imported_state(instrument)
    fake = TwoCandidateFake()
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        run_shadow_triage(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh"),
    )
    proposed = [
        candidate["question"]["route_id"] for candidate in fake.calls[1][1]["proposed_candidates"]
    ]
    assert summary["admitted_route_ids"] == proposed
    assert summary["selected_route_id"] == proposed[0]


def test_admitted_batch_order_follows_source_anchor_order_not_model_rank():
    instrument = authority()
    state = imported_state(instrument)
    first_turn_id = state["turns"][0]["turn_id"]
    state["turns"].append(
        {
            "turn_id": "later-behavioral-turn",
            "turn_role": "behavioral",
            "question_text": "Later synthetic question.",
            "answer_text": "Later synthetic answer.",
        }
    )
    context = make_gap_triage_context(state, instrument)
    routes = [
        route
        for route in context["candidate_routes"]
        if route["candidate_mode"] == "unasked" and route["self_contained"]
    ][:2]
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=["later-behavioral-turn"],
                question=Question(
                    route_id=routes[0]["id"],
                    route_type="canonical",
                    text=routes[0]["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="Later source gap.",
                    why_useful="Material.",
                ),
            ),
            GapCandidate(
                candidate_id="C2",
                rank=2,
                source_anchor_turn_ids=[first_turn_id],
                question=Question(
                    route_id=routes[1]["id"],
                    route_type="canonical",
                    text=routes[1]["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="Earlier source gap.",
                    why_useful="Material.",
                ),
            ),
        ],
    )
    admission = GapAdmission(
        source_review_complete=True,
        reviews=[
            GapCandidateAdmission(
                candidate_id=candidate.candidate_id,
                route_id=candidate.question.route_id,
                approved=True,
                source_references_valid=True,
                not_already_answered=True,
                premise_supported=True,
                antecedent_supported=True,
                context_supported=True,
                construct_discriminating=True,
                one_response_task=True,
                material_information_gain=True,
                independent_for_batch=True,
                no_unsupported_extension=True,
                failure_codes=[],
            )
            for candidate in triage.candidates
        ],
    )
    summary = privacy_safe_case_summary(
        "case-0001",
        state,
        {
            "triage": triage,
            "admission": admission,
            "match_audit": GapMatchAudit(reviews=[]),
            "calls": [],
            "triage_context_chars": 0,
            "admission_context_chars": 0,
            "match_audit_context_chars": 0,
            "eligible_route_count": len(context["candidate_routes"]),
        },
    )
    assert summary["admitted_route_ids"] == [routes[1]["id"], routes[0]["id"]]
    assert summary["selected_route_id"] == routes[1]["id"]


def test_admission_gate_and_failure_codes_must_match_exactly():
    instrument = authority()
    state = imported_state(instrument)
    result = run_shadow_triage(
        state, instrument, ApprovedFake(), model="gpt-5.6-sol", effort="xhigh"
    )
    triage = result["triage"]
    bad = GapAdmission(
        source_review_complete=True,
        reviews=[
            GapCandidateAdmission(
                candidate_id="C1",
                route_id=triage.candidates[0].question.route_id,
                approved=False,
                source_references_valid=True,
                not_already_answered=False,
                premise_supported=True,
                antecedent_supported=True,
                context_supported=True,
                construct_discriminating=True,
                one_response_task=True,
                material_information_gain=True,
                independent_for_batch=True,
                no_unsupported_extension=True,
                failure_codes=["low_information_gain"],
            )
        ],
    )
    with pytest.raises(ValueError, match="failure codes"):
        validate_gap_admission(bad, triage)


def test_admission_cannot_mark_a_declared_dependency_independent_for_batch():
    instrument = authority()
    state = imported_state(instrument)
    result = run_shadow_triage(
        state, instrument, TwoCandidateFake(), model="gpt-5.6-sol", effort="xhigh"
    )
    candidates = list(result["triage"].candidates)
    candidates[1] = candidates[1].model_copy(update={"depends_on_candidate_ids": ["C1"]})
    triage = result["triage"].model_copy(update={"candidates": candidates})
    with pytest.raises(ValueError, match="dependent gap candidate"):
        validate_gap_admission(result["admission"], triage)


def test_complete_81_turn_source_reaches_both_calls_and_excludes_nonbehavioral_source():
    instrument = authority()
    record = {
        "collection_mode": "chatgpt_text",
        "turns": [
            {
                "turn_id": f"source-{index}",
                "question_text": f"Question {index}",
                "answer_text": f"Exact answer {index}",
            }
            for index in range(1, 83)
        ]
        + [
            {
                "turn_id": "metadata",
                "turn_role": "collection_metadata",
                "question_text": "Collection mode?",
                "answer_text": "voice",
            }
        ],
    }
    state = new_state("shadow-test", "gpt-5.6-sol", "xhigh")
    import_record(state, record, "prior_json", instrument, "chatgpt_text")
    state["turns"][40]["quarantined"] = True
    fake = ApprovedFake()
    run_shadow_triage(state, instrument, fake, model="gpt-5.6-sol", effort="xhigh")
    assert len(fake.calls[0][1]["turns"]) == 81
    assert fake.calls[1][1]["turns"] == fake.calls[0][1]["turns"]
    assert all(turn["turn_id"] != "import-0041" for turn in fake.calls[0][1]["turns"])
    assert all(turn["question_text"] != "Collection mode?" for turn in fake.calls[0][1]["turns"])


def test_triage_rejects_unknown_source_anchor_turn():
    instrument = authority()
    state = imported_state(instrument)
    context = make_gap_triage_context(state, instrument)
    route = next(
        row
        for row in context["candidate_routes"]
        if row["candidate_mode"] == "unasked" and row["self_contained"]
    )
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=["missing-source-anchor"],
                question=Question(
                    route_id=route["id"],
                    route_type="canonical",
                    text=route["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="Unresolved.",
                    why_useful="Material.",
                ),
                depends_on_candidate_ids=[],
            )
        ],
    )
    with pytest.raises(ValueError, match="unknown source anchor turn"):
        validate_gap_triage(triage, state, instrument, context)


def test_triage_rejects_noncontiguous_or_forward_candidate_dependencies():
    instrument = authority()
    state = imported_state(instrument)
    context = make_gap_triage_context(state, instrument)
    route = next(
        row
        for row in context["candidate_routes"]
        if row["candidate_mode"] == "unasked" and row["self_contained"]
    )
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=[context["turns"][0]["turn_id"]],
                question=Question(
                    route_id=route["id"],
                    route_type="canonical",
                    text=route["question"],
                    antecedent_turn_ids=[],
                    equivalent_context=False,
                    missing_distinction="Unresolved.",
                    why_useful="Material.",
                ),
                depends_on_candidate_ids=["C2"],
            )
        ],
    )
    with pytest.raises(ValueError, match="earlier ranked"):
        validate_gap_triage(triage, state, instrument, context)


def test_canonical_self_contained_gap_cannot_invent_antecedent():
    instrument = authority()
    state = imported_state(instrument)
    context = make_gap_triage_context(state, instrument)
    route = next(
        row
        for row in context["candidate_routes"]
        if row["candidate_mode"] == "unasked" and row["self_contained"]
    )
    triage = GapTriage(
        decision="clarification_needed",
        candidates=[
            GapCandidate(
                candidate_id="C1",
                rank=1,
                source_anchor_turn_ids=[context["turns"][0]["turn_id"]],
                question=Question(
                    route_id=route["id"],
                    route_type="canonical",
                    text=route["question"],
                    antecedent_turn_ids=[context["turns"][0]["turn_id"]],
                    equivalent_context=False,
                    missing_distinction="Unresolved.",
                    why_useful="Material.",
                ),
                depends_on_candidate_ids=[],
            )
        ],
    )
    with pytest.raises(ValueError, match="self-contained route cannot cite"):
        validate_gap_triage(triage, state, instrument, context)


def test_benchmark_dry_run_output_and_console_are_privacy_safe(tmp_path):
    private_input = tmp_path / "participant-private-name.json"
    private_input.write_text(json.dumps(source_record()), encoding="utf-8")
    output = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(BENCHMARK),
            str(private_input),
            "--output",
            str(output),
            "--dry-run",
        ],
        env=dict(os.environ, PYTHONPATH=str(ROOT / "apps/life-patterns-participant")),
        check=True,
        capture_output=True,
        text=True,
    )
    report_text = output.read_text(encoding="utf-8")
    combined = result.stdout + result.stderr + report_text
    assert PRIVATE_SENTINEL not in combined
    assert private_input.name not in combined
    assert "private-upstream-id" not in combined
    assert "question_text" not in report_text
    assert "answer_text" not in report_text
    assert "sha256" not in report_text.lower()
    assert "content_hash" not in report_text.lower()
    report = json.loads(report_text)
    assert report["shadow_only"] is True
    assert report["live_behavior_changed"] is False
    assert report["model_calls_executed"] is False
    assert report["cases"][0]["case_id"] == "case-0001"
    assert output.stat().st_mode & 0o777 == 0o600


def test_legacy_comparison_requires_exact_selected_route_not_any_admitted_route():
    spec = util.spec_from_file_location("shadow_benchmark", BENCHMARK)
    assert spec and spec.loader
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    row = {
        "shadow_outcome": "clarification_recommended",
        "selected_route_id": "R-first",
        "admitted_route_ids": ["R-first", "R-second"],
        "semantic_duration_seconds": 50.0,
    }
    legacy = SimpleNamespace(
        case_id="case-0001",
        decision="clarification_needed",
        selected_route_ids=["R-second"],
        semantic_duration_seconds=100.0,
    )
    comparison = module._legacy_comparison(row, legacy)
    assert comparison == {
        "decision_match": True,
        "legacy_clarification_needed": True,
        "selected_route_match": False,
        "legacy_semantic_duration_seconds": 100.0,
        "speedup_ratio": 2.0,
    }


def test_legacy_results_loader_accepts_declared_privacy_safe_schema(tmp_path):
    spec = util.spec_from_file_location("shadow_benchmark_loader", BENCHMARK)
    assert spec and spec.loader
    module = util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    legacy_path = tmp_path / "legacy.json"
    legacy_path.write_text(
        json.dumps(
            {
                "schema": "life-patterns-legacy-triage-benchmark-v1",
                "cases": [
                    {
                        "case_id": "case-0001",
                        "decision": "review_ready",
                        "selected_route_ids": [],
                        "semantic_duration_seconds": 120.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    loaded = module._load_legacy(legacy_path)
    assert list(loaded) == ["case-0001"]
    assert loaded["case-0001"].decision == "review_ready"


def test_aggregate_counts_missed_legacy_clarification_as_route_mismatch():
    spec = util.spec_from_file_location("shadow_benchmark_aggregate", BENCHMARK)
    assert spec and spec.loader
    module = util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    aggregate = module._aggregate(
        [
            {
                "shadow_outcome": "no_admitted_candidate",
                "semantic_duration_seconds": 30.0,
                "legacy_comparison": {
                    "decision_match": False,
                    "legacy_clarification_needed": True,
                    "selected_route_match": False,
                },
            }
        ]
    )
    assert aggregate["clarification_selected_route_match_rate"] == 0.0


def test_shadow_module_is_not_imported_by_any_live_surface():
    live_paths = [
        ROOT / "apps/life-patterns-participant/participant/engine.py",
        ROOT / "apps/life-patterns-participant/participant/app.py",
        ROOT / "apps/life-patterns-participant/scripts/gpt_review_worker.py",
    ]
    assert all("shadow_triage" not in path.read_text(encoding="utf-8") for path in live_paths)
