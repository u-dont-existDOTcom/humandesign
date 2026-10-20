"""Offline replay of independent Iztro v2.6.0 312-chart source model parity.

The frozen corpus comprises synthetic lunar inputs, NOT actual human
participants. Source's leap convention remains original-as-next by default.
The alternative/current and half-month conventions are explicit scenarios,
not unconditional source corrections nor statistical/human validation.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
from quan_shu_fourteen_stars import fourteen_from_lunar_inputs  # noqa: E402
from ziwei_source_mechanics import STEMS  # noqa: E402

FROZEN = BASE / "batches/ChineseAstro-12/IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json"
SOURCE_STREAM_DIGEST = "37a5a7f18203b92a218a1b33adee36818928cfc2148558e083aa17793016ffdb"


class IztroExternalMechanicalParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(FROZEN.read_text(encoding="utf-8"))
        cls.rows = cls.report["all_312_case_records"]

    def test_01_all_312_vendor_output_rows_exact_digest(self):
        self.assertEqual(len(self.rows), 312)
        canon = json.dumps(self.rows, ensure_ascii=False,
                           sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertEqual(sha256(canon).hexdigest(), SOURCE_STREAM_DIGEST)
        self.assertEqual(self.report["sha256_full_312_joined_output"], SOURCE_STREAM_DIGEST)
        self.assertEqual(self.report["iztro_version"], "2.6.0")
        self.assertEqual(self.report["synthetic_cases"], 312)

    def test_02_stored_source_and_vendor_mismatches_not_rewritten(self):
        self.assertEqual(self.report["identical_14_star_and_life_body_bureau_cases"], 192)
        self.assertEqual(self.report["differing_cases"], 120)
        self.assertEqual(len(self.report["all_disagreements"]), 120)
        self.assertEqual(self.report["nonleap_cases"], 168)
        self.assertEqual(self.report["nonleap_identical"], 168)
        self.assertEqual(self.report["leap_cases"], 144)
        self.assertEqual(self.report["leap_fix_true_cases"], 72)
        self.assertEqual(self.report["leap_fix_true_identical"], 24)
        self.assertEqual(self.report["leap_fix_false_cases"], 72)
        self.assertEqual(self.report["leap_fix_false_identical"], 0)
        self.assertTrue(all(r["source_case"]["is_leap_month"]
                            for r in self.report["all_disagreements"]))
        self.assertEqual(Counter(field for r in self.report["all_disagreements"]
                                 for field in r["differing_fields"]),
                         {"life_palace": 120, "body_palace": 120,
                          "bureau_number": 60, "star_palaces": 60})
        self.assertTrue(all(len(r["iztro"]["star_palaces"]) == 14 for r in self.rows))

    def test_03_nonleap_168_all_identical_without_variant_rescue(self):
        cases = [r for r in self.rows if not r["source_case"]["is_leap_month"]]
        self.assertEqual(len(cases), 168)
        self.assertTrue(all(r["match"] for r in cases))
        self.assertTrue(all(not r["differing_fields"] for r in cases))

    def test_04_leap_policy_qualifications_are_expected_not_hidden(self):
        date_counts = Counter((r["source_case"]["gregorian_reference_date"],
                               r["source_case"]["fix_leap"], r["match"])
                              for r in self.rows if r["source_case"]["is_leap_month"])
        self.assertEqual(date_counts, {
            ("2023-03-22", False, False): 24, ("2023-03-22", True, False): 24,
            ("2023-04-19", False, False): 24, ("2023-04-19", True, True): 24,
            ("2025-07-25", False, False): 24, ("2025-07-25", True, False): 24,
        })

    def test_05_explicit_policy_alignment_replays_312_of_312_without_vendor_reinvocation(self):
        stats = Counter()
        for record in self.rows:
            src = record["source_case"]
            vendor = record["iztro"]
            # Original mode: every leap month is NEXT month.
            # Vendor fix_leap false: same month even for a leap.
            # Vendor fix_leap true: first 15 days SAME, day16+ NEXT.
            # This harmonization is a TRANSLATION OF RULESET, not a
            # statement that source original was wrong.
            as_next = (src["is_leap_month"] and src["fix_leap"]
                       and src["lunar_day"] > 15)
            year_stem = STEMS[(src["lunar_year"] - 1984) % 10]
            harmonized = fourteen_from_lunar_inputs(
                year_stem,
                src["lunar_month"],
                src["hour_branch"],
                src["lunar_day"],
                is_leap_month=as_next,
                documented_nayin_emendations=True,
                documented_diagram_corrections=True,
            )
            actual = {
                "life_palace": harmonized.partial_natal.life_palace,
                "body_palace": harmonized.partial_natal.body_palace,
                "bureau_number": harmonized.partial_natal.bureau.bureau_number,
                "star_palaces": harmonized.stars,
            }
            self.assertEqual(actual, vendor, f"Vendor and source-school-aligned rules differ: {record['id']}")
            stats["total"] += 1
            stats["leap" if src["is_leap_month"] else "nonleap"] += 1
            if not record["match"]:
                stats["original_disagreement_preserved"] += 1
        self.assertEqual(stats, Counter(
            {"total": 312, "nonleap": 168, "leap": 144,
             "original_disagreement_preserved": 120}
        ))
        self.assertEqual(self.report["differing_cases"], 120)

    def test_06_sex_legacy_source_does_not_affect_principal_star_positions(self):
        samples = {}
        for record in self.rows:
            id_ = record["id"]
            stem = id_.split("|")[0] + "|" + id_.split("|")[1] + "|" + id_.split("|")[3]
            samples.setdefault(stem, []).append(record["iztro"])
        self.assertEqual(len(samples), 156)
        for entries in samples.values():
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]["star_palaces"], entries[1]["star_palaces"])
            self.assertEqual(entries[0]["life_palace"], entries[1]["life_palace"])
            self.assertEqual(entries[0]["body_palace"], entries[1]["body_palace"])
            self.assertEqual(entries[0]["bureau_number"], entries[1]["bureau_number"])

    def test_07_no_human_prediction_claim_from_source_parity(self):
        self.assertFalse(self.report["independent_ancient_imprint_authenticated"])
        self.assertFalse(self.report["birthplace_local_to_calendar_date_verified"])
        self.assertEqual(self.report["preregistered_blinded_real_person_tests"], 0)
        self.assertEqual(self.report["runtime_astrological_forecast_promotions"], 0)
        self.assertIn("not a human", self.report["claim"])


if __name__ == "__main__":
    unittest.main()
