"""B02r exact-source documentary acceptance, contingent on reviewer findings and tests.

Writes only isolated-task-branch candidate source index and files; GitHub push,
remote readback and OS Downloads delivery each require separate receipts.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02r.md"
SOURCE="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
D=rd("RULES.json");T=rd("TEST_RUN_SUMMARY.json");C=rd("COUNTS.json")
U=rd("UNRESOLVED.json");REVIEW=rd("independent_review/FINAL_RECONCILIATION.json")
prior=rd("RETAINED_LILLY_INDEX_BEFORE.json")
I=json.loads(INDEX.read_text())
assert I==prior and I["records_count"]==1851 and I["batches"][-1]["id"]=="B02q"
assert I["next"]["chapter"]=="XLVIII" and I["next"]["pdf_page"]==330
assert C["lilly_before"]==1851 and C["new_documentary_records"]==69 and C["combined_if_accepted"]==2986
assert D["record_count"]==len(D["rules"])==69
assert [v["record_number"] for v in D["rules"]]==list(range(1852,1921))
assert [v["aphorism_number"] for v in D["rules"] if "aphorism_number" in v]==list(range(1,44))
assert D["chapter_xlviii_own_units"]==19 and D["seventh_house_bridge_units"]==6
assert D["general_horary_aphorism_units"]==43 and D["next_heading_boundary_units"]==1
assert T["successful"] and T["tests_run"]==T["distinct_test_count"]>=69
assert T["failures"]==T["errors"]==T["skipped"]==0
assert T["source_file_sha256"]["RULES.json"]==sha(B/"RULES.json")
assert T["source_file_sha256"]["AUDIT_REPORT.md"]==sha(B/"AUDIT_REPORT.md")
assert rd("CLAIM_LEDGER.json")["report_sha256"]==sha(B/"AUDIT_REPORT.md")
assert rd("SOURCE_IDENTITY.json")["source_full_pdf_sha256"]==SOURCE
assert rd("SOURCE_REPLAY_RECEIPT.json")["all_rgb_replays_identical"]
assert U["retained_count"]==len(U["limits"])
assert len(rd("SOURCE_IMAGE_MANIFEST.json")["images"])==9
assert REVIEW["verdict"]=="SOURCE_FIDELITY_RECONCILED"
assert REVIEW["initial_evaluator_kind"]=="FRESH_INDEPENDENT_SOURCE_IMAGE_REVIEW"
assert REVIEW["original_source_images_checked"]==9
assert REVIEW["records_checked"]==69 and REVIEW["general_numbered_aphorisms_checked"]==43
assert REVIEW["all_material_findings_reconciled"] is True
assert (B/"independent_review/OPUS_INITIAL_DIAGNOSIS.md").stat().st_size>100
assert all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" and
           not x["independently_verified_outcome"] and
           not x["prospective_blinded_prediction"] and
           not x["clinical_efficacy_verified"] for x in D["rules"])
assert all(C[k]==0 for k in ["new_original_horoscopes","new_historical_cases","independently_verified_outcomes","blinded_predictions"])
assert I["read_numbered_chapters"][-1]==47
I["read_numbered_chapters"].append(48)
I["read_headed_units_count"]+=3
I["records_count"]=1920
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_XLVIII_AND_SEVENTH_GENERAL_HORARY_APHORISMS_SOURCE_READ"
I["batches"].append({
 "id":"B02r","path":"batches/B02r/RULES.json",
 "records_count":69,"sha256":sha(B/"RULES.json"),
 "scope":"Lilly Book II XLVIII + seventh-house bridge + all 43 general horary aphorisms, original PDF330/printed296 below divider through PDF336/printed302 above XLIX divider, 69 source units, zero verified cases."
})
I["next"]={
 "pdf_page":336,"printed_page":302,"chapter":"XLIX",
 "heading":"Of Marriage","include_opening_paragraph":True,
 "opening_anchor":"If a Question be asked of Marriage, behold the ascendant and the Lord thereof, and the Moon",
 "position":"Original PDF336 below divider; continue on PDF337 and beyond; exclude already extracted aphorism43",
 "extracted":False,"boundary_image_read":True
}
I["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261012_B02r.md"
assert sum(x["records_count"] for x in I["batches"])==1920
assert I["runtime_promotions"]==I["empirical_validations"]==0
save(INDEX,I);save(B/"LILLY_SOURCE_EXTRACTION_INDEX_AFTER.json",I)
accept={
 "batch":"B02r","accepted":True,"accepted_as":"Historical source-documentary text only, no empirical forecast or medical or legal validation",
 "source_original_pdf_sha256":SOURCE,"source_pdf_pages":list(range(330,337)),
 "rules_sha256":sha(B/"RULES.json"),"report_sha256":sha(B/"AUDIT_REPORT.md"),
 "claim_ledger_sha256":sha(B/"CLAIM_LEDGER.json"),
 "source_regression_summary_sha256":sha(B/"TEST_RUN_SUMMARY.json"),
 "index_after_sha256":sha(INDEX),
 "record_first":"R1852","record_last":"R1920","new_source_records":69,
 "xlviii_units":19,"seventh_intro_units":6,"different_general_horary_aphorisms":43,
 "boundary_units":1,"previous_different_physician_aphorisms":43,
 "lilly_before":1851,"lilly_after_if_integrated":1920,"retained_ptolemy":1066,"combined_if_integrated":2986,
 "new_charts":0,"verified_historical_outcomes":0,"clinical_or_predictive_validity":False,
 "clinical_or_predictive_validation":False,
 "runtime_promotion":False,"tests_distinct_pass":T["distinct_test_count"],
 "original_page_pixel_replay_pages":9,"independent_review":"independent_review/OPUS_INITIAL_DIAGNOSIS.md",
 "source_fidelity_reconciliation":"independent_review/FINAL_RECONCILIATION.json",
 "remaining_source_uncertainties":U["retained_count"],"next_chapter":"XLIX","next_pdf_page":336,"next_record":"R1921"
}
save(B/"ACCEPTANCE.json",accept)
STATE.write_text(
 "# Astrology source audit — Lilly B02r accepted documentary material\n\n"
 "Original 1647 Lilly, Chapter XLVIII, 7th-house introduction and all 43 **general horary** aphorisms "
 "accepted as historical *reference-only* material, NOT clinically or predictively validated. "
 "Original pages PDF330/printed296 **below** the XLVIII divider through PDF336/printed302 "
 "**above** the XLIX divider. 69 source units R1852–R1920. Lilly **1,920**, retained Ptolemy "
 "**1,066**, combined **2,986**. The general 43 here are separate from earlier 43 physician aphorisms.\n\n"
 "Full original scan SHA256 "+SOURCE+". Nine page/errata images pixel-replayed, independent image-first "
 "source review completed and reconciled, with final verified "
 f"{T['distinct_test_count']} distinct documentary tests. "
 f"{U['retained_count']} unresolved source limitations explicitly retained. "
 "No patient charts, independent clinical/relationship outcomes, frozen forecasts, empirically confirmed "
 "predictions or runtime engine promotions. Current participant work and earlier accepted source packets "
 "remain untouched.\n\n"
 "Next reading is Chapter XLIX, **Of Marriage**, original PDF336/printed302 **below** divider, "
 "then PDF337 onward. Next reference **R1921** after checking live cumulative index. "
 "Multi-author historical-source audit OPEN. Archive usability, GitHub publication and Downloads "
 "delivery are independent downstream receipts; read B02r/PACKET_USABILITY.json, "
 "B02r/PUBLICATION_RECEIPT.json and B02r/DELIVERY_RECEIPT.json before claiming delivery.\n"
)
(B/"WORKING_CHECKPOINT.md").write_text(
 "# B02r documentary source accepted; publication and owner file delivery pending\n\n"
 "All original PDF330–336 source images and PDF337/errata888 boundary images replayed identically "
 "from verified original 1647. Original image-first reviewer findings reconciled, "
 f"{T['distinct_test_count']} source-only checks green, and "
 f"{U['retained_count']} open uncertainties retained. "
 "Proposed cumulative source index advanced 1,851→1,920 on isolated worktree only. "
 "Do NOT describe this as clinical/empirical or blind validation.\n\n"
 "Next gates: ZIP exact manifest/CRC/extraction/test replay; nonforce GitHub source and canonical branch "
 "push after exact remote-head checks; owner OS Downloads actual SHA-256 copy, publication/delivery "
 "receipts and remote readback. Parent multi-author source audit OPEN. Next source XLIX original "
 "PDF336/printed302 below divider, R1921 if accepted.\n"
)
save(B/"OWNER_OUTCOME_STATUS.json",{
 "parent":"MULTI_AUTHOR_ASTROLOGY_SOURCE_COMPLETENESS","parent_status":"OPEN",
 "batch":"B02r","source_documentary_acceptance":True,"new_source_units":69,
 "source_lilly_total_if_integrated":1920,"combined_if_integrated":2986,
 "validated_patient_cases_or_forecasts":0,
 "remaining":"Later Lilly XLIX onwards and rest of historic sources, independent empirical validation separately; ZIP and delivery receipts pending."})
(B/"LESSON_DISPOSITION.md").write_text(
 "# B02r closeout — source attribution and classification\n\n"
 "- Distinguish the two different source sets of **43** physician vs general-horary aphorisms.\n"
 "- Preserve structural sixth-house finishing and unnumbered seventh-house bridge; no phantom chapter count.\n"
 "- Preserve conditional first-lord/Moon/Sun fallback and direct/retrograde changes in source treatment of servitude.\n"
 "- Maintain original 12-degree under beams vs 16-minute cazimi and four void-course sign exceptions.\n"
 "- Flag node and Part-of-Fortune-like glyphs only where source print supports them; original copy is authoritative.\n"
 "- Do not interpret historic source conditionals as probability, modern social/medical claims or measured outcomes.\n"
 "- Generalizable source provenance is already covered by current UDA; no unsupported new universal promotion.\n"
)
print(json.dumps({"documentary_accepted":True,"lilly_candidate":1920,"combined_candidate":2986,
                  "tests":T["distinct_test_count"],"next":"XLIX PDF336 lower / R1921"}))
