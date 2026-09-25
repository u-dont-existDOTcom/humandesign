from __future__ import annotations

import json
from pathlib import Path

from hdmatch.api.life_patterns_v2_owner_recoverability import (
    RECOVERABILITY_BLUEPRINT_SHA256,
    RECOVERABILITY_BLUEPRINT_VERSION,
    RECOVERABILITY_DOMAINS,
    RecoverabilityCoverageRuntime,
    _normalize_recoverability_coverage,
    create_life_patterns_v2_owner_recoverability_app,
)


CROSSWALK_PATH = Path("reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json")


class RecoverabilitySessionModel:
    configured = True


def test_recoverability_blueprint_is_versioned_unique_and_neutral() -> None:
    ids = [domain.domain_id for domain in RECOVERABILITY_DOMAINS]

    assert RECOVERABILITY_BLUEPRINT_VERSION == "life-patterns-recoverability-coverage-v2"
    assert len(RECOVERABILITY_DOMAINS) == 23
    assert len(ids) == len(set(ids))
    assert len(RECOVERABILITY_BLUEPRINT_SHA256) == 64

    required = {
        "complex_structure",
        "insight_translation",
        "recurring_mystery",
        "original_contribution",
        "persuasion_strategy",
        "recognition_entry",
        "network_pathways",
        "role_projection",
        "immediate_body_signal",
        "autonomy_direction",
        "sanctuary_sensory",
        "romantic_attachment",
        "emotion_permeability",
        "work_energy_range",
        "consequential_effort",
        "correction_threshold",
        "retreat_privacy",
        "value_tension",
        "resource_motivation",
        "developmental_phases",
        "rhythm_continuity",
        "focus_repetition",
        "needs_responsibility",
    }
    assert set(ids) == required

    runtime_text = "\n".join(
        f"{domain.domain_id} {domain.title} {domain.definition} {domain.canonical_screener}"
        for domain in RECOVERABILITY_DOMAINS
    ).lower()
    for forbidden in ("astrology", "human design", "projector", "splenic", "birth chart"):
        assert forbidden not in runtime_text


def test_historical_recovery_crosswalk_is_complete_without_entering_runtime() -> None:
    payload = json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))
    ids = {domain.domain_id for domain in RECOVERABILITY_DOMAINS}

    merged_rows = payload["historical_merged_cluster_crosswalk"]
    assert len(merged_rows) == 19
    assert len({row["historical_cluster"] for row in merged_rows}) == 19
    assert {row["neutral_domain"] for row in merged_rows} <= ids

    clean_rows = payload["clean_v36_information_crosswalk"]
    assert len(clean_rows) == 19
    assert len({row["observable"] for row in clean_rows}) == 19
    assert {row["neutral_domain"] for row in clean_rows} <= ids

    assert payload["runtime_boundary"]["interviewer_receives_this_crosswalk"] is False
    assert payload["runtime_boundary"]["interviewer_receives_chart"] is False
    assert payload["runtime_boundary"]["post_freeze_owner_evaluation_may_use_crosswalk"] is True
    assert "Instrument coverage alone cannot pass this gate" in payload["historical_recovery_evidence"][
        "acceptance_rule"
    ]


def test_recoverability_domain_session_begins_from_neutral_screener() -> None:
    runtime = RecoverabilityCoverageRuntime(model=RecoverabilitySessionModel())  # type: ignore[arg-type]

    session, domain = runtime.create_coverage_session("immediate_body_signal")

    assert session.pattern_focus_established is True
    assert session.conversation[-1]["role"] == "assistant"
    assert session.conversation[-1]["text"] == domain.canonical_screener
    assert "bodily or felt signal" in domain.canonical_screener
    assert "Splenic" not in domain.canonical_screener


def test_normalize_recoverability_coverage_requires_fact_citation() -> None:
    class Fact:
        fact_id = "F1"

    raw = {
        "assessments": [
            {
                "domain_id": "recurring_mystery",
                "status": "sufficient",
                "evidence_fact_ids": ["DOES-NOT-EXIST"],
                "reason": "Unsupported citation.",
            },
            {
                "domain_id": "romantic_attachment",
                "status": "declined",
                "evidence_fact_ids": [],
                "reason": "Participant declined.",
            },
        ]
    }

    report = _normalize_recoverability_coverage(raw, operative_facts=(Fact(),))
    rows = {row["domain_id"]: row for row in report["assessments"]}

    assert rows["recurring_mystery"]["status"] == "unassessed"
    assert rows["romantic_attachment"]["status"] == "declined"
    assert report["required_domain_count"] == 23
    assert report["complete_domain_count"] == 1


def test_recoverability_health_contract_exposes_candidate_not_validation_claim() -> None:
    app = create_life_patterns_v2_owner_recoverability_app(
        model=RecoverabilitySessionModel()  # type: ignore[arg-type]
    )
    health_route = next(route for route in app.routes if getattr(route, "path", None) == "/healthz")
    payload = health_route.endpoint()

    assert payload["development_surface"] is True
    assert payload["target_theory_blind"] is True
    assert payload["standardized_required_coverage"] is True
    assert payload["recoverability_preservation_candidate"] is True
    assert payload["required_domain_count"] == 23
    assert payload["coverage_blueprint_version"] == RECOVERABILITY_BLUEPRINT_VERSION
    assert payload["coverage_blueprint_sha256"] == RECOVERABILITY_BLUEPRINT_SHA256
