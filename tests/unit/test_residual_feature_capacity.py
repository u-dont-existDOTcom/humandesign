from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import pytest

from hdmatch.evaluation.residual_feature_capacity import audit_v36_residual_feature_capacity
from hdmatch.runtime.century_cache import CenturyCacheManifest, CenturyCacheShard
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


def test_residual_capacity_splits_a_clean_observable_tie() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("a", start, sun_gate=1, chart_hash="0" * 64),
        _state("b", start + timedelta(hours=1), sun_gate=2, chart_hash="1" * 64),
        _state("c", start + timedelta(hours=2), sun_gate=3, chart_hash="2" * 64),
    )
    model = {
        "mappings": [
            {
                "id": "TYPE_GENERATOR",
                "cluster": "TYPE_ENTRY",
                "post_selection": False,
                "predicate": {"feature": "type", "equals": "generator"},
            }
        ],
        "contradictions": [],
    }
    report = audit_v36_residual_feature_capacity(
        states,
        _manifest(start, 3),
        model,
        reference_timestamp=start + timedelta(minutes=30),
    )
    by_id = {item.feature_id: item for item in report.ranked_features}
    sun = by_id["activation:personality:sun"]

    assert report.baseline.unique_fingerprints == 1
    assert report.reference_baseline_tie_size == 3
    assert sun.incremental_uniform_bits == pytest.approx(1.584962500721156)
    assert sun.reference_distinct_values_within_tie == 3
    assert sun.reference_tie_size_after_feature == 1
    assert sun.reference_is_unique_after_feature


def test_residual_capacity_is_not_behavioral_validation() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("a", start, sun_gate=1, chart_hash="0" * 64),
        _state("b", start + timedelta(hours=1), sun_gate=2, chart_hash="1" * 64),
    )
    model = {
        "mappings": [
            {
                "id": "TYPE_GENERATOR",
                "cluster": "TYPE_ENTRY",
                "predicate": {"feature": "type", "equals": "generator"},
            }
        ],
        "contradictions": [],
    }
    report = audit_v36_residual_feature_capacity(
        states,
        _manifest(start, 2),
        model,
        reference_timestamp=start + timedelta(minutes=30),
    )
    assert not hasattr(report.ranked_features[0], "behavioral_validity")


def _state(
    state_id: str,
    start: datetime,
    *,
    sun_gate: int,
    chart_hash: str,
) -> CandidateState:
    end = start + timedelta(hours=1)
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=chart_hash,
        chart_features=StructuralChartFeatures(
            type="generator",
            strategy="wait_to_respond",
            authority="sacral",
            profile="1/3",
            definition="single",
            defined_centers=("sacral",),
            channels=("1-8",),
            activation_gates={"personality:sun": sun_gate},
        ),
        local_date_overlaps=(
            LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),
        ),
    )


def _manifest(start: datetime, count: int) -> CenturyCacheManifest:
    end = start + timedelta(hours=count)
    return CenturyCacheManifest(
        cache_version="test",
        utc_start=start,
        utc_end_exclusive=end,
        interval_count=count,
        canonical_rows_sha256="3" * 64,
        engine_fingerprint="4" * 64,
        design_root_tolerance_seconds=0.01,
        generation_commit="test",
        created_at_utc=start,
        shards=(
            CenturyCacheShard(
                filename="test.jsonl.gz",
                first_state_utc=start,
                last_state_end_utc=end,
                state_count=count,
                sha256="5" * 64,
                uncompressed_bytes=1,
            ),
        ),
    )
