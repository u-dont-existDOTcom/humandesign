"""Focused data-integrity and source-bounded arithmetic checks, not accuracy tests."""

import hashlib
import json
from pathlib import Path
import re
import unittest

from lilly_dariot_reference import crisis_geometry, select_crisis_origin, timing_options

BATCH = Path(__file__).resolve().parent


class OriginTests(unittest.TestCase):
    def test_bed_time_precedes_available_physician_time(self):
        r = select_crisis_origin("known", "bed-hour supplied", "known", "physician-hour supplied")
        self.assertEqual((r["origin"], r["time"]), ("first_bed_hour", "bed-hour supplied"))

    def test_unavailable_bed_allows_physician_request(self):
        r = select_crisis_origin("unavailable", None, "known", "first request")
        self.assertEqual((r["status"], r["origin"], r["time"]),
                         ("selected", "first_physician_judgment_request", "first request"))

    def test_unknown_bed_does_not_authorize_fallback(self):
        r = select_crisis_origin("unknown", None, "known", "first request")
        self.assertEqual((r["status"], r["time"]), ("unresolved", None))

    def test_unavailable_and_unknown_fallback_remain_distinct(self):
        absent = select_crisis_origin("unavailable", None, "unavailable", None)
        unknown = select_crisis_origin("unavailable", None, "unknown", None)
        self.assertNotEqual(absent["reason"], unknown["reason"])
        self.assertIsNone(absent["origin"])
        self.assertIsNone(unknown["origin"])

    def test_inconsistent_time_evidence_is_rejected(self):
        for args in [("known", None, "unknown", None),
                     ("unknown", "invented", "unknown", None),
                     ("known", " ", "unknown", None),
                     ("absent", None, "known", "request")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                select_crisis_origin(*args)


class GeometryTests(unittest.TestCase):
    def test_targets_cross_zodiac_origin(self):
        r = crisis_geometry(350 * 3600 + 15 * 60, "acute", "selected")
        self.assertEqual(r["targets_arcsec"], (35 * 3600 + 15 * 60,
                                               80 * 3600 + 15 * 60,
                                               125 * 3600 + 15 * 60))
        self.assertIsNone(r["dates"])

    def test_targets_without_wrap(self):
        r = crisis_geometry(10 * 3600, "acute", "selected")
        self.assertEqual(r["targets_arcsec"], (55 * 3600, 100 * 3600, 145 * 3600))
        self.assertEqual(len(r["targets_arcsec"]), 3)

    def test_arcsecond_precision_at_last_longitude(self):
        r = crisis_geometry(360 * 3600 - 1, "acute", "selected")
        self.assertEqual(r["targets_arcsec"], (45 * 3600 - 1, 90 * 3600 - 1, 135 * 3600 - 1))

    def test_chronic_course_is_outside_this_rule(self):
        r = crisis_geometry(0, "chronic", "selected")
        self.assertEqual((r["status"], r["targets_arcsec"]), ("not_applicable", ()))

    def test_unknown_course_does_not_inherit_acute(self):
        r = crisis_geometry(0, "unknown", "selected")
        self.assertEqual((r["status"], r["targets_arcsec"]), ("unresolved", ()))

    def test_unknown_origin_does_not_emit_targets(self):
        self.assertEqual(crisis_geometry(0, "acute", "unresolved")["targets_arcsec"], ())

    def test_missing_longitude_is_not_zero(self):
        self.assertEqual(crisis_geometry(None, "acute", "selected")["status"], "unresolved")
        self.assertEqual(crisis_geometry(0, "acute", "selected")["status"], "angular_targets_only")

    def test_invalid_longitude_or_state_is_rejected(self):
        for args in [(-1, "acute", "selected"), (1296000, "acute", "selected"),
                     (True, "acute", "selected"), (0.0, "acute", "selected"),
                     (0, "unspecified", "selected"), (0, "acute", "missing")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                crisis_geometry(*args)


class TimingTests(unittest.TestCase):
    def test_conflicting_dimensions_do_not_select_a_unit(self):
        r = timing_options("common", "angular")
        self.assertEqual(r["sign_options"], ("weeks", "months"))
        self.assertEqual(r["house_options"], ("days",))
        self.assertIsNone(r["selected_unit"])
        self.assertIsNone(r["date"])
        self.assertTrue(r["prior_recovery_judgment_required"])

    def test_unknown_dimension_stays_missing(self):
        r = timing_options("unknown", "cadent")
        self.assertIsNone(r["sign_options"])
        self.assertEqual(r["house_options"], ("months", "years"))
        self.assertIsNone(r["selected_unit"])

    def test_unrecognized_categories_are_not_imputed(self):
        for args in [("mutable", "angular"), ("fixed", "eleventh"), (None, "cadent")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                timing_options(*args)


class SourceDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((BATCH / "RULES.json").read_text())
        cls.rules = cls.data["rules"]
        cls.ids = {r["id"] for r in cls.rules}

    def test_record_continuity_and_source_fields(self):
        before = json.loads((BATCH / "RETAINED_LILLY_INDEX_BEFORE.json").read_text())
        start = before["records_count"] + 1
        self.assertEqual(start, 1550)
        nums = [int(re.search(r"R(\d+)$", r["id"]).group(1)) for r in self.rules]
        self.assertEqual(nums, list(range(start, start + len(self.rules))))
        self.assertEqual(len(self.ids), len(self.rules))
        for r in self.rules:
            self.assertTrue(r["source_locator"]["passage_anchor"])
            self.assertEqual(r["source_locator"]["source_sha256"],
                             "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
            self.assertTrue(r["source_statement"])
            self.assertFalse(r["independent_evidence_unit"])

    def test_full_declared_span_and_section_links(self):
        coverage = json.loads((BATCH / "SECTION_COVERAGE.json").read_text())
        self.assertEqual(coverage["admitted_pdf_pages"], list(range(292, 303)))
        covered = [n for s in coverage["sections"] for n in s["record_ids"]]
        self.assertEqual(set(covered), self.ids)
        self.assertEqual(len(covered), len(self.ids))
        pages = {p for r in self.rules for p in r["source_locator"]["pdf_pages"]}
        self.assertEqual(pages, set(range(292, 303)))

    def test_retained_index_and_unfinished_boundary(self):
        before = json.loads((BATCH / "RETAINED_LILLY_INDEX_BEFORE.json").read_text())
        after = json.loads((BATCH / "LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json").read_text())
        self.assertEqual(after["batches"][:-1], before["batches"])
        self.assertEqual(after["records_count"], before["records_count"] + len(self.rules))
        self.assertEqual(after["read_numbered_chapters"], before["read_numbered_chapters"])
        self.assertEqual(after["next"]["pdf_page"], 302)
        self.assertFalse(after["next"]["extracted"])
        self.assertEqual(after["runtime_promotions"], 0)
        self.assertEqual(after["empirical_validations"], 0)
        raw = (BATCH / "RULES.json").read_bytes()
        self.assertEqual(after["batches"][-1]["sha256"], hashlib.sha256(raw).hexdigest())

    def test_issue_and_reference_link_integrity(self):
        issues = json.loads((BATCH / "UNRESOLVED.json").read_text())["items"]
        issue_ids = {x["id"] for x in issues}
        self.assertEqual(len(issue_ids), len(issues))
        for issue in issues:
            self.assertTrue(set(issue["record_ids"]) <= self.ids)
        for rule in self.rules:
            self.assertTrue(set(rule["unresolved_ids"]) <= issue_ids)
        references = json.loads((BATCH / "REFERENCE_TABLES.json").read_text())
        for item in references["items"]:
            self.assertTrue(item["record_ids"])
            self.assertTrue(set(item["record_ids"]) <= self.ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
