#!/usr/bin/env python3
"""Recover exact-time ADB records for external romantic-link partners that have
strictly partner-linked relationship transition events in the public C-sample.

This is a data-recovery audit for the future semi-Markov pair model. It does not
fit astrology. Public source pages are queried live; only compact derived data
are committed.
"""
from __future__ import annotations

import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "adb_external_eventlinked_exact_recovery_v1.json"
CSAMPLE = "https://www.astro.com/adbexport/c_sample.xml"
API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-research-audit/1.0"
ROMANTIC_REL_IDS = {843, 858, 859}
REL_EVENT_IDS = {807, 808, 803, 810, 811, 809, 815, 974}
HIGH_RR = {"AA", "A"}
PARTNER_RE = re.compile(r"\bwith\s+(.+?)(?:,\s*born:|$)", re.I)


def get(url: str, timeout: int = 8) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def partner_display_name(rel_text: str) -> str:
    m = PARTNER_RE.search(rel_text or "")
    if m:
        return re.sub(r"\s+", " ", m.group(1).strip(" ,"))
    s = (rel_text or "").strip()
    m2 = re.search(r"^(.*?)(?:,?\s+born\s*:)", s, flags=re.I)
    return re.sub(r"\s+", " ", (m2.group(1) if m2 else s).strip(" ,"))


def name_tokens(name: str) -> set[str]:
    stop = {"relationship", "spouse", "lover", "with", "born", "family", "associates"}
    return {t for t in norm(name).split() if len(t) >= 4 and t not in stop}


def event_matches(ev, tokens: set[str]) -> bool:
    text = norm((ev.attrib.get("evnotes", "") or "") + " " + (ev.attrib.get("sevcode", "") or ""))
    words = set(text.split())
    return bool(tokens & words)


def api_json(params: dict) -> dict | None:
    url = API + "?" + urllib.parse.urlencode(params)
    try:
        return json.loads(get(url).decode("utf-8", errors="replace"))
    except Exception:
        return None


