#!/usr/bin/env python3
"""Recover V4 broad-pair state histories from frozen H1/H2 ADB structured sources.

Requires:
  reference/research/adb_broad_exact_pair_universe_v4.json

Frozen rules:
  reference/research/adb_broad_exact_pair_universe_freeze_v4.md

No astrology or Human Design features are calculated or inspected.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import adb_broad_exact_pair_universe_v4 as uni
import adb_exact_pair_state_history_recovery_v1 as v1base
import adb_exact_pair_state_history_recovery_v1_runner as v1raw
import adb_exact_pair_state_history_recovery_v2 as v2logic

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_freeze_v4.md"
UNIVERSE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h1_h2.json"
END_WORD = re.compile(r"divorc|separat|split|broke\s+up|broken\s+up|annul|dissolv|estrang", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def exact_id(wt: str | None) -> int | None:
    return uni.exact_id(wt)


def fetch_people_wikitext(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]]:
    resolved: dict[int, tuple[str, str]] = {}
    failures: list[dict] = []
    titles = sorted({p.get("public_title") or p.get("name") for p in people.values() if p.get("public_title") or p.get("name")})
    for title, wt in uni.fetch_wikitext_batch(titles):
        eid = exact_id(wt)
        if eid in people and eid not in resolved:
            resolved[eid] = (title, wt)
    unresolved = [aid for aid in sorted(people) if aid not in resolved]
    for i, aid in enumerate(unresolved, 1):
        p = people[aid]
        candidates = uni.search_titles(p.get("name") or p.get("public_title") or "")
        found = None
        for title, wt in uni.fetch_wikitext_batch(candidates):
            if exact_id(wt) == aid:
                found = (title, wt); break
        if found:
            resolved[aid] = found
        else:
            failures.append({"adb_id": aid, "name": p.get("name"), "public_title": p.get("public_title")})
        if i % 25 == 0:
            print(f"H1 fallback {i}/{len(unresolved)}", flush=True)
    return resolved, failures


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def merge_same_event(items: list[dict]) -> list[dict]:
    """Merge only overlapping same-kind evidence; retain non-overlapping repeated transitions."""
    groups: list[dict] = []
    for ev in sorted(items, key=lambda x: (x["interval_start"], x["interval_end"], x["event_kind"], x["source_adb_id"])):
        match = None
        for g in groups:
            if g["event_kind"] == ev["event_kind"] and overlap(g, ev):
                match = g; break
        if match is None:
            groups.append({
                "event_kind": ev["event_kind"], "transition": ev["transition"],
                "interval_start": ev["interval_start"], "interval_end": ev["interval_end"],
                "precision": ev["precision"], "evidence": [ev],
            })
        else:
            match["interval_start"] = max(match["interval_start"], ev["interval_start"])
            match["interval_end"] = min(match["interval_end"], ev["interval_end"])
            match["evidence"].append(ev)
            if match["interval_start"] == match["interval_end"]:
                match["precision"] = "day"
            elif match["interval_start"][:7] == match["interval_end"][:7]:
                match["precision"] = "month"
    groups.sort(key=lambda x: (x["interval_start"], x["interval_end"], x["event_kind"]))
    return groups


def range_exit(range_ev: dict, life: dict[int, dict], a: int, b: int, formations: list[dict], explicit_exits: list[dict]):
    end_year = int(range_ev["interval_end"][:4])
    lo, hi = f"{end_year:04d}-01-01", f"{end_year:04d}-12-31"
    notes = range_ev.get("relationship_notes") or ""
    rule_a = bool(END_WORD.search(notes))
    la = life.get(a, {}).get("latest_structured_event_start")
    lb = life.get(b, {}).get("latest_structured_event_start")
    rule_b = bool(la and lb and la > hi and lb > hi)
    if not (rule_a or rule_b):
        return "excluded", {
            "relationship_range": range_ev, "reason": "neither_H2_rule_A_nor_rule_B",
            "later_a": la, "later_b": lb,
        }
    item = {
        "transition": "nonfatal_exit", "source": "H2_adb_finite_range",
        "interval_start": lo, "interval_end": hi, "precision": "year",
        "rule_A_explicit_nonfatal_wording": rule_a,
        "rule_B_both_demonstrably_alive_later": rule_b,
        "relationship_range": range_ev,
        "later_life_a": la, "later_life_b": lb,
    }
    if any(overlap(x, item) for x in explicit_exits):
        item["status"] = "corroborates_H1_explicit_exit"
        return "corroborating", item
    if any(overlap(x, item) for x in formations):
        item["status"] = "excluded_conflict_with_H1_formation"
        return "excluded", item
    item["status"] = "accepted_H2_nonfatal_exit"
    return "accepted", item


def main():
    if not UNIVERSE.is_file():
        raise SystemExit(f"missing universe artifact: {UNIVERSE}")
    data = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    pairs = data["pairs"]
    people: dict[int, dict] = {}
    for p in pairs:
        for side in ("person_a", "person_b"):
            x = p[side]
            people[int(x["adb_id"])] = x

    pages, failures = fetch_people_wikitext(people)
    print(f"H1 exact ADB pages resolved {len(pages)}/{len(people)} failures={len(failures)}", flush=True)

    # Structured life evidence for the conservative H2 competing-risk rule.
    life = {}
    for aid, (_title, wt) in pages.items():
        evs = v2logic.structured_event_intervals(wt)
        life[aid] = {
            "structured_event_count": len(evs),
            "latest_structured_event_start": max((x["interval_start"] for x in evs), default=None),
        }

    h1_kind_counts = Counter(); h1_precision = Counter(); h1_transition = Counter()
    h2_rule_counts = Counter(); pair_endpoint_count = 0; reunion_pair_count = 0
    h2_accepted_count = 0; h2_corroborating_count = 0; h2_excluded_count = 0
    interval_censored_endpoint_pairs = 0
    pair_rows = []

    for idx, p in enumerate(pairs, 1):
        a = int(p["person_a"]["adb_id"]); b = int(p["person_b"]["adb_id"])
        all_events = []
        all_ranges = []
        for src, other in ((a, b), (b, a)):
            if src not in pages:
                continue
            title, wt = pages[src]
            other_meta = people[other]
            other_title = pages.get(other, (other_meta.get("public_title") or other_meta.get("name") or "", ""))[0]
            evs = v1raw.extract_events(src, title, wt, other, other_title, other_meta.get("name") or other_title)
            rng = v1raw.extract_ranges(src, title, wt, other, other_title, other_meta.get("name") or other_title)
            all_events.extend(evs); all_ranges.extend(rng)
            for e in evs:
                h1_kind_counts[e["event_kind"]] += 1
                h1_precision[e["precision"]] += 1
                h1_transition[e["transition"]] += 1

        merged = merge_same_event(all_events)
        formations = [x for x in merged if x["transition"] == "formation"]
        explicit_exits = [x for x in merged if x["transition"] == "dissolution"]

        accepted_h2 = []; corroborating_h2 = []; excluded_h2 = []
        seen_range_keys = set()
        for r in all_ranges:
            # Mirrored A/B range templates describing the same active interval are one datum.
            rk = (r["interval_start"], r["interval_end"], r.get("code_id"))
            if rk in seen_range_keys:
                continue
            seen_range_keys.add(rk)
            status, item = range_exit(r, life, a, b, formations, explicit_exits)
            if status == "accepted":
                accepted_h2.append(item); h2_accepted_count += 1
                ra, rb = item["rule_A_explicit_nonfatal_wording"], item["rule_B_both_demonstrably_alive_later"]
                h2_rule_counts["A_and_B" if ra and rb else "A_only" if ra else "B_only"] += 1
            elif status == "corroborating":
                corroborating_h2.append(item); h2_corroborating_count += 1
            else:
                excluded_h2.append(item); h2_excluded_count += 1

        exits = [
            {"source": "H1_adb_structured_event", "event_kind": x["event_kind"],
             "interval_start": x["interval_start"], "interval_end": x["interval_end"], "precision": x["precision"]}
            for x in explicit_exits
        ] + [
            {"source": "H2_adb_finite_range", "event_kind": "range_nonfatal_exit",
             "interval_start": x["interval_start"], "interval_end": x["interval_end"], "precision": x["precision"]}
            for x in accepted_h2
        ]
        if exits:
            pair_endpoint_count += 1
            if any(x["precision"] != "day" for x in exits):
                interval_censored_endpoint_pairs += 1

        reunions = []
        for ex in exits:
            for f in formations:
                if f["interval_start"] > ex["interval_end"]:
                    reunions.append({
                        "exit": ex,
                        "later_formation": {
                            "source": "H1_adb_structured_event", "event_kind": f["event_kind"],
                            "interval_start": f["interval_start"], "interval_end": f["interval_end"],
                            "precision": f["precision"],
                        },
                    })
        if reunions:
            reunion_pair_count += 1

        pair_rows.append({
            "pair_key": p["pair_key"],
            "H1_event_evidence": all_events,
            "H1_merged_transitions": merged,
            "H1_relationship_ranges": all_ranges,
            "H2_accepted_nonfatal_exits": accepted_h2,
            "H2_corroborating_range_exits": corroborating_h2,
            "H2_excluded_ranges": excluded_h2,
            "clean_nonfatal_exits_through_H2": exits,
            "strict_reunion_sequences_through_H2": reunions,
        })
        if idx % 50 == 0:
            print(f"history H1/H2 {idx}/{len(pairs)}", flush=True)

    out = {
        "status": "development_broad_pair_history_H1_H2",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "universe_artifact": str(UNIVERSE.relative_to(REPO)),
        "universe_sha256": sha256(UNIVERSE),
        "pair_universe": len(pairs),
        "people": len(people),
        "adb_exact_pages_resolved": len(pages),
        "source_failures": failures,
        "H1_counts": {
            "event_evidence_by_kind": dict(sorted(h1_kind_counts.items())),
            "event_evidence_by_transition": dict(sorted(h1_transition.items())),
            "event_evidence_by_precision": dict(sorted(h1_precision.items())),
        },
        "H2_counts": {
            "accepted_nonfatal_range_exits": h2_accepted_count,
            "corroborating_range_exits": h2_corroborating_count,
            "excluded_ranges": h2_excluded_count,
            "rule_counts": dict(sorted(h2_rule_counts.items())),
        },
        "state_history_counts_through_H2": {
            "pairs_with_at_least_one_usable_nonfatal_exit": pair_endpoint_count,
            "pairs_with_strict_exit_then_later_same_partner_formation": reunion_pair_count,
            "endpoint_pairs_with_any_interval_censoring": interval_censored_endpoint_pairs,
        },
        "sufficiency_preview_not_model_authorization": {
            "dissolution_gate_50": pair_endpoint_count >= 50,
            "reunion_gate_30": reunion_pair_count >= 30,
            "note": "V4 requires completing frozen H3/H4 history augmentation and the final broad-universe audit before any separate model specification is written.",
        },
        "pairs": pair_rows,
        "limitations": [
            "ADB development data only; not independent validation.",
            "H1 uses exact structured ADB relationship/event templates and strict partner attribution; H2 uses only the frozen conservative finite-range rule.",
            "No Biography prose is used.",
            "No astrology or Human Design features are calculated or inspected.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
