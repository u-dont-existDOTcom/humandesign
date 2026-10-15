"""Prepare Lilly B02v source-only documentary admission candidate.

Never alter existing provisional evidence, original images, empirical chart
models or the canonical source index in this step. Guarded one-time staging.
Acceptance is EDITORIAL TEXT-INVENTORY, not validation of astrology.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(p):return json.loads((B/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=B/name
 assert not p.exists(),f"Do not overwrite existing source acceptance candidate: {name}"
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
 return sha(p)
idx=json.loads(IDX.read_text())
assert idx["records_count"]==2572 and idx["batches"][-1]["id"]=="B02u"
assert idx["next"]["chapter"]=="L" and idx["next"]["pdf_page"]==381
assert 50 not in idx["read_numbered_chapters"]
assert sum(z["records_count"] for z in idx["batches"])==2572
assert idx["runtime_promotions"]==idx["empirical_validations"]==0
rules=rd("RULES_DRAFT.json")
u=rd("UNRESOLVED_DRAFT.json")
counts=rd("COUNTS.json")
order=rd("SOURCE_ORDER_DRAFT.json")
rev=rd("independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json")
w=rd("SOURCE_IMAGE_MANIFEST.json")
replay=rd("SOURCE_REPLAY_RECEIPT.json")
tables=rd("PRINTED_DIRECTION_TABLES.json")
hi=rd("independent_review/FINITE_HIGH_RISK_SOURCE_PASS_U75_20261015.json")
err=rd("ERRATA_COLLATION.json")
assert len(rules["records"])==402 and not rules["accepted"]
assert [r["record_number"] for r in rules["records"]]==list(range(2573,2975))
assert len({r["id"] for r in rules["records"]})==402
assert all(r["batch"]=="B02v" and r["chapter"]=="L" for r in rules["records"])
assert u["retained_count"]==len(u["issues"])==75
assert u["issues"][-1]["id"]=="U75"
assert counts["accepted_lilly_before"]==2572 and counts["retained_ptolemy"]==1066
assert counts["lilly_if_accepted"]==2974 and counts["combined_if_accepted"]==4040
assert counts["accepted_new_documentary_records"]==0
assert not counts["runtime_promotion"] and counts["blinded_prospective_predictions"]==0
assert w["original_pdf_sha256"]==SRC
assert len(w["images"])==21
assert {i["pdf_page"] for i in w["images"]}==set(range(381,401))|{888}
for e in w["images"]:
 assert sha(B/e["path"])==e["sha256"]
assert replay["original_pdf_sha256"]==SRC
assert replay["all_source_image_renders_replayed_rgb_identical"]
assert order["provisional_source_units"]==402
assert order["editorial_section_marker_count"]==49
assert len(order["cross_page_source_units"])==11
assert len(order["pages"])==20 and len(order["sections"])==49
assert sum(x["editorial_record_count"] for x in order["sections"])==402
assert sum(len(t["rows"]) for t in tables["original_table_witnesses"])==36
assert rev["distinct_candidate_record_ids_mapped"]==402
assert rev["normalized_anchor_count"]==420 and len(rev["page_map_manifest"])==20
assert rev["current_source_draft_sha256"]==sha(B/"RULES_DRAFT.json")
assert not rev["independent_diplomatic_text_completeness"]
assert hi["decision"]=="RECOMMEND_SOURCE_DOCUMENTARY_ONLY_ADMISSION_WITH_RETAINED_UNCERTAINTIES"
assert len(hi["inspected_pages"])==10
assert err["candidate_in_scope"][0]["read_word_or_glyph_verified"] is False
assert rules["origin_full_pdf_sha256"]==SRC
for r in rules["records"]:
 assert r["source_witness_only"] and not r["case_evidence_countable"]
 assert not r["prospective_blinded_prediction"]
 assert not r["independently_authenticated_outcome"]
 assert not r["clinical_or_criminal_efficacy_verified"]
 assert r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED"
 assert all(381<=i<=400 for i in r["source_locator"]["pdf_pages"])
assert rules["records"][-1]["source_record_kind"]=="chapter_li_boundary"
assert "divider" in rules["records"][-1]["source_statement"]
source={
 "batch":"B02v",
 "status":"HISTORICAL_SOURCE_DOCUMENTARY_ONLY_ADMITTED_LOCALLY_CANONICAL_PUBLICATION_PENDING",
 "documentary_accepted_locally":True,
 "whole_chapter_l_complete_at_documentary_source_level":True,
 "fully_diplomatic_second_reader_completed":False,
 "source_pdf_sha256":SRC,
 "source_pages":list(range(381,401)),
 "errata_original_pdf_page":888,
 "first_record":"R2573","last_record":"R2974",
 "record_count":402,
 "rules":rules["records"],
 "accepted_as_empirical_astro_prediction":False,
 "independently_authenticated_historical_crimes":0,
 "runtime_promotions":0,
 "source_note":"Literal source ambiguity is retained in U01-U75; acceptance only inventories original printed historical rules."
}
rules_sha=save("RULES.json",source)
source_order={
 "batch":"B02v",
 "status":"HISTORICAL_SOURCE_ORDER_DOCUMENTARY_ONLY",
 "source_order_record_ids":list(range(2573,2975)),
 "source_order_source_sha256":sha(B/"SOURCE_ORDER_DRAFT.json"),
 "source_pages":order["pages"],
 "sections":order["sections"],
 "two_page_locators":order["cross_page_source_units"],
 "source_accepted_at_editorial_level":True,
 "source_diplomatic_completeness_proved":False,
 "chapter_L_next":"CHAPTER_LI_BELOW_PDF400_DIVIDER"
}
order_sha=save("SOURCE_ORDER.json",source_order)
unresolved_sha=save("UNRESOLVED.json",dict(u,admission_status="RETAINED_WITH_DOCUMENTARY_ONLY_ACCEPTANCE"))
claim={
 "batch":"B02v","source_full_pdf_sha256":SRC,
 "source_records_accepted_documentary_only":402,
 "source_conditions_examples_and_headings_included":402,
 "independent_crime_cases":0,"independent_people_identifications":0,
 "empirical_predictive_outcomes":0,"clinical_or_criminal_uses_authorized":False,
 "runtime_promotions":0,"blinded_prediction_score_improvement":None,
 "uncertainty_ledger_sha256":unresolved_sha,
 "historical_owner_report_status":"SOURCE_ONLY_NON_EMPIRICAL",
 "original_source_wording_vs_editorial_interpretation":"Explicit uncertainty and original page references retained."
}
claim_sha=save("CLAIM_LEDGER.json",claim)
result={
 "kind":"DOCUMENTARY_ONLY_SOURCE_ADMISSION_CANDIDATE_AFTER_BOUNDED_SOURCE_FIRST_PASS",
 "batch":"B02v","source_full_pdf_sha256":SRC,"first_record":"R2573","last_record":"R2974",
 "new_source_units":402,"new_empirical_cases":0,
 "lilly_before":2572,"lilly_after_if_published":2974,
 "ptolemy_retained":1066,"combined_after_if_published":4040,
 "chapter_L_source_body_covered":True,
 "original_pdf_start":381,"original_pdf_last":400,
 "chapter_LI_body_excluded":True,
 "retained_source_issues":75,
 "source_rule_sha256":rules_sha,"source_order_sha256":order_sha,
 "unresolved_sha256":unresolved_sha,"claim_ledger_sha256":claim_sha,
 "original_image_sha256_checked":21,
 "reverse_mapped_original_pages":20,
 "original_normalized_reverse_anchors":420,
 "source_highrisk_original_pages_checked":10,
 "direction_table_rows_reviewed":36,
 "erratum_p360_l4_symbol_unresolved":True,
 "source_diplomatic_100percent_verbatim_or_independent":False,
 "accepted_as_documentary_only_locally":True,
 "canonical_record_index_updated":False,
 "archive_test_extraction_pending":True,
 "nonforce_published_remote":False,
 "acceptance_assurance_comparison":"B02u accepted 267 source units with 119 unresolved textual items and no final independent post-controller review; U75 402 source units with 75 retained issues and 420 normalized original anchors.",
 "unresolved_not_promotion":"No determination of guilty persons, appearance, location, historical event accuracy, or natal chart predictive validity."
}
candidate_sha=save("ACCEPTANCE_CANDIDATE.json",result)
report=(
 "# B02v source-only documentary admission candidate — original Lilly Chapter L\n\n"
 "This accepts 402 source TEXT units R2573–R2974 at a historical documentary level, "
 "covering original PDF381 after the thief-house heading through PDF400 above Chapter LI. "
 "It is NOT a test of astrology, an identified theft or a verified event. "
 "The original Wellcome scan and three direction tables are preserved; "
 "420 normalized source-first anchors cover all 402 existing candidate IDs, "
 "and one missing Moon-house-lord application alternative was repaired as U75.\n\n"
 "Retained original ambiguities include the unresolved p360/l4 erratum, "
 "bidirectional application wording, 'truth is said of him', and several unnumbered clause groupings. "
 "The documentary acceptance assurance matches the prior B02u standard; an impossible "
 "absolute zero-omission or separate diplomatic second transcription is not newly required.\n\n"
 "The review is ORIGINAL-SOURCE-based but same-context, not independently blind. "
 "Research admission is separate from any runtime or predictive validation. "
 "Canonical integration, ZIP extracted tests, remote readback and delivery are downstream gates.\n"
)
path=B/"AUDIT_REPORT.md"
assert not path.exists()
path.write_text(report)
print(json.dumps({"local_documentary_candidate":True,"records":402,"after_if_published":2974,
 "issues":75,"rules_sha256":rules_sha,"acceptance_candidate_sha256":candidate_sha,
 "source_order_sha256":order_sha,"claims_sha256":claim_sha,"accepted_empirical_cases":0},indent=2))
