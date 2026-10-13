"""Rebuild B02s rules from immutable draft and source-review corrections.

Draft identities retained as draft_record_number. Added source clauses get
new IDs; reading order is explicitly indexed. Historical source only.
"""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
D=json.loads((B/"recovery/original_draft/RULES.json").read_text())
assert D["record_count"]==187
rs=D["rules"];by={x["record_number"]:x for x in rs}
assert list(by)==list(range(1921,2108))
provenance=[]
for name in ("REPAIRS_A1.json","REPAIRS_A2.json","REPAIRS_A3.json","REPAIRS_B1.json","REPAIRS_B2.json","REPAIRS_B3.json"):
    p=B/name
    if not p.exists():continue
    corrections=json.loads(p.read_text())
    for raw,change in corrections.items():
        n=int(raw);r=by[n]
        for field,target in (("statement","source_statement"),("kind","source_record_kind")):
            if field in change:r[target]=change[field]
        if "precondition" in change:r["preconditions"]=[change["precondition"]]
        if "limit" in change:r["exceptions_and_evidence_limits"]=[change["limit"]]
        if "pages" in change:
            ps=change["pages"];assert all(336<=z<=353 for z in ps)
            r["source_locator"]["pdf_pages"]=ps
            r["source_locator"]["printed_pages"]=[z-34 for z in ps]
            r["source_locator"]["page_images"]=[f"evidence/pdf-{z}.png" for z in ps]
        r["draft_record_number"]=n
        r["independent_review_correction_source"]=name
        provenance.append({"draft_id":f"R{n}","repair_file":name})
    print(name,len(corrections),"repairs")
new=[]
addition_paths=sorted(B.glob("SOURCE_ADDITIONS_*.json"))
if addition_paths:
    extra=[v for p in addition_paths for v in json.loads(p.read_text())["records"]]
    for i,v in enumerate(extra,2108):
        ps=v["pages"];assert ps and all(336<=p<=353 for p in ps)
        new.append({
          "id":f"LI.1647.II.XLIX.R{i}","record_number":i,
          "batch":"B02s","book":"II","chapter":"XLIX",
          "source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
          "source_locator":{"pdf_pages":ps,"printed_pages":[p-34 for p in ps],
            "page_images":[f"evidence/pdf-{p}.png" for p in ps],"source_statement_is_verbatim":False},
          "source_record_kind":v["kind"],"source_statement":v["statement"],
          "source_statement_type":"NORMALIZED_PARAPHRASE_NOT_VERBATIM",
          "preconditions":[v.get("precondition","Use all source-named planet, house, aspect and role conditions.")],
          "exceptions_and_evidence_limits":[v["limit"]],
          "case_evidence_countable":False,"independently_verified_outcome":False,
          "prospective_frozen_forecast":False,"runtime_status":"REFERENCE_ONLY_NOT_PROMOTED",
          "source_review_inserted":True,"source_order_after_draft":v["after_draft"]})
R=rs+new
assert len({x["record_number"] for x in R})==len(R)
assert all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" and not x["independently_verified_outcome"] for x in R)
read_order=[];by_anchor={}
for x in new:by_anchor.setdefault(x["source_order_after_draft"],[]).append(x["record_number"])
for x in rs:
    read_order.append(x["record_number"])
    read_order.extend(by_anchor.pop(x["record_number"],[]))
assert not by_anchor and len(read_order)==len(R) and len(set(read_order))==len(R)
# Reconcile source HEADINGS without changing the stable draft IDs used by both reviews.
def move_before(ids,anchor):
    global read_order
    seg=[z for z in read_order if z in ids]
    assert seg
    read_order=[z for z in read_order if z not in ids]
    pos=read_order.index(anchor)
    read_order[pos:pos]=seg
# Original printed314 has 'Whether a woman is honest' before 'Whether a woman trades ...'.
moral_ids=set(range(2054,2061)) | {z["record_number"] for z in new if 2054<=z["source_order_after_draft"]<=2060}
move_before(moral_ids,2050)
# Original printed316 has closing H11 judgement before H12 and its related rules.
h11_ids={2077}|{z["record_number"] for z in new if z["source_order_after_draft"]==2077}
move_before(h11_ids,2075)
assert len(read_order)==len(R) and len(set(read_order))==len(R)
O={**D,"rules":R,"status":"SOURCE_REVIEW_CORRECTED_PENDING_CHANGED_ITEM_READBACK",
   "record_count":len(R),"last_record":f"R{1920+len(R)}","initial_draft_record_count":187,
   "added_missed_original_units":len(new),"source_reading_order_manifest":"RULES_SOURCE_ORDER.json"}
(B/"RULES.json").write_text(json.dumps(O,indent=2,ensure_ascii=False)+"\n")
(B/"RULES_SOURCE_ORDER.json").write_text(json.dumps({"ids":read_order,"scope":"Actual source order with preserved draft IDs plus source-reviewed insertions."},indent=2)+"\n")
(B/"CORRECTION_PROVENANCE.json").write_text(json.dumps({
 "corrected_unique":len(set(x["draft_id"] for x in provenance)),"changes":provenance,
 "insertions":[{"id":x["record_number"],"after":x["source_order_after_draft"],"kind":x["source_record_kind"]} for x in new]},indent=2)+"\n")
print(json.dumps({"corrected_unique":len(set(x["draft_id"] for x in provenance)),
 "added":len(new),"records":len(R),"lilly_if_accepted":1920+len(R)}))
