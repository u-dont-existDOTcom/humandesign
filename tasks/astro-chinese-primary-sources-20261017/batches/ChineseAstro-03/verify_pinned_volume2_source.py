#!/usr/bin/env python3
"""Prove original Chinese short anchors against immutable Wikisource oldid 1963110.

This verifies exact source wording within the same source section and records
its byte offsets; it does NOT attest a Ming original or predictive validity.
"""

import hashlib
import json
from pathlib import Path

import requests

B = Path(__file__).resolve().parent
NOTES = B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"
URL = (
    "https://zh.wikisource.org/w/index.php?"
    "title=%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B8%E5%85%A8%E6%9B%B8/"
    "%E5%8D%B7%E4%BA%8C&oldid=1963110&action=raw"
)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def verify():
    notes = json.loads(NOTES.read_text(encoding="utf-8"))
    assert notes["wikisource_revision_id"] == 1963110
    response = requests.get(
        URL,
        timeout=35,
        headers={
            "User-Agent": (
                "HumanDesign historical-original-source audit/0.1 "
                "(github.com/u-dont-existDOTcom/humandesign)"
            )
        },
    )
    response.raise_for_status()
    original = response.content
    assert len(original) == 106736
    assert (
        digest(original)
        == notes["raw_source_sha256"]
        == ("1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72")
    )
    text = response.text
    details = []
    for row in notes["records"]:
        section = row["locator"].split(":", 1)[1]
        anchor = row["original_chinese_anchor"]
        start = text.find(section)
        pos = text.find(anchor, start)
        assert start >= 0 and start <= pos < start + 4000, (row["id"], section, anchor, start, pos)
        assert text[pos : pos + len(anchor)] == anchor
        assert row["source_revision_id"] == 1963110
        row["original_revision_quote_match_confirmed"] = True
        row["rule_status"] = "SOURCE_ONLY_DOCUMENTED"
        row["raw_revision_anchor_char_offset"] = pos
        row["raw_revision_anchor_utf8_byte_offset"] = len(text[:pos].encode("utf-8"))
        row["raw_revision_anchor_utf8_sha256"] = digest(anchor.encode("utf-8"))
        details.append(
            {
                "id": row["id"],
                "original_chinese_anchor": anchor,
                "original_source_section": section,
                "source_section_char_offset": start,
                "anchor_char_offset": pos,
                "anchor_utf8_byte_offset": row["raw_revision_anchor_utf8_byte_offset"],
                "anchor_utf8_sha256": row["raw_revision_anchor_utf8_sha256"],
            }
        )
    assert len(details) == notes["count"] == 45
    notes["original_revision_quote_matches"] = len(details)
    NOTES.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    witness = {
        "schema": "CHINESE_ZIWEI_VOL2_45_SOURCE_ANCHOR_REVISION_WITNESS_V1",
        "batch": "ChineseAstro-03",
        "pinned_wikisource_revision_id": 1963110,
        "pinned_raw_url": URL,
        "raw_source_sha256": digest(original),
        "raw_source_bytes": len(original),
        "short_exact_chinese_anchor_matches": len(details),
        "source_section_titles_and_anchor_offsets_verified": True,
        "new_history_ids": [r["id"] for r in notes["records"]],
        "audit_photo_or_printed_original_Ming_source_verified": False,
        "independent_classical_Chinese_expert_translation_verified": False,
        "complete_chinese_edition_diplomatic_collation": False,
        "independent_real_person_predictive_validity": False,
        "model_runtime_promotions": 0,
        "anchors": details,
    }
    WITNESS.write_text(json.dumps(witness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "source_revision": 1963110,
                "source_sha256": digest(original),
                "matches": len(details),
                "notes_sha256": digest(NOTES.read_bytes()),
                "witness_sha256": digest(WITNESS.read_bytes()),
                "human_prediction_validations": 0,
                "runtime_promotions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    verify()
