"""Typed adapter from chart-engine dataclasses to public experiment schemas."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from hdmatch.chart import (
    ChartFeatureVectorV2,
    SwissEphemerisProvider,
    calculate_chart,
    serialize_chart_feature_vector,
)
from hdmatch.chart.bodygraph import bodygraph_constants_sha256
from hdmatch.chart.boundaries import build_production_chart_state_intervals
from hdmatch.chart.calculator import ChartComputation
from hdmatch.chart.ephemeris import EphemerisConfigurationError
from hdmatch.chart.rave_mandala import mandala_constants_sha256
from hdmatch.schemas import Activation, CandidateState, ChartFeatures
from hdmatch.search import split_interval_by_local_date
from hdmatch.util import sha256_json


def declared_ephemeris_files(path: str | Path) -> tuple[Path, ...]:
    """Resolve the exact local Swiss files authorized for a run.

    A directory is accepted for CLI convenience, but every ``.se1`` file it
    contains is enumerated and hashed by :class:`SwissEphemerisProvider`.
    Nothing is downloaded and Swiss's analytical fallback remains forbidden.
    """

    source = Path(path).expanduser().resolve(strict=False)
    candidates: tuple[Path, ...]
    if source.is_file():
        candidates = (source,)
    elif source.is_dir():
        candidates = tuple(sorted(source.glob("*.se1")))
    else:
        raise EphemerisConfigurationError(f"ephemeris path does not exist: {source}")
    if not candidates:
        raise EphemerisConfigurationError(f"no .se1 files found under: {source}")
    return candidates


class ExactChartAdapter:
    """Calculate exact charts and complete stable interval partitions."""

    def __init__(self, ephemeris_path: str | Path) -> None:
        self.provider = SwissEphemerisProvider(declared_ephemeris_files(ephemeris_path))

    @property
    def fingerprint(self) -> str:
        metadata = self.provider.metadata
        return sha256_json(
            {
                "provider": metadata.provider,
                "library_version": metadata.library_version,
                "files": [
                    {
                        "name": Path(item.path).name,
                        "sha256": item.sha256,
                        "size_bytes": item.size_bytes,
                    }
                    for item in metadata.files
                ],
                "calculation_flags": metadata.calculation_flags,
                "coordinate_frame": metadata.coordinate_frame,
                "node_convention": metadata.node_convention.value,
                "mandala_constants_sha256": mandala_constants_sha256(),
                "bodygraph_constants_sha256": bodygraph_constants_sha256(),
            }
        )

    def calculate(self, utc_moment: datetime) -> ChartFeatures:
        return _to_chart_features(calculate_chart(self.provider, utc_moment))

    def calculate_cacheable_m0_m2(self, utc_moment: datetime) -> ChartFeatureVectorV2:
        """Return the strict discrete V2 vector without claiming scorer compliance."""

        return serialize_chart_feature_vector(
            calculate_chart(self.provider, utc_moment),
            provider=self.provider,
        )

    def candidate_states(
        self,
        start_utc: datetime,
        end_utc: datetime,
        timezone_name: str,
    ) -> tuple[CandidateState, ...]:
        intervals = build_production_chart_state_intervals(
            self.provider,
            start_utc,
            end_utc,
        )
        result: list[CandidateState] = []
        for interval in intervals:
            computation = calculate_chart(self.provider, interval.representative_utc)
            chart = _to_chart_features(computation)
            stable_hash = interval.feature_sha256
            state_id = "STATE-" + sha256_json(
                {
                    "start_utc": interval.start_utc.isoformat(),
                    "end_utc": interval.end_utc.isoformat(),
                    "stable_feature_sha256": stable_hash,
                }
            )[:24].upper()
            result.append(
                CandidateState(
                    state_id=state_id,
                    start_utc=interval.start_utc,
                    end_utc=interval.end_utc,
                    chart_features_hash=stable_hash,
                    chart_features=chart,
                    local_date_overlaps=split_interval_by_local_date(
                        interval.start_utc, interval.end_utc, timezone_name
                    ),
                    boundary_events=tuple(
                        (
                            f"{event.at_utc.isoformat()}|{event.side}|{event.body.value}|"
                            f"{event.before_gate}.{event.before_line}->"
                            f"{event.after_gate}.{event.after_line}"
                        )
                        for event in interval.boundary_events
                    ),
                )
            )
        return tuple(result)


def _to_chart_features(computation: ChartComputation) -> ChartFeatures:
    bodygraph = computation.bodygraph
    activations = {
        f"{activation.side}:{activation.body.value}": Activation(
            body=activation.body.value,
            side=activation.side,
            longitude=activation.longitude,
            gate=activation.gate,
            line=activation.line,
        )
        for activation in computation.activations
    }
    return ChartFeatures(
        personality_utc=computation.personality_utc,
        design_utc=computation.design_utc,
        type=bodygraph.type.value,
        strategy=bodygraph.strategy.value,
        authority=bodygraph.authority.value,
        profile=bodygraph.profile,
        definition=bodygraph.definition.value,
        defined_centers=tuple(center.value for center in bodygraph.defined_centers),
        channels=bodygraph.channels,
        activations=activations,
        engine_metadata={
            "chart_engine_version": computation.metadata.chart_engine_version,
            "stable_feature_sha256": computation.chart_features_sha256,
            "ephemeris": asdict(computation.metadata.ephemeris),
            "mandala_constants_sha256": computation.metadata.mandala_constants_sha256,
            "bodygraph_constants_sha256": computation.metadata.bodygraph_constants_sha256,
            "design_target_arc_degrees": computation.metadata.design_target_arc_degrees,
            "design_time_tolerance_seconds": (
                computation.metadata.design_time_tolerance_seconds
            ),
            "design_arc_tolerance_degrees": (
                computation.metadata.design_arc_tolerance_degrees
            ),
            "advanced_substructure_status": (
                computation.metadata.advanced_substructure_status
            ),
        },
    )
