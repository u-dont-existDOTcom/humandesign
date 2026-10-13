"""Source-only B02s acceptance after original, independent and deterministic checks.

Transactional on an isolated worktree. Canonical GitHub publication and owner
Downloads delivery occur in separate, receipt-backed steps.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02s.md"
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def hs(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
D=rd("RULES.json");R=D["rules"];U=rd("UNRESOLVED.json")
C=rd("COUNTS.json");T=rd("TEST_RUN_SUMMARY.json")
V=rd("independent_review/FINAL_RECONCILIATION.json")
L=rd("CLAIM_LEDGER.json");PRE=rd("RETAINED_LILLY_INDEX_BEFORE.json")
I=json.loads(INDEX.read_text())
assert I==PRE
assert I["records_count"]==1920 and I["next"]["chapter"]=="XLIX"
assert I["batches"][-1]["id"]=="B02r"
assert I["read_numbered_chapters"][-1]==48
assert D["record_count"]==len(R)>=187 and D["initial_draft_record_count"]==187
assert [x["record_number"] for x in R]==list(range(1921,1921+len(R)))
assert all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for x in R)
assert all(not x["independently_verified_outcome"] and not x["case_evidence_countable"] for x in R)
assert all(not x["prospective_frozen_forecast"] for x in R)
assert C["lilly_before"]==1920 and C["records"]==len(R)
assert C["combined_if_accepted"]==2986+len(R)
assert not C["empirical_validation"] and C["verified_couple_outcomes"]==0
assert U["retained_count"]==len(U["limits"])>=64
assert T["successful"] and T["failures"]==T["errors"]==T["skipped"]==0
assert T["tests_run"]==T["distinct_test_count"]>=260
assert T["source_file_sha256"]["RULES.json"]==hs(B/"RULES.json")
assert T["source_file_sha256"]["AUDIT_REPORT.md"]==hs(B/"AUDIT_REPORT.md")
assert L["report_sha256"]==hs(B/"AUDIT_REPORT.md")
assert rd("SOURCE_IDENTITY.json")["original_pdf_sha256"]==SRC
A=rd("SOURCE_REPLAY_RECEIPT.json")
assert A["source_full_pdf_sha256"]==SRC and A["pages_replayed"]==19
assert A["all_rgb_replays_identical"]
assert rd("ERRATA_COLLATION.json")["count"]==6
assert [x["printed_page"] for x in rd("ERRATA_COLLATION.json")["entries"]]==[305,306,307,312,315,315]
originals={"A":"2e59d1e474c45fb1b675368f76dd99ecd9d8250ba68f4a5f45549f508490da06",
           "B":"4668fea44ab93f074b3c58b059c05836f8cf6d619c1c575994d4e3a589b56f1d"}
for k,sha in originals.items():
 assert hs(B/"independent_review"/f"OPUS_{k}_INITIAL.md")==sha
 assert (B/"independent_review"/f"OPUS_{k}_CHANGED.md").is_file()
assert V["initial_source_review_windows"]==2
assert V["changed_item_review_windows"]==2
assert V["source_window_coverage"]==[336,353]
assert V["all_material_findings_reconciled"] is True
assert V["final_source_status"]=="ACCEPTABLE_DOCUMENTARY_ONLY"
num=1920+len(R)
headings=[x["source_record_kind"] for x in R if x["source_record_kind"].endswith("_heading") or x["source_record_kind"] in ("heading","other_relationship_subheading")]
headings=list(dict.fromkeys((x["record_number"],x["source_record_kind"]) for x in R if x["source_record_kind"].endswith("_heading") or x["source_record_kind"] in ("heading","other_relationship_subheading")))
new_head_count=len(headings)
assert new_head_count>=25
I["read_numbered_chapters"].append(49)
I["read_headed_units_count"]+=new_head_count
I["records_count"]=num
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIX_MARRIAGE_SOURCE_DOCUMENTED_LATER_LILLY_OPEN"
I["batches"].append({"id":"B02s","path":"batches/B02s/RULES.json",
  "records_count":len(R),"sha256":hs(B/"RULES.json"),
  "scope":"Lilly 1647 XLIX Of Marriage original PDF336 lower/printed302 through PDF353 upper/printed319; 187 reviewed draft source units plus recovered original clauses, zero externally verified outcomes."})
I["next"]={"pdf_page":353,"printed_page":319,"chapter":"L",
          "heading":"Of Servants fled, Beasts strayed, and things lost",
          "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
          "position":"Original PDF353 BELOW the horizontal divider through PDF354 onward; exclude XLIX above divider."}
I["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02s.md"
assert sum(v["records_count"] for v in I["batches"])==num
assert I["runtime_promotions"]==I["empirical_validations"]==0
save(INDEX,I)
save(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",I)
accept={
 "batch":"B02s","accepted":True,
 "kind":"HISTORICAL_DOCUMENTARY_SOURCE_INTAKE_ONLY",
 "source_original_pdf_sha256":SRC,"source_page_range":[336,353],
 "source_image_renders_rgb_matched":19,
 "rules_sha256":hs(B/"RULES.json"),"report_sha256":hs(B/"AUDIT_REPORT.md"),
 "claim_ledger_sha256":hs(B/"CLAIM_LEDGER.json"),
 "test_summary_sha256":hs(B/"TEST_RUN_SUMMARY.json"),
 "index_after_sha256":hs(INDEX),
 "record_first":"R1921","record_last":f"R{num}",
 "new_documentary_units":len(R),"original_draft_units":187,
 "recovered_original_units":len(R)-187,
 "independently_authenticated_couples_or_outcomes":0,
 "blinded_prospective_predictions":0,"predictive_or_clinical_validity":False,
 "clinical_or_predictive_validation":False,"runtime_promotion":False,
 "focused_source_tests":T["tests_run"],"retained_limits":U["retained_count"],
 "fresh_initial_source_review_windows":2,
 "post_correction_review_windows":2,
 "post_correction_readbacks_technically_blinded":False,
 "new_headed_source_units":new_head_count,
 "lilly_before":1920,"lilly_after_if_integrated":num,
 "retained_ptolemy":1066,"combined_if_integrated":1066+num,
 "next_chapter":"L","next_original_pdf_page":353,
 "next_documentary_id":f"R{num+1}"}
save(B/"ACCEPTANCE.json",accept)
STATE.write_text(
 "# Current astrology source audit — B02s Lilly Chapter XLIX (2026-10-13)\n\n"
 f"**Historical documentary intake accepted, not predictive validation**. Source PDF336/printed302 BELOW divider through PDF353/printed319 ABOVE divider. "
 f"{len(R)} accepted source-only units R1921–R{num}: 187 original drafts corrected after two original-image-first independent review windows, "
 f"{len(R)-187} missing source clauses added. Cumulative Lilly **{num}**, retained Ptolemy **1,066**, combined **{num+1066}**. "
 f"{U['retained_count']} original-source/interpretive limitations retained. Original 1647 source SHA256 {SRC}; "
 f"19 included page/errata images pixel-identical to verified original PDF; {T['tests_run']} source-specific tests PASS. "
 "Two changed-item reviews are admitted as follow-ups, **not** independent blind first reviews. "
 "Old disputed claims about marriage, intimate conduct, social class, death and parentage have no externally verified outcomes. "
 "No engine or participant/frozen forecast changes.\n\n"
 "Next Chapter L, original PDF353/printed319 BELOW horizontal divider and PDF354 onward; source-only next ID "
 f"R{num+1} after live index verification. The multi-author original-source study remains OPEN. "
 "ZIP extraction and actual owner Downloads hashes are separate post-acceptance gates, not proved by this state file.\n")
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02s accepted documentary source candidate — publication/delivery pending\n\n"
 f"Original-source pages336–353 plus errata888 authenticated, 2 independent first-pass windows "
 f"+ 2 changed-item readbacks reconciled. {len(R)} reference-only units R1921–R{num}; "
 f"{T['tests_run']} distinct source tests PASS, {U['retained_count']} limitations retained. "
 f"Lilly index candidate {num}, combined {num+1066}, solely in isolated worktree until canonical nonforce push. "
 "No independently validated couples, clinical allegations or forecasts.\n\n"
 "Next steps: exact archive manifest/CRC/extraction/test replay, nonforce GitHub integration, remote readback, "
 "OS Downloads exact bytes SHA256 receipt. Source study parent OPEN. Next Chapter L original PDF353 lower.\n")
save(B/"OWNER_OUTCOME_STATUS.json",{
 "parent":"Multi-author historical astrology source completeness","parent_status":"OPEN",
 "batch":"B02s","documentary_status":"ACCEPTED_SOURCE_ONLY",
 "new_units":len(R),"lilly_after_if_integrated":num,"combined_after_if_integrated":num+1066,
 "validated_outcomes":0,"remaining":"BookII Chapter L onward; separate blinded empirical tests, archive and owner file receipts pending."})
print(json.dumps({"accepted_documentary":True,"lilly":num,"combined":num+1066,"tests":T["tests_run"],"next":f"R{num+1}"}))
