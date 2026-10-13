"""Accept B02t phase1 documentary rules only after source readers + exact tests.

NO astro prediction validity. Adds a partial chapter L batch and source-position
handoff without marking numbered chapter50 complete. Publication and Downloads
are separate gates, requiring explicit readback receipts.
"""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02t_PHASE1.md"
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
assert not (B/"ACCEPTANCE.json").exists(),"Acceptance already written: inspect instead of replay"
D=rd("PHASE1_RULES_DRAFT.json")
R=D["rules"]
T=rd("TEST_RUN_SUMMARY.json")
C=rd("COUNTS.json")
U=rd("UNRESOLVED.json")
V=rd("independent_review/FINAL_RECONCILIATION.json")
S=rd("SOURCE_IDENTITY.json")
I=json.loads(IDX.read_text())
BEFORE=rd("RETAINED_LILLY_INDEX_BEFORE.json")
assert I==BEFORE and I["records_count"]==2137
assert I["next"]["chapter"]=="L" and I["next"]["pdf_page"]==353
assert I["batches"][-1]["id"]=="B02s" and I["read_numbered_chapters"][-1]==49
assert I["runtime_promotions"]==I["empirical_validations"]==0
assert D["record_count"]==len(R)>=162
assert [r["record_number"] for r in R]==list(range(2138,2138+len(R)))
assert all(r["source_full_pdf_sha256"]==SHA for r in R)
assert all(not r["case_evidence_countable"] and not r["independently_authenticated_outcome"] and
           not r["prospective_blind_prediction"] and not r["clinical_or_criminal_inference_verified"]
           for r in R)
assert all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in R)
assert all(r["source_locator"]["pdf_pages"] and max(r["source_locator"]["pdf_pages"])<=364 for r in R)
assert D["all_chapter_L_complete"] is False and C["all_chapter_l_complete"] is False
assert S["original_pdf_sha256"]==SHA
assert rd("SOURCE_REPLAY_RECEIPT.json")["all_rgb_pixel_identical"]
assert rd("SOURCE_REPLAY_RECEIPT.json")["images_pixel_replayed"]==19
assert len(rd("SOURCE_IMAGE_MANIFEST.json")["images"])==19
assert rd("ERRATA_COLLATION.json")["entries"][1]["replacement"]=="or"
assert U["retained_count"]==len(U["issues"])>=50
assert T["successful"] and T["failures"]==T["errors"]==T["skipped"]==0
assert T["tests_run"]==T["distinct_test_count"]>=233
assert T["source_file_sha256"]["PHASE1_RULES_DRAFT.json"]==H(B/"PHASE1_RULES_DRAFT.json")
assert T["source_file_sha256"]["AUDIT_REPORT.md"]==H(B/"AUDIT_REPORT.md")
assert rd("CLAIM_LEDGER.json")["report_sha256"]==H(B/"AUDIT_REPORT.md")
assert V["final_disposition"]=="CORRECTED_SOURCE_ONLY_ACCEPTABLE"
assert V["initial_fresh_image_first_windows"]==2
assert V["all_source_material_findings_reconciled"] is True
assert V["post_correction_source_readbacks_verified"] is True
assert V["new_prospective_verified_outcomes"]==0
for key,expected in (
 ("A","e30df2b3ce3e6f1b2088919fbb04cce899f392f532fae14944f43e44d719a6fc"),
 ("B","20de3a61ac25b299d7de909710c05b10201884497e54e260c5b80487635fa455")
):
 assert H(B/"independent_review"/f"OPUS_{key}_INITIAL.md")==expected
