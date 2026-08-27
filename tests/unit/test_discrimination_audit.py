from __future__ import annotations

import math
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.evaluation.discrimination import (
    audit_century_discrimination,
    summarize_fingerprints,
)
from hdmatch.model.mapping_library import load_mapping_library
from hdmatch.runtime.century_cache import CenturyCacheManifest, CenturyCacheShard
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures

ROOT = Path(__file__).resolve().parents[2]


def test_summarize_fingerprints_reports_oracle_ceilings() -> None:
    metrics = summarize_fingerprints(("a", "a", "b", "c"), (1.0, 1.0, 1.0, 1.0))

    assert metrics.candidate_count == 4
    assert metrics.unique_fingerprints == 3
    assert metrics.maximum_identity_bits == pytest.approx(2.0)
    assert metrics.uniform_information_bits == pytest.approx(1.5)
    assert metrics.uniform_top1_ceiling == pytest.approx(0.75)
    assert metrics.uniform_top5_ceiling == pytest.approx(1.0)
    assert metrics.tie_size_max == 2


def test_duration_weighted_top1_prefers_longer_interval() -> None:
    metrics = summarize_fingerprints(("a", "a", "b"), (9.0, 1.0, 1.0))

    expected_entropy = -(10.0 / 11.0) * math.log2(10.0 / 11.0) - (1.0 / 11.0) * math.log2(
        1.0 / 11.0
    )
    assert metrics.duration_weighted_information_bits == pytest.approx(expected_entropy)
    assert metrics.duration_weighted_top1_ceiling == pytest.approx(10.0 / 11.0)


def test_full_cache_can_distinguish_states_current_model_cannot() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    features_a = _features(definition="single", channels=("1-8",), gate=1)
    features_b = _features(definition="split", channels=("2-14",), gate=2)
    states = (
        _state("a", start, features_a, "0" * 64),
        _state("b", start + timedelta(hours=1), features_b, "1" * 64),
    )
    manifest = CenturyCacheManifest(
        cache_version="test",
        utc_start=start,
        utc_end_exclusive=start + timedelta(hours=2),
        interval_count=2,
        canonical_rows_sha256="2" * 64,
        engine_fingerprint="3" * 64,
        design_root_tolerance_seconds=0.01,
        generation_commit="test",
        created_at_utc=start,
        shards=(
            CenturyCacheShard(
                filename="test.jsonl.gz",
                first_state_utc=start,
                last_state_end_utc=start + timedelta(hours=2),
                state_count=2,
                sha256="4" * 64,
                uncompressed_bytes=1,
            ),
        ),
    )
    library = load_mapping_library(ROOT / "mappings" / "mapping_library_v1.json")

    report = audit_century_discrimination(states, manifest, library)

    assert report.coarse_structure.unique_fingerprints == 1
    assert report.canonical_answers.unique_fingerprints == 1
    assert report.scoring_rules.unique_fingerprints == 1
    assert report.full_cached_structure.unique_fingerprints == 2
    assert {"definition", "channels", "activation_gates"}.issubset(
        report.cached_features_not_model_visible
    )


def _features(
    *, definition: str, channels: tuple[str, ...], gate: int
) -> StructuralChartFeatures:
    return StructuralChartFeatures(
        type="Generator",
        strategy="Respond",
        authority="Sacral",
        profile="1/3",
        definition=definition,
        defined_centers=("Sacral",),
        channels=channels,
        activation_gates={"personality_sun": gate},
    )


def _state(
    state_id: str,
    start: datetime,
    features: StructuralChartFeatures,
    chart_hash: str,
) -> CandidateState:
    end = start + timedelta(hours=1)
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=chart_hash,
        chart_features=features,
        local_date_overlaps=(LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),),
    )
