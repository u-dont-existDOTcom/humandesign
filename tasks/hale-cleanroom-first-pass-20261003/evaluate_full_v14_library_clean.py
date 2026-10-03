from __future__ import annotations
import json, os
from datetime import UTC, datetime
from pathlib import Path
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent
EPHE=Path(os.environ["EPHEMERIS_ROOT"])
MAP=ROOT/"tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V13-TARGET-BLIND-CONSENSUS-MAP-20260924.json"
OUT=BASE/"ASTRO_V14_FULL_RULE_VECTOR_CLEAN.json"

consensus=json.loads(MAP.read_text())
rules=registry(consensus,{d["domain_id"] for d in consensus["domains"]})
snapshot=build_snapshot(
    datetime(1994,1,27,22,35,tzinfo=UTC),
    latitude=41.0138429552247,
    longitude=28.9496612548828,
    ephemeris_root=EPHE,
)
values=feature_row(snapshot,rules)
rows=[]
summary={}
for rule,value in zip(rules,values.tolist()):
    src=rule["source_id"]
    bucket=summary.setdefault(src,{"positive":0,"negative":0,"zero":0})
    bucket["positive" if value>0 else "negative" if value<0 else "zero"]+=1
    rows.append({
        "rule_id":rule["rule_id"],
        "source_id":src,
        "subject":rule["subject"],
        "condition":rule["condition"],
        "lineage_key":rule["lineage_key"],
        "supported_domain_ids":rule["supported_domain_ids"],
        "value":int(value),
    })
report={
    "schema":"hale-astrohd-v14-full-rule-vector-clean-v1",
    "classification":"outcome-blind source-grounded feature vector; not a generic personality score",
    "birth_utc":"1994-01-27T22:35:00Z",
    "location":{"latitude":41.0138429552247,"longitude":28.9496612548828,"role":"Istanbul city proxy"},
    "rule_count":len(rows),
    "summary_by_source":summary,
    "rules":rows,
}
OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(OUT)
print("rule_count",len(rows))
print(json.dumps(summary,sort_keys=True))
