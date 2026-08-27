"""Tests for the reusable verified structural-state century cache."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.runtime.century_cache import (
    CenturyCacheVerificationError,
    GlobalCandidateState,
    load_century_candidate_states,
    structural_features_sha256,
    verify_century_cache,
    write_verified_century_cache,
)
from hdmatch.schemas import StructuralChartFeatures


def _chart(label: str) -> StructuralChartFeatures:
    return StructuralChartFeatures(
        type=f"Type-{label}",
        strategy=f"Strategy-{label}",
        authority=f"Authority-{label}",
        profile="1/3",
        definition="Single",
        defined_centers=(f"Center-{label}",),
        channels=(),
        activation_gates={"personality:sun": 1 if label == "A" else 2},
    )


def _states() -> tuple[GlobalCandidateState, ...]:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    middle = start + timedelta(hours=12)
    end = start + timedelta(days=1)
    chart_a = _chart("A")
    chart_b = _chart("B")
    return (
        GlobalCandidateState(
            state_id="STATE-A",
            start_utc=start,
            end_utc=middle,
            chart_features_hash=structural_features_sha256(chart_a),
            chart_features=chart_a,
        ),
        GlobalCandidateState(
            state_id="STATE-B",
            start_utc=middle,
            end_utc=end,
            chart_features_hash=structural_features_sha256(chart_b),
            chart_features=chart_b,
        ),
    )


def _write(tmp_path: Path) -> Path:
    root = tmp_path / "century"
    write_verified_century_cache(
        root,
        _states(),
        engine_fingerprint="c" * 64,
        generation_commit="test-commit",
        created_at_utc=datetime(2026, 8, 27, tzinfo=UTC),
    )
    return root


def test_century_cache_round_trip_localizes_dates(tmp_path: Path) -> None:
    root = _write(tmp_path)
    manifest = verify_century_cache(
        root,
        expected_engine_fingerprint="c" * 64,
    )
    states = load_century_candidate_states(
        root,
        timezone_name="America/New_York",
        expected_engine_fingerprint="c" * 64,
    )
    assert manifest.schema_version == "century-candidate-cache-v2"
    assert manifest.feature_vector_schema_version == "structural-chart-features-v1"
    assert manifest.interval_count == 2
    assert len(states) == 2
    assert sum(item.seconds for item in states[0].local_date_overlaps) == 12 * 3600
    assert states[0].chart_features.type == "Type-A"


def test_century_cache_rejects_engine_mismatch(tmp_path: Path) -> None:
    root = _write(tmp_path)
    with pytest.raises(CenturyCacheVerificationError, match="engine fingerprint"):
        verify_century_cache(root, expected_engine_fingerprint="d" * 64)


def test_century_cache_rejects_tampered_shard(tmp_path: Path) -> None:
    root = _write(tmp_path)
    shard = next(root.glob("states-*.jsonl.gz"))
    shard.write_bytes(shard.read_bytes() + b"tamper")
    with pytest.raises(CenturyCacheVerificationError, match="hash mismatch"):
        verify_century_cache(root, expected_engine_fingerprint="c" * 64)


def test_century_cache_rejects_structural_hash_mismatch() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    chart = _chart("A")
    with pytest.raises(ValueError, match="structural feature hash mismatch"):
        GlobalCandidateState(
            state_id="STATE-BAD",
            start_utc=start,
            end_utc=start + timedelta(hours=1),
            chart_features_hash="f" * 64,
            chart_features=chart,
        )


def test_century_cache_rejects_adjacent_identical_features(tmp_path: Path) -> None:
    first, second = _states()
    invalid = (
        first,
        GlobalCandidateState(
            state_id="STATE-C",
            start_utc=second.start_utc,
            end_utc=second.end_utc,
            chart_features_hash=first.chart_features_hash,
            chart_features=first.chart_features,
        ),
    )
    with pytest.raises(CenturyCacheVerificationError, match="identical adjacent"):
        write_verified_century_cache(
            tmp_path / "invalid",
            invalid,
            engine_fingerprint="c" * 64,
            generation_commit="test-commit",
            created_at_utc=datetime(2026, 8, 27, tzinfo=UTC),
        )
