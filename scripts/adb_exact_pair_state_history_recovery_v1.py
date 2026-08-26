#!/usr/bin/env python3
"""Recover structured public-ADB state histories for the exact-time V3 pair universe.

Frozen spec:
  reference/research/adb_exact_pair_state_history_recovery_freeze_v1.md

This script performs data recovery only. It does not calculate or inspect
astrology/HD features for any recovered transition.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import adb_exact_pair_timing_v3 as v3
import adb_exact_pair_timing_v3_runner as v3runner

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_freeze_v1.md"
RECOVERY = REPO / "reference" / "research" / "adb_external_eventlinked_exact_recovery_v1.json"
OUT = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v1.json"
API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-state-history-recovery/1.0"
HIGH_RR = {"AA", "A"}
STOP = {"relationship", "spouse", "lover", "with", "born", "family", "associates", "equivalent"}
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
EVENT_LABELS = (
    ("meet", re.compile(r"\bmeet(?:\s+a)?\s+significant\s+person\b", re.I), "formation"),
    ("begin", re.compile(r"\bbegin\s+significant\s+relationship\b", re.I), "formation"),
    ("marriage", re.compile(r"\bmarriage\b", re.I), "formation"),
    ("end", re.compile(r"\bend\s+significant\s+relationship\b", re.I), "dissolution"),
    ("divorce", re.compile(r"\bdivorce\b", re.I), "dissolution"),
)
YEAR_RANGE_RE = re.compile(r"(?<!\d)(1[5-9]\d{2}|20\d{2})\s*[-–—]\s*(1[5-9]\d{2}|20\d{2})(?!\d)")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def name_tokens(s: str | None) -> set[str]:
    return {t for t in norm(s).split() if len(t) >= 4 and t not in STOP}


def norm_title(s: str | None) -> str:
    return norm((s or "").replace("_", " "))


def api_json(params: dict) -> dict | None:
    url = API + "?" + urllib.parse.urlencode(params)
    try:
        return json.loads(v3.get(url, timeout=10).decode("utf-8", errors="replace"))
    except Exception as exc:
        print("api failure", params.get("titles") or params.get("srsearch"), type(exc).__name__, flush=True)
        return None


def fetch_wikitext(title: str) -> str | None:
    data = api_json({
        "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
        "titles": title, "formatversion": 2, "format": "json",
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing") is not None:
        return None
    revs = pages[0].get("revisions", [])
    if not revs:
        return None
    rev = revs[0]
    slots = rev.get("slots", {})
    return (slots.get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")


def search_titles(name: str) -> list[str]:
    variants = [name]
    if "," in name:
        a, b = [x.strip() for x in name.split(",", 1)]
        if a and b:
            variants.append(f"{b} {a}")
    out: list[str] = []
    for q in variants:
        data = api_json({"action": "query", "list": "search", "srsearch": q, "srlimit": 10, "format": "json"})
        if not data:
            continue
        for hit in data.get("query", {}).get("search", []):
            t = hit.get("title")
            if t and t not in out:
                out.append(t)
    return out


def field(text: str, name: str) -> str | None:
    m = re.search(rf"\|{re.escape(name)}\s*=\s*([^\n\r|}}]+)", text or "", re.I)
    return m.group(1).strip() if m else None


def exact_id(text: str | None) -> int | None:
    x = field(text or "", "DatamainID")
    try:
        return int(x) if x is not None else None
    except ValueError:
        return None


def resolve_person(adb_id: int, display_name: str, known_title: str | None) -> tuple[str | None, str | None, str | None]:
    tried: list[str] = []
    for title in (known_title, display_name):
        if not title or title in tried:
            continue
        tried.append(title)
        wt = fetch_wikitext(title)
        if wt and exact_id(wt) == adb_id:
            return title, wt, "known_title" if title == known_title else "direct_name"
    for title in search_titles(display_name):
        if title in tried:
            continue
        tried.append(title)
        wt = fetch_wikitext(title)
        if wt and exact_id(wt) == adb_id:
            return title, wt, "search"
    return None, None, None


def section(text: str, heading: str) -> str:
    m = re.search(rf"(?im)^==\s*{re.escape(heading)}\s*==\s*$", text or "")
    if not m:
        return ""
    tail = text[m.end():]
    n = re.search(r"(?im)^==\s*[^=].*?\s*==\s*$", tail)
    return tail[:n.start()] if n else tail


def bullets(sec: str) -> list[str]:
    out: list[str] = []
    cur: list[str] = []
    for raw in sec.splitlines():
        line = raw.strip()
        if line.startswith("*"):
            if cur:
                out.append(" ".join(cur))
            cur = [line]
        elif cur and line and not line.startswith("=="):
            cur.append(line)
    if cur:
        out.append(" ".join(cur))
    return out


def links(raw: str) -> list[str]:
    return [m.group(1).strip() for m in LINK_RE.finditer(raw or "")]


def plain(raw: str) -> str:
    s = html.unescape(raw or "")
    s = LINK_RE.sub(lambda m: (m.group(2) or m.group(1)).replace("_", " "), s)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip(" *:")


def partner_attributed(raw: str, other_title: str, other_name: str) -> bool:
    nt = norm_title(other_title)
    if nt and any(norm_title(x) == nt for x in links(raw)):
        return True
    words = set(norm(plain(raw)).split())
    toks = name_tokens(other_name)
    return bool(words & toks)


def iso(y: int, m: int, d: int) -> str:
    return date(y, m, d).isoformat()


def last_day(y: int, m: int) -> int:
    if m == 12:
        return (date(y + 1, 1, 1) - date.resolution).day
    return (date(y, m + 1, 1) - date.resolution).day


def parse_date_interval(after_label: str) -> tuple[str, str, str] | None:
    s = plain(after_label)
    # Day Month Year.
    md = re.search(r"(?<!\d)(\d{1,2})\s+([A-Za-z]+)\s+(1[5-9]\d{2}|20\d{2})(?!\d)", s)
    if md:
        d = int(md.group(1)); m = MONTHS.get(md.group(2).casefold()); y = int(md.group(3))
        if m:
            try:
                z = iso(y, m, d)
                return z, z, "day"
            except ValueError:
                pass
    # Month Year.
    mm = re.search(r"\b([A-Za-z]+)\s+(1[5-9]\d{2}|20\d{2})\b", s)
    if mm:
        m = MONTHS.get(mm.group(1).casefold()); y = int(mm.group(2))
        if m:
            return iso(y, m, 1), iso(y, m, last_day(y, m)), "month"
    # Year only.
    yy = re.search(r"(?<!\d)(1[5-9]\d{2}|20\d{2})(?!\d)", s)
    if yy:
        y = int(yy.group(1))
        return iso(y, 1, 1), iso(y, 12, 31), "year"
    return None


def extract_events(source_id: int, source_title: str, wt: str, other_id: int, other_title: str, other_name: str) -> list[dict]:
    out = []
    for raw in bullets(section(wt, "Events")):
        p = plain(raw)
        if "relationship" not in p.casefold():
            continue
        for kind, rx, transition in EVENT_LABELS:
            m = rx.search(p)
            if not m:
                continue
            if not partner_attributed(raw, other_title, other_name):
                break
            dt = parse_date_interval(p[m.end():])
            if not dt:
                break
            lo, hi, precision = dt
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
                "raw": raw,
            })
            break
    return out


def extract_ranges(source_id: int, source_title: str, wt: str, other_id: int, other_title: str, other_name: str) -> list[dict]:
    out = []
    for raw in bullets(section(wt, "Relationships")):
        p = plain(raw)
        low = p.casefold()
        if not any(x in low for x in ("spouse relationship", "lover relationship", "spousal equivalent relationship")):
            continue
        if not partner_attributed(raw, other_title, other_name):
            continue
        # A range is accepted only when it is explicit in a Notes portion if present,
        # otherwise in the relationship bullet itself.
        scan = p.split("Notes:", 1)[1] if "Notes:" in p else p
        for m in YEAR_RANGE_RE.finditer(scan):
            y1, y2 = int(m.group(1)), int(m.group(2))
            if y2 < y1:
                continue
            out.append({
                "source_adb_id": source_id,
                "source_title": source_title,
                "other_adb_id": other_id,
                "section": "Relationships",
                "precision": "year_range",
                "interval_start": iso(y1, 1, 1),
                "interval_start_latest": iso(y1, 12, 31),
                "interval_end_earliest": iso(y2, 1, 1),
                "interval_end": iso(y2, 12, 31),
                "raw": raw,
            })
            break
    return out


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def merge_event_evidence(items: list[dict]) -> tuple[list[dict], int]:
    groups: list[dict] = []
    conflicts = 0
    for ev in sorted(items, key=lambda x: (x["event_kind"], x["interval_start"], x["interval_end"], x["source_adb_id"])):
        candidates = [g for g in groups if g["event_kind"] == ev["event_kind"] and overlap(g, ev)]
        if candidates:
            g = candidates[0]
            g["interval_start"] = max(g["interval_start"], ev["interval_start"])
            g["interval_end"] = min(g["interval_end"], ev["interval_end"])
            g["evidence"].append(ev)
            # The merged interval is at least as precise as every contributing interval.
            if g["interval_start"] == g["interval_end"]:
                g["precision"] = "day"
            elif len(g["interval_start"][:7]) == len(g["interval_end"][:7]) and g["interval_start"][:7] == g["interval_end"][:7]:
                g["precision"] = "month"
        else:
            # Non-overlapping same-kind reports are retained; count a conflict only if
            # a prior same-kind item exists.
            if any(g["event_kind"] == ev["event_kind"] for g in groups):
                conflicts += 1
            groups.append({
                "event_kind": ev["event_kind"],
                "transition": ev["transition"],
                "precision": ev["precision"],
                "interval_start": ev["interval_start"],
                "interval_end": ev["interval_end"],
                "evidence": [ev],
            })
    groups.sort(key=lambda x: (x["interval_start"], x["interval_end"], x["event_kind"]))
    return groups, conflicts


def precision_rank(p: str) -> int:
    return {"day": 3, "month": 2, "year": 1}.get(p, 0)


def derive_history(events: list[dict], ranges: list[dict]) -> tuple[list[dict], int, str]:
    timeline = []
    last_diss_end: str | None = None
    reunion_count = 0
    has_form = False
    has_diss = False
    form_precisions = []
    diss_precisions = []
    for ev in events:
        trans = ev["transition"]
        derived = trans
        if trans == "formation":
            has_form = True
            form_precisions.append(ev["precision"])
            if last_diss_end is not None and ev["interval_start"] > last_diss_end:
                derived = "reunion"
                reunion_count += 1
        else:
            has_diss = True
            diss_precisions.append(ev["precision"])
            last_diss_end = max(last_diss_end or ev["interval_end"], ev["interval_end"])
        timeline.append({
            "derived_transition": derived,
            "event_kind": ev["event_kind"],
            "precision": ev["precision"],
            "interval_start": ev["interval_start"],
            "interval_end": ev["interval_end"],
        })
    for r in ranges:
        timeline.append({
            "derived_transition": "coarse_active_interval",
            "precision": "year_range",
            "interval_start": r["interval_start"],
            "interval_start_latest": r["interval_start_latest"],
            "interval_end_earliest": r["interval_end_earliest"],
            "interval_end": r["interval_end"],
        })
    timeline.sort(key=lambda x: (x["interval_start"], x.get("interval_end", ""), x["derived_transition"]))

    month_or_better_form = any(precision_rank(p) >= 2 for p in form_precisions)
    month_or_better_diss = any(precision_rank(p) >= 2 for p in diss_precisions)
    if has_form and has_diss and month_or_better_form and month_or_better_diss:
        tier = "T3"
    elif has_form and has_diss:
        tier = "T2"
    elif has_form or ranges:
        tier = "T1"
    else:
        tier = "T0"
    return timeline, reunion_count, tier


def load_known_titles() -> dict[int, str]:
    data = json.loads(RECOVERY.read_text(encoding="utf-8"))
    out = {}
    for row in data.get("records", []):
        mat = row.get("matched") or {}
        if mat.get("title"):
            out[int(row["adb_id"])] = mat["title"]
    return out


def display_name(adb_id: int, entries: dict, recovery_rows: dict[int, dict]) -> str:
    if adb_id in entries:
        return entries[adb_id].get("name") or f"ADB {adb_id}"
    row = recovery_rows.get(adb_id) or {}
    return row.get("partner_name") or (row.get("matched") or {}).get("title") or f"ADB {adb_id}"


def main() -> None:
    # Reconstruct the exact V3 pair universe, including its fail-closed SWIEPH/HD
    # birth/design support gate. No event-date astrology is calculated here.
    for p in (v3.EPHE / "sepl_18.se1", v3.EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit("missing " + str(p))
    v3.swe.set_ephe_path(str(v3.EPHE))
    xml = v3.get(v3.URL, timeout=120)
    entries, _validation = v3.parse_csample(xml)
    recovered_people = v3.recovered_people()
    eligible_events = v3runner.make_events_prefilter(entries, recovered_people)
    pair_keys = sorted(set(ev.pair_key for ev in eligible_events))
    pairs = [tuple(int(x.split(":", 1)[1]) for x in pk.split("|")) for pk in pair_keys]

    recovery_data = json.loads(RECOVERY.read_text(encoding="utf-8"))
    recovery_rows = {int(x["adb_id"]): x for x in recovery_data.get("records", [])}
    known_titles = load_known_titles()
    involved = sorted({x for pair in pairs for x in pair})

    resolved: dict[int, dict] = {}
    resolution_counts = Counter()
    for i, adb_id in enumerate(involved, 1):
        name = display_name(adb_id, entries, recovery_rows)
        title, wt, method = resolve_person(adb_id, name, known_titles.get(adb_id))
        if title and wt:
            resolved[adb_id] = {"title": title, "wikitext": wt, "name": name, "method": method}
            resolution_counts[method or "resolved"] += 1
            print(f"resolve {i}/{len(involved)} {adb_id} {name} -> {title} ({method})", flush=True)
        else:
            resolution_counts["unresolved"] += 1
            print(f"resolve {i}/{len(involved)} {adb_id} {name} -> unresolved", flush=True)

    pair_rows = []
    global_counts = Counter()
    precision_counts = Counter()
    event_kind_counts = Counter()
    conflict_total = 0
    reunion_pairs = 0
    endpoint_pairs = 0

    for a, b in pairs:
        pk = f"adb:{min(a,b)}|adb:{max(a,b)}"
        raw_events: list[dict] = []
        raw_ranges: list[dict] = []
        for src, other in ((a, b), (b, a)):
            if src not in resolved or other not in resolved:
                continue
            s = resolved[src]
            o = resolved[other]
            raw_events.extend(extract_events(src, s["title"], s["wikitext"], other, o["title"], o["name"]))
            raw_ranges.extend(extract_ranges(src, s["title"], s["wikitext"], other, o["title"], o["name"]))

        merged, conflicts = merge_event_evidence(raw_events)
        conflict_total += conflicts
        timeline, reunion_count, tier = derive_history(merged, raw_ranges)
        if reunion_count:
            reunion_pairs += 1
        if any(x["transition"] == "dissolution" for x in merged) or reunion_count:
            endpoint_pairs += 1
        global_counts[f"tier_{tier}"] += 1
        global_counts["accepted_event_evidence"] += len(raw_events)
        global_counts["merged_event_transitions"] += len(merged)
        global_counts["accepted_relationship_ranges"] += len(raw_ranges)
        for x in raw_events:
            precision_counts[x["precision"]] += 1
            event_kind_counts[x["event_kind"]] += 1

        pair_rows.append({
            "pair_key": pk,
            "person_a": {"adb_id": a, "name": display_name(a, entries, recovery_rows), "wiki_title": resolved.get(a, {}).get("title")},
            "person_b": {"adb_id": b, "name": display_name(b, entries, recovery_rows), "wiki_title": resolved.get(b, {}).get("title")},
            "history_tier": tier,
            "evidence_conflicts": conflicts,
            "reunion_sequence_count": reunion_count,
            "event_evidence": raw_events,
            "merged_transitions": merged,
            "relationship_ranges": raw_ranges,
            "derived_timeline": timeline,
        })

    out = {
        "status": "development_data_recovery_audit",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "source": "public Astro-Databank C-sample plus public ADB wiki structured Relationships/Events sections",
        "pair_universe": {
            "eligible_exact_v3_pairs": len(pairs),
            "eligible_v3_events_used_to_reconstruct_universe": len(eligible_events),
            "involved_people": len(involved),
        },
        "wiki_resolution": {
            "resolved_people": len(resolved),
            "unresolved_people": len(involved) - len(resolved),
            "methods": dict(resolution_counts),
        },
        "history_counts": {
            "pair_tiers": {k.replace("tier_", ""): global_counts[k] for k in ("tier_T0", "tier_T1", "tier_T2", "tier_T3")},
            "accepted_event_evidence": global_counts["accepted_event_evidence"],
            "merged_event_transitions": global_counts["merged_event_transitions"],
            "accepted_relationship_ranges": global_counts["accepted_relationship_ranges"],
            "event_kind_evidence": dict(event_kind_counts),
            "event_precision_evidence": dict(precision_counts),
            "pairs_with_dissolution_or_reunion_endpoint": endpoint_pairs,
            "pairs_with_inferred_reunion_sequence": reunion_pairs,
            "evidence_conflicts": conflict_total,
        },
        "stop_go": {
            "minimum_endpoint_pairs_for_semimarkov_dissolution_reunion_development": 30,
            "endpoint_pairs_observed": endpoint_pairs,
            "go_for_separate_frozen_model_spec": endpoint_pairs >= 30,
        },
        "pairs": pair_rows,
        "limitations": [
            "ADB development source; not independent validation.",
            "Biography prose is excluded by the frozen V1 extraction rule.",
            "Year-range relationship notes are interval-censored coarse active intervals and are not silently converted to exact transition dates.",
            "No astrology or Human Design feature is inspected or fit in this recovery audit.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
