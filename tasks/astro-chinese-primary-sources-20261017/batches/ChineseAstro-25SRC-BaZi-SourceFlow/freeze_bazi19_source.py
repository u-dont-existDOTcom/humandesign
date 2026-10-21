#!/usr/bin/env python3
"""Exact online Di Tian Sui 19 verse/commentary/example Wikitext, no predictive tests."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import re

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW = B/"evidence/DiTianSui_19_oldid844368.wikitext"
MANIFEST = B/"PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json"
OLD = T/"CHINESE_SOURCE_AUDIT_INDEX_V24.json"
RAW_SHA = "032a772c550dedb35aa130b835bb12d09dd3f3e89652aea382d7b00587ccf28d"
OLD_SHA = "ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1"

def sha(raw:bytes)->str:
    return sha256(raw).hexdigest()
def load(p:Path)->dict:
    return json.loads(p.read_text("utf-8"))
def save(p:Path,obj:object)->None:
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def extract()->None:
    raw=RAW.read_bytes()
    if (len(raw),sha(raw))!=(909,RAW_SHA):
        raise ValueError("Wikisource Di Tian Sui original oldid844368 raw bytes changed")
    old=load(OLD);manifest=load(MANIFEST)["19"]
    if sha(OLD.read_bytes())!=OLD_SHA or old["sum_source_annotations"]!=1269:
        raise ValueError("Parent Chinese V24 index not accepted/frozen")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[(210,"BZI-R0211"),(1059,"ZWD-R1060")]:
        raise ValueError("Parent Chinese BaZi/ZiWei next source moved")
    if manifest["exact_sha256"]!=RAW_SHA or manifest["pinned_oldid"]!=844368 or manifest["exact_utf8_bytes"]!=909:
        raise ValueError("Original source provenance manifest drift")
    s=raw.decode("utf-8")
    if len(s)!=455 or not s.startswith("{{Novel|滴天髓|源流論|18|20|論}}"):
        raise ValueError("Original source title/length mismatch")
    verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",s,flags=re.S)
    commentary=re.findall(r"(?m)^:　　(.+)$",s)
    charts=re.findall(r"(?m)^\| (.+?) \|\| (.+?) \|\| (.+?) \|\| (.+)$",s)
    header="! 時 !! 日 !! 月 !! 年"
    if len(verses)!=1 or len(commentary)!=3 or len(charts)!=2 or s.count(header)!=2:
        raise ValueError("Original 19 verse/commentary/two-case table structure moved")
    if verses[0]!="何處起根源，流向可方住，機括此中求，知來亦知去。":
        raise ValueError("Original verse variant silently corrected")
    if not commentary[2].endswith("所以為僧也。") or "無從引助" not in commentary[2]:
        raise ValueError("Original second historical example wording altered")
    if not commentary[1].find("所以富貴")>=0:
        raise ValueError("Original first purported wealth outcome missing")
    if charts != [("丁巳","戊申","癸巳","辛酉"),("壬子","癸丑","壬戌","癸丑")]:
        raise ValueError("Original four-pillar case data or time-day-month-year order moved")
    content=[]
    content += [("transmitted_original_verse",verses[0])]
    content += [("transmitted_commentary","\u3000\u3000"+c) for c in []] # classification declared below
    for para in commentary:
        content.append(("transmitted_commentary",para))
    for row in charts:
        content.append(("historical_four_pillar_example","| "+" || ".join(row)))
    doc_order=sorted(content,key=lambda item:s.find(item[1]))
    if len(doc_order)!=6:
        raise ValueError("Expected six complete source verse/commentary/example units")
    records=[]
    for role,text in doc_order:
        if s.count(text)!=1:
            raise ValueError("Source component not uniquely quoted: "+text[:20])
        cp=s.index(text);offset=len(s[:cp].encode("utf-8"));enc=text.encode("utf-8")
        if raw[offset:offset+len(enc)]!=enc:
            raise ValueError("Original exact quote/UTF8 offset mismatch")
        row={
            "id":f"BZI-R{211+len(records):04d}",
            "batch":"ChineseAstro-25SRC-BaZi-SourceFlow",
            "source":"BAZI-DTS-WIKISOURCE-TRANSMITTED",
            "source_chapter":"滴天髓/19",
            "pinned_original_oldid":844368,
            "full_raw_Wikitext_SHA256":RAW_SHA,
            "source_layer":role,
            "original_exact_Chinese_quote":text,
            "quote_SHA256":sha(enc),
            "quote_UTF8_bytes":len(enc),
            "source_absolute_codepoint_offset":cp,
            "source_absolute_UTF8_byte_offset":offset,
            "original_ancient_Ming_print_authorship_verified":False,
            "independent_historical_case_outcome_verified":False,
            "real_human_blind_predictive_validations":0,
            "runtime_astrological_rule_promotions":0,
        }
        if role=="historical_four_pillar_example":
            values=[v.strip() for v in text.strip("|").split("||")]
            if len(values)!=4:raise ValueError("Four pillars must be exactly four columns")
            row["original_column_order"]=["hour","day","month","year"]
            row["historical_chart_pillars"]={k:v for k,v in zip(row["original_column_order"],values)}
            row["birth_date_and_identity_independently_known"]=False
        records.append(row)
    if [r["id"] for r in records] != [f"BZI-R{i:04d}" for i in range(211,217)]:
        raise ValueError("Six source records not sequential")
    # Source authorial case outcomes are reported narrative, not independently checked people.
    examples=[r for r in records if r["source_layer"]=="historical_four_pillar_example"]
    if [r["historical_chart_pillars"] for r in examples] != [
        {"hour":"丁巳","day":"戊申","month":"癸巳","year":"辛酉"},
        {"hour":"壬子","day":"癸丑","month":"壬戌","year":"癸丑"}]:
        raise ValueError("Historical sample chart field order corrupted")
    heads=[]
    for found in re.finditer(r"(?m)^! 時 !! 日 !! 月 !! 年$",s):
        cp=found.start()
        encoded=found.group(0).encode("utf-8")
        byte_offset=len(s[:cp].encode("utf-8"))
        if raw[byte_offset:byte_offset+len(encoded)]!=encoded:
            raise ValueError("Original example column header byte witness wrong")
        heads.append({"original_exact_Chinese_header":found.group(0),
                      "original_codepoint_offset":cp,
                      "original_UTF8_byte_offset":byte_offset,
                      "original_quote_SHA256":sha(encoded)})
    if len(heads)!=2:
        raise ValueError("Both source original table headings required")
    classification_count={key:sum(r["source_layer"]==key for r in records) for key in (
        "transmitted_original_verse","transmitted_commentary","historical_four_pillar_example")}
    if classification_count!={"transmitted_original_verse":1,
                              "transmitted_commentary":3,
                              "historical_four_pillar_example":2}:
        raise ValueError("Original verse/commentary/two-example text count changed")
    notes={
        "schema":"BAZI_DI_TIAN_SUI_SECTION19_SOURCE_FLOW_PINNED_ONLINE_SOURCE_ONLY_V1",
        "batch":"ChineseAstro-25SRC-BaZi-SourceFlow",
        "source_chapter":"滴天髓/19",
        "original_source_oldid":844368,
        "raw_wikitext_local_relative":"evidence/DiTianSui_19_oldid844368.wikitext",
        "original_full_raw_UTF8_bytes":909,
        "original_full_raw_sha256":RAW_SHA,
        "source_components":classification_count,
        "new_documentary_historical_source_records":6,
        "first_id":"BZI-R0211","last_id":"BZI-R0216","next_id":"BZI-R0217",
        "next_ziwei_source_id_unchanged":"ZWD-R1060",
        "source_case_table_header_original_time_day_month_year":heads,
        "source_verse_short_online_version":"何處起根源，流向可方住，機括此中求，知來亦知去。",
        "source_variant_compare_longer_DiTianSuiChanWei_requires_independent_pin":True,
        "source_outcome_first_example_richness_independently_authenticated":False,
        "source_outcome_second_example_monk_independently_authenticated":False,
        "source_human_prediction_accuracy_evidence":0,
        "birthdates_or_individuals_for_historic_examples_known":False,
        "original_early_print_authenticity_verified":False,
        "truly_independent_bazi_calendar_and_pillar_engine_verified":False,
        "runtime_astrological_rule_promotions":0,
        "records":records,
    }
    notes_file=B/"BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json"
    save(notes_file,notes)
    witness={
        "schema":"BAZI_DTS_19_ORIGINAL_CHINESE_CP_UTF8_SHA_WITNESS_V1",
        "source_oldid":844368,"raw_source_SHA256":RAW_SHA,"raw_UTF8_bytes":909,
        "original_source_column_order_time_day_month_year":heads,
        "record_original_quote_witness":[
          {"id":r["id"],"layer":r["source_layer"],
           "codepoint":r["source_absolute_codepoint_offset"],
           "utf8_byte_offset":r["source_absolute_UTF8_byte_offset"],
           "source_quote_SHA256":r["quote_SHA256"],
           "quote_UTF8_bytes":r["quote_UTF8_bytes"]} for r in records],
        "real_blinded_human_forecast_successes":0
    }
    witness_file=B/"SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json"
    save(witness_file,witness)
    save(B/"ACCEPTANCE.json",{
        "batch":"ChineseAstro-25SRC-BaZi-SourceFlow",
        "previous_Chinese_V24_index_SHA256":OLD_SHA,
        "Chinese_before":1269,"BaZi_before":210,"ZiWei_unchanged":1059,
        "new_BaZi_source_only_records":6,
        "Chinese_after_if_accepted":1275,"BaZi_after_if_accepted":216,
        "first_id":"BZI-R0211","last_id":"BZI-R0216",
        "next_id":"BZI-R0217","next_ZiWei":"ZWD-R1060",
        "source_oldid":844368,"source_raw_sha256":RAW_SHA,
        "source_notes_sha256":sha(notes_file.read_bytes()),
        "source_witness_sha256":sha(witness_file.read_bytes()),
        "source_case_outcomes_original_verse_and_tables_not_verified_people":True,
        "real_human_blind_predictions_validated":0,"runtime_promotions":0,
    })
    print(json.dumps({"new_historical_annotations":len(records),
        "source_components":classification_count,
        "first_id":notes["first_id"],"last_id":notes["last_id"],
        "next_id":notes["next_id"],"raw_sha256":RAW_SHA},ensure_ascii=False,indent=2))

if __name__=="__main__":
    extract()
