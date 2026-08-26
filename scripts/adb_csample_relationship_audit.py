#!/usr/bin/env python3
"""Audit Astro-Databank public C-sample for pair-transition research.

Downloads the public 2026 C-sample at runtime, parses birth records,
relationship links, and relationship events, and writes only a compact derived
audit summary. The raw XML is not committed.

This is a data-sufficiency audit, not an astrology model fit.
"""
from __future__ import annotations

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "adb_csample_relationship_audit_v2.json"
URL = "https://www.astro.com/adbexport/c_sample.xml"

ROMANTIC_REL_IDS = {843: "spouse", 859: "spousal_equivalent", 858: "lover"}
REL_EVENT_IDS = {
    807: "meet_significant_person",
    808: "begin_significant_relationship",
    803: "first_sex",
    810: "marriage",
    811: "divorce",
    809: "end_significant_relationship",
    815: "other_relationship",
    974: "extramarital_affair",
}
HIGH_RR = {"AA", "A"}
DOB_RE = re.compile(r"born:\s*([+-]?\d{1,4})/(\d{1,2})/(\d{1,2})([jg]?)", re.I)
PARTNER_RE = re.compile(r"\bwith\s+(.+?)(?:,\s*born:|$)", re.I)


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def name_tokens(name: str) -> set[str]:
    n = norm(name)
    stop = {"relationship", "spouse", "lover", "with", "born", "family", "associates"}
    return {t for t in n.split() if len(t) >= 4 and t not in stop}


def parse_partner_stub(text: str) -> dict | None:
    mdate = DOB_RE.search(text or "")
    if not mdate:
        return None
    mname = PARTNER_RE.search(text or "")
    name = mname.group(1).strip() if mname else ""
    return {
        "name": name,
        "tokens": name_tokens(name),
        "year": int(mdate.group(1)),
        "month": int(mdate.group(2)),
        "day": int(mdate.group(3)),
        "calendar": "julian" if mdate.group(4).lower() == "j" else "gregorian",
    }


def event_date(ev: ET.Element) -> dict[str, int | None]:
    sb = ev.find("./event_data/sbdate")
    if sb is None:
        return {"year": None, "month": None, "day": None}

    def iv(k: str) -> int | None:
        v = sb.attrib.get(k)
        return int(v) if v not in (None, "", "0") else None

    return {"year": iv("iyear"), "month": iv("imonth"), "day": iv("iday")}


def strict_event_matches_tokens(ev: dict, tokens: set[str]) -> bool:
    text = norm((ev.get("notes") or "") + " " + (ev.get("sevcode") or ""))
    words = set(text.split())
    return bool(tokens and any(tok in words for tok in tokens))


