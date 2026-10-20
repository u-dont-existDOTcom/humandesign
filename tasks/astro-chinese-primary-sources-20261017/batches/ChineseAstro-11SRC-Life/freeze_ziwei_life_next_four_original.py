#!/usr/bin/env python3
"""Freeze 4 further transmitted Zi Wei Life-palace principal-star profiles.

All original Simplified Chinese lines and byte offsets from exact oldid1963110.
TianTong, LianZhen, TianFu, TaiYin only; NEXT TanLang is navigation,
not claimed as reviewed. Historical beliefs, NOT real human prediction data.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
ORIG=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX=T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
OLD_V10=T/"batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
ORIGINAL_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V10_INDEX_SHA="7475cccde5aba4f0274fab1adc3b7ff1160e5494dd55cb91e8bdf6f3e5ebb366"
ORIGINAL_BYTES=106736
BATCH="ChineseAstro-11SRC-Life"
FIRST_NUMBER=310
STARS=(
    ("TianTong","天同","天同水，南斗化福"),
    ("LianZhen","廉贞","廉贞属火，北斗化次桃花杀"),
    ("TianFu","天府","天府土，南斗化令星"),
    ("TaiYin","太阴","太阴水，南北斗化富"),
)
NEXT=("TanLang","贪狼","贪狼属木，化桃花杀")
SEX_HEALTH_MORAL_TERMS=(
    "夭","刑夫","克子","娼","淫","杀","残疾","贫穷",
    "疾","寿","死","夫君","命妇","伤残","血"
)

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def hashdata(blob):
    return sha256(blob).hexdigest()

def save(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def run():
    raw=ORIG.read_bytes()
    if len(raw)!=ORIGINAL_BYTES or hashdata(raw)!=ORIGINAL_SHA:
        raise ValueError("Transmitted original full Wikitext bytes/SHA drift")
    full=raw.decode("utf-8")
    idx=read(INDEX)
    prev=read(OLD_V10)
    oldwest=read(WEST)
    if hashdata(INDEX.read_bytes())!=V10_INDEX_SHA:
        raise ValueError("Accepted V10 source index checksum changed")
    if (idx["sum_source_annotations"],idx["systems"][0]["accepted_source_annotations"],
        idx["systems"][1]["accepted_source_annotations"],idx["systems"][0]["next_id"],
        idx["systems"][1]["next_id"],idx["accepted_batches"][-1]["id"])!=(
        519,210,309,"BZI-R0211","ZWD-R0310","ChineseAstro-10SRC-Life"
    ):
        raise ValueError("Old accepted source frontier is not correct V10")
    if idx["independently_validated_real_human_claims"] or idx["runtime_promotions"]:
        raise ValueError("Old source unexpectedly represented as empirical astrology")
    if oldwest["records_count"]!=13044 or oldwest["batches"][-1]["id"]!="B07bc":
        raise ValueError("Versioned Western source snapshot no longer matches V10 parent")
    if (prev["last_id"],prev["next_id"],prev["next_star_substantive_codepoint"])!=(
        "ZWD-R0309","ZWD-R0310",22909
    ):
        raise ValueError("Previous source TianTong boundary was not a navigation marker")
    first=full.index(STARS[0][2],22000)
    nextstart=full.index(NEXT[2],first)
    siblings=full.index("===二兄弟===",nextstart)
    positions=[full.index(marker,first,nextstart) for _,_,marker in STARS]
    if (first,nextstart,siblings,positions)!=(
        22909,25795,37269,[22909,23557,24407,25060]
    ):
        raise ValueError("Original 4 star sections offsets/collation moved")
    if len(set(positions))!=4:
        raise ValueError("Source star intros duplicated")
    bounds=positions+[nextstart]
    excerpt=full[first:nextstart]
    filename=B/"SOURCE_1963110_LIFE_PALACE_NEXT_FOUR_EXACT_EXCERPT.txt"
    filename.write_bytes(excerpt.encode("utf-8"))
    if hashdata(filename.read_bytes())!=hashdata(excerpt.encode("utf-8")):
        raise ValueError("Original partial excerpt not exact")
    rows=[]
    starcounts={}
    sections=[]
    sha_segments={}
    for k,(roman,han,marker) in enumerate(STARS):
        start,end=bounds[k],bounds[k+1]
        segment=full[start:end]
        sha_segments[roman]=hashdata(segment.encode("utf-8"))
        cursor=start
        context="narrative"
        count=0
        branch_count=0
        heading_names=[]
        for line in segment.splitlines(keepends=True):
            stripped=line.strip()
            offset=line.index(stripped) if stripped else 0
            pos=cursor+offset
            cursor+=len(line)
            if not stripped or stripped in ("<poem>","</poem>"):
                continue
            if "入男命吉凶诀：" in stripped:
                context="male_life_poem_heading"
                typ="historical_poem_heading"
                heading_names.append(context)
            elif "入女命吉凶诀：" in stripped:
                context="female_life_poem_heading"
                typ="historical_poem_heading"
                heading_names.append(context)
            elif "入限吉凶诀：" in stripped:
                context="time_limit_poem_heading"
                typ="historical_poem_heading"
                heading_names.append(context)
            elif stripped.startswith(marker):
                context="narrative"
                typ="star_profile_intro"
            elif (stripped.startswith(tuple("子丑寅卯辰巳午未申酉戌亥"))
                  and "宫" in stripped and context=="narrative"):
                typ="natal_branch_condition"
                branch_count+=1
            elif context.endswith("poem_heading"):
                typ="historical_sex_coded_or_time_poem_verse"
            else:
                typ="natal_narrative_condition"
            if pos<start or pos+len(stripped)>end:
                raise ValueError("Source star input line outside exact section")
            if full[pos:pos+len(stripped)]!=stripped:
                raise ValueError("Original source copied/normalised differently")
            b=stripped.encode("utf-8")
            bytepos=len(full[:pos].encode("utf-8"))
            if raw[bytepos:bytepos+len(b)]!=b:
                raise ValueError("Wrong original UTF8 source offset")
            rows.append({
                "id":f"ZWD-R{FIRST_NUMBER+len(rows):04d}",
                "source":"ZWDS-CLASSIC-01",
                "batch":BATCH,
                "original_full_transmitted_oldid":1963110,
                "original_full_source_sha256":ORIGINAL_SHA,
                "star_group_native":han,
                "star_group_romanization":roman,
                "source_line_type":typ,
                "source_section_context":context,
                "exact_original_Chinese_Wikitext_quote":stripped,
                "source_quote_sha256_UTF8":hashdata(b),
                "source_quote_UTF8_bytes":len(b),
                "original_absolute_codepoint_offset":pos,
                "original_absolute_UTF8_byte_offset":bytepos,
                "original_excerpt_relative_codepoint_offset":pos-first,
                "historical_research_gloss_NOT_exact_translation":(
                    f"Source {han} {context} historical text line exact; its "
                    "natal, wealth, health, social, old gender or time claims "
                    "are NOT independently verified, not an expert translation."
                ),
                "contains_historic_health_sex_morality_or_death_terms":any(
                    term in stripped for term in SEX_HEALTH_MORAL_TERMS
                ),
                "source_original_Ming_printing_authenticated":False,
                "original_natal_star_premise_astronomically_verified":False,
                "genuine_human_behavior_or_fate_validated":False,
                "medical_or_moral_advice_authorized":False,
                "actual_forward_reverse_blind_people_tested":0,
                "runtime_rule_promoted":False
            })
            count+=1
        if cursor!=end:
            raise ValueError("Original star source cursor missing verse fragment")
        if count<19 or branch_count<4 or heading_names!=[
            "male_life_poem_heading","female_life_poem_heading",
            "time_limit_poem_heading"
        ]:
            raise ValueError(f"Incomplete original {roman} passage {count},{branch_count},{heading_names}")
        starcounts[roman]=count
        sections.append({
            "original_star":han,"star_roman":roman,
            "original_codepoint_start":start,
            "original_codepoint_end_exclusive":end,
            "source_original_UTF8_SHA256":sha_segments[roman],
            "source_line_annotation_count":count,
            "original_palace_line_count":branch_count,
            "all_written_male_female_limit_verses_in_source_preserved":True,
            "actual_early_print_imprint_verified":False,
            "actual_human_predictions_validated":False
        })
    nextquote=NEXT[2]
    next_utf8=nextquote.encode("utf-8")
    rows.append({
        "id":f"ZWD-R{FIRST_NUMBER+len(rows):04d}",
        "source":"ZWDS-CLASSIC-01","batch":BATCH,
        "source_line_type":"NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TANLANG_CLAIMS",
        "original_full_transmitted_oldid":1963110,
        "original_full_source_sha256":ORIGINAL_SHA,
        "star_group_native":NEXT[1],"star_group_romanization":NEXT[0],
        "exact_original_Chinese_Wikitext_quote":nextquote,
        "source_quote_sha256_UTF8":hashdata(next_utf8),
        "source_quote_UTF8_bytes":len(next_utf8),
        "original_absolute_codepoint_offset":nextstart,
        "original_absolute_UTF8_byte_offset":len(full[:nextstart].encode("utf-8")),
        "original_excerpt_relative_codepoint_offset":nextstart-first,
        "historical_research_gloss_NOT_exact_translation":(
            "Source navigation boundary for Tan Lang only: Tan Lang and all later "
            "stars are UNSTUDIED in this batch; no source rule asserted."
        ),
        "source_original_Ming_printing_authenticated":False,
        "original_natal_star_premise_astronomically_verified":False,
        "genuine_human_behavior_or_fate_validated":False,
        "medical_or_moral_advice_authorized":False,
        "actual_forward_reverse_blind_people_tested":0,
        "runtime_rule_promoted":False,
    })
    if starcounts!={"TianTong":20,"LianZhen":26,"TianFu":20,"TaiYin":23}:
        raise ValueError(f"Source line counts differ from independently inspected source {starcounts}")
    if len(rows)!=90 or rows[0]["id"]!="ZWD-R0310" or rows[-1]["id"]!="ZWD-R0399":
        raise ValueError("Wrong original Zi Wei source annotation IDs")
    src={
        "schema":"CHINESE_ASTRO_V11_SOURCE_LIFE_PALACE_NEXT_FOUR_ORIGINAL_V1",
        "status":"HISTORICAL_ORIGINAL_SOURCE_PROVISIONAL_NOT_PRODUCTION",
        "source_native_book":"紫微斗數全書 卷二",
        "original_oldid":1963110,
        "original_Wikitext_sha256":ORIGINAL_SHA,
        "original_Wikitext_bytes":ORIGINAL_BYTES,
        "original_Wikitext_repo_path":str(ORIG.relative_to(ROOT)),
        "original_excerpt_repo_path":str(filename.relative_to(ROOT)),
        "previous_V10_TianTong_only_heading_prefix_already_in_R0309":True,
        "previous_V10_source_boundary_prefix_not_prior_TianTong_description":True,
        "original_excerpt_start_codepoint":first,
        "original_excerpt_end_codepoint_exclusive":nextstart,
        "siblings_next_section_heading_codepoint":siblings,
        "original_excerpt_utf8_bytes":len(excerpt.encode("utf-8")),
        "original_excerpt_sha256":hashdata(excerpt.encode("utf-8")),
        "star_original_sections":sections,
        "star_line_counts":starcounts,
        "only_four_additional_of_all_original_Life_palace_stars":True,
        "complete_Life_palace_source_study":False,
        "original_Ming_woodblock_imprint_authenticated":False,
        "original_claims_of_sex_health_disability_and_longevity_medically_true":False,
        "source_original_inconsistent_star_conditions_resolved":False,
        "new_historical_documentary_notes":len(rows),
        "first_id":rows[0]["id"],"last_id":rows[-1]["id"],
        "next_id":"ZWD-R0400",
        "next_unstudied_star_native":"贪狼",
        "next_unstudied_star_original_codepoint":nextstart,
        "separate_BaZi_original_source_next_BZI_R0211_retained":True,
        "genuine_real_human_predictive_validations":0,
        "runtime_forecast_promotions":0,
        "records":rows
    }
    notes=B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"
    save(notes,src)
    witness={
        "schema":"CHINESE_ASTRO_V11_EXACT_SOURCE_OFFSET_WITNESS_V1",
        "original_full_Wikitext_sha256":ORIGINAL_SHA,
        "original_excerpt_sha256":src["original_excerpt_sha256"],
        "original_excerpt_source_codepoint_range":[first,nextstart],
        "exact_source_star_segment_sha256":sha_segments,
        "exact_quote_offsets":[{
            "id":x["id"],
            "original_codepoint_offset":x["original_absolute_codepoint_offset"],
            "original_UTF8_byte_offset":x["original_absolute_UTF8_byte_offset"],
            "quote_SHA256":x["source_quote_sha256_UTF8"],
            "quote_UTF8_bytes":x["source_quote_UTF8_bytes"],
        } for x in rows],
        "authentic_original_ancient_imprint_attested":False,
        "actual_human_predictions_validated":0
    }
    witnessfile=B/"SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json"
    save(witnessfile,witness)
    accept={
        "batch":BATCH,
        "prior_V10_Chinese_source_index_SHA256":V10_INDEX_SHA,
        "Chinese_before":519,"ZiWei_before":309,"BaZi_retained":210,
        "new_original_source_only_annotations":90,
        "Chinese_after_if_accepted":609,
        "ZiWei_after_if_accepted":399,
        "first_source_id":"ZWD-R0310","last_source_id":"ZWD-R0399",
        "next_ZWD":"ZWD-R0400","next_BZI":"BZI-R0211",
        "only_stars_native":["天同","廉贞","天府","太阴"],
        "next_unstudied_star_native":"贪狼",
        "full_source_SHA256":ORIGINAL_SHA,
        "excerpt_SHA256":src["original_excerpt_sha256"],
        "note_SHA256":hashdata(notes.read_bytes()),
        "witness_SHA256":hashdata(witnessfile.read_bytes()),
        "fully_critical_printed_historic_Life_palace_completed":False,
        "full_natal_chart_accurate_and_empirically_validated":False,
        "real_person_forward_reverse_tests":0,
        "runtime_promotions":0
    }
    save(B/"ACCEPTANCE.json",accept)
    print(json.dumps({
        "stage":"V11 PROVISIONAL",
        "source_notes":len(rows),"first":rows[0]["id"],
        "last":rows[-1]["id"],"next":accept["next_ZWD"],
        "four_star_counts":starcounts,
        "first_end":[first,nextstart],
        "excerpt_sha":src["original_excerpt_sha256"]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    run()
