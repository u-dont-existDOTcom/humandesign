#!/usr/bin/env python3
"""V4 broad exact-pair history H3: ADB-linked English-Wikipedia lead infobox.

Frozen source/evidence rules come from:
  reference/research/adb_broad_exact_pair_universe_freeze_v4.md
and reuse the audited V3 Rung-2 parser behavior.

No astrology or Human Design features are calculated or inspected.
"""
from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from pathlib import Path

import adb_broad_exact_pair_universe_v4 as uni
import adb_exact_pair_state_history_source_ladder_v3_rung2 as wp
import adb_exact_pair_state_history_source_ladder_v3_rung2_batch_runner as batch

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_freeze_v4.md"
UNIVERSE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
H12 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h1_h2.json"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h3.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def fetch_adb_pages(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]]:
    """Exact DatamainID page resolution; transport only, no outcome inspection."""
    resolved = {}
    failures = []
    titles = sorted({p.get("public_title") or p.get("name") for p in people.values() if p.get("public_title") or p.get("name")})
    for title, wt in uni.fetch_wikitext_batch(titles):
        eid = uni.exact_id(wt)
        if eid in people and eid not in resolved:
            resolved[eid] = (title, wt)
    unresolved = [aid for aid in sorted(people) if aid not in resolved]
    for i, aid in enumerate(unresolved, 1):
        p = people[aid]
        for title, wt in uni.fetch_wikitext_batch(uni.search_titles(p.get("name") or p.get("public_title") or "")):
            if uni.exact_id(wt) == aid:
                resolved[aid] = (title, wt)
                break
        if aid not in resolved:
            failures.append({"adb_id": aid, "stage": "adb_exact_identity", "name": p.get("name")})
        if i % 25 == 0:
            print(f"H3 ADB fallback {i}/{len(unresolved)}", flush=True)
    return resolved, failures


