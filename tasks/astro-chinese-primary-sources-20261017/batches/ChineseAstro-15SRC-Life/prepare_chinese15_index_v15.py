#!/usr/bin/env python3
"""Guarded append of Chinese V15 historical original source; no human model."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = TASK / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
NEW = TASK / "CHINESE_SOURCE_AUDIT_INDEX_V15.json"
RAW = TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
V14_NOTES = TASK / "batches/ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_15SRC_LIFE.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"
BRANCH = "research/astro-chinese-v15-lucun-kuiyue-qingyang-tuoluo-20261021"
OLD_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
SOURCE = B / "ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_LIFE_SECOND_FOUR_AUXILIARY_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, v: object) -> None:
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def unchanged_in_head(p: Path) -> None:
    rel = p.relative_to(ROOT).as_posix()
    if git("rev-parse", "HEAD:" + rel) != git("hash-object", str(p)):
        raise ValueError("Previously accepted source content modified: " + rel)


def main() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("Wrong worktree/branch for V15 source acceptance")
    if any(p.exists() for p in (NEW, LATEST, RECOVERY, RECEIPT)):
        raise ValueError("V15 interrupted index append; reconcile existing new artifacts")
    if sha(OLD) != OLD_SHA or sha(RAW) != RAW_SHA or sha(WEST) != WEST_SHA:
        raise ValueError("Immutable source or accepted index SHA mismatch")
    for p in (OLD, RAW, WEST, V14_NOTES, CURRENT):
        unchanged_in_head(p)
    before = read(OLD)
    source = read(SOURCE)
    witness = read(WITNESS)
    accept = read(B / "ACCEPTANCE.json")
    archive = read(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261021.json")
    if (before["sum_source_annotations"], before["original_chinese_source_anchors_checked_against_revision"]) != (796, 724):
        raise ValueError("Expected preaccepted V14 source counters absent")
    if before["accepted_batches"][-1]["id"] != "ChineseAstro-14SRC-Life":
        raise ValueError("Old index batch head changed")
    if [(x["accepted_source_annotations"], x["next_id"]) for x in before["systems"]] != [
        (210, "BZI-R0211"), (586, "ZWD-R0587")
    ]:
        raise ValueError("Accepted Chinese source frontiers changed")
    if before["independently_validated_real_human_claims"] or before["runtime_promotions"]:
        raise ValueError("Existing source notes are not verified human predictions")
    if len(source["records"]) != 54 or len(witness["original_quotes"]) != 54:
        raise ValueError("Missing 54 exact Chinese source annotations/witnesses")
    if [r["id"] for r in source["records"]] != [f"ZWD-R{i:04d}" for i in range(587,641)]:
        raise ValueError("Source IDs not consecutive")
    if (source["source_excerpt_start_codepoint"], source["source_excerpt_end_codepoint_exclusive"]) != (31937,33783):
        raise ValueError("Original text source span does not match contiguous segments")
    if (source["next_id"], source["next_unstudied_original_codepoint"], source["next_unstudied_star"]) != ("ZWD-R0641",33783,"火星"):
        raise ValueError("Next exact source frontier inconsistent")
    if not all([source["QingYang_duplicate_original_male_verse_heading_preserved"],
        source["TuoLuo_female_verse_markup_gap_preserved"],
        source["KuiYue_absent_dedicated_male_female_time_headings_preserved"]]):
        raise ValueError("Original source anomalies silently normalized")
    if source["original_full_Life_palace_text_completed"] or source["original_Ming_woodblock_imprint_verified"]:
        raise ValueError("Historical source completion/authenticity misrepresented")
    for r in source["records"]:
        if r["genuine_human_predictions_validated"] or r["runtime_astrology_promotions"]:
            raise ValueError("Human validation/production promotion not supported")
    hashes = (sha(SOURCE), sha(WITNESS), sha(EXCERPT))
    if accept["source_notes_SHA256"] != hashes[0] or accept["source_excerpt_SHA256"] != hashes[2]:
        raise ValueError("Frozen source artifacts changed")
    if witness["excerpt_SHA256"] != hashes[2] or witness["full_original_source_SHA256"] != RAW_SHA:
        raise ValueError("Witness source SHA mismatch")
    if not archive["ZIP_CRC_verified"] or not archive["each_member_hash_and_size_verified"]:
        raise ValueError("Independent cold archive SHA/CRC not verified")
    if (archive["independent_cold_source_tests_executed"],archive["independent_cold_source_tests_green"]) != (13,13):
        raise ValueError("Independent extracted source tests not complete")
    package = Path(archive["archive_path_on_owner_computer"])
    if not package.is_file() or sha(package) != archive["archive_sha256"]:
        raise ValueError("Portable original-source archive SHA mismatch")
    if before["systems"][0]["accepted_source_annotations"] != 210:
        raise ValueError("BaZi notes are intentionally unchanged")

    RECOVERY.mkdir(exist_ok=False)
    for p,n in ((OLD,"CHINESE_V14_BEFORE_15.json"),
                (CURRENT,"CHINESE_CURRENT_BEFORE_15.md"),
                (WEST,"WESTERN_B07bc_BEFORE_15.json")):
        (RECOVERY/n).write_bytes(p.read_bytes())
    new = copy.deepcopy(before)
    new.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V15",
        "status":"ZIWEI_LIFE_PALACE_SECOND_FOUR_AUXILIARY_STAR_SOURCE_PROFILES_PARTIAL",
        "as_of_utc":"2026-10-21",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V14.json",
        "prior_index_sha256":OLD_SHA,
        "sum_source_annotations":850,
        "original_chinese_source_anchors_checked_against_revision":778,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0
    })
    new["accepted_batches"].append({
        "id":"ChineseAstro-15SRC-Life",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":54,
        "substantive_original_lines":53,
        "navigation_only_records":1,
        "start":"ZWD-R0587","end":"ZWD-R0640",
        "path":SOURCE.relative_to(TASK).as_posix(),
        "rules_sha256":hashes[0],
        "witness_path":WITNESS.relative_to(TASK).as_posix(),
        "witness_sha256":hashes[1],
        "original_excerpt_path":EXCERPT.relative_to(TASK).as_posix(),
        "original_excerpt_sha256":hashes[2],
        "source_oldid":1963110,"source_raw_full_sha256":RAW_SHA,
        "original_auxiliary_star_groups_native":["禄存","魁钺","擎羊","陀罗"],
        "original_star_source_line_counts":[14,6,17,16],
        "QingYang_original_male_heading_twice":True,
        "TuoLuo_female_verse_missing_opening_markup":True,
        "KuiYue_dedicated_sex_time_headings_absent":True,
        "next_unstudied_auxiliary_star":"火星",
        "full_Life_palace_original_text_still_incomplete":True,
        "ancient_Ming_original_imprint_authenticity_unverified":True,
        "cold_source_test_replays":13,
        "actual_human_predictions_validated":0,
        "runtime_model_promotions":0,
    })
    zw=new["systems"][1]
    zw["accepted_source_annotations"]=640
    zw["current_ids"]="ZWD-R0001–ZWD-R0640"
    zw["next_id"]="ZWD-R0641"
    zw["current_batch"]="ChineseAstro-15SRC-Life"
    zw["source_files"].append(SOURCE.relative_to(TASK).as_posix())
    zw["chapter_coverage"]=(
        "Transmitted oldid1963110 original Zi Wei Volume II Life-palace source; "
        "all 14 principal-star narrative profiles plus now eight auxiliary-star sections documented "
        "through TuoLuo original cp33783, with original absent gender/verse markup and duplicate "
        "QingYang male heading preserved. Original Life-palace remainder through Brothers cp37269, "
        "and eleven other house texts remain incompletely collated. Modern transmitted Wikitext "
        "not authenticated as early printed edition, not whole natal chart, and not human predictive evidence."
    )
    new["next"]=(
        "Zi Wei Life-palace original Huo Xing 火星 begins cp33783; first new substantive ZWD-R0641, "
        "remaining source through Brothers heading cp37269. BaZi Di Tian Sui section19 BZI-R0211 "
        "unchanged. Obtain independent birth chart/calendar parity, conceal prospective human "
        "behavior predictions then compare against chart-decoys/nonastrology baselines before "
        "making accuracy claims. Human forecast validations 0."
    )
    new["historical_glyph_and_translator_limits"]=(
        "Source is transmitted Simplified Chinese Wikitext oldid1963110, not authenticated Ming "
        "woodblock or independent scholarly critical translation. LuCun/KuiYue/QingYang/TuoLuo "
        "exact lines and source omissions documented; historical sex, mortality, legal and moral "
        "claims are period text, not modern advice, real-human data or predictive evidence."
    )
    new["source_parallel_western_history_binding"]=(
        "Chinese research branch preserves original inherited Western B07bc index source bytes "
        "Lilly13044+Ptolemy1066. Separate B07bh newer accepted Western branch reached "
        "Lilly13271+Ptolemy1066, while B07bi was independently in progress; do not merge "
        "unrelated source registries by changing an old inherited Western snapshot. "
        "Cross-branch document counts are not human predictive success."
    )
    if new["systems"][0] != before["systems"][0] or new["accepted_batches"][:-1] != before["accepted_batches"]:
        raise ValueError("Previously accepted Chinese BaZi/source batch history mutated")
    if sum(x["accepted_source_annotations"] for x in new["systems"]) != 850:
        raise ValueError("Chinese canonical count mismatch")
    save(NEW,new)
    header=(
        "# Chinese V15 — next four Zi Wei Life-palace auxiliary source profiles\n\n"
        "**54 new historical source-only annotations ZWD-R0587–ZWD-R0640**, covering Lu Cun 14, Kui Yue 6, Qing Yang 17 and Tuo Luo 16 literal Wikitext lines plus a single following Huo Xing navigation marker. "
        "Original Qing Yang duplicates a male-life heading; Tuo Luo female verse lacks opening poem markup; Kui Yue has combined source verse. "
        "No fabricated corrections. **BaZi210 + Zi Wei640 =850** Chinese source-only annotations; source Life-palace remains PARTIAL. "
        "The separate accepted Western B07bh Lilly13271 + Ptolemy1066=14337 belongs to a different branch, not this V15 index. "
        "Next **ZWD-R0641 火星 cp33783** and **BZI-R0211 Di Tian Sui section19**. "
        "Human blind validations **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(header + "## Previous accepted Chinese V14 original-source checkpoint\n\n" +
        (RECOVERY/"CHINESE_CURRENT_BEFORE_15.md").read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(header + (B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    meta={
        "batch":"ChineseAstro-15SRC-Life",
        "status":"GUARDED_ORIGINAL_CHINESE_V15_54_SOURCE_RECORDS_LOCAL_ACCEPTED",
        "Chinese_before":796,"Chinese_after":850,
        "BaZi_retained":210,"ZiWei_before":586,"ZiWei_after":640,
        "first_ZWD":"ZWD-R0587","last_ZWD":"ZWD-R0640",
        "next_ZWD":"ZWD-R0641","next_BZI":"BZI-R0211",
        "raw_source_revision":1963110,"raw_source_SHA256":RAW_SHA,
        "old_V14_index_SHA256":OLD_SHA,"new_V15_index_SHA256":sha(NEW),
        "source_notes_SHA256":hashes[0],"source_witness_SHA256":hashes[1],
        "source_excerpt_SHA256":hashes[2],
        "portable_archive_SHA256":archive["archive_sha256"],
        "independent_cold_source_tests_green":13,
        "inherited_Western_B07bc_SHA256":WEST_SHA,
        "retained_original_section_anomalies":True,
        "whole_original_Life_palace_covered":False,
        "human_blind_validations":0,"runtime_astrological_promotions":0
    }
    save(RECEIPT,meta)
    print(json.dumps(meta,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
