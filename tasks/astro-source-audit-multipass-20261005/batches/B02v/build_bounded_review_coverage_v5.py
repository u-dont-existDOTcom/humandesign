"""Deterministic conservative record-level review coverage index for B02v.

Mark only documented page-scope, bounded source-image-to-producer reviews.
DO NOT infer per-record word-for-word fidelity, independent blind evaluation
or source-completeness from having checked a page at paraphrase level.
"""
import json,hashlib
from collections import defaultdict
from pathlib import Path
B=Path(__file__).resolve().parent
D=json.loads((B/"RULES_DRAFT.json").read_text())
C=json.loads((B/"COUNTS.json").read_text())
assert len(D["records"])==402 and not D["accepted"]
assert C["accepted_lilly_before"]==2572 and C["accepted_new_documentary_records"]==0
idx={x["record_number"]:x for x in D["records"]}
pages=defaultdict(set)
for x in D["records"]:
 for p in x["source_locator"]["pdf_pages"]: pages[p].add(x["record_number"])
groups=[
 ("2026-10-15 earlier bounded p350/351/354/360/362",
  [384,385,388,394,396],
  ["independent_review/REVIEW_COVERAGE_20261015.json","independent_review/COLLATION_P350_351_354_362_U60_20261015.md","PENDING_P360_ACCUSATION_SCOPE_20261015.md"]),
 ("2026-10-14 bounded p357/358/363/364/365",
  [391,392,397,398,399],
  ["independent_review/COLLATION_U58_P357_P363_P364_P365_20261014.md","independent_review/IMAGE_COLLATION_P391_392_397_20261014.md"]),
 ("2026-10-15 current bounded p359/360/361",
  [393,394,395],
  ["independent_review/IMAGE_COLLATION_P359_361_U64_20261015.md"]),
 ("2026-10-15 additional bounded original PDF381/382/383/386/387/389/390/400",
  [381,382,383,386,387,389,390,400],
  ["independent_review/IMAGE_COLLATION_8_REMAINING_PAGES_U65_20261015.md","independent_review/REVERSE_SOURCE_TO_RECORD_P389_20261015.json","independent_review/REVERSE_SOURCE_TO_RECORD_P390_20261015.json","independent_review/REVERSE_SOURCE_TO_RECORD_P400_20261015.json","independent_review/REVERSE_SOURCE_TO_RECORD_P387_20261015.json"]),
]
results=[]
united=set()
for name,pgs,docs in groups:
  ids=set().union(*(pages[p] for p in pgs))
  results.append({"review_scope":name,"source_pdf_pages":pgs,"included_source_record_count":len(ids),"source_record_ids":sorted(ids),"records_new_to_prior_groups":sorted(ids-united),"review_evidence_documents":docs,"review_level":"BOUNDED_MANUAL_IMAGE_TO_PARAPHRASE_AND_LOGIC; NOT_VERBATIM_FULL_FIDELITY"})
  united|=ids
excluded=sorted(set(idx)-united)
assert len(united)==402,(len(united),[len(x["source_record_ids"]) for x in results])
assert len(excluded)==0
assert len(results[0]["source_record_ids"])==103
assert len(results[1]["source_record_ids"])==109
assert len(results[2]["source_record_ids"])==64
assert len(results[2]["records_new_to_prior_groups"])==43
assert len(results[3]["source_record_ids"])==148
assert len(results[3]["records_new_to_prior_groups"])==147
not_yet_pages=[p for p in range(381,401) if p not in set(sum((x[1] for x in groups),[]))]
assert not_yet_pages==[],not_yet_pages
payload={
 "batch":"B02v","status":"BOUNDED_REVIEW_COVERAGE_ONLY_SOURCE_NOT_ACCEPTED",
 "source_witness":"William Lilly 1647 Wellcome b30338724 PDF381-400 printed347-366",
 "authoritative_source_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "draft_sha256":hashlib.sha256((B/"RULES_DRAFT.json").read_bytes()).hexdigest(),
 "proposed_documentary_source_records":402,
 "accepted_new_records":0,
 "unique_record_ids_in_bounded_review_evidence":sorted(united),
 "distinct_bounded_review_records":len(united),
 "records_without_documented_finite_page_specific_check_in_four_review_groups":excluded,
 "remaining_count_for_finite_page_specific_check":len(excluded),
 "remaining_original_pdf_pages_for_this_specific_scope":not_yet_pages,
 "important_caveat":"All candidate IDs have bounded documented page-level source comparisons, but this does not constitute independent, word-for-word, source-to-record exhaustiveness proof. This index certifies identity coverage only. Earlier evidence for a record is not automatically refreshed by a subsequent textual edit.",
 "past_review_sets":results,
 "source_independent_fidelity_review_completed":False,
 "chapter_L_source_complete":False,
 "real_world_predictive_evidence_count":0,
}
out=B/"independent_review/REVIEW_COVERAGE_CONSERVATIVE_U69_20261015.json"
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"documented_reviewed_unique":len(united),"not_in_these_finite_page_checks":len(excluded),"reviewed_group_counts":[r["included_source_record_count"] for r in results],"new_group_counts":[len(r["records_new_to_prior_groups"]) for r in results],"remaining_page_ids":not_yet_pages,"output_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"chapter_accepted":False},indent=2))
