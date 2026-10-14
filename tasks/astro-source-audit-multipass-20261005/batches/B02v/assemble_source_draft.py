"""Consolidate source-image editorial units for Lilly L FINAL SEGMENT, without acceptance.

This deliberately DOES NOT change the canonical historical source index, advance
read_numbered_chapters or present the 402 source units as empirical results.
Producer paraphrases require separate independent source review.
"""
from pathlib import Path
import hashlib,collections,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
SOURCE_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def save(n,d):(B/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
orig=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert orig["records_count"]==2572 and orig["next"]["pdf_page"]==381
assert orig["next"]["chapter"]=="L" and orig["batches"][-1]["id"]=="B02u"
files=sorted(B.glob("PRODUCER_SOURCE_DRAFT_P*.json"))
assert len(files)==7,[f.name for f in files]
units=[]
for f in files:
 d=json.loads(f.read_text())
 assert d["batch"]=="B02v"
 for i,r in enumerate(d["units"]):
  assert isinstance(r["kind"],str) and r["kind"]
  assert isinstance(r["pdf_pages"],list) and r["pdf_pages"]
  assert isinstance(r.get("source_statement") or r.get("normalized_historical_statement"),str)
  assert r["preconditions"] and r["exceptions_and_uncertainty"]
  assert all(381<=p<=400 for p in r["pdf_pages"])
  assert not r["source_statement_is_verbatim"]
  units.append((f.name,i,r))
assert len(units)==402,len(units)
kinds=[r["kind"] for _,_,r in units]
assert len(set(kinds))==402
page_starts=[min(r["pdf_pages"]) for _,_,r in units]
assert page_starts==sorted(page_starts)
assert page_starts[0]==381 and page_starts[-1]==400
records=[]
for i,(draft_name,draft_index,r) in enumerate(units):
 n=2573+i
 pages=r["pdf_pages"]
 text=r.get("source_statement") or r.get("normalized_historical_statement")
 records.append({
  "id":f"LI.1647.II.L.R{n}",
  "record_number":n,"batch":"B02v","book":"II","chapter":"L","source_id":"LILLY1647_WELLCOME_B30338724",
  "source_full_pdf_sha256":SOURCE_SHA,
  "source_locator":{"pdf_pages":pages,"printed_pages":[p-34 for p in pages],
   "page_images":[f"evidence/pdf-{p}.png" for p in pages],
   "source_statement_is_verbatim":False,
   "original_image_is_authoritative":True},
  "source_record_kind":r["kind"],
  "source_statement":text,
  "source_statement_type":"EDITORIAL_PARAPHRASE_NOT_DIPLOMATIC_TRANSCRIPTION",
  "preconditions":r["preconditions"],"exceptions_and_evidence_limits":r["exceptions_and_uncertainty"],
  "draft_origin_file":draft_name,"draft_origin_index":draft_index,
  "dependency_group":("SOURCE_HEADING" if r["kind"].endswith("_heading") else
                      "SOURCE_TABLE" if r["kind"].endswith("_table") else
                      "HISTORICAL_CONDITIONAL_OR_EXAMPLE"),
  "source_witness_only":True,
  "case_evidence_countable":False,"independently_authenticated_outcome":False,
  "prospective_blinded_prediction":False,"clinical_or_criminal_efficacy_verified":False,
  "runtime_status":"REFERENCE_ONLY_NOT_PROMOTED"
 })
assert [r["record_number"] for r in records]==list(range(2573,2975))
out={"batch":"B02v","phase":"FINAL_SEGMENT_OF_CHAPTER_L",
 "status":"PROVISIONAL_SOURCE_IMAGE_EDITORIAL_DRAFT_INDEPENDENT_REVIEW_PENDING",
 "accepted":False,"first_record":"R2573","last_record":"R2974","record_count":len(records),
 "origin_full_pdf_sha256":SOURCE_SHA,"source_pdf_pages":list(range(381,401)),
 "chapter_L_complete_if_accepted":True,
 "verified_historical_thieves_or_crimes":0,"verified_prospective_predictions":0,
 "clinical_or_criminal_validity":False,"records":records}
save("RULES_DRAFT.json",out)
save("COUNTS.json",{
 "batch":"B02v","status":"UNACCEPTED_EDITORIAL_CANDIDATE",
 "accepted_lilly_before":2572,"retained_ptolemy":1066,
 "proposed_new_documentary_records":402,
 "lilly_if_accepted":2974,"combined_if_accepted":4040,
 "accepted_new_documentary_records":0,
 "original_documentary_source_pages":20,
 "source_tables":3,"source_table_rows":36,
 "independent_fidelity_review_complete":False,
 "original_historical_cases_independently_authenticated":0,
 "blinded_prospective_predictions":0,
 "runtime_promotion":False,"full_chapter_l_completion_not_yet_admitted":True,
 "draft_sources":[{"file":f.name,"records":len(json.loads(f.read_text())["units"])} for f in files],
 "group_counts":dict(collections.Counter(r["dependency_group"] for r in records))
})
page=collections.defaultdict(list)
for r in records:
 for p in r["source_locator"]["pdf_pages"]:page[p].append(r["record_number"])
assert all(page[p] for p in range(381,401))
save("SECTION_COVERAGE_DRAFT.json",{
 "batch":"B02v","status":"PRODUCER_PAGE_COVERAGE_NOT_INDEPENDENTLY_CERTIFIED",
 "exact_start":"Original PDF381 BELOW Of the house of the Thiefe heading, excluding already accepted above-heading material",
 "exact_stop":"Original PDF400 ABOVE the horizontal divider introducing Chapter LI",
 "source_pages":[{"pdf_page":p,"printed_page":p-34,"record_count_referring_to_page":len(page[p]),
   "first_record":f"R{min(page[p])}","last_record":f"R{max(page[p])}"} for p in range(381,401)],
 "source_heading_count":sum(r["source_record_kind"].endswith("_heading") for r in records),
 "printed_table_witnesses":["evidence/pdf-398.png","evidence/pdf-399.png"],
 "source_1647_original_pdf_sha256":SOURCE_SHA,
 "same_page_prior_B02u_ending":"PDF381 above separate printed 'Of the house of the Thiefe, and the mark thereof' heading",
 "next_chapter":"LI Of Battell, Warre, or other Contentions, PDF400 BELOW divider, excluded",
 "full_chapter_l_complete":False,
 "next_untouched_beyond_boundary_pdf":400,
 "no_model_or_empirical_promotion":True
})
print(json.dumps({"source_files":len(files),"draft_records":len(records),
 "last_provisional":"R2974","candidate_lilly":2974,"candidate_combined":4040,
 "accepted_lilly_remains":2572,"source_pages":20,"source_table_rows":36}))
