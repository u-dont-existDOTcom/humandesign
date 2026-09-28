from __future__ import annotations

import hashlib
from collections import Counter
from datetime import UTC, date, datetime, timedelta

import pytest

from hdmatch.empirical_astrology import (
    NUISANCE_COLUMN_NAMES,
    BirthRecord,
    DesignNotLaunchable,
    HospitalPairSelection,
    PairEligibilityError,
    VerifiedBirthInput,
    allocate_networks_to_cohorts,
    birth_gap_bounds,
    build_pair_features,
    build_prospective_design,
    deterministic_pair_id,
    deterministic_random_feature,
    entity_hash,
    greedy_disjoint_pairs,
    pair_eligibility_errors,
    retain_one_per_relationship_component,
    select_hospital_pairs,
    validate_cohort_pair_support,
    validate_identifier,
)

PROTOCOL = "same-hospital-personality-protocol-v1b-20260928"
SEED = 20260928
OPENING = datetime(2027, 1, 1, tzinfo=UTC)


def _record(
    participant: str,
    minute: int,
    *,
    component: str | None = None,
    hospital: str = "H1",
    network: str = "N1",
    uncertainty: float = 1.0,
    local_date: date = date(2000, 1, 1),
    delivery_mode: str = "spontaneous_vaginal",
) -> BirthRecord:
    start = datetime.combine(local_date, datetime.min.time(), tzinfo=UTC)
    return BirthRecord(
        participant_id=participant,
        hospital_id=hospital,
        network_id=network,
        local_birth_date=local_date,
        birth_utc_timestamp=start + timedelta(minutes=minute),
        birth_local_clock_minutes=float(minute),
        birth_time_uncertainty_minutes=uncertainty,
        record_precision_category="recorded_to_minute",
        sex_at_birth_category="female",
        delivery_mode_category=delivery_mode,
        maternal_age_at_birth_years=30.0 + minute / 1000.0,
        gestational_age_at_birth_weeks=39.0,
        birthweight_grams=3200.0 + minute,
        recruitment_source_category="hospital_registry_invitation",
        relationship_component_id=component or f"R_{participant}",
    )


def _verified_record(record: BirthRecord) -> VerifiedBirthInput:
    return VerifiedBirthInput(
        record=record,
        birth_local_timestamp=record.birth_utc_timestamp,
        birth_timezone_name="UTC",
        documented_resolution_seconds=60.0,
        cohort_opening_utc=OPENING,
        language="English",
        multiple_birth=False,
        prior_natal_chart_reading=False,
        own_sign_trait_knowledge=False,
        hd_interpretation_exposure=False,
        astrology_belief=0,
        can_name_own_sun_sign=False,
        raw_birth_payload=f"birth:{record.participant_id}".encode(),
        eligibility_payload=f"eligibility:{record.participant_id}".encode(),
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


def _fake_hospital_selection(index: int, *, low: bool) -> HospitalPairSelection:
    pairs = []
    for pair_index in range(100):
        local_date = date(2000, 1, 1) + timedelta(days=pair_index // 5)
        gap = 0.1 if low else 1.5
        pairs.append(
            build_pair_features(
                _record(
                    f"F{index}_{pair_index}_A",
                    100,
                    hospital=f"H{index}",
                    network=f"N{index}",
                    local_date=local_date,
                ),
                _record(
                    f"F{index}_{pair_index}_B",
                    100 + int(gap * 60),
                    hospital=f"H{index}",
                    network=f"N{index}",
                    local_date=local_date,
                ),
                protocol_version=PROTOCOL,
                base_seed=SEED,
            )
        )
    return HospitalPairSelection(
        hospital_id=f"H{index}",
        network_id=f"N{index}",
        selected_pairs=tuple(pairs),
        informative_birth_dates=20,
        fraction_gap_at_most_15_minutes=1.0 if low else 0.0,
        fraction_gap_at_least_60_minutes=0.0 if low else 1.0,
        launch_gate_errors=(),
    )


def test_exposure_support_is_cohort_scoped_with_complementary_hospitals() -> None:
    selections = [_fake_hospital_selection(index, low=index < 10) for index in range(20)]
    cohort = validate_cohort_pair_support(selections, cohort_label="A")
    assert cohort.fraction_gap_at_most_15_minutes == 0.5
    assert cohort.fraction_gap_at_least_60_minutes == 0.5
    assert cohort.launch_gate_errors == ()


def _prospective_roster() -> list[VerifiedBirthInput]:
    deliveries = (
        "spontaneous_vaginal",
        "induced_vaginal",
        "assisted_vaginal",
        "planned_cesarean",
        "unplanned_cesarean",
    )
    gaps = (5, 10, 65, 90, 30)
    records: list[VerifiedBirthInput] = []
    for network_index in range(41):
        for day_index in range(20):
            local_date = date(2000, 1, 1) + timedelta(days=day_index)
            for pair_index, (delivery, gap) in enumerate(zip(deliveries, gaps, strict=True)):
                base = 120 + pair_index * 180
                for member, minute in (("A", base), ("B", base + gap)):
                    participant = f"P{network_index:02d}_{day_index:02d}_{pair_index}_{member}"
                    component = (
                        "GLOBAL_LINK"
                        if day_index == 0
                        and pair_index == 0
                        and member == "A"
                        and network_index in {0, 1}
                        else None
                    )
                    records.append(
                        _verified_record(
                            _record(
                                participant,
                                minute,
                                component=component,
                                hospital=f"H{network_index:02d}",
                                network=f"N{network_index:02d}",
                                uncertainty=0.5,
                                local_date=local_date,
                                delivery_mode=delivery,
                            )
                        )
                    )
    return records


def test_integrated_design_enforces_global_retention_allocation_and_isolation() -> None:
    roster = _prospective_roster()
    design = build_prospective_design(
        roster,
        protocol_version=PROTOCOL,
        base_seed=SEED,
    )
    assert len(design.cohort_a.hospital_selections) == 20
    assert len(design.cohort_b.hospital_selections) == 20
    assert len(design.cohort_a.selected_pairs) == 2000
    assert len(design.cohort_b.selected_pairs) == 2000
    assert design.cohort_a_entities.participant_ids.isdisjoint(
        design.cohort_b_entities.participant_ids
    )
    selected_components = (
        design.cohort_a_entities.relationship_component_ids
        | design.cohort_b_entities.relationship_component_ids
    )
    assert (
        Counter(
            item.record.relationship_component_id
            for item in roster
            if item.record.participant_id
            in design.cohort_a_entities.participant_ids | design.cohort_b_entities.participant_ids
        )["GLOBAL_LINK"]
        <= 1
    )
    assert "GLOBAL_LINK" in selected_components or any(
        exclusion.reason == "relationship_component_retention" for exclusion in design.exclusions
    )


def test_integrated_design_rejects_duplicate_participant_identity() -> None:
    record = _verified_record(_record("P1", 100))
    with pytest.raises(DesignNotLaunchable, match="duplicate"):
        build_prospective_design(
            [record, record],
            protocol_version=PROTOCOL,
            base_seed=SEED,
        )
    with pytest.raises(DesignNotLaunchable, match="verified input boundary"):
        build_prospective_design(  # type: ignore[arg-type]
            [_record("P2", 120)],
            protocol_version=PROTOCOL,
            base_seed=SEED,
        )
