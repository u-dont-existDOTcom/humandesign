#!/usr/bin/env python3
"""Freeze *transmitted* Zi Wei Life-palace Lu Cun through Tuo Luo text.

Records exact Chinese lines/offsets without making natal/person predictions.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS = TASK / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PREVIOUS_BATCH = TASK / "batches/ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
PREVIOUS_INDEX_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"
STARS = (
    ("LuCun", "禄存", "禄存土，北斗", 31937, 32457),
    ("KuiYue", "魁钺", "魁钺火", 32457, 32650),
    ("QingYang", "擎羊", "擎羊火金", 32650, 33270),
    ("TuoLuo", "陀罗", "陀罗火金", 33270, 33783),
)
NEXT = ("HuoXing", "火星", "火星，南斗浮星", 33783)
HAZARD_TERMS = ("夭", "刑夫", "克子", "娼", "淫", "杀", "残疾", "贫穷", "疾", "寿", "死", "血", "丧", "灾", "祸")


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def save(name: str, obj: object) -> None:
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze() -> None:
    raw = RAW.read_bytes()
    assert len(raw) == 106736 and digest(raw) == RAW_SHA, "original volume II bytes modified"
    assert digest(PREVIOUS.read_bytes()) == PREVIOUS_INDEX_SHA, "V14 canonical source snapshot changed"
    idx = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    assert idx["sum_source_annotations"] == 796
    assert [(s["accepted_source_annotations"], s["next_id"]) for s in idx["systems"]] == [
        (210, "BZI-R0211"), (586, "ZWD-R0587")
    ]
    assert idx["accepted_batches"][-1]["id"] == "ChineseAstro-14SRC-Life"
    prev = json.loads(PREVIOUS_BATCH.read_text(encoding="utf-8"))
    assert prev["next_id"] == "ZWD-R0587" and prev["next_unstudied_original_codepoint"] == 31937
    west = json.loads(WEST.read_text(encoding="utf-8"))
    assert west["records_count"] == 13044 and west["batches"][-1]["id"] == "B07bc"
    s = raw.decode("utf-8")
    assert s.index("===二兄弟===", 31937) == 37269
    assert all(s[a:a + len(anchor)] == anchor for _, _, anchor, a, _ in STARS)
    assert s[NEXT[3]:NEXT[3] + len(NEXT[2])] == NEXT[2]
    assert STARS[0][3] == 31937 and STARS[-1][4] == NEXT[3]
    assert all(STARS[j][4] == STARS[j + 1][3] for j in range(len(STARS) - 1))

    excerpt = s[STARS[0][3]:NEXT[3]]
    (B / "SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt").write_bytes(excerpt.encode("utf-8"))
    records: list[dict] = []
    sections: list[dict] = []
    segment_hashes: dict[str, str] = {}
    for roman, chinese, anchor, start, end in STARS:
        part = s[start:end]
        segment_hashes[roman] = digest(part.encode("utf-8"))
        cursor = start
        headings = []
        raw_line_count = 0
        structural_markup = []
        grade_phrases = []
        for raw_line in part.splitlines(keepends=True):
            stripped = raw_line.strip()
            cp = cursor + (raw_line.index(stripped) if stripped else 0)
            cursor += len(raw_line)
            if not stripped:
                continue
            if stripped in ("<poem>", "</poem>"):
                structural_markup.append([cp, stripped])
                continue
            context = "historical_source_narrative_or_verse"
            if stripped.startswith(anchor):
                context = "source_star_profile_start"
            elif "吉凶诀：" in stripped or "斷訣：" in stripped:
                context = "verbatim_heading"
                headings.append([cp, stripped])
            elif ("入庙" in stripped or "陷地" in stripped) and len(stripped) < 40:
                context = "source_grade_or_palace_location_text"
                grade_phrases.append([cp, stripped])
            if roman == "QingYang" and stripped == "擎羊入男命吉凶诀：" and len([h for h in headings if h[1] == stripped]) == 2:
                context = "source_duplicate_male_heading_followed_by_time_limit_verses"
            encoded = stripped.encode("utf-8")
            byte = len(s[:cp].encode("utf-8"))
            assert s[cp:cp + len(stripped)] == stripped
            assert raw[byte:byte + len(encoded)] == encoded
            assert start <= cp < cp + len(stripped) <= end
            records.append({
                "id": f"ZWD-R{587 + len(records):04d}",
                "source": "ZWDS-CLASSIC-01",
                "batch": "ChineseAstro-15SRC-Life",
                "original_transmitted_source_oldid": 1963110,
                "original_full_source_SHA256": RAW_SHA,
                "star_roman": roman,
                "star_native": chinese,
                "source_type": context,
                "source_original_exact_Chinese_Wikitext_quote": stripped,
                "source_quote_UTF8_bytes": len(encoded),
                "source_quote_sha256": digest(encoded),
                "absolute_codepoint_offset": cp,
                "absolute_UTF8_byte_offset": byte,
                "excerpt_relative_codepoint_offset": cp - STARS[0][3],
                "not_exact_scholarly_translation": "Original transmitted Chinese line; historical claims only, not verified traits, legal outcomes, medical conclusions or life events.",
                "mentions_historic_health_sex_morality_or_mortality": any(w in stripped for w in HAZARD_TERMS),
                "original_Ming_woodblock_imprint_authenticated": False,
                "genuine_human_predictions_validated": 0,
                "runtime_astrology_promotions": 0,
            })
            raw_line_count += 1
        assert cursor == end
        sections.append({
            "star_roman": roman, "star_native": chinese,
            "original_codepoint_start": start, "original_codepoint_end_exclusive": end,
            "original_source_segment_SHA256": segment_hashes[roman],
            "literal_source_line_count": raw_line_count,
            "original_verbatim_headings": headings,
            "source_grade_or_palace_location_phrases": grade_phrases,
            "poem_markup_exact_offsets": structural_markup,
            "no_missing_or_synthesized_gender_verse": True,
            "original_birth_record_human_validation": False,
        })

    # IMPORTANT: source prints a second male-life Qing Yang heading despite limit-oriented lines.
    qy = next(x for x in sections if x["star_roman"] == "QingYang")
    assert [h[1] for h in qy["original_verbatim_headings"]].count("擎羊入男命吉凶诀：") == 2
    assert not any("入限吉凶诀" in h[1] for h in qy["original_verbatim_headings"])
    # Tuo Luo has a female verse but no opening poem tag at that exact location.
    tl = next(x for x in sections if x["star_roman"] == "TuoLuo")
    female_cp = next(cp for cp, label in tl["original_verbatim_headings"] if label.startswith("陀罗入女命"))
    assert "<poem>" not in s[female_cp:s.index("陀罗入限", female_cp)]
    # Kui Yue has a single combined sex-neutral source heading, not three modern ones.
    ky = next(x for x in sections if x["star_roman"] == "KuiYue")
    assert len(ky["original_verbatim_headings"]) == 1

    nav = NEXT[2]
    enc = nav.encode("utf-8")
    records.append({
        "id": f"ZWD-R{587 + len(records):04d}", "source": "ZWDS-CLASSIC-01",
        "batch": "ChineseAstro-15SRC-Life",
        "source_type": "NEXT_HUOXING_SOURCE_NAVIGATION_ONLY",
        "original_transmitted_source_oldid": 1963110,
        "original_full_source_SHA256": RAW_SHA,
        "star_roman": NEXT[0], "star_native": NEXT[1],
        "source_original_exact_Chinese_Wikitext_quote": nav,
        "source_quote_UTF8_bytes": len(enc),
        "source_quote_sha256": digest(enc),
        "absolute_codepoint_offset": NEXT[3],
        "absolute_UTF8_byte_offset": len(s[:NEXT[3]].encode("utf-8")),
        "excerpt_relative_codepoint_offset": NEXT[3] - STARS[0][3],
        "not_exact_scholarly_translation": "Navigation marker only: Huo Xing substantive profile remains unread for V15.",
        "original_Ming_woodblock_imprint_authenticated": False,
        "genuine_human_predictions_validated": 0,
        "runtime_astrology_promotions": 0,
    })
    assert records[0]["id"] == "ZWD-R0587"
    assert len({r["id"] for r in records}) == len(records)
    notes = {
        "schema": "CHINESE_V15_ZIWEI_LIFE_AUXILIARY_SECOND_FOUR_SOURCE_ONLY_V1",
        "status": "SOURCE_PROVISIONAL_NOT_A_NATAL_CALCULATOR",
        "original_wikitext_oldid": 1963110,
        "original_source_full_SHA256": RAW_SHA, "original_source_full_bytes": len(raw),
        "original_source_path": str(RAW.relative_to(ROOT)),
        "source_excerpt_path": str((B / "SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt").relative_to(ROOT)),
        "source_excerpt_start_codepoint": STARS[0][3], "source_excerpt_end_codepoint_exclusive": NEXT[3],
        "source_excerpt_SHA256": digest(excerpt.encode("utf-8")),
        "original_Brothers_next_section_codepoint": 37269,
        "star_sections": sections, "source_star_line_counts": {s["star_roman"]: s["literal_source_line_count"] for s in sections},
        "previous_V14_LuCun_navigation_only_not_substantive": True,
        "four_new_auxiliary_profiles_source_covered": True,
        "auxiliary_source_incomplete_after_HuoXing": True,
        "QingYang_duplicate_original_male_verse_heading_preserved": True,
        "TuoLuo_female_verse_markup_gap_preserved": True,
        "KuiYue_absent_dedicated_male_female_time_headings_preserved": True,
        "original_Ming_woodblock_imprint_verified": False,
        "historical_health_mortality_moral_gender_statements_empirical": False,
        "original_full_Life_palace_text_completed": False,
        "new_original_source_historical_notes": len(records),
        "first_id": records[0]["id"], "last_id": records[-1]["id"],
        "next_id": f"ZWD-R{587 + len(records):04d}",
        "next_unstudied_star": NEXT[1], "next_unstudied_original_codepoint": NEXT[3],
        "BaZi_next_original_BZI_R0211_untouched": True,
        "genuine_blinded_real_human_tests": 0, "runtime_astrological_promotions": 0,
        "records": records,
    }
    out = B / "ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
    save(out.name, notes)
    save("SOURCE_LIFE_SECOND_FOUR_AUXILIARY_EXACT_OFFSET_WITNESS_V1.json", {
        "schema": "CHINESE_V15_EXACT_SOURCE_UTF8_BYTE_OFFSET_WITNESS",
        "full_original_source_SHA256": RAW_SHA,
        "excerpt_SHA256": notes["source_excerpt_SHA256"],
        "excerpt_codepoint_range": [STARS[0][3], NEXT[3]],
        "star_segment_SHA256": segment_hashes,
        "original_quotes": [{
            "id": r["id"], "codepoint": r["absolute_codepoint_offset"],
            "UTF8_byte_offset": r["absolute_UTF8_byte_offset"],
            "quote_SHA256": r["source_quote_sha256"], "quote_UTF8_bytes": r["source_quote_UTF8_bytes"],
        } for r in records],
        "human_prediction_test_count": 0,
    })
    save("ACCEPTANCE.json", {
        "batch": "ChineseAstro-15SRC-Life",
        "previous_source_V14_index_SHA256": PREVIOUS_INDEX_SHA,
        "Chinese_before": 796, "BaZi_before_after": 210, "ZiWei_before": 586,
        "new_original_source_notes": len(records),
        "Chinese_after_if_accepted": 796 + len(records), "ZiWei_after_if_accepted": 586 + len(records),
        "first_id": records[0]["id"], "last_id": records[-1]["id"],
        "next_id": notes["next_id"], "next_BZI": "BZI-R0211",
        "source_stars_native": [a[1] for a in STARS], "source_next_star_native": NEXT[1],
        "source_full_raw_SHA256": RAW_SHA, "source_notes_SHA256": digest(out.read_bytes()),
        "source_excerpt_SHA256": notes["source_excerpt_SHA256"],
        "original_full_auxiliary_and_Life_section_finished": False,
        "actual_real_human_predictive_validations": 0, "runtime_promotions": 0,
    })
    print(json.dumps({
        "new_source_only_notes": len(records), "first_id": records[0]["id"], "last_id": records[-1]["id"],
        "next_id": notes["next_id"], "per_star": notes["source_star_line_counts"],
        "excerpt_sha256": notes["source_excerpt_SHA256"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    freeze()
