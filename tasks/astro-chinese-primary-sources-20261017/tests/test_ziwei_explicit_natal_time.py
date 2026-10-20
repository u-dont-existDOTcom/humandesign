"""Modern timezone/DST/lunar-day-policy bridge, strictly synthetic timestamps.

These are calendar and source-mechanics tests only, not real people's natal
charts or validation of astrology's prospective predictive success.
"""

import hashlib
import json
import sys
import unittest
from pathlib import Path
from zoneinfo import TZPATH

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
import explicit_natal_time as t  # noqa: E402
from dual_witness_civil_lunar import CalendarParityError  # noqa: E402

LOCAL = "birth_site_civil_date_hko_lookup"
HK = "same_instant_fixed_utc_plus_8_calendar_day"
CIVIL = "recorded_local_civil_clock"
MEAN = "local_mean_solar_longitude"
MIDNIGHT = "midnight_day_boundary"

COMMON = dict(
    fold=None,
    calendar_day_policy=HK,
    hour_time_policy=CIVIL,
    longitude_east_degrees=None,
    late_zi_day_policy=MIDNIGHT,
    recorded_clock_uncertainty_seconds=0,
)


def resolve(clock="2026-02-16T21:30:00", zone="Africa/Dakar", **changes):
    opts = dict(COMMON)
    opts.update(changes)
    return t.resolve_explicit_local_birth_clock(clock, zone, **opts)


def make_chart(clock="2026-02-16T21:30:00", zone="Africa/Dakar", **changes):
    opts = dict(COMMON)
    opts.update({
        "lunar_year_boundary_policy": t.BIRTH_CALENDAR_BOUNDARY,
        "leap_month_policy": "transmitted_quan_shu_as_next",
        "documented_nayin_emendations": True,
        "documented_diagram_corrections": True,
    })
    opts.update(changes)
    return t.fourteen_stars_from_explicit_civil_birth(clock, zone, **opts)


