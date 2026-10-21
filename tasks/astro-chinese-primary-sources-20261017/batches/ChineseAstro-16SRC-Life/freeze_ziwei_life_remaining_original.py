#!/usr/bin/env python3
"""Frozen transmitted Zi Wei Life-palace remainder; never human outcomes."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V15.json"
PREV = T / "batches/ChineseAstro-15SRC-Life/ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA = "a5bf0e0cc4bd801b209caa98e1bd58558f2155fd73ba9a055d516472076311ad"
STARS = (
    ("HuoXing","火星","火星，南斗浮星",33783,34079,7),
    ("LingXing","铃星","铃星火",34079,34306,7),
    ("HuoLingCombined","火铃二星","火铃二星入男命吉凶诀",34306,34620,9),
    ("DiJie","地劫","地劫火",34620,34812,6),
    ("TianKong","天空","天空乃空亡之神",34812,35051,8),
    ("JieKongCombined","地劫天空","地劫天空同入限吉凶诀",35051,35156,3),
    ("TianShang","天伤","天伤水",35156,35226,2),
    ("TianShi","天使","天使水",35226,35351,4),
    ("TianMa","天马","天马火",35351,35522,5),
    ("HuaLu","化禄","化禄星土",35522,35758,8),
    ("HuaQuan","化权","化权星木",35758,36108,11),
    ("HuaKe","化科","化科星水",36108,36452,11),
    ("HuaJi","化忌","化忌星水",36452,37047,16),
    ("SuiJun","岁君","岁君火",37047,37202,5),
    ("DouJun","斗君","斗君",37202,37269,2),
)
FLAGS = ("夭","刑夫","克子","娼","淫","杀","殘","残","贫","疾","寿","死","血","丧","灾","祸","灾厄","刑","癫狂","伤")


def hash_bytes(b: bytes) -> str:
    return sha256(b).hexdigest()


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def write(name: str, data: object) -> None:
    (B/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")


def main() -> None:
    raw=RAW.read_bytes()
    assert (len(raw),hash_bytes(raw)) == (106736,RAW_SHA)
    old=read(OLD)
    assert hash_bytes(OLD.read_bytes()) == OLD_SHA and old["sum_source_annotations"] == 850
    assert [(a["accepted_source_annotations"],a["next_id"]) for a in old["systems"]] == [
        (210,"BZI-R0211"),(640,"ZWD-R0641")
    ]
    assert old["accepted_batches"][-1]["id"] == "ChineseAstro-15SRC-Life"
    assert (read(PREV)["next_id"],read(PREV)["next_unstudied_original_codepoint"]) == ("ZWD-R0641",33783)
    west=read(WEST)
    assert west["records_count"] == 13044 and west["batches"][-1]["id"] == "B07bc"
    s=raw.decode("utf-8")
    assert s[37269:37269+len("===二兄弟===")] == "===二兄弟==="
    assert s.index("===二兄弟===",33783) == 37269
    assert sum(x[5] for x in STARS) == 104 and len(STARS) == 15
    assert STARS[0][3] == 33783 and STARS[-1][4] == 37269
    assert all(STARS[i][4] == STARS[i+1][3] for i in range(len(STARS)-1))
    excerpt=s[33783:37269]
    (B/"SOURCE_1963110_LIFE_REMAINING_EXACT_EXCERPT.txt").write_bytes(excerpt.encode("utf-8"))
    records=[]
    sections=[]
    segment_hashes={}
    for tag,native,anchor,start,end,expected in STARS:
        part=s[start:end]
        assert part.startswith(anchor),(tag,part[:40])
        segment_hashes[tag]=hash_bytes(part.encode("utf-8"))
        cursor=start
        count=0
        headings=[]
        poem_markup=[]
        for literal in part.splitlines(keepends=True):
            stripped=literal.strip()
            cp=cursor+(literal.index(stripped) if stripped else 0)
            cursor += len(literal)
            if not stripped:
                continue
            if stripped in ("<poem>","</poem>"):
                poem_markup.append([cp,stripped])
                continue
            encoded=stripped.encode("utf-8")
            bstart=len(s[:cp].encode("utf-8"))
            assert start<=cp<cp+len(stripped)<=end,(tag,cp)
            assert raw[bstart:bstart+len(encoded)]==encoded
            if count==0:
                kind="exact_original_source_group_start"
            elif "吉凶诀" in stripped or "吉凶訣" in stripped or "斷訣" in stripped or "断诀" in stripped:
                kind="exact_original_verse_or_topic_heading"
                headings.append([cp,stripped])
            else:
                kind="exact_historic_narrative_conditional_or_verse"
            records.append({
                "id":f"ZWD-R{641+len(records):04d}",
                "source":"ZWDS-CLASSIC-01","batch":"ChineseAstro-16SRC-Life",
                "original_transmitted_source_oldid":1963110,
                "original_full_source_SHA256":RAW_SHA,
                "original_source_segment":tag,
                "original_source_native_name":native,
                "source_type":kind,
                "source_original_exact_Chinese_Wikitext_quote":stripped,
                "source_quote_UTF8_bytes":len(encoded),
                "source_quote_sha256":hash_bytes(encoded),
                "absolute_codepoint_offset":cp,
                "absolute_UTF8_byte_offset":bstart,
                "excerpt_relative_codepoint_offset":cp-33783,
                "historical_unsafe_social_medical_mortality_terms_present":any(flag in stripped for flag in FLAGS),
                "not_a_scholarly_translation_or_empirical_human_outcome":True,
                "original_Ming_woodblock_imprint_authenticated":False,
                "human_blinded_predictions_validated":0,
                "runtime_astrology_promotions":0,
            })
            count+=1
        assert (count,cursor)==(expected,end),(tag,count,cursor,expected,end)
        sections.append({
            "source_group":tag,"source_group_native":native,
            "original_codepoint_start":start,"original_codepoint_end_exclusive":end,
            "original_source_segment_SHA256":segment_hashes[tag],
            "literal_source_line_count":count,
            "original_verse_topic_headings":headings,
            "original_poem_markup_codepoints":poem_markup,
            "original_birth_record_human_validation":False
        })
    assert len(records)==104
    # Wikitext preserves traditional and simplified Chinese variants within Hua Lu.
    hua=s[35522:35758]
    assert "化禄入命断诀：" in hua
    assert "化祿入限斷訣：" in hua
    # The old source groups 'two stars' jointly; never invent separate natal profiles.
    assert s[34306:34620].startswith("火铃二星入男命吉凶诀")
    assert s[35051:35156].startswith("地劫天空同入限吉凶诀")
    nav="===二兄弟==="
    records.append({
        "id":f"ZWD-R{641+len(records):04d}",
        "source":"ZWDS-CLASSIC-01","batch":"ChineseAstro-16SRC-Life",
        "source_type":"NEXT_ORIGINAL_BROTHERS_SECTION_NAVIGATION_ONLY",
        "original_transmitted_source_oldid":1963110,
        "original_full_source_SHA256":RAW_SHA,
        "original_source_segment":"NEXT_BROTHERS_HEADING",
        "original_source_native_name":"兄弟",
        "source_original_exact_Chinese_Wikitext_quote":nav,
        "source_quote_UTF8_bytes":len(nav.encode("utf-8")),
        "source_quote_sha256":hash_bytes(nav.encode("utf-8")),
        "absolute_codepoint_offset":37269,
        "absolute_UTF8_byte_offset":len(s[:37269].encode("utf-8")),
        "excerpt_relative_codepoint_offset":37269-33783,
        "not_a_scholarly_translation_or_empirical_human_outcome":True,
        "original_Ming_woodblock_imprint_authenticated":False,
        "human_blinded_predictions_validated":0,
        "runtime_astrology_promotions":0,
    })
    assert len(records)==105 and records[0]["id"]=="ZWD-R0641" and records[-1]["id"]=="ZWD-R0745"
    notes={
        "schema":"CHINESE_V16_ZIWEI_LIFE_REMAINING_ONLINE_WIKITEXT_SOURCE_ONLY",
        "status":"ORIGINAL_TRANSMITTED_SOURCE_PROVISIONAL_NOT_EMPIRICAL_OR_NATAL_ENGINE",
        "original_wikitext_oldid":1963110,
        "original_source_full_SHA256":RAW_SHA,
        "original_source_full_bytes":len(raw),
        "original_source_path":RAW.relative_to(ROOT).as_posix(),
        "source_excerpt_path":(B/"SOURCE_1963110_LIFE_REMAINING_EXACT_EXCERPT.txt").relative_to(ROOT).as_posix(),
        "source_excerpt_start_codepoint":33783,
        "source_excerpt_end_codepoint_exclusive":37269,
        "source_excerpt_SHA256":hash_bytes(excerpt.encode("utf-8")),
        "original_next_Brothers_section_codepoint":37269,
        "source_segments":sections,
        "source_segment_original_line_counts":{x["source_group"]:x["literal_source_line_count"] for x in sections},
        "previous_V15_HuoXing_navigation_only_not_substantive":True,
        "all_remaining_online_Life_palace_original_group_lines_through_Brothers_documented":True,
        "critically_collated_ancient_Life_palace_imprint":False,
        "other_11_online_house_sections_studied_completely":False,
        "all_ZiWei_complete_natal_calendar_engine_verified":False,
        "historic_health_mortality_moral_sex_stereotypes_empirically_supported":False,
        "mixed_traditional_simplified_HuaLu_verses_retained":True,
        "combined_HuoLing_and_JieKong_groups_unseparated":True,
        "new_original_source_historical_notes":105,
        "substantive_historical_original_lines":104,
        "following_section_navigation_only":1,
        "first_id":"ZWD-R0641","last_id":"ZWD-R0745",
        "next_id":"ZWD-R0746","next_original_section":"兄弟",
        "next_original_section_codepoint":37269,
        "BaZi_next_original_BZI_R0211_untouched":True,
        "genuine_blinded_real_human_tests":0,
        "runtime_astrological_promotions":0,
        "records":records,
    }
    out=B/"ZIWEI_LIFE_REMAINING_105_SOURCE_NOTES_V1.json"
    write(out.name,notes)
    write("SOURCE_LIFE_REMAINING_105_EXACT_OFFSET_WITNESS_V1.json",{
        "schema":"CHINESE_V16_EXACT_ORIGINAL_UTF8_CODEPOINT_WITNESS",
        "source_full_SHA256":RAW_SHA,"source_excerpt_SHA256":notes["source_excerpt_SHA256"],
        "source_excerpt_start_codepoint":33783,"source_excerpt_end_codepoint_exclusive":37269,
        "original_segment_SHA256":segment_hashes,
        "original_quotes":[{"id":r["id"],"codepoint":r["absolute_codepoint_offset"],
            "UTF8_byte_offset":r["absolute_UTF8_byte_offset"],
            "quote_SHA256":r["source_quote_sha256"],
            "quote_UTF8_bytes":r["source_quote_UTF8_bytes"]} for r in records],
        "human_prediction_test_count":0
    })
    write("ACCEPTANCE.json",{
        "batch":"ChineseAstro-16SRC-Life",
        "previous_source_V15_index_SHA256":OLD_SHA,
        "Chinese_before":850,"BaZi_before_after":210,"ZiWei_before":640,
        "new_original_source_notes":105,
        "Chinese_after_if_accepted":955,"ZiWei_after_if_accepted":745,
        "first_id":"ZWD-R0641","last_id":"ZWD-R0745",
        "next_id":"ZWD-R0746","next_BZI":"BZI-R0211",
        "original_source_groups":[x[1] for x in STARS],
        "source_full_raw_SHA256":RAW_SHA,
        "source_notes_SHA256":hash_bytes(out.read_bytes()),
        "source_excerpt_SHA256":notes["source_excerpt_SHA256"],
        "source_original_life_palace_text_documented_through_Brothers":True,
        "first_Ming_printing_authenticated":False,
        "actual_real_human_predictive_validations":0,
        "runtime_promotions":0
    })
    print(json.dumps({
        "new_original_historical_annotations":len(records),
        "substantive_original_lines":104,"source_sections":len(STARS),
        "first_id":records[0]["id"],"last_id":records[-1]["id"],
        "next_id":notes["next_id"],
        "section_counts":notes["source_segment_original_line_counts"],
        "excerpt_sha256":notes["source_excerpt_SHA256"]
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
