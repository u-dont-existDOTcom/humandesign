#!/usr/bin/env python3
"""Build the exact score-relevant century universe with the proven event engine.

The generic all-lines boundary engine is intentionally conservative, but resolving
six lines for every body is unnecessary for the current structural search and made
10-year CI shards exceed 90 minutes.  This builder uses the already-audited direct
Swiss event generator to enumerate:

* every Personality/Design activation *gate* transition; and
* Personality/Design Sun *line* transitions, because those define profile.

Earth and South Node are deterministic oppositions and are updated with Sun/North
Node events.  Non-Sun line changes do not affect type, strategy, authority, profile,
definition, centers, channels, or activation gates and therefore do not split the
structural candidate universe.

The incremental state is sampled against the normal production ExactChartAdapter at
a deterministic cadence.  The cache remains fail-closed on pinned Swiss files and
records the production engine fingerprint.
"""

from __future__ import annotations

import argparse
import importlib
import os
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import swisseph as swe

from hdmatch.chart.bodygraph import GateActivation, derive_bodygraph
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.runtime.century_cache import (
    GlobalCandidateState,
    structural_features_sha256,
    write_verified_century_cache,
)
from hdmatch.runtime.chart_adapter import ExactChartAdapter
from hdmatch.schemas import ChartFeatures, StructuralChartFeatures
from hdmatch.util import sha256_json

DEFAULT_START = datetime(1926, 8, 22, tzinfo=UTC)
DEFAULT_END = datetime(2026, 8, 23, tzinfo=UTC)


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamps must include a UTC offset")
    return parsed.astimezone(UTC)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--start", type=_utc, default=DEFAULT_START)
    parser.add_argument("--end-exclusive", type=_utc, default=DEFAULT_END)
    parser.add_argument("--shard-years", type=int, default=10)
    parser.add_argument("--root-tolerance-seconds", type=float, default=0.01)
    parser.add_argument("--scan-step-days", type=float, default=0.25)
    parser.add_argument("--verify-every", type=int, default=1000)
    parser.add_argument(
        "--generation-commit",
        default=os.environ.get("GITHUB_SHA", "unknown"),
    )
    return parser.parse_args()


def _load_event_engine(args: argparse.Namespace) -> ModuleType:
    # swieph_ab_rerun computes its horizon globals at import time.
    os.environ["HD_START"] = args.start.isoformat()
    os.environ["HD_END"] = args.end_exclusive.isoformat()
    base = importlib.import_module("swieph_ab_rerun")
    base.TOL = args.root_tolerance_seconds / 86400.0
    base.STEP = args.scan_step_days
    swe.set_ephe_path(str(args.ephemeris.resolve()))
    return base


def _production_structure(chart: ChartFeatures) -> StructuralChartFeatures:
    return StructuralChartFeatures(
        type=chart.type,
        strategy=chart.strategy,
        authority=chart.authority,
        profile=chart.profile,
        definition=chart.definition,
        defined_centers=chart.defined_centers,
        channels=chart.channels,
        activation_gates={
            key: activation.gate for key, activation in sorted(chart.activations.items())
        },
    )


def _incremental_structure(acts: dict[str, dict[str, list[int]]]) -> StructuralChartFeatures:
    activations: list[GateActivation] = []
    activation_gates: dict[str, int] = {}
    for short_side, side in (("p", "personality"), ("d", "design")):
        for body_name, (gate, line) in sorted(acts[short_side].items()):
            body = CelestialBody(body_name)
            # derive_bodygraph only uses non-Sun line values for no core mechanic;
            # retain the tracked value anyway and keep a harmless dummy longitude.
            activations.append(
                GateActivation(
                    body=body,
                    side=side,  # type: ignore[arg-type]
                    longitude=0.0,
                    gate=gate,
                    line=line,
                )
            )
            activation_gates[f"{side}:{body.value}"] = gate
    bodygraph = derive_bodygraph(activations)
    return StructuralChartFeatures(
        type=bodygraph.type.value,
        strategy=bodygraph.strategy.value,
        authority=bodygraph.authority.value,
        profile=bodygraph.profile,
        definition=bodygraph.definition.value,
        defined_centers=tuple(center.value for center in bodygraph.defined_centers),
        channels=bodygraph.channels,
        activation_gates=activation_gates,
    )


def _state_id(start: datetime, end: datetime, feature_hash: str) -> str:
    return "STATE-" + sha256_json(
        {
            "start_utc": start.isoformat(),
            "end_utc": end.isoformat(),
            "structural_feature_sha256": feature_hash,
        }
    )[:24].upper()


def _event_groups(
    raw_events: list[tuple[float, str, str, str, int, int]],
    *,
    tolerance_seconds: float,
) -> list[list[tuple[float, str, str, str, int, int]]]:
    """Group only numerical duplicates from the same body/side.

    Independent bodies that happen to cross close together remain separate exact
    states; this avoids the old audit's broad 0.5-second coalescing rule.
    """

    groups: list[list[tuple[float, str, str, str, int, int]]] = []
    for event in sorted(raw_events, key=lambda item: item[0]):
        if groups:
            previous = groups[-1][0]
            close = abs(event[0] - previous[0]) * 86400.0 <= 2.0 * tolerance_seconds
            same_series = event[1:3] == previous[1:3]
            if close and same_series:
                groups[-1].append(event)
                continue
        groups.append([event])
    return groups


