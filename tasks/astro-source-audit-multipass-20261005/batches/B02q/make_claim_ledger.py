"""Bind the research report's actual paragraphs and headings to immutable hashes."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/"AUDIT_REPORT.md"
s=p.read_text()
blocks=s.rstrip("\n").split("\n\n")
units=[]
for i,block in enumerate(blocks):
 text=block+("\n" if i==len(blocks)-1 else "")
 units.append({"id":f"C{i+1:02d}","text":text,"sha256":hashlib.sha256(text.encode()).hexdigest()})
ledger={"report_sha256":hashlib.sha256(s.encode()).hexdigest(),
        "unit_count":len(units),"units":units,
        "evidence_scope":"Historical source interpretation checked against original 1647 PDF324–330 and errata888, no independent medical validity"}
(B/"CLAIM_LEDGER.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n")
assert "\n\n".join(x["text"] for x in units)==s
print(json.dumps({"report_sha256":ledger["report_sha256"],"paragraph_units":len(units)}))
