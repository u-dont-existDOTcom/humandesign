"""Generate checkpoint-2 civil-day and transition fixtures with the real engine."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from hdmatch.chart.boundaries import enumerate_chart_boundaries
from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import CelestialBody, SwissEphemerisProvider
from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.conformance import independently_enumerate_line_transitions
from hdmatch.natal_time.enumerator import _validated_civil_date_domain, enumerate_manifest
from hdmatch.natal_time.evidence import assess_evidence
from hdmatch.natal_time.models import (
    CandidateDateSetEvidence,
    DateEvidence,
    DocumentaryVerification,
    EvidenceLineage,
    EvidenceSource,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayEvidence,
)
from hdmatch.natal_time.provenance import (
    build_engine_provenance,
    full_state_identity_specification,
)
from hdmatch.natal_time.records import (
    FixtureClassification,
    NatalTimeFreeze,
    NatalTimeManifest,
    TimezoneResolution,
    deterministic_computation_sha256,
)
from hdmatch.runtime.chart_adapter import declared_ephemeris_files
from hdmatch.util import canonical_json_bytes, sha256_json

CREATED_AT = datetime(2026, 8, 30, 6, 0, tzinfo=UTC)
ROOT_TOLERANCE_SECONDS = 0.000001
FIXTURES: tuple[tuple[str, tuple[date, ...], str, tuple[float, ...]], ...] = (
    ("ordinary_and_multiple_dates", (date(2024, 1, 15), date(2024, 1, 16)), "UTC", (24, 24)),
    ("leap_day", (date(2024, 2, 29),), "UTC", (24,)),
    ("dst_gap", (date(2024, 3, 10),), "America/New_York", (23,)),
    ("dst_fold", (date(2024, 11, 3),), "America/New_York", (25,)),
    ("non_one_hour_dst", (date(2024, 4, 7),), "Australia/Lord_Howe", (24.5,)),
    ("historical_second_offset", (date(1970, 1, 1),), "Africa/Monrovia", (24,)),
    ("non_integer_offset", (date(2024, 1, 15),), "Asia/Kathmandu", (24,)),
)


def _id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:024X}"


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _lineage(index: int, candidate_dates: tuple[date, ...]) -> EvidenceLineage:
    first = candidate_dates[0]
    date_evidence = DateEvidence(
        evidence_id=_id("NTE", index * 100 + 1),
        asserted_date=first,
        source=EvidenceSource.MEMORY,
        documentary_verification=DocumentaryVerification.NOT_APPLICABLE,
        entered_at_utc=CREATED_AT,
        entered_how="conspicuously_synthetic_real_engine_fixture",
    )
    weekday = WeekdayEvidence(
        evidence_id=_id("NTE", index * 100 + 2),
        answer_status=WeekdayAnswerStatus.REMEMBERED,
        asserted_weekday=(
            Weekday.from_date(first)
            if len(candidate_dates) == 1
            else next(value for value in Weekday if value is not Weekday.from_date(first))
        ),
        entered_at_utc=CREATED_AT,
        entered_how="conspicuously_synthetic_real_engine_fixture",
        locked_at_utc=CREATED_AT,
        server_lock_sequence=index,
    )
    if len(candidate_dates) == 1:
        return EvidenceLineage(
            lineage_id=_id("NTL", index),
            version=1,
            date_evidence=(date_evidence,),
            weekday_evidence=weekday,
        )
    initial = EvidenceLineage(
        lineage_id=_id("NTL", index),
        version=1,
        date_evidence=(date_evidence,),
        weekday_evidence=weekday,
    )
    return EvidenceLineage(
        lineage_id=initial.lineage_id,
        version=2,
        date_evidence=initial.date_evidence,
        weekday_evidence=initial.weekday_evidence,
        candidate_date_set=CandidateDateSetEvidence(
            evidence_id=_id("NTE", index * 100 + 3),
            candidate_dates=candidate_dates,
            declared_date_evidence_ids=(date_evidence.evidence_id,),
            confirmed_at_utc=CREATED_AT + timedelta(minutes=index),
            confirmed_how="conspicuously_synthetic_real_engine_fixture",
        ),
        supersedes_lineage_sha256=initial.content_sha256,
    )


def _manifest_and_freeze(
    provider: SwissEphemerisProvider,
    repository_root: Path,
    repository_commit: str,
    runtime_sha256: str,
    index: int,
    candidate_dates: tuple[date, ...],
    timezone: str,
) -> tuple[NatalTimeManifest, NatalTimeFreeze]:
    lineage = _lineage(index, candidate_dates)
    assessment = assess_evidence(lineage)
    provenance = build_engine_provenance(
        provider,
        repository_commit=repository_commit,
        dependency_lock_path=repository_root / "requirements-dev.lock",
        runtime_or_container_sha256=runtime_sha256,
        iana_timezone=timezone,
        boundary_root_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    identity = full_state_identity_specification()
    manifest = NatalTimeManifest(
        manifest_id=_id("NTM", index),
        created_at_utc=CREATED_AT,
        evidence_lineage_sha256=lineage.content_sha256,
        candidate_dates=assessment.operative_dates,
        timezone_resolution=TimezoneResolution(
            iana_timezone=timezone,
            resolution_method="conspicuously_synthetic_explicit_fixture",
            participant_confirmed=True,
            timezone_database_version=provenance.timezone_database_version,
            timezone_file_sha256=provenance.timezone_file_sha256,
        ),
        engine_provenance=provenance,
        state_identity_specification=identity,
        state_identity_sha256=identity.content_sha256,
        fixture_classification=FixtureClassification.SYNTHETIC,
    )
    freeze = NatalTimeFreeze(
        freeze_id=_id("NTF", index),
        created_at_utc=CREATED_AT,
        manifest_sha256=manifest.content_sha256,
        deterministic_computation_sha256=deterministic_computation_sha256(manifest),
        repository_commit=repository_commit,
        engine_provenance_sha256=provenance.content_sha256,
        state_identity_sha256=identity.content_sha256,
    )
    return manifest, freeze


def _event_key(encoded: str) -> tuple[datetime, str, CelestialBody, int, int, int, int]:
    at, side, body, transition = encoded.split("|", 3)
    before, after = transition.split("->", 1)
    before_gate, before_line = (int(value) for value in before.split("."))
    after_gate, after_line = (int(value) for value in after.split("."))
    return (
        datetime.fromisoformat(at),
        side,
        CelestialBody(body),
        before_gate,
        before_line,
        after_gate,
        after_line,
    )


def _result_events(result: Any, civil_date: date) -> tuple[str, ...]:
    return tuple(
        event
        for interval in result.intervals
        if interval.civil_date == civil_date
        for event in interval.boundary_events
    )


def _fixture_summary(
    name: str,
    expected_hours: tuple[float, ...],
    manifest: NatalTimeManifest,
    freeze: NatalTimeFreeze,
    result: Any,
) -> dict[str, Any]:
    actual_hours = tuple(
        item.actual_duration_microseconds / 3_600_000_000 for item in result.coverage_receipts
    )
    if actual_hours != expected_hours:
        raise RuntimeError(f"{name} civil-day duration mismatch: {actual_hours}")
    return {
        "name": name,
        "synthetic": True,
        "candidate_dates": [value.isoformat() for value in manifest.candidate_dates],
        "candidate_ordering": manifest.candidate_ordering,
        "iana_timezone": manifest.timezone_resolution.iana_timezone,
        "manifest_sha256": manifest.content_sha256,
        "freeze_sha256": freeze.content_sha256,
        "result_sha256": result.content_sha256,
        "coverage_receipts": [item.model_dump(mode="json") for item in result.coverage_receipts],
        "interval_count": len(result.intervals),
        "full_state_count": len({item.full_state_sha256 for item in result.intervals}),
        "ranking_present": result.ranking_present,
        "weights_present": result.weights_present,
        "probability_present": result.probability_present,
        "relationship_evidence_included": result.relationship_evidence_included,
    }


def _ordinary_transition_audits(
    provider: SwissEphemerisProvider,
    result: Any,
) -> dict[str, Any]:
    ordinary_date = date(2024, 1, 15)
    events = _result_events(result, ordinary_date)
    production_keys = tuple(sorted(_event_key(item) for item in events))
    start = datetime(2024, 1, 15, tzinfo=UTC)
    end = datetime(2024, 1, 16, tzinfo=UTC)
    independent = independently_enumerate_line_transitions(
        provider,
        start,
        end,
        initial_scan_step_seconds=3600.0,
        design_root_time_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    independent_keys = tuple(
        (
            item.at_utc,
            item.side,
            item.body,
            item.before_gate,
            item.before_line,
            item.after_gate,
            item.after_line,
        )
        for item in independent.transitions
    )
    if production_keys != independent_keys:
        raise RuntimeError("independent transition enumeration disagrees with production")

    by_time: dict[datetime, list[tuple[datetime, str, CelestialBody, int, int, int, int]]] = (
        defaultdict(list)
    )
    for item in production_keys:
        by_time[item[0]].append(item)
    coincident = tuple(values for values in by_time.values() if len(values) > 1)
    positive_gaps = tuple(
        (following[0] - previous[0]).total_seconds()
        for previous, following in zip(production_keys, production_keys[1:], strict=False)
        if following[0] > previous[0]
    )
    near_pairs = tuple(
        (previous, following)
        for previous, following in zip(production_keys, production_keys[1:], strict=False)
        if 0 < (following[0] - previous[0]).total_seconds() <= 120.0
    )
    if not coincident or not near_pairs:
        raise RuntimeError("ordinary fixture lacks coincident or near-coincident transitions")

    ordinary_intervals = tuple(
        item for item in result.intervals if item.civil_date == ordinary_date
    )
    reduced_groups: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for interval in ordinary_intervals:
        graph = interval.full_state["bodygraph"]
        signature = (graph["type"], graph["authority"], graph["profile"])
        reduced_groups[signature].add(interval.full_state_sha256)
    collisions = tuple(
        {"reduced_signature": list(signature), "distinct_full_state_sha256": sorted(hashes)}
        for signature, hashes in sorted(reduced_groups.items())
        if len(hashes) > 1
    )
    if not collisions:
        raise RuntimeError("ordinary fixture lacks a reduced-signature collision")

    first = production_keys[0]
    edge_before = enumerate_chart_boundaries(
        provider,
        first[0] - timedelta(seconds=1),
        first[0],
        bodies=(first[2],),
        root_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    edge_after = enumerate_chart_boundaries(
        provider,
        first[0],
        first[0] + timedelta(seconds=1),
        bodies=(first[2],),
        root_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    if edge_before or edge_after:
        raise RuntimeError("half-open edge fixture duplicated an endpoint transition")

    first_design = next(item for item in production_keys if item[1] == "design")
    before_chart = calculate_chart(
        provider,
        first_design[0] - timedelta(microseconds=1),
        design_time_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    at_chart = calculate_chart(
        provider,
        first_design[0],
        design_time_tolerance_seconds=ROOT_TOLERANCE_SECONDS,
    )
    return {
        "production_event_count": len(production_keys),
        "independent_event_count": len(independent.transitions),
        "exact_event_key_agreement": True,
        "independent_enumeration_sha256": independent.content_sha256,
        "independent_series_certificates": [
            item.model_dump(mode="json") for item in independent.series_certificates
        ],
        "personality_moon_transition_count": sum(
            item[1] == "personality" and item[2] is CelestialBody.MOON for item in production_keys
        ),
        "design_moon_transition_count": sum(
            item[1] == "design" and item[2] is CelestialBody.MOON for item in production_keys
        ),
        "coincident_transition_groups": [
            [
                {"at_utc": _utc_text(item[0]), "side": item[1], "body": item[2].value}
                for item in group
            ]
            for group in coincident
        ],
        "minimum_positive_inter_event_gap_seconds": min(positive_gaps),
        "near_coincident_pairs_within_120_seconds": [
            {
                "gap_seconds": (following[0] - previous[0]).total_seconds(),
                "first": {
                    "at_utc": _utc_text(previous[0]),
                    "side": previous[1],
                    "body": previous[2].value,
                },
                "second": {
                    "at_utc": _utc_text(following[0]),
                    "side": following[1],
                    "body": following[2].value,
                },
            }
            for previous, following in near_pairs
        ],
        "reduced_signature_collisions": collisions,
        "day_edge_fixture": {
            "transition_at_exclusive_end_duplicated": False,
            "transition_at_inclusive_start_duplicated": False,
            "edge_transition": {
                "at_utc": _utc_text(first[0]),
                "side": first[1],
                "body": first[2].value,
            },
        },
        "design_root_boundary_fixture": {
            "boundary_at_utc": _utc_text(first_design[0]),
            "body": first_design[2].value,
            "before_design_utc": _utc_text(before_chart.design_utc),
            "at_design_utc": _utc_text(at_chart.design_utc),
            "before_residual_degrees": before_chart.design_root.residual_degrees,
            "at_residual_degrees": at_chart.design_root.residual_degrees,
            "time_tolerance_seconds": ROOT_TOLERANCE_SECONDS,
            "before_and_at_full_state_distinct": (
                before_chart.chart_features_sha256 != at_chart.chart_features_sha256
            ),
        },
    }


def build_audit(
    repository_root: Path,
    repository_commit: str,
    ephemeris_path: Path,
    engine_identity_path: Path,
) -> dict[str, Any]:
    identity = json.loads(engine_identity_path.read_text())
    runtime_sha256 = identity["runtime"]["sha256"]
    provider = SwissEphemerisProvider(declared_ephemeris_files(ephemeris_path))
    summaries: list[dict[str, Any]] = []
    ordinary_result: Any | None = None
    for index, (name, candidate_dates, timezone, expected_hours) in enumerate(FIXTURES, start=1):
        print(f"REAL_ENGINE_FIXTURE_START:{name}", file=sys.stderr, flush=True)
        manifest, freeze = _manifest_and_freeze(
            provider,
            repository_root,
            repository_commit,
            runtime_sha256,
            index,
            candidate_dates,
            timezone,
        )
        result = enumerate_manifest(provider, manifest, freeze)
        summaries.append(_fixture_summary(name, expected_hours, manifest, freeze, result))
        if name == "ordinary_and_multiple_dates":
            ordinary_result = result
        print(f"REAL_ENGINE_FIXTURE_DONE:{name}", file=sys.stderr, flush=True)

    if ordinary_result is None:  # pragma: no cover - fixture invariant
        raise RuntimeError("ordinary result was not generated")
    try:
        _validated_civil_date_domain(date(2011, 12, 30), ZoneInfo("Pacific/Apia"))
    except ValueError as exc:
        skipped_date = {
            "name": "skipped_civil_date",
            "civil_date": "2011-12-30",
            "iana_timezone": "Pacific/Apia",
            "enumeration_allowed": False,
            "failure_type": type(exc).__name__,
            "failure_message": str(exc),
        }
    else:  # pragma: no cover - timezone invariant
        raise RuntimeError("Pacific/Apia skipped date unexpectedly had an instant domain")

    historical = next(item for item in summaries if item["name"] == "historical_second_offset")
    historical_start = historical["coverage_receipts"][0]["domain_start"]
    kathmandu = next(item for item in summaries if item["name"] == "non_integer_offset")
    kathmandu_start = kathmandu["coverage_receipts"][0]["domain_start"]
    lord_howe = next(item for item in summaries if item["name"] == "non_one_hour_dst")
    payload: dict[str, Any] = {
        "schema_version": "natal-time-real-engine-fixture-audit-v1",
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "repository_commit": repository_commit,
        "engine_identity_packet_sha256": identity["packet_sha256"],
        "synthetic_only": True,
        "qualification_status": "pending_pro_review",
        "fixtures": summaries,
        "skipped_date_fixture": skipped_date,
        "timezone_assertions": {
            "historical_monrovia_offset_seconds": historical_start["utc_offset_seconds"],
            "kathmandu_offset_seconds": kathmandu_start["utc_offset_seconds"],
            "lord_howe_duration_hours": (
                lord_howe["coverage_receipts"][0]["actual_duration_microseconds"] / 3_600_000_000
            ),
        },
        "transition_audits": _ordinary_transition_audits(provider, ordinary_result),
        "transition_completeness_basis": {
            "primitive_changing_fields": "all personality/design gate and line activations",
            "derived_fields": (
                "all Bodygraph fields are pure functions of the complete activation vector"
            ),
            "immutable_fields": (
                "engine version, constants digests, and unavailable-substructure status"
            ),
            "direct_retrograde_stationary_repeated": (
                "speed-bounded recursion never treats equal endpoints as stability proof"
            ),
            "design_side": (
                "88-degree root solved to one Python coordinate microsecond with measured "
                "Julian-grid uncertainty"
            ),
            "equality": "exact mandala boundaries enter the new half-open sector",
            "day_edges": (
                "civil days and intervals are half-open; endpoint transitions are not duplicated"
            ),
        },
        "forbidden_semantics": {
            "ranking": False,
            "weights": False,
            "probability": False,
            "duration_mass": False,
            "candidate_selection": False,
            "relationship_evidence": False,
        },
    }
    if payload["timezone_assertions"] != {
        "historical_monrovia_offset_seconds": -2670,
        "kathmandu_offset_seconds": 20700,
        "lord_howe_duration_hours": 24.5,
    }:
        raise RuntimeError(f"timezone edge assertion changed: {payload['timezone_assertions']}")
    payload["audit_sha256"] = sha256_json(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-commit", required=True)
    parser.add_argument("--ephemeris", type=Path, default=Path("data/ephemeris"))
    parser.add_argument(
        "--engine-identity",
        type=Path,
        default=Path("state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = build_audit(
        args.repository_root.resolve(strict=True),
        args.repository_commit,
        args.ephemeris.resolve(strict=True),
        args.engine_identity.resolve(strict=True),
    )
    encoded = canonical_json_bytes(payload) + b"\n"
    if args.output is None:
        print(encoded.decode(), end="")
    else:
        write_new_bytes(args.output, encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
