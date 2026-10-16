import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED.json")
L=J("CLAIM_LEDGER_ACCEPTED_LOCAL.json")
def validate(rows):
    assert len(rows)==76
    assert [r["record_number"] for r in rows]==list(range(3671,3747))
    assert [r["id"] for r in rows]==[f"R{i}" for i in range(3671,3747)]
    assert [r["source_local_id"] for r in rows]==[f"LXVI-C{i:03}" for i in range(1,77)]
    assert all(r["global_record_number"]==r["record_number"] and
        r["historical_documentary_accepted"] and
        not r["case_independently_authenticated"] and
        not r["empirically_validated_astro_forecast"] and
        not r["runtime_rule_promoted"] for r in rows)
    assert all(r["chapter"]=="LXVI" for r in rows[:-2])
    assert all(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in rows[-2:])
    return True
class DocumentaryAdmission(unittest.TestCase):
    def test_new_ids_and_documentary_only(self):self.assertTrue(validate(R["rules"]))
    def test_original_draft_exact_survives(self):
        for old,new in zip(D,R["rules"],strict=True):
            for k in ("source_local_id","role","original_pdf_pages","original_printed_pages",
                      "historical_author_paraphrase","qualifications_ambiguity_scope","chapter"):
                self.assertEqual(old[k],new[k],(old["source_local_id"],k))
            self.assertIsNone(old["global_record_number"])
            self.assertFalse(old["historical_documentary_accepted"])
    def test_bijective_source_to_accepted(self):
        ids=[i for sp in M["source_spans"] for i in sp["canonical_record_ids"]]
        self.assertEqual(len(ids),76)
        self.assertEqual(sorted(ids),sorted(r["id"] for r in R["rules"]))
        self.assertEqual(M["span_count"],19)
        self.assertEqual(R["substantive_lxvi_annotations"],74)
    def test_four_authoritative_original_images(self):
        for im in W["original_images"]:
            self.assertEqual(H(im["path"]),im["sha256"])
            self.assertEqual((B/im["path"]).stat().st_size,im["size_bytes"])
    def test_source_hash_receipts(self):
        for f,k in [("RULES.json","rules_sha256"),
           ("SOURCE_ORDER.json","source_order_sha256"),
           ("UNRESOLVED.json","unresolved_sha256"),
           ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_source_map_sha256"),
           ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","visual_audit_sha256")]:
            self.assertEqual(H(f),A[k],f)
    def test_original_date_discrepancy_unchanged(self):
        self.assertEqual(A["original_chart_date"],"17 April 1643")
        self.assertEqual(A["original_literal_surrender_year"],"1644")
        self.assertEqual(A["historically_corrob_surrender_year"],"1643")
        self.assertTrue(A["surrender_three_days_late_as_author_says"])
        self.assertTrue(A["negotiations_near_deadline_not_identical_to_capture"])
        self.assertTrue(L["reported_1644_typographic_year_marked_not_repaired"])
    def test_no_independent_siege_or_lawsuit_cases(self):
        self.assertEqual(R["independently_validated_predictive_cases"],0)
        self.assertEqual(R["hypothetical_lawsuits_empirically_observed"],0)
        self.assertEqual(A["new_empirical_predictions_validated"],0)
        self.assertEqual(A["runtime_promotions"],0)
    def test_prior_count_then_canonical_proposal(self):
        self.assertEqual(A["previous_lilly_accepted"],3670)
        self.assertEqual(A["new_documentary_records"],76)
        self.assertEqual(A["lilly_if_published"],3746)
        self.assertEqual(A["combined_if_published"],4812)
        self.assertEqual(len(U["issues"]),23)
        self.assertFalse(A["canonical_published"])
    def test_mutant_premature_empirical_promoted_rejected(self):
        bad=copy.deepcopy(R["rules"])
        bad[20]["empirically_validated_astro_forecast"]=True
        with self.assertRaises(AssertionError):validate(bad)
    def test_mutant_wrong_record_id_rejected(self):
        bad=copy.deepcopy(R["rules"])
        bad[0]["record_number"]=0
        with self.assertRaises(AssertionError):validate(bad)
    def test_mutant_lawsuit_relabelled_next_chapter_rejected(self):
        bad=copy.deepcopy(R["rules"])
        bad[60]["chapter"]="LXVII_NAVIGATION_ONLY"
        with self.assertRaises(AssertionError):validate(bad)
    def test_mutant_navigation_swallowed_rejected(self):
        bad=copy.deepcopy(R["rules"])
        bad[-1]["chapter"]="LXVI"
        with self.assertRaises(AssertionError):validate(bad)
if __name__=="__main__":unittest.main(verbosity=2)
