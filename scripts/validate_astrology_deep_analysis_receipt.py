#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "reference" / "research" / "ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json"
ALLOWED = {"APPLIED","NOT_APPLICABLE","UNAVAILABLE","SUPERSEDED"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("receipt",type=Path)
    args=ap.parse_args()
    protocol=json.loads(PROTOCOL.read_text())
    receipt=json.loads(args.receipt.read_text())
    rows={r["id"]:r for r in receipt.get("passes",[])}
    errors=[]
    for p in protocol["required_passes"]:
        req=p["required"]
        active = req is True or (isinstance(req,str) and receipt.get("conditions",{}).get(req,False))
        if not active:
            continue
        row=rows.get(p["id"])
        if row is None:
            errors.append(f"missing required pass {p['id']}")
            continue
        status=row.get("status")
        if status not in ALLOWED:
            errors.append(f"{p['id']}: invalid status {status!r}")
            continue
        if status=="APPLIED" and not row.get("evidence"):
            errors.append(f"{p['id']}: APPLIED requires evidence")
        if status!="APPLIED" and not row.get("reason"):
            errors.append(f"{p['id']}: {status} requires reason")
        if status=="APPLIED" and protocol.get("synthesis_gate",{}).get("require_subcheck_disposition"):
            sub=row.get("check_results",{})
            for check in p.get("checks",[]):
                result=sub.get(check)
                if not isinstance(result,dict):
                    errors.append(f"{p['id']}: missing subcheck disposition: {check}")
                    continue
                sub_status=result.get("status")
                if sub_status not in {"DONE","NOT_APPLICABLE","UNAVAILABLE","SUPERSEDED"}:
                    errors.append(f"{p['id']}: invalid subcheck status {sub_status!r}: {check}")
                    continue
                if sub_status=="DONE" and not result.get("evidence"):
                    errors.append(f"{p['id']}: DONE subcheck requires evidence: {check}")
                if sub_status!="DONE" and not result.get("reason"):
                    errors.append(f"{p['id']}: {sub_status} subcheck requires reason: {check}")
    if protocol.get("claim_ledger_contract",{}).get("required_for_saved_substantive_analysis"):
        claims=receipt.get("claim_ledger",[])
        if not claims:
            errors.append("missing required claim_ledger")
        else:
            required=set(protocol["claim_ledger_contract"]["fields"])
            stable=set(protocol["claim_ledger_contract"]["allowed_stability_class"])
            evid=set(protocol["claim_ledger_contract"]["allowed_evidence_status"])
            for i,claim in enumerate(claims):
                missing=required-set(claim)
                if missing:
                    errors.append(f"claim_ledger[{i}] missing fields: {sorted(missing)}")
                    continue
                if not claim.get("support_refs"):
                    errors.append(f"claim_ledger[{i}] requires support_refs")
                if claim.get("stability_class") not in stable:
                    errors.append(f"claim_ledger[{i}] invalid stability_class")
                if claim.get("evidence_status") not in evid:
                    errors.append(f"claim_ledger[{i}] invalid evidence_status")

    if errors:
        print(json.dumps({"valid":False,"errors":errors},indent=2))
        raise SystemExit(1)
    print(json.dumps({"valid":True,"required_passes_checked":sum(1 for p in protocol["required_passes"] if p["required"] is True or (isinstance(p["required"],str) and receipt.get("conditions",{}).get(p["required"],False)))},indent=2))

if __name__=="__main__":
    main()
