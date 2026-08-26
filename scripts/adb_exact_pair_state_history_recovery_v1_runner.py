#!/usr/bin/env python3
"""Engineering runner for frozen ADB exact-pair state-history recovery V1.

The first implementation expected rendered bullet-like wikitext, while public
ADB raw pages store Relationships and Events as ASTRODATABANK_rel / _evn
templates. This runner adapts parsing to the observed raw template structure
without changing the frozen pair universe, allowed sections, transition labels,
partner-attribution standard, date-precision rules, or stop/go threshold.
"""
from __future__ import annotations

import re

import adb_exact_pair_state_history_recovery_v1 as base

ROMANTIC_CODES = {843, 858, 859}
EVENT_CODES = {
    807: ("meet", "formation"),
    808: ("begin", "formation"),
    809: ("end", "dissolution"),
    810: ("marriage", "formation"),
    811: ("divorce", "dissolution"),
}


def template_blocks(text: str, template_name: str) -> list[str]:
    lines = (text or "").splitlines()
    out: list[str] = []
    start_rx = re.compile(r"^\{\{\s*" + re.escape(template_name) + r"\s*$", re.I)
    i = 0
    while i < len(lines):
        if not start_rx.match(lines[i].strip()):
            i += 1
            continue
        block = [lines[i]]
        depth = lines[i].count("{{") - lines[i].count("}}")
        i += 1
        while i < len(lines) and depth > 0:
            block.append(lines[i])
            depth += lines[i].count("{{") - lines[i].count("}}")
            i += 1
        out.append("\n".join(block))
    return out


def fields(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in block.splitlines()[1:]:
        s = raw.strip()
        if s.startswith("|") and "=" in s:
            k, v = s[1:].split("=", 1)
            out[k.strip()] = v.strip()
    return out


def parse_sevdate(value: str | None, fallback: str | None = None):
    s = (value or "").strip()
    m = re.fullmatch(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m:
        y, mo, d = map(int, m.groups())
        if y and mo and d:
            try:
                z = base.iso(y, mo, d)
                return z, z, "day"
            except ValueError:
                return None
        if y and mo:
            try:
                return base.iso(y, mo, 1), base.iso(y, mo, base.last_day(y, mo)), "month"
            except ValueError:
                return None
        if y:
            return base.iso(y, 1, 1), base.iso(y, 12, 31), "year"
    # EventString is generally M/D/YYYY, M/YYYY, or YYYY.
    fs = (fallback or "").strip()
    md = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", fs)
    if md:
        mo, d, y = map(int, md.groups())
        try:
            z = base.iso(y, mo, d)
            return z, z, "day"
        except ValueError:
            return None
    mm = re.fullmatch(r"(\d{1,2})/(\d{4})", fs)
    if mm:
        mo, y = map(int, mm.groups())
        try:
            return base.iso(y, mo, 1), base.iso(y, mo, base.last_day(y, mo)), "month"
        except ValueError:
            return None
    yy = re.fullmatch(r"(\d{4})", fs)
    if yy:
        y = int(yy.group(1))
        return base.iso(y, 1, 1), base.iso(y, 12, 31), "year"
    return None


def event_partner_match(event_notes: str, other_name: str, other_title: str) -> bool:
    words = set(base.norm(event_notes).split())
    toks = base.name_tokens(other_name) | base.name_tokens(other_title)
    return bool(words & toks)


def extract_events(source_id: int, source_title: str, wt: str, other_id: int, other_title: str, other_name: str) -> list[dict]:
    out = []
    sec = base.section(wt, "Events")
    for raw in template_blocks(sec, "ASTRODATABANK_evn"):
        f = fields(raw)
        try:
            code = int(f.get("CodeID", "0"))
        except ValueError:
            continue
        if code not in EVENT_CODES:
            continue
        notes = f.get("EventNotes", "")
        if not event_partner_match(notes, other_name, other_title):
            continue
        dt = parse_sevdate(f.get("sevdate"), f.get("EventString"))
        if not dt:
            continue
        lo, hi, precision = dt
        kind, transition = EVENT_CODES[code]
        out.append({
            "source_adb_id": source_id,
            "source_title": source_title,
            "other_adb_id": other_id,
            "section": "Events",
            "event_kind": kind,
            "transition": transition,
            "precision": precision,
            "interval_start": lo,
            "interval_end": hi,
            "code_id": code,
            "event_notes": notes,
            "sevcode": f.get("sevcode"),
            "sevdate": f.get("sevdate"),
            "event_string": f.get("EventString"),
        })
    return out


def extract_ranges(source_id: int, source_title: str, wt: str, other_id: int, other_title: str, other_name: str) -> list[dict]:
    out = []
    sec = base.section(wt, "Relationships")
    for raw in template_blocks(sec, "ASTRODATABANK_rel"):
        f = fields(raw)
        try:
            code = int(f.get("CodeID", "0"))
            linked_id = int(f.get("RelatedDatamainID", "0"))
        except ValueError:
            continue
        if code not in ROMANTIC_CODES or linked_id != other_id:
            continue
        notes = f.get("RelationshipNotes", "")
        m = base.YEAR_RANGE_RE.search(notes)
        if not m:
            continue
        y1, y2 = int(m.group(1)), int(m.group(2))
        if y2 < y1:
            continue
        out.append({
            "source_adb_id": source_id,
            "source_title": source_title,
            "other_adb_id": other_id,
            "section": "Relationships",
            "precision": "year_range",
            "interval_start": base.iso(y1, 1, 1),
            "interval_start_latest": base.iso(y1, 12, 31),
            "interval_end_earliest": base.iso(y2, 1, 1),
            "interval_end": base.iso(y2, 12, 31),
            "code_id": code,
            "related_datamain_id": linked_id,
            "partner_name": f.get("PName"),
            "partner_link": f.get("PName_link"),
            "relationship_notes": notes,
        })
    return out


if __name__ == "__main__":
    base.extract_events = extract_events
    base.extract_ranges = extract_ranges
    base.main()
