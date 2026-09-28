"""Theory-neutral pair construction for the frozen Wave 3B model.

No astrology calculator is imported here.  The assembled model exposes only
``TN-001``: elapsed UTC birth time within a matched hospital/date stratum.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Final

IDENTIFIER_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9_-]+")

SEX_AT_BIRTH_CATEGORIES: Final[frozenset[str]] = frozenset({"female", "male", "intersex"})
DELIVERY_MODE_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        "spontaneous_vaginal",
        "induced_vaginal",
        "assisted_vaginal",
        "planned_cesarean",
        "unplanned_cesarean",
    }
)
RECRUITMENT_SOURCE_CATEGORIES: Final[frozenset[str]] = frozenset({"hospital_registry_invitation"})
RECORD_PRECISION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"recorded_to_second", "recorded_to_minute"}
)

NUISANCE_COLUMN_NAMES: Final[tuple[str, ...]] = (
    "mean(sin(theta_i),sin(theta_j))",
    "mean(cos(theta_i),cos(theta_j))",
    "mean(sin(2*theta_i),sin(2*theta_j))",
    "mean(cos(2*theta_i),cos(2*theta_j))",
    "abs(sin(theta_i)-sin(theta_j))",
    "abs(cos(theta_i)-cos(theta_j))",
    "abs(sin(2*theta_i)-sin(2*theta_j))",
    "abs(cos(2*theta_i)-cos(2*theta_j))",
    "mean(maternal_age_years_i,maternal_age_years_j)",
    "abs(maternal_age_years_i-maternal_age_years_j)",
    "mean(gestational_weeks_i,gestational_weeks_j)",
    "abs(gestational_weeks_i-gestational_weeks_j)",
    "mean(birthweight_grams_i,birthweight_grams_j)/1000",
    "abs(birthweight_grams_i-birthweight_grams_j)/1000",
)


class PairEligibilityError(ValueError):
    """Raised when two records cannot form a frozen-protocol pair."""


def validate_identifier(value: str, *, field: str = "identifier") -> str:
    """Return a valid pre-outcome identifier or fail closed."""

    if not isinstance(value, str) or IDENTIFIER_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{field} must match [A-Za-z0-9_-]+ exactly")
    return value


def _finite(value: float, *, field: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _hash_parts(*parts: str) -> str:
    return hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()


def _seed_decimal(base_seed: int) -> str:
    if isinstance(base_seed, bool) or not isinstance(base_seed, int) or base_seed < 0:
        raise ValueError("base_seed must be a non-negative integer")
    return str(base_seed)


def entity_hash(
    entity_type: str,
    entity_id: str,
    *,
    protocol_version: str,
    base_seed: int,
) -> str:
    """Return the frozen entity-priority hash."""

    if entity_type not in {"participant", "hospital", "network"}:
        raise ValueError("entity_type must be participant, hospital, or network")
    validate_identifier(entity_id, field=f"{entity_type}_id")
    validate_identifier(protocol_version, field="protocol_version")
    seed = _seed_decimal(base_seed)
    return _hash_parts(protocol_version, seed, entity_type, entity_id)


def deterministic_pair_id(
    participant_a: str,
    participant_b: str,
    *,
    protocol_version: str,
    base_seed: int,
) -> str:
    """Return the frozen pair ID and edge-priority hash."""

    left = validate_identifier(participant_a, field="participant_a")
    right = validate_identifier(participant_b, field="participant_b")
    if left == right:
        raise ValueError("a pair requires two distinct participant IDs")
    validate_identifier(protocol_version, field="protocol_version")
    smaller, larger = sorted((left, right), key=lambda item: item.encode("utf-8"))
    return _hash_parts(protocol_version, _seed_decimal(base_seed), smaller, larger)


def deterministic_random_feature(
    pair_id: str,
    diagnostic_index: int,
    *,
    protocol_version: str,
    base_seed: int,
) -> float:
    """Return one of the twenty frozen random-feature diagnostic columns."""

    validate_identifier(protocol_version, field="protocol_version")
    if re.fullmatch(r"[0-9a-f]{64}", pair_id) is None:
        raise ValueError("pair_id must be a lowercase hexadecimal SHA256")
    if (
        isinstance(diagnostic_index, bool)
        or not isinstance(diagnostic_index, int)
        or not 1 <= diagnostic_index <= 20
    ):
        raise ValueError("diagnostic_index must be an integer in 1..20")
    digest = _hash_parts(
        protocol_version,
        _seed_decimal(base_seed),
        str(diagnostic_index),
        pair_id,
    )
    return 3.0 * (int(digest, 16) + 0.5) / 2**256


@dataclass(frozen=True, slots=True)
class BirthRecord:
    """Pre-outcome fields needed for deterministic eligibility and TN-001."""

    participant_id: str
    hospital_id: str
    network_id: str
    local_birth_date: date
    birth_utc_timestamp: datetime
    birth_local_clock_minutes: float
    birth_time_uncertainty_minutes: float
    record_precision_category: str
    sex_at_birth_category: str
    delivery_mode_category: str
    maternal_age_at_birth_years: float
    gestational_age_at_birth_weeks: float
    birthweight_grams: float
    recruitment_source_category: str
    relationship_component_id: str

    def __post_init__(self) -> None:
        for field, value in (
            ("participant_id", self.participant_id),
            ("hospital_id", self.hospital_id),
            ("network_id", self.network_id),
            ("relationship_component_id", self.relationship_component_id),
        ):
            validate_identifier(value, field=field)
        if self.birth_utc_timestamp.tzinfo is None or self.birth_utc_timestamp.utcoffset() is None:
            raise ValueError("birth_utc_timestamp must be timezone-aware")
        if self.record_precision_category not in RECORD_PRECISION_CATEGORIES:
            raise ValueError("record_precision_category is outside the frozen dictionary")
        if self.sex_at_birth_category not in SEX_AT_BIRTH_CATEGORIES:
            raise ValueError("sex_at_birth_category is outside the frozen dictionary")
        if self.delivery_mode_category not in DELIVERY_MODE_CATEGORIES:
            raise ValueError("delivery_mode_category is outside the frozen dictionary")
        if self.recruitment_source_category not in RECRUITMENT_SOURCE_CATEGORIES:
            raise ValueError("recruitment_source_category is outside the frozen dictionary")
        clock = _finite(self.birth_local_clock_minutes, field="birth_local_clock_minutes")
        uncertainty = _finite(
            self.birth_time_uncertainty_minutes,
            field="birth_time_uncertainty_minutes",
        )
        if not 0.0 <= clock < 1440.0:
            raise ValueError("birth_local_clock_minutes must be in [0,1440)")
        if not 0.0 <= uncertainty <= 1.0:
            raise ValueError("birth_time_uncertainty_minutes must be in [0,1]")
        if clock - uncertainty < 0.0 or clock + uncertainty >= 1440.0:
            raise ValueError("birth uncertainty interval must remain inside the local date")
        for field, value in (
            ("maternal_age_at_birth_years", self.maternal_age_at_birth_years),
            ("gestational_age_at_birth_weeks", self.gestational_age_at_birth_weeks),
            ("birthweight_grams", self.birthweight_grams),
        ):
            if _finite(value, field=field) <= 0.0:
                raise ValueError(f"{field} must be positive")

    @property
    def utc(self) -> datetime:
        return self.birth_utc_timestamp.astimezone(UTC)

    @property
    def matching_stratum(self) -> tuple[object, ...]:
        return (
            self.hospital_id,
            self.local_birth_date,
            self.sex_at_birth_category,
            self.delivery_mode_category,
            self.recruitment_source_category,
            self.record_precision_category,
        )


@dataclass(frozen=True, slots=True)
class GapBounds:
    center_minutes: float
    lower_minutes: float
    upper_minutes: float


def birth_gap_bounds(left: BirthRecord, right: BirthRecord) -> GapBounds:
    """Return center, lower, and upper elapsed-minute bounds."""

    delta = abs((left.utc - right.utc).total_seconds()) / 60.0
    uncertainty = left.birth_time_uncertainty_minutes + right.birth_time_uncertainty_minutes
    return GapBounds(
        center_minutes=delta,
        lower_minutes=max(0.0, delta - uncertainty),
        upper_minutes=delta + uncertainty,
    )


def pair_eligibility_errors(left: BirthRecord, right: BirthRecord) -> tuple[str, ...]:
    """Return every mechanical reason a pair violates the frozen specification."""

    errors: list[str] = []
    if left.participant_id == right.participant_id:
        errors.append("same_participant")
    if left.matching_stratum != right.matching_stratum:
        errors.append("matching_stratum_mismatch")
    if left.network_id != right.network_id:
        errors.append("network_mismatch")
    if left.relationship_component_id == right.relationship_component_id:
        errors.append("known_relationship_link")
    bounds = birth_gap_bounds(left, right)
    if bounds.upper_minutes > 180.0:
        errors.append("upper_birth_gap_exceeds_180_minutes")
    if abs(left.maternal_age_at_birth_years - right.maternal_age_at_birth_years) > 5.0:
        errors.append("maternal_age_difference_exceeds_5_years")
    if abs(left.gestational_age_at_birth_weeks - right.gestational_age_at_birth_weeks) > 1.0:
        errors.append("gestational_age_difference_exceeds_1_week")
    return tuple(errors)


@dataclass(frozen=True, slots=True)
class PairFeatures:
    """Frozen theory-neutral exposure and nuisance values for one eligible pair."""

    pair_id: str
    participant_ids: tuple[str, str]
    network_id: str
    hospital_id: str
    local_birth_date: date
    center_gap_hours: float
    lower_gap_hours: float
    upper_gap_hours: float
    nuisance_values: tuple[float, ...]

    @property
    def hospital_date_group(self) -> tuple[str, date]:
        return (self.hospital_id, self.local_birth_date)


def _clock_terms(minutes: float) -> tuple[float, float, float, float]:
    theta = 2.0 * math.pi * minutes / 1440.0
    return (math.sin(theta), math.cos(theta), math.sin(2.0 * theta), math.cos(2.0 * theta))


def build_pair_features(
    left: BirthRecord,
    right: BirthRecord,
    *,
    protocol_version: str,
    base_seed: int,
) -> PairFeatures:
    """Build TN-001 and the fourteen nuisance values for an eligible pair."""

    errors = pair_eligibility_errors(left, right)
    if errors:
        raise PairEligibilityError(", ".join(errors))
    participant_ids = tuple(
        sorted((left.participant_id, right.participant_id), key=lambda item: item.encode())
    )
    bounds = birth_gap_bounds(left, right)
    clock_left = _clock_terms(left.birth_local_clock_minutes)
    clock_right = _clock_terms(right.birth_local_clock_minutes)
    clock_means = tuple((a + b) / 2.0 for a, b in zip(clock_left, clock_right, strict=True))
    clock_differences = tuple(abs(a - b) for a, b in zip(clock_left, clock_right, strict=True))
    nuisance = (
        *clock_means,
        *clock_differences,
        (left.maternal_age_at_birth_years + right.maternal_age_at_birth_years) / 2.0,
        abs(left.maternal_age_at_birth_years - right.maternal_age_at_birth_years),
        (left.gestational_age_at_birth_weeks + right.gestational_age_at_birth_weeks) / 2.0,
        abs(left.gestational_age_at_birth_weeks - right.gestational_age_at_birth_weeks),
        (left.birthweight_grams + right.birthweight_grams) / 2000.0,
        abs(left.birthweight_grams - right.birthweight_grams) / 1000.0,
    )
    if len(nuisance) != len(NUISANCE_COLUMN_NAMES):
        raise AssertionError("internal nuisance-column count differs from the frozen contract")
    return PairFeatures(
        pair_id=deterministic_pair_id(
            left.participant_id,
            right.participant_id,
            protocol_version=protocol_version,
            base_seed=base_seed,
        ),
        participant_ids=participant_ids,
        network_id=left.network_id,
        hospital_id=left.hospital_id,
        local_birth_date=left.local_birth_date,
        center_gap_hours=bounds.center_minutes / 60.0,
        lower_gap_hours=bounds.lower_minutes / 60.0,
        upper_gap_hours=bounds.upper_minutes / 60.0,
        nuisance_values=nuisance,
    )
