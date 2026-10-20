"""Read official HKO frozen UTF-8 JSON and compare optional independent software.

Historical astrology predictions are NOT tested here; calendar truth and
Chinese-year policy are prerequisite mechanics only.
"""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
import dual_witness_civil_lunar as c  # noqa: E402

LIBS_PRESENT = all(importlib.util.find_spec(x) is not None for x in ("lunar_python", "sxtwl"))


class OfficialCalendarFixtures(unittest.TestCase):
    def test_01_hko_all_ten_sha_pinned_records_replay_offline(self):
        blob = json.loads(c.HKO_WITNESS.read_text())
        self.assertEqual(len(blob["samples"]), 10)
        self.assertEqual(len({x["gregorian_date"] for x in blob["samples"]}), 10)
        self.assertEqual({x["gregorian_date"] for x in blob["samples"]},
                         {"2023-03-21", "2023-03-22", "2023-04-19", "2023-04-20",
                          "2025-07-25", "2026-02-16", "2026-02-17", "2026-10-20",
                          "2027-02-06", "2028-01-01"})
        for x in blob["samples"]:
            lunar = c.frozen_hko_example(x["gregorian_date"])
            self.assertEqual(lunar.source, "hko_original_json")
            self.assertEqual(lunar.year_method, c.LUNAR_NEW_YEAR_POLICY)

    def test_02_precise_two_2023_leap_month_borders(self):
        a = c.frozen_hko_example("2023-03-21")
        b = c.frozen_hko_example("2023-03-22")
        d = c.frozen_hko_example("2023-04-19")
        e = c.frozen_hko_example("2023-04-20")
        self.assertEqual((a.year, a.month, a.day, a.is_leap_month),
                         (2023, 2, 30, False))
        self.assertEqual((b.year, b.month, b.day, b.is_leap_month),
                         (2023, 2, 1, True))
        self.assertEqual((d.year, d.month, d.day, d.is_leap_month),
                         (2023, 2, 29, True))
        self.assertEqual((e.year, e.month, e.day, e.is_leap_month),
                         (2023, 3, 1, False))
        f = c.frozen_hko_example("2025-07-25")
        self.assertEqual((f.year, f.month, f.day, f.is_leap_month),
                         (2025, 6, 1, True))

    def test_03_new_year_2026_not_same_day_as_li_chun(self):
        before = c.frozen_hko_example("2026-02-16")
        after = c.frozen_hko_example("2026-02-17")
        self.assertEqual((before.year, before.month, before.day), (2025, 12, 29))
        self.assertEqual(before.sexagenary_year, "乙巳")
        self.assertEqual(before.year_heavenly_stem, "Yi")
        self.assertEqual((after.year, after.month, after.day), (2026, 1, 1))
        self.assertEqual(after.sexagenary_year, "丙午")
        self.assertEqual(after.year_heavenly_stem, "Bing")
        original = json.loads(c.HKO_WITNESS.read_text())
        feb16 = next(x for x in original["samples"] if x["gregorian_date"] == "2026-02-16")
        self.assertEqual(feb16["lunar_python"]["li_chun_day_ganzhi"], "丙午")
        self.assertEqual(feb16["lunar_python"]["official_lunar_year_ganzhi"], "乙巳")

    def test_04_official_2026_october_and_2027_2028_new_year(self):
        oct20 = c.frozen_hko_example("2026-10-20")
        self.assertEqual((oct20.year, oct20.month, oct20.day), (2026, 9, 11))
        feb6 = c.frozen_hko_example("2027-02-06")
        self.assertEqual((feb6.year, feb6.month, feb6.day), (2027, 1, 1))
        jan1 = c.frozen_hko_example("2028-01-01")
        self.assertEqual((jan1.year, jan1.month, jan1.day), (2027, 12, 5))

    def test_05_chinese_day_and_leap_notation_fails_closed(self):
        self.assertEqual(c._day_chinese("初一"), 1)
        self.assertEqual(c._day_chinese("初十"), 10)
        self.assertEqual(c._day_chinese("十一"), 11)
        self.assertEqual(c._day_chinese("二十"), 20)
        self.assertEqual(c._day_chinese("廿九"), 29)
        self.assertEqual(c._day_chinese("三十"), 30)
        self.assertEqual(c._month_chinese("閏二"), (2, True))
        self.assertEqual(c._month_chinese("正"), (1, False))
        for s in ("初十一", "十五五", "四十", "○", "廿十"):
            with self.assertRaises(c.CalendarParityError):
                c._day_chinese(s)
        with self.assertRaises(c.CalendarParityError):
            c._month_chinese("萬")

    def test_06_hko_response_shape_and_year_cycle_fail_closed(self):
        with self.assertRaises(c.CalendarParityError):
            c.parse_official_hko_json("2026-02-17", {"LunarDate": "正月初一"})
        with self.assertRaises(c.CalendarParityError):
            c.parse_official_hko_json("2026-02-17",
                                      {"LunarYear": "壬子年，鼠", "LunarDate": "正月初一"})

    def test_07_immutable_frozen_bytes_hash_guard(self):
        source = c.HKO_EVIDENCE_DIR / "hko_2026-02-17.json"
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, source.name).write_bytes(source.read_bytes() + b" ")
            with patch.object(c, "HKO_EVIDENCE_DIR", Path(tmp)):
                with self.assertRaisesRegex(c.CalendarParityError, "bytes changed"):
                    c.frozen_hko_example("2026-02-17")

    def test_08_missing_frozen_example_cannot_be_invented(self):
        with self.assertRaisesRegex(c.CalendarParityError, "No source-locked"):
            c.frozen_hko_example("2026-02-18")

    def test_09_calendar_date_input_limited_and_canonicalized(self):
        for day in ("1600-01-01", "2101-01-01", "2026-2-17", "2026-02-30"):
            with self.assertRaises((ValueError, c.CalendarParityError)):
                c._ymd(day)

    def test_10_no_implicit_year_policy_or_geography(self):
        self.assertFalse(c.ENGINE_SCOPE["li_chun_annual_boundary_implemented"])
        self.assertFalse(c.ENGINE_SCOPE["local_birth_time_to_reference_city_date_implemented"])
        self.assertTrue(c.ENGINE_SCOPE["calendar_reference_zone_explicitly_required"])
        self.assertEqual(c.ENGINE_SCOPE["blinded_human_predictions"], 0)
        with self.assertRaisesRegex(c.CalendarParityError, "Asia/Hong_Kong"):
            c.fourteen_from_reference_calendar_day(
                "2026-02-17", "Zi",
                calendar_reference="user-birthplace",
                year_boundary=c.LUNAR_NEW_YEAR_POLICY)
        with self.assertRaisesRegex(c.CalendarParityError, "Only official"):
            c.fourteen_from_reference_calendar_day(
                "2026-02-17", "Zi",
                calendar_reference=c.REFERENCE_ZONE_ONLY, year_boundary="li_chun")

    def test_11_missing_optional_backend_does_not_fall_back_to_6tail(self):
        with patch.object(c, "REQUIRED_LIBRARY_VERSIONS", {"missing_cal_backend_12345678": "1"}):
            with self.assertRaisesRegex(c.CalendarParityError, "not installed"):
                c.dual_library_reference_date("2026-02-17")


