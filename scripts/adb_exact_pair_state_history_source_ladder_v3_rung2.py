#!/usr/bin/env python3
"""V3 source ladder Rung 2: ADB-linked English Wikipedia infobox only.

Frozen specs:
  reference/research/adb_exact_pair_state_history_source_ladder_freeze_v3.md
  reference/research/adb_exact_pair_state_history_source_ladder_v3_rung2_parser_freeze.md

Rung-1 additions are quarantined per its engineering audit. Sufficiency accounting
starts from the clean V2 baseline of 23 endpoint-bearing pairs.
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
LADDER_FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_freeze_v3.md"
PARSER_FREEZE = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung2_parser_freeze.md"
RUNG1_AUDIT = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung1_audit.md"
V1 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v1.json"
V2 = REPO / "reference" / "research" / "adb_exact_pair_state_history_recovery_v2.json"
RUNG1 = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung1.json"
OUT = REPO / "reference" / "research" / "adb_exact_pair_state_history_source_ladder_v3_rung2.json"
ADB_API = "https://www.astro.com/wiki/astro-databank/api.php"
ENWIKI_API = "https://en.wikipedia.org/w/api.php"
UA = "humandesign-state-history-v3-rung2/1.0"

STOP = {"relationship", "spouse", "lover", "with", "born", "family", "associates", "equivalent"}
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_WORD = "(?:" + "|".join(sorted(MONTHS, key=len, reverse=True)) + ")"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
ADB_WIKI_RE = re.compile(r"\[\[\s*wikipedia\s*:\s*([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", re.I)
END_RE = re.compile(r"\b(?:divorc\w*|separat\w*|annul\w*|split\w*|breakup|broke\s+up|broken\s+up|dissolv\w*|estrang\w*)\b", re.I)
REASON_ONLY_RE = re.compile(r"^(?:div|divorc\w*|sep|separat\w*|annul\w*|split\w*|breakup|dissolv\w*|estrang\w*)$", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", urllib.parse.unquote((s or "")).replace("_", " ").casefold()).strip()


def name_tokens(s: str | None) -> set[str]:
    return {t for t in norm(s).split() if len(t) >= 4 and t not in STOP}


def api_json(base: str, params: dict) -> dict | None:
    url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception as exc:
        print("api failure", base, params.get("titles"), type(exc).__name__, flush=True)
        return None


def fetch_adb(title: str) -> str | None:
    data = api_json(ADB_API, {
        "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
        "titles": title, "formatversion": 2, "format": "json",
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing") is not None or not pages[0].get("revisions"):
        return None
    rev = pages[0]["revisions"][0]
    return (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")


def adb_id(text: str) -> int | None:
    m = re.search(r"\|DatamainID\s*=\s*(\d+)", text or "", re.I)
    return int(m.group(1)) if m else None


def adb_wikipedia_title(text: str) -> str | None:
    m = ADB_WIKI_RE.search(text or "")
    return urllib.parse.unquote(m.group(1)).replace("_", " ").strip() if m else None


def fetch_enwiki(title: str) -> tuple[str | None, str | None, str | None]:
    data = api_json(ENWIKI_API, {
        "action": "query", "prop": "revisions|pageprops", "rvprop": "content", "rvslots": "main",
        "titles": title, "redirects": 1, "formatversion": 2, "format": "json",
    })
    if not data:
        return None, None, None
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing") is not None or not pages[0].get("revisions"):
        return None, None, None
    page = pages[0]
    rev = page["revisions"][0]
    wt = (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")
    qid = (page.get("pageprops") or {}).get("wikibase_item")
    return page.get("title"), wt, qid


def balanced_block(text: str, start: int) -> str | None:
    i = start
    depth = 0
    while i < len(text) - 1:
        if text.startswith("{{", i):
            depth += 1; i += 2; continue
        if text.startswith("}}", i):
            depth -= 1; i += 2
            if depth == 0:
                return text[start:i]
            continue
        i += 1
    return None


def first_infobox(text: str) -> str | None:
    m = re.search(r"\{\{\s*Infobox\b", text or "", re.I)
    return balanced_block(text, m.start()) if m else None


def top_fields(block: str) -> dict[str, str]:
    lines = block.splitlines()
    if not lines:
        return {}
    depth = lines[0].count("{{") - lines[0].count("}}")
    current = None
    buf: list[str] = []
    out: dict[str, str] = {}

    def save():
        nonlocal current, buf
        if current is not None:
            out[current] = "\n".join(buf).strip()

    for line in lines[1:]:
        m = re.match(r"^\s*\|\s*([^=]+?)\s*=\s*(.*)$", line)
        if depth == 1 and m:
            save()
            current = re.sub(r"[^a-z]", "", m.group(1).casefold())
            buf = [m.group(2)]
        elif current is not None:
            buf.append(line)
        depth += line.count("{{") - line.count("}}")
    save()
    return out


def extract_marriage_templates(field: str) -> list[str]:
    out = []
    for m in re.finditer(r"\{\{\s*(marriage\w*|married\w*)\b", field or "", re.I):
        b = balanced_block(field, m.start())
        if b and b not in out:
            out.append(b)
    return out


def split_template_params(template: str) -> list[str]:
    s = template[2:-2]
    parts: list[str] = []
    buf: list[str] = []
    curly = 0
    square = 0
    i = 0
    while i < len(s):
        if s.startswith("{{", i): curly += 1; buf.append("{{"); i += 2; continue
        if s.startswith("}}", i): curly = max(0, curly - 1); buf.append("}}"); i += 2; continue
        if s.startswith("[[", i): square += 1; buf.append("[["); i += 2; continue
        if s.startswith("]]", i): square = max(0, square - 1); buf.append("]]"); i += 2; continue
        if s[i] == "|" and curly == 0 and square == 0:
            parts.append("".join(buf).strip()); buf = []; i += 1; continue
        buf.append(s[i]); i += 1
    parts.append("".join(buf).strip())
    return parts


def plain(s: str) -> str:
    x = html.unescape(s or "")
    x = WIKILINK_RE.sub(lambda m: (m.group(2) or m.group(1)).replace("_", " "), x)
    x = re.sub(r"<[^>]+>", " ", x)
    x = re.sub(r"\{\{[^{}]*\}\}", " ", x)
    x = x.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", x).strip()


def linked_targets(s: str) -> list[str]:
    return [urllib.parse.unquote(m.group(1)).replace("_", " ").strip() for m in WIKILINK_RE.finditer(s or "")]


def partner_match(entry: str, other_wiki_title: str | None, other_adb_name: str) -> bool:
    if other_wiki_title:
        target = norm(other_wiki_title)
        return any(norm(x) == target for x in linked_targets(entry))
    words = set(norm(plain(entry)).split())
    return bool(words & name_tokens(other_adb_name))


def iso(y: int, m: int, d: int) -> str:
    return date(y, m, d).isoformat()


def last_day(y: int, m: int) -> int:
    if m == 12:
        return (date(y + 1, 1, 1) - date.resolution).day
    return (date(y, m + 1, 1) - date.resolution).day


def date_candidates(s: str) -> list[dict]:
    text = s or ""
    out: list[dict] = []
    occupied: list[tuple[int, int]] = []

    def add(m, precision, y, mo=None, d=None):
        span = (m.start(), m.end())
        if any(not (span[1] <= a or span[0] >= b) for a, b in occupied):
            return
        try:
            if precision == "day": lo = hi = iso(y, mo, d)
            elif precision == "month": lo, hi = iso(y, mo, 1), iso(y, mo, last_day(y, mo))
            else: lo, hi = iso(y, 1, 1), iso(y, 12, 31)
        except ValueError:
            return
        occupied.append(span)
        out.append({"span": span, "text": m.group(0), "precision": precision, "interval_start": lo, "interval_end": hi})

    # Standard Wikipedia date/start-date templates.
    rx_tpl = re.compile(r"\{\{\s*(?:start\s*date|date|dts)\s*\|\s*(1[7-9]\d{2}|20\d{2})(?:\s*\|\s*(\d{1,2}))?(?:\s*\|\s*(\d{1,2}))?[^{}]*\}\}", re.I)
    for m in rx_tpl.finditer(text):
        y = int(m.group(1)); mo = int(m.group(2)) if m.group(2) else None; d = int(m.group(3)) if m.group(3) else None
        add(m, "day" if d and mo else "month" if mo else "year", y, mo, d)

    rx_dmy = re.compile(rf"(?<!\w)(\d{{1,2}})\s+({MONTH_WORD})\s+(1[7-9]\d{{2}}|20\d{{2}})(?!\d)", re.I)
    for m in rx_dmy.finditer(text): add(m, "day", int(m.group(3)), MONTHS[m.group(2).casefold()], int(m.group(1)))
    rx_mdy = re.compile(rf"(?<!\w)({MONTH_WORD})\s+(\d{{1,2}})(?:st|nd|rd|th)?[,]?\s+(1[7-9]\d{{2}}|20\d{{2}})(?!\d)", re.I)
    for m in rx_mdy.finditer(text): add(m, "day", int(m.group(3)), MONTHS[m.group(1).casefold()], int(m.group(2)))
    rx_my = re.compile(rf"(?<!\w)({MONTH_WORD})\s+(1[7-9]\d{{2}}|20\d{{2}})(?!\d)", re.I)
    for m in rx_my.finditer(text): add(m, "month", int(m.group(2)), MONTHS[m.group(1).casefold()])
    rx_y = re.compile(r"(?<!\d)(1[7-9]\d{2}|20\d{2})(?!\d)")
    for m in rx_y.finditer(text): add(m, "year", int(m.group(1)))
    return sorted(out, key=lambda x: x["span"][0])


def span_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    if a[1] < b[0]: return b[0] - a[1]
    if b[1] < a[0]: return a[0] - b[1]
    return 0


def nearest_date(text: str, term: re.Match) -> dict | None:
    dates = date_candidates(text)
    if not dates: return None
    scored = [(span_distance((term.start(), term.end()), tuple(d["span"])), d) for d in dates]
    best = min(x[0] for x in scored)
    tied = [d for dist, d in scored if dist == best]
    if len({(d["interval_start"], d["interval_end"]) for d in tied}) != 1:
        return None
    return tied[0]


def parse_template_endpoint(template: str, other_wiki: str | None, other_name: str) -> dict | None:
    if not partner_match(template, other_wiki, other_name):
        return None
    end_match = END_RE.search(plain(template))
    parts = split_template_params(template)
    if len(parts) < 2:
        return None
    named = {}
    positional = []
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            named[re.sub(r"[^a-z]", "", k.casefold())] = v.strip()
        else:
            positional.append(p.strip())
    # End reason may be compact in end=div, which plain END_RE does not catch.
    compact_reason = any(REASON_ONLY_RE.fullmatch(plain(v)) for k, v in named.items() if k in {"end", "reason", "status"})
    if not end_match and not compact_reason:
        return None

    # Prefer explicit named end-date fields that actually contain dates.
    end_date = None
    end_source = None
    for key in ("enddate", "endyear", "todate", "to", "until", "ended"):
        if key in named:
            ds = date_candidates(named[key])
            if len(ds) == 1:
                end_date = ds[0]; end_source = key; break
            if len(ds) > 1:
                # Ambiguous named end field: fail closed.
                return None
    if end_date is None and "end" in named and not REASON_ONLY_RE.fullmatch(plain(named["end"])):
        ds = date_candidates(named["end"])
        if len(ds) == 1:
            end_date = ds[0]; end_source = "end"
        elif len(ds) > 1:
            return None

    # If end=reason / reason=divorce, use the last dated positional parameter,
    # but require at least two dated positional parameters so start and end are distinguishable.
    positional_dates = []
    for idx, p in enumerate(positional):
        ds = date_candidates(p)
        if len(ds) == 1:
            positional_dates.append((idx, ds[0]))
        elif len(ds) > 1:
            return None
    if end_date is None:
        if len(positional_dates) < 2:
            return None
        end_date = positional_dates[-1][1]
        end_source = f"positional_{positional_dates[-1][0] + 1}"

    # Explicitly identify start where possible and reject same start/end.
    start_date = positional_dates[0][1] if len(positional_dates) >= 2 else None
    if start_date and (start_date["interval_start"], start_date["interval_end"]) == (end_date["interval_start"], end_date["interval_end"]):
        return None

    return {
        "evidence_type": "wikipedia_infobox_marriage_template",
        "transition": "nonfatal_exit",
        "precision": end_date["precision"],
        "interval_start": end_date["interval_start"],
        "interval_end": end_date["interval_end"],
        "date_text": end_date["text"],
        "end_date_source": end_source,
        "template": template,
    }


def remove_templates(field: str, templates: list[str]) -> str:
    out = field
    for t in templates:
        out = out.replace(t, " ")
    return out


def plain_fragments(field: str, templates: list[str]) -> list[str]:
    s = remove_templates(field, templates)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"(?m)^\s*\*\s*", "\n", s)
    return [x.strip() for x in s.splitlines() if x.strip()]


def parse_plain_endpoint(fragment: str, other_wiki: str | None, other_name: str) -> dict | None:
    if not partner_match(fragment, other_wiki, other_name):
        return None
    p = plain(fragment)
    m = END_RE.search(p)
    if not m:
        return None
    d = nearest_date(p, m)
    if not d:
        return None
    return {
        "evidence_type": "wikipedia_infobox_plain_fragment",
        "transition": "nonfatal_exit",
        "precision": d["precision"],
        "interval_start": d["interval_start"],
        "interval_end": d["interval_end"],
        "date_text": d["text"],
        "matched_term": m.group(0),
        "fragment": fragment,
    }


def overlap(a: dict, b: dict) -> bool:
    return max(a["interval_start"], b["interval_start"]) <= min(a["interval_end"], b["interval_end"])


def main() -> None:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    rung1 = json.loads(RUNG1.read_text(encoding="utf-8")) if RUNG1.exists() else {"pairs": []}
    v2_by_pair = {x["pair_key"]: x for x in v2["pairs"]}
    rung1_by_pair = {x["pair_key"]: x for x in rung1.get("pairs", [])}

    people = {}
    for p in v1["pairs"]:
        for side in ("person_a", "person_b"):
            x = p[side]
            people[int(x["adb_id"])] = {"adb_name": x["name"], "adb_title": x["wiki_title"]}

    wiki = {}
    failures = []
    link_counts = Counter()
    for i, (pid, meta) in enumerate(sorted(people.items()), 1):
        wt = fetch_adb(meta["adb_title"])
        if not wt or adb_id(wt) != pid:
            failures.append({"adb_id": pid, "stage": "adb_identity_or_fetch", "title": meta["adb_title"]})
            print(f"wiki {i}/{len(people)} adb:{pid} ADB_FAIL", flush=True)
            continue
        linked = adb_wikipedia_title(wt)
        if not linked:
            wiki[pid] = {**meta, "adb_linked_wikipedia_title": None, "canonical_wikipedia_title": None, "wikidata_qid": None, "infobox_fields": {}}
            link_counts["no_adb_wikipedia_link"] += 1
            print(f"wiki {i}/{len(people)} adb:{pid} no_link", flush=True)
            continue
        canonical, enwt, qid = fetch_enwiki(linked)
        if not canonical or not enwt:
            failures.append({"adb_id": pid, "stage": "wikipedia_fetch", "adb_linked_title": linked})
            wiki[pid] = {**meta, "adb_linked_wikipedia_title": linked, "canonical_wikipedia_title": None, "wikidata_qid": None, "infobox_fields": {}}
            link_counts["linked_but_unresolved"] += 1
            print(f"wiki {i}/{len(people)} adb:{pid} {linked} -> FAIL", flush=True)
            continue
        ib = first_infobox(enwt)
        fields = top_fields(ib) if ib else {}
        rel_fields = {k: v for k, v in fields.items() if k in {"spouse", "spouses", "partner", "partners"}}
        wiki[pid] = {**meta, "adb_linked_wikipedia_title": linked, "canonical_wikipedia_title": canonical, "wikidata_qid": qid, "infobox_fields": rel_fields}
        link_counts["resolved_wikipedia"] += 1
        if rel_fields: link_counts["with_relationship_infobox_field"] += 1
        print(f"wiki {i}/{len(people)} adb:{pid} {linked} -> {canonical} fields={list(rel_fields)}", flush=True)

    counts = Counter()
    pair_results = []
    total_endpoint_pairs = 0
    newly_endpoint_pairs = 0
    rung1_corrob_pairs = 0

    for p in v1["pairs"]:
        pk = p["pair_key"]
        a = int(p["person_a"]["adb_id"]); b = int(p["person_b"]["adb_id"])
        v2p = v2_by_pair[pk]
        v1_exits = [x for x in p.get("merged_transitions", []) if x.get("transition") == "dissolution"]
        v2_exits = v2p.get("new_v2_nonfatal_exits", [])
        baseline = ([{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v1"} for x in v1_exits] +
                    [{"interval_start": x["interval_start"], "interval_end": x["interval_end"], "source": "v2"} for x in v2_exits])
        had_baseline = bool(baseline) or bool(p.get("reunion_sequence_count"))

        evidence = []
        for src, other in ((a, b), (b, a)):
            sw = wiki.get(src) or {}
            ow = wiki.get(other) or {}
            other_title = ow.get("canonical_wikipedia_title")
            other_name = people[other]["adb_name"]
            for field_name, field_value in (sw.get("infobox_fields") or {}).items():
                templates = extract_marriage_templates(field_value)
                for t in templates:
                    ev = parse_template_endpoint(t, other_title, other_name)
                    if ev:
                        ev.update({"source_adb_id": src, "source_wikipedia_title": sw.get("canonical_wikipedia_title"), "other_adb_id": other, "infobox_field": field_name})
                        evidence.append(ev)
                for frag in plain_fragments(field_value, templates):
                    ev = parse_plain_endpoint(frag, other_title, other_name)
                    if ev:
                        ev.update({"source_adb_id": src, "source_wikipedia_title": sw.get("canonical_wikipedia_title"), "other_adb_id": other, "infobox_field": field_name})
                        evidence.append(ev)

        # Deduplicate identical source transition records.
        dedup = []
        seen = set()
        for x in evidence:
            key = (x["source_adb_id"], x["other_adb_id"], x["interval_start"], x["interval_end"], x["evidence_type"], x.get("template") or x.get("fragment"))
            if key not in seen:
                seen.add(key); dedup.append(x)
        evidence = dedup

        corroborating = []
        new = []
        for x in evidence:
            if any(overlap(x, y) for y in baseline):
                y = dict(x); y["status"] = "corroborates_v1_v2"; corroborating.append(y)
            else:
                y = dict(x); y["status"] = "new_rung2_endpoint"; new.append(y)

        has_endpoint = had_baseline or bool(new)
        if has_endpoint: total_endpoint_pairs += 1
        if new and not had_baseline: newly_endpoint_pairs += 1

        # Report whether a quarantined Rung-1 endpoint overlaps cleaner Rung-2 evidence.
        r1 = rung1_by_pair.get(pk) or {}
        r1_new = r1.get("usable_new_biography_exits", [])
        r1_corroborated = [x for x in r1_new if any(overlap(x, w) for w in evidence)]
        if r1_corroborated: rung1_corrob_pairs += 1

        counts["accepted_wikipedia_exit_evidence"] += len(evidence)
        counts["corroborating_v1_v2_evidence"] += len(corroborating)
        counts["new_wikipedia_exit_evidence"] += len(new)
        pair_results.append({
            "pair_key": pk,
            "had_clean_v1_v2_endpoint": had_baseline,
            "wikipedia_identity_a": {k: wiki.get(a, {}).get(k) for k in ("adb_linked_wikipedia_title", "canonical_wikipedia_title", "wikidata_qid")},
            "wikipedia_identity_b": {k: wiki.get(b, {}).get(k) for k in ("adb_linked_wikipedia_title", "canonical_wikipedia_title", "wikidata_qid")},
            "accepted_wikipedia_exits": evidence,
            "corroborating_v1_v2_exits": corroborating,
            "new_rung2_exits": new,
            "quarantined_rung1_exits_independently_corroborated": r1_corroborated,
        })

    out = {
        "status": "development_state_history_source_ladder_rung2",
        "ladder_freeze": str(LADDER_FREEZE.relative_to(REPO)),
        "ladder_freeze_sha256": sha256(LADDER_FREEZE),
        "parser_freeze": str(PARSER_FREEZE.relative_to(REPO)),
        "parser_freeze_sha256": sha256(PARSER_FREEZE),
        "rung1_audit": str(RUNG1_AUDIT.relative_to(REPO)),
        "v1_sha256": sha256(V1),
        "v2_sha256": sha256(V2),
        "pair_universe": len(v1["pairs"]),
        "people": len(people),
        "identity_counts": dict(link_counts),
        "source_failures": failures,
        "rung2_counts": dict(counts),
        "endpoint_counts": {
            "clean_v2_baseline_endpoint_pairs": int(v2["stop_go"]["endpoint_pairs_observed"]),
            "pairs_newly_gaining_endpoint_from_rung2": newly_endpoint_pairs,
            "total_clean_endpoint_pairs_after_rung2": total_endpoint_pairs,
            "pairs_where_rung2_corroborates_quarantined_rung1_exit": rung1_corrob_pairs,
        },
        "stop_go": {
            "minimum_endpoint_pairs": 30,
            "endpoint_pairs_observed": total_endpoint_pairs,
            "stop_source_ladder_and_freeze_model_spec": total_endpoint_pairs >= 30,
            "continue_to_rung3": total_endpoint_pairs < 30,
        },
        "pairs": pair_results,
        "limitations": [
            "Only ADB-linked English Wikipedia identities are used; no Wikipedia name search is performed.",
            "Only lead infobox spouse/partner fields are parsed; article prose is excluded.",
            "Bare end years without an explicit nonfatal ending marker do not count.",
            "Quarantined Rung-1 Biography additions do not independently contribute to the threshold count.",
            "No astrology or Human Design features are calculated or inspected.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
