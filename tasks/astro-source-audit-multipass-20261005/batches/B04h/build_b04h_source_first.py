#!/usr/bin/env python3
"""Lilly 1647 printed LXXXVII / editorial LXXXVIII eleventh-house hopes."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_AUTHORING_PART_A.json")+J("SOURCE_AUTHORING_PART_B.json")
assert len(G)==7 and sum(len(g["claims"]) for g in G)==48
rows=[];spans=[]
for g in G:
 sid=f"LXXXVIII-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in g["claims"]:
  lid=f"LXXXVIII-C{len(rows)+1:03}";ids.append(lid)
  nav=role=="next_navigation"
  rows.append({"source_local_id":lid,"batch":"B04h","role":role,
  "chapter":"LXXXIX_NAVIGATION_ONLY" if nav else "LXXXVIII",
  "original_printed_chapter_numeral":"LXXXVIII" if nav else "LXXXVII",
  "chapter_id_basis":"editorial_sequential_alias",
  "source_span_id":sid,"original_pdf_pages":g["pages"],
  "printed_pages":[p-34 for p in g["pages"]],
  "short_original_anchor_not_diplomatic":anchor,
  "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
  "global_record_number":None,"historical_documentary_accepted":False,
  "independently_authenticated_hope_fulfilment":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
 "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==48 and len(spans)==7
assert all(r["chapter"]=="LXXXVIII" and r["original_printed_chapter_numeral"]=="LXXXVII" for r in rows[:-2])
assert all(r["chapter"]=="LXXXIX_NAVIGATION_ONLY" and r["original_printed_chapter_numeral"]=="LXXXVIII" for r in rows[-2:])
full="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in (491,492,493):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
 "path":p.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
assert imgs[0]["sha256"]=="e7ba8567db2af312c2b8d73b59dcdba26a339bde55e37be021f362dd04c2e0a2"
dump("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",{"batch":"B04h","source_groups":G,"source_spans":7,"source_units":48})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04h",
 "status":"ORIGINAL_FIRST_EDITION_SOURCE_FIRST_PROVISIONAL",
 "source_units":48,"original_full_pdf_sha256":full,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04h","source_spans":spans,
 "span_count":7,"mapped_source_units":48,"original_body_pdf_pages":[491,492],
 "following_heading_pdf":493,"independent_diplomatic_second_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{"batch":"B04h","ordered_ids":[r["source_local_id"] for r in rows]})
dump("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04h","original_images":imgs,
 "original_full_pdf_sha256":full,"previous_accepted_lilly":5113,
 "original_body_pdf_pages":[491,492],"following_heading_pdf":493,
 "chapter_editorial":"LXXXVIII","chapter_original_printed":"LXXXVII",
 "following_editorial":"LXXXIX","following_original_printed":"LXXXVIII",
 "independently_verified_hope_fulfilments":0})
print(json.dumps({"batch":"B04h","source_units":48,"span_groups":7,
 "printed_chapter":"LXXXVII","editorial_alias":"LXXXVIII"}))
