"""Freeze reviewed reference-only rules before final integrity test and acceptance.

This creates a CANDIDATE file. Admission remains in ACCEPTANCE.json, never
in the source-rule status field. Rerun only after inspecting current state.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
d=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text())
assert len(d["rules"])==d["record_count"]>=162
assert not (B/"ACCEPTANCE.json").exists()
c=json.loads(json.dumps(d))
c["status"]="REVIEWED_HISTORICAL_SOURCE_REFERENCE_ONLY_NOT_YET_ADMITTED"
output=json.dumps(c,ensure_ascii=False,indent=2)+"\n"
p=B/"RULES.json"
if p.exists():assert p.read_text()==output,"RULES exists but differs from latest reviewed source draft"
else:p.write_text(output)
print(json.dumps({"reference_only_candidate_units":len(c["rules"]),"sha256":hashlib.sha256(output.encode()).hexdigest(),
 "accepted":False,"full_chapter_l_complete":False}))