def main() -> None:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    h12 = json.loads(H12.read_text(encoding="utf-8"))
    h12_by_pair = {x["pair_key"]: x for x in h12["pairs"]}
    u_by_pair = {x["pair_key"]: x for x in universe["pairs"]}

    people = {}
    for p in universe["pairs"]:
        for side in ("person_a", "person_b"):
            x = p[side]
            people[int(x["adb_id"])] = x

    adb_pages, failures = fetch_adb_pages(people)
    print(f"H3 exact ADB pages {len(adb_pages)}/{len(people)}", flush=True)

    # Extract only explicit ADB interwiki links; no Wikipedia name search.
    linked = {}
    link_counts = Counter()
    for aid, p in people.items():
        if aid not in adb_pages:
            linked[aid] = None
            continue
        title = wp.adb_wikipedia_title(adb_pages[aid][1])
        linked[aid] = title
        link_counts["with_adb_wikipedia_link" if title else "no_adb_wikipedia_link"] += 1

    # Batched Wikipedia transport, exact ADB-linked titles only.
    unique_linked = []
    seen = set()
    for t in linked.values():
        k = wp.norm(t) if t else ""
        if k and k not in seen:
            seen.add(k); unique_linked.append(t)
    wiki_cache = {}
    batch_size = 8
    for i in range(0, len(unique_linked), batch_size):
        chunk = unique_linked[i:i + batch_size]
        wiki_cache.update(batch.resolve_batch(chunk))
        if (i // batch_size + 1) % 10 == 0:
            print(f"H3 enwiki batches {i // batch_size + 1}/{(len(unique_linked)+batch_size-1)//batch_size}", flush=True)
        time.sleep(0.35)

    wiki = {}
    for aid in sorted(people):
        t = linked.get(aid)
        if not t:
            wiki[aid] = {"adb_linked_wikipedia_title": None, "canonical_wikipedia_title": None, "wikidata_qid": None, "infobox_fields": {}}
            continue
        canonical, enwt, qid = wiki_cache.get(wp.norm(t), (None, None, None))
        if not canonical or not enwt:
            failures.append({"adb_id": aid, "stage": "wikipedia_fetch", "adb_linked_title": t})
            wiki[aid] = {"adb_linked_wikipedia_title": t, "canonical_wikipedia_title": None, "wikidata_qid": None, "infobox_fields": {}}
            link_counts["linked_but_unresolved"] += 1
            continue
        ib = wp.first_infobox(enwt)
        fields = wp.top_fields(ib) if ib else {}
        rel_fields = {k: v for k, v in fields.items() if k in {"spouse", "spouses", "partner", "partners"}}
        wiki[aid] = {
            "adb_linked_wikipedia_title": t,
            "canonical_wikipedia_title": canonical,
            "wikidata_qid": qid,
            "infobox_fields": rel_fields,
        }
        link_counts["resolved_wikipedia"] += 1
        if rel_fields:
            link_counts["with_relationship_infobox_field"] += 1

    evidence_counts = Counter()
    endpoint_pairs_all = 0
    endpoint_pairs_model = 0
    new_endpoint_pairs_all = 0
    new_endpoint_pairs_model = 0
    reunion_pairs_all = 0
    reunion_pairs_model = 0
    qid_same_identity_duplicate_flags = 0
    pair_rows = []

    for p in universe["pairs"]:
        pk = p["pair_key"]
        h = h12_by_pair[pk]
        a = int(p["person_a"]["adb_id"]); b = int(p["person_b"]["adb_id"])
        baseline = list(h.get("clean_nonfatal_exits_through_H2", []))
        formations = [x for x in h.get("H1_merged_transitions", []) if x.get("transition") == "formation"]
        had_baseline = bool(baseline)
        model_ok = bool(u_by_pair[pk].get("model_eligible_birth_and_swieph"))

        # Identity-level duplicate safeguard enhancement from frozen V4 rule.
        qa = wiki.get(a, {}).get("wikidata_qid"); qb = wiki.get(b, {}).get("wikidata_qid")
        same_linked_identity = bool(qa and qb and qa == qb)
        duplicate_identity_flag = False
        if same_linked_identity:
            pa, pb = p["person_a"], p["person_b"]
            if (pa.get("birth_date") and pa.get("birth_date") == pb.get("birth_date") and
                abs(float(pa["jd_ut"]) - float(pb["jd_ut"])) * 86400 <= 60 and
                None not in (pa.get("lat"), pa.get("lon"), pb.get("lat"), pb.get("lon")) and
                abs(pa["lat"] - pb["lat"]) <= 0.01 and abs(pa["lon"] - pb["lon"]) <= 0.01):
                duplicate_identity_flag = True
                qid_same_identity_duplicate_flags += 1
                model_ok = False

        evidence = []
        for src, other in ((a, b), (b, a)):
            sw = wiki.get(src) or {}
            ow = wiki.get(other) or {}
            other_title = ow.get("canonical_wikipedia_title")
            other_name = people[other].get("name") or people[other].get("public_title") or ""
            for field_name, field_value in (sw.get("infobox_fields") or {}).items():
                templates = wp.extract_marriage_templates(field_value)
                for t in templates:
                    ev = wp.parse_template_endpoint(t, other_title, other_name)
                    if ev:
                        ev.update({
                            "source": "H3_wikipedia_infobox",
                            "source_adb_id": src,
                            "source_wikipedia_title": sw.get("canonical_wikipedia_title"),
                            "other_adb_id": other,
                            "infobox_field": field_name,
                        })
                        evidence.append(ev)
                for frag in wp.plain_fragments(field_value, templates):
                    ev = wp.parse_plain_endpoint(frag, other_title, other_name)
                    if ev:
                        ev.update({
                            "source": "H3_wikipedia_infobox",
                            "source_adb_id": src,
                            "source_wikipedia_title": sw.get("canonical_wikipedia_title"),
                            "other_adb_id": other,
                            "infobox_field": field_name,
                        })
                        evidence.append(ev)

        dedup = []
        seen_ev = set()
        for x in evidence:
            key = (x["source_adb_id"], x["other_adb_id"], x["interval_start"], x["interval_end"], x["evidence_type"], x.get("template") or x.get("fragment"))
            if key not in seen_ev:
                seen_ev.add(key); dedup.append(x)
        evidence = dedup

        corroborating = []
        new = []
        for x in evidence:
            if any(overlap(x, y) for y in baseline):
                y = dict(x); y["status"] = "corroborates_H1_H2"; corroborating.append(y)
            else:
                y = dict(x); y["status"] = "new_H3_nonfatal_exit"; new.append(y)
        evidence_counts["accepted_H3_exit_evidence"] += len(evidence)
        evidence_counts["corroborating_H1_H2"] += len(corroborating)
        evidence_counts["new_H3_exit_evidence"] += len(new)

        clean = baseline + [
            {"source": "H3_wikipedia_infobox", "event_kind": "wikipedia_nonfatal_exit",
             "interval_start": x["interval_start"], "interval_end": x["interval_end"], "precision": x["precision"]}
            for x in new
        ]
        if clean:
            endpoint_pairs_all += 1
            if model_ok: endpoint_pairs_model += 1
        if new and not had_baseline:
            new_endpoint_pairs_all += 1
            if model_ok: new_endpoint_pairs_model += 1

        reunions = []
        for ex in clean:
            for f in formations:
                if f["interval_start"] > ex["interval_end"]:
                    reunions.append({
                        "exit": ex,
                        "later_formation": {
                            "source": "H1_adb_structured_event", "event_kind": f["event_kind"],
                            "interval_start": f["interval_start"], "interval_end": f["interval_end"], "precision": f["precision"],
                        },
                    })
        if reunions:
            reunion_pairs_all += 1
            if model_ok: reunion_pairs_model += 1

        pair_rows.append({
            "pair_key": pk,
            "model_eligible_birth_and_swieph_after_H3_duplicate_guard": model_ok,
            "H3_same_linked_identity_duplicate_exclusion": duplicate_identity_flag,
            "wikipedia_identity_a": {k: wiki.get(a, {}).get(k) for k in ("adb_linked_wikipedia_title", "canonical_wikipedia_title", "wikidata_qid")},
            "wikipedia_identity_b": {k: wiki.get(b, {}).get(k) for k in ("adb_linked_wikipedia_title", "canonical_wikipedia_title", "wikidata_qid")},
            "H3_accepted_wikipedia_exits": evidence,
            "H3_corroborating_exits": corroborating,
            "H3_new_nonfatal_exits": new,
            "clean_nonfatal_exits_through_H3": clean,
            "strict_reunion_sequences_through_H3": reunions,
        })

    out = {
        "status": "development_broad_pair_history_H3",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "universe_artifact": str(UNIVERSE.relative_to(REPO)),
        "universe_sha256": sha256(UNIVERSE),
        "H1_H2_artifact": str(H12.relative_to(REPO)),
        "H1_H2_sha256": sha256(H12),
        "pair_universe": len(universe["pairs"]),
        "people": len(people),
        "identity_counts": dict(sorted(link_counts.items())),
        "source_failures": failures,
        "H3_counts": dict(sorted(evidence_counts.items())),
        "duplicate_guard": {"same_linked_identity_duplicate_exclusions": qid_same_identity_duplicate_flags},
        "state_history_counts_through_H3": {
            "all_exact_pairs_with_usable_nonfatal_exit": endpoint_pairs_all,
            "model_eligible_pairs_with_usable_nonfatal_exit": endpoint_pairs_model,
            "pairs_newly_gaining_endpoint_from_H3_all": new_endpoint_pairs_all,
            "pairs_newly_gaining_endpoint_from_H3_model_eligible": new_endpoint_pairs_model,
            "all_exact_pairs_with_strict_exit_then_later_same_partner_H1_formation": reunion_pairs_all,
            "model_eligible_pairs_with_strict_exit_then_later_same_partner_H1_formation": reunion_pairs_model,
        },
        "sufficiency_preview_not_model_authorization": {
            "dissolution_gate_50_model_eligible": endpoint_pairs_model >= 50,
            "reunion_gate_30_model_eligible": reunion_pairs_model >= 30,
            "note": "Frozen V4 requires H4 and a final source-only audit before any model specification is written.",
        },
        "pairs": pair_rows,
        "limitations": [
            "Development data only; not independent validation.",
            "Only explicit ADB-linked English-Wikipedia identities are used; no Wikipedia name search occurs.",
            "Only the lead infobox spouse/spouses/partner/partners fields are parsed under the already-audited V3 Rung-2 rules.",
            "Biography/article prose is excluded and bare end years without explicit nonfatal semantics do not count.",
            "H3 does not invent new formation dates; reunion inference uses only H1 structured later formations.",
            "No astrology or Human Design features are calculated or inspected.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
