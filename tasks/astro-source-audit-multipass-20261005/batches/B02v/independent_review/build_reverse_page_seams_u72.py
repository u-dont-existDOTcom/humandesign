"""Publish U72 versioned reverse-page maps without rewriting earlier receipts."""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]/"independent_review"
targets=[
 ("REVERSE_SOURCE_TO_RECORD_P386_20261015.json","REVERSE_SOURCE_TO_RECORD_P386_U72_20261015.json",2655,"cast out filthy Water, as a Gutter — continues Scorpio phrase from printed351"),
 ("REVERSE_SOURCE_TO_RECORD_P387_20261015.json","REVERSE_SOURCE_TO_RECORD_P387_U72_20261015.json",2674,"ing and Venus therein — completes Haly Leo-rising question from printed352")
]
for old_name,new_name,id,source in targets:
 original=B/old_name
 target=B/new_name
 assert original.exists() and not target.exists()
 data=original.read_bytes()
 j=json.loads(data)
 head={"record_number":id,"source_anchor_editorial_summary":source}
 if "note" in j["source_to_record"][0]:
  head["note"]="Original source sentence began on previous printed leaf; no new outcome is established"
 j["source_to_record"].insert(0,head)
 key="record_ids_in_print_order" if "record_ids_in_print_order" in j else "records_order"
 j[key].insert(0,id)
 count="number_of_mapped_source_anchors" if "number_of_mapped_source_anchors" in j else "count_source_unit_ids"
 j[count]=len(j["source_to_record"])
 j["supersedes_source_map_sha256"]=hashlib.sha256(data).hexdigest()
 j["version"]="U72_RECORDED_PHYSICAL_SOURCE_PAGE_SEAMS"
 j["physical_continuation_added"]=id
 j["source_anchors_editorially_normalized"]=True
 j["independent_diplomatic_source_completeness"]=False
 assert j[count]==20 and len(j[key])==20
 target.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
 print({"source_page":j["printed_page"],"record_id":id,"before_map_sha256":hashlib.sha256(data).hexdigest(),"new_map_sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
