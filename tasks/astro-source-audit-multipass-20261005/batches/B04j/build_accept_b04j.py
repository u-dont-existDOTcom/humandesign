from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
read=lambda n:json.loads((B/n).read_text())
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
groups=read("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")["source_groups"]
IDX=read(str(ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"))
assert IDX["records_count"]==5193 and IDX["batches"][-1]["id"]=="B04i"
assert IDX["next"]["chapter"]=="XC" and IDX["next"]["pdf_page"]==494
rows=[];spans=[]
for group in groups:
 sid=f"XC-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  lid=f"XC-C{len(rows)+1:03}";ids.append(lid)
  rows.append(dict(source_local_id=lid,batch="B04j",source_span_id=sid,
   role=role,chapter="XCI_NAVIGATION_ONLY" if role=="next_navigation" else "XC",
   printed_chapter="LXXXIX",original_pdf_pages=group["pages"],
   printed_pages=[n-34 for n in group["pages"]],
   short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
   original_source_qualifications=limit,global_record_number=None,
   historical_documentary_accepted=False,independently_verified_enemy_identity=False,
   empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=group["pages"],
  passage_label=group["label"],mapped_local_ids=ids))
assert len(rows)==29 and len(spans)==4
ims=[]
for n in (494,495):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 ims.append(dict(original_pdf_page=n,printed_page=n-34,path=p.relative_to(B).as_posix(),
  bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
put("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04j",source_units=29,rows=rows))
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04j",source_spans=spans,span_count=4,mapped_source_units=29))
put("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04j",original_full_pdf_sha256=IDX["source_sha256"],
 original_images=ims,previous_accepted_lilly=5193,
 next_editorial="XCI",next_printed="XC",original_body_pdf_pages=[494,495],following_heading_pdf=495))
rules=[]
for n,r in enumerate(rows,start=5194):
 rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,"independently_verified_enemy_identity":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(5194,5223))
put("RULES.json",dict(batch="B04j",kind="ORIGINAL_HISTORICAL_SECRET_ENEMIES_NO_REAL_IDENTITIES",
 status="LOCAL_SOURCE_ONLY_PENDING_REMOTE",record_count=29,first_record=5194,last_record=5222,
 substantive_source_records=27,next_heading_navigation=2,
 printed_chapter="LXXXIX",editorial_chapter="XC",source_spans=4,
 independent_verified_enemy_identifications=0,independent_medical_diagnoses=0,
 empirical_validations=0,runtime_promotions=0,rules=rules))
idmap={r["source_local_id"]:r["id"] for r in rules}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",dict(batch="B04j",
 source_spans=[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]} for s in spans],
 span_count=4,mapped_source_records=29))
put("SOURCE_ORDER.json",dict(batch="B04j",first_record=5194,last_record=5222,
 record_count=29,ids=[r["id"] for r in rules],source_pages=[494,495]))
A=dict(batch="B04j",previous_lilly=5193,new_records=29,lilly_if_published=5222,
 ptolemy_retained=1066,combined_if_published=6288,
 next_editorial="XCI",next_printed="XC",next_original_pdf_page=495,
 independent_enemy_identifications=0,independent_medical_diagnoses=0,
 empirical_validations=0,runtime_promotions=0)
for name,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256")]:A[key]=H(B/name)
put("ACCEPTANCE.json",A)
print(json.dumps(A))
