"""Differential audit primitives for certifying an ephemeris against a reference.

The intended reference is an independent JPL DE440-family implementation. The
functions are provider-agnostic so the audit logic itself can be tested offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .ephemeris import CelestialBody, EphemerisProvider


@dataclass(frozen=True, slots=True)
class AuditSample:
    body: CelestialBody
    at_utc: datetime
    candidate_longitude_deg: float
    reference_longitude_deg: float
    signed_error_arcsec: float
    abs_error_arcsec: float


@dataclass(frozen=True, slots=True)
class AuditSummary:
    sample_count: int
    max_abs_error_arcsec: float
    mean_abs_error_arcsec: float
    within_tolerance_count: int
    tolerance_arcsec: float

    @property
    def all_within_tolerance(self) -> bool:
        return self.within_tolerance_count == self.sample_count


def signed_circular_difference_deg(candidate: float, reference: float) -> float:
    """Return candidate-reference in the half-open [-180, 180) interval."""

    return (candidate - reference + 180.0) % 360.0 - 180.0


def compare_providers(
    candidate: EphemerisProvider,
    reference: EphemerisProvider,
    *,
    bodies: tuple[CelestialBody, ...],
    timestamps_utc: tuple[datetime, ...],
) -> tuple[AuditSample, ...]:
    """Compare provider longitudes without applying any astrological mapping."""

    samples: list[AuditSample] = []
    for at_utc in timestamps_utc:
        for body in bodies:
            candidate_position = candidate.position(body, at_utc)
            reference_position = reference.position(body, at_utc)
            error_deg = signed_circular_difference_deg(
                candidate_position.longitude,
                reference_position.longitude,
            )
            samples.append(
                AuditSample(
                    body=body,
                    at_utc=at_utc,
                    candidate_longitude_deg=candidate_position.longitude,
                    reference_longitude_deg=reference_position.longitude,
                    signed_error_arcsec=error_deg * 3600.0,
                    abs_error_arcsec=abs(error_deg) * 3600.0,
                )
            )
    return tuple(samples)


def summarize_audit(
    samples: tuple[AuditSample, ...],
    *,
    tolerance_arcsec: float,
) -> AuditSummary:
    """Summarize numerical agreement separately from symbolic-boundary effects."""

    if not samples:
        raise ValueError("at least one differential audit sample is required")
    if tolerance_arcsec < 0.0:
        raise ValueError("tolerance_arcsec cannot be negative")
    errors = tuple(sample.abs_error_arcsec for sample in samples)
    return AuditSummary(
        sample_count=len(samples),
        max_abs_error_arcsec=max(errors),
        mean_abs_error_arcsec=sum(errors) / len(errors),
        within_tolerance_count=sum(error <= tolerance_arcsec for error in errors),
        tolerance_arcsec=tolerance_arcsec,
    )


def equal_bin_index(longitude_deg: float, *, bins: int, offset_deg: float = 0.0) -> int:
    """Return an equal-longitude bin index for boundary-sensitivity audits."""

    if bins <= 0:
        raise ValueError("bins must be positive")
    width = 360.0 / bins
    normalized = (longitude_deg - offset_deg) % 360.0
    return int(normalized // width)


def equal_bin_assignment_changed(
    sample: AuditSample,
    *,
    bins: int,
    offset_deg: float = 0.0,
) -> bool:
    """Whether numerical disagreement crosses an equal-longitude symbolic boundary."""

    return equal_bin_index(
        sample.candidate_longitude_deg,
        bins=bins,
        offset_deg=offset_deg,
    ) != equal_bin_index(
        sample.reference_longitude_deg,
        bins=bins,
        offset_deg=offset_deg,
    )
