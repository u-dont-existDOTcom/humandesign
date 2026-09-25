from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_conversation import HiddenFactCandidate, TurnExtraction
from hdmatch.api.life_patterns_v2_owner_coverage import (
    COVERAGE_BLUEPRINT_SHA256,
    COVERAGE_BLUEPRINT_VERSION,
    COVERAGE_HTML,
    COVERAGE_STATUSES,
    REQUIRED_COVERAGE_DOMAINS,
    StandardizedCoverageRuntime,
    _normalize_coverage,
    create_life_patterns_v2_owner_coverage_app,
)


def test_required_coverage_blueprint_is_versioned_unique_and_stable_shape() -> None:
    ids = [domain.domain_id for domain in REQUIRED_COVERAGE_DOMAINS]

    assert COVERAGE_BLUEPRINT_VERSION == "life-patterns-required-coverage-v1"
    assert len(REQUIRED_COVERAGE_DOMAINS) == 10
    assert len(ids) == len(set(ids))
    assert len(COVERAGE_BLUEPRINT_SHA256) == 64
    assert set(COVERAGE_STATUSES) == {
        "unassessed",
        "partial",
        "sufficient",
        "unknown",
        "inapplicable",
        "declined",
    }
    assert "decision_process" in ids
    assert "emotion_regulation" in ids
    assert "developmental_change" in ids


def test_coverage_ui_has_required_sweep_without_claiming_forced_completion() -> None:
    assert "Continue required coverage" in COVERAGE_HTML
    assert "/api/owner-v2/conversation/coverage/sessions" in COVERAGE_HTML
    assert "remaining domains explicitly marked incomplete" in COVERAGE_HTML


class CoverageSessionModel:
    configured = True

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Decision process",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition="I usually need time before an uncertain important decision feels clear.",
                ),
            ),
        )


def test_required_domain_session_begins_from_canonical_screener() -> None:
    runtime = StandardizedCoverageRuntime(model=CoverageSessionModel())  # type: ignore[arg-type]

    session, domain = runtime.create_coverage_session("decision_process")

    assert session.pattern_focus_established is True
    assert session.conversation[-1]["role"] == "assistant"
    assert session.conversation[-1]["text"] == domain.canonical_screener
    assert "important choice" in domain.canonical_screener


def test_normalize_coverage_requires_cited_fact_for_partial_or_sufficient() -> None:
    class Fact:
        fact_id = "F1"

    raw = {
        "assessments": [
            {
                "domain_id": "decision_process",
                "status": "sufficient",
                "evidence_fact_ids": ["DOES-NOT-EXIST"],
                "reason": "Unsupported citation.",
            },
            {
                "domain_id": "emotion_regulation",
                "status": "unknown",
                "evidence_fact_ids": [],
                "reason": "Participant explicitly could not tell.",
            },
        ]
    }

    report = _normalize_coverage(raw, operative_facts=(Fact(),))
    rows = {row["domain_id"]: row for row in report["assessments"]}

    assert rows["decision_process"]["status"] == "unassessed"
    assert rows["emotion_regulation"]["status"] == "unknown"
    assert report["required_domain_count"] == 10
    assert report["complete_domain_count"] == 1


def test_coverage_health_contract_describes_standardized_adaptive_measurement() -> None:
    app = create_life_patterns_v2_owner_coverage_app(model=CoverageSessionModel())  # type: ignore[arg-type]
    health_route = next(route for route in app.routes if getattr(route, "path", None) == "/healthz")
    payload = health_route.endpoint()

    assert payload["development_surface"] is True
    assert "owner_only" not in payload
    assert payload["target_theory_blind"] is True
    assert payload["standardized_required_coverage"] is True
    assert payload["adaptive_wording_with_fixed_domains"] is True
    assert payload["required_domain_count"] == 10
    assert payload["coverage_blueprint_sha256"] == COVERAGE_BLUEPRINT_SHA256
