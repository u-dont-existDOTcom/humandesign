#!/usr/bin/env python3
"""Exact original online Zi Wei wealth source extraction (not financial predictions)."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
ORIGINAL_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
INDEX_SHA="52c5d51a281d5e641d2e029af81929e7a327d04eb5e1b510534d45b78c27fcb2"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
START,END=40563,41672
CONT={2:"ZiWei",6:"WuQu",9:"LianZhen",14:"JuMen",17:"TianLiang",19:"PoJun"}
STAR={
    1:"ZiWei",3:"TianJi",4:"TaiYang",5:"WuQu",
    7:"TianTong",8:"LianZhen",10:"TianFu",11:"TaiYin",
    12:"TanLang",13:"JuMen",15:"TianXiang",16:"TianLiang",
    18:"PoJun",20:"WenChang",21:"WenQu",22:"ZuoFuAndYouBi",
    23:"LuCun",24:"QingYang",25:"TuoLuo",26:"HuoXing",
    27:"LingXing",28:"KuiYue",29:"DouJun"
}
HISTORIC_TERMS=("财","富","贫","钱","田","禄","吉","凶","破","耗","贵","官","困","岁")


def sha(b:bytes)->str:
    return sha256(b).hexdigest()


def rd(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(name:str,obj:object)->None:
    (B/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def freeze()->None:
    raw=RAW.read_bytes()
    if (len(raw),sha(raw))!=(106736,ORIGINAL_SHA):
        raise ValueError("Original transmitted Wikitext identity changed")
    if sha(OLD.read_bytes())!=INDEX_SHA or sha(WEST.read_bytes())!=WEST_SHA:
        raise ValueError("Prior V19 or old inherited Western source index changed")
    old=rd(OLD)
    if old["sum_source_annotations"]!=1038 or [
        (x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]
    ]!=[(210,"BZI-R0211"),(828,"ZWD-R0829")]:
        raise ValueError("Source index frontier not accepted V19")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-19SRC-Children":
        raise ValueError("Prior branch index changed")
    s=raw.decode("utf-8")
    if len(s)!=48890 or not s[START:].startswith("===五财帛===") or not s[END:].startswith("===六疾厄==="):
        raise ValueError("Source Wealth/Disease boundaries absent")
    if s.index("===六疾厄===",START)!=END:
        raise ValueError("Unexpected previous physical section")
    excerpt=s[START:END]
    (B/"SOURCE_1963110_WEALTH_EXACT_EXCERPT.txt").write_bytes(excerpt.encode("utf-8"))
    cp=START
    count=0
    records=[]
    markup=[]
    for literal in excerpt.splitlines(keepends=True):
        t=literal.strip()
        start=cp+(literal.index(t) if t else 0)
        cp+=len(literal)
        if not t:continue
        if t in ("<poem>","</poem>"):
            markup.append([start,t])
            continue
        i=count
        count+=1
        if i==0: group,role="WealthSection","ORIGINAL_SECTION_HEADING"
        elif i in CONT: group,role=CONT[i],"ORIGINAL_CONTINUATION_OF_PREVIOUS_STAR_LINE"
        elif i in STAR: group,role=STAR[i],"ORIGINAL_STAR_OR_COMBINATION_TEXT_LINE"
        else: raise ValueError(f"unexpected source physical line {i}")
        encoded=t.encode("utf-8")
        by=len(s[:start].encode("utf-8"))
        if s[start:start+len(t)]!=t or raw[by:by+len(encoded)]!=encoded or not START<=start<start+len(t)<=END:
            raise ValueError("Exact source line Unicode/UTF8 offset mismatch")
        records.append({
            "id":f"ZWD-R{829+len(records):04d}",
            "source":"ZWDS-CLASSIC-01",
            "batch":"ChineseAstro-20SRC-Wealth",
            "online_source_oldid":1963110,"original_full_Wikitext_SHA256":ORIGINAL_SHA,
            "original_section":"财帛","original_line_index":i,
            "historical_clause_group":group,"source_type":role,
            "exact_original_Chinese_Wikitext_quote":t,
            "quote_sha256":sha(encoded),"quote_UTF8_bytes":len(encoded),
            "absolute_codepoint_offset":start,"absolute_UTF8_byte_offset":by,
            "excerpt_relative_codepoint_offset":start-START,
            "historical_finance_rhetoric_present":any(x in t for x in HISTORIC_TERMS),
            "original_ancient_printing_verified":False,
            "actual_real_person_financial_forecast_verified":False,
            "human_blind_predictive_validations":0,"runtime_promotions":0,
        })
    if (count,len(records),cp)!=(30,30,END):
        raise ValueError("Source line count or boundary inconsistent")
    if markup!=[[START+len(excerpt[:excerpt.index("<poem>")]),"<poem>"],
                [START+len(excerpt[:excerpt.index("</poem>")]),"</poem>"]]:
        raise ValueError("Original verse markup not preserved")
    if [row["original_line_index"] for row in records if row["source_type"]=="ORIGINAL_CONTINUATION_OF_PREVIOUS_STAR_LINE"]!=[2,6,9,14,17,19]:
        raise ValueError("Source line-continuations improperly separated")
    nav="===六疾厄==="
    records.append({
        "id":"ZWD-R0859","source":"ZWDS-CLASSIC-01",
        "batch":"ChineseAstro-20SRC-Wealth",
        "source_type":"NEXT_DISEASE_SECTION_NAVIGATION_ONLY",
        "historical_clause_group":"DiseaseNextSection",
        "online_source_oldid":1963110,"original_full_Wikitext_SHA256":ORIGINAL_SHA,
        "exact_original_Chinese_Wikitext_quote":nav,
        "quote_sha256":sha(nav.encode("utf-8")),
        "quote_UTF8_bytes":len(nav.encode("utf-8")),
        "absolute_codepoint_offset":END,
        "absolute_UTF8_byte_offset":len(s[:END].encode("utf-8")),
        "excerpt_relative_codepoint_offset":END-START,
        "original_ancient_printing_verified":False,
        "actual_real_person_financial_forecast_verified":False,
        "human_blind_predictive_validations":0,"runtime_promotions":0,
    })
    if len(records)!=31 or records[0]["id"]!="ZWD-R0829" or records[-1]["id"]!="ZWD-R0859":
        raise ValueError("Historical source record numbering not consecutive")
    doc={
        "schema":"CHINESE_V20_ZIWEI_WEALTH_TRANSMITTED_WIKITEXT_HISTORICAL_ONLY",
        "batch":"ChineseAstro-20SRC-Wealth",
        "oldid":1963110,"source_full_SHA256":ORIGINAL_SHA,
        "excerpt_codepoints":[START,END],
        "excerpt_sha256":sha(excerpt.encode("utf-8")),
        "excerpt_UTF8_bytes":len(excerpt.encode("utf-8")),
        "original_poem_markup":markup,
        "physical_source_lines_including_heading":30,
        "physical_wrapped_condition_continuation_lines":6,
        "source_other_star_or_combination_lines":23,
        "next_Disease_navigation_only_records":1,
        "new_original_source_notes":31,
        "first_id":"ZWD-R0829","last_id":"ZWD-R0859",
        "next_id":"ZWD-R0860","next_section_codepoint":END,
        "not_verified_original_Ming_printing":True,
        "not_a_traditional_natal_chart_engine":True,
        "source_finance_claims_are_not_investment_advice_or_real_human_outcomes":True,
        "human_blind_predictions_validated":0,"runtime_astrology_promotions":0,
        "records":records,
    }
    notes=B/"ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json"
    save(notes.name,doc)
    save("SOURCE_WEALTH_31_EXACT_OFFSET_WITNESS_V1.json",{
        "schema":"CHINESE_V20_SOURCE_CP_UTF8_SHA_WITNESS",
        "original_full_source_sha256":ORIGINAL_SHA,
        "source_excerpt_sha256":doc["excerpt_sha256"],
        "original_excerpt_span_codepoints":[START,END],
        "original_verse_markup":markup,
        "quotes":[{
            "id":x["id"],"cp":x["absolute_codepoint_offset"],
            "UTF8_offset":x["absolute_UTF8_byte_offset"],
            "sha256":x["quote_sha256"],"utf8_bytes":x["quote_UTF8_bytes"]
        } for x in records],
        "human_predictive_tests":0,
    })
    save("ACCEPTANCE.json",{
        "batch":"ChineseAstro-20SRC-Wealth",
        "old_index_V19_SHA256":INDEX_SHA,"BaZi_preserved":210,"ZiWei_before":828,
        "Chinese_before":1038,"new_original_source_notes":31,
        "ZiWei_after_if_accepted":859,"Chinese_after_if_accepted":1069,
        "first_id":"ZWD-R0829","last_id":"ZWD-R0859",
        "next_id":"ZWD-R0860","next_BaZi":"BZI-R0211",
        "source_excerpt_sha256":doc["excerpt_sha256"],
        "source_notes_sha256":sha(notes.read_bytes()),
        "source_full_SHA256":ORIGINAL_SHA,
        "source_continuation_lines":6,
        "real_human_blind_predictions":0,"runtime_astrological_promotions":0,
    })
    print(json.dumps({"documentary_new_records":31,"source_lines":30,
        "continuations":6,"next":"ZWD-R0860",
        "excerpt_sha256":doc["excerpt_sha256"]},ensure_ascii=False,indent=2))


if __name__=="__main__":
    freeze()
