#!/usr/bin/env python3
"""Transport-only batch runner for frozen V3 Rung 2.

The first Rung-2 run encountered Wikimedia HTTP throttling after a small number
of individual page requests. This runner leaves every parser/evidence rule in
adb_exact_pair_state_history_source_ladder_v3_rung2.py unchanged, but prefetches
ADB pages and ADB-linked Wikipedia pages in small batched MediaWiki queries,
then injects those caches into the frozen implementation.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import adb_exact_pair_state_history_source_ladder_v3_rung2 as base


def resolve_batch(titles: list[str], attempts: int = 4) -> dict[str, tuple[str | None, str | None, str | None]]:
    """Fetch a small set of exact ADB-linked enwiki titles with redirects.

    Returns a map keyed by base.norm(input title). Failures remain explicit
    (None, None, None); no name search or fallback identity resolution occurs.
    """
    unique = []
    seen = set()
    for t in titles:
        k = base.norm(t)
        if k and k not in seen:
            seen.add(k); unique.append(t)
    if not unique:
        return {}

    data = None
    for attempt in range(attempts):
        data = base.api_json(base.ENWIKI_API, {
            "action": "query",
            "prop": "revisions|pageprops",
            "rvprop": "content",
            "rvslots": "main",
            "titles": "|".join(unique),
            "redirects": 1,
            "formatversion": 2,
            "format": "json",
        })
        if data:
            break
        time.sleep(2.0 * (attempt + 1))
    if not data:
        # Fail closed. Splitting a failed batch is a transport retry only; it
        # does not search or alter identity rules.
        if len(unique) > 1:
            mid = len(unique) // 2
            out = resolve_batch(unique[:mid], attempts=attempts)
            out.update(resolve_batch(unique[mid:], attempts=attempts))
            return out
        return {base.norm(unique[0]): (None, None, None)}

    q = data.get("query", {})
    remap = {}
    for x in q.get("normalized", []) or []:
        remap[base.norm(x.get("from"))] = x.get("to")
    for x in q.get("redirects", []) or []:
        remap[base.norm(x.get("from"))] = x.get("to")

    page_by_norm = {}
    for page in q.get("pages", []) or []:
        title = page.get("title")
        if title:
            page_by_norm[base.norm(title)] = page

    out = {}
    for original in unique:
        cur = original
        traversed = set()
        while base.norm(cur) in remap and base.norm(cur) not in traversed:
            traversed.add(base.norm(cur))
            cur = remap[base.norm(cur)]
        page = page_by_norm.get(base.norm(cur))
        if not page or page.get("missing") is not None or not page.get("revisions"):
            out[base.norm(original)] = (None, None, None)
            continue
        rev = page["revisions"][0]
        wt = (rev.get("slots", {}).get("main", {}) or {}).get("content") or rev.get("content") or rev.get("*")
        qid = (page.get("pageprops") or {}).get("wikibase_item")
        out[base.norm(original)] = (page.get("title"), wt, qid)
    return out


def main() -> None:
    v1 = json.loads(base.V1.read_text(encoding="utf-8"))
    people = {}
    for pair in v1["pairs"]:
        for side in ("person_a", "person_b"):
            p = pair[side]
            people[int(p["adb_id"])] = {"adb_name": p["name"], "adb_title": p["wiki_title"]}

    # Cache the exact ADB pages once and extract only their explicit interwiki links.
    adb_cache = {}
    linked = []
    for i, (pid, meta) in enumerate(sorted(people.items()), 1):
        wt = base.fetch_adb(meta["adb_title"])
        adb_cache[meta["adb_title"]] = wt
        if wt and base.adb_id(wt) == pid:
            title = base.adb_wikipedia_title(wt)
            if title:
                linked.append(title)
        print(f"prefetch ADB {i}/{len(people)} adb:{pid}", flush=True)

    # Small batches avoid the per-page request pattern that was throttled.
    wiki_cache = {}
    unique_linked = []
    seen = set()
    for t in linked:
        k = base.norm(t)
        if k not in seen:
            seen.add(k); unique_linked.append(t)
    batch_size = 8
    for i in range(0, len(unique_linked), batch_size):
        batch = unique_linked[i:i + batch_size]
        print(f"prefetch enwiki batch {i // batch_size + 1}/{(len(unique_linked) + batch_size - 1) // batch_size} n={len(batch)}", flush=True)
        wiki_cache.update(resolve_batch(batch))
        time.sleep(1.0)

    # Transport monkeypatch only; base.main retains all frozen parsing/counting logic.
    base.fetch_adb = lambda title: adb_cache.get(title)
    base.fetch_enwiki = lambda title: wiki_cache.get(base.norm(title), (None, None, None))
    base.main()


if __name__ == "__main__":
    main()
