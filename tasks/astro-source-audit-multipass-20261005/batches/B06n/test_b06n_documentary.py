"""Original source documentary tests; absolutely not a natal mortality predictor."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class FirstEditionSpouseMortalityHistoricalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_photo_crc_jpegs_sha256_bytes(self):
        self.assertEqual(list(self.w["images"]), ["633", "634"])
        for x in self.w["images"].values():
            data = (B / x["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), x["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), x["sha256"])

    def test_02_original_folios_and_next_chapter(self):
        self.assertEqual(self.w["body_pdf_frames"], [633, 634])
        self.assertEqual(self.w["following_printed_CXXXVII_heading_pdf"], 634)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["599", "600"],
        )

    def test_03_exact_append_only_54_source_records(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(8344, 8398)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 54)

    def test_04_source_six_reversible_original_groups(self):
        ids = []
        for s, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(s["source_span"], m["source_span"])
            self.assertEqual(s["original_pdf_frames"], m["original_pdf_frames"])
            r = [x["id"] for x in s["clauses"]]
            self.assertEqual(r, m["mapped_record_ids"])
            ids.extend(r)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 6)

    def test_05_important_second_house_exception_cadent_anomaly(self):
        for key in ("cadent_condition", "second_exception", "wife_significators"):
            self.assertEqual(self.roles[key], 1)
        self.assertIn("second opposite eighth", self.text)

    def test_06_death_or_chronic_disease_are_two_alternate_outcomes(self):
        self.assertEqual(self.roles["wife_death_or_disease"], 1)

    def test_07_moon_exactly_one_planet_strength_reverse_branches(self):
        for key in (
            "moon_one_companion",
            "moon_more_fortified",
            "wife_first",
            "other_more_fortified",
            "husband_first",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_08_moon_separates_mars_applies_venus_occidental(self):
        for key in (
            "moon_separated_mars",
            "moon_applies_venus",
            "western_position",
            "many_wives",
            "all_wives_before",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_09_moon_venus_saturn_seventh_historic_alternative(self):
        for key in (
            "moon_venus_saturn",
            "saturn_seventh",
            "wife_deaths_saturn",
            "difficulty_spouse",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_10_venus_fourth_two_malefics_sign_modifier(self):
        for key in (
            "venus_fourth",
            "venus_mars_saturn_hard",
            "venus_mobile",
            "multiple_wives_mobile",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_11_moon_seventh_no_jupiter_or_venus_help_exception(self):
        for key in (
            "moon_seventh",
            "moon_malefic_hard",
            "without_jupiter",
            "without_venus",
            "wife_death_only_unassisted",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_12_venus_occidental_peregrine_malefic_contact(self):
        for key in (
            "venus_occidental",
            "venus_peregrine",
            "venus_conj_malefics",
            "venus_square_opposition",
            "short_spouse_life",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_13_mistreatment_stereotype_not_death_predicate(self):
        for key in ("venus_mars_twelfth", "native_knave", "use_wife_basely"):
            self.assertEqual(self.roles[key], 1)
        self.assertFalse(self.l["real_person_lifespan_danger_or_illness_predictions_authorized"])

    def test_14_seventh_malefics_and_house_lord_alternatives(self):
        for key in (
            "malefic_seventh_or_fourth",
            "malefics_peregrine_seventh",
            "malefics_dominion",
            "seventh_lord_combust",
            "seventh_lord_cadent",
            "seventh_lord_eighth",
        ):
            self.assertEqual(self.roles[key], 1)

    def test_15_females_marriage_next_chapter_not_accepted_here(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R8396", "R8397"],
        )
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXVII")
        self.assertEqual(self.r["substantive"], 52)

    def test_16_zero_empirical_spousal_survival_or_medical_advice(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["real_mortality_accuracy_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_spousal_mortality_accuracy_validated",
                "independent_spousal_illness_accuracy_validated",
                "independent_pair_survival_order_validated",
                "real_human_danger_or_abuse_label_authorized",
                "medical_lifespan_forecast_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key])

    def test_17_corpus_count_and_frozen_source_digest(self):
        self.assertEqual(self.accept["prior_lilly"], 8343)
        self.assertEqual(self.accept["lilly_if_published"], 8397)
        self.assertEqual(self.accept["combined_if_published"], 9463)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
