#!/usr/bin/env python3
"""Freeze original transmitted Zi Wei Children text; documentary evidence only."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
ORIGINAL = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS = T / "CHINESE_SOURCE_AUDIT_INDEX_V18.json"
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V18_SHA = "d3bdefc69a441140b9b16ef82bd10aad786a3d31e9919e5baec821fbe009e9eb"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
START, END = 39218, 40563
CONTINUATIONS = {6: "ZiWei", 11: "TianTong", 15: "TaiYin", 19: "TianXiang"}
PREAMBLES = {1, 2, 3, 4}
STARS = {
    5: "ZiWei", 7: "TianJi", 8: "TaiYang", 9: "WuQu", 10: "TianTong",
    12: "LianZhen", 13: "TianFu", 14: "TaiYin", 16: "TanLang",
    17: "JuMen", 18: "TianXiang", 20: "TianLiang", 21: "QiSha",
    22: "PoJun", 23: "ZuoFu", 24: "YouBi", 25: "WenChang",
    26: "WenQu", 27: "LuCun", 28: "YangTuo", 29: "HuoXing",
    30: "LingXing", 31: "KuiYue", 32: "DouJun",
}
FLAGS = ("男", "女", "子", "刑", "伤", "殺", "杀", "死", "绝", "疾", "孤", "克", "貴", "贵", "庶", "偏室")


def digest(b: bytes) -> str:
    return sha256(b).hexdigest()


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(name: str, obj: object) -> None:
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze() -> None:
    raw = ORIGINAL.read_bytes()
    if len(raw) != 106736 or digest(raw) != RAW_SHA:
        raise ValueError("Original Wikitext source changed")
    if digest(PREVIOUS.read_bytes()) != V18_SHA or digest(WESTERN.read_bytes()) != WEST_SHA:
        raise ValueError("Previously accepted index or inherited Western source changed")
    idx = read(PREVIOUS)
    west = read(WESTERN)
    if idx["sum_source_annotations"] != 1004 or [
        (x["accepted_source_annotations"], x["next_id"]) for x in idx["systems"]
    ] != [(210, "BZI-R0211"), (794, "ZWD-R0795")]:
        raise ValueError("Wrong Chinese V18 canonical frontier")
    if idx["accepted_batches"][-1]["id"] != "ChineseAstro-18SRC-Spouses":
        raise ValueError("V18 source list changed")
    if (west["records_count"], west["batches"][-1]["id"]) != (13044, "B07bc"):
        raise ValueError("Independent Western older snapshot changed")
    s = raw.decode("utf-8")
    if len(s) != 48890:
        raise ValueError("Original source codepoint count changed")
    if not s[START:].startswith("===四子女===") or not s[END:].startswith("===五财帛==="):
        raise ValueError("Original Children/Wealth boundaries moved")
    if s.find("===五财帛===", START) != END:
        raise ValueError("Original Wealth boundary duplicated/moved")
    excerpt = s[START:END]
    (B / "SOURCE_1963110_CHILDREN_EXACT_EXCERPT.txt").write_bytes(excerpt.encode("utf-8"))
    cursor = START
    records = []
    markup = []
    physical_line_idx = 0
    for raw_line in excerpt.splitlines(keepends=True):
        text = raw_line.strip()
        cp = cursor + (raw_line.index(text) if text else 0)
        cursor += len(raw_line)
        if not text:
            continue
        if text in ("<poem>", "</poem>"):
            markup.append({"source_codepoint": cp, "literal_markup": text})
            continue
        line_no = physical_line_idx
        physical_line_idx += 1
        if line_no == 0:
            group, kind = "ChildrenSection", "SOURCE_SECTION_HEADING"
        elif line_no in PREAMBLES:
            group, kind = "ChildrenMethodPreamble", "SOURCE_METHOD_AND_CONDITION_PREMISE"
        elif line_no in CONTINUATIONS:
            group, kind = CONTINUATIONS[line_no], "SOURCE_CONTINUED_PREVIOUS_STAR_PROFILE_LINE"
        elif line_no in STARS:
            group, kind = STARS[line_no], "SOURCE_STAR_PROFILE_OR_COMBINED_RULE_LINE"
        else:
            raise ValueError(f"Unexpected physical source line {line_no}")
        q = text.encode("utf-8")
        byte_pos = len(s[:cp].encode("utf-8"))
        if s[cp : cp + len(text)] != text or raw[byte_pos:byte_pos+len(q)] != q:
            raise ValueError("Original source quote does not match full raw bytes")
        if not (START <= cp < cp+len(text) <= END):
            raise ValueError("Source quote beyond section boundary")
        records.append({
            "id": f"ZWD-R{795+len(records):04d}",
            "source": "ZWDS-CLASSIC-01",
            "batch": "ChineseAstro-19SRC-Children",
            "original_source_revision": 1963110,
            "full_original_Wikitext_SHA256": RAW_SHA,
            "original_source_group": group,
            "source_type": kind,
            "source_original_exact_Chinese_quote": text,
            "quote_SHA256": digest(q),
            "quote_UTF8_bytes": len(q),
            "absolute_codepoint_offset": cp,
            "absolute_UTF8_byte_offset": byte_pos,
            "excerpt_relative_codepoint_offset": cp-START,
            "original_line_index": line_no,
            "historic_reproductive_health_family_welfare_stereotypes_present": any(f in text for f in FLAGS),
            "original_Ming_printing_independently_authenticated": False,
            "independent_human_blind_predictive_validations": 0,
            "runtime_astrological_promotions": 0,
        })
    if (physical_line_idx, len(records), cursor) != (33, 33, END):
        raise ValueError("Original text line count/boundary not contiguous")
    if len(markup) != 2 or [x["literal_markup"] for x in markup] != ["<poem>", "</poem>"]:
        raise ValueError("Original verse markup incomplete")
    if any(records[i]["source_type"] != "SOURCE_CONTINUED_PREVIOUS_STAR_PROFILE_LINE"
           for i in CONTINUATIONS):
        raise ValueError("Original four wrapped conditional lines misclassified")
    next_heading = "===五财帛==="
    next_quote = next_heading.encode("utf-8")
    records.append({
        "id": "ZWD-R0828", "source": "ZWDS-CLASSIC-01",
        "batch": "ChineseAstro-19SRC-Children",
        "source_type": "NEXT_WEALTH_SECTION_NAVIGATION_ONLY",
        "original_source_group": "WealthSectionNavigation",
        "original_source_revision": 1963110,
        "full_original_Wikitext_SHA256": RAW_SHA,
        "source_original_exact_Chinese_quote": next_heading,
        "quote_SHA256": digest(next_quote),
        "quote_UTF8_bytes": len(next_quote),
        "absolute_codepoint_offset": END,
        "absolute_UTF8_byte_offset": len(s[:END].encode("utf-8")),
        "excerpt_relative_codepoint_offset": END-START,
        "original_Ming_printing_independently_authenticated": False,
        "independent_human_blind_predictive_validations": 0,
        "runtime_astrological_promotions": 0,
    })
    if len(records) != 34 or records[0]["id"] != "ZWD-R0795" or records[-1]["id"] != "ZWD-R0828":
        raise ValueError("Expected source record IDs missing")
    notes = {
        "schema": "CHINESE_V19_ZIWEI_CHILDREN_EXACT_ONLINE_SOURCE_NOT_PREDICTIVE_V1",
        "batch": "ChineseAstro-19SRC-Children",
        "transmitted_source_revision": 1963110,
        "source_full_SHA256": RAW_SHA, "source_full_bytes": len(raw),
        "excerpt_span_codepoints": [START, END],
        "excerpt_SHA256": digest(excerpt.encode("utf-8")),
        "excerpt_UTF8_bytes": len(excerpt.encode("utf-8")),
        "original_verse_markup": markup,
        "original_source_lines_including_heading": 33,
        "source_method_preamble_lines": 4,
        "source_wrapped_continuation_lines": 4,
        "source_star_profile_or_conditional_lines": 24,
        "next_wealth_navigation_only_records": 1,
        "new_source_annotations": 34,
        "first_id": "ZWD-R0795", "last_id": "ZWD-R0828",
        "next_id": "ZWD-R0829", "next_original_section_codepoint": END,
        "source_family_counts_are_not_independent_forecasts": True,
        "historical_fertility_gender_children_mortality_claims_unverified": True,
        "original_Ming_printing_independently_authenticated": False,
        "all_twelve_house_source_sections_completed": False,
        "human_blind_predictive_validations": 0,
        "runtime_astrological_promotions": 0, "records": records,
    }
    file = B / "ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json"
    save(file.name, notes)
    save("SOURCE_CHILDREN_34_EXACT_OFFSET_WITNESS_V1.json", {
        "schema": "CHINESE_V19_ORIGINAL_UTF8_CP_WITNESS",
        "source_full_SHA256": RAW_SHA,
        "source_excerpt_SHA256": notes["excerpt_SHA256"],
        "original_verse_markup": markup,
        "source_excerpt_codepoints": [START, END],
        "source_excerpt_UTF8_bytes": notes["excerpt_UTF8_bytes"],
        "original_quotes": [{
            "id": row["id"], "codepoint": row["absolute_codepoint_offset"],
            "UTF8_byte_offset": row["absolute_UTF8_byte_offset"],
            "quote_SHA256": row["quote_SHA256"],
            "quote_UTF8_bytes": row["quote_UTF8_bytes"]
        } for row in records],
        "blind_human_forecasts": 0,
    })
    save("ACCEPTANCE.json", {
        "batch": "ChineseAstro-19SRC-Children",
        "previous_V18_index_SHA256": V18_SHA,
        "Chinese_before": 1004, "BaZi_retained": 210, "ZiWei_before": 794,
        "new_original_source_notes": 34,
        "Chinese_after_if_accepted": 1038, "ZiWei_after_if_accepted": 828,
        "first_id": "ZWD-R0795", "last_id": "ZWD-R0828", "next_id": "ZWD-R0829",
        "next_BaZi": "BZI-R0211", "original_source_SHA256": RAW_SHA,
        "source_notes_SHA256": digest(file.read_bytes()),
        "source_excerpt_SHA256": notes["excerpt_SHA256"],
        "source_method_lines": 4, "continuation_lines": 4,
        "historical_source_not_human_data": True,
        "human_predictive_validations": 0, "runtime_promotions": 0,
    })
    print(json.dumps({
        "original_lines": 33, "new_documentary_annotations": 34,
        "first": records[0]["id"], "last": records[-1]["id"],
        "next": notes["next_id"], "source_excerpt_sha256": notes["excerpt_SHA256"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    freeze()
