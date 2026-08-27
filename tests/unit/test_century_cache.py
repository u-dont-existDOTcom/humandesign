"""Tests for the reusable verified exact-state century cache."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.runtime.century_cache import (
    CenturyCacheVerificationError,
    GlobalCandidateState,
    load_century_candidate_states,
    verify_century_cache,
    write_verified_century_cache,
)
from hdmatch.schemas import ChartFeatures


def _chart(at_utc: datetime, label: str) -> ChartFeatures:
    return ChartFeatures(
        personality_utc=at_utc,
        design_utc=at_utc - timedelta(days=88),
        type=f"Type-{label}",
        strategy=f"Strategy-{label}",
        authority=f"Authority-{label}",
        profile="1/3",
        definition="Single",
        activations={},
    )


def _states() -> tuple[GlobalCandidateState, ...]:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    middle = start + timedelta(hours=12)
    end = start + timedelta(days=1)
    return (
        GlobalCandidateState(
            state_id="STATE-A",
            start_utc=start,
            end_utc=middle,
            chart_features_hash="a" * 64,
            chart_features=_chart(start + timedelta(hours=6), "A"),
        ),
        GlobalCandidateState(
            state_id="STATE-B",
            start_utc=middle,
            end_utc=end,
            chart_features_hash="b" * 64,
            chart_features=_chart(middle + timedelta(hours=6), "B"),
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


def test_century_cache_rejects_adjacent_identical_features(tmp_path: Path) -> None:
    first, second = _states()
    invalid = (
        first,
        second.model_copy(update={"chart_features_hash": first.chart_features_hash}),
    )
    with pytest.raises(CenturyCacheVerificationError, match="identical adjacent"):
        write_verified_century_cache(
            tmp_path / "invalid",
            invalid,
            engine_fingerprint="c" * 64,
            generation_commit="test-commit",
            created_at_utc=datetime(2026, 8, 27, tzinfo=UTC),
        )
