"""Bind author-facing report paragraphs to exact bytes; no new source inference."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
p=B/"AUDIT_REPORT.md"
raw=p.read_text()
parts=raw.rstrip("\n").split("\n\n")
items=[]
for i,part in enumerate(parts):
    t=part+("\n" if i==len(parts)-1 else "")
    items.append({"id":f"C{i+1:02d}","text":t,"sha256":hashlib.sha256(t.encode()).hexdigest()})
assert "\n\n".join(x["text"] for x in items)==raw
data={"batch":"B02u","report_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
      "units":items,"unit_count":len(items),
      "source_evidence_only":"William Lilly original 1647 print images, no real criminal or predictive validation"}
(B/"CLAIM_LEDGER.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"claim_blocks":len(items),"report_sha256":data["report_sha256"]}))