@unittest.skipUnless(LIBS_PRESENT, "Optional dual calendar libraries unavailable: only source-fixture tests run")
class DualExternalSoftwareChecks(unittest.TestCase):
    def test_12_all_ten_official_source_days_match_live_separate_engines(self):
        entries = json.loads(c.HKO_WITNESS.read_text())["samples"]
        for r in entries:
            actual = c.dual_library_reference_date(r["gregorian_date"])
            official = c.frozen_hko_example(r["gregorian_date"])
            self.assertEqual((actual.year, actual.month, actual.day, actual.is_leap_month),
                             (official.year, official.month, official.day, official.is_leap_month))

    def test_13_2036_solar_term_boundary_is_not_lunar_year(self):
        from lunar_python import Solar
        pre_spring = Solar.fromYmd(2036, 1, 28).getLunar()
        self.assertEqual((pre_spring.getYear(), pre_spring.getMonth(), pre_spring.getDay()),
                         (2036, 1, 1))
        self.assertEqual(pre_spring.getYearInGanZhi(), "丙辰")
        self.assertEqual(pre_spring.getYearInGanZhiByLiChun(), "乙卯")
        later = Solar.fromYmdHms(2036, 2, 4, 0, 0, 0).getLunar()
        self.assertNotEqual(later.getYearInGanZhiExact(), later.getYearInGanZhiByLiChun())
        self.assertEqual((c.dual_library_reference_date("2036-01-28").year,
                          c.dual_library_reference_date("2036-02-04").year), (2036, 2036))

    def test_14_explicit_calendar_reference_day_can_feed_14_major_star_layer(self):
        layout = c.fourteen_from_reference_calendar_day(
            "2026-02-17", "Zi",
            calendar_reference=c.REFERENCE_ZONE_ONLY,
            year_boundary=c.LUNAR_NEW_YEAR_POLICY,
            documented_nayin_emendations=True,
            documented_diagram_corrections=True,
        )
        self.assertEqual(len(layout.stars), 14)
        self.assertEqual(len(layout.placements_by_palace), 12)
        self.assertEqual(sum(map(len, layout.placements_by_palace.values())), 14)
        self.assertEqual(layout.partial_natal.life_palace, "Yin")

    def test_15_dependency_version_mismatch_fails_closed(self):
        with patch.object(c, "REQUIRED_LIBRARY_VERSIONS",
                          {"lunar_python": "0.0.0", "sxtwl": "2.0.7"}):
            with self.assertRaisesRegex(c.CalendarParityError, "Unexpected lunar_python version"):
                c.dual_library_reference_date("2026-02-17")

    def test_16_2057_new_moon_calendar_oracles_disagree_and_stop(self):
        # HKO publicly flags near-midnight new moon 2057-09-28 as fragile.
        # Neither software engine is silently promoted to authority.
        with self.assertRaisesRegex(c.CalendarParityError, "disagree"):
            c.dual_library_reference_date("2057-09-28")


if __name__ == "__main__":
    unittest.main()
