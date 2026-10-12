"""Pure exact-byte verifier for an extracted source packet (not validation of historical claims)."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
data=json.loads((B/"ARCHIVE_CONTENT_MANIFEST.json").read_text())
seen=set()
for e in data["files"]:
 p=Path(e["path"])
 if p.is_absolute() or ".." in p.parts or str(p) in seen: raise ValueError("Unsafe/duplicate payload entry: "+str(p))
 seen.add(str(p))
 source=B/p
 raw=source.read_bytes()
 if len(raw)!=e["bytes"] or hashlib.sha256(raw).hexdigest()!=e["sha256"]:
  raise ValueError("Archived payload differs: "+str(p))
assert len(seen)==data["file_count"]
print(json.dumps({"files_verified":len(seen),"status":"PASS","scope":"ZIP file bytes only, not source-fidelity or medical validity"}))
