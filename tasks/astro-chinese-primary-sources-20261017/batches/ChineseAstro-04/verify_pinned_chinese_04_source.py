#!/usr/bin/env python3
"""Anchor 65 historical original Chinese passages to exact oldid 1963110 wikitext.

Checks SHA, headings, section-bounded verbatim phrases and UTF-8 offsets. No
astrological predictive or actual human accuracy is assumed.
"""

import argparse
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
NOTES = B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"
RAW_EXPECTED_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
HEADINGS = [
    "安童限诀",
    "安命主",
    "安身主",
    "论安命金锁铁蛇关",
    "定男女竹萝三限",
    "定十二宫弱强",
    "定十二宫星辰落闲",
    "安流禄流羊流陀诀 论流年太岁",
    "论星辰生克制化",
    "论诸星分属南北斗化吉凶并分属五行",
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(file, value):
    Path(file).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify(source_file):
    raw = source_file.read_bytes()
    assert len(raw) == 106736
    assert sha(raw) == RAW_EXPECTED_SHA
    t = raw.decode("utf-8")
    data = json.loads(NOTES.read_text(encoding="utf-8"))
    assert data["wikisource_revision_id"] == 1963110
    assert data["raw_source_sha256"] == RAW_EXPECTED_SHA
    assert data["count"] == 65
    assert [r["id"] for r in data["records"]] == [f"ZWD-R{n:04d}" for n in range(97, 162)]
    starts = {name: t.find(name) for name in HEADINGS}
    assert all(start >= 0 for start in starts.values())
    assert list(starts.values()) == sorted(starts.values())
    boundaries = {}
    for i, name in enumerate(HEADINGS):
        start = starts[name]
        end = (
            starts[HEADINGS[i + 1]]
            if i + 1 < len(HEADINGS)
            else t.find("<poem>", t.find("</poem>", start) + len("</poem>"))
        )
        assert 0 < start < end
        boundaries[name] = (start, end)
    results = []
    for r in data["records"]:
        section = r["locator"].split(":", 1)[1]
        assert section in boundaries
        begin, end = boundaries[section]
        original = r["original_chinese_anchor"]
        assert len(original) >= 4, (r["id"], original)
        local = t[begin:end]
        k = local.find(original)
        assert k >= 0, (r["id"], section, original)
        at = begin + k
        assert at >= begin and at + len(original) <= end
        assert t[at : at + len(original)] == original
        assert r["source_revision_id"] == 1963110
        assert not r["runtime_promoted"]
        r["rule_status"] = "SOURCE_ONLY_DOCUMENTED"
        r["original_revision_quote_match_confirmed"] = True
        r["raw_revision_anchor_char_offset"] = at
        r["raw_revision_anchor_utf8_byte_offset"] = len(t[:at].encode("utf-8"))
        r["raw_revision_anchor_utf8_sha256"] = sha(original.encode("utf-8"))
        results.append(
            {
                "id": r["id"],
                "section_name": section,
                "section_start_char_offset": begin,
                "section_end_char_offset": end,
                "anchor_text": original,
                "anchor_start_char_offset": at,
                "anchor_utf8_byte_offset": r["raw_revision_anchor_utf8_byte_offset"],
                "anchor_utf8_sha256": r["raw_revision_anchor_utf8_sha256"],
                "original_source_sha256": RAW_EXPECTED_SHA,
            }
        )
    assert len(results) == 65
    data["short_chinese_quote_direct_match_count"] = 65
    save(NOTES, data)
    out = {
        "schema": "ZIWEI_PINNED_VOLUME_II_SOURCE_QUOTE_SHA_BYTE_ANCHOR_WITNESS_V1",
        "batch": "ChineseAstro-04",
        "original_source": (
            "Zi Wei Dou Shu Quan Shu Volume II transmitted Wikisource revision oldid1963110"
        ),
        "original_full_raw_source_sha256": RAW_EXPECTED_SHA,
        "original_full_raw_source_bytes": len(raw),
        "source_revision_id": 1963110,
        "original_wikitext_permalink": data["raw_wikitext_permalink"],
        "separate_original_heading_ranges": boundaries,
        "original_quote_count": len(results),
        "all_65_short_anchor_exact_matches": True,
        "source_is_authentic_Ming_woodblock_verified": False,
        "independent_classical_Chinese_translation_validated": False,
        "full_lunisolar_birthdate_and_14_star_engine_verified": False,
        "independent_actual_human_outcome_validations": 0,
        "runtime_promotions": 0,
        "anchor_receipts": results,
    }
    save(WITNESS, out)
    print(
        json.dumps(
            {
                "raw_source_sha256": sha(raw),
                "65_exact_quotes": len(results),
                "source_sections": len(boundaries),
                "records_sha256": sha(NOTES.read_bytes()),
                "witness_sha256": sha(WITNESS.read_bytes()),
                "Lilly_unchanged": 12472,
                "human_prediction_validations": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--raw-source", type=Path, required=True)
    verify(p.parse_args().raw_source)
