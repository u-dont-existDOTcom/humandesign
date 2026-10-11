#!/usr/bin/env python3
"""Frozen 2026-10-11 mundane astrology historical test.

Method freeze: reference/research/MUNDANE_HISTORICAL_EVENT_BACKTEST_FREEZE_20261011.md
Run from repository root:
    PYTHONPATH=/path/to/pyswisseph python3 scripts/research/mundane_historical_backtest_20261011.py --fetch
Re-run without --fetch from hashed source CSVs under data/mundane_historical_backtest_20261011.
Standard library + pyswisseph; no scientific/statistical packages needed.
"""
import argparse
import collections
import csv
import datetime as dt
import hashlib
import itertools
import json
import math
import pathlib
import random
import sys
import urllib.request

try:
    import swisseph as swe
except ImportError as ex:
    raise SystemExit("Install pyswisseph==2.10.3.2; import name is swisseph") from ex

BASE = pathlib.Path(__file__).resolve().parents[2]
SOURCES = BASE / "data" / "mundane_historical_backtest_20261011"
OUT = BASE / "reference" / "research" / "mundane_historical_backtest_20261011"
URLS = {
  "ERT_v16_OWID.csv": "https://ourworldindata.org/grapher/political-regime-ert-within-regimes.csv?v=1&csvType=full&useColumnShortNames=false",
  "Inter-StateWarData_v4.0.csv": "https://correlatesofwar.org/wp-content/uploads/Inter-StateWarData_v4.0.csv",
}
FLAG = swe.FLG_MOSEPH
NAMES = ("Saturn", "Uranus", "Neptune", "Pluto")
BODIES = (swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO)
PAIRS = list(itertools.combinations(range(4), 2))
COUNT_PERM = 20_000
SEED = 20261011

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fetch_inputs():
    SOURCES.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        req = urllib.request.Request(url, headers={"User-Agent":"Research reproducibility 2026-10-11 / Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=55) as response:
            data = response.read()
            if len(data) < 500: raise ValueError(f"Downloaded too little data: {url}")
        (SOURCES / name).write_bytes(data)
        print("FETCH", name, "bytes", len(data), "sha256", sha(data))

def mean(xs):
    return sum(xs)/len(xs) if xs else 0.0

def annual_exposures():
    records={}
    for y in list(range(1820,2026)) + list(range(2036,2086)):
        a=[0.,0.,0.,0.,0.]; n=0
        day=dt.date(y,1,1)
        end=dt.date(y+1,1,1)
        while day<end:
            jd=swe.julday(day.year, day.month, day.day, 0., swe.GREG_CAL)
            ll=[]
            for body in BODIES:
                vals, returned=swe.calc_ut(jd,body,FLAG)
                if not (returned & swe.FLG_MOSEPH): raise ValueError("Requested Moshier not returned")
                ll.append(vals[0])
            h=0; sat=0; out=0; soft=0
            for i,j in PAIRS:
                d=abs(ll[i]-ll[j])%360
                d=min(d,360-d)
                if min(abs(d-t) for t in (0.,90.,180.))<=3.:
                    h+=1
                    if i==0: sat+=1
                    else: out+=1
                if min(abs(d-t) for t in (60.,120.))<=3.:
                    soft+=1
            a[0]+=h;a[1]+=sat;a[2]+=out;a[3]+=int(h>=2);a[4]+=soft
            n+=1; day+=dt.timedelta(days=1)
        records[y]={"n_days":n,"hard_pair_days":a[0]/n,"saturn_hard":a[1]/n,
                    "outer_hard":a[2]/n,"concurrent_hard":a[3]/n,"soft_pair_days":a[4]/n}
    return records

def get_ert():
    d={}; invalid=0
    with (SOURCES/"ERT_v16_OWID.csv").open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        for row in reader:
            code=(row.get("Code") or "").strip()
            if len(code)!=3 or not code.isalpha():continue  # OWID regional aggregate identifiers excluded
            try: y=int(row["Year"]); regime=int(float(row["Political regime"]))
            except (ValueError,TypeError,KeyError):invalid+=1;continue
            if regime not in range(6):
                invalid+=1;continue
            key=(code,y)
            if key in d and d[key]!=regime:raise ValueError("ERT duplicate contradictory country/year "+str(key))
            d[key]=regime
    annual=collections.defaultdict(lambda:{"eligible":0,"onsets":0})
    for (code,y),regime in d.items():
        if not(1901<=y<=2024):continue
        prev=d.get((code,y-1))
        if prev in (1,4):
            annual[y]["eligible"]+=1
            if regime in (0,2,3,5): annual[y]["onsets"]+=1
    return annual,{"unique_country_years":len(d),"countries":len(set(c for c,y in d)),"invalid_skipped":invalid}

def get_wars():
    wars={}
    with (SOURCES/"Inter-StateWarData_v4.0.csv").open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        keys=reader.fieldnames
        if "WarNum" not in keys or "StartYear1" not in keys: raise ValueError("COW header mismatch: "+str(keys))
        for row in reader:
            id=(row["WarNum"] or "").strip()
            if not id:continue
            try: year=int(float(row["StartYear1"]))
            except (TypeError,ValueError):continue
            if not(1700<=year<=2100):continue
            if id not in wars or year<wars[id]:wars[id]=year
    annual=collections.Counter(y for y in wars.values() if 1820<=y<=2004)
    return annual,{"unique_wars_all_years":len(wars),"war_starts_in_scope":sum(annual.values()),"column":"WarNum+min(StartYear1)"}

def get_bins(astr,ert,war):
    def agg_years(first,last,typ):
        blocks=[]
        for first_y in range(first,last+1,5):
            yy=range(first_y,first_y+5)
            days=sum(astr[y]["n_days"] for y in yy)
            item={"start_year":first_y,"end_year":first_y+4,"period":f"{first_y}-{first_y+4}","n_days":days}
            for k in ("hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days"):
                item[k]=sum(astr[y][k]*astr[y]["n_days"] for y in yy)/days
            if typ=="ert":
                item["eligible_country_years"]=sum(ert[y]["eligible"] for y in yy)
                item["onsets"]=sum(ert[y]["onsets"] for y in yy)
                item["rate_per_100_eligible"]=100*item["onsets"]/item["eligible_country_years"] if item["eligible_country_years"] else None
                item["era"]=1900+25*((first_y-1900)//25)
            else:
                item["war_starts"]=sum(war[y] for y in yy)
                item["era"]=1820+25*((first_y-1820)//25)
            blocks.append(item)
        return blocks
    return agg_years(1900,2024,"ert"),agg_years(1820,2004,"wars")

def demean(vec,era):
    means={k:mean([v for v,z in zip(vec,era) if z==k]) for k in set(era)}
    return [float(v)-means[k] for v,k in zip(vec,era)]

def corr(x,y):
    nx=math.sqrt(sum(v*v for v in x))
    ny=math.sqrt(sum(v*v for v in y))
    return sum(a*b for a,b in zip(x,y))/(nx*ny) if nx>1e-12 and ny>1e-12 else None

def test(blocks,endpoint,series="hard_pair_days",run_nulls=True):
    valid=[z for z in blocks if z.get(endpoint) is not None]
    x=[z[series] for z in valid]
    y=[z[endpoint] for z in valid]
    era=[z["era"] for z in valid]
    xv=demean(x,era);yv=demean(y,era)
    obs=corr(xv,yv)
    ret={"predictor":series,"outcome":endpoint,"n_5yr_bins":len(x),
         "observed_detrended_pearson_r":obs,"all_years":str(valid[0]["start_year"])+"-"+str(valid[-1]["end_year"]),
         "eras":sorted(set(era))}
    if not run_nulls or obs is None:return ret
    rng=random.Random(SEED)
    group_idx=collections.defaultdict(list)
    for i,g in enumerate(era):group_idx[g].append(i)
    groups=list(group_idx.values())
    n_ge=0
    null_values=[]
    for _ in range(COUNT_PERM):
        perm_x=xv[:]
        for grp in groups:
            sh=[perm_x[i] for i in grp]
            rng.shuffle(sh)
            for i,v in zip(grp,sh):perm_x[i]=v
        res=corr(perm_x,yv)
        null_values.append(res)
        if res is not None and res >= obs-1e-14:n_ge+=1
    ret["permutation_seed"]=SEED
    ret["permutation_count"]=COUNT_PERM
    ret["permutation_ge_observed"]=n_ge
    ret["one_sided_permutation_p"]=(1+n_ge)/(COUNT_PERM+1)
    # Diagnostic only: rotate entire predictor by 5-year bins and recenter eras after shifting.
    n_better=0;shifted=[]
    for sh in range(1,len(x)):
        shifted_x=x[sh:]+x[:sh]
        r=corr(demean(shifted_x,era),yv)
        shifted.append(r)
        if r is not None and r>=obs-1e-14:n_better+=1
    ret["rotated_shift_diagnostic"]={"nonzero_rotations":len(shifted),"rotations_at_least_observed":n_better,
                                    "unshifted_rank_among_all":1+n_better,
                                    "fraction_all_at_least_observed":(1+n_better)/len(x)}
    # Predeclared descriptive top quartile by planetary intensity, not inferential substitution.
    order=sorted(range(len(x)),key=lambda i:(-x[i],valid[i]["start_year"]))
    top=set(order[:math.ceil(len(x)/4)])
    if endpoint=="rate_per_100_eligible":
        def rate(ids):
            den=sum(valid[i]["eligible_country_years"] for i in ids)
            return 100*sum(valid[i]["onsets"] for i in ids)/den if den else None
        high=rate(top);rest=rate(set(range(len(x)))-top)
    else:
        high=mean([y[i] for i in top]);rest=mean([y[i] for i in range(len(x)) if i not in top])
    ret["top_quartile_descriptive"]={"n_high":len(top),"high_mean_or_rate":high,"remaining_mean_or_rate":rest,
                                    "ratio_high_to_rest":high/rest if rest not in (None,0) else None,
                                    "high_periods":sorted(valid[i]["period"] for i in top)}
    return ret

def write_csv(path,rows,fields):
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        writer.writeheader();writer.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fetch",action="store_true",help="download pinned source URLs before analysis")
    args=ap.parse_args()
    if args.fetch:fetch_inputs()
    for name in URLS:
        if not(SOURCES/name).exists():raise SystemExit("Missing source CSV; pass --fetch: "+name)
    source_hashes={k:{"sha256":sha((SOURCES/k).read_bytes()),"bytes":(SOURCES/k).stat().st_size,"url":v}
        for k,v in URLS.items()}
    ex=annual_exposures()
    e,emeta=get_ert();w,wmeta=get_wars()
    eb,wb=get_bins(ex,e,w)
    assert len(eb)==25 and len(wb)==37
    assert all(b["eligible_country_years"]>0 for b in eb)
    assert all(b["hard_pair_days"]>=0 for b in eb+wb)
    primary_a=test(eb,"rate_per_100_eligible")
    primary_b=test(wb,"war_starts")
    exploratory={}
    for k in ("saturn_hard","outer_hard","concurrent_hard","soft_pair_days"):
        exploratory[k]={
          "ert":test(eb,"rate_per_100_eligible",k,False),
          "war":test(wb,"war_starts",k,False)
        }
    commons=[a for a in eb if a["start_year"]<=2000]
    common_wars=[a for a in wb if 1900<=a["start_year"]<=2000]
    exploratory["common_years"]={"ert":test(commons,"rate_per_100_eligible",run_nulls=False),
                                 "war":test(common_wars,"war_starts",run_nulls=False)}
    future=[]
    for first in range(2036,2086,5):
        yy=range(first,first+5)
        days=sum(ex[y]["n_days"] for y in yy)
        vals={"start_year":first,"end_year":first+4,"period":f"{first}-{first+4}"}
        for k in ("hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days"):
            vals[k]=sum(ex[y][k]*ex[y]["n_days"] for y in yy)/days
        future.append(vals)
    OUT.mkdir(parents=True,exist_ok=True)
    annual=[{"year":k,**v} for k,v in sorted(ex.items())]
    write_csv(OUT/"astrology_daily_activity_annual_1820_2085.csv",annual,["year","n_days","hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days"])
    write_csv(OUT/"ert_onsets_5yr_1900_2024.csv",eb,["period","start_year","end_year","n_days","hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days","eligible_country_years","onsets","rate_per_100_eligible","era"])
    write_csv(OUT/"cow_war_onsets_5yr_1820_2004.csv",wb,["period","start_year","end_year","n_days","hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days","war_starts","era"])
    write_csv(OUT/"future_astro_activity_5yr_2036_2085.csv",future,["period","start_year","end_year","hard_pair_days","saturn_hard","outer_hard","concurrent_hard","soft_pair_days"])
    metadata={"status":"historical-development-not-blind",
      "freeze_file":"reference/research/MUNDANE_HISTORICAL_EVENT_BACKTEST_FREEZE_20261011.md",
      "source_hashes":source_hashes,"swisseph_version":swe.version,"ephemeris_requested":"FLG_MOSEPH","orbs_deg":3.0,
      "years":{"ert": "1901-2024","cow":"1820-2004","future":"2036-2085"},
      "ert":emeta,"cow":wmeta,"primary_results":{"ert_onset":primary_a,"cow_interstate_war":primary_b},
      "significance_policy":{"two_co_primary_p_threshold_each":.025,"permutation_count":COUNT_PERM,"seed":SEED},
      "exploratory_results":exploratory,
      "future":future,
      "caveats":["historical development; analysts know notable events","outcomes proxy only political transitions and interstate war outbreaks",
      "V-Dem outcomes begin 1900 and wars end 2007","Moshier mode not SWIEPH production",
      "25-year era demeaning and permutations do not eliminate residual secular changes or serial dependence",
      "outer-planet rare contacts lack repeated historical test opportunities", "null does not refute all astrology; positive does not validate humanity forecast"]
      }
    (OUT/"MUNDANE_HISTORICAL_BACKTEST_RESULTS_20261011.json").write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ERT:",json.dumps(primary_a,indent=2))
    print("WAR:",json.dumps(primary_b,indent=2))
    print("SOURCE_HASHES",json.dumps(source_hashes))
    print("FUTURE_TOP",sorted(future,key=lambda v:-v["hard_pair_days"])[:5])
    print("OUTPUT_DIRECTORY",OUT)
if __name__=="__main__":main()
