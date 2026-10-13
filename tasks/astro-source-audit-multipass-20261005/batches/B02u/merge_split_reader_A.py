"""Lossless consolidation of two successful smaller source-reader A subwindows.
Keep overlapping page366 excluded in an audit object; retain raw source files.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
out=[]
miss=[]
sources=[]
seen_pages=set()
for name,lo,hi in (("A1",364,366),("A2",366,369)):
 p=B/f"SOURCE_READER_{name}.json"
 assert p.is_file(),("Missing source-reader evidence",p)
 d=json.loads(p.read_text())
 assert d["window"]==name and d["original_pdf_pages_read"]==list(range(lo,hi+1))
 assert len(d["units"])>=10
 src={"split_window":name,"file":p.name,
      "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
      "units":len(d["units"])}
 sources.append(src)
 selected=[];held=[]
 for u in d["units"]:
  pages=u.get("pdf_pages",[])
  if pages==[888] or (name=="A2" and not pages and u["local_id"] in {"A2069","A2070"}):
   held.append({"reason":"PRINTED_ERRATA_NOT_BODY_NOT_INDEXED",**u});continue
  assert pages and all(lo<=n<=hi for n in pages)
  if name=="A1" and min(pages)>=366:held.append({"reason":"SPLIT_OVERLAP_PAGE366_OWNED_BY_A2",**u})
  else:selected.append(u)
 out+=selected;miss+=held
 outline=d["complete_page_outline"]
 for e in outline:
  page=e.get("pdf_page")
  if page==888:continue
  assert lo<=page<=hi
  if name=="A1" and page>=366:continue
  assert page not in seen_pages
  seen_pages.add(page)
assert seen_pages==set(range(364,370)),seen_pages
assert out and len({str(u) for u in out})==len(out),"Exact duplicate unit JSON"
for i,u in enumerate(out,1):
 u["merged_local_id"]=f"A{i:03d}"
 u["merged_from_source_split"]=u["local_id"]
 u["local_id"]=f"A{i:03d}"
data={"window":"A","status":"DRAFT_SOURCE_ONLY",
      "original_pdf_pages_read":list(range(364,370)),
      "complete_page_outline":[],
      "units":out,
      "unresolved_glyphs_or_source_conflicts":[],
      "stop_boundary_observed":"PDF369 context; next B window owns new text beginning PDF369",
      "source_reader_split_provenance":sources,
      "held_original_overlap_units":len(miss)}
# Build exact outline from original two window source files; ensure 6 pages.
for name in ("A1","A2"):
 d=json.loads((B/f"SOURCE_READER_{name}.json").read_text())
 for e in d["complete_page_outline"]:
  p=e.get("pdf_page")
  if p in range(364,370) and (name=="A2" or p!=366):
   data["complete_page_outline"].append(e)
 data["unresolved_glyphs_or_source_conflicts"]+=d.get("unresolved_glyphs_or_source_conflicts",[])
assert len(data["complete_page_outline"])==6
(B/"SOURCE_READER_A.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
(B/"SPLIT_A_OVERLAP_AUDIT.json").write_text(json.dumps({
 "raw_source_files":sources,"excluded_overlap_units":miss,
 "excluded_are_NOT_deleted_from_original_source_files":True,
 "source_ownership":"A1 owns starts pages364-365; A2 owns starts366-369",
 "needs_independent_fidelity_review":True},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"merged_A_source_units":len(out),"held_overlap":len(miss),
                  "pages":len(data["complete_page_outline"]),"status":"DRAFT_ONLY"}))
