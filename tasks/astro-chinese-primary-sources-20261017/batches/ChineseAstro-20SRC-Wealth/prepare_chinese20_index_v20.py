#!/usr/bin/env python3
"""Guarded Chinese V20 original source-only index with full old-index preservation."""
from __future__ import annotations
import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V20.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR=T/"batches/ChineseAstro-19SRC-Children/ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_20SRC_WEALTH.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261021.json"
DOC=B/"ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_WEALTH_31_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_WEALTH_EXACT_EXCERPT.txt"
BRANCH="research/astro-chinese-v20-ziwei-wealth-original-source-20261021"
OLD_SHA="52c5d51a281d5e641d2e029af81929e7a327d04eb5e1b510534d45b78c27fcb2"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(p:Path)->str:
    return sha256(p.read_bytes()).hexdigest()


def rd(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))


def wr(p:Path,obj:object)->None:
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()


def unmodified(p:Path)->None:
    rel=p.relative_to(ROOT).as_posix()
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Previously accepted source file altered: "+rel)


def admit():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not in the isolated Wealth V20 source branch")
    if any(x.exists() for x in (NEW,REC,LATEST,RECEIPT)):
        raise ValueError("Interrupted existing V20 admission: reconcile, do not rerun")
    for p,expected in ((OLD,OLD_SHA),(RAW,RAW_SHA),(WEST,WEST_SHA)):
        if sha(p)!=expected:
            raise ValueError("Source/accepted predecessor hash drift: "+str(p))
    for p in (OLD,RAW,WEST,PRIOR,CURRENT):
        unmodified(p)
    index=rd(OLD)
    doc=rd(DOC)
    wit=rd(WIT)
    meta=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
    if (index["sum_source_annotations"],index["original_chinese_source_anchors_checked_against_revision"])!=(1038,966):
        raise ValueError("Expected V19 current source totals not observed")
    if index["accepted_batches"][-1]["id"]!="ChineseAstro-19SRC-Children":
        raise ValueError("Previously accepted source batch moved")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in index["systems"]] != [
        (210,"BZI-R0211"),(828,"ZWD-R0829")]:
        raise ValueError("Unexpected source-order next IDs")
    if index["independently_validated_real_human_claims"] or index["runtime_promotions"]:
        raise ValueError("Historical source has not established real-human predictive success")
    if len(doc["records"])!=31 or len(wit["quotes"])!=31:
        raise ValueError("Documentary notes and exact witness length mismatch")
    if [x["id"] for x in doc["records"]] != [f"ZWD-R{i:04d}" for i in range(829,860)]:
        raise ValueError("V20 source ID gaps or duplicates")
    if doc["excerpt_codepoints"]!=[40563,41672] or doc["next_id"]!="ZWD-R0860":
        raise ValueError("Original Wealth and Disease source boundary mismatch")
    if doc["physical_wrapped_condition_continuation_lines"]!=6:
        raise ValueError("Source continuation classification absent")
    if doc["human_blind_predictions_validated"] or doc["runtime_astrology_promotions"] or not doc["not_verified_original_Ming_printing"]:
        raise ValueError("Misleading source status")
    shas=[sha(DOC),sha(WIT),sha(EXCERPT)]
    if (meta["source_notes_sha256"],meta["source_excerpt_sha256"]) != (shas[0],shas[2]):
        raise ValueError("Original source note/excerpt bytes changed")
    if wit["source_excerpt_sha256"]!=shas[2] or wit["original_full_source_sha256"]!=RAW_SHA:
        raise ValueError("Source quote witness changed")
    if not archive["ZIP_CRC_verified"] or not archive["all_member_SHA256_and_bytes_verified"] or archive["independent_cold_extracted_source_tests_green"]!=11:
        raise ValueError("Cold historical source ZIP not reproducible")
    zipped=Path(archive["archive_path_on_owner_computer"])
    if not zipped.is_file() or sha(zipped)!=archive["archive_sha256"]:
        raise ValueError("User source evidence ZIP missing or SHA changed")
    for rec in doc["records"]:
        if rec["human_blind_predictive_validations"] or rec["runtime_promotions"]:
            raise ValueError("Old source improperly counted as human prediction")
    REC.mkdir(exist_ok=False)
    for p,n in ((OLD,"CHINESE_V19_BEFORE_20.json"),
                (CURRENT,"CHINESE_CURRENT_BEFORE_20.md"),
                (WEST,"WESTERN_B07bc_BEFORE_20.json")):
        (REC/n).write_bytes(p.read_bytes())
    new=copy.deepcopy(index)
    new.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V20",
        "status":"ZIWEI_WEALTH_SOURCE_DOCUMENTED_NEXT_DISEASE_OTHER_HOUSES_OPEN",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V19.json",
        "prior_index_sha256":OLD_SHA,"as_of_utc":"2026-10-21",
        "sum_source_annotations":1069,
        "original_chinese_source_anchors_checked_against_revision":997,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0,
    })
    new["accepted_batches"].append({
        "id":"ChineseAstro-20SRC-Wealth",
        "added_bazi_source_annotations":0,"added_ziwei_source_annotations":31,
        "source_heading_lines":1,"source_wrapped_condition_continuations":6,
        "source_star_or_combination_lines":23,"next_Disease_navigation_only":1,
        "start":"ZWD-R0829","end":"ZWD-R0859",
        "path":DOC.relative_to(T).as_posix(),"rules_sha256":shas[0],
        "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":shas[1],
        "original_excerpt_path":EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256":shas[2],
        "original_online_Wikitext_oldid":1963110,
        "original_full_Wikitext_SHA256":RAW_SHA,
        "original_codepoint_interval":[40563,41672],
        "next_original_section_heading":"===六疾厄===",
        "source_financial_claims_independently_validated":False,
        "ancient_original_woodblock_critically_authenticated":False,
        "cold_original_source_test_replays":11,
        "actual_blinded_human_predictions_validated":0,
        "runtime_astrological_rules_promoted":0,
    })
    zw=new["systems"][1]
    zw["accepted_source_annotations"]=859
    zw["current_ids"]="ZWD-R0001–ZWD-R0859"
    zw["next_id"]="ZWD-R0860"
    zw["current_batch"]="ChineseAstro-20SRC-Wealth"
    zw["source_files"].append(DOC.relative_to(T).as_posix())
    zw["chapter_coverage"]=(
        "Transmitted Zi Wei Volume II Wikitext oldid1963110 online source through Life, "
        "Brothers, Spouses, Children and now Wealth 财帛 old passages, cp40563-41672. "
        "30 physical original nonmarkup text lines: one Wealth heading, six continuations "
        "of previous conditional stellar descriptions, 23 other historical lines, "
        "plus Disease next-section navigation only. No authenticated historical woodblock, "
        "traditional full natal chart engine or empirical human wealth/finance predictive evidence."
    )
    new["next"]=(
        "Next original Zi Wei Disease/Illness 疾厄 begins cp41672, ZWD-R0860; "
        "next Travel/Migration cp42541. BaZi Di Tian Sui section19 BZI-R0211 "
        "unchanged. Continue source text without medical advice and separately "
        "verify old printing variants and independent calendar/natal engines."
    )
    new["historical_glyph_and_translator_limits"]=(
        "Wikitext oldid1963110 not independently authenticated early original woodblock "
        "or independent expert critical translation. Wealth passage historical money "
        "and economic claims are unverified; six source textual continuations preserved. "
        "Older woodblock Four Transformations discrepancy remains untested."
    )
    if new["accepted_batches"][:-1]!=index["accepted_batches"] or new["systems"][0]!=index["systems"][0]:
        raise ValueError("Previously accepted BaZi/Chinese original source mutated")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=1069:
        raise ValueError("New Chinese index source arithmetic invalid")
    wr(NEW,new)
    heading=(
      "# Chinese V20 — transmitted Zi Wei Wealth original online source\n\n"
      "**31 new historical documentary records ZWD-R0829–ZWD-R0859** from oldid1963110 "
      "Wealth 财帛 cp40563–41672, with six original star-description continuations "
      "not counted as independent forecasts. Original wording and SHA/codepoint/UTF8 "
      "witnesses intact; 11 source tests passed, and 11 independently cold-extracted "
      "source tests passed from CRC/SHA-checked portable ZIP. "
      "**BaZi210 + Zi Wei859 =1069 historical source notes**, not validated humans. "
      "Next **ZWD-R0860 Disease cp41672** and **BZI-R0211 Di Tian Sui section19**. "
      "Old historical original edition authority, natal chart engine, and any actual "
      "human finance/health predictions unverified. Genuine human forecast validations "
      "**0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(heading+"## Prior accepted Chinese source V19 checkpoint\n\n"+
        (REC/"CHINESE_CURRENT_BEFORE_20.md").read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(heading+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    receipt={
      "batch":"ChineseAstro-20SRC-Wealth",
      "status":"GUARDED_ORIGINAL_TRANSMITTED_WEALTH_V20_LOCAL_ACCEPTANCE",
      "Chinese_before":1038,"Chinese_after":1069,
      "BaZi_retained":210,"ZiWei_before":828,"ZiWei_after":859,
      "first_ZWD":"ZWD-R0829","last_ZWD":"ZWD-R0859",
      "next_ZWD":"ZWD-R0860","next_BZI":"BZI-R0211",
      "old_V19_index_SHA256":OLD_SHA,"new_V20_index_SHA256":sha(NEW),
      "source_full_SHA256":RAW_SHA,
      "source_notes_SHA256":shas[0],"source_witness_SHA256":shas[1],
      "original_excerpt_SHA256":shas[2],
      "portable_archive_SHA256":archive["archive_sha256"],
      "independent_cold_source_tests_green":11,
      "older_Western_B07bc_SHA256":WEST_SHA,
      "real_human_predictive_validations":0,"runtime_astrological_promotions":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=="__main__":
    admit()
