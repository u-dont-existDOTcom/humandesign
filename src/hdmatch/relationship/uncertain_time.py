"""Aggregate partnership mechanics across an unknown partner birth-time window.

The purpose is to report invariants and time-dependent relationship mechanics,
not to choose whichever birth time produces the most attractive narrative.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from hdmatch.chart.bodygraph import Center, Definition, HDType

from .analysis import (
    CenterConfigurationKeynote,
    ConnectionChannel,
    PartnershipAnalysis,
    PartnershipSnapshot,
    analyze_partnership,
)


@dataclass(frozen=True, slots=True)
class PartnerTimeCandidate:
    """One exact stable natal interval for the partner whose time is unknown."""

    start_utc: datetime
    end_utc: datetime
    partner: PartnershipSnapshot

    def __post_init__(self) -> None:
        start = _require_utc(self.start_utc)
        end = _require_utc(self.end_utc)
        if end <= start:
            raise ValueError("end_utc must be after start_utc")
        object.__setattr__(self, "start_utc", start)
        object.__setattr__(self, "end_utc", end)


@dataclass(frozen=True, slots=True)
class AnalyzedPartnershipInterval:
    start_utc: datetime
    end_utc: datetime
    analysis: PartnershipAnalysis

    @property
    def duration_seconds(self) -> float:
        return (self.end_utc - self.start_utc).total_seconds()


@dataclass(frozen=True, slots=True)
class UncertainPartnerTimeSummary:
    """Stable and variable mechanics across all supplied candidate intervals."""

    intervals: tuple[AnalyzedPartnershipInterval, ...]
    total_duration_seconds: float
    stable_connections: tuple[ConnectionChannel, ...]
    variable_connections: tuple[ConnectionChannel, ...]
    stable_defined_centers: tuple[Center, ...] | None
    stable_open_centers: tuple[Center, ...] | None
    stable_center_configuration: CenterConfigurationKeynote | None
    center_configuration_varies: bool
    stable_composite_definition: Definition | None
    composite_definition_varies: bool
    partner_types_seen: tuple[HDType, ...]


def summarize_uncertain_partner_time(
    known_partner: PartnershipSnapshot,
    candidates: tuple[PartnerTimeCandidate, ...],
) -> UncertainPartnerTimeSummary:
    """Analyze every candidate interval and preserve uncertainty honestly."""

    if not candidates:
        raise ValueError("at least one partner-time candidate is required")
    ordered = tuple(sorted(candidates, key=lambda item: item.start_utc))
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current.start_utc < previous.end_utc:
            raise ValueError("partner-time candidate intervals must not overlap")

    analyzed = tuple(
        AnalyzedPartnershipInterval(
            start_utc=item.start_utc,
            end_utc=item.end_utc,
            analysis=analyze_partnership(known_partner, item.partner),
        )
        for item in ordered
    )
    merged = _merge_adjacent_equal_states(analyzed)
    total_duration_seconds = sum(item.duration_seconds for item in merged)

    connection_sets = [set(item.analysis.channel_connections) for item in merged]
    stable_connections = set.intersection(*connection_sets)
    possible_connections = set.union(*connection_sets)
    variable_connections = possible_connections - stable_connections

    defined_center_values = {item.analysis.composite_defined_centers for item in merged}
    open_center_values = {item.analysis.composite_open_centers for item in merged}
    center_configuration_values = {item.analysis.center_configuration for item in merged}
    definition_values = {item.analysis.composite_definition for item in merged}
    partner_types = {
        item.analysis.partner_b_type
        for item in merged
        if item.analysis.partner_b_type is not None
    }

    return UncertainPartnerTimeSummary(
        intervals=merged,
        total_duration_seconds=total_duration_seconds,
        stable_connections=tuple(sorted(stable_connections, key=_connection_sort_key)),
        variable_connections=tuple(sorted(variable_connections, key=_connection_sort_key)),
        stable_defined_centers=(
            next(iter(defined_center_values)) if len(defined_center_values) == 1 else None
        ),
        stable_open_centers=(
            next(iter(open_center_values)) if len(open_center_values) == 1 else None
        ),
        stable_center_configuration=(
            next(iter(center_configuration_values))
            if len(center_configuration_values) == 1
            else None
        ),
        center_configuration_varies=len(center_configuration_values) > 1,
        stable_composite_definition=(
            next(iter(definition_values)) if len(definition_values) == 1 else None
        ),
        composite_definition_varies=len(definition_values) > 1,
        partner_types_seen=tuple(sorted(partner_types, key=lambda item: item.value)),
    )


def _merge_adjacent_equal_states(
    intervals: tuple[AnalyzedPartnershipInterval, ...],
) -> tuple[AnalyzedPartnershipInterval, ...]:
    merged: list[AnalyzedPartnershipInterval] = []
    for item in intervals:
        if (
            merged
            and merged[-1].end_utc == item.start_utc
            and merged[-1].analysis.fingerprint_sha256 == item.analysis.fingerprint_sha256
        ):
            previous = merged[-1]
            merged[-1] = AnalyzedPartnershipInterval(
                start_utc=previous.start_utc,
                end_utc=item.end_utc,
                analysis=previous.analysis,
            )
        else:
            merged.append(item)
    return tuple(merged)


def _connection_sort_key(item: ConnectionChannel) -> tuple[str, str, str, str]:
    return (
        item.channel,
        item.kind.value,
        item.dominant_partner or "",
        item.compromised_partner or "",
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("relationship interval timestamps must be timezone-aware")
    return value.astimezone(UTC)