def fetch_wikitext(title: str) -> str | None:
    data = api_json({
        "action":"query","prop":"revisions","rvprop":"content","rvslots":"main",
        "titles":title,"formatversion":2,"format":"json"
    })
    if not data: return None
    pages = data.get("query", {}).get("pages", [])
    if not pages: return None
    revs = pages[0].get("revisions", [])
    if not revs: return None
    rev = revs[0]
    slots = rev.get("slots", {})
    return (slots.get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")


def search_titles(name: str) -> list[str]:
    variants = [name]
    if "," in name:
        a, b = [x.strip() for x in name.split(",", 1)]
        if a and b:
            variants.append(f"{b} {a}")
    seen = []
    for q in variants:
        data = api_json({"action":"query","list":"search","srsearch":q,"srlimit":10,"format":"json"})
        if not data:
            continue
        for x in data.get("query", {}).get("search", []):
            t = x.get("title")
            if t and t not in seen:
                seen.append(t)
    return seen


def field(text: str, name: str) -> str | None:
    m = re.search(rf"\|{re.escape(name)}\s*=\s*([^\n\r|}}]+)", text or "", re.I)
    return m.group(1).strip() if m else None


def parse_dma(text: str) -> dict:
    names = [
        "DatamainID","sbdate","sbtime","t_unknown","sroddenrating","swikiname",
        "Place","BirthCountry","slati","slong","TmZnAbbr","stmerid","ctimetype",
        "stimetype","ccalendar","ctzauto","jd_ut"
    ]
    return {n: field(text, n) for n in names}


def resolve_exact_id(title: str, adb_id: int) -> tuple[dict | None, dict | None]:
    wt = fetch_wikitext(title)
    if not wt:
        return None, None
    dma = parse_dma(wt)
    rec = {"title": title, **dma}
    if dma.get("DatamainID") and str(dma["DatamainID"]) == str(adb_id):
        return rec, rec
    return None, rec


def main():
    xml = get(CSAMPLE, timeout=120)
    root = ET.fromstring(xml)
    entries = {}
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None: continue
        rr = (pub.findtext("roddenrating") or "").strip()
        bdata = pub.find("bdata")
        sbtime = bdata.find("sbtime") if bdata is not None else None
        timed = bool(sbtime is not None and (sbtime.text or "").strip() and sbtime.attrib.get("jd_ut"))
        research = e.find("research_data")
        entries[aid] = {"rr":rr,"timed":timed,"research":research}
    internal_ids = set(entries)

    targets = {}
    for aid, rec in entries.items():
        if rec["rr"] not in HIGH_RR or not rec["timed"] or rec["research"] is None:
            continue
        rel_parent = rec["research"].find("relationships")
        ev_parent = rec["research"].find("events")
        if rel_parent is None or ev_parent is None:
            continue
        for rel in rel_parent.findall("relationship"):
            try:
                rid = int(rel.attrib.get("rel_id", "0")); other = int(rel.attrib.get("rel_adb_id", "0"))
            except ValueError:
                continue
            if rid not in ROMANTIC_REL_IDS or not other or other in internal_ids:
                continue
            raw = (rel.text or "").strip(); pname = partner_display_name(raw); toks = name_tokens(pname)
            if not toks: continue
            matched_events = []
            for ev in ev_parent.findall("event"):
                try: eid = int(ev.attrib.get("evn_id", "0"))
                except ValueError: continue
                if eid in REL_EVENT_IDS and event_matches(ev, toks):
                    matched_events.append(eid)
            if not matched_events:
                continue
            t = targets.setdefault(other, {"adb_id":other,"partner_name":pname,"raw_rel_text":raw,"focal_ids":set(),"event_ids":set()})
            t["focal_ids"].add(aid); t["event_ids"].update(matched_events)

    rows=[]; stats=Counter()
    for i, other in enumerate(sorted(targets), 1):
        rec=targets[other]; best=None; first_any=None; method=None
        # Fast path: ADB relationship text often already uses the exact wiki title.
        best, first_any = resolve_exact_id(rec["partner_name"], other)
        if best is not None:
            method="direct_title"
        else:
            for title in search_titles(rec["partner_name"]):
                matched, any_rec = resolve_exact_id(title, other)
                if first_any is None and any_rec is not None: first_any=any_rec
                if matched is not None:
                    best=matched; method="search"; break
        if best is None:
            status="unresolved"
        else:
            stats["id_matched"] += 1; stats[f"method_{method}"] += 1
            unknown = bool(best.get("t_unknown")) and str(best.get("t_unknown")).strip() not in {"", "0", "None"}
            timed = bool(best.get("sbtime")) and not unknown
            if timed:
                status="exact_time"; stats["exact_time"] += 1
                if best.get("sroddenrating") in HIGH_RR: stats["high_rr_exact_time"] += 1
                if best.get("jd_ut"): stats["exact_with_jd_ut"] += 1
            else:
                status="time_unknown"; stats["time_unknown"] += 1
        rows.append({
            "adb_id":other,"partner_name":rec["partner_name"],"status":status,"resolution_method":method,
            "focal_ids":sorted(rec["focal_ids"]),"event_ids":sorted(rec["event_ids"]),
            "matched":best,"first_search_hit_if_unmatched":first_any if best is None else None,
        })
        print(f"{i}/{len(targets)} {other} {rec['partner_name']} -> {status} ({method})", flush=True)

    n=len(targets); exact=stats["exact_time"]; hi=stats["high_rr_exact_time"]
    summary={
        "source":CSAMPLE,"api":API,
        "eligible_external_eventlinked_targets":n,
        "status_counts":dict(stats),
        "exact_time_recovery_fraction": exact/n if n else 0,
        "high_rr_exact_time_recovery_fraction": hi/n if n else 0,
        "existing_internal_high_rr_timed_eventlinked_pairs":19,
        "projected_total_exact_pair_records_after_recovery":19+exact,
        "projected_total_high_rr_exact_pair_records_after_recovery":19+hi,
        "records":rows,
        "notes":[
            "Eligible targets require A/AA timed focal C-sample record plus the same strict partner-token event linkage used in the C-sample audit.",
            "Exact public record identity is accepted only when wiki DatamainID equals rel_adb_id.",
            "Direct exact-title lookup is attempted before full-text search; this changes only recovery efficiency, not inclusion.",
            "Presence of sbtime with t_unknown absent is treated as exact-time availability; Rodden quality is reported separately.",
            "A full semi-Markov build still needs reliable UTC conversion/JD for recovered partners; this audit records jd_ut if exposed by wiki source but does not invent it."
        ]
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="records"},indent=2),flush=True)

if __name__=="__main__": main()
