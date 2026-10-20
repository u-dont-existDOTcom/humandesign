#!/usr/bin/env python3
"""Guarded immutable Chinese V10→V11 exact original source-only append.

Never conflate the independent later Western source history with the older
Western parent snapshot on this separately branched Chinese research line.
"""
from __future__ import annotations
import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_11SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-chinese-v11-ziwei-life-next-four-20261020"
OLD_SHA="7475cccde5aba4f0274fab1adc3b7ff1160e5494dd55cb91e8bdf6f3e5ebb366"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"

def read(p):return json.loads(p.read_text(encoding="utf-8"))
def digest(p):return sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def assert_prior_file(p):
    relative=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+relative)!=git("hash-object",str(p)):
        raise ValueError("Existing accepted source file modified "+relative)

def accept():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not on separately accepted Zi Wei source-only V11 worktree")
    if any(p.exists() for p in (NEW,REC,RECEIPT,LATEST)):
        raise ValueError("Interrupted/previous V11 admission: recover before proceeding")
    old=read(OLD)
    src=read(B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json")
    witness=read(B/"SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json")
    meta=read(B/"ACCEPTANCE.json")
    archive=read(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if digest(OLD)!=OLD_SHA or old["sum_source_annotations"]!=519:
        raise ValueError("V10 canonical Chinese index does not match pinned SHA")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] != [
        (210,"BZI-R0211"),(309,"ZWD-R0310")
    ]:
        raise ValueError("Old accepted Zi Wei/BaZi counts or next original source IDs differ")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-10SRC-Life" or old[
        "original_chinese_source_anchors_checked_against_revision"
    ]!=447:
        raise ValueError("V10 accepted original provenance or line count changed")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Original source is not supposed to include human validations")
    if digest(RAW)!=RAW_SHA or RAW.stat().st_size!=106736:
        raise ValueError("Original transmitted Wikitext full SHA/bytes no longer match")
    if len(src["records"])!=90 or len(witness["exact_quote_offsets"])!=90:
        raise ValueError("Missing original Zi Wei star sources/offset witnesses")
    if [r["id"] for r in src["records"]] != [f"ZWD-R{x:04d}" for x in range(310,400)]:
        raise ValueError("Original source annotation identities no longer sequential")
    if (src["next_id"],src["original_excerpt_start_codepoint"],
        src["original_excerpt_end_codepoint_exclusive"])!=(
        "ZWD-R0400",22909,25795
    ):
        raise ValueError("Original source bounded Life-palace study drift")
    if src["complete_Life_palace_source_study"] or src["original_Ming_woodblock_imprint_authenticated"]:
        raise ValueError("Historical source must remain partial / provenance-limited")
    expected=(
        digest(B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"),
        digest(B/"SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json"),
        digest(B/"SOURCE_1963110_LIFE_PALACE_NEXT_FOUR_EXACT_EXCERPT.txt")
    )
    if (meta["note_SHA256"],meta["witness_SHA256"],meta["excerpt_SHA256"])!=expected:
        raise ValueError("Accepted original exact quote or excerpt SHA altered")
    if not archive["zip_CRC_verified"] or not archive["all_member_SHA_and_bytes_verified"]:
        raise ValueError("Cold independent source pack lacks CRC/members verification")
    if (archive["independently_cold_replayed_source_tests"],
        archive["independently_cold_replayed_tests_green"])!=(15,15):
        raise ValueError("Cold source tests 15/15 not completed")
    cold=Path(archive["owner_local_archive_path"])
    if not cold.is_file() or digest(cold)!=archive["archive_sha256"]:
        raise ValueError("Cold independently verified portable ZIP changed")
    west=read(WEST)
    if (west["records_count"],west["batches"][-1]["id"])!=(13044,"B07bc"):
        raise ValueError("Parallel older Western version on this source branch changed")
    for p in (
        OLD,T/"CHINESE_SOURCE_AUDIT_INDEX_V9.json",
        T/"CHINESE_SOURCE_AUDIT_INDEX_V8.json",
        RAW,T/"batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
        T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",WEST
    ):
        assert_prior_file(p)
    if any(r["genuine_human_behavior_or_fate_validated"] or r["runtime_rule_promoted"] or
           r["actual_forward_reverse_blind_people_tested"]
           for r in src["records"]):
        raise ValueError("Historical source cannot be marketed as real-person predictions")
    REC.mkdir(exist_ok=False)
    for p,name in (
        (OLD,"CHINESE_V10_BEFORE_11.json"),
        (CURRENT,"CHINESE_CURRENT_BEFORE_11.md"),
        (WEST,"WESTERN_B07bc_BEFORE_11.json")
    ):
        (REC/name).write_bytes(p.read_bytes())
    new=copy.deepcopy(old)
    new["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V11"
    new["status"]="ZIWEI_LIFE_PALACE_STARS_FIVE_THROUGH_EIGHT_SOURCE_ONLY_PARTIAL"
    new["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V10.json"
    new["prior_index_sha256"]=OLD_SHA
    new["as_of_utc"]="2026-10-20"
    new["sum_source_annotations"]=609
    new["original_chinese_source_anchors_checked_against_revision"]=537
    new["accepted_batches"].append({
        "id":"ChineseAstro-11SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":90,
        "start":"ZWD-R0310","end":"ZWD-R0399",
        "path":"batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
        "rules_sha256":expected[0],
        "witness_path":"batches/ChineseAstro-11SRC-Life/SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json",
        "witness_sha256":expected[1],
        "original_excerpt_path":"batches/ChineseAstro-11SRC-Life/SOURCE_1963110_LIFE_PALACE_NEXT_FOUR_EXACT_EXCERPT.txt",
        "original_excerpt_sha256":expected[2],
        "source_oldid":1963110,
        "source_raw_full_sha256":RAW_SHA,
        "original_star_groups_native":["天同","廉贞","天府","太阴"],
        "star_original_source_line_counts":[20,26,20,23],
        "next_unstudied_star":"贪狼",
        "original_14_star_life_palace_source_not_complete":True,
        "source_original_Ming_imprint_unverified":True,
        "cold_source_test_replays":15,
        "independent_real_human_predictions":0,
        "production_astro_rules_promoted":0
    })
    new["systems"][1]["accepted_source_annotations"]=399
    new["systems"][1]["current_ids"]="ZWD-R0001–ZWD-R0399"
    new["systems"][1]["next_id"]="ZWD-R0400"
    new["systems"][1]["current_batch"]="ChineseAstro-11SRC-Life"
    new["systems"][1]["source_files"].append(
        "batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"
    )
    new["systems"][1]["chapter_coverage"]=(
        "Original transmitted oldid1963110 Zi Wei Volume II, five bureau "
        "diagrams and symbolic conditions, Life-palace PARTIAL: now first "
        "eight stars, previously ZiWei/TianJi/TaiYang/WuQu source profiles "
        "and new TianTong/LianZhen/TianFu/TaiYin with 89 more original "
        "verbatim lines plus next TanLang navigation marker = 90 "
        "historical source-only notes. Full Life-palace text remains "
        "unstudied after cp25795; source critical first print and real "
        "human natal/behavioral tests are unverified."
    )
    if new["systems"][0]!=old["systems"][0] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Previous accepted BaZi/Chinese source records modified")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=609:
        raise ValueError("Chinese V11 sum no longer 609")
    new["separate_lilly_source_count_at_this_revision"]=13044
    new["separate_ptolemy_source_count_at_this_revision"]=1066
    new["source_parallel_western_history_binding"]=(
        "Chinese source branch independently descends from V9/V10 with "
        "unchanged Western B07bc snapshot Lilly13044+Ptolemy1066. "
        "Later Western B07bg independently accepted Lilly13236 but is "
        "not merged into this branch. Aggregate historical source "
        "annotations across distinct branches may be reported with caveat."
    )
    new["full_ziwei_original_text_collation_finished"]=False
    new["all_14_principal_stars_verified"]=False
    new["ziwei_complete_natal_calendar_engine_verified"]=False
    new["chinese_bazi_solar_term_engine_verified"]=False
    new["historical_glyph_and_translator_limits"]=(
        "This is original transmitted Simplified Chinese Wikitext oldid1963110, "
        "not an authenticated original early Ming printed or critically "
        "translated original. Partly source-copied conditional palace tables, "
        "old sex-coded, life/health/mortality/fertility and moral status "
        "claims are unverified historical rhetoric, not empirical, "
        "clinical or normative truths. Traditional calendar and old "
        "star-house interpretations unverified against actual people."
    )
    new["independently_validated_real_human_claims"]=0
    new["runtime_promotions"]=0
    new["next"]=(
        "Zi Wei Life-palace next original Tan Lang star at codepoint25795, "
        "ZWD-R0400, then remaining original star text through separate "
        "siblings heading cp37269. BaZi next BZI-R0211 Di Tian Sui "
        "section19 unchanged. Original birth-time and historical calendar "
        "engineering is partial, no source rule/human predictive "
        "validations; preregister blind actual people and controls before "
        "seeing response outcomes."
    )
    write(NEW,new)
    preface=(
        "# Chinese V11 — original Zi Wei Life-palace next four source stars\n\n"
        "**90 historical source-only notes ZWD-R0310–ZWD-R0399**, "
        "TianTong20, LianZhen26, TianFu20, TaiYin23 original lines, "
        "plus one TanLang next-star navigation. Exact oldid1963110 "
        "original codepoint+UTF8 byte-offset SHA for every line and "
        "full source witness; earlier V10 TianTong prefix was navigation "
        "only. Source Life-palace section still PARTIAL, original Ming "
        "woodblock imprint and independent specialist translation "
        "not authenticated. Historic medical/sex/moral/fate claims "
        "not empirical truth or real personal predictions. "
        "**Chinese BaZi210 unchanged + ZiWei399 =609** historic "
        "annotations; separately latest accepted Western B07bg "
        "**Lilly13236+Ptolemy1066** lives on another research branch, "
        "aggregate **14,911 source documents** (not people/test successes). "
        "Next **ZWD-R0400 TanLang** cp25795 and **BZI-R0211**. "
        "Human blind predictive studies **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(
        preface+"## Previous Chinese accepted source checkpoint retained\n\n"+
        CURRENT.read_text(encoding="utf-8"),encoding="utf-8"
    )
    LATEST.write_text(
        preface+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    rec={
        "batch":"ChineseAstro-11SRC-Life",
        "status":"GUARDED_ORIGINAL_CHINESE_V11_90_ADMITTED_LOCAL_REMOTE_PENDING",
        "Chinese_before":519,"Chinese_after":609,
        "BaZi_retained":210,"ZiWei_before":309,"ZiWei_after":399,
        "new_original_source_annotations":90,
        "first_ZWD":"ZWD-R0310","last_ZWD":"ZWD-R0399",
        "next_ZWD":"ZWD-R0400","next_BZI":"BZI-R0211",
        "original_full_source_oldid":1963110,
        "original_full_Wikitext_sha256":RAW_SHA,
        "old_V10_index_sha256":digest(REC/"CHINESE_V10_BEFORE_11.json"),
        "new_V11_index_sha256":digest(NEW),
        "source_notes_sha256":expected[0],
        "source_witness_sha256":expected[1],
        "source_excerpt_sha256":expected[2],
        "portable_cold_archive_sha256":archive["archive_sha256"],
        "cold_source_tests_green":15,
        "parent_Western_B07bc_Lilly":13044,
        "parent_Western_B07bc_Ptolemy":1066,
        "distinct_newer_Western_B07bg_Lilly":13236,
        "historical_source_counts_aggregate_across_separate_branches":14911,
        "independent_real_human_predictive_tests":0,
        "runtime_astrological_promotions":0
    }
    write(RECEIPT,rec)
    print(json.dumps(rec,ensure_ascii=False,indent=2))

if __name__=="__main__":accept()
