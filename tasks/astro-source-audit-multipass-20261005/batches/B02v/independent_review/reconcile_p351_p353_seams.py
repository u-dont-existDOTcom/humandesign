"""One-time source locator repair for two 1647 printed-page continuations.

The Scorpio water-location sentence straddles p351→352. Haly's reported
Leo/Venus question straddles p352→353. No new observed cases and no
canonical source acceptance.
"""
from pathlib import Path
import json, hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P385_387.json"
BACK=B/"recovery/producer_p385_387_before_U71_U72_20261015.json"
assert not BACK.exists(),"Original backup already exists; inspect before retry"
raw=SRC.read_bytes()
obj=json.loads(raw)
by={r["local_id"]:r for r in obj["units"]}
a=by["P385C022"]
b=by["P385C041"]
assert a["pdf_pages"]==[385] and a["kind"]=="scorpio_foul_water"
assert b["pdf_pages"]==[386] and b["kind"]=="reported_haly_leo_venus_example_start"
a["pdf_pages"]=[385,386]
a["preconditions"]=["Scorpio sign branch; original printed p351 ends after the verb 'cast' and p352 supplies the remainder of the phrase 'cast out filthy Water, as a Gutter'."]
a["exceptions_and_uncertainty"]=["A single historical watery-place classification crosses the p351→352 leaf, not two new rules. No independently known item or location."]
a["original_page_anchor"]="p351 'where they use to cast' | p352 'cast out filthy Water, as a Gutter'"
b["pdf_pages"]=[386,387]
b["preconditions"]=["Original p352 starts Haly's quoted question with Leo rising; p353 provides the completion 'ing and Venus therein' and the related unverified under-bed/robe report."]
b["exceptions_and_uncertainty"]=["The report is Haly's as quoted by Lilly; no independently dated/reconstructed chart or found object is supplied. This source sentence crosses p352→353; no second observation is created."]
b["original_page_anchor"]="p352 Haly saith ... when Leo was Ascend- | p353 -ing and Venus therein"
ledger=B/"UNRESOLVED_DRAFT.json"
j=json.loads(ledger.read_text())
assert j["retained_count"]==len(j["issues"])==70
assert not {"U71","U72"} & {x["id"] for x in j["issues"]}
j["issues"].extend([
 {"id":"U71","status":"SOURCE_CROSS_PAGE_LOCATOR_CORRECTED","description":"Original 1647 printed p351 Scorpio filthy-water clause ends 'cast' and continues at p352 'cast out filthy Water, as a Gutter'. R2655 previously cited PDF385 alone; corrected to [385,386]."},
 {"id":"U72","status":"SOURCE_CROSS_PAGE_LOCATOR_CORRECTED","description":"Haly's Leo-ascending sentence starts original PDF386/printed352 and completes 'ing and Venus therein' on PDF387/printed353. R2674 cites the continuation but formerly listed PDF386 only; corrected [386,387], without claiming an authenticated outcome."}
])
j["retained_count"]=len(j["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
ledger.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"records":[2655,2674],"source_pdf_pages":[[385,386],[386,387]],"issues":72,"preedit_sha256":hashlib.sha256(raw).hexdigest(),"postedit_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"accepted":False},indent=2))
