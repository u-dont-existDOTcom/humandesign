#!/usr/bin/env python3
"""Freeze exact transmitted Zi Wei Disease-palace source, not clinical predictions."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
SOURCE = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V20.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V20_SHA = "a6b051ed03f19f663d5a363af9a5c4efbf2ca2aea4997e94920023fdcf32f9b5"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
START, END = 41672, 42541
GROUPS = {
    2: "ZiWei", 3: "TianJi", 4: "TaiYang", 5: "WuQu",
    6: "TianTong", 7: "LianZhen", 8: "TianFu", 9: "TaiYin",
    10: "TaiYin", 11: "JuMen", 12: "TianXiang", 13: "QiSha",
    14: "PoJun", 15: "WenChang", 16: "WenQu", 17: "ZuoFu",
    18: "YouBi", 19: "LuCun", 20: "TuoLuo", 21: "QingYang",
    22: "YangLing", 23: "DouJun",
}
TERM_FLAGS = ("疾", "灾", "伤", "病", "死", "寿", "血", "疯", "残", "刑", "夭", "脓", "疮")


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def write(name: str, obj: object) -> None:
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze() -> None:
    raw = SOURCE.read_bytes()
    if (len(raw), digest(raw)) != (106736, SOURCE_SHA):
        raise ValueError("Original Wikitext full SHA/length drift")
    if digest(OLD.read_bytes()) != V20_SHA or digest(WEST.read_bytes()) != WEST_SHA:
        raise ValueError("Previously accepted Chinese or separate older Western index changed")
    old = load(OLD)
    if old["sum_source_annotations"] != 1069 or [
        (x["accepted_source_annotations"], x["next_id"]) for x in old["systems"]
    ] != [(210, "BZI-R0211"), (859, "ZWD-R0860")]:
        raise ValueError("Expected accepted source frontier not found")
    if old["accepted_batches"][-1]["id"] != "ChineseAstro-20SRC-Wealth":
        raise ValueError("Old Chinese index batch changed")
    text = raw.decode("utf-8")
    if len(text) != 48890:
        raise ValueError("Full Wikitext codepoint length not expected")
    if not text[START:].startswith("===六疾厄===") or not text[END:].startswith("===七迁移==="):
        raise ValueError("Disease and next Travel boundaries drift")
    if text.index("===七迁移===", START) != END:
        raise ValueError("Unexpected intervening source heading")
    excerpt = text[START:END]
    excerpt_file = B / "SOURCE_1963110_DISEASE_EXACT_EXCERPT.txt"
    excerpt_file.write_bytes(excerpt.encode("utf-8"))
    cursor = START
    line_number = 0
    records = []
    tags = []
    for literal in excerpt.splitlines(keepends=True):
        q = literal.strip()
        cp = cursor + (literal.index(q) if q else 0)
        cursor += len(literal)
        if not q:
            continue
        if q in ("<poem>", "</poem>"):
            tags.append([cp, q])
            continue
        if line_number == 0:
            role, group = "SOURCE_SECTION_HEADING", "Disease"
        elif line_number == 1:
            role, group = "SOURCE_GENERAL_METHOD_PREAMBLE", "GeneralDiseaseMethod"
        elif line_number == 10:
            role, group = "SOURCE_CONTINUATION_PRIOR_TAIYIN_PROFILE", "TaiYin"
        elif line_number in GROUPS:
            role, group = "SOURCE_HISTORICAL_STAR_CONDITION", GROUPS[line_number]
        else:
            raise ValueError(f"Unclassified source line {line_number}")
        encoded = q.encode("utf-8")
        bp = len(text[:cp].encode("utf-8"))
        if (text[cp:cp + len(q)] != q or raw[bp:bp + len(encoded)] != encoded
                or not START <= cp < cp + len(q) <= END):
            raise ValueError("Original line SHA/Unicode source window failure")
        records.append({
            "id": f"ZWD-R{860 + len(records):04d}",
            "source": "ZWDS-CLASSIC-01",
            "batch": "ChineseAstro-21SRC-Disease",
            "source_oldid": 1963110,
            "original_full_Wikitext_SHA256": SOURCE_SHA,
            "source_kind": role,
            "source_historical_star_group": group,
            "original_line_number": line_number,
            "source_original_exact_Chinese_Wikitext_quote": q,
            "source_quote_SHA256": digest(encoded),
            "source_quote_UTF8_bytes": len(encoded),
            "absolute_codepoint_offset": cp,
            "absolute_UTF8_byte_offset": bp,
            "excerpt_relative_codepoint_offset": cp - START,
            "historic_illness_disability_mortality_claims": any(term in q for term in TERM_FLAGS),
            "historic_text_ambiguous_yangling_glyph": "羊铃" in q,
            "modern_health_medical_prediction_allowed": False,
            "independently_authenticated_Ming_print": False,
            "real_human_predictions_validated": 0,
            "runtime_astrology_promotions": 0,
        })
        line_number += 1
    if (line_number, cursor, len(records)) != (24, END, 24):
        raise ValueError("Original physical source line or end count wrong")
    if [x[1] for x in tags] != ["<poem>", "</poem>"]:
        raise ValueError("Original verse delimiters absent")
    if (records[10]["source_historical_star_group"],
            records[10]["source_kind"]) != ("TaiYin", "SOURCE_CONTINUATION_PRIOR_TAIYIN_PROFILE"):
        raise ValueError("Source continuation misclassified")
    if sum("羊铃" in r["source_original_exact_Chinese_Wikitext_quote"] for r in records) != 2:
        raise ValueError("Both original '羊铃' appearances must be preserved")
    nxt = "===七迁移==="
    records.append({
        "id": "ZWD-R0884",
        "source": "ZWDS-CLASSIC-01",
        "batch": "ChineseAstro-21SRC-Disease",
        "source_oldid": 1963110,
        "original_full_Wikitext_SHA256": SOURCE_SHA,
        "source_kind": "NEXT_TRAVEL_PALACE_NAVIGATION_ONLY",
        "source_historical_star_group": "TravelNextHeading",
        "source_original_exact_Chinese_Wikitext_quote": nxt,
        "source_quote_SHA256": digest(nxt.encode("utf-8")),
        "source_quote_UTF8_bytes": len(nxt.encode("utf-8")),
        "absolute_codepoint_offset": END,
        "absolute_UTF8_byte_offset": len(text[:END].encode("utf-8")),
        "excerpt_relative_codepoint_offset": END-START,
        "modern_health_medical_prediction_allowed": False,
        "independently_authenticated_Ming_print": False,
        "real_human_predictions_validated": 0,
        "runtime_astrology_promotions": 0,
    })
    if len(records) != 25 or records[0]["id"] != "ZWD-R0860" or records[-1]["id"] != "ZWD-R0884":
        raise ValueError("Original source ID boundary failure")
    doc = {
        "schema": "CHINESE_V21_ZIWEI_DISEASE_ORIGINAL_WIKITEXT_DOCUMENTATION_ONLY",
        "batch": "ChineseAstro-21SRC-Disease",
        "source_online_oldid": 1963110,
        "original_full_Wikitext_SHA256": SOURCE_SHA,
        "source_excerpt_codepoints": [START, END],
        "source_excerpt_SHA256": digest(excerpt.encode("utf-8")),
        "source_excerpt_UTF8_bytes": len(excerpt.encode("utf-8")),
        "source_original_poem_markup": tags,
        "source_nonblank_nonmarkup_physical_lines": 24,
        "source_method_preamble_lines": 1,
        "source_wrapped_continuation_lines": 1,
        "source_historical_star_condition_lines": 21,
        "following_navigation_records": 1,
        "new_source_only_notes": 25,
        "first_id": "ZWD-R0860", "last_id": "ZWD-R0884",
        "next_id": "ZWD-R0885", "next_original_source_cp": END,
        "yangling_variant_preserved_not_emended": True,
        "yangling_literal_occurrences": 2,
        "same_glyph_apparent_context_dependent_adverse_vs_favorable_tension_unresolved": True,
        "historic_health_claims_not_medical_advice_or_diagnosis": True,
        "authentic_original_Ming_woodblock_collated": False,
        "complete_twelve_palace_source_collation": False,
        "human_blind_predictions_validated": 0,
        "runtime_astrology_promotions": 0,
        "records": records,
    }
    frozen = B / "ZIWEI_DISEASE_25_SOURCE_NOTES_V1.json"
    write(frozen.name, doc)
    witness = {
        "schema": "CHINESE_V21_DISEASE_EXACT_SOURCE_WITNESS",
        "original_full_Wikitext_SHA256": SOURCE_SHA,
        "source_excerpt_SHA256": doc["source_excerpt_SHA256"],
        "source_excerpt_cp_range": [START, END],
        "source_poem_markup": tags,
        "source_quotes": [
            {
                "id": r["id"],
                "original_cp": r["absolute_codepoint_offset"],
                "original_utf8_offset": r["absolute_UTF8_byte_offset"],
                "quote_sha256": r["source_quote_SHA256"],
                "quote_utf8_bytes": r["source_quote_UTF8_bytes"],
            } for r in records
        ],
        "human_blind_predictive_validations": 0,
    }
    write("SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json", witness)
    write("ACCEPTANCE.json", {
        "batch": "ChineseAstro-21SRC-Disease",
        "old_V20_index_SHA256": V20_SHA,
        "old_Chinese_total": 1069,
        "old_BaZi": 210, "old_ZiWei": 859,
        "new_original_source_only_notes": 25,
        "new_Chinese_total_if_accepted": 1094,
        "new_ZiWei_total_if_accepted": 884,
        "first": "ZWD-R0860", "last": "ZWD-R0884", "next": "ZWD-R0885",
        "next_BaZi": "BZI-R0211",
        "original_source_sha256": SOURCE_SHA,
        "new_source_notes_sha256": digest(frozen.read_bytes()),
        "source_witness_sha256": digest((B/"SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json").read_bytes()),
        "source_excerpt_sha256": doc["source_excerpt_SHA256"],
        "original_witness_not_authenticated_woodblock": True,
        "real_human_blind_predictions": 0, "runtime_promotions": 0,
    })
    print(json.dumps({"records":len(records),"first":records[0]["id"],
        "last":records[-1]["id"],"next":doc["next_id"],
        "excerpt_sha256":doc["source_excerpt_SHA256"]}, ensure_ascii=False,indent=2))


if __name__ == "__main__":
    freeze()
