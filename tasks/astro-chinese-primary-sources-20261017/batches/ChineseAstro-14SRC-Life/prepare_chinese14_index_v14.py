#!/usr/bin/env python3
"""Guarded original Chinese source V14 aux-star text append, not natal predictor."""
from __future__ import annotations
import copy,json,subprocess
from hashlib import sha256
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V14.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_14SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-chinese-v14-ziwei-life-aux-first-four-20261020"
OLD_SHA="4695dea848caacac65f4cd9d0baebf1a85a26b022ba8414b83aecc6ca5c13682"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def checksum(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*a):return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
def ensure_unchanged(p):
    rel=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Previously accepted source file changed: "+rel)

def accept():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Wrong isolated original source V14 worktree")
    if any(p.exists() for p in (NEW,REC,RECEIPT,LATEST)):
        raise ValueError("Interrupted original source admission: reconcile existing files")
    index=rd(OLD)
    source=rd(B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json")
    witness=rd(B/"SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json")
    acceptmeta=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if checksum(OLD)!=OLD_SHA or index["sum_source_annotations"]!=738:
        raise ValueError("Original previous accepted V13 Chinese index SHA drift")
    if [(p["accepted_source_annotations"],p["next_id"]) for p in index["systems"]] !=[
        (210,"BZI-R0211"),(528,"ZWD-R0529")
    ] or index["accepted_batches"][-1]["id"]!="ChineseAstro-13SRC-Life":
        raise ValueError("Accepted prior BaZi/ZiWei source frontier moved")
    if index["original_chinese_source_anchors_checked_against_revision"]!=666:
        raise ValueError("Previous exact quote provenance count changed")
    if index["independently_validated_real_human_claims"] or index["runtime_promotions"]:
        raise ValueError("Previous source wrongly promoted human prediction claims")
    if checksum(RAW)!=RAW_SHA or RAW.stat().st_size!=106736:
        raise ValueError("Original Wikitext source SHA or bytes unexpected")
    if len(source["records"])!=58 or len(witness["original_quotes"])!=58:
        raise ValueError("Original 58 source note/offset witnesses missing")
    if [r["id"] for r in source["records"]] != [
        f"ZWD-R{n:04d}" for n in range(529,587)
    ]:
        raise ValueError("Original IDs not consecutive")
    if (source["next_id"],source["source_excerpt_start_codepoint"],
        source["source_excerpt_end_codepoint_exclusive"])!=(
        "ZWD-R0587",30135,31937
    ):
        raise ValueError("Original text exact source span wrong")
    if (not source["YouBi_distinct_female_poem_heading_absent_from_original"]
        or not source["ZuoFu_YouBi_separate_palace_grade_rows_absent_from_original"]
        or source["original_full_Life_palace_text_completed"]):
        raise ValueError("Original source absent female/grade/auxiliary status overstated")
    hashes=(
       checksum(B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"),
       checksum(B/"SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json"),
       checksum(B/"SOURCE_1963110_LIFE_FIRST_FOUR_AUX_EXACT_EXCERPT.txt")
    )
    if (acceptmeta["source_notes_SHA256"],acceptmeta["source_witness_SHA256"],
        acceptmeta["source_excerpt_SHA256"])!=hashes:
        raise ValueError("Frozen Chinese source notes/UTF8 byte witnesses changed")
    if not archive["ZIP_CRC_verified"] or not archive["each_member_hash_and_size_verified"]:
        raise ValueError("Cold ZIP source hash/CRC not verified")
    if (archive["independent_cold_source_tests_executed"],
        archive["independent_cold_source_tests_green"])!=(13,13):
        raise ValueError("Cold source test suite was not 13/13 green")
    portable=Path(archive["archive_path_on_owner_computer"])
    if not portable.exists() or checksum(portable)!=archive["archive_sha256"]:
        raise ValueError("Original archived source evidence SHA drift")
    west=rd(WEST)
    if (west["records_count"],west["batches"][-1]["id"])!=(13044,"B07bc"):
        raise ValueError("Separate old Western source snapshot changed")
    for p in (
        OLD,T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json",T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json",
        RAW,T/"batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
        T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",WEST
    ):
        ensure_unchanged(p)
    if any(row["genuine_human_predictions_validated"] or row["runtime_astrology_promotions"]
           for row in source["records"]):
        raise ValueError("Historical source can't be claimed empirical human validation")
    REC.mkdir(exist_ok=False)
    for p,n in (
        (OLD,"CHINESE_V13_BEFORE_14.json"),
        (CURRENT,"CHINESE_CURRENT_BEFORE_14.md"),
        (WEST,"WESTERN_B07bc_BEFORE_14.json")
    ):
        (REC/n).write_bytes(p.read_bytes())
    new=copy.deepcopy(index)
    new["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V14"
    new["status"]="ZIWEI_LIFE_PALACE_FOUR_FIRST_AUXILIARY_STAR_SOURCE_PROFILES_PARTIAL"
    new["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V13.json"
    new["prior_index_sha256"]=OLD_SHA
    new["as_of_utc"]="2026-10-20"
    new["sum_source_annotations"]=796
    new["original_chinese_source_anchors_checked_against_revision"]=724
    new["accepted_batches"].append({
       "id":"ChineseAstro-14SRC-Life",
       "added_bazi_source_annotations":0,"added_ziwei_source_annotations":58,
       "start":"ZWD-R0529","end":"ZWD-R0586",
       "path":"batches/ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json",
       "rules_sha256":hashes[0],
       "witness_path":"batches/ChineseAstro-14SRC-Life/SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json",
       "witness_sha256":hashes[1],
       "original_excerpt_path":"batches/ChineseAstro-14SRC-Life/SOURCE_1963110_LIFE_FIRST_FOUR_AUX_EXACT_EXCERPT.txt",
       "original_excerpt_sha256":hashes[2],
       "source_oldid":1963110,"source_raw_full_sha256":RAW_SHA,
       "original_auxiliary_star_groups_native":["文昌","文曲","左辅","右弼"],
       "original_star_source_line_counts":[16,18,13,10],
       "ZuoFu_YouBi_no_separate_palace_grade_rows":True,
       "YouBi_no_female_poem_heading":True,
       "next_unstudied_auxiliary_star":"禄存",
       "full_Life_palace_original_text_still_incomplete":True,
       "ancient_Ming_original_imprint_authenticity_unverified":True,
       "cold_source_test_replays":13,
       "actual_human_predictions_validated":0,"runtime_model_promotions":0
    })
    new["systems"][1]["accepted_source_annotations"]=586
    new["systems"][1]["current_ids"]="ZWD-R0001–ZWD-R0586"
    new["systems"][1]["next_id"]="ZWD-R0587"
    new["systems"][1]["current_batch"]="ChineseAstro-14SRC-Life"
    new["systems"][1]["source_files"].append(
        "batches/ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"
    )
    new["systems"][1]["chapter_coverage"]=(
        "Transmitted original Zi Wei Volume II source Life-palace text: "
        "first 14 principal-star profiles source-annotated in V10–V13, "
        "now first four auxiliary stars WenChang, WenQu, ZuoFu, YouBi in "
        "V14 original cp30135–31937, 57 new literal text lines plus "
        "LuCun next navigation. Original ZuoFu/YouBi have no independent "
        "palace-grade table, YouBi no dedicated female verse. Remaining "
        "auxiliary profiles to Brothers heading original cp37269 OPEN. "
        "Not authenticated ancient printed source, complete natal birth "
        "chart or real-person predictive/medical evidence."
    )
    if new["systems"][0]!=index["systems"][0] or new["accepted_batches"][:-1]!=index["accepted_batches"]:
        raise ValueError("Original BaZi or prior ZiWei historical records altered")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=796:
        raise ValueError("Total new original Chinese source count inconsistent")
    new["separate_lilly_source_count_at_this_revision"]=13044
    new["separate_ptolemy_source_count_at_this_revision"]=1066
    new["source_parallel_western_history_binding"]=(
        "Independent original Chinese source branch retains Western B07bc "
        "original source snapshot Lilly13044+Ptolemy1066 byte-exact. "
        "More recent Western B07bg Lilly13236+Ptolemy1066 is a separate "
        "accepted research branch, not merged with this original Chinese "
        "source index. Cross-branch documentary total is not empirical validation."
    )
    new["full_ziwei_original_text_collation_finished"]=False
    new["all_14_principal_stars_verified"]=False
    new["ziwei_complete_natal_calendar_engine_verified"]=False
    new["chinese_bazi_solar_term_engine_verified"]=False
    new["historical_glyph_and_translator_limits"]=(
        "Simplified Chinese transmitted Wikitext oldid1963110 not independently "
        "original printed Ming text or critically translated. Original "
        "star profiles including first four auxiliary stars documented "
        "with exact textual offsets, but original source interpretations "
        "are not human outcomes, medical social/moral facts, complete "
        "auxiliary star placement/calendar or predictive accuracy. "
        "Missing ZuoFu/YouBi grades and YouBi female verse are explicit original omissions."
    )
    new["independently_validated_real_human_claims"]=0
    new["runtime_promotions"]=0
    new["next"]=(
        "Zi Wei Life-palace next original auxiliary Lu Cun 禄存 source "
        "cp31937, ZWD-R0587. Remaining original star interpretation "
        "passages to Brothers/Siblings heading cp37269 and other 11 "
        "house text areas unstudied. BaZi source next Di Tian Sui "
        "section19 BZI-R0211 unchanged. Real prospective/reverse blind "
        "human predictive tests against decoys and nonastrology baselines "
        "require independently verified birth-time/house model and "
        "preregistered source mapping before inspecting participants."
    )
    wr(NEW,new)
    header=(
        "# Chinese V14 — first four auxiliary Zi Wei Life-palace star profiles\n\n"
        "**58 source-only historical notes ZWD-R0529–ZWD-R0586**: "
        "WenChang16 WenQu18 ZuoFu13 YouBi10 exact original text lines "
        "plus one LuCun next-source prefix only. Source Wikitext oldid1963110 "
        "has exact UTF8 quote codepoint/byte offsets and hashes, but lacks "
        "separate palace-grade rows for ZuoFu/YouBi and dedicated YouBi "
        "female poem heading. Never fabricate. The source's other "
        "auxiliary profiles remain open to original Brothers heading cp37269, "
        "old Ming printing unverified. **Chinese BaZi210 +ZiWei586 =796** "
        "historical source notes. Separate Western B07bg Lilly13236 + "
        "Ptolemy1066 gives aggregate **15,098** documentary annotations "
        "across independent branches; **not** real-person prediction hits. "
        "Next **ZWD-R0587 LuCun**, **BZI-R0211 Di Tian Sui**. "
        "Independent human blind tests **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(
        header+"## Prior accepted Chinese original-source checkpoint retained\n\n"+
        CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(header+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
      "batch":"ChineseAstro-14SRC-Life",
      "status":"GUARDED_ORIGINAL_CHINESE_V14_AUXILIARY_58_ACCEPTED_LOCAL_REMOTE_PENDING",
      "Chinese_before":738,"Chinese_after":796,
      "BaZi_retained":210,"ZiWei_before":528,"ZiWei_after":586,
      "new_original_source_records":58,
      "first_ZWD":"ZWD-R0529","last_ZWD":"ZWD-R0586",
      "next_ZWD":"ZWD-R0587","next_BZI":"BZI-R0211",
      "original_full_source_oldid":1963110,
      "original_source_SHA256":RAW_SHA,
      "old_V13_index_SHA256":checksum(REC/"CHINESE_V13_BEFORE_14.json"),
      "new_V14_index_SHA256":checksum(NEW),
      "original_source_notes_SHA256":hashes[0],
      "original_source_witness_SHA256":hashes[1],
      "source_excerpt_SHA256":hashes[2],
      "portable_source_archive_SHA256":archive["archive_sha256"],
      "independent_cold_source_tests_green":13,
      "Western_parent_B07bc_Lilly":13044,
      "Western_parent_B07bc_Ptolemy":1066,
      "newer_separate_Western_B07bg_Lilly":13236,
      "aggregate_historical_source_counts_across_separate_branches":15098,
      "YouBi_female_verse_source_omission_preserved":True,
      "ZuoFu_YouBi_grade_rows_omitted_in_transmitted_source":True,
      "human_blind_validations":0,
      "runtime_astrological_promotions":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":accept()
