"""One-time source-locator correction at original PDF388→389 page break.
The Moon's animal/commodity sentence begins on printed354 and its final
'Country' word continues at top printed355. No new empirical source rule.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P388_390.json"
BACK=B/"recovery/producer_p388_390_before_U69_p354_20261015.json"
assert not BACK.exists(),"Already applied; inspect frozen bytes before retry."
raw=SRC.read_bytes()
doc=json.loads(raw)
matches=[x for x in doc["units"] if x["local_id"]=="P388C021"]
assert len(matches)==1
r=matches[0]
assert r["kind"]=="quality_second_moon_country_beasts"
assert r["pdf_pages"]==[388]
assert r["source_statement"]=="With Moon as second lord the source suggests beasts: horses, mules, cows or poultry, especially in the country."
r["pdf_pages"]=[388,389]
r["preconditions"]=["Moon rules second; printed country versus town qualification applies to this item. Sentence 'Poultry in the Coun-' on PDF388 continues 'try of all sorts' at PDF389 top."]
r["exceptions_and_uncertainty"]=["One printed item across two leaves, not two separate source records. This is a historical goods-category attribution, not verified missing property."]
r["original_page_anchor"]="☽ Beasts, as the Horse, Mules, Cowes, or Poultry in the Coun- | try of all sorts"
ledger=B/"UNRESOLVED_DRAFT.json"
issues=json.loads(ledger.read_text())
assert issues["retained_count"]==len(issues["issues"])==68
assert all(i["id"]!="U69" for i in issues["issues"])
issues["issues"].append({"id":"U69","status":"SOURCE_CROSS_PAGE_LOCATOR_CORRECTED","description":"Original PDF388/printed354 Moon-as-second-lord goods classification ends 'Poultry in the Coun-' and PDF389/printed355 begins 'try of all sorts'. R2714 previously located only to PDF388; corrected to [388,389], one source clause, not two."})
issues["retained_count"]=len(issues["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
ledger.write_text(json.dumps(issues,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"record":2714,"pages":[388,389],"preedit_sha256":hashlib.sha256(raw).hexdigest(),"post_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issues":len(issues["issues"]),"accepted_new":0},indent=2))
