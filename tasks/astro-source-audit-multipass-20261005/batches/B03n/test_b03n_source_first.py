import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json")
def check(rows,spans):
    assert len(rows)==44 and len(spans)==11
    ids=[r["source_local_id"] for r in rows]
    assert ids==[f"LXVIII-C{i:03}" for i in range(1,45)]
    mapped=[k for s in spans for k in s["mapped_source_local_ids"]]
    assert len(mapped)==44 and sorted(mapped)==sorted(ids)
    assert all(s["original_pdf_pages"]==rows[ids.index(k)]["original_pdf_pages"] for s in spans for k in s["mapped_source_local_ids"])
    assert all(r["global_record_number"] is None and
               not r["documentary_admitted"] and
               not r["independent_wealth_outcome_authenticated"] and
               not r["validated_predictive_case"] and not r["runtime_model_promoted"] for r in rows)
    assert all(r["original_printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
    assert all(r["chapter"]=="LXVIII" for r in rows[:-1])
    assert rows[-1]["chapter"]=="LXIX_NAVIGATION_ONLY" and rows[-1]["original_pdf_pages"]==[448]
    return True
class SourceFirst(unittest.TestCase):
    def test_bijective_source_mapping(self):
        self.assertTrue(check(D["rows"],M["source_spans"]))
        self.assertEqual(M["span_count"],11)
    def test_original_image_integrity(self):
        self.assertEqual(len(W["images"]),3)
        for i in W["images"]:
            b=(B/i["path"]).read_bytes()
            self.assertEqual(len(b),i["bytes"])
            self.assertEqual(hashlib.sha256(b).hexdigest(),i["sha256"])
    def test_source_boundaries(self):
        self.assertEqual(W["prior_accepted_lilly"],3932)
        self.assertEqual(W["next_chapter"],"LXIX")
        self.assertEqual(W["next_original_pdf_page"],448)
        self.assertEqual(M["source_spans"][2]["original_pdf_pages"],[446,447])
    def test_payment_and_amount_alternatives(self):
        t=" ".join(r["historical_author_paraphrase"]+" "+r["conditions_scope_and_uncertainty"] for r in D["rows"]).lower()
        for word in ["combust","retrograd","trine","sextile","square","opposition","reception","delayed","adequate"]:
            self.assertIn(word,t,word)
    def test_negative_payment_and_fraud_not_overclaimed(self):
        t=" ".join(r["historical_author_paraphrase"] for r in D["rows"]).lower()
        self.assertIn("difficulty",t)
        self.assertIn("nonpayment",t)
        self.assertIn("general rules cannot always be certain",t)
        self.assertEqual(C["independently_authenticated_dowry_receipts"],0)
        self.assertEqual(C["independently_verified_person_fraud_cases"],0)
    def test_source_limits(self):
        self.assertEqual(len(U["issues"]),15)
        self.assertEqual(C["empirical_astrology_predictions_validated"],0)
        self.assertEqual(C["new_globally_accepted_source_units"],0)
    def test_mutant_wrong_next_chapter(self):
        bad=copy.deepcopy(D["rows"]);bad[-1]["chapter"]="LXVIII"
        with self.assertRaises(AssertionError):check(bad,M["source_spans"])
    def test_mutant_false_independent_case(self):
        bad=copy.deepcopy(D["rows"]);bad[4]["independent_wealth_outcome_authenticated"]=True
        with self.assertRaises(AssertionError):check(bad,M["source_spans"])
    def test_mutant_page_drift(self):
        bad=copy.deepcopy(D["rows"]);bad[15]["original_pdf_pages"]=[446]
        with self.assertRaises(AssertionError):check(bad,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
