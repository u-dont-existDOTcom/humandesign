#!/usr/bin/env python3
"""Probe whether external Astro-Databank romantic-link targets can be resolved
back to public ADB wiki pages with exact timed natal records.

Development/data-recovery audit only. Raw public pages/XML are not committed.
"""
from __future__ import annotations

import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "adb_external_partner_exact_time_probe_v1.json"
CSAMPLE = "https://www.astro.com/adbexport/c_sample.xml"
API_CANDIDATES = [
    "https://www.astro.com/wiki/astro-databank/api.php",
    "https://www.astro.com/astro-databank/api.php",
]
ROMANTIC_REL_IDS = {843, 858, 859}
UA = "humandesign-research-audit/1.0"
PROBE_LIMIT = 60


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean_partner_name(text: str) -> str:
    # Relationship text commonly includes name plus DOB in parentheses.
    s = re.sub(r"\([^)]*\)", "", text or "").strip()
    s = re.sub(r"\s+", " ", s)
    # Convert ADB lastname-first form to natural form for search where obvious.
    if "," in s:
        a, b = [x.strip() for x in s.split(",", 1)]
        if a and b:
            return f"{b} {a}"
    return s


def api_json(api: str, params: dict) -> dict | None:
    url = api + "?" + urllib.parse.urlencode(params)
    try:
        raw = get(url)
        return json.loads(raw.decode("utf-8", errors="replace"))
    except Exception:
        return None


def search_titles(name: str) -> tuple[str | None, list[str]]:
    for api in API_CANDIDATES:
        data = api_json(api, {
            "action": "query", "list": "search", "srsearch": name,
            "srlimit": 5, "format": "json"
        })
        if not data:
            continue
        hits = [x.get("title", "") for x in data.get("query", {}).get("search", []) if x.get("title")]
        return api, hits
    return None, []


def fetch_wikitext(api: str, title: str) -> str | None:
    data = api_json(api, {
        "action": "query", "prop": "revisions", "rvprop": "content",
        "rvslots": "main", "titles": title, "formatversion": 2, "format": "json"
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return None
    revs = pages[0].get("revisions", [])
    if not revs:
        return None
    rev = revs[0]
    slots = rev.get("slots", {})
    if "main" in slots:
        return slots["main"].get("content")
    return rev.get("content") or rev.get("*")


def parse_dma(text: str) -> dict:
    def field(name: str):
        m = re.search(rf"\|{re.escape(name)}\s*=\s*([^\n\r|}}]+)", text or "", re.I)
        return m.group(1).strip() if m else None
    return {
        "DatamainID": field("DatamainID"),
        "sbdate": field("sbdate"),
        "sbtime": field("sbtime"),
        "t_unknown": field("t_unknown"),
        "sroddenrating": field("sroddenrating"),
        "swikiname": field("swikiname"),
    }


def main():
    xml = get(CSAMPLE, timeout=120)
    root = ET.fromstring(xml)
    internal_ids = {int(e.attrib["adb_id"]) for e in root.findall("adb_entry")}
    external = {}
    for e in root.findall("adb_entry"):
        research = e.find("research_data")
        if research is None: continue
        rel_parent = research.find("relationships")
        if rel_parent is None: continue
        for rel in rel_parent.findall("relationship"):
            try:
                rid = int(rel.attrib.get("rel_id", "0"))
                other = int(rel.attrib.get("rel_adb_id", "0"))
            except ValueError:
                continue
            if rid not in ROMANTIC_REL_IDS or not other or other in internal_ids:
                continue
            text = (rel.text or "").strip()
            name = clean_partner_name(text)
            if name:
                external.setdefault(other, {"adb_id": other, "name": name, "raw_rel_text": text})

    sample = [external[k] for k in sorted(external)[:PROBE_LIMIT]]
    rows = []
    status = Counter()
    exact = 0
    high_rr_exact = 0
    id_match = 0
    for i, rec in enumerate(sample, 1):
        api, titles = search_titles(rec["name"])
        best = None
        if api:
            for title in titles:
                wt = fetch_wikitext(api, title)
                if not wt: continue
                dma = parse_dma(wt)
                if dma.get("DatamainID") and str(rec["adb_id"]) == str(dma["DatamainID"]):
                    best = {"title": title, **dma, "id_match": True}
                    id_match += 1
                    break
                if best is None:
                    best = {"title": title, **dma, "id_match": False}
        if not api:
            st = "api_unreachable"
        elif not titles:
            st = "no_search_hit"
        elif best is None:
            st = "no_wikitext"
        elif not best.get("id_match"):
            st = "search_hit_wrong_id"
        else:
            unknown = bool(best.get("t_unknown")) and str(best.get("t_unknown")).strip() not in {"", "0", "None"}
            timed = bool(best.get("sbtime")) and not unknown
            if timed:
                st = "resolved_exact_time"
                exact += 1
                if best.get("sroddenrating") in {"AA", "A"}:
                    high_rr_exact += 1
            else:
                st = "resolved_time_unknown"
        status[st] += 1
        rows.append({
            "adb_id": rec["adb_id"], "name": rec["name"], "status": st,
            "matched": best,
        })
        print(i, rec["adb_id"], rec["name"], st, flush=True)

    n = len(rows)
    summary = {
        "source": CSAMPLE,
        "external_unique_romantic_targets_total": len(external),
        "probe_limit": PROBE_LIMIT,
        "probe_n": n,
        "api_candidates": API_CANDIDATES,
        "status_counts": dict(status),
        "id_matched_public_records": id_match,
        "resolved_exact_time": exact,
        "resolved_high_rr_exact_time": high_rr_exact,
        "exact_time_recovery_fraction": exact / n if n else 0,
        "high_rr_exact_time_recovery_fraction": high_rr_exact / n if n else 0,
        "projection_if_representative": {
            "exact_times_among_all_external_targets": round(len(external) * exact / n, 1) if n else 0,
            "high_rr_exact_times_among_all_external_targets": round(len(external) * high_rr_exact / n, 1) if n else 0,
        },
        "records": rows,
        "note": "Projection is only an engineering estimate; full recovery must enumerate all targets and verify DatamainID matches."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k != "records"}, indent=2), flush=True)

if __name__ == "__main__":
    main()
