from __future__ import annotations
import json, os
from datetime import UTC, datetime
from pathlib import Path
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot, score_snapshot

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent
EPHE=Path(os.environ["EPHEMERIS_ROOT"])
MAP=ROOT/"tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V13-TARGET-BLIND-CONSENSUS-MAP-20260924.json"
OUT=BASE/"ASTRO_DOMAIN_VOTES.json"

consensus=json.loads(MAP.read_text())
snapshot=build_snapshot(
    datetime(1994,1,27,22,35,tzinfo=UTC),
    latitude=41.0138429552247,
    longitude=28.9496612548828,
    ephemeris_root=EPHE,
)
weights={row["domain_id"]:1.0 for row in consensus["domains"]}
report=score_snapshot(snapshot,consensus_map=consensus,behavior_weights=weights)
report["note"]="Generic equal-domain inspection of the pre-existing target-blind consensus map; no Hale outcomes used. These domains originated in the project ontology and are corroborative, not a complete generic personality taxonomy."
OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(OUT)
