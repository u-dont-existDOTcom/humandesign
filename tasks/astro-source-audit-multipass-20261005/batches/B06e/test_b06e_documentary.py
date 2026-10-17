"""Original Lilly CXXVIII disease sources: DOCUMENTARY integrity, not medical validation."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class EyesEarsSpeechDiseaseOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.boundary = j("ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_images_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(615, 628)])
        for row in self.w["images"].values():
            path = B / row["file"]
            data = path.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(sha(path), row["sha256"])

    def test_02_original_chapter_boundaries_and_folios(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [615, 616, 617, 618, 619])
        self.assertEqual(self.w["next_printed_CHAP_CXXIX_heading_pdf"], 619)
        self.assertEqual(self.w["following_CHAP_CXXX_heading_pdf"], 620)
        self.assertEqual(self.boundary["printed_chapter"], "CXXVIII")
        self.assertEqual(self.boundary["following_printed_chapter"], "CXXIX")
        self.assertEqual(self.boundary["last_chapter_text_pdf_frame"], 619)
        self.assertEqual(
            [self.w["images"][str(n)]["printed_folio"] for n in range(615, 621)],
            ["581", "582", "583", "584", "585", "586"],
        )

    def test_03_all_records_in_order_no_reuse(self):
        self.assertEqual(
            [row["record_number"] for row in self.r["rules"]],
            list(range(7696, 7809)),
        )
        self.assertEqual(len({row["id"] for row in self.r["rules"]}), 113)

    def test_04_bidirectional_eleven_passage_groups_exact(self):
        refs = []
        for authored, reverse in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], reverse["source_span"])
            self.assertEqual(authored["original_pdf_frames"], reverse["original_pdf_frames"])
            group_ids = [item["id"] for item in authored["claims"]]
            self.assertEqual(reverse["mapped_record_ids"], group_ids)
            refs.extend(group_ids)
        self.assertEqual(refs, [row["id"] for row in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 11)

    def test_05_all_eight_named_medical_subsections_preserved(self):
        self.assertEqual(len(self.a["historical_topics"]), 8)
        self.assertEqual(self.roles["heading"], 8)
        for label in ("Sight", "Eares", "Tongue", "Tooth", "Falling", "Stone", "Gout", "Fals"):
            self.assertIn(label, self.text)

    def test_06_eye_sun_moon_infortunes_and_angular_qualifications(self):
        for role in ("vision_condition", "vision_angle", "vision_result", "angular_harm"):
            self.assertEqual(self.roles[role], 1)

    def test_07_three_original_milky_way_windows(self):
        self.assertEqual(self.roles["star_window"], 3)
        for term in (
            "21 Gemini",
            "seventh to seventeenth Sagittarius",
            "twenty second Sagittarius",
        ):
            self.assertIn(term, self.text)

    def test_08_cloudy_stars_historic_name_list(self):
        self.assertEqual(self.roles["cloudy_star"], 5)
        for term in ("Pleiades", "Praesepe", "Coma Berenices", "Orion"):
            self.assertIn(term, self.text)

    def test_09_eye_laterality_and_old_harm_mitigation(self):
        self.assertEqual(self.roles["sun_eye"], 1)
        self.assertEqual(self.roles["moon_eye"], 1)
        self.assertEqual(self.roles["eye_cause"], 2)
        self.assertEqual(self.roles["vision_contrary"], 1)
        self.assertEqual(self.roles["squint_result"], 1)

    def test_10_ear_saturn_mercury_malefics_and_benefic_mitigation(self):
        for role in (
            "ear_malefics",
            "ear_saturn",
            "ear_house",
            "ear_mercury",
            "ear_saturn_aspect",
            "ear_moon",
            "ear_infortunes",
            "ear_mercury_alt",
            "ear_hearing_result",
            "ear_tenth",
            "ear_mitigation",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_11_speech_sun_mercury_saturn_and_mute_signs_separate(self):
        for role in (
            "speech_sun",
            "speech_angular",
            "speech_no_benefic",
            "speech_beams",
            "speech_mute",
            "speech_combust",
            "speech_water",
            "speech_sixth",
            "speech_saturn",
            "speech_scorpio",
            "speech_moon",
            "speech_lord_sixth",
            "speech_all_mute",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_12_dental_planet_and_zodiac_exceptions(self):
        for role in (
            "teeth_mars",
            "teeth_cancer_pisces",
            "teeth_loss",
            "teeth_saturn",
            "teeth_malefics",
            "teeth_saturn_asc",
            "teeth_seventh",
            "teeth_earth",
            "teeth_air",
            "teeth_fire",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("except Capricorn or Aquarius", self.text)

    def test_13_falling_sickness_historical_attribution_four_sources(self):
        for role in (
            "seizure_authority",
            "seizure_first",
            "seizure_second_signs",
            "seizure_second_houses",
            "seizure_third_daynight",
            "seizure_third_position",
            "seizure_fourth",
            "seizure_result",
        ):
            self.assertEqual(self.roles[role], 1)
        for name in ("Albubater", "Cardanus", "Pontanus"):
            self.assertIn(name, self.text)

    def test_14_seizure_falls_symptom_not_medical_diagnosis(self):
        self.assertEqual(self.roles["seizure_humors"], 1)
        self.assertEqual(self.roles["seizure_symptom"], 1)
        self.assertIn("foame at mouth", self.text)

    def test_15_neurologic_and_psychiatric_stereotypes_unvalidated(self):
        self.assertEqual(self.roles["mental_overlap"], 1)
        for role in (
            "mental_moon",
            "mental_malefics",
            "mental_solar",
            "mental_sun_venus",
            "mental_moon_house",
            "mental_fullmoon",
            "mental_venus_mercury",
            "mental_sun_cancer",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_16_stone_urinary_symptoms_signs_aspects_distinct(self):
        for role in (
            "stone_sect",
            "stone_mars",
            "stone_moon",
            "stone_moon_sign",
            "stone_result",
            "strangury_scorpio",
            "strangury_taurus",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_17_gout_age_and_nocturnal_compound_preserved(self):
        for role in (
            "gout_luminaries",
            "gout_signs",
            "gout_placement",
            "gout_age",
            "gout_night",
            "gout_saturn",
            "gout_saturn_pisces",
            "gout_saturn_weak",
            "gout_hard",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("Youth afterward Gout", self.text)

    def test_18_violent_falls_malefics_fixed_stars_travel_and_houses(self):
        for role in (
            "fall_airy",
            "fall_tenth",
            "fall_author",
            "fall_mars_twelfth",
            "fall_horses",
            "fall_saturn",
            "fall_aspect",
            "fall_house",
            "fall_outcome",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_19_author_retroactive_claim_is_not_proof(self):
        x = next(row for row in self.r["rules"] if row["role"] == "fall_author")
        self.assertEqual(x["source_qualification"], "unverified-author-anecdote")
        self.assertFalse(x["independent_human_medical_result_validated"])

    def test_20_unresolved_glyphs_are_not_executable(self):
        unresolved = [
            r
            for r in self.r["rules"]
            if r["source_qualification"] in {"glyph-qualified", "glyph-unresolved"}
        ]
        self.assertGreaterEqual(len(unresolved), 3)
        self.assertTrue(all(not r["runtime_model_promoted"] for r in unresolved))

    def test_21_curability_cxxix_and_servants_cxxx_not_ingested(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7807", "R7808"],
        )
        self.assertEqual(self.r["substantive_historical_conditions"], 111)
        self.assertEqual(self.acc["next_printed_chapter"], "CXXIX")
        self.assertEqual(self.acc["next_original_pdf"], 619)

    def test_22_zero_human_medicine_psychiatry_validations_and_runtime(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_medical_or_psychiatric_accuracy"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.a["medical_clinical_evidence"])
        self.assertFalse(self.l["clinical_medical_advice_authorized"])
        self.assertFalse(self.l["actual_person_psychological_labels_authorized"])
        for row in self.r["rules"]:
            self.assertFalse(row["independent_human_medical_result_validated"])
            self.assertFalse(row["modern_ophthalmic_neurological_diagnosis_validated"])
            self.assertFalse(row["reliable_falls_disability_or_lifespan_prediction"])
            self.assertFalse(row["person_level_moral_or_psychiatric_label_authorized"])
            self.assertFalse(row["clinical_or_medical_treatment_advice_authorized"])
            self.assertFalse(row["runtime_model_promoted"])

    def test_23_scanned_document_not_full_diplomatic(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.l["issues"]), 20)

    def test_24_final_frozen_source_hashes_and_count(self):
        self.assertEqual(self.acc["previous_lilly"], 7695)
        self.assertEqual(self.acc["lilly_if_published"], 7808)
        self.assertEqual(self.acc["combined_if_published"], 8874)
        self.assertEqual(sha(B / "RULES.json"), self.acc["rules_sha256"])
        self.assertEqual(
            sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"), self.acc["authoring_sha256"]
        )
        self.assertEqual(
            sha(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json"), self.acc["boundary_sha256"]
        )


if __name__ == "__main__":
    unittest.main()
