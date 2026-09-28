from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime, timedelta

import pytest

from hdmatch.empirical_astrology import (
    NUISANCE_COLUMN_NAMES,
    BirthRecord,
    DesignNotLaunchable,
    PairEligibilityError,
    allocate_networks_to_cohorts,
    birth_gap_bounds,
    build_pair_features,
    deterministic_pair_id,
    deterministic_random_feature,
    entity_hash,
    greedy_disjoint_pairs,
    pair_eligibility_errors,
    retain_one_per_relationship_component,
    select_hospital_pairs,
    validate_identifier,
)

PROTOCOL = "same-hospital-personality-protocol-v1b-20260928"
SEED = 20260928


def _record(
    participant: str,
    minute: int,
    *,
    component: str | None = None,
    hospital: str = "H1",
    network: str = "N1",
    uncertainty: float = 1.0,
) -> BirthRecord:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    return BirthRecord(
        participant_id=participant,
        hospital_id=hospital,
        network_id=network,
        local_birth_date=date(2000, 1, 1),
        birth_utc_timestamp=start + timedelta(minutes=minute),
        birth_local_clock_minutes=float(minute),
        birth_time_uncertainty_minutes=uncertainty,
        record_precision_category="recorded_to_minute",
        sex_at_birth_category="female",
        delivery_mode_category="spontaneous_vaginal",
        maternal_age_at_birth_years=30.0 + minute / 1000.0,
        gestational_age_at_birth_weeks=39.0,
        birthweight_grams=3200.0 + minute,
        recruitment_source_category="hospital_registry_invitation",
        relationship_component_id=component or f"R_{participant}",
    )


def test_identifier_and_hash_formulas_have_fixed_golden_values() -> None:
    assert validate_identifier("A_b-9") == "A_b-9"
    for invalid in ("", "has space", "é", "a\0b"):
        with pytest.raises(ValueError):
            validate_identifier(invalid)
    expected_entity = hashlib.sha256(f"{PROTOCOL}\0{SEED}\0participant\0P1".encode()).hexdigest()
    assert (
        entity_hash("participant", "P1", protocol_version=PROTOCOL, base_seed=SEED)
        == expected_entity
    )
    expected_pair = hashlib.sha256(f"{PROTOCOL}\0{SEED}\0P1\0P2".encode()).hexdigest()
    assert (
        deterministic_pair_id("P2", "P1", protocol_version=PROTOCOL, base_seed=SEED)
        == expected_pair
    )
    literal = hashlib.sha256(
        "\0".join((PROTOCOL, str(SEED), "7", expected_pair)).encode()
    ).hexdigest()
    expected_random = 3.0 * (int(literal, 16) + 0.5) / 2**256
    assert (
        deterministic_random_feature(expected_pair, 7, protocol_version=PROTOCOL, base_seed=SEED)
        == expected_random
    )


def test_gap_bounds_and_nuisance_order() -> None:
    left = _record("P1", 100)
    right = _record("P2", 160)
    bounds = birth_gap_bounds(left, right)
    assert (bounds.center_minutes, bounds.lower_minutes, bounds.upper_minutes) == (
        60.0,
        58.0,
        62.0,
    )
    pair = build_pair_features(left, right, protocol_version=PROTOCOL, base_seed=SEED)
    assert pair.center_gap_hours == 1.0
    assert pair.lower_gap_hours == 58 / 60
    assert pair.upper_gap_hours == 62 / 60
    assert len(pair.nuisance_values) == len(NUISANCE_COLUMN_NAMES) == 14


def test_pair_boundary_and_matching_fail_closed() -> None:
    left = _record("P1", 100)
    exactly = _record("P2", 278)
    assert birth_gap_bounds(left, exactly).upper_minutes == 180.0
    assert pair_eligibility_errors(left, exactly) == ()
    over = _record("P3", 279)
    assert "upper_birth_gap_exceeds_180_minutes" in pair_eligibility_errors(left, over)
    mismatch = _record("P4", 120, hospital="H2")
    with pytest.raises(PairEligibilityError, match="matching_stratum_mismatch"):
        build_pair_features(left, mismatch, protocol_version=PROTOCOL, base_seed=SEED)


def test_birth_uncertainty_must_stay_inside_local_date() -> None:
    with pytest.raises(ValueError, match="remain inside"):
        _record("P1", 0, uncertainty=1.0)


def test_greedy_pairing_is_input_order_invariant_and_disjoint() -> None:
    records = [_record(f"P{i}", 100 + i * 5) for i in range(8)]
    forward = greedy_disjoint_pairs(records, protocol_version=PROTOCOL, base_seed=SEED)
    reverse = greedy_disjoint_pairs(
        list(reversed(records)), protocol_version=PROTOCOL, base_seed=SEED
    )
    assert [pair.pair_id for pair in forward] == [pair.pair_id for pair in reverse]
    participants = [participant for pair in forward for participant in pair.participant_ids]
    assert len(participants) == len(set(participants))


def test_relationship_component_retention_uses_smallest_hash() -> None:
    records = [
        _record("P1", 100, component="FAMILY"),
        _record("P2", 105, component="FAMILY"),
        _record("P3", 110),
    ]
    retained = retain_one_per_relationship_component(
        records, protocol_version=PROTOCOL, base_seed=SEED
    )
    family_expected = min(
        ("P1", "P2"),
        key=lambda participant: (
            entity_hash("participant", participant, protocol_version=PROTOCOL, base_seed=SEED),
            participant.encode(),
        ),
    )
    assert {record.participant_id for record in retained} == {family_expected, "P3"}


def test_network_allocation_and_hospital_gate_report_failures_without_reselection() -> None:
    allocation = allocate_networks_to_cohorts(
        [f"N{i:02d}" for i in range(45)], protocol_version=PROTOCOL, base_seed=SEED
    )
    assert len(allocation["A"]) == len(allocation["B"]) == 20
    assert set(allocation["A"]).isdisjoint(allocation["B"])
    with pytest.raises(DesignNotLaunchable):
        allocate_networks_to_cohorts(
            [f"N{i}" for i in range(39)], protocol_version=PROTOCOL, base_seed=SEED
        )
    selection = select_hospital_pairs(
        [_record(f"P{i}", 100 + i * 3) for i in range(10)],
        protocol_version=PROTOCOL,
        base_seed=SEED,
        strict_prospective_gate=False,
    )
    assert "selected_pair_count_not_100" in selection.launch_gate_errors
    with pytest.raises(DesignNotLaunchable):
        select_hospital_pairs(
            [_record(f"P{i}", 100 + i * 3) for i in range(10)],
            protocol_version=PROTOCOL,
            base_seed=SEED,
        )
