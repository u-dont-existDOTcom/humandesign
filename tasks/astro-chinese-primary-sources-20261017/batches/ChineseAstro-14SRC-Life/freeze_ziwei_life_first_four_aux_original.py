#!/usr/bin/env python3
"""Zi Wei Life-palace first four auxiliary star ORIGINAL text, no human evidence.

Wen Chang, Wen Qu, Zuo Fu, You Bi source-only original oldid1963110.
No assumption every star needs grade rows or a female-verse heading.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
FULL=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
LAST=T/"batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
ORIGINAL_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V13_SHA="4695dea848caacac65f4cd9d0baebf1a85a26b022ba8414b83aecc6ca5c13682"
STARS=(
    ("WenChang","文昌","文昌金，南北斗",30135,30665,16,4,True),
    ("WenQu","文曲","文曲水，北斗",30665,31212,18,4,True),
    ("ZuoFu","左辅","左辅土，南北斗",31212,31613,13,0,True),
    ("YouBi","右弼","右弼水，南北斗",31613,31937,10,0,False),
)
NEXT_STAR=("LuCun","禄存","禄存土，北斗",31937)
TERM_FLAGS=("夭","刑夫","克子","娼","淫","杀","残疾","贫穷","疾","寿","死","夫君","命妇","伤残","血")
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def hash_bytes(b):return sha256(b).hexdigest()
def write(p,r):p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def make():
    raw=FULL.read_bytes()
    if len(raw)!=106736 or hash_bytes(raw)!=ORIGINAL_SHA:
        raise ValueError("Original Zi Wei source Wikitext raw SHA/bytes changed")
    s=raw.decode("utf-8")
    index=load(OLD);prior=load(LAST);west=load(WEST)
    if hash_bytes(OLD.read_bytes())!=V13_SHA:
        raise ValueError("Accepted original source V13 index SHA wrong")
    if index["sum_source_annotations"]!=738 or [(a["accepted_source_annotations"],a["next_id"]) for a in index["systems"]] != [
        (210,"BZI-R0211"),(528,"ZWD-R0529")
    ] or index["accepted_batches"][-1]["id"]!="ChineseAstro-13SRC-Life":
        raise ValueError("Expected accepted Chinese source index V13 missing")
    if west["records_count"]!=13044 or west["batches"][-1]["id"]!="B07bc":
        raise ValueError("Parallel old Western parent snapshot changed")
    if (prior["last_id"],prior["next_id"],prior["next_unstudied_star_original_codepoint"])!=(
        "ZWD-R0528","ZWD-R0529",30135
    ):
        raise ValueError("Previously accepted source Wen Chang marker not at expected boundary")
    if (s.index("===二兄弟===",31937),s.find("禄存土，北斗",31000))!=(37269,31937):
        raise ValueError("Original Life-palace auxiliary star/source boundaries changed")
    for name,cn,anchor,start,end,count,grade,has_female in STARS:
        if s[start:start+len(anchor)]!=anchor or s.find(anchor,start+1,end)!=-1:
            raise ValueError("Original source auxiliary star anchor moved/duplicated")
    start=STARS[0][3];end=NEXT_STAR[3]
    excerpt=s[start:end]
    excerpt_file=B/"SOURCE_1963110_LIFE_FIRST_FOUR_AUX_EXACT_EXCERPT.txt"
    excerpt_file.write_bytes(excerpt.encode("utf-8"))
    sections=[];records=[];segment_shas={}
    for roman,cn,anchor,a,b,expected_count,expected_grade,has_female in STARS:
        part=s[a:b];segment_shas[roman]=hash_bytes(part.encode("utf-8"))
        headings=[]; cursor=a;context="narrative";grades=0;count=0
        for line in part.splitlines(keepends=True):
            text=line.strip()
            cp=cursor+(line.index(text) if text else 0)
            cursor+=len(line)
            if not text or text in ("<poem>","</poem>"):
                continue
            if "入男命吉凶诀：" in text:
                context="male_life_poem_heading";kind="historical_poem_heading";headings.append(context)
            elif "入女命吉凶诀：" in text:
                context="female_life_poem_heading";kind="historical_poem_heading";headings.append(context)
            elif "入限吉凶诀：" in text:
                context="time_limit_poem_heading";kind="historical_poem_heading";headings.append(context)
            elif text.startswith(anchor):
                context="narrative";kind="auxiliary_star_profile_intro"
            elif context=="narrative" and text.startswith(tuple("子丑寅卯辰巳午未申酉戌亥")) and "宫" in text:
                kind="auxiliary_palace_grade_condition";grades+=1
            elif context.endswith("poem_heading"):
                kind="historical_sex_coded_or_time_poem_verse"
            else:
                kind="auxiliary_natal_narrative_condition"
            data=text.encode("utf-8")
            bytepos=len(s[:cp].encode("utf-8"))
            if s[cp:cp+len(text)]!=text or raw[bytepos:bytepos+len(data)]!=data or not a<=cp<cp+len(text)<=b:
                raise ValueError("Source original line byte and codepoint positions fail")
            records.append({
                "id":f"ZWD-R{529+len(records):04d}",
                "source":"ZWDS-CLASSIC-01","batch":"ChineseAstro-14SRC-Life",
                "original_transmitted_source_oldid":1963110,
                "original_full_source_SHA256":ORIGINAL_SHA,
                "star_roman":roman,"star_native":cn,
                "source_type":kind,"source_context":context,
                "source_original_exact_Chinese_Wikitext_quote":text,
                "source_quote_UTF8_bytes":len(data),
                "source_quote_sha256":hash_bytes(data),
                "absolute_codepoint_offset":cp,
                "absolute_UTF8_byte_offset":bytepos,
                "excerpt_relative_codepoint_offset":cp-start,
                "not_exact_scholarly_translation":"Original source line recorded verbatim. Historical status, sex, health and timed claims remain unverified.",
                "mentions_historic_health_sex_morality_or_mortality":any(f in text for f in TERM_FLAGS),
                "original_Ming_woodblock_imprint_authenticated":False,
                "genuine_human_predictions_validated":0,
                "runtime_astrology_promotions":0,
            })
            count+=1
        expected_headings=["male_life_poem_heading"]
        if has_female:expected_headings.append("female_life_poem_heading")
        expected_headings.append("time_limit_poem_heading")
        if (count,grades,headings,cursor)!=(expected_count,expected_grade,expected_headings,b):
            raise ValueError(f"Original source {roman} missing or invented verses/grade rows {(count,grades,headings,cursor)}")
        sections.append({
            "star_native":cn,"star_roman":roman,
            "original_codepoint_start":a,
            "original_codepoint_end_exclusive":b,
            "original_source_segment_SHA256":segment_shas[roman],
            "literal_source_line_count":count,
            "original_palace_grade_rows":grades,
            "has_independent_original_female_poem_heading":has_female,
            "all_originally_present_sex_timing_verse_headings_preserved":True,
            "original_birth_record_human_validation":False
        })
    nav=NEXT_STAR[2];encoded=nav.encode("utf-8")
    records.append({
        "id":f"ZWD-R{529+len(records):04d}",
        "source":"ZWDS-CLASSIC-01","batch":"ChineseAstro-14SRC-Life",
        "source_type":"NEXT_AUXILIARY_LUCUN_NAVIGATION_ONLY",
        "original_transmitted_source_oldid":1963110,
        "original_full_source_SHA256":ORIGINAL_SHA,
        "star_roman":NEXT_STAR[0],"star_native":NEXT_STAR[1],
        "source_original_exact_Chinese_Wikitext_quote":nav,
        "source_quote_UTF8_bytes":len(encoded),
        "source_quote_sha256":hash_bytes(encoded),
        "absolute_codepoint_offset":end,
        "absolute_UTF8_byte_offset":len(s[:end].encode("utf-8")),
        "excerpt_relative_codepoint_offset":end-start,
        "not_exact_scholarly_translation":"Lu Cun boundary marker only; no substantive Lu Cun profile interpreted.",
        "original_Ming_woodblock_imprint_authenticated":False,
        "genuine_human_predictions_validated":0,
        "runtime_astrology_promotions":0
    })
    if len(records)!=58 or records[0]["id"]!="ZWD-R0529" or records[-1]["id"]!="ZWD-R0586":
        raise ValueError("Historical auxiliary source count/ID mismatch")
    src={
        "schema":"CHINESE_V14_ZIWEI_LIFE_AUXILIARY_FIRST_FOUR_SOURCE_ONLY_V1",
        "status":"SOURCE_PROVISIONAL_NOT_A_NATAL_CALCULATOR",
        "original_wikitext_oldid":1963110,
        "original_source_full_SHA256":ORIGINAL_SHA,
        "original_source_full_bytes":len(raw),
        "original_source_path":str(FULL.relative_to(ROOT)),
        "source_excerpt_path":str(excerpt_file.relative_to(ROOT)),
        "source_excerpt_start_codepoint":start,
        "source_excerpt_end_codepoint_exclusive":end,
        "source_excerpt_SHA256":hash_bytes(excerpt.encode("utf-8")),
        "original_Brothers_next_section_codepoint":37269,
        "star_sections":sections,
        "source_star_line_counts":{row["star_roman"]:row["literal_source_line_count"] for row in sections},
        "previous_principal_source_finished_through_PoJun":True,
        "source_V13_WenChang_navigation_only_not_prior_substantive_claim":True,
        "four_new_auxiliary_profiles_source_covered":True,
        "auxiliary_source_incomplete_after_LuCun":True,
        "YouBi_distinct_female_poem_heading_absent_from_original":True,
        "ZuoFu_YouBi_separate_palace_grade_rows_absent_from_original":True,
        "original_Ming_woodblock_imprint_verified":False,
        "historical_health_mortality_moral_gender_statements_empirical":False,
        "original_full_Life_palace_text_completed":False,
        "new_original_source_historical_notes":len(records),
        "first_id":records[0]["id"],
        "last_id":records[-1]["id"],
        "next_id":"ZWD-R0587",
        "next_unstudied_star":"禄存",
        "next_unstudied_original_codepoint":end,
        "BaZi_next_original_BZI_R0211_untouched":True,
        "genuine_blinded_real_human_tests":0,
        "runtime_astrological_promotions":0,
        "records":records,
    }
    file=B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"
    write(file,src)
    witness={
        "schema":"CHINESE_V14_EXACT_SOURCE_UTF8_BYTE_OFFSET_WITNESS",
        "full_original_source_SHA256":ORIGINAL_SHA,
        "excerpt_SHA256":src["source_excerpt_SHA256"],
        "excerpt_codepoint_range":[start,end],
        "star_segment_SHA256":segment_shas,
        "original_quotes":[{
            "id":r["id"],"codepoint":r["absolute_codepoint_offset"],
            "UTF8_byte_offset":r["absolute_UTF8_byte_offset"],
            "quote_SHA256":r["source_quote_sha256"],
            "quote_UTF8_bytes":r["source_quote_UTF8_bytes"]
        } for r in records],
        "human_prediction_test_count":0,
    }
    wit=B/"SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json"
    write(wit,witness)
    accept={
        "batch":"ChineseAstro-14SRC-Life",
        "previous_source_V13_index_SHA256":V13_SHA,
        "Chinese_before":738,"BaZi_before_after":210,"ZiWei_before":528,
        "new_original_source_notes":58,
        "Chinese_after_if_accepted":796,"ZiWei_after_if_accepted":586,
        "first_id":"ZWD-R0529","last_id":"ZWD-R0586",
        "next_id":"ZWD-R0587","next_BZI":"BZI-R0211",
        "source_stars_native":["文昌","文曲","左辅","右弼"],
        "source_next_star_native":"禄存",
        "source_full_raw_SHA256":ORIGINAL_SHA,
        "source_notes_SHA256":hash_bytes(file.read_bytes()),
        "source_witness_SHA256":hash_bytes(wit.read_bytes()),
        "source_excerpt_SHA256":src["source_excerpt_SHA256"],
        "original_full_auxiliary_and_Life_section_finished":False,
        "actual_real_human_predictive_validations":0,
        "runtime_promotions":0
    }
    write(B/"ACCEPTANCE.json",accept)
    print(json.dumps({"source_notes":len(records),"first":records[0]["id"],
        "last":records[-1]["id"],"next":src["next_id"],
        "star_counts":src["source_star_line_counts"],
        "source_span":[start,end],"excerpt_sha256":src["source_excerpt_SHA256"]},
        ensure_ascii=False,indent=2))
if __name__=="__main__":make()
