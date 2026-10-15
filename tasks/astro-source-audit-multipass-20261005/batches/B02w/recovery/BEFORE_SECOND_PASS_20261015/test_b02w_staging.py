"""B02w: primary-source documentary staging checks, not empirical validation.

This suite verifies exact original image hashes, source-boundary separation,
record and condition integrity, editorial uncertainty, and unchanged
accepted Lilly predecessor. It does NOT independently re-read the 1647 pages.
"""
import unittest,json,hashlib
from pathlib import Path
from collections import Counter

B=Path(__file__).resolve().parent
def read(name):return json.loads((B/name).read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
D=read("RULES_DRAFT.json")
S=read("SOURCE_FIRST_CLAUSES_DRAFT.json")
W=read("SOURCE_WINDOW_MANIFEST.json")
O=read("SOURCE_ORDER_DRAFT.json")
U=read("UNRESOLVED_DRAFT.json")
BASE=read("RETAINED_LILLY_INDEX_BEFORE_B02w.json")
REC=D["records"]
BY_KIND={r["source_record_kind"]:r for r in REC}
BY_NUM={r["record_number"]:r for r in REC}

class ChapterLIProvisionalIntegrity(unittest.TestCase):
 def test_original_accepted_baseline_is_fixed(self):
  self.assertEqual(BASE["records_count"],2974)
  self.assertEqual(BASE["batches"][-1]["id"],"B02v")
  self.assertEqual(BASE["next"]["chapter"],"LI")
  self.assertEqual(BASE["next"]["pdf_page"],400)
  self.assertEqual(D["previous_accepted_lilly"],2974)
  self.assertEqual(D["ptolemy_retained"],1066)

 def test_provisional_never_accepted_or_empirical(self):
  self.assertFalse(D["accepted"])
  self.assertEqual(D["newly_accepted_documentary_records"],0)
  self.assertFalse(D["historical_predictive_accuracy_validated"])
  self.assertFalse(D["original_to_record_completeness_proven"])
  self.assertFalse(D["independent_semantic_source_review_complete"])
  self.assertTrue(all(not r["case_evidence_countable"] and not r["prospective_blinded_prediction"] for r in REC))
  self.assertTrue(all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in REC))

 def test_source_image_witnesses_hashed(self):
  self.assertEqual([x["original_pdf_page"] for x in W["source_images"]],[400,401,402,403])
  for item in W["source_images"]:
   p=item["path"]
   self.assertEqual((B/p).stat().st_size,item["bytes"])
   self.assertEqual(sha(p),item["sha256"])
  # This source-side PDF400 is exactly the accepted B02v original witness.
  q=B.parent/"B02v/evidence/pdf-400.png"
  if q.exists():self.assertEqual(sha("evidence/pdf-400.png"),hashlib.sha256(q.read_bytes()).hexdigest())

 def test_original_full_pdf_identity_grounded_to_previous_receipt(self):
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
  self.assertEqual(D["original_source_pdf_sha256"],W["original_full_pdf_sha256"])
  self.assertEqual(W["source_image_originals_preserved"],True)

 def test_physical_source_window_and_next_heading(self):
  self.assertEqual((W["opening"]["pdf_page"],W["opening"]["printed_page"]),(400,366))
  self.assertIn("BELOW",W["opening"]["position"])
  self.assertEqual(W["closing"]["last_chapter_LI_pdf_page"],402)
  self.assertEqual(W["closing"]["last_chapter_LI_printed_page"],368)
  self.assertEqual(W["closing"]["next_heading_pdf_page"],403)
  self.assertIn("CHAP. LII",W["closing"]["next_heading"])
  self.assertFalse(W["includes_any_chapter_LII_body"])
  self.assertFalse(W["includes_any_chapter_L_above_divider"])

 def test_42_contiguous_unique_documentary_units(self):
  self.assertEqual(len(REC),42)
  self.assertEqual([x["record_number"] for x in REC],list(range(2975,3017)))
  self.assertEqual(len(BY_KIND),42)
  self.assertEqual(len(BY_NUM),42)
  self.assertEqual([x["id"] for x in REC],[f"LI.1647.II.LI.R{i}" for i in range(2975,3017)])
  self.assertEqual(len(S["rows"]),len(REC))
  self.assertEqual([x["local_id"] for x in S["rows"]],[f"LI-C{i:03}" for i in range(1,43)])

 def test_original_page_locators_correct_for_every_unit(self):
  for r in REC:
   pages=r["source_locator"]["pdf_pages"]
   self.assertEqual(r["source_locator"]["printed_pages"],[p-34 for p in pages])
   self.assertEqual(r["source_locator"]["page_images"],[f"evidence/pdf-{p}.png" for p in pages])
   self.assertTrue(all(p in (400,401,402,403) for p in pages))
   self.assertTrue(r["source_locator"]["original_image_is_authoritative"])
  self.assertEqual(O["source_pages_including_boundary"],[400,401,402,403])

 def test_chapter_LII_is_boundary_only(self):
  r=REC[-1]
  self.assertEqual(r["source_record_kind"],"chapter_lii_boundary")
  self.assertEqual(r["source_record_role"],"boundary")
  self.assertEqual(r["source_locator"]["pdf_pages"],[403])
  self.assertTrue(all(x["source_record_role"]!="boundary" for x in REC[:-1]))
  self.assertTrue(all(403 not in x["source_locator"]["pdf_pages"] for x in REC[:-1]))

 def test_cross_leaf_conditions(self):
  self.assertEqual(O["cross_page_record_ids"],[2978,2999])
  self.assertEqual(BY_NUM[2978]["source_locator"]["pdf_pages"],[400,401])
  self.assertEqual(BY_NUM[2999]["source_locator"]["pdf_pages"],[401,402])
  self.assertIn("separated",BY_KIND["contest_querent_significator_assignment"]["source_statement"])
  self.assertIn("applies",BY_KIND["contest_opponent_significator_assignment"]["source_statement"])

 def test_source_role_separation(self):
  kinds=[r["source_record_kind"] for r in REC]
  self.assertIn("war_dangerous_voyage_return_heading",kinds)
  self.assertIn("war_return_safe_heading",kinds)
  self.assertIn("what_will_ensue_war_heading",kinds)
  self.assertIn("war_side_houses_querent_marginal",kinds)
  self.assertIn("war_side_houses_opponent_marginal",kinds)
  self.assertEqual(D["original_chapter_LI_body_pages"],[400,401,402])

 def test_original_logical_and_or_categories(self):
  r=BY_KIND["war_safe_return_first_lord_good_or_good_in_asc"]
  self.assertIn(" OR ",r["preconditions"][0])
  r=BY_KIND["war_result_benefic_first_malefic_seventh_strong_first"]
  self.assertIn(" AND ",r["preconditions"][0])
  r=BY_KIND["war_malefic_with_first_benefic_in_first_loss_wound_not_death"]
  self.assertIn("not death",r["source_statement"].lower())
  r=BY_KIND["war_result_both_lords_first_benefic_first_malefic_seventh_both_loss"]
  self.assertIn("loss for both",r["source_statement"])
  r=BY_KIND["war_result_both_lords_first_benefics_second_cusp"]
  self.assertIn("CUSP",r["preconditions"][0])

 def test_abbreviated_converses_remain_unexpanded(self):
  rs=[r for r in REC if r["source_record_role"]=="converse"]
  self.assertEqual(len(rs),6)
  self.assertTrue(all(r["preconditions"]==[] for r in rs))
  self.assertTrue(all(r["exceptions_and_evidence_limits"] for r in rs))
  self.assertTrue(all(not r["source_locator"]["source_statement_is_verbatim"] for r in rs))

 def test_retained_uncertainties_and_not_clinical(self):
  self.assertEqual(U["retained_count"],11)
  self.assertEqual(len(U["issues"]),11)
  self.assertEqual(len(set(x["id"] for x in U["issues"])),11)
  self.assertTrue(all(x["id"].startswith("LI-U") for x in U["issues"]))
  self.assertFalse(U["any_retroactive_chart_score_change"])

 def test_original_to_draft_traceability_exact(self):
  src={r["local_id"]:r for r in S["rows"]}
  for r in REC:
   original=src[r["draft_origin_local_id"]]
   self.assertEqual(r["source_statement"],original["source_statement"])
   self.assertEqual(r["source_record_kind"],original["kind"])
   self.assertEqual(r["preconditions"],original["preconditions"])
   self.assertEqual(r["exceptions_and_evidence_limits"],original["exceptions_and_uncertainty"])
   self.assertFalse(original["accepted"])

 def test_upstream_hashes_recompute(self):
  self.assertEqual(D["source_window_manifest_sha256"],sha("SOURCE_WINDOW_MANIFEST.json"))
  for file,digest in O["upstream_sha256"].items():
   self.assertEqual(sha(file),digest)

 def test_no_canonical_promotion_or_failed_mission(self):
  self.assertEqual(D["previous_accepted_lilly"],2974)
  self.assertEqual(D["provisional_new_units"],42)
  self.assertEqual(D["lilly_if_accepted_not_current"],3016)
  self.assertEqual(D["combined_if_accepted_not_current"],4082)
  self.assertEqual(D["newly_accepted_documentary_records"],0)
  self.assertFalse(O["independent_full_fidelity_review"])

if __name__=="__main__": unittest.main()
