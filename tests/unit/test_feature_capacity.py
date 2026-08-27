from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import pytest

from hdmatch.evaluation.feature_capacity import audit_structural_feature_capacity
from hdmatch.runtime.century_cache import CenturyCacheManifest, CenturyCacheShard
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


def test_feature_capacity_ranks_increment_beyond_coarse_structure() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state(
            "a",
            start,
            definition="single",
            channels=("1-8",),
            activations={"personality:sun": 1, "design:sun": 2},
            chart_hash="0" * 64,
        ),
        _state(
            "b",
            start + timedelta(hours=1),
            definition="split",
            channels=("2-14",),
            activations={"personality:sun": 2, "design:sun": 2},
            chart_hash="1" * 64,
        ),
        _state(
            "c",
            start + timedelta(hours=2),
            definition="split",
            channels=("2-14",),
            activations={"personality:sun": 3, "design:sun": 4},
            chart_hash="2" * 64,
        ),
    )
    report = audit_structural_feature_capacity(states, _manifest(start, 3))
    by_id = {item.feature_id: item for item in report.ranked_features}

    assert report.baseline.unique_fingerprints == 1
    assert by_id["activation:personality:sun"].combined_unique_fingerprints == 3
    assert by_id["activation:personality:sun"].incremental_uniform_bits == pytest.approx(
        1.584962500721156
    )
    assert by_id["definition"].combined_unique_fingerprints == 2
    assert by_id["activation_vector:all"].combined_unique_fingerprints == 3
    assert report.ranked_features[0].incremental_duration_weighted_bits >= report.ranked_features[-1].incremental_duration_weighted_bits


def test_feature_capacity_does_not_label_structural_capacity_behavioral_validity() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state(
            "a",
            start,
            definition="single",
            channels=("1-8",),
            activations={"personality:sun": 1},
            chart_hash="0" * 64,
        ),
        _state(
            "b",
            start + timedelta(hours=1),
            definition="single",
            channels=("1-8",),
            activations={"personality:sun": 2},
            chart_hash="1" * 64,
        ),
    )
    report = audit_structural_feature_capacity(states, _manifest(start, 2))

    assert not hasattr(report.ranked_features[0], "behavioral_validity")
    assert not hasattr(report.ranked_features[0], "predictive_validity")


def _state(
    state_id: str,
    start: datetime,
    *,
    definition: str,
    channels: tuple[str, ...],
    activations: dict[str, int],
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
            definition=definition,
            defined_centers=("sacral",),
            channels=channels,
            activation_gates=activations,
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
