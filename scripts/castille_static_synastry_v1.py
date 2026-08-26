#!/usr/bin/env python3
"""Large-N independent static synastry test on Didier Castille a00 data.

Frozen spec: reference/research/castille_static_synastry_freeze_v1.md
The source rows are downloaded at runtime; only aggregate model results are
committed. Astrology is never used to create splits or synthetic negatives.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import statistics
import urllib.request
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
FREEZE = REPO / "reference" / "research" / "castille_static_synastry_freeze_v1.md"
OUT = REPO / "reference" / "research" / "castille_static_synastry_results_v1.json"
URL = "https://raw.githubusercontent.com/tig12/g5-other/main/castille/a00/a00.csv.zip"

SEED = 202608261432
ALPHAS = (1e-5, 1e-4, 1e-3, 1e-2)
CAPS = {"discovery": 100_000, "validation": 60_000, "final": 100_000}
RISK_TASKS = 20_000
RISK_DECOYS = 20
ASPECTS = (0.0, 60.0, 90.0, 120.0, 180.0)
SIGMA = 3.0
BODY_NAMES = ("Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")
BODY_IDS = (swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN)
FLAGS = swe.FLG_SWIEPH
EPH_MASK = swe.FLG_JPLEPH | swe.FLG_SWIEPH | swe.FLG_MOSEPH
BASE_NAMES = (
    "mother_age_at_wedding",
    "father_age_at_wedding",
    "mother_minus_father_age",
    "absolute_age_difference",
    "wedding_year_scaled",
    "mother_birth_year_scaled",
    "father_birth_year_scaled",
)
SYN_NAMES = tuple(
    f"syn_{ma}_{fb}_a{int(asp)}"
    for ma in BODY_NAMES for fb in BODY_NAMES for asp in ASPECTS
)
ALL_NAMES = BASE_NAMES + SYN_NAMES


@dataclass(frozen=True)
class Record:
    mother: tuple[int, int, int]
    father: tuple[int, int, int]
    wedding: tuple[int, int, int]
    digest: str
    split: str

    @property
    def canonical(self) -> str:
        return canonical(self.mother, self.father, self.wedding)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(m: tuple[int, int, int], f: tuple[int, int, int], w: tuple[int, int, int]) -> str:
    def s(x): return f"{x[0]:04d}-{x[1]:02d}-{x[2]:02d}"
    return f"{s(m)}|{s(f)}|{s(w)}"


def split_for_digest(digest: str) -> str:
    bucket = int(digest[:8], 16) % 100
    if bucket <= 39:
        return "discovery"
    if bucket <= 59:
        return "validation"
    return "final"


def valid_date(y: int, m: int, d: int) -> bool:
    try:
        date(y, m, d)
        return True
    except Exception:
        return False


def iv(row: dict[str, str], key: str) -> int:
    try:
        return int((row.get(key) or "0").strip())
    except Exception:
        return 0


def parse_dob(row: dict[str, str], who: str) -> tuple[int, int, int] | None:
    if who == "m":
        d, m, y = iv(row, "JNAISM"), iv(row, "MNAISM"), iv(row, "ANAISM")
    else:
        d, m, y = iv(row, "JNAISP"), iv(row, "MNAISP"), iv(row, "ANAISP")
    return (y, m, d) if valid_date(y, m, d) else None


def parse_wedding(row: dict[str, str]) -> tuple[int, int, int] | None:
    d, m, y = iv(row, "JMAR"), iv(row, "MMAR"), iv(row, "AMAR")
    return (y, m, d) if valid_date(y, m, d) else None


def age_years(birth: tuple[int, int, int], event: tuple[int, int, int]) -> float:
    return (date(*event) - date(*birth)).days / 365.2425


def download_records() -> tuple[list[Record], int, dict]:
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-castille-synastry/1.0"})
    with urllib.request.urlopen(req, timeout=180) as response:
        raw = response.read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
    if len(csv_names) != 1:
        raise RuntimeError(f"expected one CSV, got {csv_names}")

    seen: set[str] = set()
    records: list[Record] = []
    counts = defaultdict(int)
    with z.open(csv_names[0]) as fb:
        text = io.TextIOWrapper(fb, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.DictReader(text, delimiter=";")
        for row in reader:
            counts["source_rows"] += 1
            m = parse_dob(row, "m"); f = parse_dob(row, "f"); w = parse_wedding(row)
            if m is None or f is None or w is None:
                counts["missing_or_invalid_required_date"] += 1
                continue
            ma = age_years(m, w); fa = age_years(f, w)
            if not (14.0 <= ma <= 85.0 and 14.0 <= fa <= 85.0):
                counts["implausible_parent_age"] += 1
                continue
            c = canonical(m, f, w)
            if c in seen:
                counts["exact_tuple_duplicate"] += 1
                continue
            seen.add(c)
            digest = hashlib.sha256(c.encode("utf-8")).hexdigest()
            records.append(Record(m, f, w, digest, split_for_digest(digest)))
    counts["unique_eligible_tuples"] = len(records)
    return records, len(raw), dict(counts)


def cap_splits(records: list[Record]) -> dict[str, list[Record]]:
    out = {}
    for split, cap in CAPS.items():
        rows = sorted((r for r in records if r.split == split), key=lambda r: (r.digest, r.canonical))
        out[split] = rows[:cap]
    return out


def make_matched_pairs(rows: list[Record]) -> tuple[list[tuple[Record, tuple[int, int, int]]], dict]:
    strata: dict[tuple[int, int], list[Record]] = defaultdict(list)
    for r in rows:
        strata[(r.wedding[0], r.father[0])].append(r)
    for vals in strata.values():
        vals.sort(key=lambda r: (r.digest, r.canonical))

    pairs: list[tuple[Record, tuple[int, int, int]]] = []
    dropped = defaultdict(int)
    for vals in strata.values():
        n = len(vals)
        distinct = {r.father for r in vals}
        if len(distinct) < 2:
            dropped["stratum_no_distinct_alternative_father_dob"] += n
            continue
        for i, r in enumerate(vals):
            synth = None
            for step in range(1, n + 1):
                cand = vals[(i + step) % n].father
                if cand != r.father:
                    synth = cand
                    break
            if synth is None:
                dropped["unexpected_no_alternative"] += 1
            else:
                pairs.append((r, synth))
    return pairs, dict(dropped)


def jd_for_birth(dob: tuple[int, int, int], hour: float) -> float:
    return swe.julday(dob[0], dob[1], dob[2], hour, swe.GREG_CAL)


def planet_positions(dates: set[tuple[int, int, int]], hour: float) -> dict[tuple[int, int, int], np.ndarray]:
    out: dict[tuple[int, int, int], np.ndarray] = {}
    for idx, dob in enumerate(sorted(dates), 1):
        jd = jd_for_birth(dob, hour)
        vals = []
        for body in BODY_IDS:
            xx, ret = swe.calc_ut(jd, body, FLAGS)
            used = ret & EPH_MASK
            if used != swe.FLG_SWIEPH:
                raise RuntimeError(f"EPHEMERIS_FALLBACK dob={dob} body={body} used={used} ret={ret}")
            vals.append(float(xx[0] % 360.0))
        out[dob] = np.asarray(vals, dtype=np.float32)
        if idx % 5000 == 0:
            print(f"computed natal positions {idx}/{len(dates)} at hour={hour}", flush=True)
    return out


def baseline_features(m: tuple[int,int,int], f: tuple[int,int,int], w: tuple[int,int,int]) -> np.ndarray:
    ma = age_years(m, w); fa = age_years(f, w)
    signed = ma - fa
    return np.asarray([
        ma, fa, signed, abs(signed),
        (w[0] - 1985.0) / 20.0,
        (m[0] - 1965.0) / 20.0,
        (f[0] - 1960.0) / 20.0,
    ], dtype=np.float32)


def syn_features(pm: np.ndarray, pf: np.ndarray) -> np.ndarray:
    # 6 x 6 ordered mother->father longitude differences.
    diff = (pm[:, None].astype(np.float64) - pf[None, :].astype(np.float64) + 180.0) % 360.0 - 180.0
    feats = np.empty((6, 6, 5), dtype=np.float32)
    for k, asp in enumerate(ASPECTS):
        if asp == 0.0:
            resid = np.abs(diff)
        elif asp == 180.0:
            resid = np.abs(np.abs(diff) - 180.0)
        else:
            resid = np.minimum(np.abs(diff - asp), np.abs(diff + asp))
        feats[:, :, k] = np.exp(-0.5 * (resid / SIGMA) ** 2).astype(np.float32)
    return feats.reshape(-1)


def build_binary_matrix(
    pairs: list[tuple[Record, tuple[int,int,int]]],
    positions: dict[tuple[int,int,int], np.ndarray],
    include_syn: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = 7 + (180 if include_syn else 0)
    X = np.empty((len(pairs) * 2, p), dtype=np.float32)
    y = np.empty(len(pairs) * 2, dtype=np.int8)
    group = np.empty(len(pairs) * 2, dtype=np.int32)
    for i, (r, synth_f) in enumerate(pairs):
        for j, (fdob, label) in enumerate(((r.father, 1), (synth_f, 0))):
            row = 2 * i + j
            X[row, :7] = baseline_features(r.mother, fdob, r.wedding)
            if include_syn:
                X[row, 7:] = syn_features(positions[r.mother], positions[fdob])
            y[row] = label; group[row] = i
        if (i + 1) % 25000 == 0:
            print(f"built binary features {i+1}/{len(pairs)} include_syn={include_syn}", flush=True)
    return X, y, group


def scale_baseline_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = X[:, :7].mean(axis=0, dtype=np.float64).astype(np.float32)
    sd = X[:, :7].std(axis=0, dtype=np.float64).astype(np.float32)
    sd[sd < 1e-8] = 1.0
    return mean, sd


def apply_baseline_scale(X: np.ndarray, mean: np.ndarray, sd: np.ndarray) -> np.ndarray:
    Z = X.copy()
    Z[:, :7] = (Z[:, :7] - mean) / sd
    return Z


def new_sgd(alpha: float) -> SGDClassifier:
    return SGDClassifier(
        loss="log_loss",
        penalty="elasticnet",
        l1_ratio=0.5,
        alpha=alpha,
        max_iter=2000,
        tol=1e-4,
        random_state=SEED % (2**32),
        shuffle=True,
        average=False,
    )


def binary_metrics(y: np.ndarray, decision: np.ndarray) -> dict[str, float]:
    prob = 1.0 / (1.0 + np.exp(-np.clip(decision.astype(np.float64), -50, 50)))
    return {
        "roc_auc": float(roc_auc_score(y, decision)),
        "log_loss": float(log_loss(y, prob, labels=[0,1])),
        "brier": float(brier_score_loss(y, prob)),
    }


def fit_select(
    Xd: np.ndarray, yd: np.ndarray,
    Xv: np.ndarray, yv: np.ndarray,
    include_syn: bool,
) -> dict:
    mean, sd = scale_baseline_fit(Xd)
    Zd = apply_baseline_scale(Xd, mean, sd)
    Zv = apply_baseline_scale(Xv, mean, sd)
    trials = []
    for alpha in ALPHAS:
        clf = new_sgd(alpha).fit(Zd, yd)
        decision = clf.decision_function(Zv)
        met = binary_metrics(yv, decision)
        trials.append({"alpha": alpha, **met, "nonzero_coefficients": int(np.sum(np.abs(clf.coef_[0]) > 1e-10))})
        print(f"validation include_syn={include_syn} alpha={alpha} auc={met['roc_auc']:.6f}", flush=True)
    best_auc = max(t["roc_auc"] for t in trials)
    eligible = [t for t in trials if best_auc - t["roc_auc"] <= 1e-4]
    selected = max(eligible, key=lambda t: t["alpha"])
    return {"trials": trials, "selected_alpha": selected["alpha"], "selected_validation": selected}


def refit_final(
    Xd: np.ndarray, yd: np.ndarray,
    Xv: np.ndarray, yv: np.ndarray,
    Xf: np.ndarray, yf: np.ndarray,
    alpha: float,
) -> tuple[dict, SGDClassifier, np.ndarray, np.ndarray, np.ndarray]:
    Xt = np.concatenate([Xd, Xv], axis=0)
    yt = np.concatenate([yd, yv], axis=0)
    mean, sd = scale_baseline_fit(Xt)
    Zt = apply_baseline_scale(Xt, mean, sd)
    Zf = apply_baseline_scale(Xf, mean, sd)
    clf = new_sgd(alpha).fit(Zt, yt)
    decision = clf.decision_function(Zf)
    met = binary_metrics(yf, decision)
    # Calibration intercept/slope on untouched final predictions. This is descriptive,
    # not used to alter predictions.
    cal = LogisticRegression(penalty=None, solver="lbfgs", max_iter=2000).fit(decision.reshape(-1,1), yf)
    met["calibration_intercept"] = float(cal.intercept_[0])
    met["calibration_slope"] = float(cal.coef_[0][0])
    met["nonzero_coefficients"] = int(np.sum(np.abs(clf.coef_[0]) > 1e-10))
    return met, clf, mean, sd, decision


def score_rows(clf, mean, sd, X):
    return clf.decision_function(apply_baseline_scale(X, mean, sd))


def full_final_strata(records: list[Record]) -> dict[tuple[int,int], list[Record]]:
    strata: dict[tuple[int,int], list[Record]] = defaultdict(list)
    for r in records:
        if r.split == "final":
            strata[(r.wedding[0], r.father[0])].append(r)
    for vals in strata.values():
        vals.sort(key=lambda r: (r.digest, r.canonical))
    return strata


def make_risk_tasks(records: list[Record]) -> tuple[list[tuple[Record, list[tuple[int,int,int]]]], dict]:
    final_sorted = sorted((r for r in records if r.split == "final"), key=lambda r: (r.digest, r.canonical))
    strata = full_final_strata(records)
    tasks = []
    drop = defaultdict(int)
    for r in final_sorted[:RISK_TASKS]:
        vals = strata[(r.wedding[0], r.father[0])]
        # Locate this exact tuple; deterministic forward offsets in stratum order.
        idx = next((i for i, x in enumerate(vals) if x.canonical == r.canonical), None)
        if idx is None:
            drop["record_not_found_in_stratum"] += 1
            continue
        decoys: list[tuple[int,int,int]] = []
        seen = {r.father}
        for step in range(1, len(vals) + 1):
            fd = vals[(idx + step) % len(vals)].father
            if fd in seen:
                continue
            seen.add(fd); decoys.append(fd)
            if len(decoys) == RISK_DECOYS:
                break
        if len(decoys) < RISK_DECOYS:
            drop["fewer_than_20_distinct_father_dob_decoys"] += 1
            continue
        tasks.append((r, decoys))
    return tasks, dict(drop)


def risk_metrics_for_model(
    tasks,
    positions,
    include_syn,
    clf,
    mean,
    sd,
    batch_tasks=500,
) -> dict[str, float]:
    ranks=[]; pcts=[]
    for start in range(0, len(tasks), batch_tasks):
        batch=tasks[start:start+batch_tasks]
        p=7+(180 if include_syn else 0)
        X=np.empty((len(batch)*(RISK_DECOYS+1), p), dtype=np.float32)
        for bi,(r,decoys) in enumerate(batch):
            fathers=[r.father]+decoys
            for j,fd in enumerate(fathers):
                row=bi*(RISK_DECOYS+1)+j
                X[row,:7]=baseline_features(r.mother,fd,r.wedding)
                if include_syn:
                    X[row,7:]=syn_features(positions[r.mother],positions[fd])
        scores=score_rows(clf,mean,sd,X).reshape(len(batch),RISK_DECOYS+1)
        for arr in scores:
            true=float(arr[0]); ctl=arr[1:]
            higher=int(np.sum(ctl>true+1e-12)); tied=int(np.sum(np.abs(ctl-true)<=1e-12))
            rank=1.0+higher+0.5*tied
            pct=100.0*(RISK_DECOYS-higher-0.5*tied)/RISK_DECOYS
            ranks.append(rank); pcts.append(pct)
        print(f"risk-set scored {min(start+batch_tasks,len(tasks))}/{len(tasks)} include_syn={include_syn}",flush=True)
    return {
        "tasks":len(ranks),
        "mean_true_partner_percentile":float(np.mean(pcts)),
        "median_true_partner_percentile":float(np.median(pcts)),
        "top1_rate":float(np.mean([r<=1.0+1e-12 for r in ranks])),
        "top5_rate":float(np.mean([r<=5.0+1e-12 for r in ranks])),
        "mean_reciprocal_rank":float(np.mean([1.0/r for r in ranks])),
    }


def final_features_at_hour(pairs, hour, include_syn=True):
    dates=set()
    for r,sf in pairs:
        dates.add(r.mother);dates.add(r.father);dates.add(sf)
    pos=planet_positions(dates,hour)
    X,y,_=build_binary_matrix(pairs,pos,include_syn)
    return X,y,pos


def permutation_diagnostic(y, decision, pair_count=20_000, n=200):
    # Binary rows are [real, synthetic] for every matched pair.
    n_pairs=min(pair_count,len(y)//2)
    scores=decision[:2*n_pairs].reshape(n_pairs,2)
    rng=random.Random(SEED)
    observed=float(roc_auc_score(np.tile([1,0],n_pairs),scores.reshape(-1)))
    vals=[]
    for _ in range(n):
        labels=np.empty((n_pairs,2),dtype=np.int8)
        for i in range(n_pairs):
            if rng.random()<0.5: labels[i]=[1,0]
            else: labels[i]=[0,1]
        vals.append(float(roc_auc_score(labels.reshape(-1),scores.reshape(-1))))
    ge=sum(v>=observed-1e-12 for v in vals)
    return {"pairs":n_pairs,"n":n,"observed_auc":observed,"null_mean_auc":statistics.fmean(vals),"null_sd_auc":statistics.stdev(vals),"null_ge_observed":ge,"empirical_p_ge_observed":(ge+1)/(n+1)}


def main():
    for p in (EPHE/"sepl_18.se1",EPHE/"semo_18.se1"):
        if not p.is_file():raise SystemExit("Missing Swiss file: "+str(p))
    swe.set_ephe_path(str(EPHE))
    records,raw_bytes,audit=download_records()
    splits=cap_splits(records)
    matched={}; drop={}
    for s,rows in splits.items():
        matched[s],drop[s]=make_matched_pairs(rows)
        print(f"{s}: capped_real={len(rows)} matched_real={len(matched[s])}",flush=True)

    dates=set()
    for plist in matched.values():
        for r,sf in plist:
            dates.update((r.mother,r.father,sf))
    # Risk tasks may use father DOBs outside binary caps; add their dates before noon cache.
    risk_tasks,risk_drop=make_risk_tasks(records)
    for r,decs in risk_tasks:
        dates.add(r.mother);dates.add(r.father);dates.update(decs)
    noon=planet_positions(dates,12.0)

    Xd0,yd,_=build_binary_matrix(matched["discovery"],noon,False)
    Xv0,yv,_=build_binary_matrix(matched["validation"],noon,False)
    Xf0,yf,_=build_binary_matrix(matched["final"],noon,False)
    Xds,yds,_=build_binary_matrix(matched["discovery"],noon,True)
    Xvs,yvs,_=build_binary_matrix(matched["validation"],noon,True)
    Xfs,yfs,_=build_binary_matrix(matched["final"],noon,True)
    if not (np.array_equal(yd,yds) and np.array_equal(yv,yvs) and np.array_equal(yf,yfs)):
        raise RuntimeError("label mismatch between baseline and synastry matrices")

    sel0=fit_select(Xd0,yd,Xv0,yv,False)
    sels=fit_select(Xds,yd,Xvs,yv,True)
    met0,clf0,mean0,sd0,dec0=refit_final(Xd0,yd,Xv0,yv,Xf0,yf,sel0["selected_alpha"])
    mets,clfs,means,sds,decs=refit_final(Xds,yd,Xvs,yv,Xfs,yf,sels["selected_alpha"])

    risk0=risk_metrics_for_model(risk_tasks,noon,False,clf0,mean0,sd0)
    risks=risk_metrics_for_model(risk_tasks,noon,True,clfs,means,sds)
    delta_auc=mets["roc_auc"]-met0["roc_auc"]
    delta_loss=mets["log_loss"]-met0["log_loss"]
    promising=(mets["roc_auc"]>=0.52 and delta_auc>=0.01 and delta_loss<=-0.002 and risks["mean_true_partner_percentile"]>=55.0)
    strong=(mets["roc_auc"]>=0.55 and delta_auc>=0.03 and risks["mean_true_partner_percentile"]>=60.0)

    perm=permutation_diagnostic(yf,decs,20_000,200)

    sensitivity={}
    for label,hour in (("00UTC",0.0),("2359UTC",23.0+59.0/60.0)):
        Xalt,yalt,posalt=final_features_at_hour(matched["final"],hour,True)
        decalt=score_rows(clfs,means,sds,Xalt)
        bmet=binary_metrics(yalt,decalt)
        rmet=risk_metrics_for_model(risk_tasks,posalt,True,clfs,means,sds)
        sensitivity[label]={"binary":bmet,"risk_set":rmet,"qualitative_promising_threshold_components":{"auc_ge_052":bmet["roc_auc"]>=0.52,"risk_percentile_ge_55":rmet["mean_true_partner_percentile"]>=55.0}}

    promoted=None
    if promising:
        coefs=clfs.coef_[0]
        # Coefficient 0..6 are baseline; 7.. are frozen synastry features.
        rows=[]
        for name,val in zip(ALL_NAMES,coefs):
            if name.startswith("syn_") and abs(float(val))>1e-10:
                rows.append({"feature":name,"coefficient":float(val),"abs_coefficient":abs(float(val))})
        rows.sort(key=lambda x:x["abs_coefficient"],reverse=True)
        promoted=rows[:30]

    result={
        "status":"independent_large_n_final_test_complete",
        "freeze_spec":str(FREEZE.relative_to(REPO)),"freeze_sha256":sha256_file(FREEZE),
        "source":URL,"source_raw_bytes":raw_bytes,
        "source_notice":["Didier Castille adaptation of INSEE files, not official INSEE files.","Source README states scientific validity depends on Castille's good faith.","Birth and wedding dates are untimed."],
        "data_audit":audit,
        "split_counts":{s:{"capped_real":len(splits[s]),"matched_real":len(matched[s]),"synthetic_drop":drop[s]} for s in ("discovery","validation","final")},
        "risk_set":{"requested_tasks":RISK_TASKS,"usable_tasks":len(risk_tasks),"drop":risk_drop,"decoys_per_task":RISK_DECOYS},
        "ephemeris":{"requested":"SWIEPH","returned":"SWIEPH or abort","sepl_18_sha256":sha256_file(EPHE/"sepl_18.se1"),"semo_18_sha256":sha256_file(EPHE/"semo_18.se1")},
        "models":{
            "M0C":{"selection":sel0,"final_binary":met0,"final_risk_set":risk0},
            "MWSC":{"selection":sels,"final_binary":mets,"final_risk_set":risks,"delta_auc_vs_M0C":delta_auc,"delta_log_loss_vs_M0C":delta_loss,"promising_threshold_met":promising,"strong_threshold_met":strong},
        },
        "permutation_diagnostic":perm,
        "birth_time_sensitivity":sensitivity,
        "promoted_synastry_features":promoted,
        "interpretation_rule":"Promote a date-stable synastry formula only if the frozen promising threshold is met on untouched final data; otherwise preserve as a negative/small-effect result without coefficient tuning.",
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    print("wrote",OUT,"sha256",sha256_file(OUT),flush=True)

if __name__=="__main__":main()
