"""B02p source-only acceptance and cumulative-index candidate. Does not publish."""
from pathlib import Path
import json, hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02p.md"
def rd(n): return json.loads((B/n).read_text())
def hashfile(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
rule=rd("RULES.json"); tests=rd("TEST_RUN_SUMMARY.json")
counts=rd("COUNTS.json");cases=rd("CASE_EVIDENCE.json")
review=rd("independent_review/FINAL_RECONCILIATION.json")
before=rd("RETAINED_LILLY_INDEX_BEFORE.json")
ix=json.loads(IDX.read_text())
assert len(rule["rules"])==24 and rule["record_count"]==24
assert [r["id"] for r in rule["rules"]]==[f"LI.1647.II.XLVI.R{i}" for i in range(1770,1794)]
assert ix["records_count"]==before["records_count"]==counts["lilly_before"]==1769
assert ix["batches"][-1]["id"]=="B02o" and sum(b["records_count"] for b in ix["batches"])==1769
assert tests["successful"] and tests["tests_run"]==tests["distinct_test_count"]==60
assert tests["failures"]==tests["errors"]==tests["skipped"]==0
assert tests["source_file_sha256"]["RULES.json"]==hashfile(B/"RULES.json")
assert tests["source_file_sha256"]["AUDIT_REPORT.md"]==hashfile(B/"AUDIT_REPORT.md")
assert len(review["second_review_findings_reconciled"])==13 and review["independent_final_third_pass"]==False
assert cases["independent_outcome_verification"]==False and cases["count_as_validated_prediction"]==False
assert all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in rule["rules"])
u=rd("UNRESOLVED.json")
assert u["retained_count"]==len(u["limits"])==40
assert rd("CLAIM_LEDGER.json")["report_sha256"]==hashfile(B/"AUDIT_REPORT.md")
assert [p.name for p in sorted((B/"evidence").glob("pdf-3*.png"))]==["pdf-323.png","pdf-324.png"]
ix["records_count"]=1793
ix["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLVI_SOURCE_READ_LATER_LILLY_OPEN"
assert ix["read_numbered_chapters"][-1]==45
ix["read_numbered_chapters"].append(46)
ix["read_headed_units_count"]+=1
ix["batches"].append({
 "id":"B02p", "path":"batches/B02p/RULES.json","records_count":24,
 "sha256":hashfile(B/"RULES.json"),
 "scope":"Book II XLVI July1645 illness judgement original PDF323/printed289 through PDF324/printed290 ABOVE divider; one horoscope, 24 documentary units, one author-reported death, zero verified outcomes."})
ix["next"]={
 "pdf_page":324, "printed_page":290, "chapter":"XLVII",
 "heading":"Of the CRYSIS in Diseases",
 "include_opening_paragraph":True,
 "opening_anchor":"CRYSIS is no other thing then a duell or contention betwixt nature and the infirmity",
 "position":"Below divider on PDF324, continue onto PDF325 without omitting page-crossing text.",
 "extracted":False,"boundary_image_read":True}
ix["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02p.md"
assert sum(b["records_count"] for b in ix["batches"])==1793
assert ix["runtime_promotions"]==ix["empirical_validations"]==0
save(IDX,ix)
save(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",ix)
accept={
 "batch":"B02p","accepted":True,
 "kind":"historical source text/documentary intake only; no clinical or prediction validation",
 "source_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "original_pdf_pages":[323,324],"printed_pages":[289,290],
 "rules_sha256":hashfile(B/"RULES.json"),
 "report_sha256":hashfile(B/"AUDIT_REPORT.md"),
 "test_summary_sha256":hashfile(B/"TEST_RUN_SUMMARY.json"),
 "claim_ledger_sha256":hashfile(B/"CLAIM_LEDGER.json"),
 "index_after_sha256":hashfile(IDX),
 "records":24,"first_record":"R1770","last_record":"R1793",
 "lilly_before":1769,"lilly_after_if_integrated":1793,
 "ptolemy_retained":1066,"combined_if_integrated":2859,
 "source_patients":1,"source_charts":1,"independently_verified_outcomes":0,
 "clinical_or_predictive_validation":False,"runtime_promotion":False,
 "distinct_tests":60,"retained_issues":40,
 "initial_independent_review":"independent_review/OPUS_INITIAL_DIAGNOSIS.md",
 "changed_review_diagnosis":"SECOND_REVIEW_OPEN_FINDINGS_20261012.md",
 "finding_reconciliation":"independent_review/FINAL_RECONCILIATION.json",
 "third_independent_model_readback_after_final_repair":False,
 "next_chapter":"XLVII","next_pdf_page":324,"next_id":"R1794"}
save(B/"ACCEPTANCE.json",accept)
STATE.write_text(
 "# Current astrology source audit — B02p (2026-10-12)\n\n"
 "Accepted as historical documentary source intake only: Lilly Book II Chapter XLVI, "
 "original PDF323/printed289 through PDF324/printed290 above the XLVII divider; "
 "24 source units R1770–R1793. Lilly 1,793, retained Ptolemy 1,066, combined 2,859. "
 "One printed horoscope, one author-reported sick person's death; zero independently "
 "authenticated patient outcomes or pre-frozen predictions.\n\n"
 "Corrected SIXTH-house Aquarius vs mistaken first-house Virgo; preserved copy-specific Saturn "
 "planetary hour, Mercury→Saturn retrospective square, ambiguous Moon 'that day', weak printed July28 date, "
 "and editorial 12-day subtraction. 60 distinct structural/source regression tests passed. "
 "The second independent changed-item review was primed, and there was no third independent final readback. "
 "40 unresolved source/reconstruction/empirical limitations retained. Original 1647 source PDF "
 "SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. "
 "This neither endorses medical doctrines nor promotes an astrology engine or constitutes validation.\n\n"
 "NEXT: Chapter XLVII, Of the CRYSIS in Diseases, below divider on original PDF324/printed290 "
 "and through PDF325 onward. Next R1794 only after exact cumulative index readback. "
 "Multi-author parent work OPEN. For publication and owner Downloads read B02p/ACCEPTANCE.json, "
 "PUBLICATION_RECEIPT.json and DELIVERY_RECEIPT.json separately. Historic source batches, "
 "PASS_PLAN/CURRENT, participant data, fitted models and prediction freezes unchanged.\n")
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02p accepted documentary checkpoint — publication and delivery pending\n\n"
 "Reconciled source images (original PDF323–324), both independent Opus review stages, "
 "40 retained unresolved issues and 60/60 green source-regression checks. "
 "Accepted *documentary content* on this branch; nonforce canonical publication and "
 "owner Downloads transfer are NOT yet proved. No empirical validation.\n\n"
 "Next gated steps: zip exact-byte extraction replay; check live canonical source-index head, "
 "publish B02p by nonforce Git if unchanged; verify GitHub readback and actual owner Downloads "
 "files versus SHA256 manifest. Parent source audit OPEN, next XLVII PDF324 lower/R1794.\n")
save(B/"OWNER_OUTCOME_STATUS.json",{
 "parent_task":"ASTROLOGY-MULTIAUTHOR-SOURCE-AUDIT","parent_status":"OPEN","batch":"B02p",
 "source_fidelity":"ACCEPTED_DOCUMENTARY_ONLY","new_reference_units":24,
 "external_patient_outcomes":0,"remaining":"Lilly XLVII onward and other primary sources; canonical publication, archive and Downloads receipts pending."})
(B/"LESSON_DISPOSITION.md").write_text(
 "# B02p source-fidelity lesson closeout\n\n"
 "Source image and original spelling outrank interpreted paraphrase. Historical Moon SIXTH-house "
 "Aquarius corrected from first-house Virgo and frozen in tests. "
 "Later source review caught ambiguous pronouns, exact clock/day wording, unsupported planet signs "
 "and mercury/Saturn direction; all named items repaired or retained uncertain with regressions. "
 "Changed-item review was primed and no third independent readback was run. "
 "One printed historical case supplies no independent predictive or clinical result. "
 "Project source-fidelity guidance already covers these lessons; no universal promotion requested.\n")
print(json.dumps({"documentary_accepted":True,"lilly_index_candidate":1793,
                  "regression_tests":tests["tests_run"],"next":"XLVII original PDF324 below divider"}))
