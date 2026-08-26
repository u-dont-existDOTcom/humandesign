#!/usr/bin/env python3
"""V3 source ladder, Rung 1: strict ADB Biography same-sentence extraction.

Frozen spec:
  reference/research/adb_exact_pair_state_history_source_ladder_freeze_v3.md

No astrology or Human Design features are calculated or inspected.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_freeze_v3.md"
V1 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v1.json"
V2 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v2.json"
OUT = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung1.json"
API = "https://www.astro.com/wiki/astro-databank/api.php"
UA = "humandesign-state-history-v3-rung1/1.0"

STOP = {"relationship", "spouse", "lover", "with", "born", "family", "associates", "equivalent"}
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_WORD = "(?:" + "|".join(sorted(MONTHS, key=len, reverse=True)) + ")"

END_PATTERNS = [
    ("divorce", re.compile(r"\bdivorc\w*\b", re.I)),
    ("separation", re.compile(r"\bseparat\w*\b", re.I)),
    ("breakup", re.compile(r"\bsplit\w*\b|\bbroke\s+up\b|\bbroken\s+up\b", re.I)),
    ("annulment", re.compile(r"\bannul\w*\b", re.I)),
    ("dissolution", re.compile(r"\bdissolv\w*\b", re.I)),
    ("estrangement", re.compile(r"\bestrang\w*\b", re.I)),
]
REL_CUE = re.compile(r"\b(?:marri\w*|wife|wives|husband|spouse|lover|relationship|dating|dated|romance|couple|affair|partner)\b", re.I)
FORMATION_PATTERNS = [
    ("meet", re.compile(r"\bmet\b", re.I)),
    ("dating", re.compile(r"\bbegan\s+dating\b|\bstarted\s+dating\b", re.I)),
    ("marriage", re.compile(r"\bmarri\w*\b|\bwedding\b", re.I)),
]
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
EXT_LINK_RE = re.compile(r"\[(?:https?://[^\s\]]+)(?:\s+([^\]]+))?\]")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def name_tokens(s: str | None) -> set[str]:
    return {t for t in norm(s).split() if len(t) >= 4 and t not in STOP}


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
    try:
        return int(field(text, "DatamainID") or 0) == expected
    except ValueError:
        return False


def section(text: str, heading: str) -> str:
    m = re.search(rf"(?im)^==\s*{re.escape(heading)}\s*==\s*$", text or "")
    if not m:
        return ""
    tail = text[m.end():]
    n = re.search(r"(?im)^==\s*[^=].*?\s*==\s*$", tail)
    return tail[:n.start()] if n else tail


def strip_templates(s: str) -> str:
    # Repeatedly remove non-nested templates. Biography citations/templates are
    # irrelevant to the frozen same-sentence rule.
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    return s


def plain_biography(wt: str) -> str:
    s = section(wt, "Biography")
    s = re.sub(r"<ref\b[^>]*>.*?</ref\s*>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<ref\b[^>]*/\s*>", " ", s, flags=re.I)
    s = LINK_RE.sub(lambda m: (m.group(2) or m.group(1)).replace("_", " "), s)
    s = EXT_LINK_RE.sub(lambda m: m.group(1) or " ", s)
    s = strip_templates(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("'''", "").replace("''", "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def sentences(text: str) -> list[str]:
    # Conservative sentence splitter: punctuation followed by whitespace and a
    # likely new sentence token. False negatives are preferable to cross-sentence inference.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“‘])", text)
    return [x.strip() for x in parts if x.strip()]


def iso(y: int, m: int, d: int) -> str:
    return date(y, m, d).isoformat()


def last_day(y: int, m: int) -> int:
    if m == 12:
        return (date(y + 1, 1, 1) - date.resolution).day
    return (date(y, m + 1, 1) - date.resolution).day


def date_candidates(sentence: str) -> list[dict]:
    specs = [
        ("day", re.compile(rf"(?<!\w)(\d{{1,2}})\s+({MONTH_WORD})\s+(1[5-9]\d{{2}}|20\d{{2}})(?!\d)", re.I), "dmy"),
        ("day", re.compile(rf"(?<!\w)({MONTH_WORD})\s+(\d{{1,2}})(?:st|nd|rd|th)?[,]?\s+(1[5-9]\d{{2}}|20\d{{2}})(?!\d)", re.I), "mdy"),
        ("month", re.compile(rf"(?<!\w)({MONTH_WORD})\s+(1[5-9]\d{{2}}|20\d{{2}})(?!\d)", re.I), "my"),
        ("year", re.compile(r"(?<!\d)(1[5-9]\d{2}|20\d{2})(?!\d)"), "y"),
    ]
    occupied: list[tuple[int, int]] = []
    out = []
    for precision, rx, fmt in specs:
        for m in rx.finditer(sentence):
            if any(not (m.end() <= a or m.start() >= b) for a, b in occupied):
                continue
            try:
                if fmt == "dmy":
                    d, mon, y = int(m.group(1)), MONTHS[m.group(2).casefold()], int(m.group(3))
                    lo = hi = iso(y, mon, d)
                elif fmt == "mdy":
                    mon, d, y = MONTHS[m.group(1).casefold()], int(m.group(2)), int(m.group(3))
                    lo = hi = iso(y, mon, d)
                elif fmt == "my":
                    mon, y = MONTHS[m.group(1).casefold()], int(m.group(2))
                    lo, hi = iso(y, mon, 1), iso(y, mon, last_day(y, mon))
                else:
                    y = int(m.group(1)); lo, hi = iso(y, 1, 1), iso(y, 12, 31)
            except (ValueError, KeyError):
                continue
            occupied.append((m.start(), m.end()))
            out.append({"span": [m.start(), m.end()], "text": m.group(0), "precision": precision, "interval_start": lo, "interval_end": hi})
    return sorted(out, key=lambda x: x["span"][0])


def span_distance(a: tuple[int, int], b: list[int]) -> int:
    if a[1] < b[0]:
        return b[0] - a[1]
    if b[1] < a[0]:
        return a[0] - b[1]
    return 0


def nearest_date(term_span: tuple[int, int], dates: list[dict]) -> dict | None:
    if not dates:
        return None
    ds = [(span_distance(term_span, d["span"]), d) for d in dates]
    best = min(x[0] for x in ds)
    tied = [d for dist, d in ds if dist == best]
    unique_intervals = {(d["interval_start"], d["interval_end"]) for d in tied}
    if len(unique_intervals) != 1:
        return None
    return tied[0]


def partner_match(sentence: str, other_name: str, other_title: str) -> bool:
    words = set(norm(sentence).split())
    return bool(words & (name_tokens(other_name) | name_tokens(other_title)))


def extract_sentence_evidence(source_id: int, source_title: str, text: str, other_id: int, other_name: str, other_title: str):
    exits = []
    formations = []
    for sent in sentences(text):
        if not partner_match(sent, other_name, other_title):
            continue
        dates = date_candidates(sent)
        if not dates:
            continue
        romantic = bool(REL_CUE.search(sent))
        if romantic:
            for end_kind, rx in END_PATTERNS:
                for m in rx.finditer(sent):
                    d = nearest_date((m.start(), m.end()), dates)
                    if not d:
                        continue
                    exits.append({
                        "source_adb_id": source_id,
                        "source_title": source_title,
                        "other_adb_id": other_id,
                        "evidence_type": "adb_biography_same_sentence",
                        "transition": "nonfatal_exit",
                        "end_kind": end_kind,
                        "matched_term": m.group(0),
                        "precision": d["precision"],
                        "interval_start": d["interval_start"],
                        "interval_end": d["interval_end"],
                        "date_text": d["text"],
                        "sentence": sent,
                    })
        for form_kind, rx in FORMATION_PATTERNS:
            for m in rx.finditer(sent):
                d = nearest_date((m.start(), m.end()), dates)
                if not d:
                    continue
                formations.append({
                    "source_adb_id": source_id,
                    "source_title": source_title,
                    "other_adb_id": other_id,
                    "evidence_type": "adb_biography_same_sentence",
                    "transition": "formation",
                    "formation_kind": form_kind,
                    "matched_term": m.group(0),
                    "precision": d["precision"],
                    "interval_start": d["interval_start"],
                    "interval_end": d["interval_end"],
                    "date_text": d["text"],
                    "sentence": sent,
                })
    # Exact duplicates can arise from repeated regex paths; deduplicate deterministically.
    def dedupe(items, kind_key):
        seen = set(); out = []
        for x in items:
            key = (x[kind_key], x["interval_start"], x["interval_end"], x["source_adb_id"], x["sentence"])
            if key not in seen:
                seen.add(key); out.append(x)
        return out
    return dedupe(exits, "end_kind"), dedupe(formations, "formation_kind")


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def main() -> None:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    v2_by_pair = {x["pair_key"]: x for x in v2["pairs"]}

    people = {}
    for p in v1["pairs"]:
        for side in ("person_a", "person_b"):
            q = p[side]
            people[int(q["adb_id"])] = {"name": q["name"], "title": q["wiki_title"]}

    bios = {}
    failures = []
    for i, (adb_id, meta) in enumerate(sorted(people.items()), 1):
        wt = fetch_wikitext(meta["title"])
        if not wt or not exact_id(wt, adb_id):
            failures.append({"adb_id": adb_id, "title": meta["title"]})
            print(f"bio {i}/{len(people)} {adb_id} FAILED", flush=True)
            continue
        bios[adb_id] = plain_biography(wt)
        print(f"bio {i}/{len(people)} {adb_id} chars={len(bios[adb_id])}", flush=True)

    counts = Counter()
    pair_results = []
    total_endpoint_pairs = 0
    newly_endpoint_pairs = 0
    reunion_pairs = 0

    for p in v1["pairs"]:
        pk = p["pair_key"]
        a = int(p["person_a"]["adb_id"]); b = int(p["person_b"]["adb_id"])
        ma, mb = people[a], people[b]
        exits = []
        forms = []
        if a in bios:
            e, f = extract_sentence_evidence(a, ma["title"], bios[a], b, mb["name"], mb["title"]); exits += e; forms += f
        if b in bios:
            e, f = extract_sentence_evidence(b, mb["title"], bios[b], a, ma["name"], ma["title"]); exits += e; forms += f

        v1_exits = [x for x in p.get("merged_transitions", []) if x.get("transition") == "dissolution"]
        v1_forms = [x for x in p.get("merged_transitions", []) if x.get("transition") == "formation"]
        v2p = v2_by_pair[pk]
        v2_exits = v2p.get("new_v2_nonfatal_exits", [])
        baseline_exits = ([{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v1"} for x in v1_exits] +
                          [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v2"} for x in v2_exits])
        had_baseline = bool(baseline_exits) or bool(p.get("reunion_sequence_count"))

        corroborating = []
        new = []
        conflicts = []
        for x in exits:
            if any(overlap(x, y) for y in baseline_exits):
                x = dict(x); x["status"] = "corroborates_higher_precedence_exit"; corroborating.append(x)
            else:
                new.append(x)

        # Same-kind, non-overlapping biography claims are retained as conflicts.
        by_kind = {}
        for x in new:
            by_kind.setdefault(x["end_kind"], []).append(x)
        conflicted_ids = set()
        for kind, items in by_kind.items():
            groups = []
            for x in sorted(items, key=lambda z: (z["interval_start"], z["interval_end"])):
                if any(overlap(x, g[0]) for g in groups):
                    for g in groups:
                        if overlap(x, g[0]): g.append(x); break
                else:
                    groups.append([x])
            if len(groups) > 1:
                for g in groups:
                    for x in g: conflicted_ids.add(id(x))
                conflicts.append({"end_kind": kind, "nonoverlapping_groups": groups})
        usable_new = [x for x in new if id(x) not in conflicted_ids]

        has_endpoint = had_baseline or bool(usable_new)
        if has_endpoint:
            total_endpoint_pairs += 1
        if usable_new and not had_baseline:
            newly_endpoint_pairs += 1

        all_exits = baseline_exits + [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v3_rung1_bio"} for x in usable_new]
        all_forms = ([{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v1", "kind": x.get("event_kind")} for x in v1_forms] +
                     [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v3_rung1_bio", "kind": x.get("formation_kind")} for x in forms])
        reunions = []
        for ex in all_exits:
            for fm in all_forms:
                if fm["interval_start"] > ex["interval_end"]:
                    reunions.append({"exit": ex, "later_formation": fm})
        if reunions:
            reunion_pairs += 1

        counts["accepted_exit_evidence"] += len(exits)
        counts["accepted_formation_evidence"] += len(forms)
        counts["usable_new_exit_evidence"] += len(usable_new)
        counts["corroborating_exit_evidence"] += len(corroborating)
        counts["conflict_groups"] += len(conflicts)
        pair_results.append({
            "pair_key": pk,
            "had_v1_v2_endpoint": had_baseline,
            "accepted_biography_exits": exits,
            "usable_new_biography_exits": usable_new,
            "corroborating_biography_exits": corroborating,
            "accepted_biography_formations": forms,
            "biography_conflicts": conflicts,
            "inferred_reunion_sequences": reunions,
        })

    out = {
        "status": "development_state_history_source_ladder_rung1",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "v1_sha256": sha256(V1),
        "v2_sha256": sha256(V2),
        "pair_universe": len(v1["pairs"]),
        "people": len(people),
        "resolved_biographies": len(bios),
        "source_failures": failures,
        "rung1_counts": dict(counts),
        "endpoint_counts": {
            "baseline_v2_endpoint_pairs": int(v2["stop_go"]["endpoint_pairs_observed"]),
            "pairs_newly_gaining_endpoint_from_rung1": newly_endpoint_pairs,
            "total_endpoint_pairs_after_rung1": total_endpoint_pairs,
            "pairs_with_inferred_reunion_after_rung1": reunion_pairs,
        },
        "stop_go": {
            "minimum_endpoint_pairs": 30,
            "endpoint_pairs_observed": total_endpoint_pairs,
            "stop_source_ladder_and_freeze_model_spec": total_endpoint_pairs >= 30,
            "continue_to_rung2": total_endpoint_pairs < 30,
        },
        "pairs": pair_results,
        "limitations": [
            "ADB Biography prose is used only under the frozen same-sentence lexical rules; no cross-sentence pronoun resolution or manual interpretation is allowed.",
            "This remains ADB development data and is not independent validation.",
            "No astrology or Human Design features are calculated or inspected in Rung 1.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
