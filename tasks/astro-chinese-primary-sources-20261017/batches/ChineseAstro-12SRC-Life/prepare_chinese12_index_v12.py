#!/usr/bin/env python3
"""Guarded Chinese V11→V12 original source appendix, no natal predictions."""
from __future__ import annotations
import copy,json,subprocess
from hashlib import sha256
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_12SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-chinese-v12-ziwei-life-third-four-20261020"
OLD_SHA="86451a64172a37192026b701ab3cd0df54759ea7cfe1ccee6be83b8ec3de916e"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sh(p):return sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def unchanged(p):
    rel=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Earlier accepted original source changed "+rel)

def accept():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Wrong isolated source branch")
    if any(p.exists() for p in (NEW,REC,RECEIPT,LATEST)):
        raise ValueError("Interrupted source index append: reconcile rather than rerun")
    old=rd(OLD)
    source=rd(B/"ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json")
    wit=rd(B/"SOURCE_LIFE_THIRD_FOUR_83_EXACT_OFFSET_WITNESS_V1.json")
    meta=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if sh(OLD)!=OLD_SHA or old["sum_source_annotations"]!=609:
        raise ValueError("V11 prior accepted index bytes not correct")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[
        (210,"BZI-R0211"),(399,"ZWD-R0400")
    ]:
        raise ValueError("Previously accepted ZiWei/BaZi source frontier altered")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-11SRC-Life" or old[
        "original_chinese_source_anchors_checked_against_revision"
    ]!=537:
        raise ValueError("Old original-source historical annotation ledger differs")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Old source falsely contains empirical validation")
    if sh(RAW)!=RAW_SHA or RAW.stat().st_size!=106736:
        raise ValueError("Original pinned transmitted Chinese Wikitext SHA changed")
    if len(source["records"])!=83 or len(wit["exact_quote_offsets"])!=83:
        raise ValueError("Four next source profiles / 83 quoted entries incomplete")
    if [r["id"] for r in source["records"]]!=[
        f"ZWD-R{x:04d}" for x in range(400,483)
    ]:
        raise ValueError("Original source IDs duplicate or not consecutive")
    if (source["next_id"],source["original_excerpt_start_codepoint"],
        source["original_excerpt_end_codepoint_exclusive"])!=(
        "ZWD-R0483",25795,28621
    ):
        raise ValueError("Unexpected Life-palace excerpt boundaries")
    if not source["TianLiang_source_has_no_distinct_female_verse_heading"]:
        raise ValueError("Missing original Tian Liang source omission evidence")
    if source["complete_Life_palace_source_study"] or source["original_Ming_woodblock_imprint_authenticated"]:
        raise ValueError("Historical source outside scope or unsupported original provenance")
    expected=(
        sh(B/"ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"),
        sh(B/"SOURCE_LIFE_THIRD_FOUR_83_EXACT_OFFSET_WITNESS_V1.json"),
        sh(B/"SOURCE_1963110_LIFE_PALACE_THIRD_FOUR_EXACT_EXCERPT.txt")
    )
    if (meta["note_SHA256"],meta["witness_SHA256"],meta["excerpt_SHA256"])!=expected:
        raise ValueError("Original quote/offset/full excerpt hash drift")
    if not archive["zip_CRC_verified"] or not archive["all_member_SHA_and_bytes_verified"]:
        raise ValueError("Independent original source archive not checksum checked")
    if (archive["independently_cold_replayed_source_tests"],
        archive["independently_cold_replayed_tests_green"])!=(15,15):
        raise ValueError("Cold original source fixture not replayed")
    portable=Path(archive["owner_local_archive_path"])
    if not portable.is_file() or sh(portable)!=archive["archive_sha256"]:
        raise ValueError("Portable archival source ZIP SHA no longer accepted")
    west=rd(WEST)
    if (west["records_count"],west["batches"][-1]["id"])!=(13044,"B07bc"):
        raise ValueError("Parent Chinese source's older Western snapshot modified")
    for p in (
        OLD,T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json",
        T/"CHINESE_SOURCE_AUDIT_INDEX_V9.json",RAW,
        T/"batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
        T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",
        WEST
    ):
        unchanged(p)
    if any(r["genuine_human_behavior_or_fate_validated"] or
           r["runtime_rule_promoted"] or r["actual_forward_reverse_blind_people_tested"]
           for r in source["records"]):
        raise ValueError("Historical verses cannot become real-person empirical predictions")
    REC.mkdir(exist_ok=False)
    for p,name in (
        (OLD,"CHINESE_V11_BEFORE_12.json"),
        (CURRENT,"CHINESE_CURRENT_BEFORE_12.md"),
        (WEST,"WESTERN_B07bc_BEFORE_12.json")
    ):
        (REC/name).write_bytes(p.read_bytes())
    new=copy.deepcopy(old)
    new["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V12"
    new["status"]="ZIWEI_LIFE_PALACE_STARS_9_TO_12_SOURCE_ONLY_PARTIAL"
    new["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V11.json"
    new["prior_index_sha256"]=OLD_SHA
    new["as_of_utc"]="2026-10-20"
    new["sum_source_annotations"]=692
    new["original_chinese_source_anchors_checked_against_revision"]=620
    new["accepted_batches"].append({
        "id":"ChineseAstro-12SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":83,
        "start":"ZWD-R0400","end":"ZWD-R0482",
        "path":"batches/ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
        "rules_sha256":expected[0],
        "witness_path":"batches/ChineseAstro-12SRC-Life/SOURCE_LIFE_THIRD_FOUR_83_EXACT_OFFSET_WITNESS_V1.json",
        "witness_sha256":expected[1],
        "original_excerpt_path":"batches/ChineseAstro-12SRC-Life/SOURCE_1963110_LIFE_PALACE_THIRD_FOUR_EXACT_EXCERPT.txt",
        "original_excerpt_sha256":expected[2],
        "source_oldid":1963110,"source_raw_full_sha256":RAW_SHA,
        "original_star_groups_native":["贪狼","巨门","天相","天梁"],
        "star_original_source_line_counts":[21,22,21,18],
        "no_dedicated_TianLiang_female_poem_heading_in_original":True,
        "next_unstudied_star":"七杀",
        "complete_Life_palace_source_study":False,
        "original_ancient_printing_unverified":True,
        "portable_cold_source_test_replays":15,
        "genuine_human_predictive_validations":0,
        "runtime_promotions":0
    })
    new["systems"][1]["accepted_source_annotations"]=482
    new["systems"][1]["current_ids"]="ZWD-R0001–ZWD-R0482"
    new["systems"][1]["next_id"]="ZWD-R0483"
    new["systems"][1]["current_batch"]="ChineseAstro-12SRC-Life"
    new["systems"][1]["source_files"].append(
        "batches/ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"
    )
    new["systems"][1]["chapter_coverage"]=(
        "Original transmitted Zi Wei Volume II oldid1963110, five bureau "
        "source diagrams, and Life-palace star profiles 1–12 only: original "
        "first eight accepted previously; new TanLang21, JuMen22, "
        "TianXiang21, TianLiang18 original lines, plus navigation-only "
        "QiSha prefix source marker. Original TianLiang contains male "
        "and time-limit verse headings but no dedicated female poem heading; "
        "DO NOT fabricate it. Later star profiles and remainder of "
        "Life-palace to Siblings cp37269 remain unstudied. No authenticated "
        "old printed imprint, full original natal/calendar or human validity."
    )
    if new["systems"][0]!=old["systems"][0] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Historical accepted BaZi or previous ZiWei batches rewritten")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=692:
        raise ValueError("New 692 Chinese historical source count inconsistent")
    new["separate_lilly_source_count_at_this_revision"]=13044
    new["separate_ptolemy_source_count_at_this_revision"]=1066
    new["source_parallel_western_history_binding"]=(
        "Chinese V12 original source lineage inherits accepted older Western "
        "B07bc snapshot Lilly13044+Ptolemy1066 byte-identical. Separate "
        "later Western B07bg original source has Lilly13236+Ptolemy1066 "
        "without being merged into this Chinese branch; aggregate source "
        "numbers may be summed as documentary counts only."
    )
    new["full_ziwei_original_text_collation_finished"]=False
    new["all_14_principal_stars_verified"]=False
    new["ziwei_complete_natal_calendar_engine_verified"]=False
    new["chinese_bazi_solar_term_engine_verified"]=False
    new["historical_glyph_and_translator_limits"]=(
        "Transmitted Simplified Chinese Wikitext oldid1963110 is not "
        "original authenticated Ming print or expert translation. "
        "Source star grade, natal class and old sex-coded mortality/"
        "medical/gender stereotyped descriptions are historical rhetoric, "
        "not empirical, clinical or socially normative facts. "
        "TianLiang dedicated female verse omission preserved, not "
        "replaced from any modern text. Model or human predictions untested."
    )
    new["independently_validated_real_human_claims"]=0
    new["runtime_promotions"]=0
    new["next"]=(
        "Next source Zi Wei Life-palace Qi Sha 七杀 starts cp28621, "
        "ZWD-R0483; then Po Jun and later original descriptions to "
        "Brothers/Siblings ===二兄弟=== cp37269. BaZi Di Tian Sui "
        "section19 next BZI-R0211 unchanged. Independent natal astro-"
        "time/calendar and original chart parsing partial; no frozen real "
        "human predictions; preregister blind humans with decoys/non-"
        "astrology baselines before seeing any outcomes."
    )
    save(NEW,new)
    summary=(
        "# Chinese V12 — original Zi Wei Life-palace third four star profiles\n\n"
        "**83 source-only historical annotations ZWD-R0400–ZWD-R0482**: "
        "TanLang21, JuMen22, TianXiang21, TianLiang18 verbatim "
        "source lines plus next QiSha navigation marker. Exact oldid1963110 "
        "original UTF8 byte offsets, quote SHA and segments preserved, "
        "with missing dedicated TianLiang female poem heading explicitly "
        "documented, NOT fabricated. Full original Life-palace source "
        "is still PARTIAL, original Ming-era printed imprint unverified; "
        "old sex/medical/mortality claims unvalidated and not advice. "
        "**Chinese BaZi210 + ZiWei482 =692** historical source notes. "
        "Separate Western B07bg Lilly13236+Ptolemy1066 on independent "
        "branch means aggregate **14,994** text notes, not subjects or "
        "predictive hits. Next **ZWD-R0483 QiSha** cp28621, BaZi "
        "**BZI-R0211**. Genuine human blind validations **0**, "
        "runtime astrology promotions **0**.\n\n"
    )
    CURRENT.write_text(
        summary+"## Previous Chinese accepted source checkpoint retained\n\n"+
        CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(
        summary+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    receipt={
        "batch":"ChineseAstro-12SRC-Life",
        "status":"GUARDED_ORIGINAL_CHINESE_V12_83_ACCEPTED_LOCAL_REMOTE_PENDING",
        "Chinese_before":609,"Chinese_after":692,
        "BaZi_retained":210,"ZiWei_before":399,"ZiWei_after":482,
        "new_source_only_historical_records":83,
        "first_ZWD":"ZWD-R0400","last_ZWD":"ZWD-R0482",
        "next_ZWD":"ZWD-R0483","next_BZI":"BZI-R0211",
        "original_oldid":1963110,"full_source_SHA256":RAW_SHA,
        "previous_V11_index_SHA256":sh(REC/"CHINESE_V11_BEFORE_12.json"),
        "new_V12_index_SHA256":sh(NEW),
        "source_notes_SHA256":expected[0],
        "source_quote_witness_SHA256":expected[1],
        "source_excerpt_SHA256":expected[2],
        "cold_zip_SHA256":archive["archive_sha256"],
        "cold_tests_replayed":15,
        "parent_Western_B07bc_Lilly":13044,
        "parent_Western_B07bc_Ptolemy":1066,
        "newer_separate_Western_B07bg_Lilly":13236,
        "aggregate_original_source_notes_across_separate_branches":14994,
        "TianLiang_missing_distinct_female_heading_preserved":True,
        "real_human_predictive_validations":0,
        "production_astrology_rules_promoted":0
    }
    save(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":accept()
