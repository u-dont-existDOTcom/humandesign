"""Strict birth-input and response provenance boundaries for frozen v1b.

These validators do not authorize recruitment or reveal.  They turn raw values
into verified records only after all outcome-blind eligibility, civil-time, and
collection-window rules represented here have passed.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .features import BirthRecord, PairFeatures, validate_identifier
from .outcome import responses_to_pair_distance, validate_ipip50_responses
from .protocol import SHA256_PATTERN


class ProvenanceError(ValueError):
    """Raised when an eligibility, civil-time, or response boundary fails."""


def _utc(value: datetime, *, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProvenanceError(f"{field_name} must be timezone-aware")
    result = value.astimezone(UTC)
    if value.utcoffset() is None:
        raise ProvenanceError(f"{field_name} has no resolved UTC offset")
    return result


def _completed_age(birth_date: date, opening_date: date) -> int:
    return (
        opening_date.year
        - birth_date.year
        - ((opening_date.month, opening_date.day) < (birth_date.month, birth_date.day))
    )


@dataclass(frozen=True, slots=True)
class VerifiedBirthInput:
    """A low-level ``BirthRecord`` plus the metadata needed to trust it."""

    record: BirthRecord
    birth_local_timestamp: datetime
    birth_timezone_name: str
    documented_resolution_seconds: float
    cohort_opening_utc: datetime
    language: str
    multiple_birth: bool
    prior_natal_chart_reading: bool
    own_sign_trait_knowledge: bool
    hd_interpretation_exposure: bool
    astrology_belief: int
    can_name_own_sun_sign: bool
    raw_birth_payload: bytes = field(repr=False)
    eligibility_payload: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.raw_birth_payload, bytes) or not self.raw_birth_payload:
            raise ProvenanceError("raw_birth_payload must be nonempty bytes")
        if not isinstance(self.eligibility_payload, bytes) or not self.eligibility_payload:
            raise ProvenanceError("eligibility_payload must be nonempty bytes")
        if self.language != "English":
            raise ProvenanceError("primary eligibility requires English")
        if self.multiple_birth:
            raise ProvenanceError("multiple-birth records are ineligible")
        if self.prior_natal_chart_reading:
            raise ProvenanceError("prior natal-chart reading is ineligible")
        if self.own_sign_trait_knowledge:
            raise ProvenanceError("own-sign trait knowledge is ineligible")
        if self.hd_interpretation_exposure:
            raise ProvenanceError("prior Human Design interpretation is ineligible")
        if (
            isinstance(self.astrology_belief, bool)
            or not isinstance(self.astrology_belief, int)
            or not 0 <= self.astrology_belief <= 4
        ):
            raise ProvenanceError("astrology_belief must be an integer in 0..4")
        if not isinstance(self.can_name_own_sun_sign, bool):
            raise ProvenanceError("can_name_own_sun_sign must be boolean")

        resolution = float(self.documented_resolution_seconds)
        if not math.isfinite(resolution) or resolution <= 0.0:
            raise ProvenanceError("documented resolution must be finite and positive")
        if self.record.record_precision_category == "recorded_to_second":
            if resolution > 1.0:
                raise ProvenanceError("recorded_to_second requires resolution <=1 second")
        elif not 1.0 < resolution <= 60.0:
            raise ProvenanceError("recorded_to_minute requires resolution >1 and <=60 seconds")

        opening = _utc(self.cohort_opening_utc, field_name="cohort_opening_utc")
        try:
            timezone = ZoneInfo(self.birth_timezone_name)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ProvenanceError("birth_timezone_name is not a resolved IANA timezone") from exc
        supplied_local = self.birth_local_timestamp
        if supplied_local.tzinfo is None or supplied_local.utcoffset() is None:
            raise ProvenanceError("birth_local_timestamp must be timezone-aware")
        resolved_local = self.record.utc.astimezone(timezone)
        if supplied_local.astimezone(UTC) != self.record.utc:
            raise ProvenanceError("local and UTC birth timestamps identify different instants")
        if (
            supplied_local.replace(tzinfo=None) != resolved_local.replace(tzinfo=None)
            or supplied_local.utcoffset() != resolved_local.utcoffset()
            or supplied_local.fold != resolved_local.fold
        ):
            raise ProvenanceError("local birth timestamp conflicts with timezone/DST resolution")
        if resolved_local.date() != self.record.local_birth_date:
            raise ProvenanceError("resolved local date conflicts with recorded local birth date")
        clock_minutes = (
            resolved_local.hour * 60.0
            + resolved_local.minute
            + resolved_local.second / 60.0
            + resolved_local.microsecond / 60_000_000.0
        )
        if not math.isclose(
            clock_minutes,
            self.record.birth_local_clock_minutes,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ProvenanceError("resolved local clock conflicts with recorded clock minutes")
        uncertainty = timedelta(minutes=self.record.birth_time_uncertainty_minutes)
        if (self.record.utc - uncertainty).astimezone(
            timezone
        ).date() != self.record.local_birth_date:
            raise ProvenanceError("lower birth-time uncertainty bound leaves the local date")
        if (self.record.utc + uncertainty).astimezone(
            timezone
        ).date() != self.record.local_birth_date:
            raise ProvenanceError("upper birth-time uncertainty bound leaves the local date")
        age = _completed_age(self.record.local_birth_date, opening.astimezone(timezone).date())
        if not 18 <= age <= 65:
            raise ProvenanceError("completed age at cohort opening must be in 18..65")

    @property
    def raw_birth_input_sha256(self) -> str:
        return hashlib.sha256(self.raw_birth_payload).hexdigest()

    @property
    def eligibility_sha256(self) -> str:
        return hashlib.sha256(self.eligibility_payload).hexdigest()


@dataclass(frozen=True, slots=True)
class ResponseSubmission:
    """One immutable response submission before acceptance into analysis."""

    participant_id: str
    submitted_at_utc: datetime
    responses: Mapping[int, int]
    response_complete_status: bool
    withdrawal_status: bool
    questionnaire_package_sha256: str
    raw_response_payload: bytes = field(repr=False)

    def __post_init__(self) -> None:
        validate_identifier(self.participant_id, field="participant_id")
        _utc(self.submitted_at_utc, field_name="submitted_at_utc")
        if not isinstance(self.response_complete_status, bool):
            raise ProvenanceError("response_complete_status must be boolean")
        if not isinstance(self.withdrawal_status, bool):
            raise ProvenanceError("withdrawal_status must be boolean")
        if (
            not isinstance(self.questionnaire_package_sha256, str)
            or SHA256_PATTERN.fullmatch(self.questionnaire_package_sha256) is None
        ):
            raise ProvenanceError("questionnaire_package_sha256 must be lowercase SHA256")
        if not isinstance(self.raw_response_payload, bytes) or not self.raw_response_payload:
            raise ProvenanceError("raw_response_payload must be nonempty bytes")

    @property
    def raw_response_sha256(self) -> str:
        return hashlib.sha256(self.raw_response_payload).hexdigest()

    @property
    def coded_response_sha256(self) -> str:
        canonical = json.dumps(
            {str(item): self.responses[item] for item in sorted(self.responses)},
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
        return hashlib.sha256(canonical).hexdigest()


@dataclass(frozen=True, slots=True)
class VerifiedResponse:
    participant_id: str
    submitted_at_utc: datetime
    responses: tuple[tuple[int, int], ...]
    raw_response_sha256: str
    coded_response_sha256: str
    questionnaire_package_sha256: str

    def response_map(self) -> dict[int, int]:
        return dict(self.responses)


@dataclass(frozen=True, slots=True)
class ResponseAttrition:
    participant_id: str
    reason: str


@dataclass(frozen=True, slots=True)
class ResponseCollection:
    accepted: tuple[VerifiedResponse, ...]
    attrition: tuple[ResponseAttrition, ...]

    @property
    def by_participant(self) -> dict[str, VerifiedResponse]:
        return {response.participant_id: response for response in self.accepted}


@dataclass(frozen=True, slots=True)
class PairOutcomeRecord:
    pair: PairFeatures
    outcome_distance: float | None
    status: str
    reason: str | None


def validate_response_collection(
    preselected_participant_ids: Sequence[str],
    submissions: Sequence[ResponseSubmission],
    *,
    cohort_opening_utc: datetime,
    cohort_closing_utc: datetime,
    questionnaire_package_sha256: str,
) -> ResponseCollection:
    """Accept first complete immutable responses and retain every attrition reason."""

    opening = _utc(cohort_opening_utc, field_name="cohort_opening_utc")
    closing = _utc(cohort_closing_utc, field_name="cohort_closing_utc")
    if (closing - opening).total_seconds() != 30 * 86400:
        raise ProvenanceError("response window must be exactly 30*86400 seconds")
    if SHA256_PATTERN.fullmatch(questionnaire_package_sha256) is None:
        raise ProvenanceError("expected questionnaire package must be lowercase SHA256")
    participants = tuple(preselected_participant_ids)
    if len(participants) != len(set(participants)):
        raise ProvenanceError("preselected participant IDs must be unique")
    for participant in participants:
        validate_identifier(participant, field="preselected participant ID")
    allowed = set(participants)
    grouped: dict[str, list[ResponseSubmission]] = defaultdict(list)
    for submission in submissions:
        if submission.participant_id not in allowed:
            raise ProvenanceError("response submitted by a non-preselected participant")
        grouped[submission.participant_id].append(submission)

    accepted: list[VerifiedResponse] = []
    attrition: list[ResponseAttrition] = []
    for participant in participants:
        candidates = sorted(
            grouped.get(participant, ()),
            key=lambda item: (item.submitted_at_utc.astimezone(UTC), item.raw_response_sha256),
        )
        complete = [item for item in candidates if item.response_complete_status]
        if len(complete) > 1:
            raise ProvenanceError("multiple complete submissions violate immutable first response")
        if not complete:
            attrition.append(ResponseAttrition(participant, "no_complete_response"))
            continue
        response = complete[0]
        submitted = response.submitted_at_utc.astimezone(UTC)
        if not opening <= submitted < closing:
            attrition.append(ResponseAttrition(participant, "response_outside_frozen_window"))
            continue
        if response.questionnaire_package_sha256 != questionnaire_package_sha256:
            attrition.append(ResponseAttrition(participant, "questionnaire_package_mismatch"))
            continue
        if response.withdrawal_status:
            attrition.append(ResponseAttrition(participant, "withdrawn"))
            continue
        try:
            valid = validate_ipip50_responses(response.responses)
        except ValueError:
            attrition.append(ResponseAttrition(participant, "invalid_or_incomplete_ipip50"))
            continue
        accepted.append(
            VerifiedResponse(
                participant_id=participant,
                submitted_at_utc=submitted,
                responses=tuple(sorted(valid.items())),
                raw_response_sha256=response.raw_response_sha256,
                coded_response_sha256=response.coded_response_sha256,
                questionnaire_package_sha256=response.questionnaire_package_sha256,
            )
        )
    return ResponseCollection(accepted=tuple(accepted), attrition=tuple(attrition))


def build_pair_outcome_ledger(
    pairs: Sequence[PairFeatures],
    collection: ResponseCollection,
) -> tuple[PairOutcomeRecord, ...]:
    """Score only the frozen pairs; missing responses never trigger re-pairing."""

    responses = collection.by_participant
    seen: set[str] = set()
    ledger: list[PairOutcomeRecord] = []
    for pair in pairs:
        if any(participant in seen for participant in pair.participant_ids):
            raise ProvenanceError("a participant appears in more than one frozen pair")
        seen.update(pair.participant_ids)
        left = responses.get(pair.participant_ids[0])
        right = responses.get(pair.participant_ids[1])
        missing = [
            participant
            for participant, response in zip(pair.participant_ids, (left, right), strict=True)
            if response is None
        ]
        if missing:
            ledger.append(
                PairOutcomeRecord(
                    pair=pair,
                    outcome_distance=None,
                    status="MISSING_SELECTED_PAIR",
                    reason="missing response for " + ",".join(missing),
                )
            )
            continue
        assert left is not None and right is not None
        ledger.append(
            PairOutcomeRecord(
                pair=pair,
                outcome_distance=responses_to_pair_distance(
                    left.response_map(),
                    right.response_map(),
                ),
                status="COMPLETE",
                reason=None,
            )
        )
    return tuple(ledger)
