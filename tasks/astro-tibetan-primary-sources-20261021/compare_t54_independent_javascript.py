#!/usr/bin/env python3
"""Phugpa daily differential parity against a pinned independent JavaScript library.

No JS upstream source is vendored; dependency installation is outside this repo,
using npm ci --omit=dev --ignore-scripts --no-audit --no-fund in a temp clone.
"""
from datetime import date,timedelta
from pathlib import Path
import argparse
import importlib.util
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
PIN="7651b8b579c8332442198cc0d9ca14d0b0e8b3a8"
JS_CODE=r"""
import fs from "node:fs";
import {pathToFileURL} from "node:url";
const root=process.argv[1];
const m=await import(pathToFileURL(root+"/src/index.js").href);
let data=JSON.parse(fs.readFileSync(0,"utf8"));
let out=[];
for (const [y,mn,d] of data) {
 const x=new m.CalendarTibetan().fromGregorian(y,mn,d).get();
 // 17th Rabjung cycle starts in 1987.
 out.push([1987+60*(x[0]-17)+(x[1]-1),x[2],x[3],x[4],x[5]]);
}
process.stdout.write(JSON.stringify(out));
"""

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--reference",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    opt=p.parse_args()
    ref=opt.reference.resolve()
    got=subprocess.check_output(["git","-C",str(ref),"rev-parse","HEAD"],text=True).strip()
    assert got==PIN
    assert "MIT License" in (ref/"LICENSE").read_text(encoding="utf8")
    assert (ref/"node_modules/astronomia").is_dir(), "npm ci --omit=dev --ignore-scripts required"
    src=ROOT/"batches/T54/tibetan_true_dates.py"
    spec=importlib.util.spec_from_file_location("t54_self_js_compare",src)
    assert spec and spec.loader
    ours=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=ours
    spec.loader.exec_module(ours)
    yrs=(1950,1984,1985,2000,2024,2026)
    days=[date(y,1,1)+timedelta(days=d)
          for y in yrs for d in range((date(y+1,1,1)-date(y,1,1)).days)]
    inp=[[d.year,d.month,d.day] for d in days]
    result=subprocess.run(
        ["node","--input-type=module","--eval",JS_CODE,str(ref)],
        input=json.dumps(inp),text=True,capture_output=True,check=True,
        timeout=180)
    external=json.loads(result.stdout)
    assert len(external)==len(days)
    errors=[]
    for day,other in zip(days,external):
        calc=ours.gregorian_day_to_tibetan(day,system="phugpa",epoch=1987,
                                          anomaly_policy="rounded")
        own=[calc.year,calc.month,calc.leap_month,calc.lunar_day,calc.leap_day]
        if own!=other:
            errors.append({"Gregorian":day.isoformat(),"ours":own,"external_js":other})
    receipt={
       "schema":"T54_INDEPENDENT_JS_PARITY_V1",
       "external_repo":"hnw/date-tibetan",
       "git_commit":PIN,
       "external_package_license":"MIT",
       "npm_install":"npm ci --omit=dev --ignore-scripts --no-audit --no-fund",
       "tested_system":"Phugpa only (JS library does not implement Tsurphu)",
       "source_based_engine":"T54 Janson rational E1987 rounded anomaly",
       "original_upstream_code_in_our_repository":False,
       "years":list(yrs),"compared_day_count":len(days),
       "disagreements":len(errors),"disagreement_examples":errors[:100],
       "status":"PASS" if not errors else "DISAGREEMENT",
       "human_predictive_tests":0
    }
    opt.output.parent.mkdir(parents=True,exist_ok=True)
    opt.output.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    if errors:
        raise SystemExit(f"JS comparison disagrees on {len(errors)} days")
    print(f"T54 INDEPENDENT JS PARITY PASS: {len(days)} Phugpa days, source pinned {PIN[:12]}")

if __name__=="__main__":
    main()
