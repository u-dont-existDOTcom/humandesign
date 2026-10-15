"""Create corrected printed355 source-first map without mutating U68 frozen map.
First printed words 'try of all sorts' finish p354 Moon-goods phrase,
now cited from both original PDFs 388→389 (U69).
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
OLD=B/"independent_review/REVERSE_SOURCE_TO_RECORD_P389_20261015.json"
OUT=B/"independent_review/REVERSE_SOURCE_TO_RECORD_P389_U70_20261015.json"
if OUT.exists():raise RuntimeError("Output already exists; verify rather than overwrite")
raw=OLD.read_bytes()
j=json.loads(raw)
assert j["original_pdf_page"]==389 and j["printed_page"]==355
assert j["source_phrase_count"]==27 and j["mapped_unique_record_count"]==23
assert j["mapped_provisional_record_numbers"]==list(range(2715,2738))
prefix={
 "source_anchor_editorial_normalization":"try of all sorts [completes Moon goods-quality Country on previous leaf]",
 "record_numbers":[2714],
 "disposition":"MAPPED_TO_PROVISIONAL_SOURCE_UNIT",
 "review_note":"Printed p355 begins with final fragment of Moon goods-quality clause from p354, not a new observed item; R2714 now cites original [388,389], U69."
}
j["source_to_record"].insert(0,prefix)
j["mapped_provisional_record_numbers"]=[2714]+j["mapped_provisional_record_numbers"]
j["source_phrase_count"]=len(j["source_to_record"])
j["mapped_unique_record_count"]=len(j["mapped_provisional_record_numbers"])
j["supersedes_map_sha256"]=hashlib.sha256(raw).hexdigest()
j["revision"]="U70_CORRECTED_ORIGINAL_388_TO_389_PAGE_SEAM"
j["source_anchor_warning"]="All anchor strings are editorial normalized source fragments; confirm exact printing against original page images."
j["independent_blinded_reviewer"]=False
j["diplomatic_character_for_character_completeness_certified"]=False
assert j["source_phrase_count"]==28 and j["mapped_unique_record_count"]==24
OUT.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"old_sha256":hashlib.sha256(raw).hexdigest(),"new_sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),"page":389,"record_count":24,"phrase_anchors":28},indent=2))
