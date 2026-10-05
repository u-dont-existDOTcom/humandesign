#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROTOCOL=ROOT/"reference"/"research"/"ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--timing",action="store_true")
    ap.add_argument("--exact-date",action="store_true")
    ap.add_argument("--cross-system",action="store_true")
    ap.add_argument("--subject-label",default="UNSET")
    args=ap.parse_args()
    conditions={
        "when timing is asked": bool(args.timing or args.exact_date),
        "when exact date/localization is asked": bool(args.exact_date),
        "when requested": bool(args.cross_system),
    }
    p=json.loads(PROTOCOL.read_text())
    rows=[]
    for item in p["required_passes"]:
        req=item["required"]
        active=req is True or (isinstance(req,str) and conditions.get(req,False))
        if not active:
            continue
        rows.append({
            "id":item["id"],
            "status":"TODO",
            "evidence":[],
            "reason":"",
            "check_results":{
                check:{"status":"TODO","evidence":[],"reason":""}
                for check in item.get("checks",[])
            },
        })
    out={
        "schema_version":1,
        "protocol_id":p["protocol_id"],
        "subject_label":args.subject_label,
        "conditions":conditions,
        "passes":rows,
        "claim_ledger":[],
        "final_synthesis_admitted":False,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2)+"\n")
    print(args.out)

if __name__=="__main__":
    main()
