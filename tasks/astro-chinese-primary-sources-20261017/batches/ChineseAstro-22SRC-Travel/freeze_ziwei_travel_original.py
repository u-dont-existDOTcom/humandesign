#!/usr/bin/env python3
"""Record original transmitted Chinese Zi Wei Travel text without making predictions."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V21.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA = "0b22a13f164891fa60be0b8630aa6ed131cf27f425ad492557a9d814d7375c03"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
START, END = 42541, 43499
GROUPS = [
    "ZiWei", "TianJi", "TaiYang", "WuQu", "TianTong", "LianZhen",
    "TianFu", "TaiYin", "TanLang", "JuMen", "TianXiang", "TianLiang",
    "QiSha", "PoJun", "WenChang", "WenQu", "ZuoFu", "YouBi",
    "LuCun", "QingYang", "TuoLuo", "HuoXing", "LingXing", "DouJun"
]


def hash_bytes(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze() -> None:
    raw = RAW.read_bytes()
    if (len(raw), hash_bytes(raw)) != (106736, SOURCE_SHA):
        raise ValueError("Full original online Wikitext byte identity changed")
    if hash_bytes(OLD.read_bytes()) != OLD_SHA or hash_bytes(WEST.read_bytes()) != WEST_SHA:
        raise ValueError("Prior Chinese V21 or old Western inherited source differs")
    prev = read(OLD)
    if prev["sum_source_annotations"] != 1094 or [
        (x["accepted_source_annotations"], x["next_id"]) for x in prev["systems"]
    ] != [(210, "BZI-R0211"), (884, "ZWD-R0885")]:
        raise ValueError("Not at accepted Chinese V21 original source frontier")
    if prev["accepted_batches"][-1]["id"] != "ChineseAstro-21SRC-Disease":
        raise ValueError("V21 batch source not accepted")
    s = raw.decode("utf-8")
    if not s[START:].startswith("===七迁移===") or not s[END:].startswith("===八奴仆==="):
        raise ValueError("Travel/Servants source heading moved")
    if s.index("===八奴仆===", START) != END:
        raise ValueError("Source section boundary changed")
    excerpt = s[START:END]
    path = B / "SOURCE_1963110_TRAVEL_EXACT_EXCERPT.txt"
    path.write_bytes(excerpt.encode("utf-8"))
    cp = START
    records = []
    tags = []
    line_no = 0
    for line in excerpt.splitlines(keepends=True):
        txt = line.strip()
        start = cp + (line.index(txt) if txt else 0)
        cp += len(line)
        if not txt:
            continue
        if txt in ("<poem>", "</poem>"):
            tags.append([start, txt])
            continue
        if line_no == 0:
            group, role = "Travel", "SOURCE_TRAVEL_PALACE_HEADING"
        elif 1 <= line_no <= 24:
            group, role = GROUPS[line_no-1], "ORIGINAL_HISTORICAL_STAR_OR_COMBINATION_CLAUSE"
        else:
            raise ValueError("Travel line extra unexpectedly")
        q = txt.encode("utf-8")
        byte = len(s[:start].encode("utf-8"))
        if (not START <= start < start + len(txt) <= END or
            s[start:start+len(txt)] != txt or
            raw[byte:byte+len(q)] != q):
            raise ValueError("Source line Unicode/UTF8 offset mismatch")
        records.append({
            "id": f"ZWD-R{885+len(records):04d}", "source": "ZWDS-CLASSIC-01",
            "batch": "ChineseAstro-22SRC-Travel", "transmitted_source_oldid": 1963110,
            "full_original_Wikitext_SHA256": SOURCE_SHA,
            "source_kind": role, "historical_source_group": group,
            "physical_line_number": line_no,
            "original_exact_Chinese_Wikitext_quote": txt,
            "quote_SHA256": hash_bytes(q), "quote_UTF8_bytes": len(q),
            "original_codepoint_offset": start, "original_UTF8_byte_offset": byte,
            "relative_excerpt_codepoint_offset": start-START,
            "suspicious_fuchi_segment": "贵人扶，持同" in txt,
            "taiyin_self_conjunction_source_ambiguous": group == "TaiYin" and "太阴同" in txt,
            "Ming_woodblock_imprint_authenticated": False,
            "real_person_travel_outcomes_predictively_verified": False,
            "human_blind_predictions_validated": 0, "runtime_rule_promotions": 0,
        })
        line_no += 1
    if len(records) != 25 or cp != END or len(tags) != 2:
        raise ValueError("Original Travel physical lines/markup/boundaries missing")
    if [t[1] for t in tags] != ["<poem>", "</poem>"]:
        raise ValueError("Original physical Wikitext poem tags missing")
    if [r["physical_line_number"] for r in records] != list(range(25)):
        raise ValueError("Physical original source lines do not match exact section")
    if sum(r["suspicious_fuchi_segment"] for r in records) != 1:
        raise ValueError("Source clause punctuation error not retained")
    if sum(r["taiyin_self_conjunction_source_ambiguous"] for r in records) != 1:
        raise ValueError("Source TaiYin self-name condition not retained")
    nxt = "===八奴仆==="
    records.append({
        "id": "ZWD-R0910", "source": "ZWDS-CLASSIC-01",
        "batch": "ChineseAstro-22SRC-Travel",
        "transmitted_source_oldid": 1963110,
        "full_original_Wikitext_SHA256": SOURCE_SHA,
        "source_kind": "NEXT_SERVANTS_SOURCE_NAVIGATION_ONLY",
        "historical_source_group": "Servants",
        "original_exact_Chinese_Wikitext_quote": nxt,
        "quote_SHA256": hash_bytes(nxt.encode("utf-8")),
        "quote_UTF8_bytes": len(nxt.encode("utf-8")),
        "original_codepoint_offset": END,
        "original_UTF8_byte_offset": len(s[:END].encode("utf-8")),
        "relative_excerpt_codepoint_offset": END-START,
        "Ming_woodblock_imprint_authenticated": False,
        "real_person_travel_outcomes_predictively_verified": False,
        "human_blind_predictions_validated": 0, "runtime_rule_promotions": 0,
    })
    if len(records) != 26 or records[0]["id"] != "ZWD-R0885" or records[-1]["id"] != "ZWD-R0910":
        raise ValueError("Exact record ID frontier does not match")
    frozen = {
        "schema": "ZIWEI_V22_TRAVEL_ORIGINAL_ONLINE_SOURCE_DOCUMENTARY_ONLY_V1",
        "batch": "ChineseAstro-22SRC-Travel", "source_oldid": 1963110,
        "full_original_Wikitext_SHA256": SOURCE_SHA,
        "source_excerpt_codepoint_range": [START, END],
        "source_excerpt_sha256": hash_bytes(excerpt.encode("utf-8")),
        "source_excerpt_UTF8_bytes": len(excerpt.encode("utf-8")),
        "original_poem_markup": tags, "source_nonmarkup_lines_including_heading": 25,
        "historical_main_or_combined_star_lines": 24,
        "next_section_navigation_only": 1,
        "source_punctuation_fuchi_ambiguity_unresolved": True,
        "source_taiyin_self_reference_ambiguity_unresolved": True,
        "new_documentary_source_records": 26,
        "first_id": "ZWD-R0885", "last_id": "ZWD-R0910",
        "next_id": "ZWD-R0911", "next_source_cp": END,
        "original_printed_woodblock_authenticated": False,
        "travel_law_migration_or_finance_advice_authorized": False,
        "real_human_blind_forecasts_validated": 0,"runtime_astrology_promotions":0,
        "records": records,
    }
    out = B / "ZIWEI_TRAVEL_26_SOURCE_NOTES_V1.json"
    save(out, frozen)
    witness = {
        "schema": "ZIWEI_V22_TRAVEL_LITERAL_CP_UTF8_SHA_WITNESS_V1",
        "source_full_SHA256": SOURCE_SHA,
        "source_excerpt_SHA256": frozen["source_excerpt_sha256"],
        "source_excerpt_codepoint_interval": [START, END],
        "original_poem_markup": tags,
        "quote_witnesses": [
            {"id": r["id"],"cp":r["original_codepoint_offset"],
             "UTF8_offset":r["original_UTF8_byte_offset"],
             "quote_SHA256":r["quote_SHA256"],
             "quote_UTF8_bytes":r["quote_UTF8_bytes"]} for r in records
        ],
        "verified_person_predictions": 0,
    }
    w = B / "SOURCE_TRAVEL_26_EXACT_OFFSET_WITNESS_V1.json"
    save(w, witness)
    save(B / "ACCEPTANCE.json", {
        "batch": "ChineseAstro-22SRC-Travel",
        "prior_index_V21_SHA256": OLD_SHA, "Chinese_before": 1094,
        "BaZi_retained": 210, "ZiWei_before": 884,
        "new_source_documentary_annotations": 26,
        "Chinese_after_if_accepted": 1120,
        "ZiWei_after_if_accepted": 910,
        "first_id":"ZWD-R0885","last_id":"ZWD-R0910",
        "next_id":"ZWD-R0911","next_BaZi":"BZI-R0211",
        "source_notes_SHA256":hash_bytes(out.read_bytes()),
        "source_witness_SHA256":hash_bytes(w.read_bytes()),
        "source_excerpt_SHA256":frozen["source_excerpt_sha256"],
        "original_full_Wikitext_SHA256":SOURCE_SHA,
        "actual_blinded_human_predictions":0,"runtime_rule_promotions":0,
    })
    print(json.dumps({"original_lines":25,"source_only_notes":len(records),
        "first":records[0]["id"],"last":records[-1]["id"],
        "next":frozen["next_id"],"excerpt_sha":frozen["source_excerpt_sha256"]},
        ensure_ascii=False,indent=2))


if __name__ == "__main__":
    freeze()
