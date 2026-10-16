import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
O=J("SOURCE_ORDER_DRAFT.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
L=J("CLAIM_LEDGER.json")
SCOPE=J("SOURCE_WINDOW_PROVISIONAL.json")
def validate(rows,spans):
    assert len(rows)==186 and len(spans)==38
    ids=[r["source_local_id"] for r in rows]
    assert ids==[f"LXVII-C{i:03}" for i in range(1,187)]
    mapped=[k for s in spans for k in s["mapped_source_local_ids"]]
    assert len(mapped)==len(ids) and sorted(mapped)==sorted(ids)
    positions={r["source_local_id"]:r["original_pdf_pages"] for r in rows}
    assert all(s["original_pdf_pages"]==positions[k] for s in spans for k in s["mapped_source_local_ids"])
    assert all(r["original_printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
    assert all(r["global_record_number"] is None and
      r["source_original_1647_image_authority"] and
      not r["historical_documentary_accepted"] and
      not r["empirically_validated_astrology_prediction"] and
      not r["authenticated_individual_outcome"] and
      not r["usable_for_personal_death_or_health_judgment"] and
      not r["runtime_model_promoted"] for r in rows)
    assert all(r["chapter"]=="LXVII" for r in rows[:-2])
    assert all(r["chapter"]=="LXVIII_NAVIGATION_ONLY" and r["role"]=="next_navigation" for r in rows[-2:])
    assert rows[0]["original_pdf_pages"]==[438]
    assert rows[-1]["original_pdf_pages"]==[446]
    assert {p for s in spans for p in s["original_pdf_pages"]}==set(range(438,447))
    assert [s["original_pdf_pages"][0] for s in spans]==sorted(s["original_pdf_pages"][0] for s in spans)
    return True
class SourceFirst(unittest.TestCase):
    def test_full_source_to_draft_bijection(self):
        self.assertTrue(validate(D["rows"],M["source_spans"]))
        self.assertEqual(O["ordered_local_ids"],[r["source_local_id"] for r in D["rows"]])
        self.assertEqual(O["following_chapter_navigation_only"],[r["source_local_id"] for r in D["rows"][-2:]])
    def test_original_image_hashes_bitwise(self):
        self.assertEqual(len(W["original_images"]),9)
        for image in W["original_images"]:
            raw=(B/image["path"]).read_bytes()
            self.assertEqual(len(raw),image["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),image["sha256"])
        self.assertEqual([v["sha256"] for v in W["original_images"]],
           [v["sha256"] for v in SCOPE["images"]])
    def test_canonical_1647_source_and_predecessor(self):
        self.assertEqual(W["source_original_pdf_sha256"],
          "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
        self.assertEqual(W["previous_accepted_lilly"],3746)
        self.assertEqual(W["original_pdf_pages"],list(range(438,447)))
        self.assertEqual(W["next_numbered_chapter"],"LXVIII")
    def test_all_unnumbered_sections_present(self):
        heads=[r["short_editorial_anchor_not_full_transcript"].lower()
               for r in D["rows"] if r["role"]=="subheading"]
        expected=["whether one absent will return","the time when",
          "of the death of the querent","when, or about what time",
          "whether the man or wife","what manner of death"]
        self.assertTrue(all(any(term in h for h in heads) for term in expected),heads)
        self.assertEqual(len(heads),6)
    def test_cross_page_seams_preserved(self):
        crossings=[s["original_pdf_pages"] for s in M["source_spans"]
                   if len(s["original_pdf_pages"])>1]
        self.assertEqual(crossings,[[p,p+1] for p in range(438,446)])
        self.assertEqual(len(O["cross_page_ids"]),len([r for r in D["rows"] if len(r["original_pdf_pages"])>1]))
    def test_reception_and_absence_qualifiers_not_lost(self):
        text=" ".join(r["historical_author_assertion_paraphrase"]+" "+
                      r["original_scope_exception_uncertainty"] for r in D["rows"]).lower()
        for phrase in ["corroborating","without reception","benefic","applying",
                       "separat","eighth","does not","mutual reception"]:
            self.assertIn(phrase,text,phrase)
    def test_return_and_letter_separated(self):
        body=" ".join(r["historical_author_assertion_paraphrase"]+" "+r["original_scope_exception_uncertainty"] for r in D["rows"]).lower()
        for item in ["receiving news","reunion","long distances","short","surprise return"]:
            self.assertIn(item,body,item)
    def test_natal_priority_and_death_qualifiers(self):
        body=" ".join(r["historical_author_assertion_paraphrase"]+" "+r["original_scope_exception_uncertainty"] for r in D["rows"]).lower()
        for item in ["birth charts","first-house ruler","strong first lord",
                     "eighth","climacteric","fixed stars"]:
            self.assertIn(item,body,item)
    def test_no_real_person_or_medical_validation(self):
        self.assertEqual(L["source_narrated_independent_absent_person_outcomes"],0)
        self.assertEqual(L["observed_return_cases"],0)
        self.assertEqual(L["observed_lifespan_cases"],0)
        self.assertEqual(L["observed_spouse_mortality_comparison_cases"],0)
        self.assertEqual(L["independently_verified_clinical_or_death_predictions"],0)
        self.assertEqual(L["new_empirically_validated_astrological_outcomes"],0)
        self.assertFalse(L["individual_specific_health_or_absence_judgment_authorized"])
    def test_source_limit_inventory(self):
        self.assertEqual(len(U["issues"]),31)
        self.assertEqual(M["span_count"],38)
        self.assertEqual(D["source_units"],186)
        self.assertFalse(D["full_blind_diplomatic_transcription_done"])
    def test_mutant_duplicate_mapping_detected(self):
        bad=copy.deepcopy(M["source_spans"])
        bad[0]["mapped_source_local_ids"].append(bad[1]["mapped_source_local_ids"][0])
        with self.assertRaises(AssertionError):validate(D["rows"],bad)
    def test_mutant_missing_mapping_detected(self):
        bad=copy.deepcopy(M["source_spans"])
        bad[1]["mapped_source_local_ids"].pop()
        with self.assertRaises(AssertionError):validate(D["rows"],bad)
    def test_mutant_source_page_drift_detected(self):
        bad=copy.deepcopy(D["rows"]);bad[9]["original_pdf_pages"]=[440]
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
    def test_mutant_promoted_death_prediction_detected(self):
        bad=copy.deepcopy(D["rows"]);bad[80]["empirically_validated_astrology_prediction"]=True
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
    def test_mutant_personal_death_applicability_detected(self):
        bad=copy.deepcopy(D["rows"]);bad[145]["usable_for_personal_death_or_health_judgment"]=True
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
    def test_mutant_eighth_house_next_chapter_swallow_detected(self):
        bad=copy.deepcopy(D["rows"]);bad[-1]["chapter"]="LXVII"
        with self.assertRaises(AssertionError):validate(bad,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
