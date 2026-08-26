#!/usr/bin/env python3
"""V4 broad exact-pair history H4: exact linked-Wikidata relationship qualifiers.

Frozen rules:
  reference/research/adb_broad_exact_pair_universe_freeze_v4.md
  reference/research/adb_exact_pair_state_history_source_ladder_v3_rung3_parser_freeze.md

Identity QIDs are inherited only from V4 H3's exact ADB -> explicit linked
English-Wikipedia chain. No Wikidata search occurs. No astrology/HD features are
calculated or inspected.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import adb_exact_pair_state_history_source_ladder_v3_rung3 as wd

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_freeze_v4.md"
WD_FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung3_parser_freeze.md"
UNIVERSE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
H12 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h1_h2.json"
H3 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h3.json"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h4.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def time_interval(statement: dict, prop: str) -> dict:
    """Use the already-frozen Wikidata time parser/overlap rule for P580 or P582."""
    return wd.merge_end_times(((statement.get("qualifiers") or {}).get(prop) or []))


def main() -> None:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    h12 = json.loads(H12.read_text(encoding="utf-8"))
    h3 = json.loads(H3.read_text(encoding="utf-8"))
    h12_by = {x["pair_key"]: x for x in h12["pairs"]}

    qids = sorted({
        q
        for p in h3["pairs"]
        for ident in (p.get("wikipedia_identity_a") or {}, p.get("wikipedia_identity_b") or {})
        for q in [ident.get("wikidata_qid")]
        if q
    })
    entities = wd.fetch_entities(qids, "claims")

    exact_statements: dict[str, list[dict]] = {}
    cause_qids = set()
    exact_statement_count = 0
    for p in h3["pairs"]:
        pk = p["pair_key"]
        qa = (p.get("wikipedia_identity_a") or {}).get("wikidata_qid")
        qb = (p.get("wikipedia_identity_b") or {}).get("wikidata_qid")
        rows = []
        if qa and qb and qa != qb:
            for src_q, other_q, direction in ((qa, qb, "a_to_b"), (qb, qa, "b_to_a")):
                claims = ((entities.get(src_q) or {}).get("claims") or {})
                for prop in wd.REL_PROPS:
                    for statement_index, st in enumerate(claims.get(prop, []) or []):
                        if st.get("rank") == "deprecated":
                            continue
                        if wd.entity_value_id(st.get("mainsnak") or {}) != other_q:
                            continue
                        exact_statement_count += 1
                        causes = wd.qualifier_entity_ids(st, "P1534")
                        cause_qids.update(causes)
                        rows.append({
                            "source_qid": src_q,
                            "other_qid": other_q,
                            "direction": direction,
                            "property": prop,
                            "statement_index": statement_index,
                            "statement": st,
                            "cause_qids": causes,
                        })
        exact_statements[pk] = rows

    cause_entities = wd.fetch_entities(sorted(cause_qids), "labels") if cause_qids else {}
    cause_labels = {
        q: (((cause_entities.get(q) or {}).get("labels") or {}).get("en") or {}).get("value")
        for q in sorted(cause_qids)
    }

    counts = Counter()
    cause_label_counts = Counter()
    endpoint_all = endpoint_model = new_pair_all = new_pair_model = 0
    reunion_all = reunion_model = 0
    repeated_start_reunion_all = repeated_start_reunion_model = 0
    pair_rows = []

    for p in h3["pairs"]:
        pk = p["pair_key"]
        baseline = list(p.get("clean_nonfatal_exits_through_H3", []))
        had_baseline = bool(baseline)
        model_ok = bool(p.get("model_eligible_birth_and_swieph_after_H3_duplicate_guard"))
        h1_formations = [x for x in h12_by[pk].get("H1_merged_transitions", []) if x.get("transition") == "formation"]

        accepted = []
        corroborating = []
        nonqualifying = []
        explicit_episode_starts = []

        for row in exact_statements.get(pk, []):
            st = row["statement"]
            start = time_interval(st, "P580")
            end = time_interval(st, "P582")

            # V4 explicitly permits separate Wikidata relationship statements to
            # establish repeated starts only when both start and end intervals are
            # explicit and ordered without overlap. P580-only statements are kept
            # as provenance but do not establish a repeated episode here.
            ordered_episode = bool(
                start.get("usable") and end.get("usable") and
                start["interval_end"] < end["interval_start"]
            )
            if ordered_episode:
                explicit_episode_starts.append({
                    "source": "H4_wikidata_exact_pair_statement",
                    "source_qid": row["source_qid"],
                    "other_qid": row["other_qid"],
                    "direction": row["direction"],
                    "relationship_property": row["property"],
                    "statement_index": row["statement_index"],
                    "start": start,
                    "end": end,
                })
                counts["ordered_explicit_start_end_statements"] += 1

            cause_info = []
            for q in row["cause_qids"]:
                label = cause_labels.get(q)
                nlab = wd.norm_label(label)
                info = {
                    "qid": q,
                    "english_label": label,
                    "normalized_label": nlab,
                    "matches_nonfatal_family": bool(wd.NONFATAL_RE.search(nlab)),
                    "matches_fatal_conflict_family": bool(wd.FATAL_RE.search(nlab)),
                }
                cause_info.append(info)
                cause_label_counts[label or f"UNRESOLVED:{q}"] += 1

            any_nonfatal = any(x["matches_nonfatal_family"] for x in cause_info)
            any_fatal = any(x["matches_fatal_conflict_family"] for x in cause_info)
            cause_conflict = any_nonfatal and any_fatal
            item = {
                "source": "H4_wikidata_exact_pair_statement",
                "source_qid": row["source_qid"],
                "other_qid": row["other_qid"],
                "direction": row["direction"],
                "relationship_property": row["property"],
                "statement_index": row["statement_index"],
                "statement_rank": st.get("rank"),
                "start_time": start,
                "end_time": end,
                "end_causes": cause_info,
                "cause_conflict": cause_conflict,
            }
            if end.get("usable"):
                item.update({
                    "precision": end["precision"],
                    "interval_start": end["interval_start"],
                    "interval_end": end["interval_end"],
                })

            if end.get("usable") and any(overlap(end, b) for b in baseline):
                item["status"] = "corroborates_H1_H2_H3"
                corroborating.append(item)
                counts["corroborating_statement_evidence"] += 1
                continue

            qualifies = bool(
                end.get("usable") and row["cause_qids"] and
                any_nonfatal and not any_fatal and not cause_conflict
            )
            if qualifies:
                item["status"] = "new_H4_nonfatal_exit"
                accepted.append(item)
                counts["new_qualifying_statement_evidence"] += 1
            else:
                if not end.get("usable"):
                    reason = end.get("reason")
                elif not row["cause_qids"]:
                    reason = "no_P1534_end_cause"
                elif cause_conflict or any_fatal:
                    reason = "fatal_nonfatal_cause_conflict_or_fatal_cause"
                elif not any_nonfatal:
                    reason = "P1534_label_not_in_frozen_nonfatal_families"
                else:
                    reason = "does_not_qualify"
                item["status"] = "nonqualifying"
                item["nonqualification_reason"] = reason
                nonqualifying.append(item)
                counts[f"nonqualifying_{reason}"] += 1

        clean = baseline + [
            {
                "source": "H4_wikidata_exact_pair_statement",
                "event_kind": "wikidata_nonfatal_exit",
                "interval_start": x["interval_start"],
                "interval_end": x["interval_end"],
                "precision": x["precision"],
                "statement_identity": {
                    "source_qid": x["source_qid"],
                    "other_qid": x["other_qid"],
                    "relationship_property": x["relationship_property"],
                    "statement_index": x["statement_index"],
                },
            }
            for x in accepted
        ]

        if clean:
            endpoint_all += 1
            if model_ok:
                endpoint_model += 1
        if accepted and not had_baseline:
            new_pair_all += 1
            if model_ok:
                new_pair_model += 1

        # Strict reunion sequences can arise from a later accepted H1 formation,
        # or from a later ordered H4 relationship statement with explicit P580/P582.
        reunions = []
        seen_reunion = set()
        for ex in clean:
            for f in h1_formations:
                if f["interval_start"] > ex["interval_end"]:
                    key = (ex["interval_start"], ex["interval_end"], f["interval_start"], f["interval_end"], "H1")
                    if key not in seen_reunion:
                        seen_reunion.add(key)
                        reunions.append({
                            "exit": ex,
                            "later_formation": {
                                "source": "H1_adb_structured_event",
                                "event_kind": f["event_kind"],
                                "interval_start": f["interval_start"],
                                "interval_end": f["interval_end"],
                                "precision": f["precision"],
                            },
                        })
            for ep in explicit_episode_starts:
                st = ep["start"]
                if st["interval_start"] > ex["interval_end"]:
                    key = (ex["interval_start"], ex["interval_end"], st["interval_start"], st["interval_end"], "H4")
                    if key not in seen_reunion:
                        seen_reunion.add(key)
                        reunions.append({
                            "exit": ex,
                            "later_formation": {
                                "source": "H4_wikidata_explicit_repeated_start",
                                "event_kind": "relationship_start",
                                "interval_start": st["interval_start"],
                                "interval_end": st["interval_end"],
                                "precision": st["precision"],
                                "statement": ep,
                            },
                        })

        has_h4_repeated_start_reunion = any(
            x["later_formation"]["source"] == "H4_wikidata_explicit_repeated_start"
            for x in reunions
        )
        if reunions:
            reunion_all += 1
            if model_ok:
                reunion_model += 1
        if has_h4_repeated_start_reunion:
            repeated_start_reunion_all += 1
            if model_ok:
                repeated_start_reunion_model += 1

        pair_rows.append({
            "pair_key": pk,
            "model_eligible_birth_and_swieph_after_duplicate_guard": model_ok,
            "exact_wikidata_relationship_statement_count": len(exact_statements.get(pk, [])),
            "H4_ordered_explicit_relationship_episodes": explicit_episode_starts,
            "H4_new_nonfatal_endpoints": accepted,
            "H4_corroborating_endpoints": corroborating,
            "H4_nonqualifying_statements": nonqualifying,
            "clean_nonfatal_exits_through_H4": clean,
            "strict_reunion_sequences_through_H4": reunions,
        })

    out = {
        "status": "development_broad_pair_history_H4_source_ladder_complete",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "wikidata_parser_freeze": str(WD_FREEZE.relative_to(REPO)),
        "wikidata_parser_freeze_sha256": sha256(WD_FREEZE),
        "universe_artifact": str(UNIVERSE.relative_to(REPO)),
        "universe_sha256": sha256(UNIVERSE),
        "H1_H2_artifact": str(H12.relative_to(REPO)),
        "H1_H2_sha256": sha256(H12),
        "H3_artifact": str(H3.relative_to(REPO)),
        "H3_sha256": sha256(H3),
        "pair_universe": len(universe["pairs"]),
        "linked_wikidata_qids": len(qids),
        "resolved_claim_entities": sum(1 for q in qids if q in entities and "missing" not in (entities.get(q) or {})),
        "exact_pair_P26_P451_statements": exact_statement_count,
        "P1534_cause_qids": sorted(cause_qids),
        "P1534_english_labels": cause_labels,
        "P1534_label_occurrences_on_exact_pair_statements": dict(sorted(cause_label_counts.items())),
        "H4_counts": dict(sorted(counts.items())),
        "final_state_history_counts": {
            "all_exact_pairs_with_usable_nonfatal_exit": endpoint_all,
            "model_eligible_pairs_with_usable_nonfatal_exit": endpoint_model,
            "pairs_newly_gaining_endpoint_from_H4_all": new_pair_all,
            "pairs_newly_gaining_endpoint_from_H4_model_eligible": new_pair_model,
            "all_exact_pairs_with_strict_exit_then_later_same_partner_formation": reunion_all,
            "model_eligible_pairs_with_strict_exit_then_later_same_partner_formation": reunion_model,
            "all_pairs_with_reunion_supported_by_H4_repeated_start": repeated_start_reunion_all,
            "model_eligible_pairs_with_reunion_supported_by_H4_repeated_start": repeated_start_reunion_model,
        },
        "frozen_gate_result": {
            "dissolution_nonfatal_exit_gate_min_pairs": 50,
            "dissolution_gate_passed_all_exact": endpoint_all >= 50,
            "dissolution_gate_passed_model_eligible": endpoint_model >= 50,
            "same_partner_reunion_gate_min_pairs": 30,
            "reunion_gate_passed_all_exact": reunion_all >= 30,
            "reunion_gate_passed_model_eligible": reunion_model >= 30,
            "source_hierarchy_complete": True,
        },
        "pairs": pair_rows,
        "limitations": [
            "ADB/public linked-source development data only; not independent validation.",
            "Only exact QIDs inherited from H3 are used; no Wikidata search occurs.",
            "Only P26/P451 exact opposite-partner statements and P580/P582/P1534 qualifiers are inspected.",
            "A new H4 nonfatal exit requires usable P582 plus a P1534 English label in the frozen nonfatal lexical families.",
            "End times without qualifying end cause do not create new endpoint-bearing pairs.",
            "A Wikidata repeated-start reunion requires a separate exact-pair statement with usable ordered P580 and P582; P580-only statements are not enough.",
            "No astrology or Human Design features are calculated or inspected.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
