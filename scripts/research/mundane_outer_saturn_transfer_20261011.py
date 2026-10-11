#!/usr/bin/env python3
"""Post-discovery Saturn/outer hard-aspect transfer test (2026-10-11).

Freeze: reference/research/MUNDANE_OUTER_VS_SATURN_FOLLOWUP_FREEZE_20261011.md
Inputs: historical astronomy and two old datasets frozen on 2026-10-11;
        Powell–Thyne Aug 2026 coups; UCDP intrastate conflict onset v25.1.
No new aspect fitting; use only original 3-degree / Moshier hard-geometry index.
"""
import argparse
import urllib.request
import collections
import csv
import hashlib
import importlib.util
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
OLD=ROOT/"reference/research/mundane_historical_backtest_20261011"
SRC=ROOT/"data/mundane_outer_saturn_transfer_20261011"
OUT=ROOT/"reference/research/mundane_outer_saturn_transfer_20261011"
OLD_CALC=ROOT/"scripts/research/mundane_historical_backtest_20261011.py"
FILES={
  "powell_thyne_20260829.csv":{
   "sha256":"1e8f933b22f4b9a77d0ba5eb59bf0d8158adcaab27746adcf345195be87a9012",
   "source_url":"https://jonathanmpowell.com/wp-content/uploads/2026/08/pt_20260829.csv"},
  "ucdp_intrastate_conflict_onset_251.csv":{
   "sha256":"a5a64b749693c85fd3b50a1311608a44c0846d528352baeb3767f25e50d52fe1",
   "source_url":"https://ucdp.uu.se/downloads/onset/ucdp-intrastate-conflict-onset-251.csv"}}
YEARS=range(1950,2025)
PRIMARY=("coup_attempts","ucdp_intrastate_onsets")
ASTRO_FIELDS=("hard_pair_days","outer_hard","saturn_hard","concurrent_hard","soft_pair_days")

spec=importlib.util.spec_from_file_location("original_mundane",OLD_CALC)
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
old.SEED=20261012
assert old.COUNT_PERM==20000

def fetch_verified_source_data():
    """Get pinned original CSVs if absent; never silently overwrite changed snapshots."""
    SRC.mkdir(parents=True,exist_ok=True)
    for name, meta in FILES.items():
        path=SRC/name
        if path.exists():
            got=hashlib.sha256(path.read_bytes()).hexdigest()
            if got!=meta["sha256"]:raise RuntimeError("Local source differs from frozen SHA: "+name)
            continue
        request=urllib.request.Request(meta["source_url"],
             headers={"User-Agent":"Historical academic research / Mozilla/5.0"})
        with urllib.request.urlopen(request,timeout=60) as response:
            data=response.read()
        got=hashlib.sha256(data).hexdigest()
        if got!=meta["sha256"]:
            raise RuntimeError("Upstream source changed; obtain frozen original snapshot: "+name+" "+got)
        path.write_bytes(data)

