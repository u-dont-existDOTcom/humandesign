import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
A=J("ACCEPTANCE.json")
U=J("UNRESOLVED.json")
L=J("CLAIM_LEDGER_ACCEPTED_LOCAL.json")
def validate_accepted(rows):
    assert len(rows)==186
    assert [r["record_number"] for r in rows]==list(range(3747,3933))
    assert [r["id"] for r in rows]==[f"R{i}" for i in range(3747,3933)]
    assert [r["source_local_id"] for r in rows]==[f"LXVII-C{i:03}" for i in range(1,187)]
    assert all(r["global_record_number"]==r["record_number"] and
               r["historical_documentary_accepted"] and
               not r["empirically_validated_astrology_prediction"] and
               not r["authenticated_individual_outcome"] and
               not r["usable_for_personal_death_or_health_judgment"] and
               not r["runtime_model_promoted"] for r in rows)
    assert all(r["chapter"]=="LXVII" for r in rows[:-2])
    assert all(r["chapter"]=="LXVIII_NAVIGATION_ONLY" for r in rows[-2:])
    return True
class DocumentaryAdmission(unittest.TestCase):
    def test_contiguous_source_ids_and_no_runtimes(self):
        self.assertTrue(validate_accepted(R["rules"]))
        self.assertEqual(R["record_count"],186)
        self.assertEqual(R["substantive_chapter_lxvii_units"],184)
        self.assertEqual(R["next_heading_navigation_units"],2)
    def test_pre_admission_draft_exact_preservation(self):
        for raw,final in zip(D,R["rules"],strict=True):
            for k in ("source_local_id","original_pdf_pages","original_printed_pages",
                      "chapter","role","short_editorial_anchor_not_full_transcript",
                      "historical_author_assertion_paraphrase",
                      "original_scope_exception_uncertainty"):
                self.assertEqual(raw[k],final[k],(raw["source_local_id"],k))
            self.assertIsNone(raw["global_record_number"])
            self.assertFalse(raw["historical_documentary_accepted"])
    def test_full_bijective_reverse_mapping(self):
        mapped=[i for s in M["source_spans"] for i in s["accepted_global_record_ids"]]
        self.assertEqual(sorted(mapped),sorted(r["id"] for r in R["rules"]))
        self.assertEqual(len(mapped),186)
        self.assertEqual(M["span_count"],38)
    def test_every_source_image_exact_hash(self):
        self.assertEqual(len(W["original_images"]),9)
        for im in W["original_images"]:
            self.assertEqual(H(im["path"]),im["sha256"])
            self.assertEqual((B/im["path"]).stat().st_size,im["bytes"])
    def test_frozen_accepted_file_hashes(self):
        for f,k in [("RULES.json","rules_sha256"),
          ("SOURCE_ORDER.json","source_order_sha256"),
          ("UNRESOLVED.json","unresolved_sha256"),
          ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","original_reverse_map_sha256"),
          ("CLAIM_LEDGER_ACCEPTED_LOCAL.json","claim_ledger_sha256"),
          ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","original_visual_audit_sha256")]:
            self.assertEqual(H(f),A[k],f)
    def test_source_only_case_counts(self):
        self.assertEqual(R["independent_absent_person_return_outcomes"],0)
        self.assertEqual(R["independent_lifespan_outcomes"],0)
        self.assertEqual(R["independent_spouse_death_order_outcomes"],0)
        self.assertEqual(R["independent_medical_cause_of_death_outcomes"],0)
        self.assertFalse(R["allowed_for_real_person_prediction"])
        self.assertEqual(A["new_empirically_validated_predictions"],0)
        self.assertEqual(A["runtime_model_promotions"],0)
    def test_predecessor_and_totals(self):
        self.assertEqual(A["prior_accepted_lilly"],3746)
        self.assertEqual(A["new_documentary_source_records"],186)
        self.assertEqual(A["lilly_if_published"],3932)
        self.assertEqual(A["combined_if_published"],4998)
        self.assertEqual(A["ptolemy_retained"],1066)
        self.assertFalse(A["remote_canonical_published"])
        self.assertEqual(A["next_numbered_chapter"],"LXVIII")
    def test_uncertainties_and_cross_pages(self):
        self.assertEqual(len(U["issues"]),31)
        self.assertEqual(R["retained_original_source_limits"],31)
        self.assertFalse(A["complete_independent_diplomatic_second_reader"])
        self.assertEqual(L["new_globally_accepted_source_units"],0)
        cross=[x["original_pdf_pages"] for x in M["source_spans"] if len(x["original_pdf_pages"])>1]
        self.assertEqual(cross,[[i,i+1] for i in range(438,446)])
    def test_mutants_detected(self):
        bad=copy.deepcopy(R["rules"])
        bad[4]["record_number"]=0
        with self.assertRaises(AssertionError):validate_accepted(bad)
        bad=copy.deepcopy(R["rules"])
        bad[25]["empirically_validated_astrology_prediction"]=True
        with self.assertRaises(AssertionError):validate_accepted(bad)
        bad=copy.deepcopy(R["rules"])
        bad[100]["usable_for_personal_death_or_health_judgment"]=True
        with self.assertRaises(AssertionError):validate_accepted(bad)
        bad=copy.deepcopy(R["rules"])
        bad[-1]["chapter"]="LXVII"
        with self.assertRaises(AssertionError):validate_accepted(bad)
if __name__=="__main__":unittest.main(verbosity=2)
