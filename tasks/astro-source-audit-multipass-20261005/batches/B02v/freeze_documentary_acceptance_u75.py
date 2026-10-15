"""Freeze locally admitted B02v documentary-only acceptance evidence.
Publishing to the canonical source index is a separate non-force step.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
out=B/"ACCEPTANCE.json"
assert not out.exists(),"Acceptance already exists"
read=lambda n:json.loads((B/n).read_text())
sha=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
d=read("ACCEPTANCE_CANDIDATE.json")
tests=read("TEST_RUN_SUMMARY.json")
assert tests["successful"] and tests["distinct_test_count"]==109
assert [r["exit_code"] for r in tests["suite_results"]]==[0]*5
assert d["new_source_units"]==402 and d["lilly_before"]==2572
assert d["retained_source_issues"]==75
assert read("RULES.json")["documentary_accepted_locally"]
assert read("UNRESOLVED.json")["retained_count"]==75
assert d["source_rule_sha256"]==sha("RULES.json")
assert d["source_order_sha256"]==sha("SOURCE_ORDER.json")
assert d["unresolved_sha256"]==sha("UNRESOLVED.json")
assert d["claim_ledger_sha256"]==sha("CLAIM_LEDGER.json")
r={
 "batch":"B02v","phase":"CHAPTER_L_FINAL_SOURCE_WINDOW",
 "accepted":True,"kind":"HISTORICAL_SOURCE_DOCUMENTARY_ONLY",
 "admission_state":"LOCALLY_VERIFIED_PENDING_CANONICAL_GIT_READBACK",
 "chapter_L_source_text_covered":True,
 "original_source_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "source_original_pdf_pages":list(range(381,401)),
 "original_errata_pdf_page":888,
 "prior_accepted_lilly":2572,"new_documentary_source_units":402,
 "first_record":"R2573","last_record":"R2974",
 "lilly_after_if_integrated":2974,"ptolemy_retained":1066,
 "combined_after_if_integrated":4040,
 "new_verified_predictive_cases":0,"new_independently_authenticated_crimes":0,
 "new_clinical_medical_or_criminal_validations":0,"runtime_promotions":0,
 "uncertainties_retained":75,
 "printed_p360_line4_erratum_glyph_unresolved":True,
 "source_independent_full_diplomatic_transcription_done":False,
 "original_pages_image_replayed":21,
 "printed_direction_table_rows_normalized_reviewed":36,
 "normalized_source_first_anchors":420,
 "all_proposed_record_ids_page_mapped":True,
 "finite_original_first_high_risk_reviewed_pages":10,
 "rules_sha256":sha("RULES.json"),
 "source_order_sha256":sha("SOURCE_ORDER.json"),
 "unresolved_sha256":sha("UNRESOLVED.json"),
 "claim_ledger_sha256":sha("CLAIM_LEDGER.json"),
 "audit_report_sha256":sha("AUDIT_REPORT.md"),
 "source_first_finite_review_sha256":sha("independent_review/FINITE_HIGH_RISK_SOURCE_PASS_U75_20261015.json"),
 "source_reverse_20p_map_sha256":sha("independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json"),
 "source_tests_summary_sha256":sha("TEST_RUN_SUMMARY.json"),
 "source_only_tests_passed":109,
 "archive_extracted_tests_receipt":"not_yet_emitted_at_local_admission",
 "canonical_published":False,
 "next_source":{"pdf_page":400,"printed_page":366,"chapter":"LI",
                "heading":"Of Battell, Warre, or other Contentions",
                "physical_boundary":"BELOW printed horizontal divider, no overlap with Chapter L"}
}
out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"admitted_locally_documentary_only":True,"source_records":402,"source_tests_passed":109,"acceptance_sha256":sha("ACCEPTANCE.json"),"canonical_published":False},indent=2))
