#!/usr/bin/env python3
"""Guarded Chinese source V10 append; original V9 and Western untouched."""
from __future__ import annotations

import copy
import json
import subprocess
from hashlib import sha256
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V9.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_10SRC_LIFE.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
OLD_SHA="b84922b8614017fb20403f1556a885f2b3d8ed55314566140d67109e4c2022ad"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
BRANCH="research/astro-chinese-v10-ziwei-life-first-four-20261020"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def check_original_unchanged(p):
    rel=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Accepted original source changed: "+rel)

def accept():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Chinese source admission on wrong branch")
    if any(p.exists() for p in (NEW,REC,RECEIPT,LATEST)):
        raise ValueError("Interrupted prior V10 admission: reconcile")
    old=rd(OLD)
    src=rd(B/"ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json")
    witness=rd(B/"SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json")
    meta=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if sha(OLD)!=OLD_SHA or old["sum_source_annotations"]!=430:
        raise ValueError("Canonical Chinese V9 original source mutated")
    if [x["accepted_source_annotations"] for x in old["systems"]] != [210,220]:
        raise ValueError("Chinese BaZi/ZiWei source counts changed")
    if [x["next_id"] for x in old["systems"]] != ["BZI-R0211","ZWD-R0221"]:
        raise ValueError("Expected original next source IDs changed")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-09" or old["original_chinese_source_anchors_checked_against_revision"]!=358:
        raise ValueError("Accepted V9 original source provenance changed")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Source does not carry empirical outcomes")
    if sha(RAW)!=RAW_SHA or RAW.stat().st_size!=106736:
        raise ValueError("Frozen Chinese Wikitext original SHA/bytes changed")
    if len(src["records"])!=89 or len(witness["exact_source_quote_provenance"])!=89:
        raise ValueError("Source quotes and provenance incomplete")
    if [r["id"] for r in src["records"]] != [f"ZWD-R{i:04d}" for i in range(221,310)]:
        raise ValueError("New Life palace IDs not consecutive")
    if (src["next_id"]!="ZWD-R0310" or not src["only_four_of_many_life_palace_stars_covered"]
        or src["all_life_palace_section_covered"]):
        raise ValueError("Life Palace original text scope overstated")
    expected=(
        sha(B/"ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"),
        sha(B/"SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json"),
        sha(B/"SOURCE_1963110_LIFE_PALACE_FIRST_FOUR_EXACT_EXCERPT.txt")
    )
    provided=(meta["source_notes_sha256"],meta["source_offset_witness_sha256"],meta["source_excerpt_sha256"])
    if provided!=expected:
        raise ValueError("Original quote/witness/excerpt SHA drift")
    if not archive["ZIP_CRC_validated"] or not archive["ZIP_member_SHA_and_bytes_validated"]:
        raise ValueError("Source ZIP CRC/bytes not independently tested")
    if archive["independently_extracted_test_count"]!=17 or not archive["independently_extracted_tests_all_green"]:
        raise ValueError("Independent cold source tests 17/17 not verified")
    portable=Path(archive["archive_path_on_owner_machine"])
    if not portable.is_file() or sha(portable)!=archive["archive_sha256"]:
        raise ValueError("Cold-source archive SHA changed")
    west=rd(WEST)
    if (west["records_count"],west["batches"][-1]["id"])!=(13044,"B07bc"):
        raise ValueError("Previous V9 parallel Western snapshot changed")
    for p in (OLD,T/"CHINESE_SOURCE_AUDIT_INDEX_V8.json",
              T/"CHINESE_SOURCE_AUDIT_INDEX_V7.json",RAW,
              T/"batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json",
              T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",WEST):
        check_original_unchanged(p)
    if any(r["runtime_astrological_rule_promoted"] or
           r["independent_human_personality_relationship_or_fate_validation"] or
           r["predictions_issued_to_blind_real_people"] for r in src["records"]):
        raise ValueError("Cannot count historical text as predictive evidence")
    REC.mkdir(exist_ok=False)
    for p,name in ((OLD,"CHINESE_V9_BEFORE_10.json"),
                   (CURRENT,"CHINESE_CURRENT_BEFORE_10.md"),
                   (WEST,"WESTERN_B07bc_BEFORE_10.json")):
        (REC/name).write_bytes(p.read_bytes())
    new=copy.deepcopy(old)
    new["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V10"
    new["status"]="ZIWEI_LIFE_PALACE_FIRST_FOUR_STAR_SOURCE_ONLY_PARTIAL"
    new["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V9.json"
    new["prior_index_sha256"]=OLD_SHA
    new["as_of_utc"]="2026-10-20"
    new["sum_source_annotations"]=519
    new["original_chinese_source_anchors_checked_against_revision"]=447
    new["accepted_batches"].append({
        "id":"ChineseAstro-10SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":89,
        "start":"ZWD-R0221","end":"ZWD-R0309",
        "path":"batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
        "rules_sha256":expected[0],
        "witness_path":"batches/ChineseAstro-10SRC-Life/SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json",
        "witness_sha256":expected[1],
        "original_excerpt_path":"batches/ChineseAstro-10SRC-Life/SOURCE_1963110_LIFE_PALACE_FIRST_FOUR_EXACT_EXCERPT.txt",
        "original_excerpt_sha256":expected[2],
        "source_oldid":1963110,
        "source_raw_full_sha256":RAW_SHA,
        "original_star_groups_native":["紫微","天机","太阳","武曲"],
        "star_original_source_line_counts":[22,20,24,22],
        "next_unstudied_star":"天同",
        "full_Life_palace_section_not_complete":True,
        "source_original_early_Ming_woodblock_edition_authenticated":False,
        "portable_cold_extracted_source_test_replays":17,
        "human_predictive_validations":0,
        "runtime_astrological_promotions":0,
    })
    new["systems"][1]["accepted_source_annotations"]=309
    new["systems"][1]["current_ids"]="ZWD-R0001–ZWD-R0309"
    new["systems"][1]["next_id"]="ZWD-R0310"
    new["systems"][1]["current_batch"]="ChineseAstro-10SRC-Life"
    new["systems"][1]["source_files"].append(
        "batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"
    )
    new["systems"][1]["chapter_coverage"]=(
        "Transmitted Zi Wei Volume II original Wikitext oldid1963110 through "
        "prior four source diagrams, and now PARTIAL Life-palace prose for "
        "exactly four first star groups: 紫微(22 original lines), 天机(20), "
        "太阳(24), 武曲(22), plus one 天同 boundary source marker. "
        "89 codepoint/UTF8-byte-offset SHA-anchored source-only records. "
        "All subsequent Life-palace stars and the other eleven houses are "
        "still unstudied. Early actual printed Ming source, independent "
        "traditional calendar and real human natal predictions unverified."
    )
    if new["systems"][0]!=old["systems"][0] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Old BaZi source or accepted Chinese historical batches rewritten")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=519:
        raise ValueError("V10 Chinese original historical total must be519")
    new["separate_lilly_source_count_at_this_revision"]=13044
    new["separate_ptolemy_source_count_at_this_revision"]=1066
    new["source_parallel_western_history_binding"]=(
        "Independent source V10 starts from accepted Chinese V9 old Western B07bc "
        "snapshot with 13,044 Lilly+1,066 Ptolemy, unchanged bytewise. "
        "A DIFFERENT later accepted Western B07bg branch has 13,236 Lilly; "
        "do not pretend this Chinese source branch merges it."
    )
    new["full_ziwei_original_text_collation_finished"]=False
    new["all_14_principal_stars_verified"]=False
    new["ziwei_complete_natal_calendar_engine_verified"]=False
    new["chinese_bazi_solar_term_engine_verified"]=False
    new["historical_glyph_and_translator_limits"]=(
        "Simplified Chinese transmitted Wikitext revision1963110 is not an "
        "authenticated early printed Ming original or critical professional "
        "translation. Original four Life-palace star sections include "
        "conditional fortune, bodily, sex/gender stereotypes, mortality and "
        "medical claims as HISTORICAL WORDING only, not scientific truth. "
        "Verse encounter 遇 must not be silently equated to exact same-degree "
        "同度; no model likelihoods or real-human predictive results."
    )
    new["independently_validated_real_human_claims"]=0
    new["runtime_promotions"]=0
    new["next"]=(
        "Zi Wei Life-palace next Tian Tong substantive source at original "
        "codepoint22909, next ZWD-R0310, through remaining first section "
        "before siblings ===二兄弟=== codepoint37269. "
        "BaZi Di Tian Sui section19 source next BZI-R0211 unchanged. "
        "Source original astrology and historic calendar/chart model not "
        "fully verified; preregister untouched real-human tests against "
        "matched charts/decoys and nonastrology baseline before responses."
    )
    wr(NEW,new)
    header=(
        "# Chinese source V10 — first four Zi Wei Life-palace original profiles\n\n"
        "**89 historical source-only annotations ZWD-R0221–ZWD-R0309** "
        "(88 original lines for ZiWei/TianJi/TaiYang/WuQu and 1 next "
        "TianTong navigation marker) each original exact Unicode codepoint "
        "and UTF8 source byte offset/SHA independently verified against "
        "Wikitext oldid1963110. This is PARTIAL Life-palace text, "
        "not authentic Ming woodblock or real-person predictive evidence. "
        "Old fortune/body/sex/mortality claims have no human validations. "
        "**Chinese BaZi210 unchanged + ZiWei309 =519** source notes; "
        "Western accepted B07bg Lilly13236+Ptolemy1066 lives on separate "
        "branch (aggregate source counts **14,821**, not merged). "
        "Inherited Western B07bc historical snapshot remains unmodified. "
        "Next **ZWD-R0310 TianTong**, original codepoint22909, "
        "**BZI-R0211** Di Tian Sui section19. "
        "Human real prospective/reverse blind tests **0**, "
        "runtime astro rules promoted **0**.\n\n"
    )
    CURRENT.write_text(header+"## Previous accepted historical source retained\n\n"+
                       CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(header+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
        "batch":"ChineseAstro-10SRC-Life",
        "status":"GUARDED_SOURCE_V10_89_ACCEPTED_LOCALLY_REMOTE_PENDING",
        "Chinese_before":430,"Chinese_after":519,
        "BaZi_before_after":210,"ZiWei_before":220,"ZiWei_after":309,
        "new_source_only_notes":89,
        "first_ZWD":"ZWD-R0221","last_ZWD":"ZWD-R0309",
        "next_ZWD":"ZWD-R0310","next_BZI":"BZI-R0211",
        "transmitted_source_original_oldid":1963110,
        "source_full_wikitext_SHA256":RAW_SHA,
        "old_V9_index_SHA256":sha(REC/"CHINESE_V9_BEFORE_10.json"),
        "new_V10_index_SHA256":sha(NEW),
        "source_note_SHA256":expected[0],
        "source_quote_witness_SHA256":expected[1],
        "source_excerpt_SHA256":expected[2],
        "cold_ZIP_SHA256":archive["archive_sha256"],
        "cold_source_tests_replayed":17,
        "parallel_old_Western_B07bc_Lilly":13044,
        "parallel_old_Western_B07bc_Ptolemy":1066,
        "latest_distinct_Western_B07bg_Lilly":13236,
        "parallel_Western_bytes_unchanged":True,
        "genuine_real_human_predictive_tests":0,
        "runtime_astrological_promotions":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,indent=2,ensure_ascii=False))

if __name__=="__main__":
    accept()
