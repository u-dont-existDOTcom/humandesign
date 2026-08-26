#!/usr/bin/env python3
"""Compact engineering probe for Astro-Databank raw MediaWiki structure.

This does not alter any research inclusion rule. It records only tiny excerpts
needed to make the frozen structured-section parser match the site's actual
wikitext representation.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "adb_wiki_structure_probe_v1.json"
API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-wiki-structure-probe/1.0"
TITLES = ["Bardot, Brigitte", "Charrier, Jacques", "Nielsen, Brigitte"]


def get_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def fetch_wikitext(title):
    data = get_json({
        "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
        "titles": title, "formatversion": 2, "format": "json",
    })
    pages = data.get("query", {}).get("pages", [])
    if not pages or not pages[0].get("revisions"):
        return None
    rev = pages[0]["revisions"][0]
    return (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")


def template_blocks(text, template_name):
    lines = (text or "").splitlines()
    out = []
    i = 0
    start_rx = re.compile(r"^\{\{\s*" + re.escape(template_name) + r"\s*$", re.I)
    while i < len(lines):
        if start_rx.match(lines[i].strip()):
            block = [lines[i]]
            i += 1
            depth = 1
            while i < len(lines):
                block.append(lines[i])
                depth += lines[i].count("{{") - lines[i].count("}}")
                if depth <= 0:
                    break
                i += 1
            out.append("\n".join(block))
        i += 1
    return out


def fields(block):
    d = {}
    for line in block.splitlines()[1:]:
        s = line.strip()
        if s.startswith("|") and "=" in s:
            k, v = s[1:].split("=", 1)
            d[k.strip()] = v.strip()
    return d


def compact_probe(text):
    lines = (text or "").splitlines()
    headings = []
    hits = []
    for i, raw in enumerate(lines):
        s = raw.strip()
        if re.match(r"^=+.*=+$", s):
            headings.append({"line": i + 1, "text": s[:300]})
        if re.search(r"relationship|events|spouse|divorce|marriage", s, re.I):
            lo = max(0, i - 1); hi = min(len(lines), i + 2)
            hits.append({"line": i + 1, "context": lines[lo:hi]})

    rels = [fields(x) for x in template_blocks(text, "ASTRODATABANK_rel")]
    evns = [fields(x) for x in template_blocks(text, "ASTRODATABANK_evn")]
    spouse_samples = [x for x in rels if x.get("CodeID") in {"843", "858", "859"}][:5]
    relationship_event_samples = [x for x in evns if x.get("CodeID") in {"807", "808", "809", "810", "811"}][:8]
    return {
        "line_count": len(lines),
        "headings": headings[:50],
        "keyword_contexts": hits[:80],
        "relationship_template_field_names": sorted({k for x in rels for k in x}),
        "event_template_field_names": sorted({k for x in evns for k in x}),
        "romantic_relationship_template_samples": spouse_samples,
        "relationship_event_template_samples": relationship_event_samples,
    }


def main():
    rows = []
    for title in TITLES:
        wt = fetch_wikitext(title)
        rows.append({"title": title, "resolved": bool(wt), "probe": compact_probe(wt) if wt else None})
        print(title, "ok" if wt else "missing", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"status": "engineering_probe", "pages": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
