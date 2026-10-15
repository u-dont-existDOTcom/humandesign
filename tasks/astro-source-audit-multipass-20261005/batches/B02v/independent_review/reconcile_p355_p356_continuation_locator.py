"""One-time source-locator correction for original PDF389→390 sentence.

Printed p355 ends with the initiating application clause and p356 starts
with its target/consequent. Preserve both physical source pages for R2737.
This changes provenance, not the claimed result or canonical acceptance.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P388_390.json"
BACK=B/"recovery/producer_p388_390_before_U67_20261015.json"
assert not BACK.exists(), "U67 migration previously attempted; inspect instead"
raw=SRC.read_bytes()
doc=json.loads(raw)
rows=[r for r in doc["units"] if r["local_id"]=="P388C044"]
assert len(rows)==1
r=rows[0]
assert r["pdf_pages"]==[390]
assert r["source_statement"]=="Continuation says if the Moon's term/house ruler or second-house ruler applies to ascendant lord, the thing lost shall be recovered."
r["pdf_pages"]=[389,390]
r["source_statement"]="Original printed p355 begins a conditional application of the Moon's term ruler OR Moon's house ruler OR second-house ruler, completed on p356 by 'unto the Lord of the Ascendant'; Lilly then claims the stolen thing shall be recovered."
r["preconditions"]=["One of Moon's term ruler, Moon's domicile ruler, OR second-house ruler applies to ascendant lord; single sentence crosses original PDF389→390 (printed355→356)."]
r["exceptions_and_uncertainty"]=["Do not read a whole additional recovery rule on either leaf; both are one source conditional. Historical predictive claim only, with no observed recovered property."]
r["source_image_anchor"]="Also if the Lord of the terme of the ☽ ... apply unto | the Lord of the Ascendant"
issues_path=B/"UNRESOLVED_DRAFT.json"
issues=json.loads(issues_path.read_text())
assert issues["retained_count"]==len(issues["issues"])==66
assert all(e["id"]!="U67" for e in issues["issues"])
issues["issues"].append({"id":"U67","status":"SOURCE_CROSS_PAGE_LOCATOR_CORRECTED","description":"R2737/P388C044 sentence begins original PDF389/printed355 and ends PDF390/printed356; prior source locator [390] omitted first half. Corrected to [389,390], preserving single-rule identity, literal alternative applicants and recovery consequent."})
issues["retained_count"]=len(issues["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
issues_path.write_text(json.dumps(issues,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"record":"R2737","pdf_pages":[389,390],"before_sha256":hashlib.sha256(raw).hexdigest(),"after_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issues":len(issues["issues"]),"accepted":False},indent=2))
