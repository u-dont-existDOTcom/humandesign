"""Persist independently sourced review history and controller reconciliation.
No new blind claim: the two changed-item reviews evaluated an earlier candidate.
"""
from pathlib import Path
import hashlib,json,shutil
B=Path(__file__).resolve().parent
Q=B/"independent_review"
RAW=Path(__import__("os").environ.get("LILLY_REVIEW_STAGING_DIR", str(Path.home()/"ai-source-review")))
assert not (Q/"FINAL_RECONCILIATION.json").exists(), "Reconciliation exists; inspect it"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
orig={"A":"2e59d1e474c45fb1b675368f76dd99ecd9d8250ba68f4a5f45549f508490da06",
      "B":"4668fea44ab93f074b3c58b059c05836f8cf6d619c1c575994d4e3a589b56f1d"}
review=[]
for key in ("A","B"):
    initial=Q/f"OPUS_{key}_INITIAL.md"
    assert initial.is_file() and sha(initial)==orig[key]
    original=RAW/f"b02s-changed-{key.lower()}-20261013"
    assert (original/"review.exit").read_text().strip()=="0"
    changed=Q/f"CHANGED_{key}_DIAGNOSIS.md"
    assert sha(changed)==sha(original/"review.stdout")
    target=Q/f"OPUS_{key}_CHANGED.md"
    assert not target.exists()
    shutil.copy2(changed,target)
    review.append({
     "window":key,
     "original_first_review_sha256":sha(initial),
     "informed_changed_item_review_sha256":sha(changed),
     "original_source_image_pdf_window":[336,345] if key=="A" else [344,353],
     "changed_review_exit":0,
     "changed_review_interim_verdict":"REPAIR_REQUIRED",
     "review_type":"INFORMED_FOLLOWUP_NOT_NEW_BLIND",
     "original_report":f"OPUS_{key}_INITIAL.md",
     "changed_report":target.name
    })
T=json.loads((B/"TEST_RUN_SUMMARY.json").read_text())
D=json.loads((B/"RULES.json").read_text())
U=json.loads((B/"UNRESOLVED.json").read_text())
assert D["record_count"]==len(D["rules"])==217
assert U["retained_count"]==len(U["limits"])==68
assert T["successful"] and T["tests_run"]==T["distinct_test_count"]==281
mat=[
  {"pages":"p308","record":"R1992","finding":"gendered person-description roles reversed","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p309–310","record":"R2010","finding":"moon in fall/bad aspect plus ascendant beholding omitted by earlier repair","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p310","record":"R2009","finding":"Saturn omitted from ascendant planets","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p303","record":"R1931","finding":"and Moon likewise incorrectly narrowed to dignity only","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p309","record":"R2007","finding":"seventh lord angular and may strive, non-angular fallback separate","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p310","record":"R2021","finding":"heavy ponderous receiver misread as heavily afflicted","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p305","record":"R1952","finding":"in seventh especially domicile mistaken as alternatives","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p304","record":"R1945","finding":"Moon in seventh marriage completion branch absent","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p315","record":"R2064","finding":"explicit denial of other man's subjugation replaced with invented guilt","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p313","record":"R2120","finding":"deceived vs accused actions conflated; Mars substitution misrepresented","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p313","record":"R2119","finding":"fixed angles and still tempted source conditions dropped","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p315","record":"R2067,R2126","finding":"Mars AS seventh lord misread as with seventh lord","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p316","record":"R2075","finding":"Dragon Head same conclusion omitted","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p315","record":"R2066","finding":"past attachment before she knew husband omitted","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p347 printed313","record":"R2047","finding":"printed false-rumour denial and gave-no-credit clause restored","disposition":"CONTROLLER_REPAIRED"},
  {"pages":"p318","record":"R2137","finding":"also resolves mistress/sweetheart question omitted","disposition":"CONTROLLER_ADDED_SOURCE_SCOPE"},
  {"pages":"p305,306,307,312,315","record":"ERRATA_COLLATION","finding":"print/editorial errata and later marginalia previously conflated","disposition":"SOURCE_QUALIFIED_UNRESOLVED_PRINT_DETAILS"}
]
doc={
 "batch":"B02s",
 "final_source_status":"ACCEPTABLE_DOCUMENTARY_ONLY",
 "initial_source_review_windows":2,
 "changed_item_review_windows":2,
 "source_window_coverage":[336,353],
 "reviewed_original_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "source_images_with_errata":19,
 "all_material_findings_reconciled":True,
 "technical_source_review_not_prospective_validation":True,
 "initial_results_not_overwritten":True,
 "changed_review_results_not_overwritten":True,
 "informed_followups_not_blind":True,
 "post_final_repair_third_independent_blind_review":False,
 "controller_verified_source_fix_after_followups":True,
 "review_windows":review,
 "material_changed_findings":mat,
 "unchanged_source_ambiguities":"68 source/extraction limits in UNRESOLVED.json including original catchword/glyph ambiguity, assent contradictory wording and gendered source classifications.",
 "accepted_source_records_candidate":217,
 "first_record":"R1921","last_record":"R2137",
 "last_source_tests":281,
 "independently_observed_couples":0,
 "successful_prospective_predictions":0,
 "source_review_note":"The changed-item reviewer reports say REPAIR_REQUIRED for the earlier versions; this controller repaired them against original pages. That is not an independent model readback of the final files."
}
(Q/"FINAL_RECONCILIATION.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"final_status":doc["final_source_status"],"source_windows":4,"initial_independent":2,"informed":2,
                  "record_count":217,"material_dispositions":len(mat),
                  "tests":281,"limits":68}))