def main() -> None:
    print(f"downloading {URL}", flush=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-research-audit/2.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        xml_bytes = r.read()
    print(f"downloaded {len(xml_bytes)} bytes", flush=True)

    root = ET.fromstring(xml_bytes)
    entries: dict[int, dict] = {}
    rr_counts = Counter()
    gender_counts = Counter()
    event_counts = Counter()

    for e in root.findall("adb_entry"):
        adb_id = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None:
            continue
        name = (pub.findtext("name") or "").strip()
        rr = (pub.findtext("roddenrating") or "").strip()
        gender_el = pub.find("gender")
        gender = gender_el.attrib.get("csex", "") if gender_el is not None else ""
        bdata = pub.find("bdata")
        sbdate = bdata.find("sbdate") if bdata is not None else None
        birth_date = None
        if sbdate is not None:
            try:
                birth_date = {
                    "year": int(sbdate.attrib["iyear"]),
                    "month": int(sbdate.attrib["imonth"]),
                    "day": int(sbdate.attrib["iday"]),
                    "calendar": "julian" if sbdate.attrib.get("ccalendar") == "j" else "gregorian",
                }
            except Exception:
                birth_date = None
        sbtime = bdata.find("sbtime") if bdata is not None else None
        timed = bool(sbtime is not None and (sbtime.text or "").strip() and sbtime.attrib.get("jd_ut"))
        jd_ut = float(sbtime.attrib["jd_ut"]) if timed else None
        rr_counts[rr] += 1
        gender_counts[gender] += 1

        rels = []
        events = []
        research = e.find("research_data")
        if research is not None:
            rel_parent = research.find("relationships")
            if rel_parent is not None:
                for rel in rel_parent.findall("relationship"):
                    try:
                        rel_id = int(rel.attrib.get("rel_id", "0"))
                        other = int(rel.attrib.get("rel_adb_id", "0"))
                    except ValueError:
                        continue
                    text = (rel.text or "").strip()
                    rels.append({
                        "rel_id": rel_id,
                        "other": other,
                        "text": text,
                        "notes": rel.attrib.get("relnotes", ""),
                        "partner_stub": parse_partner_stub(text),
                    })
            ev_parent = research.find("events")
            if ev_parent is not None:
                for ev in ev_parent.findall("event"):
                    try:
                        evn_id = int(ev.attrib.get("evn_id", "0"))
                    except ValueError:
                        continue
                    event_counts[evn_id] += 1
                    events.append({
                        "evn_id": evn_id,
                        "sevcode": ev.attrib.get("sevcode", ""),
                        "notes": ev.attrib.get("evnotes", ""),
                        **event_date(ev),
                    })

        entries[adb_id] = {
            "id": adb_id,
            "name": name,
            "tokens": name_tokens(name),
            "rr": rr,
            "gender": gender,
            "birth_date": birth_date,
            "timed": timed,
            "jd_ut": jd_ut,
            "relationships": rels,
            "events": events,
        }

    pair_rel_types: dict[tuple[int, int], set[int]] = defaultdict(set)
    directed_romantic = 0
    external_romantic = 0
    external_parseable_dob = 0
    external_high_rr_timed_focal_parseable_dob = 0
    external_strict_linked_event_rows = []
    external_strict_pairs = set()

    for a, rec in entries.items():
        for rel in rec["relationships"]:
            if rel["rel_id"] not in ROMANTIC_REL_IDS:
                continue
            directed_romantic += 1
            b = rel["other"]
            if b in entries:
                pair_rel_types[tuple(sorted((a, b)))].add(rel["rel_id"])
                continue
            external_romantic += 1
            stub = rel.get("partner_stub")
            if not stub:
                continue
            external_parseable_dob += 1
            if rec["rr"] in HIGH_RR and rec["timed"]:
                external_high_rr_timed_focal_parseable_dob += 1
            linked_here = False
            for ev in rec["events"]:
                if ev["evn_id"] not in REL_EVENT_IDS:
                    continue
                if strict_event_matches_tokens(ev, stub["tokens"]):
                    external_strict_linked_event_rows.append({
                        "source_id": a,
                        "partner_id": b,
                        "event": REL_EVENT_IDS[ev["evn_id"]],
                        "event_id": ev["evn_id"],
                        "year": ev["year"],
                        "month": ev["month"],
                        "day": ev["day"],
                        "focal_high_rr_timed": rec["rr"] in HIGH_RR and rec["timed"],
                    })
                    linked_here = True
            if linked_here:
                external_strict_pairs.add((a, b))

    strict_linked_events = []
    strict_pairs = set()
    romantic_pair_records = []
    for (a, b), reltypes in sorted(pair_rel_types.items()):
        ra, rb = entries[a], entries[b]
        linked = []
        for source, target in ((ra, rb), (rb, ra)):
            for ev in source["events"]:
                if ev["evn_id"] in REL_EVENT_IDS and strict_event_matches_tokens(ev, target["tokens"]):
                    row = {
                        "source_id": source["id"],
                        "partner_id": target["id"],
                        "event": REL_EVENT_IDS[ev["evn_id"]],
                        "event_id": ev["evn_id"],
                        "year": ev["year"],
                        "month": ev["month"],
                        "day": ev["day"],
                    }
                    strict_linked_events.append(row)
                    linked.append(row)
                    strict_pairs.add((a, b))
        romantic_pair_records.append({
            "a": a,
            "b": b,
            "rel_types": sorted(ROMANTIC_REL_IDS[x] for x in reltypes),
            "both_high_rr": ra["rr"] in HIGH_RR and rb["rr"] in HIGH_RR,
            "both_timed": ra["timed"] and rb["timed"],
            "both_high_rr_timed": ra["rr"] in HIGH_RR and rb["rr"] in HIGH_RR and ra["timed"] and rb["timed"],
            "strict_linked_event_count": len(linked),
        })

    pair_counts = {
        "internal_unique_romantic_pairs": len(pair_rel_types),
        "internal_both_timed": sum(p["both_timed"] for p in romantic_pair_records),
        "internal_both_high_rr": sum(p["both_high_rr"] for p in romantic_pair_records),
        "internal_both_high_rr_timed": sum(p["both_high_rr_timed"] for p in romantic_pair_records),
        "internal_with_strict_linked_transition_event": len(strict_pairs),
        "internal_high_rr_timed_with_strict_linked_transition_event": sum(
            p["both_high_rr_timed"] and p["strict_linked_event_count"] > 0 for p in romantic_pair_records
        ),
        "external_romantic_links": external_romantic,
        "external_romantic_links_with_parseable_partner_dob": external_parseable_dob,
        "external_high_rr_timed_focal_links_with_parseable_partner_dob": external_high_rr_timed_focal_parseable_dob,
        "external_pairs_with_strict_linked_transition_event_and_partner_dob": len(external_strict_pairs),
        "external_high_rr_timed_focal_pairs_with_strict_linked_transition_event_and_partner_dob": len({
            (r["source_id"], r["partner_id"]) for r in external_strict_linked_event_rows if r["focal_high_rr_timed"]
        }),
    }

    all_strict_events = strict_linked_events + external_strict_linked_event_rows
    event_precision = Counter()
    for row in all_strict_events:
        precision = "day" if row["day"] else "month" if row["month"] else "year" if row["year"] else "unknown"
        event_precision[precision] += 1

    exact_pair_count = pair_counts["internal_high_rr_timed_with_strict_linked_transition_event"]
    date_only_pair_count = pair_counts["external_high_rr_timed_focal_pairs_with_strict_linked_transition_event_and_partner_dob"]

    summary = {
        "source": URL,
        "raw_bytes": len(xml_bytes),
        "entry_count": len(entries),
        "rodden_rating_counts": dict(sorted(rr_counts.items())),
        "gender_counts": dict(sorted(gender_counts.items())),
        "relationship_scope": {
            "romantic_rel_ids": {str(k): v for k, v in ROMANTIC_REL_IDS.items()},
            "directed_romantic_links": directed_romantic,
            **pair_counts,
        },
        "relationship_event_counts_all_entries": {
            REL_EVENT_IDS[k]: event_counts.get(k, 0) for k in sorted(REL_EVENT_IDS)
        },
        "strict_partner_linkage": {
            "rule": "relationship event evnotes/sevcode must contain >=4-char token from linked/relationship-text partner name; no unique-partner inference",
            "strict_linked_event_count_internal_plus_external": len(all_strict_events),
            "date_precision": dict(event_precision),
            "event_type_counts": dict(Counter(x["event"] for x in all_strict_events)),
        },
        "model_readiness": {
            "minimum_recommended_exact_pair_count_for_first_full_pair_transition_model": 50,
            "exact_high_quality_linked_pairs_available": exact_pair_count,
            "exact_pair_model_sufficient": exact_pair_count >= 50,
            "date_only_external_pair_events_available": date_only_pair_count,
            "date_only_development_model_sufficient_if_50": date_only_pair_count >= 50,
        },
        "notes": [
            "C-sample contains only names beginning with C, so many relationship targets are outside the sample.",
            "For external linked partners, V2 parses only partner birth DATE from the relationship text; no time is invented.",
            "External partner date-only records can support Sun/Venus/Mars/Jupiter/Saturn pair features but not reliable Moon/angles/houses.",
            "This audit intentionally uses strict partner-name matching for dated relationship events and does not infer partner identity merely because only one romantic link exists.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
