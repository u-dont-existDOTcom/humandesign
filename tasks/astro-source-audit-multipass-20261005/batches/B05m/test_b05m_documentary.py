"""Original 1647 second-house source/attribution validation, not financial predictive tests."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class WealthSourceDocumentary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.rules = j("RULES.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.images = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.a = j("ACCEPTANCE.json")

    def test_01_primary_source_image_identity(self):
        for img in self.images["pages"].values():
            source = B / img["file"]
            self.assertEqual(h(source), img["sha256"])
            self.assertEqual(source.stat().st_size, img["bytes"])
            self.assertEqual(source.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_source_boundary_distinct_numbered_chapter(self):
        self.assertEqual(self.images["body_pdf_frames"], [586, 587])
        self.assertEqual(self.images["following_heading_pdf_frame"], 587)
        self.assertEqual(
            [p["printed_folio"] for p in self.images["pages"].values()],
            ["552", "553", "554"],
        )

    def test_03_record_ids_contiguous(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]],
            list(range(6809, 6854)),
        )

    def test_04_mapping_source_both_directions(self):
        all_ids = []
        for section, cross in zip(
            self.author["source_groups"], self.mapping["source_groups"], strict=True
        ):
            self.assertEqual(section["id"], cross["source_span"])
            self.assertEqual(section["original_pdf_pages"], cross["original_pdf_pages"])
            ids = [item["id"] for item in section["claims"]]
            self.assertEqual(ids, cross["mapped_records"])
            all_ids.extend(ids)
        self.assertEqual(all_ids, [r["id"] for r in self.rules["rules"]])
        self.assertEqual(len(set(all_ids)), 45)
        self.assertEqual(self.mapping["group_count"], 6)

    def test_05_original_cusp_interval_included_without_operator_invention(self):
        text = " ".join(r["original_anchor_not_diplomatic"] for r in self.rules["rules"])
        self.assertIn("five degrees before", text)
        self.assertIn("within five degrees", text)
        self.assertTrue(
            any(
                "before second cusp" in issue and "original inclusion language" in issue
                for issue in self.limits["issues"]
            )
        )

    def test_06_distinct_significator_sources(self):
        types = Counter(r["role"] for r in self.rules["rules"])
        for role in ("house_ruler", "intercepted_sign", "fortune_factor", "occupant"):
            self.assertGreater(types[role], 0)
        self.assertEqual(types["occupant_distance"], 1)

    def test_07_wealth_mechanisms_all_five_planets(self):
        roles = ("route_saturn", "route_jupiter", "route_mars", "route_venus", "route_mercury")
        text = " ".join(r["role"] for r in self.rules["rules"])
        for role in roles:
            self.assertEqual(text.split().count(role), 1)

    def test_08_ptolemy_and_leovitius_origanus_separate(self):
        text = " ".join(r["original_anchor_not_diplomatic"] for r in self.rules["rules"])
        for x in ("PTOLOMEY", "Leovitius", "Origanus", "lib. 4. cap. 1"):
            self.assertIn(x, text)
        self.assertTrue(
            all(not r["source_attribution_verified_against_ptolemy"] for r in self.rules["rules"])
        )

    def test_09_inheritance_requires_parent_conditions(self):
        types = Counter(r["role"] for r in self.rules["rules"])
        self.assertEqual(types["inheritance"], 2)
        self.assertGreaterEqual(types["inheritance_alternative"], 3)
        self.assertEqual(types["inheritance_result"], 1)
        self.assertTrue(any("unresolved" in issue.lower() for issue in self.limits["issues"]))

    def test_10_wealth_retention_and_loss_compete(self):
        types = Counter(r["role"] for r in self.rules["rules"])
        self.assertEqual(types["wealth_retention"], 2)
        self.assertEqual(types["estate_damage"], 2)
        self.assertEqual(types["wealth_timing"], 2)

    def test_11_timing_and_vocations_not_inheritance_only(self):
        text = " ".join(r["original_anchor_not_diplomatic"] for r in self.rules["rules"])
        self.assertIn("angles and succedant places", text)
        self.assertIn("Buildings", text)
        self.assertIn("Merchandizing", text)

    def test_12_navigation_after_substantive(self):
        self.assertEqual(
            [r["id"] for r in self.rules["rules"] if r["role"] == "next_chapter_navigation"],
            ["R6852", "R6853"],
        )
        self.assertEqual(self.rules["substantive_historical_records"], 43)
        self.assertEqual(self.a["next_pdf_frame"], 587)

    def test_13_original_diplomatic_not_claimed(self):
        self.assertFalse(self.rules["original_diplomatic_transcription_complete"])
        self.assertGreaterEqual(len(self.limits["issues"]), 12)

    def test_14_no_human_financial_forecast_successes(self):
        self.assertEqual(self.rules["independent_wealth_outcomes_validated"], 0)
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for row in self.rules["rules"]:
            self.assertFalse(row["independent_human_economic_prediction"])
            self.assertFalse(row["actual_inheritance_prediction_validated"])
            self.assertFalse(row["runtime_scoring_rule_promoted"])

    def test_15_rules_hash_and_batch_total(self):
        self.assertEqual(self.a["previous_lilly"], 6808)
        self.assertEqual(self.a["lilly_if_published"], 6853)
        self.assertEqual(self.a["combined_if_published"], 7919)
        self.assertEqual(h(B / "RULES.json"), self.a["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
