from __future__ import annotations
import json, hashlib, os
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row, planet_for

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).with_name("ASTRO_V14_FULL_RULE_VECTOR.json")
EPHE=Path(os.environ["EPHEMERIS_ROOT"])
MAP=ROOT/"tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V13-TARGET-BLIND-CONSENSUS-MAP-20260924.json"
when=datetime(1994,1,27,22,35,tzinfo=UTC)
snap=build_snapshot(when,latitude=41.0138429552247,longitude=28.9496612548828,ephemeris_root=EPHE)
cons=json.loads(MAP.read_text())
rows=registry(cons,{d["domain_id"] for d in cons["domains"]})
vals=feature_row(snap,rows)
items=[]
by_source=defaultdict(Counter)
by_subject=defaultdict(Counter)
by_domain=defaultdict(Counter)
for rule,val in zip(rows,vals.tolist()):
    v=int(val)
    resolved_planet=planet_for(snap,rule["source_id"],rule["subject"])
    item={**rule,"value":v,"resolved_planet":resolved_planet}
    items.append(item)
    label="positive" if v>0 else "negative" if v<0 else "zero"
    by_source[rule["source_id"]][label]+=1
    by_subject[f"{rule['source_id']}/{rule['subject']}"][label]+=1
    for d in rule["supported_domain_ids"]:
        by_domain[d][label]+=1
report={
 "schema":"hale-v14-full-rule-vector-v1",
 "birth_utc":"1994-01-27T22:35:00Z",
 "rule_count":len(rows),
 "source_map_sha256":hashlib.sha256(MAP.read_bytes()).hexdigest(),
 "summary":{
   "overall":dict(Counter("positive" if v>0 else "negative" if v<0 else "zero" for v in vals.tolist())),
   "by_source":{k:dict(v) for k,v in sorted(by_source.items())},
   "by_subject":{k:dict(v) for k,v in sorted(by_subject.items())},
   "by_domain":{k:dict(v) for k,v in sorted(by_domain.items())},
 },
 "rules":items,
}
OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print("rules",len(rows))
print("overall",report["summary"]["overall"])
print("by_source",report["summary"]["by_source"])
print("by_subject")
for k,v in report["summary"]["by_subject"].items():
    if v.get("positive",0) or v.get("negative",0): print(k,v)
print(hashlib.sha256(OUT.read_bytes()).hexdigest())
