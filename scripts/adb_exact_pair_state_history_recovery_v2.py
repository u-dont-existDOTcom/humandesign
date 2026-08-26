#!/usr/bin/env python3
"""Frozen V2 competing-risk/later-life augmentation for exact-pair ADB histories.

Spec: reference/research/adb_exact_pair_state_history_recovery_freeze_v2.md
No astrology/HD features are calculated or inspected.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_freeze_v2.md"
V1 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v1.json"
OUT = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v2.json"
API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-state-history-v2/1.0"
END_WORD = re.compile(r"divorc|separat|split|broke\s+up|broken\s+up|annul|dissolv|estrang", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def api_json(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def fetch_wikitext(title: str) -> str | None:
    try:
        data = api_json({
            "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
            "titles": title, "formatversion": 2, "format": "json",
        })
    except Exception as exc:
        print("fetch failure", title, type(exc).__name__, flush=True)
        return None
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing") is not None or not pages[0].get("revisions"):
        return None
    rev = pages[0]["revisions"][0]
    return (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")


def field(text: str, name: str) -> str | None:
    m = re.search(rf"\|{re.escape(name)}\s*=\s*([^\n\r|}}]+)", text or "", re.I)
    return m.group(1).strip() if m else None


def exact_id(text: str, expected: int) -> bool:
    x = field(text, "DatamainID")
    try:
        return int(x or 0) == expected
    except ValueError:
        return False


def section(text: str, heading: str) -> str:
    m = re.search(rf"(?im)^==\s*{re.escape(heading)}\s*==\s*$", text or "")
    if not m:
        return ""
    tail = text[m.end():]
    n = re.search(r"(?im)^==\s*[^=].*?\s*==\s*$", tail)
    return tail[:n.start()] if n else tail


def template_blocks(text: str, template_name: str) -> list[str]:
    lines = (text or "").splitlines()
    out = []
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
    out = {}
    for raw in block.splitlines()[1:]:
        s = raw.strip()
        if s.startswith("|") and "=" in s:
            k, v = s[1:].split("=", 1)
            out[k.strip()] = v.strip()
    return out


def iso(y: int, m: int, d: int) -> str:
    return date(y, m, d).isoformat()


def last_day(y: int, m: int) -> int:
    if m == 12:
        return (date(y + 1, 1, 1) - date.resolution).day
    return (date(y, m + 1, 1) - date.resolution).day


def parse_event_interval(sevdate: str | None, event_string: str | None = None):
    s = (sevdate or "").strip()
    m = re.fullmatch(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m:
        y, mo, d = map(int, m.groups())
        if y and mo and d:
            try:
                z = iso(y, mo, d); return z, z, "day"
            except ValueError:
                return None
        if y and mo:
            try:
                return iso(y, mo, 1), iso(y, mo, last_day(y, mo)), "month"
            except ValueError:
                return None
        if y:
            return iso(y, 1, 1), iso(y, 12, 31), "year"
    s = (event_string or "").strip()
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        mo, d, y = map(int, m.groups())
        try:
            z = iso(y, mo, d); return z, z, "day"
        except ValueError:
            return None
    m = re.fullmatch(r"(\d{1,2})/(\d{4})", s)
    if m:
        mo, y = map(int, m.groups())
        try:
            return iso(y, mo, 1), iso(y, mo, last_day(y, mo)), "month"
        except ValueError:
            return None
    if re.fullmatch(r"\d{4}", s):
        y = int(s); return iso(y, 1, 1), iso(y, 12, 31), "year"
    return None


def structured_event_intervals(wt: str) -> list[dict]:
    out = []
    for raw in template_blocks(section(wt, "Events"), "ASTRODATABANK_evn"):
        f = fields(raw)
        dt = parse_event_interval(f.get("sevdate"), f.get("EventString"))
        if not dt:
            continue
        lo, hi, precision = dt
        out.append({
            "interval_start": lo,
            "interval_end": hi,
            "precision": precision,
            "code_id": f.get("CodeID"),
            "sevcode": f.get("sevcode"),
            "event_notes": f.get("EventNotes"),
        })
    return out


def overlaps_year(ev: dict, year: int) -> bool:
    lo, hi = iso(year, 1, 1), iso(year, 12, 31)
    return max(ev["interval_start"], lo) <= min(ev["interval_end"], hi)


def main() -> None:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    pairs = v1["pairs"]
    people = {}
    for p in pairs:
        for side in ("person_a", "person_b"):
            x = p[side]
            people[int(x["adb_id"])] = {"title": x["wiki_title"], "name": x["name"]}

    life = {}
    failures = []
    for i, (adb_id, meta) in enumerate(sorted(people.items()), 1):
        wt = fetch_wikitext(meta["title"])
        if not wt or not exact_id(wt, adb_id):
            failures.append({"adb_id": adb_id, "title": meta["title"]})
            print(f"life {i}/{len(people)} {adb_id} FAILED", flush=True)
            continue
        evs = structured_event_intervals(wt)
        latest = max((x["interval_start"] for x in evs), default=None)
        life[adb_id] = {"latest_structured_event_start": latest, "structured_event_count": len(evs)}
        print(f"life {i}/{len(people)} {adb_id} events={len(evs)} latest={latest}", flush=True)

    rule_counts = Counter()
    new_endpoint_pairs = 0
    total_endpoint_pairs = 0
    reunion_pairs = 0
    conflict_count = 0
    pair_results = []

    for p in pairs:
        a = int(p["person_a"]["adb_id"]); b = int(p["person_b"]["adb_id"])
        explicit_diss = [x for x in p.get("merged_transitions", []) if x.get("transition") == "dissolution"]
        formations = [x for x in p.get("merged_transitions", []) if x.get("transition") == "formation"]
        inferred = []
        corroborating = []
        excluded = []

        for r in p.get("relationship_ranges", []):
            end_year = int(r["interval_end"][:4])
            end_lo, end_hi = iso(end_year, 1, 1), iso(end_year, 12, 31)
            notes = r.get("relationship_notes") or ""
            rule_a = bool(END_WORD.search(notes))
            la = life.get(a, {}).get("latest_structured_event_start")
            lb = life.get(b, {}).get("latest_structured_event_start")
            rule_b = bool(la and lb and la > end_hi and lb > end_hi)
            if not (rule_a or rule_b):
                excluded.append({"relationship_range": r, "reason": "neither_rule_A_nor_rule_B", "later_a": la, "later_b": lb})
                continue

            item = {
                "derived_transition": "nonfatal_exit_range",
                "interval_start": end_lo,
                "interval_end": end_hi,
                "precision": "year",
                "rule_A_explicit_nonfatal_wording": rule_a,
                "rule_B_both_demonstrably_alive_later": rule_b,
                "relationship_range": r,
                "later_life_a": la,
                "later_life_b": lb,
            }
            if rule_a and rule_b: rule_counts["A_and_B"] += 1
            elif rule_a: rule_counts["A_only"] += 1
            else: rule_counts["B_only"] += 1

            if any(max(d["interval_start"], end_lo) <= min(d["interval_end"], end_hi) for d in explicit_diss):
                item["status"] = "corroborates_explicit_v1_dissolution"
                corroborating.append(item)
                continue
            conflict = any(overlaps_year(f, end_year) for f in formations)
            if conflict:
                item["status"] = "excluded_conflict_with_v1_formation"
                excluded.append(item)
                conflict_count += 1
                continue
            item["status"] = "new_v2_nonfatal_exit"
            inferred.append(item)

        had_v1_endpoint = bool(explicit_diss) or bool(p.get("reunion_sequence_count"))
        has_endpoint = had_v1_endpoint or bool(inferred)
        if has_endpoint:
            total_endpoint_pairs += 1
        if inferred and not had_v1_endpoint:
            new_endpoint_pairs += 1

        exits = [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v1_explicit"} for x in explicit_diss]
        exits += [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v2_range"} for x in inferred]
        reunions = []
        for ex in exits:
            for f in formations:
                if f["interval_start"] > ex["interval_end"]:
                    reunions.append({"exit": ex, "later_formation": {k: f.get(k) for k in ("event_kind", "precision", "interval_start", "interval_end")}})
        if reunions:
            reunion_pairs += 1

        pair_results.append({
            "pair_key": p["pair_key"],
            "had_v1_explicit_endpoint": had_v1_endpoint,
            "new_v2_nonfatal_exits": inferred,
            "corroborating_range_exits": corroborating,
            "excluded_range_exits": excluded,
            "v2_reunion_sequences": reunions,
        })

    out = {
        "status": "development_data_recovery_augmentation",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "v1_artifact": str(V1.relative_to(REPO)),
        "v1_artifact_sha256": sha256(V1),
        "pair_universe": len(pairs),
        "people": len(people),
        "people_with_later_life_event_scan": len(life),
        "source_failures": failures,
        "augmentation_counts": {
            "range_rule_counts": dict(rule_counts),
            "pairs_newly_gaining_nonfatal_exit": new_endpoint_pairs,
            "total_pairs_with_explicit_or_v2_nonfatal_endpoint": total_endpoint_pairs,
            "pairs_with_inferred_reunion_sequence_after_v2": reunion_pairs,
            "excluded_conflicts": conflict_count,
        },
        "stop_go": {
            "minimum_endpoint_pairs": 30,
            "endpoint_pairs_observed": total_endpoint_pairs,
            "go_only_to_separate_model_freeze": total_endpoint_pairs >= 30,
        },
        "pairs": pair_results,
        "limitations": [
            "ADB development source only; not independent validation.",
            "Rule B uses structured dated events only as conservative proof that both partners were alive after the relationship-range endpoint.",
            "Range-derived exits remain full-year interval-censored and are not exact breakup dates.",
            "No astrology or Human Design features are calculated or inspected in V2.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
