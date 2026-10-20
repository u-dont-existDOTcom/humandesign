#!/usr/bin/env python3
"""Guard original Zi Wei final two principal profiles into Chinese source V13.

No original ancient printing, natal chart predictions, real-person tests.
"""
from __future__ import annotations
import copy,json,subprocess
from hashlib import sha256
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_13SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-chinese-v13-ziwei-final-two-principal-20261020"
OLD_SHA="1eb313d0e6b84695a3d8448204969a67592d4ba16b25e70ae4727163098f9d14"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"

def read(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def unchanged(p):
    name=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+name)!=git("hash-object",str(p)):
        raise ValueError("Earlier source index or original file changed "+name)

def main():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Wrong isolated V13 branch")
    if any(x.exists() for x in (NEW,REC,RECEIPT,LATEST)):
        raise ValueError("Interrupted prior index admission; reconcile before re-running")
    old=read(OLD)
    source=read(B/"ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json")
    witness=read(B/"SOURCE_LIFE_FINAL_TWO_46_EXACT_OFFSET_WITNESS_V1.json")
    accept=read(B/"ACCEPTANCE.json")
    archive=read(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if h(OLD)!=OLD_SHA or old["sum_source_annotations"]!=692:
        raise ValueError("Previous accepted Chinese V12 original source SHA drift")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[
        (210,"BZI-R0211"),(482,"ZWD-R0483")
    ]:
        raise ValueError("Parent original BaZi/ZiWei source frontier changed")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-12SRC-Life" or old[
        "original_chinese_source_anchors_checked_against_revision"
    ]!=620:
        raise ValueError("Parent original source batch or witness counts changed")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Previous documentary index wrongly contains predictions")
    if h(RAW)!=RAW_SHA or RAW.stat().st_size!=106736:
        raise ValueError("Frozen transmitted original Wikitext SHA/size drift")
    if len(source["records"])!=46 or len(witness["exact_quote_offsets"])!=46:
        raise ValueError("Missing original Qi Sha / Po Jun lines or next boundary")
    if [r["id"] for r in source["records"]]!=[
        f"ZWD-R{x:04d}" for x in range(483,529)
    ]:
        raise ValueError("Documentary source note IDs not consecutive")
    if (source["next_id"],source["original_excerpt_start_codepoint"],
        source["original_excerpt_end_codepoint_exclusive"])!=(
        "ZWD-R0529",28621,30135
    ):
        raise ValueError("Original source exact final principal star bounds wrong")
    if not source["all_fourteen_principal_star_profiles_now_source_covered"] or not source[
        "auxiliary_star_text_from_WenChang_through_Siblings_heading_unstudied"
    ] or source["complete_Life_palace_source_study"]:
        raise ValueError("Do not conflate fourteen principal profile texts with all other Life material")
    if source["original_Ming_woodblock_imprint_authenticated"]:
        raise ValueError("Unverified ancient original printing cannot be claimed")
    shas=(
        h(B/"ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"),
        h(B/"SOURCE_LIFE_FINAL_TWO_46_EXACT_OFFSET_WITNESS_V1.json"),
        h(B/"SOURCE_1963110_LIFE_PALACE_FINAL_TWO_EXACT_EXCERPT.txt")
    )
    if (accept["note_SHA256"],accept["witness_SHA256"],accept["excerpt_SHA256"])!=shas:
        raise ValueError("Exact original Chinese source note/offset SHA drift")
    if not archive["zip_CRC_verified"] or not archive["all_member_SHA_and_bytes_verified"]:
        raise ValueError("Cold archive original SHA/CRC not validated")
    if (archive["independently_cold_replayed_source_tests"],
        archive["independently_cold_replayed_tests_green"])!=(14,14):
        raise ValueError("Cold original source archive replay not accepted")
    fp=Path(archive["owner_local_archive_path"])
    if not fp.is_file() or h(fp)!=archive["archive_sha256"]:
        raise ValueError("Original source archive external file checksum changed")
    west=read(WEST)
    if (west["records_count"],west["batches"][-1]["id"])!=(13044,"B07bc"):
        raise ValueError("Inherited Western snapshot changed: separate accepted source lane not merged")
    for p in (
        OLD,T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json",
        T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json",RAW,
        T/"batches/ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
        T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",
        WEST
    ):
        unchanged(p)
    if any(r["genuine_human_behavior_or_fate_validated"] or
           r["runtime_rule_promoted"] or r["actual_forward_reverse_blind_people_tested"]
           for r in source["records"]):
        raise ValueError("Historical text not actual human predictive success")
    REC.mkdir(exist_ok=False)
    for p,n in (
        (OLD,"CHINESE_V12_BEFORE_13.json"),
        (CURRENT,"CHINESE_CURRENT_BEFORE_13.md"),
        (WEST,"WESTERN_B07bc_BEFORE_13.json")
    ):
        (REC/n).write_bytes(p.read_bytes())
    new=copy.deepcopy(old)
    new["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V13"
    new["status"]="ALL_FOURTEEN_PRINCIPAL_STAR_LIFE_PROFILE_PROSE_SOURCE_COVERED_AUXILIARY_OPEN"
    new["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V12.json"
    new["prior_index_sha256"]=OLD_SHA
    new["as_of_utc"]="2026-10-20"
    new["sum_source_annotations"]=738
    new["original_chinese_source_anchors_checked_against_revision"]=666
    new["accepted_batches"].append({
        "id":"ChineseAstro-13SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":46,
        "start":"ZWD-R0483","end":"ZWD-R0528",
        "path":"batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
        "rules_sha256":shas[0],
        "witness_path":"batches/ChineseAstro-13SRC-Life/SOURCE_LIFE_FINAL_TWO_46_EXACT_OFFSET_WITNESS_V1.json",
        "witness_sha256":shas[1],
        "original_excerpt_path":"batches/ChineseAstro-13SRC-Life/SOURCE_1963110_LIFE_PALACE_FINAL_TWO_EXACT_EXCERPT.txt",
        "original_excerpt_sha256":shas[2],
        "source_oldid":1963110,"source_raw_full_sha256":RAW_SHA,
        "last_two_principal_star_profiles":["七杀","破军"],
        "last_two_original_source_line_counts":[22,23],
        "now_all_14_principal_star_source_profile_texts_completed":True,
        "all_Life_palace_original_text_completed":False,
        "next_auxiliary_star":"文昌",
        "source_early_original_Ming_woodblock_verified":False,
        "cold_source_test_replays":14,
        "real_human_predictive_validations":0,
        "runtime_rule_promotions":0
    })
    new["systems"][1]["accepted_source_annotations"]=528
    new["systems"][1]["current_ids"]="ZWD-R0001–ZWD-R0528"
    new["systems"][1]["next_id"]="ZWD-R0529"
    new["systems"][1]["current_batch"]="ChineseAstro-13SRC-Life"
    new["systems"][1]["source_files"].append(
        "batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"
    )
    new["systems"][1]["chapter_coverage"]=(
        "Transmitted Zi Wei Volume II first Life-palace 14 named "
        "principal-star INDIVIDUAL descriptive prose source-studied "
        "across ChineseAstro-10SRC..13SRC through source original PoJun "
        "cp30135, including 14-star profile conditional palace lines "
        "and old sex/time-limited verses. V13 adds QiSha22, PoJun23 "
        "and WenChang auxiliary heading navigation-only. Remaining "
        "Life-palace auxiliary stars to Siblings original heading "
        "cp37269 and other eleven houses remain unstudied. "
        "This does not establish astronomical placement/calendar "
        "engine correctness or genuine human behavioral prediction."
    )
    if new["systems"][0]!=old["systems"][0] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Previous accepted historic ZiWei and BaZi source rewritten")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=738:
        raise ValueError("Chinese source cumulative 738 not consistent")
    new["separate_lilly_source_count_at_this_revision"]=13044
    new["separate_ptolemy_source_count_at_this_revision"]=1066
    new["source_parallel_western_history_binding"]=(
        "Chinese branch inherits frozen older original Western B07bc "
        "snapshot Lilly13044+Ptolemy1066, distinct later Western B07bg "
        "has Lilly13236+Ptolemy1066 without merging into Chinese branch. "
        "Total cross-branch documentation is an aggregate, not one "
        "accepted shared original source index or real-person successes."
    )
    new["full_ziwei_original_text_collation_finished"]=False
    new["all_14_principal_stars_verified"]=False
    new["ziwei_complete_natal_calendar_engine_verified"]=False
    new["chinese_bazi_solar_term_engine_verified"]=False
    new["historical_glyph_and_translator_limits"]=(
        "Fourteen separate principal-star Life-palace prose source "
        "profiles have exact Simplified Chinese oldid1963110 anchors "
        "and byte offsets, but are not critical early printed "
        "traditional Ming text or translated specialist edition. "
        "Auxiliary-star text still not covered, and no birth-star "
        "calendar/house computation, empirically measured human "
        "predictive validity, or clinical/moral truth established."
    )
    new["independently_validated_real_human_claims"]=0
    new["runtime_promotions"]=0
    new["next"]=(
        "Original source QiSha and PoJun last main-star profiles "
        "complete; NEXT ZiWei auxiliary Wen Chang 文昌 at cp30135, "
        "ZWD-R0529, then other Life-palace auxiliary star descriptions "
        "through original Siblings heading ===二兄弟=== cp37269. "
        "BaZi original Di Tian Sui section19 next BZI-R0211 "
        "untouched. Independently verified complete traditional "
        "chart/astronomy and real-human predictive studies open, "
        "freeze model first then preregister blind decoys/control tests."
    )
    save(NEW,new)
    summary=(
        "# Chinese V13 — all fourteen principal star Life-profile prose source covered\n\n"
        "**46 historical source-only annotations ZWD-R0483–ZWD-R0528**, "
        "QiSha22 and PoJun23 exact source lines plus one next WenChang "
        "auxiliary-source navigation. All 14 main star descriptive "
        "profiles in this transmitted oldid1963110 Life-palace source "
        "now historically annotated, with full exact UTF8 byte "
        "offsets and SHA; NOT the complete Life-palace (auxiliary "
        "passages after cp30135 remain) or an ancient authenticated "
        "Ming imprint, accurate complete natal chart or real human "
        "prediction. **Chinese BaZi210 + ZiWei528=738** text annotations. "
        "Latest independent Western B07bg Lilly13236+Ptolemy1066 "
        "produces aggregate **15,040** historical source notes "
        "on DIFFERENT source branches; not 15,040 people. "
        "Next **ZWD-R0529 WenChang**, original cp30135, "
        "BaZi **BZI-R0211** Di Tian Sui section19. "
        "Actual human blind predictive validations **0**, "
        "runtime astrology promotions **0**.\n\n"
    )
    CURRENT.write_text(
        summary+"## Prior original Chinese source checkpoint retained\n\n"+
        CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(
        summary+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    receipt={
        "batch":"ChineseAstro-13SRC-Life",
        "status":"GUARDED_CHINESE_V13_FINAL_14_PRINCIPAL_SOURCE_ACCEPTED_LOCAL_REMOTE_PENDING",
        "Chinese_before":692,"Chinese_after":738,
        "BaZi_retained":210,"ZiWei_before":482,"ZiWei_after":528,
        "new_original_source_annotations":46,
        "first_ZWD":"ZWD-R0483","last_ZWD":"ZWD-R0528",
        "next_ZWD":"ZWD-R0529","next_BZI":"BZI-R0211",
        "original_oldid":1963110,"original_full_source_SHA256":RAW_SHA,
        "previous_V12_index_SHA256":h(REC/"CHINESE_V12_BEFORE_13.json"),
        "new_V13_index_SHA256":h(NEW),
        "source_notes_SHA256":shas[0],
        "source_offset_witness_SHA256":shas[1],
        "source_excerpt_SHA256":shas[2],
        "portable_source_archive_SHA256":archive["archive_sha256"],
        "cold_source_tests":14,
        "parent_Western_B07bc_Lilly":13044,
        "parent_Western_B07bc_Ptolemy":1066,
        "latest_separate_Western_B07bg_Lilly":13236,
        "aggregate_historical_source_annotations_across_branches":15040,
        "all_14_principal_star_source_profiles_documented":True,
        "Life_auxiliary_sources_still_incomplete":True,
        "real_human_blind_predictions_validated":0,
        "runtime_astrology_promotions":0
    }
    save(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
