"""C29 document-only matrix and strict non-predictive model scope."""
import hashlib
import json
import unittest
from pathlib import Path

from hellenistic_c29_source_candidate_matrix import (
    CANDIDATES, ROOT, SNAPSHOT, build_documentary_matrix,
    frozen_source_snapshot,
)
from paulus_bysign_papyrus_c04 import (
    documented_papyrus_check, sign_monomoiria,
)
from paulus_monomoiria_source_c04 import edited_day_degree_ruler
from paulus_c21_luminary_scope import chapter32_sect_light_ruler


class TestC29DocumentarySourceMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cls.generated = frozen_source_snapshot()
        cls.rows = cls.generated["trigon_rows"]
        cls.signs = cls.generated["by_sign_rows"]

    def test_exact_frozen_snapshot_reproduces(self):
        self.assertEqual(self.expected, self.generated)
        self.assertEqual(len(self.generated["documentary_matrix_sha256"]), 64)

    def test_source_dependency_hashes_real_bytes(self):
        for path, digest in self.generated["source_input_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        self.assertEqual(len(self.generated["source_input_sha256"]), 10)

    def test_no_biographical_input_or_human_validation(self):
        self.assertEqual(self.generated["root_goal_status"], "OPEN")
        self.assertEqual(self.generated["gates"]["human_predictive_validations"], 0)
        self.assertFalse(self.generated["gates"]["production_scoring_modified"])
        self.assertFalse(self.generated["gates"]["input_dates_or_life_events_used"])
        self.assertTrue(self.generated["gates"]["ruler_data_not_behavioral_outcome_mapping"])

    def test_360_sign_vs_120_trigon_no_conflation(self):
        self.assertEqual(len(self.signs), 360)
        self.assertEqual(len(self.rows), 120)
        self.assertEqual(len({(r["sign"],r["completed_degrees"]) for r in self.signs}),360)
        self.assertEqual(len({(r["trigon"],r["ordinal_degree"]) for r in self.rows}),120)
        self.assertEqual(self.signs[0]["sign"], "Aries")
        self.assertEqual(self.signs[0]["completed_degrees"], 0)
        self.assertEqual(self.signs[0]["CH5_BY_SIGN_CHALDEAN"], "Mars")
        self.assertEqual(self.rows[0]["CH32_GREEK_NARRATIVE_DAY"], "Sun")

    def test_physical_vs_ordinal_degree_one_based(self):
        self.assertEqual(sign_monomoiria("Aries",0,0),sign_monomoiria("Aries",0,59))
        self.assertEqual(self.signs[0]["ordinal_degree"],1)
        self.assertEqual(self.signs[29]["ordinal_degree"],30)
        with self.assertRaises(ValueError):
            sign_monomoiria("Aries",30,0)
        with self.assertRaises(ValueError):
            sign_monomoiria("Aries",0,60)

    def test_manifest_candidate_status_and_domains(self):
        m={x["id"]:x for x in CANDIDATES}
        self.assertEqual(len(m),9)
        self.assertEqual({m["FLORENCE_COMMENTARY_FIRST_SLOT"]["sect"],
                          m["FLORENCE_COMMENTARY_SECOND_SLOT"]["sect"]},{"UNKNOWN"})
        self.assertEqual(m["VIENNA_115_STRUCTURAL_ONLY"]["row_count"],0)
        self.assertEqual(m["VIENNA_108_CATALOGUE_ONLY"]["row_count"],0)
        self.assertTrue(all(x["eligible_as_verified_human_outcome_model"] is False
                            for x in CANDIDATES))

    def test_printed_editor_day_never_impersonates_night(self):
        with self.assertRaises(ValueError):
            edited_day_degree_ruler("Aries",1,sect="night")

    def test_greek_ch32_only_on_actual_light_of_sect(self):
        self.assertEqual(chapter32_sect_light_ruler(
            sect="day",luminary="Sun",light_sign="Aries",ordinal_degree=1),"Sun")
        self.assertEqual(chapter32_sect_light_ruler(
            sect="night",luminary="Moon",light_sign="Aries",ordinal_degree=1),"Jupiter")
        with self.assertRaises(ValueError):
            chapter32_sect_light_ruler(
                sect="night",luminary="Sun",light_sign="Aries",ordinal_degree=1)

    def test_all_earlier_photo_disagreements_explicit(self):
        x=self.generated["summary"]
        self.assertEqual(x["Greek_day_vs_Greenbaum_edited_day_disagreements"],34)
        self.assertEqual(x["Florence_first_vs_Greek_day_matches"],104)
        self.assertEqual(x["Florence_first_vs_Greenbaum_day_matches"],102)
        self.assertEqual(x["Florence_second_vs_Greek_night_matches"],48)
        self.assertEqual(x["Florence_second_adjacent_pair_swap_matches"],120)
        self.assertEqual(x["Older_Paulus_vatican_matches_neither_day"],96)

    def test_ancient_ch5_negative_still_reported(self):
        p=documented_papyrus_check()
        mercury=[x for x in p["records"] if x["body"]=="Mercury"]
        self.assertEqual(len(mercury),1)
        self.assertFalse(mercury[0]["agrees"])
        self.assertEqual(mercury[0]["textual_status"],"SOURCE_REPORTED_ERROR")

    def test_unknown_manuscript_sources_not_inferred_to_day_or_night(self):
        self.assertTrue(self.generated["gates"]["unknown_photo_slot_sect_not_inferred"])
        self.assertTrue(self.generated["gates"]["C28_codex_108_115_distinction_preserved"])
        self.assertTrue(self.generated["gates"]["no_auto_selection_or_weighted_ensemble"])
        self.assertTrue(self.generated["gates"]["Boer_1962_apparatus_still_unread"])
        for row in self.rows:
            self.assertNotIn("VIENNA_108_CATALOGUE_ONLY", row)
            self.assertNotIn("VIENNA_115_STRUCTURAL_ONLY", row)

    def test_no_hephaistio_time_lord_accidental_blend(self):
        self.assertFalse(self.generated["unresolved_separate_timing_family"]
                         ["production_timing_prediction_available"])


if __name__ == "__main__":
    unittest.main()
