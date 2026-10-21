#!/usr/bin/env python3
"""Differential calendar test against an independently authored, pinned MIT library.

Run e.g. python3 compare_t54_independent_tibcal.py
    --reference /tmp/hd-tibcal-ref-20261021 --output /tmp/t54-parity.json

The reference repository is **not** committed/vendor-copied into HumanDesign.
Source under test uses Janson formulas written separately; this checks two
independent implementations of a shared mathematical source, not astrological
human efficacy, actual astronomical sky or original Tibetan manuscript parity.
"""
import argparse
from datetime import date,timedelta
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
REFERENCE_SHA="01591b5bf03d038b864c4138fde3cc4285ca8001"
SOURCE_SHA="4110a30342f05dd58a4167634370db52b1baa436"


def load(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reference",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    ref=args.reference.resolve()
    commit=subprocess.check_output(["git","-C",str(ref),"rev-parse","HEAD"],text=True).strip()
    assert commit==REFERENCE_SHA, "reference commit changed; update after source review"
    license=(ref/"LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in license, "unexpected license"
    ours=load(ROOT/"batches/T54/tibetan_true_dates.py","tibetan_true_dates_t54_compare")
    theirs=load(ref/"public/tibetan_calendar.py","dorjeduck_tibcal_ref")
    output=[]
    total=0
    difference=[]
    years=(1950,1984,1985,2000,2024,2026)
    for system,epoch,ref_enum in (
        ("phugpa",1987,theirs.TibetanTradition.PHUGPA),
        ("tsurphu",1852,theirs.TibetanTradition.TSURPHU),
    ):
        for year in years:
            western=theirs.tibetan_calendar_for_year(year,ref_enum)
            ref_days={}
            for month in western.months:
                for d in month.days:
                    if d.is_skipped or d.gregorian is None or d.gregorian.year!=year:
                        continue
                    if d.gregorian in ref_days:
                        raise AssertionError("Reference duplicate Gregorian day")
                    ref_days[d.gregorian]=d
            first=date(year,1,1)
            length=(date(year+1,1,1)-first).days
            assert len(ref_days)==length,(system,year,len(ref_days),length)
            checked=0
            for i in range(length):
                day=first+timedelta(days=i)
                old=ref_days[day]
                new=ours.gregorian_day_to_tibetan(day,system=system,epoch=epoch,
                                                  anomaly_policy="rounded")
                left=(new.year,new.month,new.leap_month,new.lunar_day,
                      new.leap_day,new.jdn)
                right=(old.year,old.month,old.is_leap_month,old.day,
                       old.is_leap_day,old.julian_day)
                if left!=right:
                    difference.append({"system":system,"gregorian":day.isoformat(),
                                       "ours":left,"reference":right})
                checked+=1
            output.append({"system":system,"Gregorian_year":year,
                           "compared_days":checked})
            total+=checked
            print("DIFF",system,year,checked,"cumulative mismatches",len(difference),flush=True)
    receipt={
        "schema":"T54_PINNED_INDEPENDENT_COMPARISON_V1",
        "source_repo":"dorjeduck/tibcal",
        "reference_commit_sha":REFERENCE_SHA,
        "reference_license":"MIT",
        "original_base_commit":SOURCE_SHA,
        "reference_algorithm":"Janson Phugpa E806/Tsurphu E1852, code independently authored by upstream",
        "our_algorithm":"Janson Phugpa E1987/Tsurphu E1852, Fraction implementation",
        "source_code_vendored":False,
        "human_predictive_claims":0,
        "day_comparisons":total,
        "case_groups":output,
        "mismatches":difference[:100],
        "mismatch_count":len(difference),
        "status":"PARITY_PASS" if not difference else "PARITY_DISAGREEMENT"
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    if difference:
        raise SystemExit(f"{len(difference)} independent reference mismatches; see {args.output}")
    print(f"T54 INDEPENDENT PARITY PASS: {total} civil days both traditions across {len(years)} sampled years.")


if __name__=="__main__":
    main()
