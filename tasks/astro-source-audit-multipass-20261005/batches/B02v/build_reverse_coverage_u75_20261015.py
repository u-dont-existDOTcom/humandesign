"""Validate bounded reverse mappings for original Lilly PDF381-400.

Maps were written from visually inspected original pages, in the same model
context. Coverage of existing candidate IDs is NOT original-text omission
proof, independent review, diplomatic transcription, or astrology validation.
"""
from pathlib import Path
from collections import Counter
import json,hashlib
B=Path(__file__).resolve().parent
def jread(path):return json.loads((B/path).read_text(encoding="utf-8"))
R=jread("RULES_DRAFT.json")
U=jread("UNRESOLVED_DRAFT.json")
M=jread("SOURCE_IMAGE_MANIFEST.json")
assert not R["accepted"] and len(R["records"])==402
assert U["retained_count"]==75
by={r["record_number"]:r for r in R["records"]}
assert sorted(by)==list(range(2573,2975))
frozen={
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
391:"REVERSE_SOURCE_TO_RECORD_P391_U75_20261015.json",
392:"REVERSE_SOURCE_TO_RECORD_P392_U74_20261015.json",
393:"REVERSE_SOURCE_TO_RECORD_P393_U74_20261015.json",
394:"REVERSE_SOURCE_TO_RECORD_P394_20261015.json",
395:"REVERSE_SOURCE_TO_RECORD_P395_20261015.json",
396:"REVERSE_SOURCE_TO_RECORD_P396_20261015.json",
397:"REVERSE_SOURCE_TO_RECORD_P397_20261015.json",
398:"REVERSE_SOURCE_TO_RECORD_P398_20261015.json",
399:"REVERSE_SOURCE_TO_RECORD_P399_20261015.json",
400:"REVERSE_SOURCE_TO_RECORD_P400_20261015.json"}
ims={item["pdf_page"]:item for item in M["images"]}
def record_id(a):
 if "record_number" in a:return a["record_number"]
 if "record_numbers" in a:
  assert len(a["record_numbers"])==1
  return a["record_numbers"][0]
 if "record_ids" in a:
  assert len(a["record_ids"])==1
  return a["record_ids"][0]
 raise ValueError(a)
maps=[]
for page in range(381,401):
 file=frozen[page]
 p=B/"independent_review"/file
 raw=p.read_bytes()
 source=json.loads(raw)
 assert source["printed_page"]==page-34, file
 assert page in ims
 img=B/ims[page]["path"]
 assert hashlib.sha256(img.read_bytes()).hexdigest()==ims[page]["sha256"]
 rows=source["source_to_record"]
 ids=[record_id(x) for x in rows]
 assert all(n in by and page in by[n]["source_locator"]["pdf_pages"] for n in ids),(page,ids)
 maps.append({"original_pdf_page":page,"printed_page":page-34,"map_file":"independent_review/"+file,
  "map_sha256":hashlib.sha256(raw).hexdigest(),"source_image_sha256":ims[page]["sha256"],
  "normalized_anchor_count":len(rows),"distinct_ids":sorted(set(ids)),
  "distinct_mapped_id_count":len(set(ids))})
all_ids=[i for row in maps for i in row["distinct_ids"]]
uniq=sorted(set(all_ids))
assert uniq==list(range(2573,2975))
assert len(maps)==20
assert sum(m["normalized_anchor_count"] for m in maps)==420
assert [m["distinct_mapped_id_count"] for m in maps[13:19]]==[21,21,21,23,21,23]
assert len(all_ids)==413
repeated={str(i):v for i,v in Counter(all_ids).items() if v>1}
assert len(repeated)==11 and set(repeated.values())=={2}
result={
 "source":"William Lilly, Christian Astrology, original 1647 Wellcome b30338724",
 "original_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "status":"CANDIDATE_ID_REVERSE_PAGE_COVERAGE_FULL; CLAUSE_OMISSION_FIDELITY_NOT_CERTIFIED",
 "current_source_draft_sha256":hashlib.sha256((B/"RULES_DRAFT.json").read_bytes()).hexdigest(),
 "logged_source_issues":75,"current_accepted_Lilly":2572,"newly_accepted":0,
 "source_reverse_pages_mapped":20,"pdf_pages":list(range(381,401)),
 "normalized_anchor_count":sum(m["normalized_anchor_count"] for m in maps),
 "distinct_candidate_record_ids_mapped":len(uniq),"distinct_candidate_record_ids":uniq,
 "record_page_appearances":len(all_ids),"repeated_cross_page_record_ids":repeated,
 "record_ids_unmapped":[],
 "table_note":"A source anchor may summarize a multi-row original printed direction table; normalized anchor count is not a count of every printed token/line/clause.",
 "limitations":["Maps were produced in the same context as editorial extraction; not independently blind.",
 "All 402 existing candidate IDs were located on their cited original page(s); this cannot rule out omitted unrecorded source clauses.",
 "Original p360 line4 errata glyph remains unresolved and is not conjecturally altered.",
 "No text-based historical prediction is validated against real-world cases."],
 "independent_diplomatic_text_completeness":False,
 "original_to_record_exhaustiveness_proved":False,
 "chapter_L_documentary_source_accepted":False,
 "page_map_manifest":maps
}
dest=B/"independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json"
assert not dest.exists(),"Already created; do not overwrite evidence"
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"page_count":len(maps),"anchors":result["normalized_anchor_count"],
 "mapped_unique_ids":len(uniq),"record_page_appearances":len(all_ids),
 "cross_page_duplicates":len(repeated),"unmapped":0,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
 "accepted":False},indent=2))
