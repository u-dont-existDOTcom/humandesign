#!/usr/bin/env python3
"""V3 source ladder Rung 3: exact linked-Wikidata spouse/partner qualifiers.

Frozen specs:
  reference/research/adb_exact_pair_state_history_source_ladder_freeze_v3.md
  reference/research/adb_exact_pair_state_history_source_ladder_v3_rung3_parser_freeze.md

No astrology or Human Design features are calculated or inspected.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LADDER_FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_freeze_v3.md"
PARSER_FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung3_parser_freeze.md"
V1 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v1.json"
V2 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v2.json"
R2 = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung2.json"
OUT = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung3.json"
API = "https://www.wikidata.org/w/api.php"
UA = "humandesign-state-history-v3-rung3/1.0"
REL_PROPS = ("P26", "P451")
NONFATAL_RE = re.compile(r"divorc|separat|annul|split|break\s*[- ]?\s*up|breakup|dissolv|estrang", re.I)
FATAL_RE = re.compile(r"death|deceas|widow|killed|murder", re.I)
GREGORIAN_QID = "Q1985727"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def api_json(params: dict, attempts: int = 5) -> dict | None:
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception as exc:
            print("wikidata api failure", type(exc).__name__, "attempt", attempt + 1, flush=True)
            time.sleep(2.0 * (attempt + 1))
    return None


def fetch_entities(qids: list[str], props: str) -> dict[str, dict]:
    unique = []
    seen = set()
    for q in qids:
        if q and q not in seen:
            seen.add(q); unique.append(q)
    out: dict[str, dict] = {}
    batch_size = 25
    for i in range(0, len(unique), batch_size):
        batch = unique[i:i + batch_size]
        print(f"wikidata {props} batch {i // batch_size + 1}/{(len(unique) + batch_size - 1) // batch_size} n={len(batch)}", flush=True)
        data = api_json({
            "action": "wbgetentities",
            "ids": "|".join(batch),
            "props": props,
            "languages": "en",
            "format": "json",
        })
        if not data:
            if len(batch) == 1:
                out[batch[0]] = {"id": batch[0], "missing": ""}
            else:
                # Transport fallback only: exact QIDs are split into smaller requests;
                # no identity search or evidence-rule change occurs.
                for q in batch:
                    one = api_json({
                        "action": "wbgetentities", "ids": q, "props": props,
                        "languages": "en", "format": "json",
                    })
                    out[q] = ((one or {}).get("entities") or {}).get(q, {"id": q, "missing": ""})
            continue
        out.update(data.get("entities", {}))
        time.sleep(0.5)
    return out


def entity_value_id(snak: dict) -> str | None:
    if (snak or {}).get("snaktype") != "value":
        return None
    dv = (snak or {}).get("datavalue") or {}
    if dv.get("type") != "wikibase-entityid":
        return None
    v = dv.get("value") or {}
    return v.get("id")


def qualifier_entity_ids(statement: dict, prop: str) -> list[str]:
    out = []
    for snak in ((statement.get("qualifiers") or {}).get(prop) or []):
        q = entity_value_id(snak)
        if q:
            out.append(q)
    return out


def norm_label(s: str | None) -> str:
    x = unicodedata.normalize("NFKD", (s or "").casefold())
    x = "".join(c for c in x if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", x).strip()


def last_day(y: int, m: int) -> int:
    if m == 12:
        return (date(y + 1, 1, 1) - date.resolution).day
    return (date(y, m + 1, 1) - date.resolution).day


def iso(y: int, m: int, d: int) -> str:
    return date(y, m, d).isoformat()


def parse_wikidata_time_snak(snak: dict) -> dict:
    dv = (snak or {}).get("datavalue") or {}
    if (snak or {}).get("snaktype") != "value" or dv.get("type") != "time":
        return {"usable": False, "reason": "not_time_value", "raw": snak}
    v = dv.get("value") or {}
    raw_time = v.get("time")
    precision = int(v.get("precision", 0) or 0)
    before = int(v.get("before", 0) or 0)
    after = int(v.get("after", 0) or 0)
    calendar = v.get("calendarmodel")
    cal_qid = (calendar or "").rsplit("/", 1)[-1] if calendar else None
    m = re.fullmatch(r"([+-])(\d+)-(\d{2})-(\d{2})T.*", raw_time or "")
    base = {
        "raw_time": raw_time,
        "precision_value": precision,
        "before": before,
        "after": after,
        "calendar_model": calendar,
        "calendar_qid": cal_qid,
        "raw": snak,
    }
    if not m or m.group(1) == "-":
        return {**base, "usable": False, "reason": "unparseable_or_bce"}
    y, mo, d = int(m.group(2)), int(m.group(3)), int(m.group(4))
    if precision < 9:
        return {**base, "usable": False, "reason": "precision_below_year"}
    if before or after:
        return {**base, "usable": False, "reason": "before_after_uncertainty"}
    if precision >= 11:
        if cal_qid != GREGORIAN_QID:
            return {**base, "usable": False, "reason": "non_gregorian_day_precision"}
        try:
            lo = hi = iso(y, mo, d)
        except ValueError:
            return {**base, "usable": False, "reason": "invalid_day"}
        p = "day"
    elif precision == 10:
        if cal_qid != GREGORIAN_QID:
            return {**base, "usable": False, "reason": "non_gregorian_month_precision"}
        try:
            lo, hi = iso(y, mo, 1), iso(y, mo, last_day(y, mo))
        except ValueError:
            return {**base, "usable": False, "reason": "invalid_month"}
        p = "month"
    else:
        # Per frozen rule, year precision is usable regardless of calendar model.
        try:
            lo, hi = iso(y, 1, 1), iso(y, 12, 31)
        except ValueError:
            return {**base, "usable": False, "reason": "invalid_year"}
        p = "year"
    return {**base, "usable": True, "precision": p, "interval_start": lo, "interval_end": hi}


def merge_end_times(snaks: list[dict]) -> dict:
    parsed = [parse_wikidata_time_snak(x) for x in snaks]
    usable = [x for x in parsed if x.get("usable")]
    if not usable:
        return {"usable": False, "reason": "no_usable_end_time", "values": parsed}
    lo = max(x["interval_start"] for x in usable)
    hi = min(x["interval_end"] for x in usable)
    if lo > hi:
        return {"usable": False, "reason": "nonoverlapping_end_times", "values": parsed}
    # Use the narrowest resulting interval; precision label is descriptive only.
    precision = "day" if lo == hi else "month" if lo[:7] == hi[:7] else "year"
    return {"usable": True, "precision": precision, "interval_start": lo, "interval_end": hi, "values": parsed}


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def main() -> None:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    r2 = json.loads(R2.read_text(encoding="utf-8"))
    v1_by = {x["pair_key"]: x for x in v1["pairs"]}
    v2_by = {x["pair_key"]: x for x in v2["pairs"]}

    # Exact linked QIDs come only from completed Rung 2 identities.
    qids = sorted({
        q
        for p in r2["pairs"]
        for ident in (p.get("wikipedia_identity_a") or {}, p.get("wikipedia_identity_b") or {})
        for q in [ident.get("wikidata_qid")]
        if q
    })
    entities = fetch_entities(qids, "claims")

    # Collect only P1534 cause-QIDs appearing on exact pair relationship statements.
    exact_statements: dict[str, list[dict]] = {}
    cause_qids = set()
    exact_statement_count = 0
    for p in r2["pairs"]:
        pk = p["pair_key"]
        qa = (p.get("wikipedia_identity_a") or {}).get("wikidata_qid")
        qb = (p.get("wikipedia_identity_b") or {}).get("wikidata_qid")
        rows = []
        if qa and qb:
            for src_q, other_q, direction in ((qa, qb, "a_to_b"), (qb, qa, "b_to_a")):
                ent = entities.get(src_q) or {}
                claims = ent.get("claims") or {}
                for prop in REL_PROPS:
                    for st in claims.get(prop, []) or []:
                        if st.get("rank") == "deprecated":
                            continue
                        if entity_value_id(st.get("mainsnak") or {}) != other_q:
                            continue
                        exact_statement_count += 1
                        cause_ids = qualifier_entity_ids(st, "P1534")
                        cause_qids.update(cause_ids)
                        rows.append({"source_qid": src_q, "other_qid": other_q, "direction": direction, "property": prop, "statement": st, "cause_qids": cause_ids})
        exact_statements[pk] = rows

    cause_entities = fetch_entities(sorted(cause_qids), "labels") if cause_qids else {}
    cause_labels = {}
    for q in sorted(cause_qids):
        ent = cause_entities.get(q) or {}
        label = ((ent.get("labels") or {}).get("en") or {}).get("value")
        cause_labels[q] = label

    counts = Counter()
    pair_results = []
    total_endpoint_pairs = 0
    newly_endpoint_pairs = 0
    cause_label_counts = Counter()

    for r2p in r2["pairs"]:
        pk = r2p["pair_key"]
        v1p = v1_by[pk]
        v2p = v2_by[pk]
        v1_exits = [x for x in v1p.get("merged_transitions", []) if x.get("transition") == "dissolution"]
        v2_exits = v2p.get("new_v2_nonfatal_exits", [])
        r2_exits = r2p.get("new_rung2_exits", [])
        baseline = (
            [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v1"} for x in v1_exits]
            + [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v2"} for x in v2_exits]
            + [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "rung2"} for x in r2_exits]
        )
        had_baseline = bool(baseline) or bool(v1p.get("reunion_sequence_count"))

        accepted = []
        corroborating = []
        nonqualifying = []
        for row in exact_statements.get(pk, []):
            st = row["statement"]
            end = merge_end_times(((st.get("qualifiers") or {}).get("P582") or []))
            cause_info = []
            for q in row["cause_qids"]:
                lab = cause_labels.get(q)
                nlab = norm_label(lab)
                info = {
                    "qid": q,
                    "english_label": lab,
                    "normalized_label": nlab,
                    "matches_nonfatal_family": bool(NONFATAL_RE.search(nlab)),
                    "matches_fatal_conflict_family": bool(FATAL_RE.search(nlab)),
                }
                cause_info.append(info)
                cause_label_counts[lab or f"UNRESOLVED:{q}"] += 1

            any_nonfatal = any(x["matches_nonfatal_family"] for x in cause_info)
            any_fatal = any(x["matches_fatal_conflict_family"] for x in cause_info)
            cause_conflict = any_nonfatal and any_fatal
            exact = {
                "source_qid": row["source_qid"],
                "other_qid": row["other_qid"],
                "direction": row["direction"],
                "relationship_property": row["property"],
                "statement_rank": st.get("rank"),
                "end_time": end,
                "end_causes": cause_info,
                "cause_conflict": cause_conflict,
            }
            if end.get("usable"):
                exact.update({
                    "precision": end["precision"],
                    "interval_start": end["interval_start"],
                    "interval_end": end["interval_end"],
                })

            overlaps_baseline = bool(end.get("usable") and any(overlap(end, b) for b in baseline))
            if overlaps_baseline:
                exact["status"] = "corroborates_higher_precedence_endpoint"
                corroborating.append(exact)
                counts["corroborating_statement_evidence"] += 1
                continue

            qualifies = bool(end.get("usable") and row["cause_qids"] and any_nonfatal and not any_fatal and not cause_conflict)
            if qualifies:
                exact["status"] = "new_rung3_nonfatal_endpoint"
                accepted.append(exact)
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
                exact["status"] = "nonqualifying"
                exact["nonqualification_reason"] = reason
                nonqualifying.append(exact)
                counts[f"nonqualifying_{reason}"] += 1

        has_endpoint = had_baseline or bool(accepted)
        if has_endpoint:
            total_endpoint_pairs += 1
        if accepted and not had_baseline:
            newly_endpoint_pairs += 1

        pair_results.append({
            "pair_key": pk,
            "had_clean_through_rung2_endpoint": had_baseline,
            "exact_wikidata_relationship_statement_count": len(exact_statements.get(pk, [])),
            "new_rung3_nonfatal_endpoints": accepted,
            "corroborating_wikidata_endpoints": corroborating,
            "nonqualifying_wikidata_statements": nonqualifying,
        })

    out = {
        "status": "development_state_history_source_ladder_rung3",
        "ladder_freeze": str(LADDER_FREEZE.relative_to(REPO)),
        "ladder_freeze_sha256": sha256(LADDER_FREEZE),
        "parser_freeze": str(PARSER_FREEZE.relative_to(REPO)),
        "parser_freeze_sha256": sha256(PARSER_FREEZE),
        "v1_sha256": sha256(V1),
        "v2_sha256": sha256(V2),
        "rung2_sha256": sha256(R2),
        "pair_universe": len(r2["pairs"]),
        "linked_wikidata_qids": len(qids),
        "resolved_claim_entities": sum(1 for q in qids if q in entities and "missing" not in (entities.get(q) or {})),
        "exact_pair_P26_P451_statements": exact_statement_count,
        "P1534_cause_qids": sorted(cause_qids),
        "P1534_english_labels": cause_labels,
        "P1534_label_occurrences_on_exact_pair_statements": dict(cause_label_counts),
        "rung3_counts": dict(counts),
        "endpoint_counts": {
            "clean_rung2_baseline_endpoint_pairs": int(r2["stop_go"]["endpoint_pairs_observed"]),
            "pairs_newly_gaining_endpoint_from_rung3": newly_endpoint_pairs,
            "total_clean_endpoint_pairs_after_rung3": total_endpoint_pairs,
        },
        "stop_go": {
            "minimum_endpoint_pairs": 30,
            "endpoint_pairs_observed": total_endpoint_pairs,
            "source_ladder_exhausted": True,
            "sufficiency_gate_passed": total_endpoint_pairs >= 30,
            "next_action": "freeze_separate_semimarkov_model_spec" if total_endpoint_pairs >= 30 else "declare_public_source_universe_insufficient_do_not_fit",
        },
        "pairs": pair_results,
        "limitations": [
            "Only exact Wikidata QIDs inherited from the frozen ADB->English-Wikipedia identity chain are used; no Wikidata search occurs.",
            "Only P26/P451 exact opposite-partner statements and P580/P582/P1534 qualifiers are inspected.",
            "A new nonfatal endpoint requires a usable P582 plus an exact P1534 English label in the frozen nonfatal lexical families.",
            "End times without qualifying end cause do not create new endpoint-bearing pairs.",
            "No astrology or Human Design features are calculated or inspected.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
