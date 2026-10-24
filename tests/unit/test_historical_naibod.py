"""Witness-exact Naibod numerical diagnostics and continuity regression.

The witness is a 2003 retypeset presentation of Lilly's Book III pp.713-715.
It is *not* assumed to be an authenticated original 1647 printing.
No astrology/event predictive validity claims, and no literal table fallback
is silently passed into the chronology engine.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.cli import main
from hdmatch.astrology.historical_naibod import (
    DEGREE_COMPONENTS,
    KNOWN_WITNESS_ISSUES,
    MINUTE_COMPONENTS,
    literal_naibod_lookup,
    source_issues,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.timeline import TimeKey, degrees_per_symbolic_year, generate_timeline

HERE = Path(__file__).resolve().parents[2]
EPHE = Path(
    os.getenv(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


def test_degree_table_known_cells_against_visual_pages() -> None:
    assert len(DEGREE_COMPONENTS) == 91
    expected = {
        0: (0, 0),
        1: (5, 8),
        2: (10, 17),
        11: (58, 21),
        19: (101, 17),
        30: (160, 14),
        31: (165, 23),
        60: (321, 4),
        68: (364, 0),
        69: (4, 3),
        80: (62, 24),
        90: (116, 13),
    }
    for idx, component in expected.items():
        assert DEGREE_COMPONENTS[idx] == component


def test_minute_table_known_cells_against_visual_pages() -> None:
    assert len(MINUTE_COMPONENTS) == 60  # includes 0 and 60; 27 absent
    expected = {
        0: (0, 0),
        1: (6, 4),
        7: (43, 6),
        8: (44, 10),
        9: (55, 14),
        26: (160, 14),
        28: (166, 18),
        29: (172, 23),
        30: (179, 3),
        31: (191, 11),
        44: (271, 8),
        52: (321, 4),
        55: (339, 17),
        59: (364, 10),
        60: (374, 14),
    }
    for idx, component in expected.items():
        assert MINUTE_COMPONENTS[idx] == component
    assert 27 not in MINUTE_COMPONENTS


def test_lilly_first_worked_example_exactly_reproduced() -> None:
    result = literal_naibod_lookup(11, 55)
    assert (
        result.literal_degree_years,
        result.literal_degree_days,
        result.literal_degree_hours,
    ) == (11, 58, 21)
    assert (result.literal_minute_days, result.literal_minute_hours) == (339, 17)
    assert (result.resulting_years, result.resulting_days, result.resulting_hours) == (12, 33, 14)
    assert result.warnings == ()
    assert result.to_dict()["not_continuous_key"] is True


def test_lilly_second_worked_example_internal_arithmetic_disagreement() -> None:
    result = literal_naibod_lookup(19, 52)
    assert (result.resulting_years, result.resulting_days, result.resulting_hours) == (20, 57, 21)
    assert any("22y57d21h" in msg for msg in result.warnings)
    # Source witness visibly prints "aged 22 yeers", despite its own steps
    # 19y+422d+21h -> 20y57d21h. It is not quietly corrected in the source.


def test_literal_degree_69_year_rollover_is_not_silently_repaired() -> None:
    prev = literal_naibod_lookup(68, 0)
    next_ = literal_naibod_lookup(69, 0)
    assert (prev.resulting_years, prev.resulting_days) == (68, 364)
    assert (next_.resulting_years, next_.resulting_days) == (69, 4)
    assert next_.resulting_years == 69  # not a silently reconstructed 70
    assert any("reset" in x for x in next_.warnings)


def test_raw_hour_24_and_unknown_minutes_27_are_preserved() -> None:
    raw = literal_naibod_lookup(80, 0)
    assert raw.literal_degree_hours == 24
    assert raw.resulting_hours == 0
    assert raw.resulting_days == 63
    assert any("HR=24" in w for w in raw.warnings)
    with pytest.raises(ValueError, match="missing: 27"):
        literal_naibod_lookup(20, 27)
    with pytest.raises(ValueError, match="D 0–90"):
        literal_naibod_lookup(19, 60)
    with pytest.raises(TypeError):
        literal_naibod_lookup(11.5, 55)
    with pytest.raises(TypeError):
        literal_naibod_lookup(True, 8)


def test_table_60_minutes_contradicts_one_degree_do_not_equate() -> None:
    day, hour = MINUTE_COMPONENTS[60]
    d1, h1 = DEGREE_COMPONENTS[1]
    # 1° equivalent, 365days/year: days should be 365+5=370, not 374.
    assert (day, hour) == (374, 14)
    assert (365 + d1, h1) == (370, 8)
    assert 24 * (day - (365 + d1)) + (hour - h1) == 102


def test_source_warnings_nonempty_and_specific() -> None:
    issues = source_issues()
    assert issues == KNOWN_WITNESS_ISSUES
    assert len(issues) >= 7
    assert len(literal_naibod_lookup(10, 8).warnings) > 0
    assert len(literal_naibod_lookup(10, 29).warnings) > 0
    assert len(literal_naibod_lookup(10, 44).warnings) > 0
    assert len(literal_naibod_lookup(10, 55).warnings) == 0


def test_time_keys_not_conflated() -> None:
    one = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR
    mean = TimeKey.MODERN_MEAN_SOLAR_DIAGNOSTIC
    printed = TimeKey.NAIBOD_59M08S_FIXED_DIAGNOSTIC
    rational = TimeKey.NAIBOD_EXACT_360_OVER_365_25_DIAGNOSTIC
    assert degrees_per_symbolic_year(one) == 1
    assert degrees_per_symbolic_year(printed) == pytest.approx((59 * 60 + 8) / 3600)
    assert degrees_per_symbolic_year(rational) == pytest.approx(360 / 365.25)
    assert degrees_per_symbolic_year(mean) == pytest.approx(360 / 365.2422)
    assert (
        0 < (degrees_per_symbolic_year(rational) - degrees_per_symbolic_year(printed)) * 3600 < 0.26
    )
    assert len({degrees_per_symbolic_year(k) for k in TimeKey}) == len(TimeKey)
    with pytest.raises(ValueError):
        degrees_per_symbolic_year("lilly_literal_table_1647_verified")


def test_75degree_arc_keys_late_ages_are_distinct() -> None:
    arc = 75
    y_lilly_reported = arc / degrees_per_symbolic_year(TimeKey.NAIBOD_59M08S_FIXED_DIAGNOSTIC)
    y_mean_exact = arc / degrees_per_symbolic_year(TimeKey.NAIBOD_EXACT_360_OVER_365_25_DIAGNOSTIC)
    assert y_mean_exact == pytest.approx(76.09375, abs=1e-11)
    assert y_lilly_reported == pytest.approx(76.09921082299887, abs=1e-10)
    assert (y_lilly_reported - y_mean_exact) * 365.25 > 1.99
    assert (y_lilly_reported - y_mean_exact) * 365.25 < 2.01


@pytest.mark.skipif(not EPHE.exists(), reason="official Swiss files unavailable")
def test_existing_timeline_unchanged_while_new_keys_are_selectable() -> None:
    sky = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    default = generate_timeline(sky).to_dict()
    old = json.loads(
        (
            HERE / "docs/astrology-research-map/gansten-primary-timeline-20261024/"
            "examples/synthetic_2000_timeline.json"
        ).read_text()
    )
    assert default == old
    for key in (
        TimeKey.NAIBOD_59M08S_FIXED_DIAGNOSTIC,
        TimeKey.NAIBOD_EXACT_360_OVER_365_25_DIAGNOSTIC,
    ):
        result = generate_timeline(sky, time_key=key).to_dict()
        assert result["technique_provenance"]["time_key"] == key.value
        assert result["astronomy_provenance"] == default["astronomy_provenance"]
        assert result["coverage"]["evaluated_method_pair_combinations"] == 168


@pytest.mark.skipif(not EPHE.exists(), reason="official Swiss files unavailable")
def test_cli_new_key_tagged_without_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "diagnostic.json"
    command = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        str(EPHE),
        "--key",
        "naibod_59m08s_fixed_diagnostic",
        "--method",
        "proportional_semi_arc",
        "--output",
        str(target),
    ]
    assert main(command) == 0
    record = json.loads(target.read_text())
    assert record["technique_provenance"]["time_key"] == command[command.index("--key") + 1]
    raw = target.read_bytes()
    with pytest.raises(SystemExit):
        main(command)
    assert target.read_bytes() == raw


@pytest.mark.skipif(not EPHE.exists(), reason="official Swiss ephemeris unavailable")
def test_all_existing_contact_families_support_new_keys_without_reinterpreting_geometry() -> None:
    from hdmatch.astrology.aspect_timeline import AspectProfile, generate_aspect_timeline
    from hdmatch.astrology.role_directions import (
        ContactConstruction,
        RotationRegime,
        generate_role_timeline,
    )

    sky = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    k = TimeKey.NAIBOD_EXACT_360_OVER_365_25_DIAGNOSTIC
    rays = generate_aspect_timeline(
        sky,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        time_key=k,
    ).to_dict()
    roles = generate_role_timeline(
        sky,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
        time_key=k,
    ).to_dict()
    assert rays["method_provenance"]["time_key"] == k.value
    assert roles["movement_provenance"]["time_key"] == k.value
    assert rays["coverage"]["evaluated"] == 1176
    assert roles["coverage"]["evaluated"] == 882
    assert all(record["time_key"] == k.value for record in rays["directions"])
    assert all(record["time_key"] == k.value for record in roles["directions"])
