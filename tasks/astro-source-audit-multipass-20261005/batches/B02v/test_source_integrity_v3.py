"""B02v source-only integrity checks, revision V3 after original PDF388 correction.

V2 remains frozen as historical verification of the first archival snapshot;
its hard-coded 50-issue assertion is obsolete for the 51-issue V3 source state.
Neither test version certifies a 402-record exhaustive independent review.
"""
import hashlib
import json
import unittest
from pathlib import Path

B=Path(__file__).resolve().parent
def get(name):return json.loads((B/name).read_text())
R=get("RULES_DRAFT.json")
C=get("COUNTS.json")
U=get("UNRESOLVED_DRAFT.json")
P={r["record_number"]:r for r in R["records"]}
M=get("SOURCE_IMAGE_MANIFEST.json")
D=get("PRINTED_DIRECTION_TABLES.json")
I=get("RETAINED_LILLY_INDEX_BEFORE.json")

class V3OriginalSourceSafety(unittest.TestCase):
    def test_previous_accepted_is_unchanged(self):
        self.assertEqual(I["records_count"],2572)
        self.assertEqual(I["batches"][-1]["id"],"B02u")
        self.assertEqual(C["accepted_lilly_before"],2572)
        self.assertEqual(C["retained_ptolemy"],1066)
    def test_current_research_is_still_provisional(self):
        self.assertFalse(R["accepted"])
        self.assertEqual(C["accepted_new_documentary_records"],0)
        self.assertFalse(C["independent_fidelity_review_complete"])
        self.assertTrue(C["full_chapter_l_completion_not_yet_admitted"])
        self.assertFalse(C["runtime_promotion"])
    def test_402_serial_source_units_only(self):
        self.assertEqual([x["record_number"] for x in R["records"]],list(range(2573,2975)))
        self.assertEqual(C["proposed_new_documentary_records"],402)
        self.assertEqual((C["lilly_if_accepted"],C["combined_if_accepted"]),(2974,4040))
    def test_every_record_is_historical_not_observed_case(self):
        self.assertTrue(all(x["source_witness_only"] and not x["case_evidence_countable"] and not x["prospective_blinded_prediction"] for x in R["records"]))
        self.assertTrue(all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for x in R["records"]))
    def test_source_images_original_bytes(self):
        self.assertEqual(len(M["images"]),21)
        self.assertEqual(sorted(x["pdf_page"] for x in M["images"]),list(range(381,401))+[888])
        for x in M["images"]:
            f=B/x["path"]
            self.assertEqual((f.stat().st_size,hashlib.sha256(f.read_bytes()).hexdigest()),(x["bytes"],x["sha256"]))
    def test_corrected_quern_not_oven(self):
        row=P[2699]
        self.assertEqual(row["source_record_kind"],"tenth_moon_underground_quern")
        self.assertIn("quern",row["source_statement"].lower())
        self.assertNotIn("oven",row["source_statement"].lower())
        original=B/"recovery/producer_p388_390_before_20261014_quern_review.json"
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),"8f629a70b9b693a26928e1c77fb0b41990ab19b2f69c59019771b7fa68e6ea10")
    def test_corrupted_p360_and_others_not_regressed(self):
        expect={
            2576:"sun_as_thief_house_marker",
            2577:"sun_oriental_house_east",
            2785:"first_lord_to_second_second_lord_to_asc_textual",
            2819:"sun_conjunction_square_opposition_thief_known",
            2832:"owner_self_second_sixth_seventh",
            2848:"part_fortune_or_lord7_free_first_offence",
            2873:"age_methods_greatest_number_textual"}
        for n,kind in expect.items(): self.assertEqual(P[n]["source_record_kind"],kind)
    def test_365_capture_list_distinct_from_366(self):
        expect=["capture_seventh_lord_join_retrograde","capture_moon_from_seventh_to_conj_first","capture_moon_from_conj_first_toward_seventh","capture_sun_moon_seventh_join_or_behold","capture_seventh_lord_to_combustion","capture_first_lord_conjunction_angles_or_infortune_seventh"]
        self.assertEqual([P[n]["source_record_kind"] for n in range(2940,2946)],expect)
        self.assertTrue(all(P[n]["source_locator"]["pdf_pages"]==[399] for n in range(2940,2946)))
        self.assertEqual(P[2968]["source_locator"]["pdf_pages"],[400])
        self.assertIn("Mars",P[2968]["source_statement"])
    def test_unresolved_51_and_unique_ids(self):
        self.assertEqual(U["retained_count"],51)
        self.assertEqual(len(U["issues"]),51)
        self.assertEqual(len({x["id"] for x in U["issues"]}),51)
        self.assertEqual(U["issues"][-1]["id"],"U51")
    def test_original_table_witnesses_three_12rows(self):
        ts=D["original_table_witnesses"]
        self.assertEqual([len(t["rows"]) for t in ts],[12,12,12])
        self.assertEqual([t["source_pdf_page"] for t in ts],[398,399,399])
    def test_p360_erratum_kept_separate(self):
        e=get("ERRATA_COLLATION.json")["candidate_in_scope"][0]
        self.assertEqual((e["printed_page"],e["original_pdf_page"]),(360,394))
        self.assertFalse(e["read_word_or_glyph_verified"])
    def test_chapter_li_below_divider_not_transcribed(self):
        self.assertEqual(P[2974]["source_record_kind"],"chapter_li_boundary")
        self.assertEqual(P[2974]["chapter"],"L")
        self.assertIn("divider",P[2974]["source_statement"])
if __name__=="__main__":unittest.main()
