from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
def put(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
idx=J(ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json")
assert idx["records_count"]==5222 and idx["batches"][-1]["id"]=="B04j"
assert idx["next"]["chapter"]=="XCI" and idx["next"]["pdf_page"]==495
g=J(B/"SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")["source_groups"];D=[];M=[]
for group in g:
 sid=f"XCI-S{len(M)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  lid=f"XCI-C{len(D)+1:03}";ids.append(lid)
  D.append(dict(source_local_id=lid,batch="B04k",source_span_id=sid,role=role,
   chapter="XCII_NAVIGATION_ONLY" if role=="next_navigation" else "XCI",
   printed_chapter="XC",original_pdf_pages=group["pages"],
   printed_pages=[p-34 for p in group["pages"]],
   short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
   original_source_qualifications=limit,global_record_number=None,
   historical_documentary_accepted=False,independently_verified_prisoner_outcome=False,
   empirically_validated_prediction=False,runtime_model_promoted=False))
 M.append(dict(span_id=sid,original_pdf_pages=group["pages"],passage_label=group["label"],mapped_local_ids=ids))
assert len(D)==85 and len(M)==12
assert all(r["chapter"]=="XCI" for r in D[:-2])
images=[]
for n in (495,496,497):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append(dict(original_pdf_page=n,printed_page=n-34,path=p.relative_to(B).as_posix(),
  bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
assert idx["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert len(J(B/"UNRESOLVED_SOURCE_LIMITS.json")["issues"])==22
put(B/"SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04k",source_units=85,rows=D))
put(B/"ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04k",source_spans=M,span_count=12,mapped_source_units=85))
put(B/"SOURCE_WINDOW_MANIFEST.json",dict(batch="B04k",original_full_pdf_sha256=idx["source_sha256"],original_images=images,
 original_body_pdf_pages=[495,496,497],following_heading_pdf=497,previous_accepted_lilly=5222,
 original_printed_chapter="XC",editorial_chapter="XCI",next_printed="XCI",next_editorial="XCII"))
rs=[]
for n,r in enumerate(D,start=5223):
 rs.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,"historical_documentary_accepted":True,
  "independently_verified_prisoner_outcome":False,"empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rs]==list(range(5223,5308))
R=dict(batch="B04k",kind="HISTORICAL_IMPRISONMENT_ESCAPE_AND_HARM_SOURCE_ONLY",
 status="LOCAL_DOCUMENTARY_PENDING_REMOTE",record_count=85,first_record=5223,last_record=5307,
 substantive_source_records=83,following_heading_navigation=2,source_spans=12,
 printed_chapter="XC",editorial_chapter="XCI",source_uncertainties=22,
 independently_verified_prisoner_outcomes=0,independently_verified_deaths=0,
 new_empirical_validations=0,runtime_promotions=0,rules=rs)
put(B/"RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rs}
put(B/"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",dict(batch="B04k",
 source_spans=[{**s,"accepted_global_record_ids":[idmap[x] for x in s["mapped_local_ids"]]} for s in M],
 span_count=12,mapped_source_records=85))
put(B/"SOURCE_ORDER.json",dict(batch="B04k",first_record=5223,last_record=5307,record_count=85,ids=[r["id"] for r in rs]))
A=dict(batch="B04k",previous_lilly=5222,new_records=85,lilly_if_published=5307,
 retained_ptolemy=1066,combined_if_published=6373,next_editorial="XCII",next_printed="XCI",
 next_original_pdf_page=497,independent_prisoner_outcomes=0,independent_deaths=0,
 empirical_validations=0,runtime_promotions=0)
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("UNRESOLVED_SOURCE_LIMITS.json","issues_sha256")]:A[k]=H(B/f)
put(B/"ACCEPTANCE.json",A)
print(json.dumps(A))
