"""U75 source-only regression. Extends historical U74 source checks without altering them.

This certifies selective original-reading repairs and provisional data
consistency, NOT independent diplomatic completeness or predictive efficacy.
"""
from pathlib import Path
import json,hashlib,unittest
import test_source_integrity_v17 as old

B=old.B
P=old.P
def load(f):return json.loads((B/f).read_text())
def sha(f):return hashlib.sha256((B/f).read_bytes()).hexdigest()

class CurrentV18(old.CurrentV17):
    def test_unresolved_53_and_unique_ids(self):
        u=load("UNRESOLVED_DRAFT.json")
        self.assertEqual(len(u["issues"]),75)
        self.assertEqual(u["retained_count"],75)
        self.assertEqual(len({x["id"] for x in u["issues"]}),75)
        self.assertEqual(u["issues"][-1]["id"],"U75")
    def test_explicit_moon_house_lord_to_moon_branch(self):
        r=P[2769]
        self.assertEqual(r["source_locator"]["pdf_pages"],[391])
        self.assertEqual(r["source_record_kind"],"part_fortune_and_moon_domicile_alternative_timing")
        self.assertIn("lord of the Moon's domicile applying to the Moon",r["source_statement"])
        self.assertIn("recovery",r["source_statement"])
        self.assertIn("OR original distinct branch",r["preconditions"][1])
        self.assertFalse(r["case_evidence_countable"])
        self.assertFalse(r["prospective_blinded_prediction"])
        self.assertEqual(sha("recovery/producer_p391_392_before_U75_moon_domicile_20261015.json"),
            "fbba3b6e146c582f04a58866330f5ae02e2ca48059416e318f08eb3868857492")
    def test_revised_p357_reverse_map_explicit_source_anchor(self):
        j=load("independent_review/REVERSE_SOURCE_TO_RECORD_P391_U75_20261015.json")
        self.assertEqual(j["number_of_mapped_source_anchors"],20)
        self.assertEqual(len([x for x in j["source_to_record"] if x["record_number"]==2769]),2)
        self.assertIn("Moon",j["source_to_record"][-2]["source_anchor_editorial_summary"] + j["source_to_record"][-3]["source_anchor_editorial_summary"])
        self.assertFalse(j["independent_diplomatic_source_completeness"])
    def test_bounded_402_source_records_review_map_exact(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U75_20261015.json")
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["distinct_bounded_review_records"],len(P))
        self.assertEqual(j["draft_sha256"],sha("RULES_DRAFT.json"))
        self.assertEqual([x["included_source_record_count"] for x in j["past_review_sets"]],[103,109,65,149])
        self.assertFalse(j["chapter_L_source_complete"])
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        for group in j["past_review_sets"]:
            for doc in group["review_evidence_documents"]:
                self.assertTrue((B/doc).is_file(),doc)
    def test_no_canonical_advance_or_glyph_guess(self):
        c=load("COUNTS.json")
        self.assertEqual(c["accepted_lilly_before"],2572)
        self.assertEqual(c["accepted_new_documentary_records"],0)
        self.assertFalse(load("RULES_DRAFT.json")["accepted"])
        e=load("ERRATA_COLLATION.json")["candidate_in_scope"][0]
        self.assertFalse(e["read_word_or_glyph_verified"])

if __name__=="__main__":unittest.main()
