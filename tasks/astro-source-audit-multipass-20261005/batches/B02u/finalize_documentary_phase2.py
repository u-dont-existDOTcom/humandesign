"""Accept ONLY the second documentary part of Lilly Book II, Chapter L.

This is NOT independently verified crime, suspect, name, prognosis or astrology
science. Final GitHub/owner delivery is a separate post-local-acceptance gate.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02u_PHASE2.md"
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(path):return json.loads((B/path).read_text())
def SHA(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
assert not (B/"ACCEPTANCE.json").exists(),"Previously accepted; no blind replay"
D=rd("RULES.json")
T=rd("TEST_RUN_SUMMARY.json")
C=rd("COUNTS.json")
U=rd("UNRESOLVED.json")
REVIEW=rd("independent_review/FINAL_RECONCILIATION.json")
ORDER=rd("SOURCE_ORDER.json")
MAN=rd("SOURCE_IMAGE_MANIFEST.json")
REPLAY=rd("SOURCE_REPLAY_RECEIPT.json")
A=rd("A1_A2_RECONCILIATION.json")
BEFORE=rd("RETAINED_LILLY_INDEX_BEFORE.json")
idx=json.loads(INDEX.read_text())
assert idx==BEFORE and idx["records_count"]==2305 and idx["batches"][-1]["id"]=="B02t"
assert idx["next"]["chapter"]=="L" and idx["next"]["pdf_page"]==364
assert idx["read_numbered_chapters"][-1]==49 and 50 not in idx["read_numbered_chapters"]
assert idx["runtime_promotions"]==idx["empirical_validations"]==0
assert D["record_count"]==len(D["rules"])==267 and D["first_record"]=="R2306" and D["last_record"]=="R2572"
assert [r["record_number"] for r in D["rules"]]==list(range(2306,2573))
assert len(ORDER["source_order_record_ids"])==267
assert set(ORDER["source_order_record_ids"])=={x["record_number"] for x in D["rules"]}
assert ORDER["source_order_record_ids"][ORDER["source_order_record_ids"].index(2319)+1]==2572
assert C["candidate_source_documentary_units"]==267 and C["lilly_total_if_accepted"]==2572
assert C["combined_total_if_accepted"]==3638 and C["retained_ptolemy"]==1066
assert MAN["full_original_1647_sha256"]==SRC
assert REPLAY["all_rgb_identical"] and REPLAY["images_pixel_replayed"]==20
assert len(MAN["original_images"])==20
assert rd("SOURCE_IDENTITY.json")["full_1647_pdf_sha256"]==SRC
assert U["retained_count"]==len(U["issues"])==119
assert T["successful"] and T["tests_run"]==T["distinct_test_count"]>=314
assert T["failures"]==T["errors"]==T["skipped"]==0
for name in ["RULES.json","AUDIT_REPORT.md"]:
 assert T["source_file_sha256"][name]==SHA(B/name),name
assert rd("CLAIM_LEDGER.json")["report_sha256"]==SHA(B/"AUDIT_REPORT.md")
assert REVIEW["final_disposition"]=="DOCUMENTARY_SOURCE_FIDELITY_CONTROLLER_RECONCILED_WITH_RETAINED_AMBIGUITIES"
assert len(REVIEW["five_original_image_review_windows"])==5
assert REVIEW["all_five_initial_evaluators_found_issues"] is True
assert REVIEW["controller_source_correspondence_repaired"] is True
assert REVIEW["post_final_controller_change_new_blind_model_review"] is False
assert REVIEW["original_uncertainties_retained"]==119
for name in ("A1","A2","B","C","D"):
 r=next(x for x in REVIEW["five_original_image_review_windows"] if x["window"]==name)
 assert SHA(B/r["review_file"])==r["sha256"]
assert A["source_glyph_conflict_R2338"].startswith("Independent readers disagree")
assert all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in D["rules"])
assert all(not r["case_evidence_countable"] and
 not r["independently_authenticated_human_case"] and
 not r["prospective_frozen_prediction"] and
 not r["verified_crime_identification"] and
 not r["clinical_medical_or_criminal_use_authorized"] for r in D["rules"])
assert D["whole_chapter_l_complete"] is False and C["whole_chapter_l_complete"] is False
assert all(364<=p<=381 for r in D["rules"] for p in r["source_locator"]["pdf_pages"])
N=rd("NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json")
assert "BEFORE" in N["phase_current_stop"]
assert len(N["unextracted_next_phase_sections_pdf381"])>=5
assert not D["original_table_rows_diplomatically_transcribed"]
assert sum(x["records_count"] for x in idx["batches"])==2305
idx["records_count"]=2572
idx["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIX_PLUS_L_PHASE1_AND_THIEF_PHASE2_DOCUMENTED_L_REMAINDER_OPEN"
idx["batches"].append({
 "id":"B02u","path":"batches/B02u/RULES.json","records_count":267,
 "sha256":SHA(B/"RULES.json"),
 "scope":"Lilly Book II Chapter L SECOND phase, original PDF364 BELOW Of a Thief and Theft to PDF381 BEFORE Of the house of the Thiefe, 267 historical source units, 0 cases validated. Chapter L still incomplete."
})
idx["next"]={
 "pdf_page":381,"printed_page":347,"chapter":"L",
 "heading":"Of the house of the Thiefe, and the mark thereof",
 "include_opening_paragraph":True,
 "extracted":False,"boundary_image_read":True,
 "position":"Original PDF381 below Of the house of the Thiefe heading; PDF381 before heading already in B02u. Continue including Of the Door of the house and original PDF382 through PDF400 ABOVE Chapter LI; avoid overlap."
}
idx["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02u_PHASE2.md"
assert 50 not in idx["read_numbered_chapters"]
assert sum(x["records_count"] for x in idx["batches"])==2572
assert idx["runtime_promotions"]==idx["empirical_validations"]==0
save(INDEX,idx)
save(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",idx)
accept={
 "batch":"B02u","phase":"2_OF_CHAPTER_L","accepted":True,
 "kind":"HISTORICAL_SOURCE_DOCUMENTARY_ONLY",
 "chapter_L_complete":False,
 "source_full_pdf_sha256":SRC,
 "source_pages":list(range(364,382)),
 "next_source_in_same_original_page":381,
 "prior_accepted_lilly":2305,"new_documentary_units":267,
 "first_record":"R2306","last_record":"R2572",
 "lilly_after_if_integrated":2572,"retained_ptolemy":1066,
 "combined_after_if_integrated":3638,
 "rules_sha256":SHA(B/"RULES.json"),
 "report_sha256":SHA(B/"AUDIT_REPORT.md"),
 "source_review_sha256":SHA(B/"independent_review/FINAL_RECONCILIATION.json"),
 "claim_ledger_sha256":SHA(B/"CLAIM_LEDGER.json"),
 "focused_tests_summary_sha256":SHA(B/"TEST_RUN_SUMMARY.json"),
 "index_after_sha256":SHA(INDEX),
 "source_original_page_pixel_replay_count":20,
 "focused_source_tests":T["distinct_test_count"],
 "retained_textual_uncertainties":119,
 "initial_independent_source_image_review_windows":5,
 "post_controller_final_blind_evaluation":False,
 "original_six_planet_zodiac_classes_kept_distinct":True,
 "historical_illustration_not_human_observation":True,
 "independently_verified_criminal_cases":0,"verified_predictive_cases":0,
 "clinical_medical_or_criminal_validity":False,"runtime_promotions":0,
 "named_table_full_diplomatic_cells_accepted":False,
 "next_source_heading":"Of the house of the Thiefe, and the mark thereof",
 "next_pdf_page":381,"next_provisional_record":"R2573"
}
save(B/"ACCEPTANCE.json",accept)
STATE.write_text(
 "# Astrology source audit — Lilly B02u Chapter L Phase 2 locally accepted, parent OPEN\n\n"
 "Original William Lilly 1647, Chapter L second source section, PDF364 printed330 BELOW "
 "*Of a Thief and Theft* through PDF381 printed347 BEFORE *Of the house of the Thiefe*. "
 "Historical **documentary** source-only intake 267 units R2306–R2572. Cumulative "
 "**2,572 Lilly**, **1,066 retained Ptolemy**, **3,638 combined** after verified publication. "
 "Full chapter L still OPEN through PDF400 above Chapter LI; Chapter50 not marked complete.\n\n"
 f"20 original page images independently pixel-replayed from exact 1647 scan SHA256 {SRC}. "
 f"Five original-image reader windows returned source corrections; final controller corrections "
 "documented with one unresolved important glyph disagreement, 119 retained source uncertainties. "
 f"{T['distinct_test_count']} source-only tests passed. No current person, crime, forecast, "
 "clinical outcome or model improvement proven; human and forward-blind data untouched.\n\n"
 "Next phase starts original PDF381 at *Of the house of the Thiefe* heading, "
 "then *Of the Door of the house* continuing original PDF382. "
 "Next provisional source ID R2573. The 1647 printed name/color tables remain SOURCE IMAGE "
 "witnesses, not checked individual machine name-to-planet mapping. "
 "ZIP extracted replay, Git publication and owner Downloads are separate downstream gates; "
 "read B02u/PACKET_USABILITY.json, PUBLICATION_RECEIPT.json, DELIVERY_RECEIPT.json before claiming them.\n"
)
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02u original source phase 2 locally accepted; release/delivery not yet proven\n\n"
 "267 source-only historical text units R2306–R2572; prior Lilly2,305, candidate Lilly2,572 "
 "plus Ptolemy1,066 =3,638. Chapter L NOT complete. Five independent source-image first "
 "readers reviewed initial original text windows; some source statements corrected under "
 "documented uncertainty including a conflicting aspect glyph in original p332. "
 f"{T['distinct_test_count']} documentary tests PASS; 119 unresolved source textual matters retained. "
 "Next gates: ZIP CRC/manifest/real extraction and same tests replay, clean nonforce source/canonical "
 "GitHub pushes and remote readback, owner OS Downloads SHA256 delivery and receipts. "
 "Then continue on original PDF381 below *Of the house of the Thiefe* to PDF400 above Chapter LI.\n"
)
(B/"LESSON_DISPOSITION.md").write_text(
 "# B02u source-fidelity lessons\n\n"
 "- Five independent source-image first-reader windows exposed glyph errors and operator/actor losses. "
 "Independent readers' conflicting glyphs remain source uncertainty; not a reason to invent an aspect.\n"
 "- Preserve printed errata apart from handwritten margin and original body (p3?7 locator is unresolved).\n"
 "- A source reader's whole-PDF page request can exceed a phase stop placed at an original heading "
 "on that same page; hand off the excluded body as the next phase, do not double count or omit it.\n"
 "- Source table images are preserved, but symbolic human names/physical descriptions are NOT validated "
 "predictions of actual people and not fully diplomatic numerical cell data.\n"
 "- Existing UDA source-provenance and independent-evaluation separation already address these; no new "
 "portable universal rule claimed without external transfer justification.\n"
)
save(B/"OWNER_OUTCOME_STATUS.json",{
 "parent":"ASTROLOGY_MULTIAUTHOR_PRIMARY_SOURCE_COMPLETENESS",
 "status":"OPEN","batch":"B02u","documentary_phase2_accepted_locally":True,
 "whole_Chapter_L_complete":False,"new_units":267,
 "lilly_if_integrated":2572,"retained_ptolemy":1066,
 "combined_if_integrated":3638,
 "verified_predictions_or_crime_identifications":0,
 "next_source":"PDF381 Of the house of the Thiefe, original Chapter L to PDF400"
})
print(json.dumps({"locally_accepted":True,"new_units":267,"lilly":2572,
"combined":3638,"tests":T["distinct_test_count"],"next":"PDF381 Of the house of the Thiefe",
"chapter_L_complete":False}))
