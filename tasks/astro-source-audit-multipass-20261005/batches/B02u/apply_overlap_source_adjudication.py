"""Original-image-read manual adjudication of p339 classification compression.
Raw C006 combined several printed sign classifications; preserve original and
substitute six separate page-localized B070–B075 units, without double-counting.
"""
import json,copy,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
P=B/"DRAFT_CONSOLIDATED.json"
D=json.loads(P.read_text())
assert D["status"]=="UNACCEPTED_CONSOLIDATED_SOURCE_DRAFT"
r=D["units"]
matches=[i for i,x in enumerate(r) if x["window"]=="C" and x["window_local_id"]=="C006"]
assert len(matches)==1,matches
pos=matches[0];old=r[pos]
assert old["pdf_pages"]==[373]
raw=json.loads((B/"SOURCE_READER_B.json").read_text())
targets={u["local_id"]:u for u in raw["units"] if u["local_id"] in [f"B{i:03d}" for i in range(70,76)]}
assert len(targets)==6
replacements=[]
for name in [f"B{i:03d}" for i in range(70,76)]:
 u=targets[name]
 assert u["pdf_pages"]==[373]
 n=copy.deepcopy(old)
 n.update({"window":"B","window_local_id":name,"preliminary_key":"B."+name,
          "source_images":["evidence/pdf-373.png"],"pdf_pages":[373],"printed_pages":[339],
          "source_anchor":u["short_original_anchor"],
          "section_heading":u.get("section_heading","If one Thiefe or more."),
          "source_kind":u.get("kind","source_conditional"),
          "source_statement":u["normalized_historical_statement"],
          "preconditions":u.get("preconditions",[]),
          "exceptions_and_uncertainty":u.get("exceptions_and_uncertainty",[]),
          "source_reader_confidence":u.get("confidence","unreported"),
          "raw_source_reader_draft":"SOURCE_READER_B.json",
          "overlap_review_override":"PRIMARY_ORIGINAL_PDF373_CONFIRMS_SEPARATE_SIGN_CLASSIFICATION"})
 replacements.append(n)
r[pos:pos+1]=replacements
for i,x in enumerate(r):
 x["record_number"]=2306+i
 x["id"]=f"LI.1647.II.L.B02u.R{2306+i}"
assert len(set(x["id"] for x in r))==len(r)
D["unit_count"]=len(r)
D["provisional_last_record"]="R"+str(2305+len(r))
D["conditional_cumulative_lilly_if_accepted"]=2305+len(r)
D["conditional_combined_if_accepted"]=3371+len(r)
D["status"]="DRAFT_SOURCE_CONSOLIDATED_WITH_ORIGINAL_PAGE373_DISAGGREGATION"
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+"\n")
audit={"original_pdf_page":373,"printed_page":339,
       "reason":"Original p339 explicitly enumerates six distinct zodiac sign classifications; source reader C bundled six into one clause.",
       "superseded_in_index_but_retained_raw":old,
       "inserted_raw_B_local_ids":[x["window_local_id"] for x in replacements],
       "original_image":"evidence/pdf-373.png",
       "multiple_reader_sources":["SOURCE_READER_B.json","SOURCE_READER_C.json"],
       "not_empirical_validation":True,
       "independent_fidelity_review_pending":True}
(B/"OVERLAP_ADJUDICATION.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_c_unit_replaced":"C006","separate_classifications_inserted":6,
                  "net_increase":5,"candidate_total":len(r),"accepted":False}))