O=rd("SOURCE_ORDER.json")
assert len(O["ids"])==len(set(O["ids"]))==len(R)
assert set(O["ids"])=={x["record_number"] for x in R}
# Source text remains stable; acceptance is a separate canonical file.
src=rd("RULES.json")
assert src["rules"]==R
assert src["status"]=="REVIEWED_HISTORICAL_SOURCE_REFERENCE_ONLY_NOT_YET_ADMITTED"
assert T["source_file_sha256"]["RULES.json"]==H(B/"RULES.json")
last=2137+len(R)
I["records_count"]=last
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIX_PLUS_L_PHASE1_SOURCE_READ_L_REMAINDER_OPEN"
I["batches"].append({
 "id":"B02t","path":"batches/B02t/RULES.json",
 "records_count":len(R),"sha256":H(B/"RULES.json"),
 "scope":"Lilly Chapter L first phase only: original PDF353 below XLIX divider to PDF364 above 'Of a Thief and Theft'; remains chapter L incomplete. No cases validated."
})
# Deliberately DO NOT add 50 to read_numbered_chapters nor increment
# completed headed-unit count; the complete numbered chapter is still OPEN.
I["next"]={
 "pdf_page":364,"printed_page":330,"chapter":"L",
 "heading":"Of a Thief and Theft (continuation of Chapter L)",
 "include_opening_paragraph":True,"extracted":False,
 "boundary_image_read":True,
 "position":"Original PDF364 BELOW Of a Thief and Theft heading; do not recount first-phase Of a Woman flying from her Husband; complete Chapter L to PDF400 above LI."
}
I["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02t_PHASE1.md"
assert len(I["read_numbered_chapters"])==49
assert sum(x["records_count"] for x in I["batches"])==last
save(IDX,I)
save(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",I)
a={
 "batch":"B02t","phase":"1_OF_CHAPTER_L","accepted":True,
 "kind":"HISTORICAL_DOCUMENTARY_SOURCE_ONLY",
 "chapter_L_complete":False,
 "source_pdf_full_sha256":SHA,"source_pages_first_phase":list(range(353,365)),
 "candidate_unmodified_previous_records":2137,
 "new_documentary_units":len(R),"first_id":"R2138","last_id":f"R{last}",
 "lilly_before":2137,"lilly_after_if_integrated":last,
 "ptolemy_retained":1066,"combined_if_integrated":last+1066,
 "rules_sha256":H(B/"RULES.json"),"report_sha256":H(B/"AUDIT_REPORT.md"),
 "claim_ledger_sha256":H(B/"CLAIM_LEDGER.json"),
 "test_summary_sha256":H(B/"TEST_RUN_SUMMARY.json"),
 "index_after_sha256":H(IDX),
 "source_replay_original_images":19,"focused_documentary_tests":T["distinct_test_count"],
 "original_uncertainties_retained":U["retained_count"],
 "blind_independent_review_windows":2,
 "corrected_source_review":"independent_review/FINAL_RECONCILIATION.json",
 "no_actual_lost_goods_or_persons_verified":True,
 "independently_verified_cases":0,"prospective_frozen_predictions":0,
 "criminal_or_medical_validity":False,"runtime_promotions":0,
 "next_original_pdf_page":364,"next_source_heading":"Of a Thief and Theft",
 "next_candidate_record":f"R{last+1}"}
save(B/"ACCEPTANCE.json",a)
STATE.write_text(
 "# HumanDesign astrology source audit — B02t Phase1 (Chapter L still OPEN)\n\n"
 f"Original 1647 Lilly, Chapter L first-phase only (PDF353/printed319 below divider "
 f"through PDF364/printed330 above the separate *Of a Thief and Theft* heading), "
 f"{len(R)} source-only units R2138–R{last}. Cumulative Lilly **{last}**, retained "
 f"Ptolemy **1,066**, combined **{last+1066}**. This does not complete Chapter L, "
 "which ends original PDF400/printed366 above Chapter LI. "
 f"All 19 original page/errata images pixel replayed; {T['distinct_test_count']} unique "
 "documentary checks pass; source readbacks and unresolved evidence in B02t/. "
 "Zero independent outcome confirmations, prospective forecasts, participant data changes "
 "or runtime promotions.\n\n"
 "Next: *Of a Thief and Theft* begins original PDF364 below heading; next candidate "
 f"R{last+1}. Continue remainder of Chapter L through PDF400 ABOVE Chapter LI. "
 "No archive/GitHub publication or Downloads completion is implied by local acceptance; "
 "check separate post-acceptance receipts. Parent multi-author study OPEN.\n")
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02t source-only Phase1 accepted in isolated worktree; downstream delivery gated\n\n"
 f"{len(R)} source-only documentary units R2138–R{last}; prior accepted Lilly2137, "
 f"candidate after integration {last}; combined {last+1066}. Chapter L is only "
 "partially source-read; the theft subsection remains unextracted. "
 "Initial 2 independent image-first reviews plus corrected source readback admitted; "
 f"{T['distinct_test_count']} regression checks passed; "
 f"{U['retained_count']} uncertainties retained. \n\n"
 "Next: exact archive extraction and full test replay; nonforce canonical/source "
 "GitHub integration with exact-head preflight; owner Downloads SHA-256 delivery "
 "and receipts. After phase1, next source is PDF364 beneath Of a Thief and Theft, "
 f"tentative R{last+1}; continue to PDF400 above Chapter LI. Parent study OPEN.\n")
print(json.dumps({"source_documentary_accepted_locally":True,"records":len(R),
                  "candidate_lilly":last,"combined":last+1066,"tests":T["tests_run"],
                  "full_chapter_L_complete":False}))