def _build_states(
    base: ModuleType,
    adapter: ExactChartAdapter,
    *,
    verify_every: int,
    tolerance_seconds: float,
) -> tuple[GlobalCandidateState, ...]:
    raw: dict[tuple[str, str], list[float]] = {}
    for name, body_id in base.BODY_IDS.items():
        events = base.generate(name, body_id, "gate")
        raw[(name, "gate")] = events
        print("EVENTS", name, "gate", len(events), flush=True)
    sun_lines = base.generate("sun", swe.SUN, "line")
    raw[("sun", "line")] = sun_lines
    print("EVENTS sun line", len(sun_lines), flush=True)

    events: list[tuple[float, str, str, str, int, int]] = []
    epsilon_days = max(2.0 * tolerance_seconds, 0.02) / 86400.0
    for (name, kind), event_jds in raw.items():
        body_id = base.BODY_IDS[name]
        for event_jd in event_jds:
            longitude_after, _ = base.lon_speed(event_jd + epsilon_days, body_id)
            after_gate, after_line = base.gate_line(longitude_after)
            if base.START < event_jd < base.END:
                events.append((event_jd, "p", name, kind, after_gate, after_line))
            if base.START - 105.0 < event_jd < base.END - 70.0:
                birth_jd = base.forward_birth(event_jd)
                if base.START < birth_jd < base.END:
                    events.append((birth_jd, "d", name, kind, after_gate, after_line))

    groups = _event_groups(events, tolerance_seconds=tolerance_seconds)
    group_jds = [sum(event[0] for event in group) / len(group) for group in groups]
    bounds = [base.START, *group_jds, base.END]
    print("BOUNDARIES", len(bounds), "GROUPS", len(groups), flush=True)

    acts = base.initial_state((bounds[0] + bounds[1]) / 2.0)
    counter = base.gate_counter(acts)
    states: list[GlobalCandidateState] = []
    for index, (left_jd, right_jd) in enumerate(zip(bounds, bounds[1:], strict=False)):
        if index > 0:
            for _, side, name, kind, after_gate, after_line in groups[index - 1]:
                base.apply_event(
                    acts,
                    counter,
                    side,
                    name,
                    kind,
                    after_gate,
                    after_line,
                )
        start = base.dt_from_jd(left_jd)
        end = base.dt_from_jd(right_jd)
        if end <= start:
            raise RuntimeError("event builder produced a non-positive structural interval")
        features = _incremental_structure(acts)
        feature_hash = structural_features_sha256(features)

        should_verify = (
            verify_every > 0
            and (index == 0 or index == len(bounds) - 2 or index % verify_every == 0)
        )
        if should_verify:
            representative = start + (end - start) / 2
            exact = _production_structure(adapter.calculate(representative))
            if exact != features:
                raise RuntimeError(
                    "incremental structural state disagrees with production chart engine "
                    f"at {representative.isoformat()}"
                )

        ending_events: tuple[str, ...] = ()
        if index < len(groups):
            at = base.dt_from_jd(group_jds[index])
            ending_events = tuple(
                f"{at.isoformat()}|{'personality' if side == 'p' else 'design'}|"
                f"{name}|{kind}|{after_gate}.{after_line}"
                for _, side, name, kind, after_gate, after_line in groups[index]
            )
        states.append(
            GlobalCandidateState(
                state_id=_state_id(start, end, feature_hash),
                start_utc=start,
                end_utc=end,
                chart_features_hash=feature_hash,
                chart_features=features,
                boundary_events=ending_events,
            )
        )

    # Numerical duplicate groups should already prevent identical adjacent rows.
    # If an event has no effect on the stored structural vector, merge it rather
    # than manufacturing an unobservable candidate state.
    merged: list[GlobalCandidateState] = []
    for state in states:
        if merged and merged[-1].chart_features_hash == state.chart_features_hash:
            previous = merged.pop()
            merged.append(
                GlobalCandidateState(
                    state_id=_state_id(previous.start_utc, state.end_utc, state.chart_features_hash),
                    start_utc=previous.start_utc,
                    end_utc=state.end_utc,
                    chart_features_hash=state.chart_features_hash,
                    chart_features=state.chart_features,
                    boundary_events=previous.boundary_events + state.boundary_events,
                )
            )
        else:
            merged.append(state)
    return tuple(merged)


def main() -> None:
    args = parse_args()
    if args.end_exclusive <= args.start:
        raise SystemExit("--end-exclusive must be after --start")
    if args.root_tolerance_seconds <= 0.0:
        raise SystemExit("--root-tolerance-seconds must be positive")
    if args.scan_step_days <= 0.0:
        raise SystemExit("--scan-step-days must be positive")

    adapter = ExactChartAdapter(args.ephemeris)
    base = _load_event_engine(args)
    print("engine_fingerprint", adapter.fingerprint, flush=True)
    print("building_structural_states", args.start.isoformat(), args.end_exclusive.isoformat())
    states = _build_states(
        base,
        adapter,
        verify_every=args.verify_every,
        tolerance_seconds=args.root_tolerance_seconds,
    )
    print("structural_interval_count", len(states), flush=True)

    manifest = write_verified_century_cache(
        args.output,
        states,
        engine_fingerprint=adapter.fingerprint,
        generation_commit=args.generation_commit,
        created_at_utc=datetime.now(UTC),
        design_root_tolerance_seconds=args.root_tolerance_seconds,
        shard_years=args.shard_years,
    )
    print("cache_version", manifest.cache_version, flush=True)
    print("interval_count", manifest.interval_count, flush=True)
    print("canonical_rows_sha256", manifest.canonical_rows_sha256, flush=True)
    print("manifest", args.output / "manifest.json", flush=True)


if __name__ == "__main__":
    main()
