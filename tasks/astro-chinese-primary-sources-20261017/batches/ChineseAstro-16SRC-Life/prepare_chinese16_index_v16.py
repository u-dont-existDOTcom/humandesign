#!/usr/bin/env python3
"""Guarded Chinese V16 last online Life-palace source append, no real humans."""
from __future__ import annotations
import copy,hashlib,json,subprocess
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V15.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V16.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
V15_NOTES=T/"batches/ChineseAstro-15SRC-Life/ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_16SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261021.json"
SOURCE=B/"ZIWEI_LIFE_REMAINING_105_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_LIFE_REMAINING_105_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_REMAINING_EXACT_EXCERPT.txt"
BRANCH="research/astro-chinese-v16-ziwei-life-complete-online-source-20261021"
OLD_SHA="a5bf0e0cc4bd801b209caa98e1bd58558f2155fd73ba9a055d516472076311ad"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def assert_accepted_unchanged(p):
    rel=p.relative_to(ROOT).as_posix()
    assert git("rev-parse","HEAD:"+rel)==git("hash-object",str(p)),f"previously accepted modified: {rel}"


def accept():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("wrong isolated writer branch for Zi Wei V16 source")
    if any(p.exists() for p in (NEW,LATEST,REC,RECEIPT)):
        raise ValueError("interrupted admission: reconcile existing new original-source state")
    if (sha(OLD),sha(RAW),sha(WEST))!=(OLD_SHA,RAW_SHA,WEST_SHA):
        raise ValueError("immutable Chinese previous index, original source or Western snapshot changed")
    for p in (OLD,RAW,WEST,V15_NOTES,CURRENT):
        assert_accepted_unchanged(p)
    before=read(OLD)
    source=read(SOURCE)
    witness=read(WIT)
    a=read(B/"ACCEPTANCE.json")
    archive=read(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261021.json")
    if (before["sum_source_annotations"],before["original_chinese_source_anchors_checked_against_revision"])!=(850,778):
        raise ValueError("prior V15 Chinese source index counts changed")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in before["systems"]] != [
        (210,"BZI-R0211"),(640,"ZWD-R0641")
    ]:
        raise ValueError("unexpected accepted original BaZi/ZiWei frontier")
    if before["accepted_batches"][-1]["id"]!="ChineseAstro-15SRC-Life":
        raise ValueError("previous accepted original source batch changed")
    if before["independently_validated_real_human_claims"] or before["runtime_promotions"]:
        raise ValueError("source notes are not independently evaluated real-human predictions")
    if len(source["records"])!=105 or len(witness["original_quotes"])!=105:
        raise ValueError("missing 105 original Chinese source notes")
    if [r["id"] for r in source["records"]] != [f"ZWD-R{i:04d}" for i in range(641,746)]:
        raise ValueError("source ID duplicates/gaps")
    if (source["source_excerpt_start_codepoint"],source["source_excerpt_end_codepoint_exclusive"])!=(33783,37269):
        raise ValueError("exact source Life remainder boundary not preserved")
    if (source["next_id"],source["next_original_section_codepoint"],source["next_original_section"])!=("ZWD-R0746",37269,"兄弟"):
        raise ValueError("original source next Brothers boundary mismatch")
    if not (source["mixed_traditional_simplified_HuaLu_verses_retained"]
       and source["combined_HuoLing_and_JieKong_groups_unseparated"]
       and source["all_remaining_online_Life_palace_original_group_lines_through_Brothers_documented"]):
        raise ValueError("original source line/variant/scope not verified")
    if (source["critically_collated_ancient_Life_palace_imprint"]
        or source["other_11_online_house_sections_studied_completely"]
        or source["genuine_blinded_real_human_tests"]
        or source["runtime_astrological_promotions"]):
        raise ValueError("historical source interpreted beyond evidence")
    if any(r["human_blinded_predictions_validated"] or r["runtime_astrology_promotions"] for r in source["records"]):
        raise ValueError("individual historical lines promoted as predictions")
    hashes=(sha(SOURCE),sha(WIT),sha(EXCERPT))
    if a["source_notes_SHA256"]!=hashes[0] or a["source_excerpt_SHA256"]!=hashes[2]:
        raise ValueError("frozen source notes/excerpt SHA mismatch")
    if witness["source_excerpt_SHA256"]!=hashes[2] or witness["source_full_SHA256"]!=RAW_SHA:
        raise ValueError("source witness did not capture exact Wikitext")
    if not archive["ZIP_CRC_verified"] or not archive["each_member_hash_and_size_verified"]:
        raise ValueError("portable archive failed ZIP CRC/member hash")
    if (archive["independent_cold_source_tests_executed"],archive["independent_cold_source_tests_green"])!=(12,12):
        raise ValueError("independent cold extracted source tests missing")
    package=Path(archive["archive_path_on_owner_computer"])
    if not package.is_file() or sha(package)!=archive["archive_sha256"]:
        raise ValueError("owner source ZIP lost or SHA changed")
    REC.mkdir(exist_ok=False)
    for src,dest in (
      (OLD,"CHINESE_V15_BEFORE_16.json"),
      (CURRENT,"CHINESE_CURRENT_BEFORE_16.md"),
      (WEST,"WESTERN_B07bc_BEFORE_16.json")
    ):
        (REC/dest).write_bytes(src.read_bytes())
    new=copy.deepcopy(before)
    new.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V16",
        "status":"ZIWEI_LIFE_PALACE_TRANSMITTED_ONLINE_TEXT_SOURCE_SEGMENT_COVERED_OTHER_HOUSES_OPEN",
        "as_of_utc":"2026-10-21",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V15.json",
        "prior_index_sha256":OLD_SHA,
        "sum_source_annotations":955,
        "original_chinese_source_anchors_checked_against_revision":883,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0
    })
    new["accepted_batches"].append({
        "id":"ChineseAstro-16SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":105,
        "substantive_original_lines":104,
        "following_section_navigation_only_records":1,
        "start":"ZWD-R0641","end":"ZWD-R0745",
        "path":SOURCE.relative_to(T).as_posix(),
        "rules_sha256":hashes[0],
        "witness_path":WIT.relative_to(T).as_posix(),
        "witness_sha256":hashes[1],
        "original_excerpt_path":EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256":hashes[2],
        "source_oldid":1963110,"source_raw_full_sha256":RAW_SHA,
        "original_source_group_count":15,
        "original_source_group_line_counts":[7,7,9,6,8,3,2,4,5,8,11,11,16,5,2],
        "original_HuoLing_JieKong_combined_groups_preserved":True,
        "mixed_original_HuaLu_traditional_simplified_variants_preserved":True,
        "online_original_Life_palace_through_Brothers_heading_documented":True,
        "original_critical_book_completed":False,
        "ancient_Ming_original_imprint_authenticity_unverified":True,
        "other_11_houses_still_unstudied_as_complete_source_sections":True,
        "cold_source_test_replays":12,
        "actual_human_predictions_validated":0,
        "runtime_model_promotions":0,
    })
    ziwei=new["systems"][1]
    ziwei["accepted_source_annotations"]=745
    ziwei["current_ids"]="ZWD-R0001–ZWD-R0745"
    ziwei["next_id"]="ZWD-R0746"
    ziwei["current_batch"]="ChineseAstro-16SRC-Life"
    ziwei["source_files"].append(SOURCE.relative_to(T).as_posix())
    ziwei["chapter_coverage"]=(
      "Source-anchored transmitted Zi Wei volume II Wikitext oldid1963110 original Life-palace "
      "principal and auxiliary groups through literal Brothers heading cp37269, including "
      "fifteen final-group segments cp33783–37269 and combined-star and Chinese-character variants. "
      "This online Life section textual coverage is NOT independently authenticated Ming print, "
      "whole original critical edition, all twelve houses, traditional lunar/solar natal chart "
      "engine or empirical person prediction. Other eleven house text sections remain open."
    )
    new["next"]=(
      "Continue original volume II Brothers/Siblings 兄弟 section beginning literal heading "
      "===二兄弟=== cp37269; next Zi Wei source-only ZWD-R0746. Separate BaZi "
      "Di Tian Sui section19 BZI-R0211. Verify exact further twelve palace source boundaries "
      "and independent natal engine/consenting untouched blind human baselines. "
      "No real-human predictions have been validated."
    )
    new["historical_glyph_and_translator_limits"]=(
      "Online Simplified Chinese Wikitext with original mixed traditional glyphs, "
      "not authenticated original Ming woodblock or scholarly critical translation. "
      "Source line consistency, exact codepoint/UTF8 and combined-star prose studied "
      "through online Life section; neither historical text nor horoscope attribution is "
      "an observed modern behavioural, clinical or predictive fact."
    )
    new["source_parallel_western_history_binding"]=(
      "Independent Chinese branch retains older immutable Western B07bc Lilly13044+Ptolemy1066 "
      "source snapshot; separate Western B07bh accepted Lilly13271+Ptolemy1066 and "
      "B07bi imprisonment writer was active in another worktree at this continuation. "
      "Do not merge unrelated branches as if one source index, and documentary record "
      "counts are not predictive human success."
    )
    if new["systems"][0]!=before["systems"][0] or new["accepted_batches"][:-1]!=before["accepted_batches"]:
        raise ValueError("accepted previous BaZi/Chinese source history changed")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=955:
        raise ValueError("V16 source registry count inconsistent")
    save(NEW,new)
    header=(
      "# Chinese V16 — transmitted online original Zi Wei Life-palace text through Brothers\n\n"
      "**105 new source-only historical annotations ZWD-R0641–ZWD-R0745**, 104 "
      "literal source lines across 15 groups from Huo Xing to Dou Jun cp33783–37269 "
      "plus **one original Brothers heading navigation-only marker**. Original combined "
      "Huo/Ling and DiJie/TianKong passages kept together; mixed traditional/simplified "
      "Hua Lu glyphs preserved. Online Life-palace Wikitext section annotated to Brothers; "
      "other eleven houses and authentic Ming edition still unstudied. "
      "**BaZi210 + ZiWei745 =955 Chinese historical text records**; "
      "latest separately accepted Western B07bh Lilly13271+Ptolemy1066 is on another branch. "
      "Next **ZWD-R0746 兄弟 cp37269** and **BZI-R0211 Di Tian Sui section19**. "
      "Actual human blind validations **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(header+"## Previous accepted Chinese V15 checkpoint\n\n"+
        (REC/"CHINESE_CURRENT_BEFORE_16.md").read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(header+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
    result={
      "batch":"ChineseAstro-16SRC-Life",
      "status":"GUARDED_CHINESE_V16_105_HISTORICAL_SOURCE_LINES_LOCAL_ACCEPTED",
      "Chinese_before":850,"Chinese_after":955,
      "BaZi_retained":210,"ZiWei_before":640,"ZiWei_after":745,
      "new_historical_source_annotations":105,"literal_source_lines":104,
      "first_ZWD":"ZWD-R0641","last_ZWD":"ZWD-R0745",
      "next_ZWD":"ZWD-R0746","next_BZI":"BZI-R0211",
      "raw_source_oldid":1963110,"raw_source_SHA256":RAW_SHA,
      "old_V15_index_SHA256":OLD_SHA,"new_V16_index_SHA256":sha(NEW),
      "source_notes_SHA256":hashes[0],"source_witness_SHA256":hashes[1],
      "source_excerpt_SHA256":hashes[2],
      "portable_archive_SHA256":archive["archive_sha256"],
      "independent_cold_source_tests_green":12,
      "inherited_Western_B07bc_SHA256":WEST_SHA,
      "all_remaining_online_Life_palace_source_lines_through_Brothers_documented":True,
      "ancient_original_printing_authenticated":False,
      "remaining_11_house_texts_complete":False,
      "human_blind_validations":0,"runtime_astrological_promotions":0
    }
    save(RECEIPT,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    accept()
