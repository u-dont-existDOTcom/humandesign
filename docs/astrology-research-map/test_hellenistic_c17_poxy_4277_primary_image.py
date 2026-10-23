"""C17 Oxford original P.Oxy. 4277 image authentication and negative arithmetic.

Hashing a genuine papyrus photo is not equivalent to palaeographic
verification of all reported numerical labels, nor to human prediction.
"""
import unittest
from pathlib import Path

from poxy4277_original_image_c17 import (
    source_record, historical_documentary_comparison,verify_local_study_images
)


class TestC17OxfordPrimaryPhotographs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=source_record()
        cls.summary=historical_documentary_comparison()

    def test_exact_oxford_publication_identity(self):
        r=self.record["record"]
        self.assertEqual(r["title"],"P.Oxy. LXI 4277. Deluxe Horoscope")
        self.assertEqual(r["official_record_id"],21178150)
        self.assertEqual(r["doi"],"10.25446/oxford.21178150.v1")
        self.assertEqual(r["collection_group_id"],35280)
        self.assertIn("/21178150",r["official_record_link"])
        self.assertIn("figshare.com/v2/articles/21178150",r["official_machine_record"])

    def test_oxford_publisher_two_exact_image_file_ids(self):
        arr=self.record["official_images"]
        self.assertEqual(len(arr),2)
        self.assertEqual([f["id"] for f in arr],[37552438,37552441])
        self.assertEqual([f["downloaded_bytes"] for f in arr],[9361845,192831])
        self.assertEqual([f["image_dimensions"] for f in arr],[[3660,2632],[567,343]])

    def test_main_photo_publisher_md5_and_local_sha_verifiable(self):
        f=self.record["official_images"][0]
        self.assertEqual(f["publisher_md5"],"b62daf036de9d026b8e986f7c74c5bb3")
        self.assertEqual(f["sha256"],"aefec1af94416903fc25863bc7f8f74d9278fd9d4b3cc8f18056b01f2b06a084")
        self.assertTrue(f["visual_inspection"].startswith("PRIMARY ORIGINAL"))
        self.assertFalse(f["complete_image_in_git"])

    def test_second_fragment_does_not_claim_verso(self):
        f=self.record["official_images"][1]
        self.assertEqual(f["publisher_md5"],"fbfc8184bec0bc05f8f61b5d3c4ff506")
        self.assertEqual(f["sha256"],"60e243177a325b26c53be96f17db439a2e176729ac64dd4f884a2708a69c9abe")
        self.assertIn("did not assume recto/verso",f["visual_inspection"])
        self.assertFalse(f["complete_image_in_git"])

    def test_original_object_image_verified_not_individual_glyphs(self):
        r=self.summary
        self.assertTrue(r["Oxford_exact_object_identity_verified"])
        self.assertEqual(r["photographs_directly_visually_inspected"],2)
        self.assertTrue(r["Publisher_supplied_and_local_MD5_sha256_verified"])
        self.assertEqual(r["historical_readings_independently_collated_from_photo"],0)
        self.assertEqual(self.record["comparison_with_older_C05"]["old_three_labels_confirmed_by_independent_palaeographic_reading_in_C17"],0)

    def test_C05_1_of_3_calculation_and_both_negative_cases_survive(self):
        r=self.summary
        self.assertEqual(r["preexisting_C05_source_arithmetic_agreements"],1)
        self.assertEqual(r["preexisting_C05_source_arithmetic_disagreements"],2)
        self.assertEqual([(d["object"],d["matches"]) for d in r["rows"]],[("Mercury",False),("Midheaven",False),("Lower midheaven",True)])
        self.assertTrue(all(not d["original_photo_label_read_independently"] for d in r["rows"]))

    def test_no_retroactive_source_upgrade_of_C05(self):
        r=self.record["comparison_with_older_C05"]
        self.assertIn("NOT_RECHECKED",r["C05_status_at_that_time"])
        self.assertIn("NUMERICAL_GLYPHS_NOT_INDEPENDENTLY_RETRANSCRIBED",r["C17_status"])

    def test_zodiacal_place_is_not_monomoiria(self):
        s=self.record["separate_categories"]
        self.assertIn("Valens VIII.7",s["zodiacal_place"])
        self.assertIn("NOT the same doctrine",s["zodiacal_place"])
        self.assertIn("Do not pool",s["zodiacal_terms_and_triplicity"])

    def test_hash_verify_missing_id_fails_closed(self):
        with self.assertRaises(ValueError):
            verify_local_study_images({37552438:Path("/definitely/not/valid")})

    def test_hash_verify_nonexistent_files_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            verify_local_study_images({37552438:Path("/missing/papyrus1.jpg"),37552441:Path("/missing/papyrus2.jpg")})

    def test_copyright_no_papyrus_files_redistributed(self):
        r=self.record["copyright"]
        self.assertTrue(r["not_redistributed"])
        self.assertEqual(r["image_rights"],"In Copyright")
        self.assertTrue(r["repo_contains_only_original_image_checksums_and_interpretation"])
        self.assertTrue(r["purchased_Gansten_Kindle_not_extracted"])

    def test_not_validating_real_human_chart_predictions(self):
        self.assertFalse(self.summary["scoring_rule_promoted"])
        self.assertEqual(self.summary["newly_confirmed_astrological_natal_predictions"],0)
        self.assertFalse(self.record["remaining_tasks"]["production_rule_promotion"])
        self.assertEqual(self.record["audit_controls"]["blind_human_predictive_validations"],0)


if __name__=="__main__":
    unittest.main()
