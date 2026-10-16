#!/usr/bin/env python3
"""Original image-only scope proof for Lilly LXVII; no historical rule admission."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
OUT=B/"SOURCE_WINDOW_PROVISIONAL.json"
assert not OUT.exists(),"No overwrite without reviewing new source authority"
imgs=[]
for i in range(438,447):
    f=B/"evidence"/f"pdf_1647-{i}.jpg"
    b=f.read_bytes()
    assert len(b)>250_000 and b[:3]==b"\xff\xd8\xff"
    imgs.append({"original_pdf_page":i,"printed_page":i-34,
       "path":f.relative_to(B).as_posix(),
       "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
record={"batch":"B03m","status":"PROVISIONAL_SCOPE_ONLY_NOT_EXTRACTED_NOT_ADMITTED",
 "source":"William Lilly Christian Astrology 1647 original Wellcome b30338724",
 "full_original_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "accepted_predecessor_lilly_count":3746,"retained_ptolemy_count":1066,
 "body_pages":list(range(438,447)),
 "original_opening":"PDF438 below ornamental divider and eighth-house preface",
 "original_ending":"PDF446 above Chapter LXVIII divider",
 "next_chapter":"LXVIII","next_original_pdf_page":446,
 "images":imgs,"rule_extraction_complete":False,
 "numbered_chapter_admitted":False,"new_source_records":0,
 "empirical_predictions_validated":0,"runtime_promotions":0}
OUT.write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("FROZEN ORIGINAL WINDOW",len(imgs),"pages; new canonical records",0,
      "source byte count",sum(x["bytes"] for x in imgs))
