"""Hash exact original-source report prose units for future source claim review."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
raw=(B/"AUDIT_REPORT.md").read_text()
parts=raw.rstrip("\n").split("\n\n")
rows=[]
for i,body in enumerate(parts):
  text=body+("\n" if i==len(parts)-1 else "")
  rows.append({"id":f"C{i+1:03d}","text":text,"sha256":hashlib.sha256(text.encode()).hexdigest()})
assert "\n\n".join(q["text"] for q in rows)==raw
packet={"batch":"B02t","phase":"1","source_report_sha256":hashlib.sha256(raw.encode()).hexdigest(),
        "report_sha256":hashlib.sha256(raw.encode()).hexdigest(),"unit_count":len(rows),
        "units":rows,"claims_are": "source interpretation and documentary provenance only"}
(B/"CLAIM_LEDGER.json").write_text(json.dumps(packet,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"claim_units":len(rows),"report_sha256":packet["report_sha256"]}))