class SyntheticTimezoneAndMeanSolar(unittest.TestCase):
    def test_01_same_instant_hk_vs_birthplace_day_end_of_2025_lunar_year(self):
        hk = resolve()
        native = resolve(calendar_day_policy=LOCAL)
        self.assertEqual(hk.birth_utc_instant, "2026-02-16T21:30:00+00:00")
        self.assertEqual(hk.birthplace_civil_calendar_day, "2026-02-16")
        self.assertEqual(hk.same_instant_fixed_utc_plus_8_calendar_day, "2026-02-17")
        self.assertEqual(hk.standard_utc_plus_8_calendar_clock, "2026-02-17T05:30:00+08:00")
        self.assertEqual(hk.selected_chinese_calendar_day, "2026-02-17")
        self.assertEqual(native.selected_chinese_calendar_day, "2026-02-16")
        self.assertEqual(hk.recorded_civil_hour_branch, "Hai")
        self.assertEqual(hk.selected_hour_branch, "Hai")
        self.assertEqual(hk.utc_offset_seconds, 0)
        self.assertIsNone(hk.mean_solar_local_clock)

    def test_02_us_new_york_to_hk_reference_day_crosses_date(self):
        r = resolve("2026-02-17T17:30:00", "America/New_York")
        self.assertEqual(r.birth_utc_instant, "2026-02-17T22:30:00+00:00")
        self.assertEqual(r.same_instant_fixed_utc_plus_8_calendar_day, "2026-02-18")
        self.assertEqual(r.birthplace_civil_calendar_day, "2026-02-17")
        self.assertEqual(r.recorded_civil_hour_branch, "You")
        self.assertEqual(r.utc_offset_seconds, -18000)
        self.assertEqual(r.fold, 0)

    def test_03_dst_local_time_gap_must_fail_instead_of_guessing(self):
        for f in (None, 0, 1):
            with self.assertRaisesRegex(t.NatalTimeResolutionError, "Nonexistent"):
                resolve("2026-03-08T02:30:00", "America/New_York", fold=f)

    def test_04_autumn_dst_fold_must_be_explicit_and_resolves_two_utc_instants(self):
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "Ambiguous"):
            resolve("2026-11-01T01:30:00", "America/New_York")
        early = resolve("2026-11-01T01:30:00", "America/New_York", fold=0)
        late = resolve("2026-11-01T01:30:00", "America/New_York", fold=1)
        self.assertEqual(early.birth_utc_instant, "2026-11-01T05:30:00+00:00")
        self.assertEqual(late.birth_utc_instant, "2026-11-01T06:30:00+00:00")
        self.assertEqual((early.utc_offset_seconds,late.utc_offset_seconds), (-14400,-18000))
        self.assertEqual((early.fold,late.fold), (0,1))

    def test_05_fold_one_rejected_for_nonambiguous_clock(self):
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "fold=1 invalid"):
            resolve(fold=1)

    def test_06_pacific_apia_entire_missing_december_30_2011(self):
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "Nonexistent"):
            resolve("2011-12-30T12:00:00", "Pacific/Apia")

    def test_07_local_mean_solar_new_york_daylight_saving_can_shift_hour_branch(self):
        civil = resolve("2026-07-01T13:30:00", "America/New_York",
                        longitude_east_degrees="-74")
        solar = resolve("2026-07-01T13:30:00", "America/New_York",
                        longitude_east_degrees="-74", hour_time_policy=MEAN)
        self.assertEqual(civil.utc_offset_seconds, -14400)
        self.assertEqual(civil.birth_utc_instant, "2026-07-01T17:30:00+00:00")
        self.assertEqual(civil.recorded_civil_hour_branch, "Wei")
        self.assertEqual(solar.mean_solar_local_clock, "2026-07-01T12:34:00.000000")
        self.assertEqual(solar.mean_solar_hour_branch, "Wu")
        self.assertEqual(solar.selected_hour_branch, "Wu")
        self.assertEqual(civil.selected_hour_branch, "Wei")
        self.assertEqual(civil.selected_chinese_calendar_day, solar.selected_chinese_calendar_day)

    def test_08_dakar_local_mean_hour_from_longitude_not_dst_offset(self):
        civil = resolve(longitude_east_degrees="-17.4")
        solar = resolve(longitude_east_degrees="-17.4", hour_time_policy=MEAN)
        self.assertEqual(civil.selected_hour_branch, "Hai")
        self.assertEqual(solar.mean_solar_local_clock, "2026-02-16T20:20:24.000000")
        self.assertEqual(solar.selected_hour_branch, "Xu")
        self.assertEqual(solar.utc_offset_seconds, 0)

    def test_09_historic_hong_kong_dst_is_not_official_fixed_utc8_day(self):
        # HKO lists summer time in Hong Kong 1965-04-18..1965-10-17.
        # HK civil clock +09 and fixed +08 standard reference can differ
        # in date for 00:00-00:59. Source-calendar policy must not
        # silently use IANA Asia/Hong_Kong daylight time as if UTC+8.
        fixed = resolve("1965-07-01T00:30:00", "Asia/Hong_Kong")
        actual_civil = resolve(
            "1965-07-01T00:30:00", "Asia/Hong_Kong", calendar_day_policy=LOCAL
        )
        self.assertEqual(fixed.birth_utc_instant, "1965-06-30T15:30:00+00:00")
        self.assertEqual(fixed.utc_offset_seconds, 32400)
        self.assertEqual(fixed.birthplace_civil_calendar_day, "1965-07-01")
        self.assertEqual(fixed.same_instant_fixed_utc_plus_8_calendar_day, "1965-06-30")
        self.assertEqual(fixed.standard_utc_plus_8_calendar_clock, "1965-06-30T23:30:00+08:00")
        self.assertEqual(fixed.selected_chinese_calendar_day, "1965-06-30")
        self.assertEqual(actual_civil.selected_chinese_calendar_day, "1965-07-01")

    def test_09_timezone_tzif_binary_provenance(self):
        r = resolve("2026-02-17T10:00:00", "America/New_York")
        self.assertEqual(r.birth_iana_timezone, "America/New_York")
        candidates = [Path(root) / "America/New_York" for root in TZPATH]
        present = next((path for path in candidates if path.is_file()), None)
        if present is None:
            self.assertIsNone(r.tzif_sha256)
        else:
            self.assertEqual(len(r.tzif_sha256), 64)
            self.assertEqual(
                r.tzif_sha256, hashlib.sha256(present.read_bytes()).hexdigest()
            )

    def test_10_immutable_separate_node_intl_time_engine_witness(self):
        report = json.loads((BASE / "batches/ChineseAstro-13/"
            "NODE_INTL_PYTHON_ZONEINFO_12_SYNTHETIC_PARITY_V1.json").read_text())
        self.assertEqual((report["sample_count"],
                          report["identical_civil_dates_and_hours"],
                          report["disagreement_count"]), (12, 12, 0))
        self.assertEqual(report["sample_rows_sha256_canonical"],
                         "861970c4035adc4314da88ddd6e72294e817706b288e3f5f324d1b54cc4a9173")
        canon = json.dumps(report["cases"], ensure_ascii=False,
                           sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertEqual(hashlib.sha256(canon).hexdigest(),
                         report["sample_rows_sha256_canonical"])
        self.assertTrue(all(x["agree"] for x in report["cases"]))
        self.assertEqual({x["id"] for x in report["cases"] if
                          x["python_zoneinfo_fold"] == 1},
                         {"ny-2026-autumn-fold1"})

    def test_10_require_full_unambiguous_date_and_year_range(self):
        for bad in ("2026-2-17T10:00:00","2026-02-17 10:00:00",
                    "2026-02-17T10:00:00+00:00","2026-02-30T10:00:00",
                    "1800-02-17T10:00:00","2101-02-17T10:00:00"):
            with self.assertRaises(t.NatalTimeResolutionError):
                resolve(bad)

    def test_11_invalid_timezone_and_longitude_rejected(self):
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "IANA"):
            resolve(zone="Europe/ThisCityDoesNotExist")
        for invalid in (True, float("nan"), float("inf"), 181, -180.01, "hi"):
            with self.assertRaisesRegex(t.NatalTimeResolutionError, "Longitude"):
                resolve(longitude_east_degrees=invalid)
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "longitude"):
            resolve(hour_time_policy=MEAN)

    def test_12_policies_are_mandatory_and_unimplemented_apparent_solar_fails(self):
        for invalid in ("apparent_solar", "automatic", None):
            with self.assertRaisesRegex(
                t.NatalTimeResolutionError, "civil-clock or local-mean-solar"
            ):
                resolve(hour_time_policy=invalid)
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "Explicit fixed UTC"):
            resolve(calendar_day_policy="automatic")
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "23:00 Zi-day"):
            resolve(late_zi_day_policy="zi_day_starts_23")
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "interval propagation"):
            resolve(recorded_clock_uncertainty_seconds=120)
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "interval propagation"):
            resolve(recorded_clock_uncertainty_seconds=-1)

    def test_13_hour_cycle_explicit_23_and_after_midnight(self):
        self.assertEqual([t._branch_for_hour(h) for h in range(24)], [
            "Zi","Chou","Chou","Yin","Yin","Mao","Mao","Chen",
            "Chen","Si","Si","Wu","Wu","Wei","Wei","Shen",
            "Shen","You","You","Xu","Xu","Hai","Hai","Zi"
        ])
        with self.assertRaises(t.NatalTimeResolutionError):
            t._branch_for_hour(True)
        with self.assertRaises(t.NatalTimeResolutionError):
            t._branch_for_hour(24)

    def test_14_west_longitude_and_hk_east_longitude_mean_solar_are_not_apparent(self):
        ny = resolve("2026-07-01T13:30:00", "America/New_York",
                     longitude_east_degrees=-74, hour_time_policy=MEAN)
        hk = resolve("2026-07-01T13:30:00", "Asia/Hong_Kong",
                     longitude_east_degrees="114.174333333", hour_time_policy=MEAN)
        self.assertNotEqual(ny.birth_utc_instant, hk.birth_utc_instant)
        self.assertEqual(ny.mean_solar_hour_branch, "Wu")
        self.assertEqual(hk.utc_offset_seconds, 28800)
        self.assertNotEqual(hk.mean_solar_local_clock, "2026-07-01T13:30:00.000000")

    def test_15_model_flags_do_not_claim_genuine_birth_chart_or_forecast(self):
        self.assertFalse(t.ENGINE_SCOPE["astronomical_apparent_solar_equation_of_time"])
        self.assertFalse(t.ENGINE_SCOPE["late_zi_23_day_start_supported"])
        self.assertFalse(t.ENGINE_SCOPE["nonzero_birth_clock_uncertainty_propagation"])
        self.assertFalse(t.ENGINE_SCOPE["full_classical_historic_calendar_parity"])
        self.assertEqual(t.ENGINE_SCOPE["independent_blinded_predictive_human_tests"], 0)


