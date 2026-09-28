from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta

import pytest

from hdmatch.empirical_astrology import (
    BirthRecord,
    ProvenanceError,
    ResponseSubmission,
    VerifiedBirthInput,
    build_pair_features,
    build_pair_outcome_ledger,
    validate_response_collection,
)

PROTOCOL = "same-hospital-personality-protocol-v1b-20260928"
PACKAGE_SHA = hashlib.sha256(b"questionnaire package").hexdigest()
OPENING = datetime(2027, 1, 1, tzinfo=UTC)
CLOSING = OPENING + timedelta(days=30)


def _record(participant: str, minute: int = 600) -> BirthRecord:
    birth_date = date(2000, 1, 1)
    return BirthRecord(
        participant_id=participant,
        hospital_id="H1",
        network_id="N1",
        local_birth_date=birth_date,
        birth_utc_timestamp=datetime(2000, 1, 1, tzinfo=UTC) + timedelta(minutes=minute),
        birth_local_clock_minutes=float(minute),
        birth_time_uncertainty_minutes=0.5,
        record_precision_category="recorded_to_minute",
        sex_at_birth_category="female",
        delivery_mode_category="spontaneous_vaginal",
        maternal_age_at_birth_years=30.0,
        gestational_age_at_birth_weeks=39.0,
        birthweight_grams=3200.0,
        recruitment_source_category="hospital_registry_invitation",
        relationship_component_id=f"R_{participant}",
    )


def _verified(participant: str = "P1") -> VerifiedBirthInput:
    record = _record(participant)
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
        raw_birth_payload=b"raw birth source",
        eligibility_payload=b"eligibility source",
    )


def test_verified_birth_input_binds_resolution_civil_time_and_provenance() -> None:
    verified = _verified()
    assert verified.raw_birth_input_sha256 == hashlib.sha256(b"raw birth source").hexdigest()
    assert verified.eligibility_sha256 == hashlib.sha256(b"eligibility source").hexdigest()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("language", "French", "English"),
        ("multiple_birth", True, "multiple-birth"),
        ("prior_natal_chart_reading", True, "natal-chart"),
        ("own_sign_trait_knowledge", True, "own-sign"),
        ("hd_interpretation_exposure", True, "Human Design"),
        ("documented_resolution_seconds", 61.0, "recorded_to_minute"),
    ],
)
def test_verified_birth_input_rejects_each_frozen_exclusion(
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ProvenanceError, match=message):
        replace(_verified(), **{field: value})


def test_verified_birth_input_rejects_civil_time_and_age_conflicts() -> None:
    with pytest.raises(ProvenanceError, match="different instants"):
        replace(
            _verified(),
            birth_local_timestamp=datetime(2000, 1, 1, 11, tzinfo=UTC),
        )
    with pytest.raises(ProvenanceError, match="18..65"):
        replace(_verified(), cohort_opening_utc=datetime(2010, 1, 1, tzinfo=UTC))


def _responses(value: int = 3) -> dict[int, int]:
    return {item: value for item in range(1, 51)}


def _submission(
    participant: str,
    *,
    submitted: datetime | None = None,
    complete: bool = True,
    withdrawn: bool = False,
    package_sha: str = PACKAGE_SHA,
    responses: dict[int, int] | None = None,
) -> ResponseSubmission:
    return ResponseSubmission(
        participant_id=participant,
        submitted_at_utc=submitted or OPENING + timedelta(days=1),
        responses=_responses() if responses is None else responses,
        response_complete_status=complete,
        withdrawal_status=withdrawn,
        questionnaire_package_sha256=package_sha,
        raw_response_payload=f"raw:{participant}:{submitted}".encode(),
    )


def test_response_collection_enforces_window_package_first_complete_and_attrition() -> None:
    collection = validate_response_collection(
        ["P1", "P2", "P3", "P4", "P5"],
        [
            _submission("P1"),
            _submission("P2", submitted=CLOSING),
            _submission("P3", withdrawn=True),
            _submission("P4", package_sha="0" * 64),
            _submission("P5", responses={1: 3}),
        ],
        cohort_opening_utc=OPENING,
        cohort_closing_utc=CLOSING,
        questionnaire_package_sha256=PACKAGE_SHA,
    )
    assert [response.participant_id for response in collection.accepted] == ["P1"]
    assert {item.reason for item in collection.attrition} == {
        "response_outside_frozen_window",
        "withdrawn",
        "questionnaire_package_mismatch",
        "invalid_or_incomplete_ipip50",
    }
    with pytest.raises(ProvenanceError, match="multiple complete"):
        validate_response_collection(
            ["P1"],
            [_submission("P1"), _submission("P1", submitted=OPENING + timedelta(days=2))],
            cohort_opening_utc=OPENING,
            cohort_closing_utc=CLOSING,
            questionnaire_package_sha256=PACKAGE_SHA,
        )


def test_pair_outcome_ledger_keeps_missing_pair_without_repairing() -> None:
    pair = build_pair_features(
        _record("P1", 600),
        _record("P2", 660),
        protocol_version=PROTOCOL,
        base_seed=20260928,
    )
    collection = validate_response_collection(
        ["P1", "P2"],
        [_submission("P1")],
        cohort_opening_utc=OPENING,
        cohort_closing_utc=CLOSING,
        questionnaire_package_sha256=PACKAGE_SHA,
    )
    ledger = build_pair_outcome_ledger([pair], collection)
    assert len(ledger) == 1
    assert ledger[0].status == "MISSING_SELECTED_PAIR"
    assert ledger[0].outcome_distance is None
