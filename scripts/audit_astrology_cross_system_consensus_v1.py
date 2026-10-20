#!/usr/bin/env python3
"""Conservative source/signal-lineage convergence audit (symbolic, not calibrated).

This tool does NOT convert multiple astrological testimonies to probabilities.
It reports one vote per source tradition, collapsing identical underlying signals
and source lineages. No respondent outcomes are accepted or read.
"""

from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SCHEMA = "astro-cross-system-consensus-input-v1"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def nonempty(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def list_of_nonempty(x: Any) -> bool:
    return isinstance(x, list) and bool(x) and all(nonempty(y) for y in x) and len(x) == len(set(x))


def grouped_votes(votes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Union connected components sharing any source lineage or sky-signal root."""
    if not votes:
        return []
    parent = list(range(len(votes)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    keys: dict[str, int] = {}
    for i, v in enumerate(votes):
        for key in v["dependency_keys"]:
            if key in keys:
                union(i, keys[key])
            else:
                keys[key] = i

    out: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for i, v in enumerate(votes):
        out[find(i)].append(v)
    result = []
    for members in out.values():
        favored = {m["preferred_outcome"] for m in members}
        result.append({
            "systems": sorted(m["system_id"] for m in members),
            "preferred_outcome": next(iter(favored)) if len(favored) == 1 else None,
            "conflicted": len(favored) > 1,
            "shared_dependency_keys": sorted(set().union(*(set(m["dependency_keys"]) for m in members))),
        })
    return sorted(result, key=lambda g: (g["systems"], g["shared_dependency_keys"]))


def audit(data: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(data, dict) and data.get("schema") == SCHEMA, "invalid schema")
    require(nonempty(data.get("study_id")), "missing study_id")
    claims = data.get("claims")
    require(isinstance(claims, list) and bool(claims), "nonempty claims required")
    claim_ids: set[str] = set()
    results = []
    for cl in claims:
        require(isinstance(cl, dict), "each claim must be an object")
        cid = cl.get("claim_id")
        require(nonempty(cid) and cid not in claim_ids, "missing/duplicate claim_id")
        claim_ids.add(cid)
        outcomes = cl.get("outcomes")
        require(list_of_nonempty(outcomes) and len(outcomes) >= 2, f"{cid}: exclusive outcomes required")
        testimony = cl.get("testimonies")
        require(isinstance(testimony, list), f"{cid}: testimonies must be list")
        seen_ids: set[str] = set()
        raw_per_system: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in testimony:
            require(isinstance(item, dict), f"{cid}: invalid testimony")
            ident, system, pref = item.get("testimony_id"), item.get("system_id"), item.get("preferred_outcome")
            require(nonempty(ident) and ident not in seen_ids, f"{cid}: missing/duplicate testimony_id")
            seen_ids.add(ident)
            require(nonempty(system), f"{cid}/{ident}: system_id required")
            require(pref in outcomes or pref is None, f"{cid}/{ident}: preference outside outcomes")
            require(nonempty(item.get("source_locator")), f"{cid}/{ident}: source locator required")
            signal = item.get("signal_keys")
            lineage = item.get("source_lineage_keys")
            require(list_of_nonempty(signal) and list_of_nonempty(lineage),
                    f"{cid}/{ident}: nonempty signal_keys and source_lineage_keys required")
            raw_per_system[system].append(item)
        system_rows = []
        admitted = []
        for system, items in sorted(raw_per_system.items()):
            directions = {item["preferred_outcome"] for item in items if item["preferred_outcome"] is not None}
            prefer = next(iter(directions)) if len(directions) == 1 else None
            status = "CONFLICTED" if len(directions) > 1 else "ABSTAIN" if not directions else "DIRECTIONAL"
            keys = sorted({"sky:" + s for item in items for s in item["signal_keys"]}
                          | {"source:" + s for item in items for s in item["source_lineage_keys"]})
            system_rows.append({"system_id": system, "status": status, "preferred_outcome": prefer,
                                "testimony_count": len(items), "dependency_keys": keys})
            if status == "DIRECTIONAL":
                admitted.append({"system_id": system, "preferred_outcome": prefer, "dependency_keys": keys})
        groups = grouped_votes(admitted)
        support = {o: sum(g["preferred_outcome"] == o for g in groups) for o in outcomes}
        conflicting_groups = sum(g["conflicted"] for g in groups)
        max_votes = max(support.values(), default=0)
        tops = [o for o in outcomes if support[o] == max_votes]
        winner = tops[0] if max_votes > 0 and len(tops) == 1 and not conflicting_groups else None
        results.append({
            "claim_id": cid,
            "outcomes": outcomes,
            "raw_testimony_count": len(testimony),
            "system_count": len(raw_per_system),
            "admitted_directional_system_count": len(admitted),
            "system_votes": system_rows,
            "lineage_distinct_groups": groups,
            "lineage_distinct_support_by_outcome": support,
            "conflicted_lineage_groups": conflicting_groups,
            "symbolic_consensus_option": winner,
            "symbolic_consensus_strength": max_votes if winner else 0,
            "empirical_probability_or_validated_weight": None,
        })
    return {
        "schema": "astro-cross-system-consensus-audit-v1",
        "study_id": data["study_id"],
        "input_sha256": hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(),
        "status": "UNVALIDATED_SYMBOLIC_LINEAGE_AUDIT",
        "independent_human_predictive_success": None,
        "interpretation": "A convergence count is a research diagnostic, never an empirical accuracy estimate. Source and astronomy dependencies may remain unobserved.",
        "claims": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input_json.read_text(encoding="utf-8"))
        result = audit(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())