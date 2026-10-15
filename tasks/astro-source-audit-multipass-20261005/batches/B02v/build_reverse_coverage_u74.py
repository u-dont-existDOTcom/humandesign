"""Machine-auditable coverage of bounded reverse source→record maps.

This is NOT full textual omission proof: all anchors remain editorial
summaries created by same source investigator. No new empirical evidence.
"""
from pathlib import Path
import json,hashlib
from collections import Counter
B=Path(__file__).resolve().parent
D=json.loads((B/"RULES_DRAFT.json").read_text())
M=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
I={r["record_number"]:r for r in D["records"]}
pages={
381:"REVERSE_SOURCE_TO_RECORD_P381_20261015.json",
382:"REVERSE_SOURCE_TO_RECORD_P382_20261015.json",
383:"REVERSE_SOURCE_TO_RECORD_P383_20261015.json",
384:"REVERSE_SOURCE_TO_RECORD_P384_20261015.json",
385:"REVERSE_SOURCE_TO_RECORD_P385_20261015.json",
386:"REVERSE_SOURCE_TO_RECORD_P386_U72_20261015.json",
387:"REVERSE_SOURCE_TO_RECORD_P387_U72_20261015.json",
388:"REVERSE_SOURCE_TO_RECORD_P388_20261015.json",
389:"REVERSE_SOURCE_TO_RECORD_P389_U70_20261015.json",
390:"REVERSE_SOURCE_TO_RECORD_P390_20261015.json",
391:"REVERSE_SOURCE_TO_RECORD_P391_U74_20261015.json",
392:"REVERSE_SOURCE_TO_RECORD_P392_U74_20261015.json",
393:"REVERSE_SOURCE_TO_RECORD_P393_U74_20261015.json",
400:"REVERSE_SOURCE_TO_RECORD_P400_20261015.json",
}
images={x["pdf_page"]:x for x in M["images"]}
def idof(r):
 if "record_number" in r:return r["record_number"]
 if "record_numbers" in r:
  assert len(r["record_numbers"])==1
  return r["record_numbers"][0]
 if "record_ids" in r:
  assert len(r["record_ids"])==1
  return r["record_ids"][0]
 raise ValueError("Missing record identifier")
mapping=[]
for page,file in pages.items():
 p=B/"independent_review"/file
 raw=p.read_bytes()
 j=json.loads(raw)
 assert j["printed_page"]==page-34
 src=images[page]
 assert hashlib.sha256((B/src["path"]).read_bytes()).hexdigest()==src["sha256"]
 ids=[idof(x) for x in j["source_to_record"]]
 assert all(x in I and page in I[x]["source_locator"]["pdf_pages"] for x in ids),(page,ids)
 distinct=sorted(set(ids))
 mapping.append({"original_pdf_page":page,"printed_page":page-34,
  "map_path":"independent_review/"+file,"map_sha256":hashlib.sha256(raw).hexdigest(),
  "normalized_anchor_count":len(j["source_to_record"]),
  "distinct_mapped_ids":len(distinct),"record_ids":distinct,
  "source_image_sha256":src["sha256"]})
all_ids=[x for p in mapping for x in p["record_ids"]]
unique=sorted(set(all_ids))
assert unique==list(range(2573,2816))+list(range(2946,2975))
assert len(unique)==272
assert len(all_ids)==283
repeated={n:c for n,c in Counter(all_ids).items() if c>1}
assert repeated=={2579:2,2597:2,2631:2,2632:2,2633:2,2655:2,2674:2,2714:2,2737:2,2770:2,2793:2}
assert sum(x["normalized_anchor_count"] for x in mapping)==289
remaining=[n for n in I if n not in set(unique)]
assert remaining==list(range(2816,2946))
payload={
"source":"William Lilly Christian Astrology 1647 Wellcome b30338724",
"source_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
"status":"BOUNDED_SAME_CONTEXT_REVERSE_MAP_UNACCEPTED",
"source_bounded_reverse_page_count":len(mapping),
"source_pages_with_reverse_map":list(pages),
"source_anchor_count":sum(x["normalized_anchor_count"] for x in mapping),
"distinct_provisional_records_reverse_mapped":len(unique),
"distinct_reverse_mapped_record_ids":unique,
"records_not_yet_reverse_mapped":remaining,
"remaining_reverse_page_ids":list(range(394,400)),
"repeat_page_reference_ids":repeated,
"source_pages":mapping,
"limit":"Maps are source-first editorial normalized anchors, NOT independent fully diplomatic clause reconstruction; remaining record IDs are not alleged missing source records, only not yet reverse mapped. 402/402 earlier record-to-image bounded review is a separate weaker coverage axis.",
"source_reverse_completeness_proved":False,
"source_independent_reviewer":False,
"newly_accepted_records":0}
out=B/"independent_review/REVERSE_SOURCE_COVERAGE_U74_20261015.json"
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"mapped_pages":len(mapping),"mapped_source_anchors":payload["source_anchor_count"],"mapped_record_ids":len(unique),"remaining_record_ids":len(remaining),"remaining_source_pages":payload["remaining_reverse_page_ids"],"repeat_ids":repeated,"output_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"accepted":False},indent=2))
