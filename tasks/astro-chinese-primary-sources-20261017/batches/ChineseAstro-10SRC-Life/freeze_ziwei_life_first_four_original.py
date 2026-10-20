#!/usr/bin/env python3
"""Freeze first four complete Zi Wei Life-palace original-source profiles only.

Original oldid1963110 Simplified Chinese Wikisource text, not authenticated
ancient printed edition. Each non-XML, nonblank SOURCE LINE gives ONE
historical source annotation, with exact original raw UTF-8 byte offsets,
not an individually validated predictive event. The previously accepted
Life-palace heading ===一 命宫=== is NOT counted twice.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-chinese-primary-sources-20261017"
ORIGINAL = TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX = TASK / "CHINESE_SOURCE_AUDIT_INDEX_V9.json"
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
ORIGINAL_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
ORIGINAL_BYTES = 106736
INDEX_V9_SHA = "b84922b8614017fb20403f1556a885f2b3d8ed55314566140d67109e4c2022ad"
START_ID = 221
FIRST_SECTION_HEADING = "===一 命宫==="
NEXT_SECTION_HEADING = "===二兄弟==="
STARS = (
    ("ZiWei", "紫微", "紫微土，南北斗化帝座"),
    ("TianJi", "天机", "天机属木，南斗化善星"),
    ("TaiYang", "太阳", "太阳火，南北斗化贵"),
    ("WuQu", "武曲", "武曲金，北斗化财"),
)
NEXT_STAR_START = "天同水，南斗化福"
HISTORIC_HIGH_RISK_WORDS = (
    "夭", "刑夫", "克子", "娼", "淫", "杀", "残疾",
    "贫穷", "疾", "寿", "死", "夫君", "命妇",
)

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def digest(blob):
    return sha256(blob).hexdigest()

def write(path, thing):
    path.write_text(json.dumps(thing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def make():
    original_bytes = ORIGINAL.read_bytes()
    if digest(original_bytes) != ORIGINAL_SHA or len(original_bytes) != ORIGINAL_BYTES:
        raise ValueError("Frozen transmitted original Zi Wei Wikitext SHA/bytes changed")
    full = original_bytes.decode("utf-8")
    old = read(INDEX)
    west = read(WESTERN)
    if digest(INDEX.read_bytes()) != INDEX_V9_SHA:
        raise ValueError("Accepted Chinese V9 index no longer at source frontier")
    if not (
        old["sum_source_annotations"] == 430
        and old["systems"][0]["accepted_source_annotations"] == 210
        and old["systems"][0]["next_id"] == "BZI-R0211"
        and old["systems"][1]["accepted_source_annotations"] == 220
        and old["systems"][1]["next_id"] == "ZWD-R0221"
        and old["accepted_batches"][-1]["id"] == "ChineseAstro-09"
        and old["independently_validated_real_human_claims"] == 0
        and old["runtime_promotions"] == 0
    ):
        raise ValueError("Accepted Chinese V9 source counts / next IDs drift")
    if west["records_count"] != 13044 or west["batches"][-1]["id"] != "B07bc":
        raise ValueError("Separate Western parent snapshot is not exact Chinese-V9 version")
    start = full.index(FIRST_SECTION_HEADING)
    end = full.index(NEXT_STAR_START, start)
    next_section = full.index(NEXT_SECTION_HEADING, end)
    first_star_start = full.index(STARS[0][2], start)
    if (start, first_star_start, end, next_section) != (19953, 19965, 22909, 37269):
        raise ValueError("Original source Life-palace first-four boundaries moved")
    if full.count(FIRST_SECTION_HEADING) != 1 or full.count(NEXT_SECTION_HEADING) != 1:
        raise ValueError("Ambiguous original Chinese Life or Siblings section")
    positions = [full.index(item[2], start, end) for item in STARS]
    if positions != sorted(positions) or len(set(positions)) != 4:
        raise ValueError("Expected four ordered original principal-star entries")
    bounds = positions + [end]
    whole = full[start:end]
    section_path = B / "SOURCE_1963110_LIFE_PALACE_FIRST_FOUR_EXACT_EXCERPT.txt"
    section_path.write_text(whole, encoding="utf-8")
    if digest(section_path.read_bytes()) != digest(whole.encode("utf-8")):
        raise ValueError("Saved original Life-palace excerpt changed")
    records = []
    star_counts = {}
    sections = []
    original_segment_hashes = {}
    for i, (roman, han, marker) in enumerate(STARS):
        section = full[bounds[i]:bounds[i+1]]
        original_segment_hashes[roman] = digest(section.encode("utf-8"))
        cursor = bounds[i]
        current_section = "narrative"
        n_for_star = 0
        palace_lines = []
        for line in section.splitlines(keepends=True):
            stripped = line.strip()
            index_of_stripped = line.index(stripped) if stripped else 0
            abs_start = cursor + index_of_stripped
            cursor += len(line)
            if not stripped or stripped in ("<poem>", "</poem>"):
                continue
            if "入男命吉凶诀：" in stripped:
                current_section = "male_life_poem_heading"
                typ = "historical_poem_heading"
            elif "入女命吉凶诀：" in stripped:
                current_section = "female_life_poem_heading"
                typ = "historical_poem_heading"
            elif "入限吉凶诀：" in stripped:
                current_section = "time_limit_poem_heading"
                typ = "historical_poem_heading"
            elif stripped.startswith(marker):
                current_section = "narrative"
                typ = "star_profile_intro"
            elif stripped.startswith(tuple("子丑寅卯辰巳午未申酉戌亥")) and "宫" in stripped and current_section == "narrative":
                typ = "natal_branch_condition"
                palace_lines.append(stripped)
            elif current_section.endswith("poem_heading"):
                typ = "historical_sex_coded_or_time_poem_verse"
            else:
                typ = "natal_narrative_condition"
            if abs_start < bounds[i] or abs_start+len(stripped) > bounds[i+1]:
                raise ValueError("Original exact verse line outside correct star bounds")
            if full[abs_start:abs_start+len(stripped)] != stripped:
                raise ValueError("Original quote not actually exact substring")
            original_bytes_offset = len(full[:abs_start].encode("utf-8"))
            if original_bytes[original_bytes_offset:original_bytes_offset+len(stripped.encode("utf-8"))] != stripped.encode("utf-8"):
                raise ValueError("Original UTF-8 offset points to different actual source bytes")
            rec = {
                "id":f"ZWD-R{START_ID+len(records):04d}",
                "source":"ZWDS-CLASSIC-01",
                "batch":"ChineseAstro-10SRC-Life",
                "original_full_transmitted_oldid":1963110,
                "original_full_source_sha256":ORIGINAL_SHA,
                "star_group_native":han,
                "star_group_romanization":roman,
                "source_line_type":typ,
                "source_section_context":current_section,
                "exact_original_Chinese_Wikitext_quote":stripped,
                "source_quote_sha256_UTF8":digest(stripped.encode("utf-8")),
                "source_quote_UTF8_bytes":len(stripped.encode("utf-8")),
                "original_absolute_codepoint_offset":abs_start,
                "original_absolute_UTF8_byte_offset":original_bytes_offset,
                "original_excerpt_relative_codepoint_offset":abs_start-start,
                "historical_research_gloss_NOT_exact_translation":(
                    f"Original {han} {current_section} historical line retained verbatim; "
                    "its conditional natal/wealth/body/sex/time claims are not "
                    "empirically verified and require independent expert translation."
                ),
                "contains_historic_high_risk_health_sex_or_morality_words":any(word in stripped for word in HISTORIC_HIGH_RISK_WORDS),
                "source_original_Ming_woodblock_imprint_authenticated":False,
                "independent_human_personality_relationship_or_fate_validation":False,
                "source_14_star_engine_externally_verified_for_this_verse":False,
                "predictions_issued_to_blind_real_people":0,
                "runtime_astrological_rule_promoted":False,
            }
            records.append(rec)
            n_for_star += 1
        if cursor != bounds[i+1]:
            raise ValueError("Original source line cursor gap")
        if n_for_star < 18 or len(palace_lines) < 6:
            raise ValueError("A first-four Zi Wei star description is missing palace/verse lines")
        star_counts[roman] = n_for_star
        sections.append({
            "original_star":han,
            "star_roman":roman,
            "original_codepoint_start":bounds[i],
            "original_codepoint_end_exclusive":bounds[i+1],
            "original_utf8_sha256":digest(section.encode("utf-8")),
            "line_level_source_notes":n_for_star,
            "original_palace_conditional_lines":len(palace_lines),
            "source_full_original_verses_covered":True,
            "historical_expert_claims_predictively_validated":False,
        })
    # Navigation only: next substantive unstudied passage starts with Tian Tong.
    boundary = NEXT_STAR_START
    b_utf8 = boundary.encode("utf-8")
    records.append({
        "id":f"ZWD-R{START_ID+len(records):04d}",
        "source":"ZWDS-CLASSIC-01","batch":"ChineseAstro-10SRC-Life",
        "source_line_type":"NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TIANTONG_CLAIMS",
        "original_full_transmitted_oldid":1963110,
        "original_full_source_sha256":ORIGINAL_SHA,
        "star_group_native":"天同",
        "star_group_romanization":"TianTong",
        "exact_original_Chinese_Wikitext_quote":boundary,
        "source_quote_sha256_UTF8":digest(b_utf8),
        "source_quote_UTF8_bytes":len(b_utf8),
        "original_absolute_codepoint_offset":end,
        "original_absolute_UTF8_byte_offset":len(full[:end].encode("utf-8")),
        "original_excerpt_relative_codepoint_offset":end-start,
        "historical_research_gloss_NOT_exact_translation":"Source boundary only. Tian Tong and all subsequent Life palace passages are NOT examined in this batch.",
        "source_original_Ming_woodblock_imprint_authenticated":False,
        "independent_human_personality_relationship_or_fate_validation":False,
        "source_14_star_engine_externally_verified_for_this_verse":False,
        "predictions_issued_to_blind_real_people":0,
        "runtime_astrological_rule_promoted":False,
    })
    if len(records) != 89 or star_counts != {"ZiWei":22,"TianJi":20,"TaiYang":24,"WuQu":22}:
        raise ValueError(f"Unexpected source count {len(records)} {star_counts}")
    if records[0]["id"] != "ZWD-R0221" or records[-1]["id"] != "ZWD-R0309":
        raise ValueError("Unexpected next Zi Wei source annotation range")
    source_doc = {
        "schema":"CHINESEASTRO_10SRC_ORIGINAL_ZIWEI_FIRST_FOUR_LIFE_PALACE_SOURCE_V1",
        "status":"PROVISIONAL_SOURCE_ONLY_NOT_YET_CANONICAL",
        "source_native_book":"紫微斗數全書 卷二",
        "original_wikitext_revision_oldid":1963110,
        "original_full_Wikitext_path":str(ORIGINAL.relative_to(ROOT)),
        "original_full_Wikitext_SHA256":ORIGINAL_SHA,
        "original_full_UTF8_bytes":ORIGINAL_BYTES,
        "original_source_exact_excerpt_path":str(section_path.relative_to(ROOT)),
        "source_life_palace_heading_already_accepted_as_ZWD_R0220":True,
        "source_original_life_palace_heading_codepoint":start,
        "original_first_ZiWei_profile_codepoint":first_star_start,
        "original_source_span_end_exclusive":end,
        "original_Chinese_siblings_next_section_starts_codepoint":next_section,
        "original_source_excerpt_sha256_UTF8":digest(whole.encode("utf-8")),
        "original_source_excerpt_bytes":len(whole.encode("utf-8")),
        "only_four_of_many_life_palace_stars_covered":True,
        "all_life_palace_section_covered":False,
        "original_14_star_condition_table_critical_verified":False,
        "original_old_Ming_woodblock_source_edition_authenticated":False,
        "earlier_source_body_appearance_health_gender_claims_are_historic_not_medical_truth":True,
        "star_original_sections":sections,
        "star_source_note_counts":star_counts,
        "new_documentary_Chinese_ziwei_source_note_count":len(records),
        "first_id":records[0]["id"],
        "last_id":records[-1]["id"],
        "next_id":"ZWD-R0310",
        "next_unstudied_star_native":"天同",
        "next_star_substantive_codepoint":end,
        "separate_original_bazi_chapter19_and_next_BZI_R0211_unchanged":True,
        "validated_actual_human_chart_predictive_tests":0,
        "production_astrological_rule_promotions":0,
        "records":records,
    }
    write(B/"ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",source_doc)
    witness={
        "schema":"CHINESEASTRO_10SRC_ZWD_OFFSET_WITNESS_V1",
        "original_full_Wikitext_SHA256":ORIGINAL_SHA,
        "original_excerpt_SHA256":source_doc["original_source_excerpt_sha256_UTF8"],
        "original_exact_source_codepoint_range":[start,end],
        "original_verse_star_segment_sha256":original_segment_hashes,
        "exact_source_quote_provenance":[
            {
                "id":r["id"],
                "original_absolute_codepoint_offset":r["original_absolute_codepoint_offset"],
                "original_absolute_UTF8_byte_offset":r["original_absolute_UTF8_byte_offset"],
                "original_quote_sha256":r["source_quote_sha256_UTF8"],
                "original_quote_UTF8_bytes":r["source_quote_UTF8_bytes"]
            } for r in records
        ],
        "early_printed_original_authentication":False,
        "independent_real_human_outcomes":0,
    }
    write(B/"SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json",witness)
    accept={
        "batch":"ChineseAstro-10SRC-Life",
        "previous_accepted_Chineses_source_total":430,
        "previous_BaZi_records":210,
        "previous_ZiWei_records":220,
        "new_historical_ziwei_source_annotations":len(records),
        "Chinese_after_if_accepted":430+len(records),
        "BaZi_after_if_accepted":210,
        "ZiWei_after_if_accepted":220+len(records),
        "source_start_ZWD":records[0]["id"],
        "source_last_ZWD":records[-1]["id"],
        "next_ZWD":"ZWD-R0310",
        "next_BZI":"BZI-R0211",
        "next_star":"天同 TianTong in original Life palace",
        "first_four_profiles_only":True,
        "source_original_verbatim_Wikitext_oldid":1963110,
        "source_original_Wikitext_sha256":ORIGINAL_SHA,
        "accepted_previous_V9_index_sha256":INDEX_V9_SHA,
        "source_notes_sha256":digest((B/"ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json").read_bytes()),
        "source_offset_witness_sha256":digest((B/"SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json").read_bytes()),
        "source_excerpt_sha256":source_doc["original_source_excerpt_sha256_UTF8"],
        "complete_original_Life_palace_source_critical_transcription":False,
        "actual_birth_calendar_star_models_independently_human_validated":False,
        "prospectively_validated_real_human_predictions":0,
        "runtime_promoted_forecasts":0,
    }
    write(B/"ACCEPTANCE.json",accept)
    print(json.dumps({
        "status":"SOURCE_PROVISIONAL_ONLY",
        "first":records[0]["id"],"last":records[-1]["id"],
        "next":"ZWD-R0310","count":len(records),"by_star":star_counts,
        "chinese_if_accepted":accept["Chinese_after_if_accepted"],
        "source_excerpt_sha":source_doc["original_source_excerpt_sha256_UTF8"]
    },ensure_ascii=False,indent=2))

if __name__ == "__main__":
    make()
