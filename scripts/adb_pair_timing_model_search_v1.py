#!/usr/bin/env python3
"""Frozen ADB C-sample pair-timing astrology model search V1.

Spec: reference/research/adb_pair_timing_model_search_freeze_v1.md
Development/model-selection only. Uses verified SWIEPH and aborts on fallback.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
FREEZE = REPO / "reference" / "research" / "adb_pair_timing_model_search_freeze_v1.md"
OUT = REPO / "reference" / "research" / "adb_pair_timing_model_search_results_v1.json"
URL = "https://www.astro.com/adbexport/c_sample.xml"

ROMANTIC_REL_IDS = {843, 858, 859}
EVENTS = {807: "meet", 808: "begin", 810: "marriage", 811: "divorce", 809: "end"}
FORMATION = {807, 808, 810}
DISSOLUTION = {811, 809}
HIGH_RR = {"AA", "A"}
DOB_RE = re.compile(r"born:\s*([+-]?\d{1,4})/(\d{1,2})/(\d{1,2})([jg]?)", re.I)
PARTNER_RE = re.compile(r"\bwith\s+(.+?)(?:,\s*born:|$)", re.I)

FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
EPH_MASK = swe.FLG_JPLEPH | swe.FLG_SWIEPH | swe.FLG_MOSEPH
TROPICAL_YEAR = 365.2422
ASPECTS = (0, 60, 90, 120, 180)
NATAL_BODIES = {
    "Sun": swe.SUN,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}
PROG_BODIES = {k: NATAL_BODIES[k] for k in ("Sun", "Mercury", "Venus", "Mars")}
TRANSIT_BODIES = {
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}
C_GRID = (0.01, 0.1, 1.0, 10.0)
SHIFT_YEARS = tuple(range(-10, 0)) + tuple(range(1, 11))
RNG_SEED = 202608261311


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def calc(jd: float, body: int) -> tuple[float, float]:
    xx, ret = swe.calc_ut(jd, body, FLAGS)
    used = ret & EPH_MASK
    if used != swe.FLG_SWIEPH:
        raise RuntimeError(f"EPHEMERIS_FALLBACK body={body} jd={jd} used={used} ret={ret}")
    return xx[0] % 360.0, xx[3]


def wrap180(x: float) -> float:
    return (x + 180.0) % 360.0 - 180.0


def aspect_residual(moving: float, target: float, aspect: int) -> float:
    if aspect == 0:
        return abs(wrap180(moving - target))
    if aspect == 180:
        return abs(wrap180(moving - target - 180.0))
    return min(abs(wrap180(moving - target - aspect)), abs(wrap180(moving - target + aspect)))


def kernel(moving: float, target: float, sigma: float) -> float:
    r = min(aspect_residual(moving, target, a) for a in ASPECTS)
    return math.exp(-0.5 * (r / sigma) ** 2)


def midpoint(a: float, b: float) -> float:
    return (a + wrap180(b - a) / 2.0) % 360.0


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def tokens(name: str) -> set[str]:
    stop = {"relationship", "spouse", "lover", "with", "born", "family", "associates"}
    return {t for t in norm(name).split() if len(t) >= 4 and t not in stop}


def parse_partner_stub(text: str) -> dict | None:
    md = DOB_RE.search(text or "")
    if not md:
        return None
    mn = PARTNER_RE.search(text or "")
    name = mn.group(1).strip() if mn else ""
    return {
        "name": name,
        "tokens": tokens(name),
        "year": int(md.group(1)),
        "month": int(md.group(2)),
        "day": int(md.group(3)),
        "calendar": "julian" if md.group(4).lower() == "j" else "gregorian",
    }


def strict_match(notes: str, ptokens: set[str]) -> bool:
    words = set(norm(notes).split())
    return bool(ptokens and any(t in words for t in ptokens))


def date_jd(y: int, m: int, d: int, hour: float = 12.0) -> float:
    return swe.julday(y, m, d, hour, swe.GREG_CAL)


def date_from_attrs(sb: ET.Element | None) -> dict | None:
    if sb is None:
        return None
    try:
        y = int(sb.attrib.get("iyear", "0"))
        m = int(sb.attrib.get("imonth", "0"))
        d = int(sb.attrib.get("iday", "0"))
    except ValueError:
        return None
    if not y or not m:
        return None
    return {
        "year": y,
        "month": m,
        "day": d if d else None,
        "calendar": "julian" if sb.attrib.get("ccalendar") == "j" else "gregorian",
    }


@dataclass(frozen=True)
class Person:
    adb_id: int
    name: str
    rr: str
    exact_jd: float | None
    birth_date: tuple[int, int, int] | None

    @property
    def high_timed(self) -> bool:
        return self.rr in HIGH_RR and self.exact_jd is not None

    def parity_birth_jd(self) -> float | None:
        if self.birth_date is None:
            return None
        y, m, d = self.birth_date
        return date_jd(y, m, d, 12.0)


@dataclass(frozen=True)
class EventRecord:
    pair_key: str
    focal: Person
    partner: Person
    event_id: int
    event_name: str
    transition: str
    year: int
    month: int
    day: int
    precision: str


def download_parse() -> tuple[dict[int, Person], dict[int, list[dict]], dict[int, list[dict]], int]:
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-pair-model/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    root = ET.fromstring(raw)
    persons: dict[int, Person] = {}
    rels: dict[int, list[dict]] = defaultdict(list)
    events: dict[int, list[dict]] = defaultdict(list)
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None:
            continue
        name = (pub.findtext("name") or "").strip()
        rr = (pub.findtext("roddenrating") or "").strip()
        bd = pub.find("./bdata/sbdate")
        bdv = date_from_attrs(bd)
        birth_tuple = None
        if bdv and bdv["calendar"] == "gregorian" and bdv["day"]:
            birth_tuple = (bdv["year"], bdv["month"], int(bdv["day"]))
        bt = pub.find("./bdata/sbtime")
        exact_jd = None
        if bt is not None and bt.attrib.get("jd_ut") and (bt.text or "").strip():
            try:
                exact_jd = float(bt.attrib["jd_ut"])
            except ValueError:
                pass
        persons[aid] = Person(aid, name, rr, exact_jd, birth_tuple)
        research = e.find("research_data")
        if research is None:
            continue
        rp = research.find("relationships")
        if rp is not None:
            for rel in rp.findall("relationship"):
                try:
                    rid = int(rel.attrib.get("rel_id", "0")); other = int(rel.attrib.get("rel_adb_id", "0"))
                except ValueError:
                    continue
                if rid in ROMANTIC_REL_IDS:
                    text = (rel.text or "").strip()
                    rels[aid].append({"rel_id": rid, "other": other, "text": text, "stub": parse_partner_stub(text)})
        ep = research.find("events")
        if ep is not None:
            for ev in ep.findall("event"):
                try:
                    eid = int(ev.attrib.get("evn_id", "0"))
                except ValueError:
                    continue
                if eid not in EVENTS:
                    continue
                dv = date_from_attrs(ev.find("./event_data/sbdate"))
                if not dv:
                    continue
                events[aid].append({
                    "event_id": eid,
                    "notes": ev.attrib.get("evnotes", ""),
                    "date": dv,
                })
    return persons, rels, events, len(raw)


def build_events(persons: dict[int, Person], rels: dict[int, list[dict]], events: dict[int, list[dict]]) -> tuple[list[EventRecord], dict]:
    records: list[EventRecord] = []
    excluded = Counter()
    seen = set()
    for aid, person in persons.items():
        if not person.high_timed or not person.birth_date:
            continue
        for rel in rels.get(aid, []):
            other = rel["other"]
            if other in persons and persons[other].birth_date:
                partner = persons[other]
                ptok = tokens(partner.name)
            else:
                stub = rel.get("stub")
                if not stub or stub["calendar"] != "gregorian":
                    excluded["partner_dob_missing_or_julian"] += 1
                    continue
                try:
                    date(stub["year"], stub["month"], stub["day"])
                except Exception:
                    excluded["partner_dob_invalid"] += 1
                    continue
                partner = Person(other, stub["name"], "date-only", None, (stub["year"], stub["month"], stub["day"]))
                ptok = stub["tokens"]
            if not partner.birth_date:
                continue
            for ev in events.get(aid, []):
                if not strict_match(ev["notes"], ptok):
                    continue
                dv = ev["date"]
                if dv["calendar"] != "gregorian":
                    excluded["event_julian"] += 1
                    continue
                if dv["day"]:
                    eday = int(dv["day"]); precision = "day"
                else:
                    eday = 15; precision = "month"
                try:
                    date(dv["year"], dv["month"], eday)
                except Exception:
                    excluded["event_invalid_date"] += 1
                    continue
                if dv["year"] < 1800 or dv["year"] > 2399:
                    excluded["event_outside_ephemeris"] += 1
                    continue
                if person.birth_date[0] < 1800 or partner.birth_date[0] < 1800:
                    excluded["birth_outside_ephemeris"] += 1
                    continue
                pk = f"{min(aid, other)}:{max(aid, other)}"
                dedup = (pk, ev["event_id"], dv["year"], dv["month"], eday)
                if dedup in seen:
                    excluded["mirrored_duplicate"] += 1
                    continue
                seen.add(dedup)
                records.append(EventRecord(
                    pair_key=pk,
                    focal=person,
                    partner=partner,
                    event_id=ev["event_id"],
                    event_name=EVENTS[ev["event_id"]],
                    transition="formation" if ev["event_id"] in FORMATION else "dissolution",
                    year=dv["year"], month=dv["month"], day=eday, precision=precision,
                ))
    return records, dict(excluded)


def safe_shift(y: int, m: int, d: int, dy: int) -> tuple[int, int, int, bool] | None:
    yy = y + dy
    dd = d
    adjusted = False
    try:
        date(yy, m, dd)
    except ValueError:
        if m == 2 and d == 29:
            dd = 28; adjusted = True
        else:
            return None
    return yy, m, dd, adjusted


def natal_positions(birth_jd: float) -> dict[str, float]:
    return {n: calc(birth_jd, b)[0] for n, b in NATAL_BODIES.items()}


def progressed_positions(birth_jd: float, candidate_jd: float) -> dict[str, float]:
    age = (candidate_jd - birth_jd) / TROPICAL_YEAR
    pj = birth_jd + age
    return {n: calc(pj, b)[0] for n, b in PROG_BODIES.items()}


def activation_by_mover(movers: dict[str, float], targets: dict[str, float], sigma: float) -> dict[str, float]:
    return {f"{mn}": max(kernel(mlon, tlon, sigma) for tlon in targets.values()) for mn, mlon in movers.items()}


def feature_dict(ev: EventRecord, cy: int, cm: int, cd: int) -> dict[str, float]:
    cj = date_jd(cy, cm, cd, 12.0)
    a_birth = ev.focal.exact_jd
    b_birth = ev.partner.parity_birth_jd()
    assert a_birth is not None and b_birth is not None
    na = natal_positions(a_birth); nb = natal_positions(b_birth)
    pa = progressed_positions(a_birth, cj); pb = progressed_positions(b_birth, cj)
    tr = {n: calc(cj, b)[0] for n, b in TRANSIT_BODIES.items()}
    f: dict[str, float] = {}

    age_a = (cj - a_birth) / TROPICAL_YEAR
    age_b = (cj - b_birth) / TROPICAL_YEAR
    f.update({
        "m0_age_a": age_a,
        "m0_age_b": age_b,
        "m0_abs_age_diff": abs(age_a - age_b),
        "m0_year_scaled": (cy - 1950.0) / 50.0,
        "m0_transition_dissolution": 1.0 if ev.transition == "dissolution" else 0.0,
    })
    for eid in sorted(EVENTS):
        f[f"m0_event_{eid}"] = 1.0 if ev.event_id == eid else 0.0

    for prefix, natal, prog in (("a", na, pa), ("b", nb, pb)):
        for mn, val in activation_by_mover(tr, natal, 1.5).items():
            f[f"m1_{prefix}_transit_{mn}"] = val
        for mn, val in activation_by_mover(prog, natal, 1.0).items():
            f[f"m1_{prefix}_prog_{mn}"] = val

    for mn, mlon in pa.items():
        f[f"m3a_pa_nb_{mn}"] = max(kernel(mlon, t, 1.0) for t in nb.values())
    for mn, mlon in pb.items():
        f[f"m3a_pb_na_{mn}"] = max(kernel(mlon, t, 1.0) for t in na.values())
    for mn, mlon in pa.items():
        f[f"m3a_pa_pb_{mn}"] = max(kernel(mlon, t, 1.0) for t in pb.values())

    comp_n = {n: midpoint(na[n], nb[n]) for n in NATAL_BODIES}
    for mn, mlon in tr.items():
        f[f"m3b_transit_ncomp_{mn}"] = max(kernel(mlon, t, 1.5) for t in comp_n.values())

    comp_p = {n: midpoint(pa[n], pb[n]) for n in PROG_BODIES}
    for mn, mlon in tr.items():
        f[f"m3c_transit_pcomp_{mn}"] = max(kernel(mlon, t, 1.5) for t in comp_p.values())
    return f


def build_rows(events: list[EventRecord]) -> tuple[list[dict], dict]:
    rows = []
    counts = Counter()
    for ei, ev in enumerate(events):
        candidates = [(ev.year, ev.month, ev.day, True, False)]
        for dy in SHIFT_YEARS:
            s = safe_shift(ev.year, ev.month, ev.day, dy)
            if not s:
                continue
            y, m, d, adj = s
            a_jd = ev.focal.exact_jd; b_jd = ev.partner.parity_birth_jd()
            assert a_jd is not None and b_jd is not None
            cj = date_jd(y, m, d, 12.0)
            aa = (cj - a_jd) / TROPICAL_YEAR; ab = (cj - b_jd) / TROPICAL_YEAR
            if not (16 <= aa <= 85 and 16 <= ab <= 85):
                counts["control_age_excluded"] += 1
                continue
            candidates.append((y, m, d, False, adj))
        if len(candidates) < 6:
            counts["event_too_few_controls"] += 1
            continue
        event_key = f"{ev.pair_key}|{ev.event_id}|{ev.year:04d}-{ev.month:02d}-{ev.day:02d}"
        for y, m, d, actual, adjusted in candidates:
            rows.append({
                "event_key": event_key,
                "pair_key": ev.pair_key,
                "transition": ev.transition,
                "event_name": ev.event_name,
                "actual": int(actual),
                "candidate_date": f"{y:04d}-{m:02d}-{d:02d}",
                "leap_adjusted": adjusted,
                "features": feature_dict(ev, y, m, d),
            })
    return rows, dict(counts)


def feature_names_for(model: str, all_names: list[str]) -> list[str]:
    keep = []
    for n in all_names:
        if n.startswith("m0_"):
            keep.append(n); continue
        if model in {"M1", "M3A", "M3B", "M3C", "M3ALL"} and n.startswith("m1_"):
            keep.append(n); continue
        if model in {"M3A", "M3ALL"} and n.startswith("m3a_"):
            keep.append(n); continue
        if model in {"M3B", "M3ALL"} and n.startswith("m3b_"):
            keep.append(n); continue
        if model in {"M3C", "M3ALL"} and n.startswith("m3c_"):
            keep.append(n); continue
    return keep


def metrics_from_scores(rows: list[dict], scores: np.ndarray) -> dict[str, float]:
    by_event: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for r, s in zip(rows, scores):
        by_event[r["event_key"]].append((float(s), r["actual"]))
    ranks = []; percentiles = []; losses = []
    for vals in by_event.values():
        vals = sorted(vals, key=lambda x: x[0], reverse=True)
        rank = next(i + 1 for i, (_, y) in enumerate(vals) if y == 1)
        n = len(vals)
        pct = 100.0 if n == 1 else 100.0 * (n - rank) / (n - 1)
        ranks.append(rank); percentiles.append(pct)
        arr = np.array([x[0] for x in vals], dtype=float)
        arr -= arr.max()
        probs = np.exp(arr); probs /= probs.sum()
        idx = next(i for i, (_, y) in enumerate(vals) if y == 1)
        losses.append(-math.log(max(float(probs[idx]), 1e-15)))
    return {
        "events": len(ranks),
        "mean_true_date_percentile": float(np.mean(percentiles)),
        "median_true_date_percentile": float(np.median(percentiles)),
        "top1_rate": float(np.mean([r == 1 for r in ranks])),
        "top3_rate": float(np.mean([r <= 3 for r in ranks])),
        "mean_reciprocal_rank": float(np.mean([1.0 / r for r in ranks])),
        "softmax_log_loss": float(np.mean(losses)),
    }


def choose_c(train_rows: list[dict], names: list[str]) -> float:
    groups = np.array([r["pair_key"] for r in train_rows])
    uniq = sorted(set(groups))
    nsplit = min(3, max(2, len(uniq) // 4))
    if len(uniq) < 4:
        return 0.1
    gkf = GroupKFold(n_splits=min(nsplit, len(uniq)))
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in train_rows], dtype=float)
    y = np.array([r["actual"] for r in train_rows])
    best = None
    for c in C_GRID:
        pcts = []
        for ti, vi in gkf.split(X, y, groups):
            sc = StandardScaler().fit(X[ti]); xt = sc.transform(X[ti]); xv = sc.transform(X[vi])
            clf = LogisticRegression(C=c, class_weight="balanced", max_iter=4000, solver="liblinear").fit(xt, y[ti])
            met = metrics_from_scores([train_rows[i] for i in vi], clf.decision_function(xv))
            pcts.append(met["mean_true_date_percentile"])
        score = float(np.mean(pcts))
        if best is None or score > best[0] + 1e-12 or (abs(score - best[0]) < 1e-12 and c < best[1]):
            best = (score, c)
    return float(best[1])


def evaluate_model(rows: list[dict], model: str) -> tuple[dict, list[float]]:
    all_names = sorted(rows[0]["features"])
    names = feature_names_for(model, all_names)
    groups = np.array([r["pair_key"] for r in rows])
    uniq = sorted(set(groups))
    nsplit = min(5, len(uniq) // 5)
    if nsplit < 2:
        raise RuntimeError(f"too few pair groups for grouped CV: {len(uniq)}")
    gkf = GroupKFold(n_splits=nsplit)
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in rows], dtype=float)
    y = np.array([r["actual"] for r in rows])
    out_scores = np.full(len(rows), np.nan)
    cs = []
    for ti, vi in gkf.split(X, y, groups):
        tr = [rows[i] for i in ti]
        c = choose_c(tr, names); cs.append(c)
        sc = StandardScaler().fit(X[ti]); xt = sc.transform(X[ti]); xv = sc.transform(X[vi])
        clf = LogisticRegression(C=c, class_weight="balanced", max_iter=4000, solver="liblinear").fit(xt, y[ti])
        out_scores[vi] = clf.decision_function(xv)
    met = metrics_from_scores(rows, out_scores)
    met.update({"model": model, "feature_count": len(names), "outer_folds": nsplit, "selected_C_by_fold": cs})
    return met, out_scores.tolist()


def evaluate_subset(rows: list[dict], subset: str) -> dict:
    rr = rows if subset == "pooled" else [r for r in rows if r["transition"] == subset]
    events = len({r["event_key"] for r in rr}); pairs = len({r["pair_key"] for r in rr})
    if events < 20 or pairs < 10:
        return {"status": "insufficient", "events": events, "pairs": pairs}
    result = {"status": "ok", "events": events, "pairs": pairs, "models": {}}
    for m in ("M0", "M1", "M3A", "M3B", "M3C", "M3ALL"):
        met, _ = evaluate_model(rr, m); result["models"][m] = met
    return result


def full_fit_top_coefficients(rows: list[dict], model: str) -> dict:
    all_names = sorted(rows[0]["features"]); names = feature_names_for(model, all_names)
    c = choose_c(rows, names)
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in rows], float)
    y = np.array([r["actual"] for r in rows])
    sc = StandardScaler().fit(X); xs = sc.transform(X)
    clf = LogisticRegression(C=c, class_weight="balanced", max_iter=4000, solver="liblinear").fit(xs, y)
    co = sorted(zip(names, clf.coef_[0]), key=lambda x: abs(x[1]), reverse=True)
    return {"C": c, "top_coefficients": [{"feature": n, "coef_standardized": float(v)} for n, v in co[:15]]}


def permutation_best(rows: list[dict], model: str, observed_pct: float, nperm: int = 100) -> dict:
    rng = random.Random(RNG_SEED)
    event_to_idx: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows): event_to_idx[r["event_key"]].append(i)
    null = []
    # Fixed feature matrix; only within-event label identity changes. Re-run the same grouped CV/tuning.
    for p in range(nperm):
        rr = [dict(r) for r in rows]
        for idxs in event_to_idx.values():
            chosen = rng.choice(idxs)
            for i in idxs: rr[i]["actual"] = int(i == chosen)
        met, _ = evaluate_model(rr, model)
        null.append(met["mean_true_date_percentile"])
        if (p + 1) % 10 == 0:
            print(f"permutation {p+1}/{nperm}", flush=True)
    exceed = sum(x >= observed_pct - 1e-12 for x in null)
    return {
        "n": nperm,
        "empirical_p_ge_observed": (exceed + 1) / (nperm + 1),
        "null_mean_percentile": float(np.mean(null)),
        "null_sd_percentile": float(np.std(null, ddof=1)),
        "null_ge_observed": exceed,
    }


def main() -> None:
    for p in (EPHE / "sepl_18.se1", EPHE / "semo_18.se1"):
        if not p.is_file(): raise SystemExit("Missing Swiss ephemeris file: " + str(p))
    swe.set_ephe_path(str(EPHE))
    # Fail-closed probes.
    for j in (date_jd(1800, 1, 2), date_jd(1950, 1, 1), date_jd(2026, 1, 1), date_jd(2398, 1, 1)):
        for b in list(NATAL_BODIES.values()) + list(TRANSIT_BODIES.values()): calc(j, b)

    persons, rels, events, raw_bytes = download_parse()
    evs, excluded = build_events(persons, rels, events)
    rows, control_excluded = build_rows(evs)
    dataset = {
        "unique_events_pre_controls": len(evs),
        "unique_pairs_pre_controls": len({e.pair_key for e in evs}),
        "events_by_type": dict(Counter(e.event_name for e in evs)),
        "events_by_transition": dict(Counter(e.transition for e in evs)),
        "precision": dict(Counter(e.precision for e in evs)),
        "parser_exclusions": excluded,
        "control_exclusions": control_excluded,
        "rows": len(rows),
        "usable_events": len({r["event_key"] for r in rows}),
        "usable_pairs": len({r["pair_key"] for r in rows}),
    }
    print("dataset", json.dumps(dataset, indent=2), flush=True)

    results = {s: evaluate_subset(rows, s) for s in ("pooled", "formation", "dissolution")}
    pooled = results["pooled"]
    permutation = None; best_family = None
    top_coeff = {}
    if pooled.get("status") == "ok":
        models = pooled["models"]
        m1 = models["M1"]["mean_true_date_percentile"]
        pair_models = ["M3A", "M3B", "M3C", "M3ALL"]
        best_family = max(pair_models, key=lambda m: models[m]["mean_true_date_percentile"] - m1)
        observed = models[best_family]["mean_true_date_percentile"]
        permutation = permutation_best(rows, best_family, observed, 100)
        for m in ("M1", best_family): top_coeff[m] = full_fit_top_coefficients(rows, m)

    data = {
        "status": "development_model_selection",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "source": URL,
        "source_raw_bytes": raw_bytes,
        "ephemeris": {
            "requested": "SWIEPH", "returned": "SWIEPH or abort",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "dataset": dataset,
        "results": results,
        "best_pair_dynamic_family_by_pooled_mean_percentile_improvement": best_family,
        "permutation_diagnostic_for_selected_family": permutation,
        "development_refit_coefficients": top_coeff,
        "decision_rule": "promising only if pair family improves mean true-date percentile over M1 by >=5 points and does not materially worsen softmax log loss",
        "limitations": [
            "Partner birth time is unknown for most external linked partners; Moon/houses/angles/HD are excluded.",
            "This is event-date case-crossover model selection, not the full semi-Markov transition-hazard test.",
            "The same C-sample is used to choose the candidate family, so permutation p-values are development diagnostics only.",
            "Any selected family requires independent validation before being used as an empirical relationship predictor.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"dataset": dataset, "results": results, "best": best_family, "permutation": permutation}, indent=2), flush=True)
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)


if __name__ == "__main__":
    main()
