from __future__ import annotations

from hdmatch.api.life_patterns_recoverability_domains import RECOVERABILITY_DOMAINS
from hdmatch.api.life_patterns_v2_owner_coverage import StandardizedCoverageOpenAIModel
from hdmatch.api.life_patterns_v2_owner_dynamic_ui import DYNAMIC_RECOVERABILITY_HTML
from hdmatch.api.life_patterns_v2_owner_recoverability import (
    RecoverabilityCoverageOpenAIModel,
    RecoverabilityCoverageRuntime,
    create_life_patterns_v2_owner_recoverability_app,
)


def test_dynamic_selector_uses_existing_answers_instead_of_registry_order(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call(self, **kwargs):
        calls.append(kwargs)
        return {
            "primary_domain_id": RECOVERABILITY_DOMAINS[2].domain_id,
            "opening": "You mentioned that unanswered questions can stay with you. What usually makes one worth returning to?",
            "internal_reason": "This bridges from known material and avoids restarting the partially covered topic.",
        }

    monkeypatch.setattr(StandardizedCoverageOpenAIModel, "_conversation_call_json", fake_call)
    model = RecoverabilityCoverageOpenAIModel(api_key="test")
    plan = model.plan_next_coverage_question(
        open_domains=(RECOVERABILITY_DOMAINS[1], RECOVERABILITY_DOMAINS[2]),
        aggregate_coverage=[
            {
                "domain_id": RECOVERABILITY_DOMAINS[1].domain_id,
                "status": "partial",
                "reason": "The participant already described translating insights into structure but not when they abandon an insight.",
            }
        ],
        completed_results=[
            {
                "status": "accepted",
                "wording": "I keep returning to unresolved questions that feel consequential.",
            }
        ],
    )

    assert plan["primary_domain_id"] == RECOVERABILITY_DOMAINS[2].domain_id
    assert len(calls) == 1
    instructions = str(calls[0]["instructions"])
    assert "NOT a script" in instructions
    assert "must not be re-asked" in instructions
    assert "ask only for the missing discriminator" in instructions
    assert "One question may illuminate several still-open dimensions" in instructions
    payload = calls[0]["payload"]
    assert isinstance(payload, dict)
    assert payload["completed_results"][0]["status"] == "accepted"


class DynamicPlannerModel:
    configured = True

    def plan_next_coverage_question(self, **kwargs):
        open_ids = [domain.domain_id for domain in kwargs["open_domains"]]
        assert RECOVERABILITY_DOMAINS[0].domain_id not in open_ids
        assert RECOVERABILITY_DOMAINS[1].domain_id in open_ids
        return {
            "primary_domain_id": RECOVERABILITY_DOMAINS[1].domain_id,
            "opening": "Building on what you already said, when does an insight become something you actually organize or build?",
            "internal_reason": "Use existing context and target the still-open part.",
        }


def test_runtime_skips_completed_dimension_and_seeds_natural_next_question() -> None:
    runtime = RecoverabilityCoverageRuntime(model=DynamicPlannerModel())  # type: ignore[arg-type]
    session, domain, opening = runtime.create_dynamic_coverage_session(
        aggregate_coverage=[
            {
                "domain_id": RECOVERABILITY_DOMAINS[0].domain_id,
                "status": "sufficient",
                "reason": "Already established from participant-led material.",
            },
            {
                "domain_id": RECOVERABILITY_DOMAINS[1].domain_id,
                "status": "partial",
                "reason": "Some relevant information is already present.",
            },
        ],
        completed_results=[
            {"status": "accepted", "wording": "I naturally organize complex material into structures."}
        ],
    )

    assert domain.domain_id == RECOVERABILITY_DOMAINS[1].domain_id
    assert opening.startswith("Building on what you already said")
    assert session.conversation[-1]["text"] == opening
    assert session.pattern_focus_established is True


def test_new_participant_led_thread_receives_planning_only_prior_context() -> None:
    runtime = RecoverabilityCoverageRuntime(model=DynamicPlannerModel())  # type: ignore[arg-type]
    session = runtime.create_contextual_session(
        aggregate_coverage=[
            {
                "domain_id": RECOVERABILITY_DOMAINS[0].domain_id,
                "status": "sufficient",
                "reason": "The earlier thread already established this dimension.",
            }
        ],
        completed_results=[
            {"status": "accepted", "wording": "I tend to structure complex material."},
            {"status": "rejected", "wording": "This should not be treated as settled."},
        ],
    )

    assert len(session.conversation) == 1
    note = session.conversation[0]["text"]
    assert note.startswith("INTERNAL PRIOR CONTEXT — PLANNING ONLY, NOT PARTICIPANT EVIDENCE")
    assert "I tend to structure complex material." in note
    assert "This should not be treated as settled." not in note
    assert "do not extract hidden facts from it" in note.lower()


def test_dynamic_ui_uses_cross_thread_context_and_not_first_missing_category() -> None:
    assert "Continue interview" in DYNAMIC_RECOVERABILITY_HTML
    assert "/api/owner-v2/conversation/coverage/next-session" in DYNAMIC_RECOVERABILITY_HTML
    assert "/api/owner-v2/conversation/sessions/contextual" in DYNAMIC_RECOVERABILITY_HTML
    assert "aggregate_coverage:Object.values(coverageAggregate)" in DYNAMIC_RECOVERABILITY_HTML
    assert "completed_results:completedResults.map" in DYNAMIC_RECOVERABILITY_HTML
    assert "startCoverageDomain(missing[0])" not in DYNAMIC_RECOVERABILITY_HTML
    assert "Still open: '+missing.map(d=>d.title)" not in DYNAMIC_RECOVERABILITY_HTML
    assert "One answer can cover several areas" in DYNAMIC_RECOVERABILITY_HTML
    assert "adaptive coverage" not in DYNAMIC_RECOVERABILITY_HTML


def test_dynamic_ui_has_persistent_progress_and_rough_remaining_estimate() -> None:
    assert 'id="interviewProgress"' in DYNAMIC_RECOVERABILITY_HTML
    assert 'id="progressBar"' in DYNAMIC_RECOVERABILITY_HTML
    assert 'id="progressText"' in DYNAMIC_RECOVERABILITY_HTML
    assert "function coverageMetrics()" in DYNAMIC_RECOVERABILITY_HTML
    assert "function renderProgress()" in DYNAMIC_RECOVERABILITY_HTML
    assert "roughly ${m.lowQ}–${m.highQ} questions left" in DYNAMIC_RECOVERABILITY_HTML
    assert "Very rough time estimate" in DYNAMIC_RECOVERABILITY_HTML
    assert "One answer can cover several areas" in DYNAMIC_RECOVERABILITY_HTML
    assert "renderProgress();" in DYNAMIC_RECOVERABILITY_HTML


def test_health_declares_dynamic_coverage_and_cross_thread_reuse() -> None:
    app = create_life_patterns_v2_owner_recoverability_app(
        model=DynamicPlannerModel()  # type: ignore[arg-type]
    )
    health_route = next(route for route in app.routes if getattr(route, "path", None) == "/healthz")
    payload = health_route.endpoint()

    assert payload["dynamic_coverage_selection"] is True
    assert payload["cross_thread_coverage_reuse"] is True
    assert payload["cross_thread_planning_context"] is True
    assert payload["canonical_screeners_are_fallbacks_not_script"] is True
