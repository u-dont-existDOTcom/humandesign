"""One-time add the explicit Moon-domicile-to-Moon original phrase to p357 reverse map.
Preserves the previous U74 mapping verbatim; does not fabricate new record IDs.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
source=B/"independent_review/REVERSE_SOURCE_TO_RECORD_P391_U74_20261015.json"
target=B/"independent_review/REVERSE_SOURCE_TO_RECORD_P391_U75_20261015.json"
assert not target.exists(),"Already generated, inspect current map"
raw=source.read_bytes()
doc=json.loads(raw)
assert doc["source_pdf_page"]==391 and doc["number_of_mapped_source_anchors"]==19
matches=[i for i,x in enumerate(doc["source_to_record"]) if x["record_number"]==2769]
assert len(matches)==1
doc["source_to_record"][matches[0]]["source_anchor_editorial_summary"]="Part-of-Fortune testimony with lord1 or Moon, and applications between them for timing of hopeful recovery"
doc["source_to_record"].insert(matches[0]+1,{
 "record_number":2769,
 "source_anchor_editorial_summary":"OR the lord of the Moon's own house APPLYING TO the Moon; separate alternative timing testimony, now restored under U75"
})
doc["number_of_mapped_source_anchors"]=len(doc["source_to_record"])
doc["revision"]="U75_RESTORES_EXPLICIT_MOON_DOMICILE_APPLICATION_BRANCH"
doc["preceding_map_sha256"]=hashlib.sha256(raw).hexdigest()
doc["independent_diplomatic_source_completeness"]=False
assert doc["number_of_mapped_source_anchors"]==20
assert len(set(x["record_number"] for x in doc["source_to_record"]))==19
target.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
print({"prior_sha256":hashlib.sha256(raw).hexdigest(),"new_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"anchors":20,"unique_ids":19})