def read_csv(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def read_coups(path):
    rows=read_csv(path)
    needed={"country","ccode","year","month","day","coup"}
    if not rows or not needed.issubset(rows[0]):raise ValueError("Coups source schema changed")
    annual=collections.Counter()
    successful=collections.Counter()
    seen=set()
    excluded=0
    for row in rows:
        y=int(row["year"])
        if y not in YEARS:excluded+=1;continue
        status=row["coup"].strip()
        if status not in {"1","2"}:raise ValueError("Unrecognized coup status")
        mo=int(row["month"]);day=int(row["day"])
        import datetime
        datetime.date(y,mo,day) # date must be valid
        code=row["ccode"].strip()
        if not code:raise ValueError("Missing country code")
        key=(code,y,mo,day)
        if key in seen:raise ValueError("Duplicated coup date/country; requires explicit source ID")
        seen.add(key);annual[y]+=1
        if status=="2":successful[y]+=1
    return annual,successful,{"rows_total":len(rows),"out_of_scope":excluded,"events_in_scope":len(seen),
          "successful_in_scope":sum(successful.values())}

def read_conflicts(path):
    rows=read_csv(path)
    required={"abc","year","onset1","conflict_ids"}
    if not rows or not required.issubset(rows[0]):raise ValueError("UCDP onset source schema changed")
    annual=collections.Counter()
    seen=set();excluded=0;skipped_no_onset=0
    for row in rows:
        y=int(row["year"])
        if y not in YEARS:excluded+=1;continue
        onset=row["onset1"].strip()
        if onset not in {"0","1"}:raise ValueError("Unexpected UCDP onset1 value")
        if onset=="0":skipped_no_onset+=1;continue
        cid=row["conflict_ids"].strip()
        if not cid or not cid.isdigit():raise ValueError("Missing/ambiguous conflict id")
        abc=row["abc"].strip()
        if not abc:raise ValueError("Missing UCDP country code")
        key=(abc,y,cid)
        if key in seen:raise ValueError("Duplicate UCDP conflict_id/country/year")
        seen.add(key)
        annual[y]+=1
    return annual,{"rows_total":len(rows),"out_of_scope":excluded,"inactive_rows":skipped_no_onset,
        "onsets_in_scope":len(seen),"onset_field":"onset1",
        "uniqueness":"country code + conflict_ids + year"}

def load_astro():
    rows=read_csv(OLD/"astrology_daily_activity_annual_1820_2085.csv")
    arr={}
    for r in rows:
        row={"year":int(r["year"]),"n_days":int(r["n_days"])}
        for key in ASTRO_FIELDS:row[key]=float(r[key])
        arr[row["year"]]=row
    assert set(YEARS).issubset(arr)
    return arr

def aggregate(astro,coup,success,conf):
    blocks=[]
    for start in range(1950,2025,5):
        years=range(start,start+5)
        days=sum(astro[y]["n_days"] for y in years)
        b={"period":f"{start}-{start+4}","start_year":start,"end_year":start+4,
            "era":1950+25*((start-1950)//25),"n_days":days,
            "coup_attempts":sum(coup[y] for y in years),
            "coup_successes":sum(success[y] for y in years),
            "ucdp_intrastate_onsets":sum(conf[y] for y in years)}
        for field in ASTRO_FIELDS:
            b[field]=sum(astro[y][field]*astro[y]["n_days"] for y in years)/days
        b["outer_minus_saturn"]=b["outer_hard"]-b["saturn_hard"]
        assert abs(b["outer_minus_saturn"]-(b["outer_hard"]-b["saturn_hard"]))<1e-10
        blocks.append(b)
    assert len(blocks)==15
    return blocks

def load_parent():
    e=read_csv(OLD/"ert_onsets_5yr_1900_2024.csv")
    w=read_csv(OLD/"cow_war_onsets_5yr_1820_2004.csv")
    for rows,field in ((e,"rate_per_100_eligible"),(w,"war_starts")):
        for r in rows:
            for k in ASTRO_FIELDS:r[k]=float(r[k])
            r[field]=float(r[field])
            for k in ("start_year","end_year","era"):r[k]=int(r[k])
            r["outer_minus_saturn"]=r["outer_hard"]-r["saturn_hard"]
            if field=="rate_per_100_eligible":
                r["onsets"]=int(r["onsets"])
                r["eligible_country_years"]=int(r["eligible_country_years"])
    return e,w

def score(rows,outcome,predictor="outer_minus_saturn",run_nulls=True):
    # The unchanged first-study test uses 25-year era centering and 20k within-era permutations.
    return old.test(rows,outcome,series=predictor,run_nulls=run_nulls)

def diagnostic(rows,outcome):
    results={}
    for predictor in ("outer_minus_saturn","outer_hard","saturn_hard","hard_pair_days",
                      "concurrent_hard","soft_pair_days"):
        results[predictor]=score(rows,outcome,predictor,
             run_nulls=(predictor=="outer_minus_saturn"))
    eras=sorted(set(r["era"] for r in rows))
    loo={}
    for era in eras:
        left=[r for r in rows if r["era"]!=era]
        loo[str(era)]=score(left,outcome,run_nulls=False)["observed_detrended_pearson_r"]
    results["leave_one_25y_era_out"]=loo
    return results

def save_csv(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch",action="store_true",help="fetch exact SHA-pinned source CSVs if missing")
    args=parser.parse_args()
    if args.fetch:fetch_verified_source_data()
    missing=[name for name in FILES if not (SRC/name).exists()]
    if missing:
        raise RuntimeError("Missing original research CSV(s): "+str(missing)+". Run with --fetch.")
    manifest={}
    for fname, expected in FILES.items():
        src=SRC/fname
        data=src.read_bytes()
        actual=hashlib.sha256(data).hexdigest()
        if actual!=expected["sha256"]:
            raise RuntimeError(f"Source hash changed! {fname}: {actual} != {expected['sha256']}")
        manifest[fname]={**expected,"bytes":len(data)}
    astro=load_astro()
    c,success,c_meta=read_coups(SRC/"powell_thyne_20260829.csv")
    u,u_meta=read_conflicts(SRC/"ucdp_intrastate_conflict_onset_251.csv")
    b=aggregate(astro,c,success,u)
    old_ert,old_war=load_parent()
    primary={k:diagnostic(b,k) for k in PRIMARY}
    secondary={
      "coup_successes":diagnostic(b,"coup_successes"),
      "ert_original_discovery":diagnostic(old_ert,"rate_per_100_eligible"),
      "war_1820_2004":diagnostic(old_war,"war_starts"),
      "war_1950_2004":diagnostic([r for r in old_war if 1950<=r["start_year"]<=2000],"war_starts")
    }
    def two_periods(data,outcome):
        partitions=[
            ("1950-1984",[z for z in data if z["start_year"]<=1980]),
            ("1985-2024",[z for z in data if z["start_year"]>=1985])]
        return {name:{"n_blocks":len(series),
                 "detrended_r":score(series,outcome,run_nulls=False)["observed_detrended_pearson_r"]}
                for name,series in partitions}
    splits={k:two_periods(b,k) for k in PRIMARY}
    # Preselected severe sensitivity: remove the 1990-94 block from the discovery-only ERT series.
    ert_no_1990=[z for z in old_ert if z["start_year"]!=1990]
    secondary["ert_excluding_1990_1994"]=score(ert_no_1990,"rate_per_100_eligible")
    alpha=.025
    requirements={}
    for key in PRIMARY:
        a=primary[key]
        ar=a["outer_minus_saturn"]
        sign_ok=(a["outer_hard"]["observed_detrended_pearson_r"] is not None
              and a["outer_hard"]["observed_detrended_pearson_r"]>0
              and a["saturn_hard"]["observed_detrended_pearson_r"] is not None
              and a["saturn_hard"]["observed_detrended_pearson_r"]<0)
        loo=list(a["leave_one_25y_era_out"].values())
        stable=all(x is not None and x>0 for x in loo)
        p=ar["one_sided_permutation_p"]
        requirements[key]={"passes_bonferroni":bool(p<alpha),
          "components_reproduce_split":sign_ok,"all_era_omissions_positive":stable}
    replicated=all(all(x.values()) for x in requirements.values())
    result={
      "version":"mundane-outer-vs-saturn-transfer-v1",
      "freeze":"reference/research/MUNDANE_OUTER_VS_SATURN_FOLLOWUP_FREEZE_20261011.md",
      "status":"SIGNAL_REPLICATED_IN_DIFFERENT_ENDPOINT" if replicated else "UNSUPPORTED",
      "interpretation":"POST_DISCOVERY_DEVELOPMENT; not an independent blind/prospective test",
      "orb_degrees":3,"ephemeris_source":"pinned original annual daily MOSEPH",
      "outcome_period":"1950-2024","unit":"15 fixed 5-year blocks",
      "source_manifest":manifest,
      "earlier_astronomy_csv_sha256":hashlib.sha256((OLD/"astrology_daily_activity_annual_1820_2085.csv").read_bytes()).hexdigest(),
      "earlier_ert_csv_sha256":hashlib.sha256((OLD/"ert_onsets_5yr_1900_2024.csv").read_bytes()).hexdigest(),
      "earlier_cow_csv_sha256":hashlib.sha256((OLD/"cow_war_onsets_5yr_1820_2004.csv").read_bytes()).hexdigest(),
      "outcome_audit":{"coups":c_meta,"ucdp":u_meta},
      "seed":old.SEED,"permutations":old.COUNT_PERM,"bonferroni_alpha_each":alpha,
      "primary":primary,"requirements":requirements,
      "chronological_splits":splits,
      "secondary_and_discovery":secondary,
      "not_independent_evidence":["Any ERT result: index directions selected from ERT",
       "UCDP intrastate onsets and coup attempts share some episodes",
       "new outcomes transfer endpoints, not person/era-blind validation",
       "20k era permutations ignore some serial dependence; shifted rotations are diagnostic",
       "the 2061/2079 unusual alignments have few repeated historical analogues"]
      }
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"transfer_results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    save_csv(OUT/"independent_outcomes_1950_2024_5yr.csv",b)
    annual=[{"year":y,"coup_attempts":c[y],"coup_successes":success[y],
              "ucdp_intrastate_onsets":u[y],
              "outer_hard":astro[y]["outer_hard"],"saturn_hard":astro[y]["saturn_hard"],
              "outer_minus_saturn":astro[y]["outer_hard"]-astro[y]["saturn_hard"]}
            for y in YEARS]
    save_csv(OUT/"independent_outcomes_1950_2024_annual.csv",annual)
    print("OUTCOME_AUDIT",json.dumps(result["outcome_audit"]))
    for outcome in PRIMARY:
        print("TRANSFER",outcome)
        for key in ("outer_minus_saturn","outer_hard","saturn_hard","hard_pair_days"):
            v=primary[outcome][key]
            print(key,round(v["observed_detrended_pearson_r"],4),
                 "p",v.get("one_sided_permutation_p","exploratory"),"rotations",v.get("rotated_shift_diagnostic"))
        print("LOO",primary[outcome]["leave_one_25y_era_out"])
        print("SPLIT",splits[outcome])
    print("OLD_ERT_SPLIT",{k:round(secondary["ert_original_discovery"][k]["observed_detrended_pearson_r"],3)
          for k in ("outer_minus_saturn","outer_hard","saturn_hard")})
    print("ERT_REMOVE_1990",secondary["ert_excluding_1990_1994"]["observed_detrended_pearson_r"])
    print("PRIMARY_REPLICATION",result["status"],json.dumps(requirements))
    print("RESULTS",OUT)
if __name__=="__main__":main()
