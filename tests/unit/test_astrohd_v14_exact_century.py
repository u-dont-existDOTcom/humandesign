"""Direct checks of the exact minute-grid consumer, not source-token checks."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
import random
import sys

import pytest
import swisseph as swe

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import scan_astrohd_v14_exact_century as scan


def test_coordinate_success_cannot_hide_ephemeris_fallback(monkeypatch):
    monkeypatch.setattr(swe, 'calc_ut', lambda *args: ((123.0, 0, 0, 0, 0, 0), swe.FLG_MOSEPH))
    with pytest.raises(RuntimeError, match='Ephemeris fallback'):
        scan.longitude(2446100.0, swe.VENUS)


def test_mixed_fallback_flags_are_rejected(monkeypatch):
    monkeypatch.setattr(swe, 'calc_ut', lambda *args: ((123.0, 0, 0, 0, 0, 0), swe.FLG_MOSEPH | swe.FLG_SWIEPH))
    with pytest.raises(RuntimeError, match='Ephemeris fallback'):
        scan.longitude(2446100.0, swe.VENUS)


@pytest.fixture
def ephemeris():
    value = os.environ.get('HD_SWISS_EPH')
    if not value:
        pytest.skip('Exact production-file test requires HD_SWISS_EPH')
    path = Path(value)
    for filename in ('sepl_18.se1', 'semo_18.se1'):
        assert (path / filename).is_file()
    scan.initialize(str(path))
    return path


def test_recorded_minute_and_neighbor_ties_are_preserved(ephemeris):
    target = datetime(1985, 1, 29, 10, 25, tzinfo=UTC)
    for offset in range(-7, 2):
        assert scan.first_failure(scan.datetime_to_jd(target + timedelta(minutes=offset))) == 6
    for offset in (-8, 2):
        assert scan.first_failure(scan.datetime_to_jd(target + timedelta(minutes=offset))) != 6
    competitor = datetime(2013, 1, 28, 8, 30, tzinfo=UTC)
    assert scan.first_failure(scan.datetime_to_jd(competitor)) != 6


def test_chunk_every_minute_once_including_endpoints(ephemeris):
    start = datetime(1985, 1, 29, 10, 0, tzinfo=UTC)
    a = scan.run_chunk(scan.datetime_to_jd(start), 0, 20)
    b = scan.run_chunk(scan.datetime_to_jd(start), 20, 61)
    assert a['count'] + b['count'] == 61
    assert sum(a['first_failure_counts_then_matches']) == 20
    assert sum(b['first_failure_counts_then_matches']) == 41
    assert a['hit_indices'] + b['hit_indices'] == list(range(18, 27))


def test_optimized_boolean_evaluator_matches_frozen_full_model(ephemeris):
    import json
    model = json.loads((scan.TASK / 'ASTROHD-V14-SIX-RULE-MODEL-20260925.json').read_text())
    result = scan.parity_audit(datetime(1926, 8, 24, 10, 42, tzinfo=UTC), 52596001, model, ephemeris)
    assert result['compared'] == 1211
    assert result['maximum_score_cases'] >= 9
    assert result['disagreements'] == 0


def test_julian_minute_arithmetic_does_not_change_classification(ephemeris):
    start = datetime(1926, 8, 24, 10, 42, tzinfo=UTC)
    jd = scan.datetime_to_jd(start)
    rng = random.Random(2514)
    for minute in [rng.randrange(52596001) for _ in range(128)]:
        canonical = scan.datetime_to_jd(start + timedelta(minutes=minute))
        arithmetic = jd + minute / 1440.0
        assert abs(canonical - arithmetic) <= 1e-9
        assert scan.first_failure(canonical) == scan.first_failure(arithmetic)
