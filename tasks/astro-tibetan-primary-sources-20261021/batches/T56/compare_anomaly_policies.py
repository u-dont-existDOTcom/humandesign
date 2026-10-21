#!/usr/bin/env python3
"""Measure whether Janson's rounded and Dharmashri/Henning exact anomaly
increments change calendar-day numbers. Pure model sensitivity, not human
evidence. Both source versions remain accepted and separate.
"""
from pathlib import Path
import argparse
from datetime import date
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"T54/tibetan_true_dates.py"
spec=importlib.util.spec_from_file_location("tibetan_dates_sensitivity",p)
assert spec and spec.loader
t=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=t
spec.loader.exec_module(t)

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",required=True,type=Path)
    a.add_argument("--first-year",default=1987,type=int)
    a.add_argument("--last-year",default=2051,type=int)
    x=a.parse_args()
    if x.last_year-x.first_year!=64:
        raise ValueError("Expected exactly 65 Tibetan-year labels for fixed denominator")
    receipt={
        "schema":"T56_JANSON_LUNAR_ANOMALY_ALTERNATIVE_SENSITIVITY_V1",
        "source":"Janson 2014 §7 Remark14; Dharmashri/Henning a2 exact Eq7.24",
        "tested_years":[x.first_year,x.last_year],
        "methods":["rounded:1/28","dharmashri_exact:3781/105840"],
        "systems":{},
        "human_prediction_successes":0,
        "source_note_increment":0,
    }
    for sysname,epoch in (("phugpa",1987),("tsurphu",1852)):
        checked=0
        changes=[]
        losar_changes=[]
        for y in range(x.first_year,x.last_year+1):
            a0=t.losar_jdn(y,system=sysname,epoch=epoch,anomaly_policy="rounded")
            a1=t.losar_jdn(y,system=sysname,epoch=epoch,anomaly_policy="dharmashri_exact")
            if a0!=a1:
                losar_changes.append({"year":y,"rounded":a0,"exact":a1})
            for month in range(1,13):
                for true_month,is_leap in t.month_instances(y,month,system=sysname,epoch=epoch):
                    for d in range(1,31):
                        z0=t.true_date_jdn(d,true_month,system=sysname,epoch=epoch,
                                           anomaly_policy="rounded")
                        z1=t.true_date_jdn(d,true_month,system=sysname,epoch=epoch,
                                           anomaly_policy="dharmashri_exact")
                        checked+=1
                        if z0!=z1:
                            changes.append({
                                "Tibetan_year":y,"month":month,"leap_month":is_leap,
                                "lunar_day":d,"rounded_jdn":z0,"exact_jdn":z1,
                                "day_number_change":z1-z0,
                            })
        receipt["systems"][sysname]={
            "epoch":epoch,
            "tithi_ends_compared":checked,
            "tithi_end_JDN_disagreements":len(changes),
            "disagreement_first_20":changes[:20],
            "Losar_disagreements":len(losar_changes),
            "Losar_disagreement_examples":losar_changes[:20]
        }
        print(sysname,checked,"tithi-end JDN disagreements",len(changes),
              "Losar disagreements",len(losar_changes),flush=True)
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print("SOURCE VARIANT SENSITIVITY ONLY: not a human prognostic comparison.")

if __name__=="__main__":
    main()
