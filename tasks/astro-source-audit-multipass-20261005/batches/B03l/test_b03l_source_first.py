import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
L=J("CLAIM_LEDGER.json")
O=J("SOURCE_ORDER_DRAFT.json")
def validate(rows,spans):
    assert len(rows)==76 and len(spans)==19
    ids=[r["source_local_id"] for r in rows]
    assert ids==[f"LXVI-C{i:03}" for i in range(1,77)]
    refs=[key for s in spans for key in s["mapped_source_local_ids"]]
    assert len(refs)==76 and sorted(refs)==sorted(ids)
    assert all(s["original_pdf_pages"]==rows[ids.index(k)]["original_pdf_pages"]
               for s in spans for k in s["mapped_source_local_ids"])
    assert all(r["global_record_number"] is None and
               not r["historical_documentary_accepted"] and
               not r["case_independently_authenticated"] and
               not r["empirically_validated_astro_forecast"] and
               not r["runtime_rule_promoted"] for r in rows)
    assert all(r["original_printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
    assert all(set(r["original_pdf_pages"]).issubset({435,436,437,438}) for r in rows)
    assert all(r["chapter"]=="LXVI" for r in rows[:-2])
    assert all(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in rows[-2:])
    assert rows[0]["role"]=="heading" and rows[0]["original_pdf_pages"]==[435]
    assert rows[-1]["original_pdf_pages"]==[438]
    return True
class SourceFirst(unittest.TestCase):
    def test_bidirectional_source_mapping(self):
        self.assertTrue(validate(D["rows"],M["source_spans"]))
        self.assertEqual(O["ordered_local_ids"],[r["source_local_id"] for r in D["rows"]])
    def test_original_scan_integrity(self):
        self.assertEqual(W["original_source_body_pages"] if "original_source_body_pages" in W else W["original_source_body_pages"],[435,436,437,438])
        for i in W["original_images"]:
            b=(B/i["path"]).read_bytes()
            self.assertEqual(len(b),i["size_bytes"])
            self.assertEqual(hashlib.sha256(b).hexdigest(),i["sha256"])
    def test_original_source_pdf(self):
        self.assertEqual(D["original_full_pdf_sha256"],
          "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
    def test_chronology_literal_vs_historical_year(self):
        self.assertEqual(W["original_figure_date"],"17 April 1643")
        self.assertEqual(W["original_surrender_sentence_year"],"1644")
        self.assertEqual(W["historically_corrob_surrender_year"],"1643")
        self.assertEqual(L["surrender_forecast_days_late_as_admitted_by_author"],3)
        self.assertEqual(L["reported_negotiation_day_relative_to_chart"],8)
    def test_report_is_not_future_predicted_accuracy(self):
        text=" ".join(r["historical_author_paraphrase"]+" "+r["qualifications_ambiguity_scope"] for r in D["rows"]).lower()
        for phrase in ("three days after","negotiations","printed","1644","1643","eight days"):
            self.assertIn(phrase,text,phrase)
        self.assertEqual(L["new_empirical_predictive_validations"],0)
        self.assertFalse(D["source_case_outcome_independently_validated"])
    def test_non_obvious_counterfactual_lawsuit_preserved(self):
        text=" ".join(r["historical_author_paraphrase"]+" "+r["qualifications_ambiguity_scope"] for r in D["rows"]).lower()
        for key in ("lawsuit","plaintiff","defendant","judge","jury","saturn",
                    "priest","lawyer","context"):
            self.assertIn(key,text,key)
        self.assertEqual(L["hypothetical_lawsuit_real_outcomes_counted"],0)
    def test_three_page_crossings(self):
        cross=[s["original_pdf_pages"] for s in M["source_spans"] if len(s["original_pdf_pages"])>1]
        self.assertEqual(cross,[[435,436],[436,437],[437,438]])
        self.assertEqual(len(O["cross_page_ids"]),len([r for r in D["rows"] if len(r["original_pdf_pages"])>1]))
    def test_next_section_not_swallowed(self):
        self.assertEqual(len(O["next_section_navigation_only"]),2)
        self.assertEqual(D["rows"][-1]["chapter"],"LXVII_NAVIGATION_ONLY")
        self.assertTrue(all(x["original_pdf_pages"]==[438] for x in D["rows"][-2:]))
    def test_uncertainty_and_source_only_ledger(self):
        self.assertEqual(len(U["issues"]),23)
        self.assertEqual(L["previous_accepted_lilly"],3670)
        self.assertEqual(L["globally_accepted_new_units"],0)
        self.assertEqual(L["independently_reproduced_astro_prediction_accuracy_count"],0)
    def test_mutant_missing_source_detected(self):
        with self.assertRaises(AssertionError):validate(D["rows"][:-1],M["source_spans"])
    def test_mutant_duplicate_source_detected(self):
        bad=copy.deepcopy(M["source_spans"])
        bad[0]["mapped_source_local_ids"].append(bad[1]["mapped_source_local_ids"][0])
        with self.assertRaises(AssertionError):validate(D["rows"],bad)
    def test_mutant_false_empirical_flag_detected(self):
        bad=copy.deepcopy(D["rows"])
        bad[10]["empirically_validated_astro_forecast"]=True
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
    def test_mutant_wrong_date_page_detected(self):
        bad=copy.deepcopy(D["rows"])
        bad[4]["original_pdf_pages"]=[436]
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
    def test_mutant_navigation_leak_detected(self):
        bad=copy.deepcopy(D["rows"])
        bad[-1]["chapter"]="LXVI"
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
