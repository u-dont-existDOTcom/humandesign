#!/usr/bin/env python3
"""Source-only episode construction/readiness audit for frozen dissolution V1.

Spec:
  reference/research/adb_broad_exact_pair_dissolution_semimarkov_freeze_v1.md

This script constructs first-episode annual risk histories from already frozen
H1-H4 source evidence. It does not calculate astrology or Human Design features
and does not fit any outcome model.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

import adb_exact_pair_state_history_source_ladder_v3_rung2 as wp
import adb_exact_pair_state_history_source_ladder_v3_rung2_batch_runner as batch

REPO = Path(__file__).resolve().parents[1]
SPEC = REPO / "reference" / "research" / "adb_broad_exact_pair_dissolution_semimarkov_freeze_v1.md"
UNIVERSE = REPO / "reference" / "research" / "adb_broad_exact_pair_universe_v4.json"
H12 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h1_h2.json"
H3 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h3.json"
H4 = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_h4.json"
FINAL = REPO / "reference" / "research" / "adb_broad_exact_pair_history_v4_final_audit.json"
OUT = REPO / "reference" / "research" / "adb_broad_exact_pair_dissolution_episode_readiness_v1.json"
SNAPSHOT_DATE = "2026-08-26"
SNAPSHOT_YEAR = 2026
FATAL_RE = re.compile(r"\b(death|widow|widower|widowhood|died|deceased)\b", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def definitely_before(a: dict, b: dict) -> bool:
    return a["interval_end"] < b["interval_start"]


def year_of(s: str) -> int:
    return int(s[:4])


def parse_template_parts(template: str):
    parts = wp.split_template_params(template)
    named = {}
    positional = []
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            named[re.sub(r"[^a-z]", "", k.casefold())] = v.strip()
        else:
            positional.append(p.strip())
    return named, positional


def h3_current_marker(entry: str, is_template: bool, other_wiki: str | None, other_name: str):
    if not wp.partner_match(entry, other_wiki, other_name):
        return None
    p = wp.plain(entry)
    if wp.END_RE.search(p):
        return None
    if is_template:
        named, positional = parse_template_parts(entry)
        if any(wp.REASON_ONLY_RE.fullmatch(wp.plain(v)) for k, v in named.items() if k in {"end", "reason", "status"}):
            return None
        # Any parseable named end field makes this non-current regardless of reason.
        for key in ("enddate", "endyear", "todate", "to", "until", "ended", "end"):
            if key in named and wp.date_candidates(named[key]):
                return None
        dates = []
        for idx, val in enumerate(positional):
            ds = wp.date_candidates(val)
            if len(ds) > 1:
                return None
            if len(ds) == 1:
                dates.append((idx, ds[0]))
        # First positional field is partner; current marriage templates should have
        # exactly one dated positional field (the start). Two dates imply an end.
        if len(dates) != 1:
            return None
        start = dates[0][1]
        return {
            "source_family": "H3", "source": "H3_wikipedia_current_open",
            "start": {k: start[k] for k in ("precision", "interval_start", "interval_end", "text")},
            "raw": entry,
        }
    # Conservative plain-fragment current marker: exact partner, no end semantics,
    # exactly one explicit date in a spouse/partner infobox field.
    ds = wp.date_candidates(entry)
    if len(ds) != 1:
        return None
    start = ds[0]
    return {
        "source_family": "H3", "source": "H3_wikipedia_current_open_plain",
        "start": {k: start[k] for k in ("precision", "interval_start", "interval_end", "text")},
        "raw": entry,
    }


def fetch_h3_current_markers(universe: dict, h3: dict):
    people = {}
    for p in universe["pairs"]:
        for side in ("person_a", "person_b"):
            x = p[side]; people[int(x["adb_id"])] = x
    h3_by = {x["pair_key"]: x for x in h3["pairs"]}

    titles = []
    seen = set()
    for p in h3["pairs"]:
        for ident in (p.get("wikipedia_identity_a") or {}, p.get("wikipedia_identity_b") or {}):
            t = ident.get("canonical_wikipedia_title")
            k = wp.norm(t) if t else ""
            if k and k not in seen:
                seen.add(k); titles.append(t)
    cache = {}
    batch_size = 25
    for i in range(0, len(titles), batch_size):
        cache.update(batch.resolve_batch(titles[i:i + batch_size]))
        if (i // batch_size + 1) % 5 == 0:
            print(f"episode H3 current-marker batches {i//batch_size+1}/{(len(titles)+batch_size-1)//batch_size}", flush=True)
        time.sleep(0.35)

    by_pair = {}
    failures = []
    for up in universe["pairs"]:
        pk = up["pair_key"]; hp = h3_by[pk]
        a = int(up["person_a"]["adb_id"]); b = int(up["person_b"]["adb_id"])
        ia = hp.get("wikipedia_identity_a") or {}; ib = hp.get("wikipedia_identity_b") or {}
        entries = []
        for src, other, sident, oident, direction in (
            (a, b, ia, ib, "a_to_b"), (b, a, ib, ia, "b_to_a")
        ):
            st = sident.get("canonical_wikipedia_title")
            ot = oident.get("canonical_wikipedia_title")
            if not st or not ot:
                continue
            canonical, wt, _qid = cache.get(wp.norm(st), (None, None, None))
            if not canonical or not wt:
                failures.append({"pair_key": pk, "source_adb_id": src, "wikipedia_title": st})
                continue
            ibox = wp.first_infobox(wt); fields = wp.top_fields(ibox) if ibox else {}
            for field_name in ("spouse", "spouses", "partner", "partners"):
                field = fields.get(field_name)
                if not field: continue
                templates = wp.extract_marriage_templates(field)
                for t in templates:
                    marker = h3_current_marker(t, True, ot, people[other].get("name") or ot)
                    if marker:
                        marker.update({"direction": direction, "source_adb_id": src, "other_adb_id": other, "infobox_field": field_name, "source_wikipedia_title": canonical})
                        entries.append(marker)
                for frag in wp.plain_fragments(field, templates):
                    marker = h3_current_marker(frag, False, ot, people[other].get("name") or ot)
                    if marker:
                        marker.update({"direction": direction, "source_adb_id": src, "other_adb_id": other, "infobox_field": field_name, "source_wikipedia_title": canonical})
                        entries.append(marker)
        # Deduplicate same source/direction/start/raw.
        dedup=[]; keys=set()
        for x in entries:
            k=(x["source_family"],x["direction"],x["start"]["interval_start"],x["start"]["interval_end"],x["raw"])
            if k not in keys: keys.add(k); dedup.append(x)
        by_pair[pk]=dedup
    return by_pair, failures


def h4_all_statements(p4: dict):
    rows=[]
    for key in ("H4_new_nonfatal_endpoints", "H4_corroborating_endpoints", "H4_nonqualifying_statements"):
        rows.extend(p4.get(key, []) or [])
    # Dedup by exact statement identity where available.
    out=[]; seen=set()
    for x in rows:
        k=(x.get("source_qid"),x.get("other_qid"),x.get("relationship_property"),x.get("statement_index"),x.get("direction"))
        if k not in seen: seen.add(k); out.append(x)
    return out


def collect_entries(p12: dict, p4: dict):
    out=[]
    for f in p12.get("H1_merged_transitions", []) or []:
        if f.get("transition") != "formation": continue
        kind=f.get("event_kind")
        if kind not in {"begin","marriage"}: continue
        out.append({"source": f"H1_{kind}", "source_family":"H1", "kind":kind,
                    "precision":f["precision"],"interval_start":f["interval_start"],"interval_end":f["interval_end"]})
    for r in p12.get("H1_relationship_ranges", []) or []:
        out.append({"source":"H1_range_start","source_family":"H1","kind":"relationship_range",
                    "precision":"year","interval_start":r["interval_start"],
                    "interval_end":r.get("interval_start_latest") or r["interval_start"]})
    for st in h4_all_statements(p4):
        s=st.get("start_time") or {}
        if s.get("usable"):
            out.append({"source":"H4_P580","source_family":"H4","kind":"P580",
                        "precision":s["precision"],"interval_start":s["interval_start"],"interval_end":s["interval_end"],
                        "statement":{"source_qid":st.get("source_qid"),"other_qid":st.get("other_qid"),"direction":st.get("direction"),"property":st.get("relationship_property"),"statement_index":st.get("statement_index")}})
    # Dedup exact interval/source-kind candidates.
    dedup=[]; seen=set()
    for x in sorted(out,key=lambda z:(z["interval_start"],z["interval_end"],z["source"],z["kind"])):
        k=(x["source"],x["kind"],x["interval_start"],x["interval_end"])
        if k not in seen: seen.add(k); dedup.append(x)
    return dedup


def collect_h4_censors(p4: dict):
    out=[]
    for st in h4_all_statements(p4):
        e=st.get("end_time") or {}
        if not e.get("usable"): continue
        causes=st.get("end_causes") or []
        nonfatal=any(x.get("matches_nonfatal_family") for x in causes)
        fatal=any(x.get("matches_fatal_conflict_family") or FATAL_RE.search(x.get("english_label") or "") for x in causes)
        if nonfatal and not fatal:
            continue
        ctype="fatal_H4" if fatal else "unknown_cause_H4"
        out.append({"source":ctype,"source_family":"H4","censor_type":ctype,
                    "precision":e["precision"],"interval_start":e["interval_start"],"interval_end":e["interval_end"],
                    "statement":{"source_qid":st.get("source_qid"),"other_qid":st.get("other_qid"),"direction":st.get("direction"),"property":st.get("relationship_property"),"statement_index":st.get("statement_index")},
                    "end_causes":causes})
    return out


def collect_h4_current_markers(p4: dict):
    out=[]
    for st in h4_all_statements(p4):
        s=st.get("start_time") or {}; e=st.get("end_time") or {}
        # Current-open marker requires usable P580 and *absence* of P582 values,
        # not merely an unusably coarse/conflicted end.
        if s.get("usable") and not e.get("usable") and not (e.get("values") or []):
            out.append({"source_family":"H4","source":"H4_wikidata_current_open",
                        "direction":st.get("direction"),"start":{"precision":s["precision"],"interval_start":s["interval_start"],"interval_end":s["interval_end"]},
                        "statement":{"source_qid":st.get("source_qid"),"other_qid":st.get("other_qid"),"property":st.get("relationship_property"),"statement_index":st.get("statement_index")}})
    # dedup statement identities
    dedup=[]; seen=set()
    for x in out:
        st=x["statement"]; k=(x["source_family"],x["direction"],st.get("source_qid"),st.get("other_qid"),st.get("property"),st.get("statement_index"))
        if k not in seen: seen.add(k); dedup.append(x)
    return dedup


def strong_current_censor(h3markers: list[dict], h4markers: list[dict]):
    markers=h3markers+h4markers
    # At least two unique source-family/direction markers, thereby differing by
    # source family or subject direction as frozen.
    signatures={(x.get("source_family"),x.get("direction")) for x in markers}
    if len(signatures)<2:
        return None
    return {"source":"strong_current_open_2026","source_family":"H3_H4","censor_type":"right_current",
            "precision":"day","interval_start":SNAPSHOT_DATE,"interval_end":SNAPSHOT_DATE,
            "marker_signatures":[list(x) for x in sorted(signatures)],"markers":markers}


def choose_entry(entries: list[dict], exits: list[dict]):
    for e in sorted(entries,key=lambda x:(x["interval_start"],x["interval_end"],x["source"])):
        if any(definitely_before(x,e) for x in exits):
            continue
        return e
    return None


def earliest_after_entry(items: list[dict], entry: dict):
    valid=[x for x in items if not definitely_before(x,entry)]
    return min(valid,key=lambda x:(x["interval_start"],x["interval_end"],x.get("source",""))) if valid else None


def union_find_components(episodes: list[dict]):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb:
            if str(ra)<str(rb): parent[rb]=ra
            else: parent[ra]=rb
    for ep in episodes:
        a,b=ep["person_a_id"],ep["person_b_id"]
        union(a,b)
    comps=defaultdict(list)
    for ep in episodes:
        root=find(ep["person_a_id"]); comps[root].append(ep)
    return comps


def main():
    u=json.loads(UNIVERSE.read_text(encoding="utf-8")); h12=json.loads(H12.read_text(encoding="utf-8")); h3=json.loads(H3.read_text(encoding="utf-8")); h4=json.loads(H4.read_text(encoding="utf-8")); final=json.loads(FINAL.read_text(encoding="utf-8"))
    ub={x["pair_key"]:x for x in u["pairs"]}; b12={x["pair_key"]:x for x in h12["pairs"]}; b3={x["pair_key"]:x for x in h3["pairs"]}; b4={x["pair_key"]:x for x in h4["pairs"]}
    if not (set(ub)==set(b12)==set(b3)==set(b4)):
        raise RuntimeError("pair universes differ")

    h3current,h3fail=fetch_h3_current_markers(u,h3)
    episodes=[]; exclusions=[]; pair_rows=[]; counts=Counter()

    for pk in sorted(ub):
        up=ub[pk]; p12=b12[pk]; p4=b4[pk]
        model_ok=bool(p4.get("model_eligible_birth_and_swieph_after_duplicate_guard"))
        if not model_ok:
            exclusions.append({"pair_key":pk,"reason":"not_model_eligible_birth_swieph_duplicate_guard"}); counts["exclude_not_model_eligible"]+=1; continue
        exits=list(p4.get("clean_nonfatal_exits_through_H4",[]) or [])
        entries=collect_entries(p12,p4)
        entry=choose_entry(entries,exits)
        if not entry:
            exclusions.append({"pair_key":pk,"reason":"no_usable_first_episode_entry","entry_candidates":entries,"exits":exits}); counts["exclude_no_entry"]+=1; continue
        event=earliest_after_entry(exits,entry)

        censors=collect_h4_censors(p4)
        # H1 finite range ends not already represented by a clean nonfatal exit.
        for r in p12.get("H1_relationship_ranges",[]) or []:
            cand={"source":"H1_finite_range_generic_end","source_family":"H1","censor_type":"generic_range_end","precision":"year",
                  "interval_start":r.get("interval_end_earliest") or r["interval_end"],"interval_end":r["interval_end"],"relationship_range":r}
            if not any(overlap(cand,x) for x in exits): censors.append(cand)
        current=strong_current_censor(h3current.get(pk,[]),collect_h4_current_markers(p4))
        if current: censors.append(current)
        censor=earliest_after_entry(censors,entry)

        outcome=None; ambiguity=None
        if event and censor:
            if definitely_before(event,censor): outcome="event"
            elif definitely_before(censor,event): outcome="censor"
            else:
                # Fatal/current overlap is genuinely ambiguous. A lower-precedence
                # H4 unknown-cause end overlapping a clean higher-precedence event
                # is treated as the same transition with the clean nonfatal cause.
                if censor.get("censor_type")=="unknown_cause_H4" and event.get("source")!="H4_wikidata_exact_pair_statement": outcome="event"
                else: ambiguity="event_censor_intervals_overlap"
        elif event: outcome="event"
        elif censor: outcome="censor"
        else:
            exclusions.append({"pair_key":pk,"reason":"no_event_or_source_supported_censor","entry":entry}); counts["exclude_no_outcome_or_censor"]+=1; continue
        if ambiguity:
            exclusions.append({"pair_key":pk,"reason":ambiguity,"entry":entry,"event":event,"censor":censor}); counts["exclude_ambiguous_event_censor"]+=1; continue

        final_end=event if outcome=="event" else censor
        entry_year=year_of(entry["interval_start"]); end_year=year_of(final_end["interval_start"])
        if end_year<entry_year:
            exclusions.append({"pair_key":pk,"reason":"end_year_before_entry_year","entry":entry,"end":final_end}); counts["exclude_negative_duration"]+=1; continue
        if outcome=="censor" and end_year<=entry_year:
            exclusions.append({"pair_key":pk,"reason":"censor_not_after_entry_year","entry":entry,"censor":final_end}); counts["exclude_zero_followup_censor"]+=1; continue

        ids=sorted([int(up["person_a"]["adb_id"]),int(up["person_b"]["adb_id"])])
        relation_codes=sorted(set(up.get("relation_codes") or []))
        ep={"pair_key":pk,"person_a_id":ids[0],"person_b_id":ids[1],"entry":entry,"entry_year":entry_year,
            "outcome":outcome,"event":event if outcome=="event" else None,"censor":censor if outcome=="censor" else None,
            "end_year":end_year,"duration_years":end_year-entry_year,"relation_codes":relation_codes,
            "H3_current_markers":h3current.get(pk,[]),"H4_current_markers":collect_h4_current_markers(p4)}
        episodes.append(ep); counts[f"accepted_{outcome}_episodes"]+=1
        for year in range(entry_year,end_year+1):
            # Event occurs only in final event year. A censor year remains a
            # non-event risk row, as frozen in the annual discrete-time design.
            pass
        pair_rows.append({"pair_key":pk,"entry_candidates":entries,"selected_entry":entry,"all_clean_nonfatal_exits":exits,"candidate_censors":censors,"selected_outcome":outcome,"selected_event":ep["event"],"selected_censor":ep["censor"]})

    pair_year_rows=[]
    for ep in episodes:
        for y in range(ep["entry_year"],ep["end_year"]+1):
            pair_year_rows.append({"pair_key":ep["pair_key"],"person_a_id":ep["person_a_id"],"person_b_id":ep["person_b_id"],"calendar_year":y,
                                   "duration_since_entry_year":y-ep["entry_year"],"event":int(ep["outcome"]=="event" and y==ep["end_year"]),
                                   "final_row":int(y==ep["end_year"]),"final_row_type":ep["outcome"] if y==ep["end_year"] else None,
                                   "relation_codes":ep["relation_codes"],"entry_source":ep["entry"]["source"],"entry_precision":ep["entry"]["precision"]})

    comps=union_find_components(episodes)
    component_summary=[]; event_components=0
    for root,eps in sorted(comps.items(),key=lambda kv:str(kv[0])):
        ev=sum(e["outcome"]=="event" for e in eps); rows=sum(e["duration_years"]+1 for e in eps)
        if ev: event_components+=1
        component_summary.append({"root_person_id":root,"pairs":len(eps),"events":ev,"pair_year_rows":rows,"pair_keys":sorted(e["pair_key"] for e in eps)})

    event_pairs=sum(e["outcome"]=="event" for e in episodes); censored_pairs=sum(e["outcome"]=="censor" for e in episodes); nrows=len(pair_year_rows)
    gates={"event_pairs_ge_50":event_pairs>=50,"censored_non_event_pairs_ge_30":censored_pairs>=30,"pair_year_rows_ge_200":nrows>=200,"event_components_ge_5":event_components>=5}
    ready=all(gates.values())
    out={"status":"development_dissolution_episode_readiness_source_only","model_spec":str(SPEC.relative_to(REPO)),"model_spec_sha256":sha256(SPEC),
         "input_hashes":{"universe":sha256(UNIVERSE),"H1_H2":sha256(H12),"H3":sha256(H3),"H4":sha256(H4),"final_history_audit":sha256(FINAL)},
         "source_snapshot_date":SNAPSHOT_DATE,"H3_current_marker_fetch_failures":h3fail,"counts":dict(sorted(counts.items())),
         "readiness":{"accepted_model_eligible_episodes":len(episodes),"event_pairs":event_pairs,"censored_or_competing_non_event_pairs":censored_pairs,"pair_year_rows":nrows,
                      "connected_components":len(comps),"event_containing_components":event_components,"gates":gates,"READY_FOR_FEATURE_REGISTRY_FREEZE":ready,
                      "next_action":"freeze_machine_readable_feature_registry_and_engine_audit" if ready else "STOP_do_not_fit_and_do_not_lower_gate"},
         "component_summary":component_summary,"episodes":episodes,"pair_year_rows":pair_year_rows,"exclusions":exclusions,"pair_source_audit":pair_rows,
         "limitations":["Source-only development audit; no astrology/HD features calculated.","Current-open censoring requires at least two frozen structured markers; absence of an exit alone is never treated as ongoing.",
                        "Primary timing resolution is annual; source day/month precision is retained only for ordering and provenance.","Unknown/fatal ends are censors, not nonfatal-exit events."]}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k not in {"episodes","pair_year_rows","exclusions","pair_source_audit","component_summary"}},indent=2,ensure_ascii=False),flush=True)
    print(json.dumps({"readiness":out["readiness"],"counts":out["counts"],"H3_current_marker_fetch_failures_n":len(h3fail)},indent=2),flush=True)


if __name__=="__main__": main()
