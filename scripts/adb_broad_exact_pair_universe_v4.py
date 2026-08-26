#!/usr/bin/env python3
"""Build the frozen outcome-independent ADB broad exact-time romantic-pair universe V4.

Frozen spec:
  reference/research/adb_broad_exact_pair_universe_freeze_v4.md

This script uses relationship-link structure and birth-data quality only. It does
not inspect relationship outcomes and does not calculate pair astrology/HD
features. Swiss ephemeris is used only for the frozen model-eligibility preflight.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import swisseph as swe

import adb_exact_pair_timing_v3 as v3

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_freeze_v4.md"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
EPHE = REPO / "data" / "ephemeris"
CSAMPLE = "https://www.astro.com/adbexport/c_sample.xml"
ADB_API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-broad-exact-pair-v4/1.0"
HIGH_RR = {"AA", "A"}
ROMANTIC = {843: "spouse", 858: "lover", 859: "spousal_equivalent"}
PARTNER_RE = re.compile(r"\bwith\s+(.+?)(?:,\s*born:|$)", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def get_bytes(url: str, timeout: int = 120, tries: int = 4) -> bytes:
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if i + 1 < tries:
                time.sleep(0.7 * (2 ** i))
    raise RuntimeError(f"fetch failed after {tries} attempts: {url}: {last}")


def api_json(params: dict, timeout: int = 30) -> dict:
    url = ADB_API + "?" + urllib.parse.urlencode(params)
    return json.loads(get_bytes(url, timeout=timeout).decode("utf-8", errors="replace"))


def field(text: str | None, name: str) -> str | None:
    m = re.search(rf"\|{re.escape(name)}\s*=\s*([^\n\r|}}]+)", text or "", re.I)
    return m.group(1).strip() if m else None


def parse_dma(text: str | None) -> dict:
    names = [
        "DatamainID", "sbdate", "sbtime", "t_unknown", "sroddenrating", "swikiname",
        "Place", "BirthCountry", "slati", "slong", "TmZnAbbr", "stmerid", "ctimetype",
        "stimetype", "ccalendar", "ctzauto", "jd_ut",
    ]
    return {n: field(text, n) for n in names}


def exact_id(text: str | None) -> int | None:
    x = field(text, "DatamainID")
    try:
        return int(x) if x is not None else None
    except ValueError:
        return None


def fetch_wikitext_batch(titles: list[str]) -> list[tuple[str, str]]:
    """Fetch raw ADB pages in small batches. Returned pages need not preserve input title."""
    out: list[tuple[str, str]] = []
    for i in range(0, len(titles), 10):
        batch = titles[i:i + 10]
        data = api_json({
            "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
            "titles": "|".join(batch), "redirects": 1, "formatversion": 2, "format": "json",
        })
        for page in data.get("query", {}).get("pages", []):
            if page.get("missing") is not None:
                continue
            revs = page.get("revisions", [])
            if not revs:
                continue
            rev = revs[0]
            wt = (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")
            if wt:
                out.append((page.get("title") or "", wt))
    return out


def search_titles(name: str) -> list[str]:
    variants = [name]
    if "," in name:
        a, b = [x.strip() for x in name.split(",", 1)]
        if a and b:
            variants.append(f"{b} {a}")
    out: list[str] = []
    for q in variants:
        data = api_json({"action": "query", "list": "search", "srsearch": q, "srlimit": 10, "format": "json"})
        for hit in data.get("query", {}).get("search", []):
            t = hit.get("title")
            if t and t not in out:
                out.append(t)
    return out


def partner_display_name(rel_text: str) -> str:
    m = PARTNER_RE.search(rel_text or "")
    if m:
        return re.sub(r"\s+", " ", m.group(1).strip(" ,"))
    s = (rel_text or "").strip()
    m2 = re.search(r"^(.*?)(?:,?\s+born\s*:)", s, flags=re.I)
    return re.sub(r"\s+", " ", (m2.group(1) if m2 else s).strip(" ,"))


def parse_csample(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    entries = {}
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None:
            continue
        name = (pub.findtext("name") or "").strip()
        rr = (pub.findtext("roddenrating") or "").strip()
        bdata = pub.find("bdata")
        rec = {
            "adb_id": aid, "name": name, "rr": rr, "jd_ut": None,
            "birth_date": None, "birth_clock": None, "lat": None, "lon": None,
            "rels": [],
        }
        if bdata is not None:
            sd = bdata.find("sbdate")
            st = bdata.find("sbtime")
            pl = bdata.find("place")
            if sd is not None:
                try:
                    y = int(sd.attrib["iyear"]); m = int(sd.attrib["imonth"]); d = int(sd.attrib["iday"])
                    rec["birth_date"] = f"{y:04d}-{m:02d}-{d:02d}"
                except Exception:
                    pass
            if st is not None and (st.text or "").strip():
                rec["birth_clock"] = (st.text or "").strip()
                try:
                    if st.attrib.get("jd_ut"):
                        rec["jd_ut"] = float(st.attrib["jd_ut"])
                except Exception:
                    pass
            if pl is not None:
                try:
                    rec["lat"] = v3.parse_coord(pl.attrib.get("slati", ""))
                    rec["lon"] = v3.parse_coord(pl.attrib.get("slong", ""), False)
                except Exception:
                    pass
        research = e.find("research_data")
        if research is not None:
            rp = research.find("relationships")
            if rp is not None:
                for r in rp.findall("relationship"):
                    try:
                        rid = int(r.attrib.get("rel_id", "0")); other = int(r.attrib.get("rel_adb_id", "0"))
                    except ValueError:
                        continue
                    rec["rels"].append({"rel_id": rid, "other_adb_id": other, "text": (r.text or "").strip()})
        entries[aid] = rec
    return entries


def external_person(adb_id: int, display_name: str, title: str, wt: str) -> tuple[dict | None, str | None]:
    dma = parse_dma(wt)
    if str(dma.get("DatamainID") or "") != str(adb_id):
        return None, "datamain_id_mismatch"
    rr = (dma.get("sroddenrating") or "").strip()
    if rr not in HIGH_RR:
        return None, "rodden_not_A_AA"
    unknown = bool(dma.get("t_unknown")) and str(dma.get("t_unknown")).strip() not in {"", "0", "None"}
    if unknown or not (dma.get("sbtime") or "").strip():
        return None, "time_unknown"
    try:
        y, m, d = map(int, (dma.get("sbdate") or "").split("/"))
        jd = v3.local_to_jd(y, m, d, dma["sbtime"], dma.get("ccalendar") or "g", dma["stmerid"])
        lat = v3.parse_coord(dma.get("slati") or "")
        lon = v3.parse_coord(dma.get("slong") or "", False)
    except Exception as exc:
        return None, f"utc_or_coordinate_reconstruction_failed:{type(exc).__name__}"
    return {
        "adb_id": adb_id,
        "name": display_name,
        "public_title": title,
        "rr": rr,
        "jd_ut": jd,
        "birth_date": f"{y:04d}-{m:02d}-{d:02d}",
        "birth_clock": dma.get("sbtime"),
        "lat": lat,
        "lon": lon,
        "birth_place": dma.get("Place"),
        "birth_country": dma.get("BirthCountry"),
        "stmerid": dma.get("stmerid"),
        "ccalendar": dma.get("ccalendar") or "g",
        "swikiname": dma.get("swikiname"),
        "source": "public_adb_exact_id",
    }, None


def internal_person(r: dict) -> dict:
    return {
        "adb_id": r["adb_id"], "name": r["name"], "public_title": r["name"],
        "rr": r["rr"], "jd_ut": r["jd_ut"], "birth_date": r["birth_date"],
        "birth_clock": r["birth_clock"], "lat": r["lat"], "lon": r["lon"],
        "source": "c_sample",
    }


def is_exact_high_rr(r: dict) -> bool:
    return r.get("rr") in HIGH_RR and r.get("jd_ut") is not None and bool(r.get("birth_clock"))


def same_person_duplicate(a: dict, b: dict) -> bool:
    if norm(a.get("name")) != norm(b.get("name")):
        return False
    if not a.get("birth_date") or a.get("birth_date") != b.get("birth_date"):
        return False
    if abs(float(a["jd_ut"]) - float(b["jd_ut"])) * 86400 > 60:
        return False
    if None in (a.get("lat"), a.get("lon"), b.get("lat"), b.get("lon")):
        return False
    return abs(a["lat"] - b["lat"]) <= 0.01 and abs(a["lon"] - b["lon"]) <= 0.01


def swieph_person_supported(p: dict) -> tuple[bool, str | None]:
    try:
        for body in v3.NATAL_IDS.values():
            v3.calc(float(p["jd_ut"]), body)
        # natal_gates evaluates both personality and design-root positions.
        v3.hd.natal_gates(v3.hd.dt_from_jd(float(p["jd_ut"])))
        return True, None
    except Exception as exc:
        return False, str(exc)


def pair_key(a: int, b: int) -> str:
    x, y = sorted((a, b))
    return f"adb:{x}|adb:{y}"


def main():
    for p in (EPHE / "sepl_18.se1", EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit(f"missing pinned ephemeris file: {p}")
    swe.set_ephe_path(str(EPHE))

    xml = get_bytes(CSAMPLE, timeout=120)
    entries = parse_csample(xml)
    internal_ids = set(entries)
    focal_ids = {aid for aid, r in entries.items() if is_exact_high_rr(r)}

    directed = []
    internal_candidate_pairs = set()
    internal_final_pairs = set()
    external_targets: dict[int, dict] = {}
    self_links = 0

    for aid in sorted(focal_ids):
        r = entries[aid]
        for rel in r["rels"]:
            if rel["rel_id"] not in ROMANTIC:
                continue
            bid = rel["other_adb_id"]
            if not bid:
                continue
            if bid == aid:
                self_links += 1
                continue
            directed.append({
                "focal_adb_id": aid, "other_adb_id": bid,
                "rel_id": rel["rel_id"], "rel_type": ROMANTIC[rel["rel_id"]],
                "text": rel["text"],
            })
            if bid in internal_ids:
                pk = pair_key(aid, bid)
                internal_candidate_pairs.add(pk)
                if is_exact_high_rr(entries[bid]):
                    internal_final_pairs.add(pk)
            else:
                t = external_targets.setdefault(bid, {
                    "adb_id": bid,
                    "display_name": partner_display_name(rel["text"]),
                    "seed_links": [],
                })
                t["seed_links"].append({"focal_adb_id": aid, "rel_id": rel["rel_id"], "text": rel["text"]})

    # Resolve all external targets independently of outcome availability.
    resolved_pages: dict[int, tuple[str, str]] = {}
    direct_titles = []
    for t in external_targets.values():
        if t["display_name"]:
            direct_titles.append(t["display_name"])
    # Fetch unique direct titles in deterministic order; exact DatamainID does the identity match.
    for title, wt in fetch_wikitext_batch(sorted(set(direct_titles))):
        eid = exact_id(wt)
        if eid in external_targets and eid not in resolved_pages:
            resolved_pages[eid] = (title, wt)

    unresolved_after_direct = [x for x in sorted(external_targets) if x not in resolved_pages]
    for i, eid in enumerate(unresolved_after_direct, 1):
        name = external_targets[eid]["display_name"]
        candidates = search_titles(name)
        if not candidates:
            continue
        for title, wt in fetch_wikitext_batch(candidates):
            if exact_id(wt) == eid:
                resolved_pages[eid] = (title, wt)
                break
        if i % 25 == 0:
            print(f"search fallback {i}/{len(unresolved_after_direct)}", flush=True)

    external_people: dict[int, dict] = {}
    external_status = Counter()
    external_audit = []
    for eid in sorted(external_targets):
        target = external_targets[eid]
        if eid not in resolved_pages:
            external_status["unresolved_exact_id"] += 1
            external_audit.append({**target, "status": "unresolved_exact_id"})
            continue
        title, wt = resolved_pages[eid]
        external_status["exact_id_resolved"] += 1
        person, reason = external_person(eid, target["display_name"], title, wt)
        if person is None:
            external_status[reason or "ineligible"] += 1
            external_audit.append({**target, "status": "resolved_ineligible", "public_title": title, "reason": reason})
            continue
        external_status["exact_time_A_AA_recovered"] += 1
        external_people[eid] = person
        external_audit.append({**target, "status": "exact_time_A_AA_recovered", "public_title": title, "person": person})

    people = {aid: internal_person(entries[aid]) for aid in focal_ids}
    people.update(external_people)

    pair_relations: dict[str, list[dict]] = defaultdict(list)
    for rel in directed:
        a, b = rel["focal_adb_id"], rel["other_adb_id"]
        if a in people and b in people:
            pair_relations[pair_key(a, b)].append(rel)

    sw_support: dict[int, tuple[bool, str | None]] = {}
    pair_rows = []
    dup_count = 0
    sw_pair_count = 0
    sw_failure_people = Counter()
    for pk in sorted(pair_relations, key=lambda z: tuple(map(int, re.findall(r"\d+", z)))):
        ids = [int(x) for x in re.findall(r"\d+", pk)]
        a, b = people[ids[0]], people[ids[1]]
        dup = same_person_duplicate(a, b)
        if dup:
            dup_count += 1
        for pid, person in ((ids[0], a), (ids[1], b)):
            if pid not in sw_support:
                sw_support[pid] = swieph_person_supported(person)
                if not sw_support[pid][0]:
                    sw_failure_people[pid] += 1
        sw_ok = sw_support[ids[0]][0] and sw_support[ids[1]][0]
        model_eligible = sw_ok and not dup
        if model_eligible:
            sw_pair_count += 1
        pair_rows.append({
            "pair_key": pk,
            "person_a": a,
            "person_b": b,
            "relation_records": pair_relations[pk],
            "relation_codes": sorted({x["rel_id"] for x in pair_relations[pk]}),
            "possible_same_person_duplicate": dup,
            "swieph_natal_design_preflight": {
                "person_a_ok": sw_support[ids[0]][0],
                "person_b_ok": sw_support[ids[1]][0],
                "person_a_error": sw_support[ids[0]][1],
                "person_b_error": sw_support[ids[1]][1],
            },
            "model_eligible_birth_and_swieph": model_eligible,
        })

    counts = {
        "c_sample_entries": len(entries),
        "c_sample_A_AA_exact_time_focal_people": len(focal_ids),
        "directed_eligible_romantic_links": len(directed),
        "self_links_excluded": self_links,
        "internal_candidate_pairs": len(internal_candidate_pairs),
        "internal_final_exact_time_pairs": len(internal_final_pairs),
        "unique_external_target_ids": len(external_targets),
        "external_public_pages_exact_id_resolved": external_status["exact_id_resolved"],
        "external_public_pages_unresolved": external_status["unresolved_exact_id"],
        "external_exact_time_A_AA_partners_recovered": external_status["exact_time_A_AA_recovered"],
        "final_unique_birth_data_qualified_exact_time_pairs": len(pair_rows),
        "possible_same_person_duplicate_exclusions": dup_count,
        "pairs_surviving_swieph_natal_design_preflight": sw_pair_count,
        "unique_people_in_final_pairs": len({p["person_a"]["adb_id"] for p in pair_rows} | {p["person_b"]["adb_id"] for p in pair_rows}),
    }

    out = {
        "status": "development_outcome_independent_pair_universe_audit",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "source": CSAMPLE,
        "source_raw_bytes": len(xml),
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or pair marked unsupported",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "counts": counts,
        "external_resolution_status_counts": dict(sorted(external_status.items())),
        "external_targets": external_audit,
        "pairs": pair_rows,
        "history_recovery_complete": False,
        "history_recovery_next": "Apply frozen V4 H1-H4 source hierarchy to this outcome-independent pair universe before any model specification.",
        "limitations": [
            "Astro-Databank development source; not independent validation.",
            "Pair membership uses relationship-link structure and birth-data quality only; no relationship outcome is required.",
            "Possible same-person duplicates are currently detected from name+birth-date+UTC+coordinates; linked Wikipedia/Wikidata identity can add a later duplicate safeguard during H3 without changing pair discovery.",
            "No relationship history evidence or pair astrology/HD feature is inspected in this universe-construction audit.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"], "counts": counts,
        "external_resolution_status_counts": out["external_resolution_status_counts"],
    }, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
