"""Consolidate four source-image-first model OUTLINES, preserving overlaps for audit.

This only builds a source-DRAFT and does NOT confer source acceptance or
empirical astrology, criminal/legal identification or prognostic validity.
"""
from pathlib import Path
import json,hashlib,collections
B=Path(__file__).resolve().parent
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
ranges={"A":(364,369),"B":(369,373),"C":(373,377),"D":(377,381)}
ownership={"A":(364,368),"B":(369,372),"C":(373,376),"D":(377,381)}
ctx={};picked=[];held=[];errata=[];pagecount=collections.Counter();issues=[]
for k,(lo,hi) in ranges.items():
 f=B/f"SOURCE_READER_{k}.json"
 manifest=load(B/f"SOURCE_READER_INPUT_{k}.json")
 assert f.is_file(),f"Missing draft from source window {k}"
 D=load(f)
 assert D["window"]==k and D["original_pdf_pages_read"]==list(range(lo,hi+1)),(k,D.get("original_pdf_pages_read"))
 units=D.get("units",[])
 assert len(units)>=10 and len(units)<=130,(k,len(units))
 assert all("source_images/" in x["name"] for x in manifest["files"] if "pdf-" in x["name"])
 context={"window":k,"pdf_pages":[lo,hi],"source_draft_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),
          "unit_count":len(units),"confidence_model":"model_generated_needs_image_review",
          "image_first_claim":True}
 ctx[k]=context
 assert len({u["local_id"] for u in units})==len(units)
 for u in units:
  pages=u["pdf_pages"]
  if pages==[888]:
   errata.append({"window":k,"draft_unit":u,"source_type":"PRINTED_ERRATA_SEPARATE_FROM_CHAPTER_BODY"})
   continue
  assert pages and all(lo<=p<=hi for p in pages),(k,pages)
  assert all(364<=p<=381 for p in pages)
  statement=u.get("normalized_historical_statement","").strip()
  assert len(statement)>=16,(k,u.get("local_id"),statement)
  start=min(pages)
  key=f"{k}.{u['local_id']}"
  record={"window":k,"window_local_id":u["local_id"],"preliminary_key":key,
         "pdf_pages":pages,"printed_pages":[p-34 for p in pages],
         "source_images":[f"evidence/pdf-{p}.png" for p in pages],
         "section_heading":u.get("section_heading",""),
         "source_kind":u.get("kind","source_conditional"),
         "source_anchor":u.get("short_original_anchor",""),
         "source_statement":statement,
         "preconditions":u.get("preconditions",[]),
         "exceptions_and_uncertainty":u.get("exceptions_and_uncertainty",[]),
         "source_reader_confidence":u.get("confidence","unreported"),
         "source_pdf_full_sha256":SRC,
         "raw_source_reader_draft":f.name}
  if ownership[k][0]<=start<=ownership[k][1]:
   picked.append(record);pagecount[start]+=1
  else:held.append({**record,"exclusion_reason":"SOURCE_PAGE_OVERLAP_OUTSIDE_WINDOW_OWNERSHIP"})
 for e in D.get("unresolved_glyphs_or_source_conflicts",[]):
  issues.append({"window":k,**e})
 assert len(units)==context["unit_count"]
# preserve reader-level original order on one page; source may continue on next page
picked.sort(key=lambda x:(min(x["pdf_pages"]), "ABCD".index(x["window"]),
                           int("".join(z for z in x["window_local_id"] if z.isdigit()) or "0")))
assert len({u["preliminary_key"] for u in picked})==len(picked)
assert all(pagecount[n]>0 for n in range(364,382)),pagecount
for i,u in enumerate(picked):
 n=2306+i
 u["record_number"]=n
 u["id"]=f"LI.1647.II.L.B02u.R{n}"
 u["source_status"]="SOURCE_DRAFT_PENDING_SEPARATE_PAGE_REVIEW"
 u["original_human_cases_verified"]=0
 u["source_claim_not_predictive_validation"]=True
 u["runtime_status"]="REFERENCE_ONLY_NOT_PROMOTED"
D={"batch":"B02u","scope":"Chapter L original PDF364 below thief heading through PDF381 before house-of-thief heading",
   "status":"UNACCEPTED_CONSOLIDATED_SOURCE_DRAFT",
   "original_pdf_sha256":SRC,
   "unit_count":len(picked),"provisional_first_record":"R2306",
   "provisional_last_record":f"R{2305+len(picked)}",
   "canonical_accepted_lilly_still":2305,
   "conditional_cumulative_lilly_if_accepted":2305+len(picked),
   "retained_ptolemy":1066,
   "conditional_combined_if_accepted":3371+len(picked),
   "window_provenance":ctx,
   "unresolved_reader_findings_count":len(issues),
   "overlap_units_held_for_fidelity_review":len(held),
   "whole_chapter_L_complete":False,
   "independently_confirmed_thieves_crimes_or_recoveries":0,
   "units":picked}
(B/"DRAFT_CONSOLIDATED.json").write_text(json.dumps(D,indent=2,ensure_ascii=False)+"\n")
(B/"SOURCE_READER_ERRATA.json").write_text(json.dumps({"separate_from_body":True,"units":errata},indent=2,ensure_ascii=False)+"\n")
(B/"READER_OVERLAP_AUDIT.json").write_text(json.dumps({
 "window_ownership":ownership,"overlap_input_units":held,
 "every_discarded_overlap_clause_requires_review":True,
 "uncertainties":[{"window":k,"finding":e} for k,e in []],
 "raw_reader_uncertainties":issues,
 "page_counts_by_start":{str(n):pagecount[n] for n in sorted(pagecount)},
 "draft_not_accepted":True},indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"source_reader_windows":4,"draft_units":len(picked),"held_overlap":len(held),
                 "unresolved":len(issues),"provisional_last_record":D["provisional_last_record"],
                 "all_source_pages_have_candidate":True,"accepted":False}))
