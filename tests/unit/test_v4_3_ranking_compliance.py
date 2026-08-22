from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

import pytest

from hdmatch.model.v4_3 import (
    V43CandidateScore,
    V43ComplianceError,
    V43ComplianceEvidence,
    assess_v4_3_compliance,
    rank_exact_intervals,
    require_v4_3_compliance,
)
from hdmatch.model.v4_3.contracts import (
    RUBRIC_UNIT,
    V43_RANKING_POLICY_VERSION,
    V43_SCORING_ENGINE_VERSION,
)
from hdmatch.model.v4_3.ranking import ScoredExactInterval


def _score(
    *,
    net: float,
    contradictions: int = 0,
    detailed: float = 50.0,
    core: float = 50.0,
) -> V43CandidateScore:
    evidence = max(net, 0.0)
    contradiction_bits = evidence - net
    return V43CandidateScore(
        scoring_engine_version=V43_SCORING_ENGINE_VERSION,
        rubric_unit=RUBRIC_UNIT,
        evidence_rubric_bits=evidence,
        contradiction_rubric_bits=contradiction_bits,
        net_information=net,
        detailed_support=detailed,
        core_fit=core,
        meaningful_contradictions=contradictions,
        clusters=(),
        core_blocks=(),
        prevalence_universe_sha256="a" * 64,
        prevalence_policy_version="conditional-v1",
        prevalence_parent_hierarchy_sha256="b" * 64,
    )


def _candidate(
    candidate_id: str,
    score: V43CandidateScore,
    *,
    duration: int = 60_000_000,
    minute: int = 0,
) -> ScoredExactInterval:
    return ScoredExactInterval(
        candidate_id=candidate_id,
        utc_start=datetime(2000, 1, 1, 0, minute, tzinfo=UTC),
        stable_duration_microseconds=duration,
        score=score,
    )


def test_exact_rank_tuple_is_lexicographic_and_never_adds_corefit() -> None:
    # If CoreFit were added to NetInformation, "huge-core" would incorrectly win.
    net_winner = _candidate("net-winner", _score(net=2.0, core=0.0))
    huge_core = _candidate("huge-core", _score(net=1.0, core=100.0))
    fewer_contradictions = _candidate(
        "fewer-contradictions", _score(net=0.5, contradictions=0, detailed=0, core=0)
    )
    more_contradictions = _candidate(
        "more-contradictions", _score(net=0.5, contradictions=1, detailed=100, core=100)
    )
    detailed_winner = _candidate(
        "detailed-winner", _score(net=0.25, detailed=80, core=0), duration=1
    )
    core_winner = _candidate(
        "core-winner", _score(net=0.25, detailed=70, core=100), duration=1
    )

    ranking = rank_exact_intervals(
        (
            core_winner,
            more_contradictions,
            huge_core,
            net_winner,
            detailed_winner,
            fewer_contradictions,
        )
    )

    assert [record.candidate.candidate_id for record in ranking.records] == [
        "net-winner",
        "huge-core",
        "fewer-contradictions",
        "more-contradictions",
        "detailed-winner",
        "core-winner",
    ]
    assert ranking.ranking_policy_version == V43_RANKING_POLICY_VERSION


def test_all_five_equal_is_substantive_tie_and_utc_only_orders_display() -> None:
    score = _score(net=2.0, contradictions=1, detailed=75, core=80)
    later = _candidate("later", score, duration=3600, minute=2)
    earlier = _candidate("earlier", score, duration=3600, minute=1)
    shorter = _candidate("shorter", score, duration=3599, minute=0)

    ranking = rank_exact_intervals((later, shorter, earlier))

    assert [record.candidate.candidate_id for record in ranking.records] == [
        "earlier",
        "later",
        "shorter",
    ]
    assert ranking.records[0].rank_start == 1
    assert ranking.records[0].rank_end == 2
    assert ranking.records[0].midrank == pytest.approx(1.5)
    assert ranking.records[1].substantively_tied
    assert ranking.records[2].rank_start == ranking.records[2].rank_end == 3


def test_hidden_corefit_or_bonus_inside_netinformation_is_rejected() -> None:
    valid = _score(net=1.0, core=90.0)
    with pytest.raises(ValueError, match="hidden bonus"):
        replace(valid, net_information=91.0)


def test_rank_inputs_require_exact_positive_duration_and_unique_identity() -> None:
    with pytest.raises(ValueError, match="positive"):
        _candidate("zero", _score(net=0.0), duration=0.0)
    with pytest.raises(ValueError, match="UTC start"):
        ScoredExactInterval(
            candidate_id="offset",
            utc_start=datetime(2000, 1, 1, tzinfo=timezone(timedelta(hours=1))),
            stable_duration_microseconds=1,
            score=_score(net=0.0),
        )
    candidate = _candidate("duplicate", _score(net=0.0))
    with pytest.raises(ValueError, match="unique"):
        rank_exact_intervals((candidate, candidate))


