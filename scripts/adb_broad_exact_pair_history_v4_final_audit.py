#!/usr/bin/env python3
"""Final source-only audit for V4 broad exact-time romantic-pair histories.

This script summarizes the completed H1-H4 history ladder and evaluates the
already-frozen sample-size gates. It performs no astrology/HD feature
calculation and fits no statistical model.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_freeze_v4.md"
UNIVERSE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
H12 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h1_h2.json"
H3 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h3.json"
H4 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h4.json"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_final_audit.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    u = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    h12 = json.loads(H12.read_text(encoding="utf-8"))
    h3 = json.loads(H3.read_text(encoding="utf-8"))
    h4 = json.loads(H4.read_text(encoding="utf-8"))

    u_by = {x["pair_key"]: x for x in u["pairs"]}
    h12_by = {x["pair_key"]: x for x in h12["pairs"]}
    h3_by = {x["pair_key"]: x for x in h3["pairs"]}
    h4_by = {x["pair_key"]: x for x in h4["pairs"]}
    key_sets = [set(x) for x in (u_by, h12_by, h3_by, h4_by)]
    if not all(s == key_sets[0] for s in key_sets[1:]):
        raise RuntimeError("V4 artifact pair-key universes differ; do not audit/freeze a model")

    source_counts = Counter()
    precision_counts = Counter()
    formation_kind_counts = Counter()
    formation_precision_counts = Counter()
    conflict_counts = Counter()

    endpoint_pairs_all = endpoint_pairs_model = 0
    endpoint_transitions_all = endpoint_transitions_model = 0
    interval_censored_endpoint_pairs_all = interval_censored_endpoint_pairs_model = 0
    reunion_pairs_all = reunion_pairs_model = 0
    reunion_sequences_all = reunion_sequences_model = 0
    repeated_start_reunion_pairs_all = repeated_start_reunion_pairs_model = 0
    model_eligible_pair_count = 0
    model_pairs_with_endpoint_and_prior_state_entry = 0
    all_pairs_with_endpoint_and_prior_state_entry = 0
    model_pairs_with_day_or_month_exit = 0
    all_pairs_with_day_or_month_exit = 0

    for pk in sorted(u_by):
        up = u_by[pk]
        p12 = h12_by[pk]
        p4 = h4_by[pk]
        model_ok = bool(p4.get("model_eligible_birth_and_swieph_after_duplicate_guard"))
        if model_ok:
            model_eligible_pair_count += 1

        exits = p4.get("clean_nonfatal_exits_through_H4", [])
        if exits:
            endpoint_pairs_all += 1
            if model_ok:
                endpoint_pairs_model += 1
            endpoint_transitions_all += len(exits)
            if model_ok:
                endpoint_transitions_model += len(exits)
            if any(x.get("precision") != "day" for x in exits):
                interval_censored_endpoint_pairs_all += 1
                if model_ok:
                    interval_censored_endpoint_pairs_model += 1
            if any(x.get("precision") in {"day", "month"} for x in exits):
                all_pairs_with_day_or_month_exit += 1
                if model_ok:
                    model_pairs_with_day_or_month_exit += 1
            for x in exits:
                source_counts[x.get("source") or "unknown"] += 1
                precision_counts[x.get("precision") or "unknown"] += 1

        # H1 accepted formations are the cleanest explicit state entries available
        # without adding new post-freeze interpretation. H1 relationship-range
        # starts are also explicit interval-censored active-range starts.
        starts = []
        for f in p12.get("H1_merged_transitions", []):
            if f.get("transition") == "formation":
                starts.append({
                    "source": "H1_adb_structured_event",
                    "interval_start": f["interval_start"],
                    "interval_end": f["interval_end"],
                    "precision": f["precision"],
                })
                formation_kind_counts[f.get("event_kind") or "unknown"] += 1
                formation_precision_counts[f.get("precision") or "unknown"] += 1
        for r in p12.get("H1_relationship_ranges", []):
            starts.append({
                "source": "H1_adb_relationship_range_start",
                "interval_start": r["interval_start"],
                "interval_end": r.get("interval_start_latest") or r["interval_start"],
                "precision": "year",
            })

        if exits and any(s["interval_end"] < e["interval_start"] for e in exits for s in starts):
            all_pairs_with_endpoint_and_prior_state_entry += 1
            if model_ok:
                model_pairs_with_endpoint_and_prior_state_entry += 1

        reunions = p4.get("strict_reunion_sequences_through_H4", [])
        if reunions:
            reunion_pairs_all += 1
            reunion_sequences_all += len(reunions)
            if model_ok:
                reunion_pairs_model += 1
                reunion_sequences_model += len(reunions)
            if any((x.get("later_formation") or {}).get("source") == "H4_wikidata_explicit_repeated_start" for x in reunions):
                repeated_start_reunion_pairs_all += 1
                if model_ok:
                    repeated_start_reunion_pairs_model += 1

        for x in p12.get("H2_excluded_ranges", []):
            if x.get("status") == "excluded_conflict_with_H1_formation":
                conflict_counts["H2_range_vs_H1_formation"] += 1
        for x in p4.get("H4_nonqualifying_statements", []):
            if x.get("cause_conflict"):
                conflict_counts["H4_fatal_nonfatal_cause_conflict"] += 1
            if (x.get("end_time") or {}).get("reason") == "nonoverlapping_end_times":
                conflict_counts["H4_nonoverlapping_P582_values"] += 1

    # The final H4 artifact itself is authoritative for the completed source ladder.
    h4_counts = h4.get("final_state_history_counts", {})
    if endpoint_pairs_all != int(h4_counts.get("all_exact_pairs_with_usable_nonfatal_exit", -1)):
        raise RuntimeError("final audit endpoint count disagrees with H4 artifact")
    if endpoint_pairs_model != int(h4_counts.get("model_eligible_pairs_with_usable_nonfatal_exit", -1)):
        raise RuntimeError("final audit model-eligible endpoint count disagrees with H4 artifact")

    dissolution_gate_all = endpoint_pairs_all >= 50
    dissolution_gate_model = endpoint_pairs_model >= 50
    reunion_gate_all = reunion_pairs_all >= 30
    reunion_gate_model = reunion_pairs_model >= 30

    if dissolution_gate_all and dissolution_gate_model:
        dissolution_next = "write_and_freeze_separate_dissolution_semimarkov_model_spec_do_not_fit_yet"
    elif dissolution_gate_all:
        dissolution_next = "frozen_pair_count_gate_passes_but_preflight_eligible_count_is_below_50_write_spec_only_with_fit_blocker"
    else:
        dissolution_next = "do_not_write_or_fit_dissolution_model_spec_insufficient_pairs"

    reunion_next = (
        "write_and_freeze_separate_reunion_hazard_model_spec_do_not_fit_yet"
        if reunion_gate_all and reunion_gate_model else
        "do_not_write_or_fit_reunion_model_spec_insufficient_strict_reunion_pairs"
    )

    out = {
        "status": "development_broad_pair_history_V4_final_source_only_audit",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "artifact_hashes": {
            "universe": sha256(UNIVERSE),
            "H1_H2": sha256(H12),
            "H3": sha256(H3),
            "H4": sha256(H4),
        },
        "universe_counts": u.get("counts", {}),
        "model_eligible_pairs_after_all_duplicate_and_swieph_guards": model_eligible_pair_count,
        "history_evidence": {
            "nonfatal_exit_transitions_by_source": dict(sorted(source_counts.items())),
            "nonfatal_exit_transitions_by_precision": dict(sorted(precision_counts.items())),
            "H1_formation_transitions_by_kind": dict(sorted(formation_kind_counts.items())),
            "H1_formation_transitions_by_precision": dict(sorted(formation_precision_counts.items())),
            "source_defined_conflicts": dict(sorted(conflict_counts.items())),
            "H1_counts": h12.get("H1_counts", {}),
            "H2_counts": h12.get("H2_counts", {}),
            "H3_counts": h3.get("H3_counts", {}),
            "H4_counts": h4.get("H4_counts", {}),
        },
        "final_history_counts": {
            "all_exact_pairs_with_usable_nonfatal_exit": endpoint_pairs_all,
            "model_eligible_pairs_with_usable_nonfatal_exit": endpoint_pairs_model,
            "all_clean_nonfatal_exit_transitions": endpoint_transitions_all,
            "model_eligible_clean_nonfatal_exit_transitions": endpoint_transitions_model,
            "all_endpoint_pairs_with_any_interval_censoring": interval_censored_endpoint_pairs_all,
            "model_endpoint_pairs_with_any_interval_censoring": interval_censored_endpoint_pairs_model,
            "all_endpoint_pairs_with_at_least_one_day_or_month_exit": all_pairs_with_day_or_month_exit,
            "model_endpoint_pairs_with_at_least_one_day_or_month_exit": model_pairs_with_day_or_month_exit,
            "all_endpoint_pairs_with_explicit_prior_H1_state_entry": all_pairs_with_endpoint_and_prior_state_entry,
            "model_endpoint_pairs_with_explicit_prior_H1_state_entry": model_pairs_with_endpoint_and_prior_state_entry,
            "all_pairs_with_strict_reunion_sequence": reunion_pairs_all,
            "model_eligible_pairs_with_strict_reunion_sequence": reunion_pairs_model,
            "all_strict_reunion_sequences": reunion_sequences_all,
            "model_eligible_strict_reunion_sequences": reunion_sequences_model,
            "all_pairs_with_H4_repeated_start_supported_reunion": repeated_start_reunion_pairs_all,
            "model_pairs_with_H4_repeated_start_supported_reunion": repeated_start_reunion_pairs_model,
        },
        "frozen_gate_decisions": {
            "dissolution_nonfatal_exit": {
                "minimum_unique_exact_pairs": 50,
                "all_exact_pair_gate_passed": dissolution_gate_all,
                "model_eligible_pair_count_also_at_least_50": dissolution_gate_model,
                "next_action": dissolution_next,
            },
            "same_partner_reunion": {
                "minimum_unique_exact_pairs_with_strict_sequence": 30,
                "all_exact_pair_gate_passed": reunion_gate_all,
                "model_eligible_pair_count_also_at_least_30": reunion_gate_model,
                "next_action": reunion_next,
            },
        },
        "source_completion": {
            "H1_H2_adb_exact_pages_resolved": h12.get("adb_exact_pages_resolved"),
            "H1_H2_source_failures": h12.get("source_failures", []),
            "H3_identity_counts": h3.get("identity_counts", {}),
            "H3_source_failures": h3.get("source_failures", []),
            "H4_linked_wikidata_qids": h4.get("linked_wikidata_qids"),
            "H4_resolved_claim_entities": h4.get("resolved_claim_entities"),
            "H4_exact_pair_P26_P451_statements": h4.get("exact_pair_P26_P451_statements"),
            "source_hierarchy_complete": bool((h4.get("frozen_gate_result") or {}).get("source_hierarchy_complete")),
        },
        "interpretation": [
            "This audit concerns development-data availability, not astrological predictive performance.",
            "Crossing a frozen sample-size gate authorizes only a separately frozen model specification; it does not authorize immediate fitting.",
            "The reunion gate is evaluated independently and unlike transitions are not pooled merely to reach sample size.",
            "Independent external couples remain required for confirmatory validation of any later development result.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
