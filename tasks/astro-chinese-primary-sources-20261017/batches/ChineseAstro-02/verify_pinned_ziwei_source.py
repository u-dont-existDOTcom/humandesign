#!/usr/bin/env python3
"""Verify short Chinese passage anchors against pinned Wikisource original revision."""

import hashlib
import json
import sys
from pathlib import Path

import requests

B = Path(__file__).resolve().parent
SOURCE = B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"


def verify():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    url = "https://zh.wikisource.org/w/index.php?title=紫微斗數全書/卷二&oldid=1963110&action=raw"
    result = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": (
                "HumanDesign historical-source audit/0.1 "
                "(github.com/u-dont-existDOTcom/humandesign)"
            )
        },
    )
    result.raise_for_status()
    raw = result.content
    full_hash = hashlib.sha256(raw).hexdigest()
    assert full_hash == data["raw_source_sha256"], (
        "Pinned original text changed bytes! Stop rather than silently accepting."
    )
    text = result.text
    unmatched = []
    for row in data["records"]:
        anchor = row["original_chinese_anchor"]
        section = row["locator"].split(":", 1)[1]
        if anchor not in text or section not in text:
            unmatched.append(
                {
                    "id": row["id"],
                    "anchor": anchor,
                    "section": section,
                    "anchor_found": anchor in text,
                    "section_found": section in text,
                }
            )
        else:
            row["original_revision_quote_match_confirmed"] = True
    report = {
        "schema": "ZIWEI_ORIGINAL_PINNED_WIKISOURCE_WITNESS_V1",
        "wikisource_revision_id": 1963110,
        "source_raw_url": url,
        "wikitext_bytes": len(raw),
        "wikitext_sha256": full_hash,
        "accepted_quote_count": len(data["records"]) - len(unmatched),
        "total": len(data["records"]),
        "unmatched": unmatched,
        "copyright_scope": "Store only short anchors and hashes, not full host text.",
        "independent_expert_translation_validation": False,
        "human_astrological_validation": False,
    }
    WITNESS.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if unmatched:
        sys.exit(1)


if __name__ == "__main__":
    verify()