def _compliance_evidence() -> V43ComplianceEvidence:
    return V43ComplianceEvidence(
        declared_model_version="V4.3",
        reduced_model_label="M0-architecture-only",
        calculation_tier="M2",
        scoring_tier="M2",
        mapping_schema_version="mapping-library-v2",
        required_feature_ids=frozenset({"type", "channel:1-8", "personality:sun:gate-line"}),
        available_feature_ids=frozenset(
            {"type", "channel:1-8", "personality:sun:gate-line"}
        ),
        exact_interval_source_verified=True,
        cache_verified=True,
        astronomy_provenance_verified=True,
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        flexibility_penalty_enabled=True,
        conditional_prevalence_enabled=True,
        duration_weighted_prevalence_enabled=True,
        prevalence_source_scope="declared-global-utc-universe",
        dependency_control_enabled=True,
        corroboration_cap=0.15,
        full_declared_universe_rescored=True,
        scoring_engine_version=V43_SCORING_ENGINE_VERSION,
        ranking_policy_version=V43_RANKING_POLICY_VERSION,
    )


def test_caller_constructed_or_replaced_evidence_cannot_emit_canonical_v4_3() -> None:
    evidence = _compliance_evidence()
    compliance = assess_v4_3_compliance(evidence)

    assert not compliance.v4_3_compliant
    assert any("canonical artifact adapter" in item for item in compliance.failure_reasons)
    with pytest.raises(V43ComplianceError, match="canonical artifact adapter"):
        require_v4_3_compliance(evidence)


def test_m0_claim_is_downgraded_and_fail_closed_requirement_raises() -> None:
    evidence = replace(
        _compliance_evidence(),
        calculation_tier="M0",
        scoring_tier="M0",
        available_feature_ids=frozenset({"type"}),
    )
    compliance = assess_v4_3_compliance(evidence)

    assert not compliance.v4_3_compliant
    assert compliance.status == "partial/non-compliant"
    assert compliance.reported_model_version == "M0-architecture-only"
    assert compliance.simplified
    assert compliance.required_feature_coverage == pytest.approx(1 / 3)
    assert compliance.missing_required_feature_ids == (
        "channel:1-8",
        "personality:sun:gate-line",
    )
    with pytest.raises(V43ComplianceError, match="calculation tier"):
        require_v4_3_compliance(evidence)


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"flexibility_penalty_enabled": False}, "flexibility penalty"),
        ({"conditional_prevalence_enabled": False}, "conditional prevalence"),
        ({"duration_weighted_prevalence_enabled": False}, "duration-weighted"),
        ({"dependency_control_enabled": False}, "dependency control"),
        ({"corroboration_cap": 0.150001}, "exactly 0.15"),
        ({"full_declared_universe_rescored": False}, "complete declared universe"),
        ({"cache_verified": False}, "cache"),
        ({"ephemeris_returned": "MOSHIER"}, "returned ephemeris"),
        ({"ranking_policy_version": "scalar-rank"}, "ranking policy"),
        ({"scoring_engine_version": "no-flexibility"}, "scoring engine"),
    ],
)
def test_anti_simplification_mutations_cannot_claim_v4_3(
    changes: dict[str, object], reason: str
) -> None:
    evidence = replace(_compliance_evidence(), **changes)
    compliance = assess_v4_3_compliance(evidence)

    assert not compliance.v4_3_compliant
    assert compliance.reported_model_version == "M0-architecture-only"
    assert any(reason in item for item in compliance.failure_reasons)


def test_empty_required_registry_cannot_report_full_coverage() -> None:
    evidence = replace(
        _compliance_evidence(),
        required_feature_ids=frozenset(),
        available_feature_ids=frozenset(),
    )
    compliance = assess_v4_3_compliance(evidence)

    assert compliance.required_feature_coverage == 0.0
    assert not compliance.v4_3_compliant
    assert "required feature registry is empty" in compliance.failure_reasons


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (_score(net=2.0), _score(net=1.0)),
        (_score(net=1.0, contradictions=0), _score(net=1.0, contradictions=1)),
        (_score(net=1.0, detailed=60), _score(net=1.0, detailed=50)),
        (_score(net=1.0, core=60), _score(net=1.0, core=50)),
    ],
)
def test_each_score_rank_key_independently_orders_candidates(
    left: V43CandidateScore, right: V43CandidateScore
) -> None:
    ranking = rank_exact_intervals((_candidate("right", right), _candidate("left", left)))
    assert ranking.records[0].candidate.candidate_id == "left"


def test_exact_integer_duration_is_the_isolated_fifth_rank_key() -> None:
    score = _score(net=1.0, contradictions=0, detailed=50, core=50)
    ranking = rank_exact_intervals(
        (
            _candidate("short", score, duration=1_000_000),
            _candidate("long", score, duration=1_000_001),
        )
    )
    assert ranking.records[0].candidate.candidate_id == "long"
    with pytest.raises(ValueError, match="exact positive microseconds"):
        _candidate("float", score, duration=1.5)  # type: ignore[arg-type]
