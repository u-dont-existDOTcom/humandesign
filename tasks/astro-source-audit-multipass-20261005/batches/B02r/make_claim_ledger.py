"""Stable hashes for every source-audit report block."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
p=B/"AUDIT_REPORT.md"
s=p.read_text()
blocks=s.rstrip("\n").split("\n\n")
rows=[]
for i,block in enumerate(blocks):
 t=block+("\n" if i==len(blocks)-1 else "")
 rows.append({"id":f"C{i+1:02d}","text":t,"sha256":hashlib.sha256(t.encode()).hexdigest()})
assert "\n\n".join(x["text"] for x in rows)==s
o={"batch":"B02r","report_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"unit_count":len(rows),"units":rows,
   "source_scope":"Original 1647 William Lilly PDF330–336 and errata888, editorial paraphrases; no validated forecasts"}
(B/"CLAIM_LEDGER.json").write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"claim_units":len(rows),"report_sha256":o["report_sha256"]}))
