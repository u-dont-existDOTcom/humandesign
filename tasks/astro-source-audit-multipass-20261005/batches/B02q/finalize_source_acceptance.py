"""Promote B02q *documentary only* after actual source review and green tests.

This writes an isolated branch candidate; GitHub canonical integration is a
separate non-force, exact-head operation. Never interpret historical medicine
or the mathematical table as predictive/clinical evidence.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02q.md"
def rd(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
d=rd("RULES.json")
tests=rd("TEST_RUN_SUMMARY.json")
counts=rd("COUNTS.json")
review=rd("independent_review/FINAL_RECONCILIATION.json")
original=rd("RETAINED_LILLY_INDEX_BEFORE.json")
current=json.loads(INDEX.read_text())
unresolved=rd("UNRESOLVED.json")
original_source_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert counts["lilly_before"]==1793 and counts["new_documentary_records"]==58
assert len(d["rules"])==58 and [r["id"] for r in d["rules"]]==[f"LI.1647.II.XLVII.R{i}" for i in range(1794,1852)]
assert current==original and current["records_count"]==1793 and current["batches"][-1]["id"]=="B02p"
assert current["next"]["chapter"]=="XLVII"
assert sum(b["records_count"] for b in current["batches"])==1793
assert tests["successful"] and tests["failures"]==tests["errors"]==tests["skipped"]==0
assert tests["tests_run"]==tests["distinct_test_count"] and tests["tests_run"]>=42
assert tests["source_file_sha256"]["RULES.json"]==sha(B/"RULES.json")
assert tests["source_file_sha256"]["AUDIT_REPORT.md"]==sha(B/"AUDIT_REPORT.md")
assert rd("CLAIM_LEDGER.json")["report_sha256"]==sha(B/"AUDIT_REPORT.md")
assert unresolved["retained_count"]==len(unresolved["limits"])
assert rd("SOURCE_IDENTITY.json")["source_full_pdf_sha256"]==original_source_sha
assert rd("SOURCE_REPLAY_RECEIPT.json")["all_replayed_images_rgb_pixel_identical"]
assert rd("TABLE_GEOMETRY.json")["derived_coordinate_cells"]==480
assert review["source_images_read"] and review["source_rules_read"]==58
assert review["final_disposition"]=="SOURCE_FIDELITY_CORRECTIONS_RECONCILED"
assert (B/"independent_review/OPUS_INITIAL_DIAGNOSIS.md").stat().st_size>100
assert all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" and
           not x["case_evidence_countable"] and
           not x["clinical_efficacy_verified"] and
           not x["blinded_prospective_prediction"]
           for x in d["rules"])
assert all(counts[x]==0 for x in ["new_historical_patient_cases","new_original_patient_charts","independently_verified_patient_outcomes","preregistered_predictions"])
assert current["read_numbered_chapters"][-1]==46
current["read_numbered_chapters"].append(47)
current["read_headed_units_count"]+=1
current["records_count"]=1851
current["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLVII_SOURCE_READ_LATER_LILLY_OPEN"
current["batches"].append({
  "id":"B02q","path":"batches/B02q/RULES.json","records_count":58,
  "sha256":sha(B/"RULES.json"),
  "scope":"Lilly BookII.XLVII crisis and critical-day source doctrine. Original PDF324/printed290 below divider through PDF330/printed296 above divider; one original 30x16 table and editorial geometry, zero new verified patient outcomes."
})
current["next"]={
 "pdf_page":330,"printed_page":296,"chapter":"XLVIII",
 "heading":"If a Servant shall get free from his Master?",
 "include_opening_paragraph":True,
 "opening_anchor":"The first house, the Lord thereof, and the Moon, shall signifie the Servant",
 "position":"Original PDF330 below divider after Master Booker sentence; continue after page turn.",
 "extracted":False,"boundary_image_read":True}
current["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02q.md"
assert sum(q["records_count"] for q in current["batches"])==1851
assert current["runtime_promotions"]==current["empirical_validations"]==0
write(INDEX,current)
write(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",current)
acc={
 "batch":"B02q","accepted":True,"acceptance_kind":"Historical source-only documentary rule intake; no clinical or prediction validation",
 "rules_sha256":sha(B/"RULES.json"),
 "report_sha256":sha(B/"AUDIT_REPORT.md"),
 "test_summary_sha256":sha(B/"TEST_RUN_SUMMARY.json"),
 "claim_ledger_sha256":sha(B/"CLAIM_LEDGER.json"),
 "index_after_sha256":sha(INDEX),"original_source_pdf_sha256":original_source_sha,
 "source_pdf_pages":list(range(324,331)),"source_printed_pages":list(range(290,297)),
 "records":58,"first_record":"R1794","last_record":"R1851",
 "lilly_before":1793,"lilly_after_if_integrated":1851,"ptolemy_retained":1066,"combined_if_integrated":2917,
 "original_table_count":1,"printed_table_rows":30,"printed_table_columns":16,
 "editorial_geometry_cells_not_a_source_transcription":480,
 "distinct_new_patients":0,"source_dependent_worked_figures_not_new_patients":1,
 "independently_verified_outcomes":0,"preregistered_predictions":0,
 "clinical_or_predictive_validation":False,"runtime_promotion":False,
 "distinct_tests":tests["distinct_test_count"],"retained_issues":unresolved["retained_count"],
 "independent_source_review":"independent_review/OPUS_INITIAL_DIAGNOSIS.md",
 "reconciliation":"independent_review/FINAL_RECONCILIATION.json",
 "independent_review_did_not_certify":"Astrology truth, source ancient-author correctness, ephemeris parity, clinical effectiveness, or predictive validation",
 "next_chapter":"XLVIII","next_pdf_page":330,"next_record":"R1852"}
write(B/"ACCEPTANCE.json",acc)
STATE.write_text(
 "# Current astrology source audit — B02q (2026-10-12)\n\n"
 "**Documentary intake accepted, no predictive or clinical validation**: William Lilly's "
 "*Christian Astrology* (1647) Book II chapter XLVII 'Of the CRYSIS in Diseases', from "
 "original PDF324 printed290 below the divider through PDF330 printed296 above XLVIII. "
 "58 reference-only units R1794–R1851; cumulative Lilly **1,851**, retained Ptolemy "
 "**1,066**, combined **2,917**. Original source SHA256 "+original_source_sha+".\n\n"
 "Original text covers alternative crisis definitions, onset→urine specimen→doctor consultation "
 "hierarchy, lunar-radix/indicative/quadrature method, four hypothetical worked lunar examples "
 "from the previously counted July1645 figure, 30-by-16 source table, conditional benefic/infortune "
 "aspects, source medical/humoral sign/planet tables, and Master Booker boundary. "
 "The separately generated 480-cell geometry is editorial, not full source transcription. "
 "No new historical patient, verified medical outcome, frozen prediction or algorithm promotion. "
 f"All eight admitted page images match fresh RGB pixel renderings from the verified original. "
 f"Source review, final reconciled findings and {tests['distinct_test_count']} deterministic regression "
 "tests are in B02q/. Historic PASS_PLAN/CURRENT, previous accepted records, participant data, "
 "fitted models and prediction freezes remain untouched.\n\n"
 "**Next source:** chapter XLVIII, *If a Servant shall get free from his Master?*, beginning "
 "original PDF330/printed296 **below** the divider, next tentative R1852 after checking live index. "
 "Parent Lilly and multi-author source audit OPEN. Publication/archive/owner Downloads "
 "are separate verification boundaries: see B02q/PUBLICATION_RECEIPT.json, "
 "B02q/PACKET_USABILITY.json, and B02q/DELIVERY_RECEIPT.json when present.\n"
)
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02q source-fidelity accepted — publication and delivery gated\n\n"
 "All original PDF324–330/errata888 images reviewed/replayed; 58 reference-only"
 "records R1794–R1851 reconciled against independent source reader; "
 f"{tests['distinct_test_count']} distinct source/structural regressions PASS; "
 f"{unresolved['retained_count']} unresolved issues retained. Cumulative index candidate "
 "1793→1851 on isolated worktree only. The original 30x16 image is authoritative "
 "over the editorial 480-cell table geometry; clinical/predictive validity untested.\n\n"
 "Remaining: exact ZIP extraction and test replay; nonforce canonical GitHub "
 "integration with exact remote-head preflight; owner OS Downloads SHA-256 "
 "delivery; receipts. Parent astrology source study OPEN; next XLVIII PDF330 lower/R1852.\n"
)
write(B/"OWNER_OUTCOME_STATUS.json",{
 "parent":"ASTROLOGY-MULTIAUTHOR-SOURCE-COMPLETENESS","parent_status":"OPEN",
 "batch":"B02q","source_fidelity":"DOCUMENTARY_ACCEPTED_ONLY",
 "lilly_after_if_integrated":1851,"combined_after_if_integrated":2917,
 "independently_verified_patients_or_clinical_outcomes":0,
 "remaining":"Complete later Lilly and all other source authors; audit not a prospective performance test; publication/archive/delivery receipts separate."})
(B/"LESSON_DISPOSITION.md").write_text(
 "# B02q source-fidelity closeout\n\n"
 "- Preserve exact printed source and original-volume errata separately; no silent emendations.\n"
 "- Preserve three time anchors as hierarchy, not competing concurrent indications.\n"
 "- Original numeric table is primary; 480 generated grid cells are only editorial geometry.\n"
 "- Prior July1645 worked figure is hypothetical and does not create a new case or validated prediction.\n"
 "- Preserve the 'if ordained for life' escape condition and all brace-scoped historical purging claims.\n"
 "- Ancient author descriptions are Lilly-mediated, not independently verified ancient-source quotations.\n"
 "- No therapeutic or predictive inference may be promoted from documentary source indexing.\n"
 "- No universal promotion unless a new transferable lesson beyond existing UDA source-provenance rules is shown.\n"
)
print(json.dumps({"source_only_accepted":True,"lilly":1851,"combined":2917,"tests":tests["distinct_test_count"],"next":"XLVIII PDF330 lower"}))
