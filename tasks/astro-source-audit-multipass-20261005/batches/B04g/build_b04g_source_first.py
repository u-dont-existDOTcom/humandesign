from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
groups=sum((J(f"SOURCE_AUTHORING_PART_{s}.json") for s in "ABC"),[])
assert len(groups)==6 and sum(len(g["claims"]) for g in groups)==33
rows=[];spans=[]
for group in groups:
 sid=f"LXXXVII-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  loc=f"LXXXVII-C{len(rows)+1:03}";ids.append(loc)
  navigation=role=="next_navigation"
  rows.append({"source_local_id":loc,"batch":"B04g","role":role,
   "chapter":"LXXXVIII_NAVIGATION_ONLY" if navigation else "LXXXVII",
   "original_printed_chapter_numeral":"LXXXVII" if navigation else "LXXXVI",
   "chapter_id_basis":"editorial_sequential_alias",
   "source_span_id":sid,"original_pdf_pages":group["pages"],
   "printed_pages":[p-34 for p in group["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_preferment_outcome":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":group["pages"],
 "passage_label":group["label"],"mapped_local_ids":ids})
assert len(rows)==33 and len(spans)==6
assert all(r["chapter"]=="LXXXVII" for r in rows[:-2])
assert all(r["original_printed_chapter_numeral"]=="LXXXVI" for r in rows[:-2])
assert all(r["chapter"]=="LXXXVIII_NAVIGATION_ONLY" for r in rows[-2:])
full="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in (490,491):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
assert imgs[0]["sha256"]=="391689a475ff7523ae8891f325201ac8dd11dd988c049bbb867ba58577317c19"
dump("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",{"batch":"B04g","source_units":33,"source_spans":6,"source_groups":groups})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04g","source_units":33,
 "original_full_pdf_sha256":full,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04g","span_count":6,
 "source_spans":spans,"mapped_source_units":33,
 "original_body_pdf_pages":[490,491],"following_heading_pdf":491})
dump("SOURCE_ORDER_DRAFT.json",{"batch":"B04g","ordered_ids":[r["source_local_id"] for r in rows]})
dump("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04g","original_full_pdf_sha256":full,
 "original_images":imgs,"previous_accepted_lilly":5080,
 "original_body_pdf_pages":[490,491],"following_heading_pdf":491,
 "source_editorial_chapter":"LXXXVII","source_original_printed_chapter":"LXXXVI",
 "next_editorial_chapter":"LXXXVIII","next_original_printed_chapter":"LXXXVII",
 "question_follows_previous_within_five_minutes":True,
 "source_absolute_question_date_not_printed":True,"independently_verified_appointments":0})
print(json.dumps({"batch":"B04g","annotations":33,"passages":6,
"original_printed":"LXXXVI","editorial_alias":"LXXXVII"}))
