"""B02v source-only provenance and repaired semantic boundaries.

These checks do NOT prove that 402 paraphrases fully match the historical scan,
that the entire chapter has been independently reviewed, or that astrology
makes valid claims about real people or objects. B02v remains UNACCEPTED.
"""
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


RULES = load("RULES_DRAFT.json")
COUNTS = load("COUNTS.json")
ISSUES = load("UNRESOLVED_DRAFT.json")
TABLES = load("PRINTED_DIRECTION_TABLES.json")
IMAGE_MANIFEST = load("SOURCE_IMAGE_MANIFEST.json")
INDEX = load("RETAINED_LILLY_INDEX_BEFORE.json")
RECORDS = RULES["records"]
BY_NO = {r["record_number"]: r for r in RECORDS}


class DocumentaryIntegrity(unittest.TestCase):
    def test_unchanged_accepted_predecessor(self):
        self.assertEqual(INDEX["records_count"], 2572)
        self.assertEqual(INDEX["batches"][-1]["id"], "B02u")
        self.assertEqual(INDEX["next"]["pdf_page"], 381)
        self.assertEqual(COUNTS["accepted_lilly_before"], 2572)
        self.assertEqual(COUNTS["retained_ptolemy"], 1066)

    def test_provisional_never_accepted(self):
        self.assertFalse(RULES["accepted"])
        self.assertFalse(COUNTS["independent_fidelity_review_complete"])
        self.assertTrue(COUNTS["full_chapter_l_completion_not_yet_admitted"])
        self.assertEqual(COUNTS["accepted_new_documentary_records"], 0)
        self.assertFalse(COUNTS["runtime_promotion"])

    def test_records_contiguous_and_unique(self):
        self.assertEqual(len(RECORDS), 402)
        self.assertEqual(len(BY_NO), 402)
        self.assertEqual(list(BY_NO), list(range(2573, 2975)))
        self.assertEqual([r["id"] for r in RECORDS],
            [f"LI.1647.II.L.R{i}" for i in range(2573, 2975)])
        self.assertEqual(len({r["source_record_kind"] for r in RECORDS}), 402)

    def test_no_chapter_li_body_admitted(self):
        self.assertTrue(all(r["chapter"] == "L" for r in RECORDS))
        self.assertEqual(BY_NO[2974]["source_record_kind"], "chapter_li_boundary")
        self.assertIn("divider", BY_NO[2974]["source_statement"])
        self.assertEqual(BY_NO[2974]["source_locator"]["pdf_pages"], [400])

    def test_every_original_page_located(self):
        seen = {p for r in RECORDS for p in r["source_locator"]["pdf_pages"]}
        self.assertEqual(seen, set(range(381, 401)))
        self.assertEqual(len(RULES["source_pdf_pages"]), 20)
        for r in RECORDS:
            ps = r["source_locator"]["pdf_pages"]
            self.assertEqual(r["source_locator"]["printed_pages"], [p - 34 for p in ps])

    def test_manifest_21_original_images_and_hashes(self):
        self.assertEqual(len(IMAGE_MANIFEST["images"]), 21)
        self.assertEqual(
            sorted(x["pdf_page"] for x in IMAGE_MANIFEST["images"]),
            list(range(381, 401)) + [888])
        for item in IMAGE_MANIFEST["images"]:
            source = BASE / item["path"]
            self.assertEqual(source.stat().st_size, item["bytes"])
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), item["sha256"])

    def test_three_distinct_source_tables(self):
        witness = TABLES["original_table_witnesses"]
        self.assertEqual(len(witness), 3)
        self.assertEqual([len(t["rows"]) for t in witness], [12, 12, 12])
        self.assertEqual([t["source_pdf_page"] for t in witness], [398, 399, 399])
        self.assertNotEqual(witness[1]["rows"], witness[2]["rows"])

    def test_corrected_house_vs_door_glyph(self):
        self.assertEqual(BY_NO[2576]["source_record_kind"], "sun_as_thief_house_marker")
        self.assertEqual(BY_NO[2577]["source_record_kind"], "sun_oriental_house_east")
        self.assertIn("Moon", BY_NO[2576]["source_statement"])

    def test_p358_cusps_not_silently_rulers(self):
        self.assertEqual(
            BY_NO[2785]["source_record_kind"],
            "first_lord_to_second_second_lord_to_asc_textual")
        self.assertIn("'the second'", BY_NO[2785]["source_statement"])
        self.assertIn("'the Ascendant'", BY_NO[2785]["source_statement"])

    def test_p360_aspect_includes_conjunction(self):
        self.assertEqual(
            BY_NO[2819]["source_record_kind"],
            "sun_conjunction_square_opposition_thief_known")
        self.assertIn("conjunction, square or opposition", BY_NO[2819]["source_statement"])

    def test_p360_sixth_not_first(self):
        self.assertEqual(BY_NO[2832]["source_record_kind"], "owner_self_second_sixth_seventh")
        self.assertIn("second, sixth or seventh", BY_NO[2832]["source_statement"])

    def test_p361_specific_part_of_fortune(self):
        self.assertEqual(
            BY_NO[2848]["source_record_kind"],
            "part_fortune_or_lord7_free_first_offence")
        self.assertIn("Part of Fortune", BY_NO[2848]["source_statement"])

    def test_p362_age_source_literal(self):
        self.assertEqual(
            BY_NO[2873]["source_record_kind"],
            "age_methods_greatest_number_textual")
        self.assertIn("greatest number", BY_NO[2873]["source_statement"])

    def test_p365_capture_repair_no_p366_copy(self):
        expected = {
            2940: "capture_seventh_lord_join_retrograde",
            2941: "capture_moon_from_seventh_to_conj_first",
            2942: "capture_moon_from_conj_first_toward_seventh",
            2943: "capture_sun_moon_seventh_join_or_behold",
            2944: "capture_seventh_lord_to_combustion",
            2945: "capture_first_lord_conjunction_angles_or_infortune_seventh",
        }
        for n, kind in expected.items():
            self.assertEqual(BY_NO[n]["source_record_kind"], kind)
            self.assertEqual(BY_NO[n]["source_locator"]["pdf_pages"], [399])
        self.assertIn("some say", BY_NO[2943]["exceptions_and_evidence_limits"][0])
        self.assertNotIn("square to Mars", BY_NO[2941]["source_statement"])

    def test_p366_capture_list_remains_distinct(self):
        self.assertEqual(BY_NO[2968]["source_locator"]["pdf_pages"], [400])
        self.assertIn("square", BY_NO[2968]["source_statement"])
        self.assertIn("Mercury", BY_NO[2969]["source_statement"])
        self.assertEqual(BY_NO[2973]["source_locator"]["pdf_pages"], [400])

    def test_retained_issues_count_and_unique(self):
        self.assertEqual(ISSUES["retained_count"], len(ISSUES["issues"]))
        self.assertEqual(len({i["id"] for i in ISSUES["issues"]}), ISSUES["retained_count"])
        self.assertEqual(ISSUES["retained_count"], 50)
        self.assertIn("U50", {i["id"] for i in ISSUES["issues"]})

    def test_every_record_reference_only(self):
        for r in RECORDS:
            self.assertFalse(r["prospective_blinded_prediction"])
            self.assertFalse(r["case_evidence_countable"])
            self.assertFalse(r["independently_authenticated_outcome"])
            self.assertTrue(r["source_witness_only"])
            self.assertEqual(r["runtime_status"], "REFERENCE_ONLY_NOT_PROMOTED")

    def test_source_component_counts_sum(self):
        self.assertEqual(sum(x["records"] for x in COUNTS["draft_sources"]), 402)
        self.assertEqual(len(COUNTS["draft_sources"]), 7)
        self.assertEqual(COUNTS["lilly_if_accepted"], 2974)
        self.assertEqual(COUNTS["combined_if_accepted"], 4040)

    def test_originals_frozen_before_edit(self):
        backups = {
            "producer_p381_384_before_20261014_sun_review.json":
                "0157b9b0c1855f49cf24f462b9aac1f9e613548bb41211911e3911df350dfd5a",
            "producer_p393_395_before_20261014_p360_review.json":
                "176c99f0c9c36309ae6b311a4d2510c3819bd58484bf7f0e64ad895aed4b6561",
            "producer_p391_392_before_20261014_p358_review.json":
                "d468270e13eb4d1dae295733d39832f9596baa684f05ee149511b37ab6c761f9",
            "producer_p398_400_before_20261014_p365_capture_review.json":
                "db7505bcf5ff0ea149c876d7a6eedc460ca47c4f4620160f20dd91780335598e",
        }
        for name, expected in backups.items():
            p = BASE / "recovery" / name
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), expected)

    def test_p360_erratum_kept_unresolved(self):
        entry = load("ERRATA_COLLATION.json")["candidate_in_scope"][0]
        self.assertEqual(entry["printed_page"], 360)
        self.assertEqual(entry["original_pdf_page"], 394)
        self.assertTrue(entry["body_line_located"])
        self.assertFalse(entry["read_word_or_glyph_verified"])


if __name__ == "__main__":
    unittest.main()
