from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
groups=sum((j(f"SOURCE_GROUPS_PART{i}.json") for i in (1,2,3)),[])
N=sum(len(g["claims"]) for g in groups)
assert len(groups)==13 and N==99
rows=[];spans=[]
for g in groups:
 sid=f"RECTIFY-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in g["claims"]:
  lid=f"RECTIFY-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B04w","source_local_id":lid,"source_span_id":sid,
   "section":"NEXT_ANIMODAR_NAV_ONLY" if role=="next_navigation" else "TRUTINE_AND_OTHER_RECTIFICATION_METHODS",
   "printed_chapter":"XCVIII","original_pdf_pages":g["pages"],
   "printed_pages":[n-34 for n in g["pages"]],
   "role":role,"short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "source_numeric_table_fully_transcribed":False,
   "independently_verified_conception_event":False,
   "independently_verified_natal_birth_time":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],"passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==99 and all(r["section"]=="TRUTINE_AND_OTHER_RECTIFICATION_METHODS" for r in rows[:-3])
assert all(r["section"]=="NEXT_ANIMODAR_NAV_ONLY" for r in rows[-3:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in range(534,540):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B04w","source_groups":groups,"source_spans":13,"source_units":99})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04w","original_full_pdf_sha256":sha,
 "status":"ORIGINAL_RECTIFICATION_SOURCE_FIRST_PROVISIONAL","source_units":99,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04w","span_count":13,
 "source_spans":spans,"mapped_source_units":99,"original_body_pdf_pages":list(range(534,540)),
 "following_animodar_heading_pdf":539})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04w","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_chapter_nav_ids":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04w","original_full_pdf_sha256":sha,
 "original_images":images,"original_body_pdf_pages":list(range(534,540)),
 "next_printed_chapter":"XCIX","next_editorial_chapter":"C","next_heading_pdf":539,
 "previous_accepted_lilly":5824,"next_global_record":5825,
 "merchant_natal_year_source":1616,"merchant_birth_month_day":"September 19",
 "merchant_prenatal_gestation_days_source":285,"merchant_assumed_conception":"10 December 1615",
 "merchant_conception_independently_verified":False,
 "trutine_sign_help_reported_exact_degree_rare":True,
 "source_says_hour_of_conception_alternative_not_credited":True,
 "full_gestation_table_numeric_transcribed":False})
print(json.dumps({"batch":"B04w","draft_annotations":99,"passage_groups":13,"original_pdf_pages":[534,535,536,537,538,539],"next":"printed XCIX Animodar on PDF539"}))
