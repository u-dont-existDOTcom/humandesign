"""Generate a source-order index for provisional Lilly B02v without source acceptance.

The headings/records are producer paraphrases, NOT a diplomatic transcription.
Every image and cross-page source locator is preserved for later visual review.
"""
import hashlib
import json
from collections import defaultdict
from pathlib import Path

B=Path(__file__).resolve().parent
def raw(name):return (B/name).read_bytes()
def data(name):return json.loads(raw(name))
def h(b):return hashlib.sha256(b).hexdigest()
r=data("RULES_DRAFT.json")
manifest=data("SOURCE_IMAGE_MANIFEST.json")
counts=data("COUNTS.json")
assert not r["accepted"] and counts["accepted_new_documentary_records"]==0
records=r["records"]
assert len(records)==402
assert [x["record_number"] for x in records]==list(range(2573,2975))
images={x["pdf_page"]:x for x in manifest["images"] if x["pdf_page"]!=888}
assert set(images)==set(range(381,401))
headings=[(i,x) for i,x in enumerate(records) if x["source_record_kind"].endswith("_heading")]
assert len(headings)==49
table_kinds={"house_direction_table","primary_sign_direction_table","parallel_sign_direction_table"}
sections=[]
for k,(index,first) in enumerate(headings):
    stop=headings[k+1][0] if k+1<len(headings) else len(records)
    group=records[index:stop]
    sections.append({
      "sequence":k+1,
      "start_record":first["record_number"],
      "end_record":group[-1]["record_number"],
      "heading_record_kind":first["source_record_kind"],
      "marker_type":("PROSE_LIST_LEAD_IN" if first["record_number"]==2913 else "PRINTED_SECTION_HEADING_CANDIDATE"),
      "heading_paraphrase":first["source_statement"],
      "source_pdf_pages":sorted({p for x in group for p in x["source_locator"]["pdf_pages"]}),
      "editorial_record_count":len(group),
      "source_text_status":"PRODUCER_PARAPHRASE_SOURCE_IMAGE_REVIEW_NOT_FULLY_INDEPENDENT",
    })
assert sum(s["editorial_record_count"] for s in sections)==402
assert sections[-1]["end_record"]==2974
page_records=defaultdict(list)
for rec in records:
    for p in rec["source_locator"]["pdf_pages"]:
        page_records[p].append(rec["record_number"])
pages=[]
for p in range(381,401):
    source=images[p]
    pages.append({
      "original_pdf_page":p,"printed_page":p-34,
      "original_image":source["path"],"sha256":source["sha256"],
      "all_records_referencing_page":page_records[p],
      "starting_on_this_page":[x["record_number"] for x in records if x["source_locator"]["pdf_pages"][0]==p],
      "headings":[x["record_number"] for x in records if x["source_locator"]["pdf_pages"][0]==p and x["source_record_kind"].endswith("_heading")],
      "cross_page_records":[x["record_number"] for x in records if p in x["source_locator"]["pdf_pages"] and len(x["source_locator"]["pdf_pages"])>1],
    })
assert all(p["starting_on_this_page"] for p in pages)
cross=[{"record":x["record_number"],"pdf_pages":x["source_locator"]["pdf_pages"],"page_role":("LITERAL_PRINTED_CLAUSE_CONTINUES_OVER_LEAF" if x["record_number"] in (2579,2597,2633,2655,2674,2714,2737,2770,2793) else "CONTEXT_CROSS_REFERENCE_FOR_SAME_DISTANCE_METHOD")} for x in records if len(x["source_locator"]["pdf_pages"])>1]
assert len(cross)==11
assert [x["record"] for x in cross if x["page_role"].startswith("LITERAL")]==[2579,2597,2633,2655,2674,2714,2737,2770,2793]
result={
 "batch":"B02v",
 "status":"PROVISIONAL_PRODUCER_SOURCE_ORDER_INDEX_NOT_FULL_IMAGE_SEMANTIC_CERTIFICATION",
 "full_original_pdf_sha256":manifest["original_pdf_sha256"],
 "opening":"Original PDF381 below Of the house of the Thiefe, and the mark thereof (prior upper section B02u)",
 "closing":"Original PDF400 above Chapter LI divider; Chapter LI itself excluded",
 "provisional_source_units":402,
 "starting_id":"R2573","ending_id":"R2974",
 "numbered_chapter_L_completed_and_accepted":False,
 "previous_accepted_lilly":2572,
 "source_page_count":len(pages),
 "editorial_section_marker_count":len(sections),
 "printed_heading_candidates":sum(s["marker_type"]=="PRINTED_SECTION_HEADING_CANDIDATE" for s in sections),
 "prose_list_lead_in_count":sum(s["marker_type"]=="PROSE_LIST_LEAD_IN" for s in sections),
 "printed_tables":3,
 "printed_table_rows":36,
 "review_not_completed":"Source-image first pass exists for some spans; this automated order index does not validate every sentence or solve glyph ambiguities.",
 "upstream_sha256":{
   name:h(raw(name)) for name in ["RULES_DRAFT.json","SOURCE_IMAGE_MANIFEST.json","PRINTED_DIRECTION_TABLES.json","UNRESOLVED_DRAFT.json"]},
 "sections":sections,"pages":pages,"cross_page_source_units":cross,
}
out=B/"SOURCE_ORDER_DRAFT.json"
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"section_count":len(sections),"page_count":len(pages),"record_count":len(records),"cross_page":cross,"output_sha256":h(out.read_bytes()),"accepted":False},indent=2))
