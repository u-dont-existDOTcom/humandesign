"""Historical-only first-edition source-coverage and archive tests for B05j."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class FirstEditionFacialSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.records = read("RULES.json")
        cls.mapping = read("SOURCE_FIRST_REVERSE_MAP.json")
        cls.orig = read("ORIGINAL_SOURCE_INTEGRITY.json")
        cls.window = read("SOURCE_WINDOW_20261017.json")
        cls.unresolved = read("UNRESOLVED_SOURCE_QUALIFICATIONS.json")
        cls.admission = read("ACCEPTANCE.json")

    def test_01_original_source_bytes(self):
        for page in self.orig["images"].values():
            source = BASE / self.window["original_scans"][str(page["pdf_frame"])]["file"]
            self.assertEqual(digest(source), page["image_sha256"])
            self.assertEqual(source.stat().st_size, page["bytes"])
            self.assertEqual(source.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_misprinted_folio_preserved_in_physical_order(self):
        self.assertEqual(
            self.orig["printed_folio_sequence"], ["539", "548", "549", "542", "543", "552"]
        )
        self.assertEqual(self.orig["source_body_original_pdf_frames"], [581, 582, 583])

    def test_03_first_next_heading_same_physical_page(self):
        self.assertEqual(self.orig["first_next_chapter_heading_pdf_frame"], 583)
        self.assertEqual(self.admission["next_original_pdf_frame"], 583)

    def test_04_consecutive_source_record_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.records["rules"]], list(range(6672, 6734))
        )
        self.assertEqual(self.records["record_count"], 62)

    def test_05_bidirectional_source_coverage(self):
        found = []
        for s, mapping in zip(
            self.input["source_groups"], self.mapping["source_groups"], strict=True
        ):
            self.assertEqual(s["source_span"], mapping["source_span"])
            self.assertEqual(s["original_pdf_frames"], mapping["original_pdf_pages"])
            self.assertEqual([c["id"] for c in s["claims"]], mapping["mapped_record_ids"])
            found += mapping["mapped_record_ids"]
        self.assertEqual(found, [r["id"] for r in self.records["rules"]])
        self.assertEqual(len(found), len(set(found)))
        self.assertEqual(len(self.mapping["source_groups"]), 11)

    def test_06_all_zodiac_groups_separated(self):
        signs = [
            "Aries",
            "Taurus",
            "Libra",
            "Scorpio",
            "Leo",
            "Virgo",
            "Sagittarius",
            "Cancer",
            "Capricorn",
            "Pisces",
            "Gemini",
            "Aquarius",
        ]
        z = [r for r in self.records["rules"] if r["role"] == "zodiac_stature"]
        self.assertEqual(len(z), 5)
        joined = " ".join(r["anchor_not_diplomatic"] for r in z)
        for sign in signs:
            self.assertEqual(joined.split().count(sign), 1, sign)

    def test_07_distinct_colour_testimony_sources(self):
        roles = Counter(r["role"] for r in self.records["rules"])
        self.assertEqual(roles["source_selection"], 6)

    def test_08_all_humours_and_benefic_malefic_modifiers(self):
        text = " ".join(r["anchor_not_diplomatic"] for r in self.records["rules"])
        for token in (
            "Sanguine",
            "Phlegmatick",
            "Cholerick",
            "Melanchollick",
            "Fortunes",
            "Infortunes",
        ):
            self.assertIn(token, text)

    def test_09_premodern_majority_mixture_discretion(self):
        kinds = [r for r in self.records["rules"] if r["role"] == "scoring_procedure"]
        self.assertEqual(len(kinds), 3)
        self.assertTrue(any("greater number" in r["anchor_not_diplomatic"] for r in kinds))
        self.assertTrue(any("discretionary" in r["meaning_historical_only"] for r in kinds))

    def test_10_explicit_geographical_override(self):
        roles = Counter(r["role"] for r in self.records["rules"])
        self.assertEqual(roles["geographic_override"], 1)
        self.assertEqual(roles["geographic_example"], 2)
        text = " ".join(r["anchor_not_diplomatic"] for r in self.records["rules"])
        for token in ("Spaniard", "Danes", "Climate or Country"):
            self.assertIn(token, text)

    def test_11_five_separate_facial_proportion_sources(self):
        self.assertEqual(sum(r["role"] == "facial_proportions" for r in self.records["rules"]), 5)

    def test_12_waxing_planet_quality_not_unconditional(self):
        roles = Counter(r["role"] for r in self.records["rules"])
        self.assertEqual(roles["planetary_favour"], 2)
        self.assertEqual(roles["planetary_exception"], 2)
        self.assertEqual(roles["luminary_dignity"], 1)
        self.assertEqual(roles["sun_exception"], 1)

    def test_13_seasonal_appearance_fully_recorded(self):
        r = [x for x in self.records["rules"] if x["role"] == "seasonal_form"]
        self.assertEqual(len(r), 4)
        joined = " ".join(x["anchor_not_diplomatic"] for x in r)
        for part in ("Vernall", "AEstivall", "Autumnall", "Hybernall"):
            self.assertIn(part, joined)

    def test_14_stature_fallbacks_not_dropped(self):
        role_count = Counter(r["role"] for r in self.records["rules"])
        self.assertEqual(role_count["planet_stature"], 3)
        self.assertEqual(role_count["planet_stature_exception"], 1)
        self.assertEqual(role_count["selection_fallback"], 3)
        self.assertEqual(role_count["luminary_fallback"], 1)
        self.assertEqual(role_count["mercury_override"], 1)

    def test_15_chapter_opening_is_not_an_ingested_rule(self):
        nav = [x for x in self.records["rules"] if x["role"] == "next_chapter_navigation"]
        self.assertEqual([r["id"] for r in nav], ["R6732", "R6733"])
        self.assertEqual(self.records["substantive_historical_units"], 60)

    def test_16_no_biometric_ancestry_diagnosis_or_science_proof(self):
        self.assertEqual(self.admission["human_biometric_validations"], 0)
        self.assertEqual(self.admission["medical_or_ancestry_validations"], 0)
        self.assertEqual(self.records["empirical_validations"], 0)
        self.assertEqual(self.records["runtime_promotions"], 0)
        for r in self.records["rules"]:
            self.assertTrue(r["historical_documentary_accepted"])
            for field in (
                "independent_human_biometric_validation",
                "validated_ancestry_or_ethnicity_prediction",
                "validated_medical_or_disability_prediction",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[field])

    def test_17_qualifications_explicitly_unresolved(self):
        text = " ".join(self.unresolved["unresolved"])
        for x in ("glyph", "Climate", "Spaniard", "Dane", "Book I", "stigma", "source"):
            # Check conceptual provenance without claiming a full transcription.
            self.assertTrue(
                x.lower() in text.lower() or (x == "stigma" and "disability" in text.lower()), x
            )
        self.assertFalse(self.unresolved["exact_diplomatic_transcription"])

    def test_18_corpus_count_and_source_checksums(self):
        self.assertEqual(self.admission["previous_lilly"], 6671)
        self.assertEqual(self.admission["lilly_if_published"], 6733)
        self.assertEqual(self.admission["historical_corpus_if_published"], 7799)
        self.assertEqual(digest(BASE / "RULES.json"), self.admission["records_sha256"])
        self.assertEqual(
            digest(BASE / "SOURCE_FIRST_AUTHORING_20261017.json"),
            self.admission["source_authoring_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