class SyntheticFourteenStarTimeIntegration(unittest.TestCase):
    def test_16_hk_vs_birth_site_gregorian_day_produces_distinct_cny_year(self):
        hk = make_chart()
        local = make_chart(calendar_day_policy=LOCAL)
        self.assertEqual(hk.official_chinese_lunar_date.sexagenary_year, "丙午")
        self.assertEqual(local.official_chinese_lunar_date.sexagenary_year, "乙巳")
        self.assertEqual((hk.official_chinese_lunar_date.month, hk.official_chinese_lunar_date.day),
                         (1,1))
        self.assertEqual(
            (local.official_chinese_lunar_date.month, local.official_chinese_lunar_date.day),
            (12,29),
        )
        self.assertNotEqual(hk.principal_stars.stars, local.principal_stars.stars)
        self.assertEqual(len(hk.principal_stars.stars), 14)
        self.assertEqual(len(local.principal_stars.stars), 14)

    def test_17_recorded_clock_vs_local_mean_solar_alters_chart_hour(self):
        kw=dict(longitude_east_degrees="-74")
        civil=make_chart("2026-07-01T13:30:00", "America/New_York", **kw)
        solar=make_chart("2026-07-01T13:30:00", "America/New_York",
                         hour_time_policy=MEAN, **kw)
        self.assertEqual(civil.official_chinese_lunar_date, solar.official_chinese_lunar_date)
        self.assertNotEqual(civil.clock.selected_hour_branch, solar.clock.selected_hour_branch)
        self.assertNotEqual(civil.principal_stars.partial_natal.life_palace,
                            solar.principal_stars.partial_natal.life_palace)

    def test_18_source_leap_always_next_differs_from_modern_first_half(self):
        original=make_chart("2023-03-22T12:00:00", "Asia/Hong_Kong")
        modern=make_chart("2023-03-22T12:00:00", "Asia/Hong_Kong",
                          leap_month_policy="modern_leap_first_15_same_else_next")
        self.assertTrue(original.official_chinese_lunar_date.is_leap_month)
        self.assertEqual(original.official_chinese_lunar_date.day, 1)
        self.assertNotEqual(original.principal_stars.partial_natal.life_palace,
                            modern.principal_stars.partial_natal.life_palace)
        self.assertEqual(len(original.principal_stars.stars),14)
        self.assertEqual(len(modern.principal_stars.stars),14)

    def test_19_last_half_leap_modern_matches_source_next(self):
        original=make_chart("2023-04-19T12:00:00","Asia/Hong_Kong")
        modern=make_chart("2023-04-19T12:00:00","Asia/Hong_Kong",
                          leap_month_policy="modern_leap_first_15_same_else_next")
        self.assertEqual(original.official_chinese_lunar_date.day,29)
        self.assertEqual(original.principal_stars.stars,modern.principal_stars.stars)
        self.assertEqual(original.principal_stars.partial_natal.life_palace,
                         modern.principal_stars.partial_natal.life_palace)

    def test_20_conflicted_2057_software_date_fails_closed(self):
        with self.assertRaisesRegex(CalendarParityError, "disagree"):
            make_chart("2057-09-28T12:00:00","Asia/Hong_Kong")

    def test_22_1965_hong_kong_summer_birth_has_two_different_calendar_day_charts(self):
        standard=make_chart("1965-07-01T00:30:00","Asia/Hong_Kong")
        civil=make_chart("1965-07-01T00:30:00","Asia/Hong_Kong",
                         calendar_day_policy=LOCAL)
        self.assertEqual(standard.clock.utc_offset_seconds,32400)
        self.assertEqual(standard.clock.selected_chinese_calendar_day,"1965-06-30")
        self.assertEqual(civil.clock.selected_chinese_calendar_day,"1965-07-01")
        self.assertNotEqual(standard.official_chinese_lunar_date.day,
                            civil.official_chinese_lunar_date.day)
        self.assertNotEqual(standard.principal_stars.stars,civil.principal_stars.stars)

    def test_21_li_chun_year_and_unsupported_leap_policy_fail_closed(self):
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "Li Chun"):
            make_chart(lunar_year_boundary_policy="li_chun")
        with self.assertRaisesRegex(t.NatalTimeResolutionError, "Leap month method"):
            make_chart(leap_month_policy="guess_automatically")


if __name__=="__main__":
    unittest.main()
