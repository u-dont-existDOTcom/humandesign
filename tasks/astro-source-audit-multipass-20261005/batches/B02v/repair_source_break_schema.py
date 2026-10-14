"""Correct FIVE local page-break draft rows whose fields were shifted.
Original input is preserved byte-for-byte in recovery/first_381_384_pre_schema.json.
One-time source normalization only, not independent source review.
"""
from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent
P=B/"PRODUCER_SOURCE_DRAFT_P381_384.json"
REC=B/"recovery/first_381_384_pre_schema.json"
assert not REC.exists(), "Already repaired; inspect file before rerunning"
REC.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(P,REC)
d=json.loads(P.read_text())
R=d["units"]
assert len(R)==61
todo={6:(382,"door_moon_house_quadrant"),24:(383,"thief_dwelling_sign_quarter"),
      58:(385,"fixed_four_miles_per_sign"),59:(385,"common_one_half_miles_per_sign"),60:(385,"movable_half_mile_per_sign")}
for index,(continued,kind) in todo.items():
 r=R[index]
 assert r["kind"]==continued and r["normalized_historical_statement"]==kind
 assert len(r["preconditions"])==len(r["exceptions_and_uncertainty"])==1
 old_pre=r["preconditions"][0]
 old_uncertain=r["exceptions_and_uncertainty"][0]
 original=r["pdf_pages"]
 assert original==[continued-1],(index,original,continued)
 r.update(kind=kind,
    normalized_historical_statement=old_pre,
    preconditions=[old_uncertain],
    exceptions_and_uncertainty=["Continuation spans the original page break. This row had a shifted original draft schema; the exact prior source bytes were frozen before mechanical repair.",
                                "Editorial source paraphrase only; no independently authenticated person or outcome."],
    pdf_pages=[continued-1,continued],
    printed_pages=[continued-35,continued-34],
    page_break_source_repair=True)
assert all(isinstance(r["kind"],str) and r["kind"] and len(r["normalized_historical_statement"])>25 for r in R)
assert all(r["printed_pages"]==[p-34 for p in r["pdf_pages"]] for r in R)
d["status"]="SOURCE_DRAFT_PAGE_BREAK_FIELDS_REPAIRED_PENDING_INDEPENDENT_SOURCE_REVIEW"
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"corrected_page_breaks":len(todo),"source_records_preserved":len(R),
 "kind_ids":[x[1] for x in todo.values()],"no_runtime_promotion":True}))
