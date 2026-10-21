#!/usr/bin/env python3
"""Guarded append of Zi Wei Servants documentary notes; no runtime predictions."""
from __future__ import annotations
import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V22.json"
NEW = T / "CHINESE_SOURCE_AUDIT_INDEX_V23.json"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR = T / "batches/ChineseAstro-22SRC-Travel/ZIWEI_TRAVEL_26_SOURCE_NOTES_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_23SRC_SERVANTS.md"
REC = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"
NOTES = B / "ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json"
WIT = B / "SOURCE_SERVANTS_26_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_SERVANTS_EXACT_EXCERPT.txt"
LEASE = B / "WRITER_LEASE.json"
BRANCH = "research/astro-chinese-v23-ziwei-servants-original-source-20261021"
PREV_SHA = "3c3d74b9f53d10e7905f026733d902511bf19f2f0f64ae34bed9f4af894bba68"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"

def sha(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()

def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def write(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def unchanged(p: Path) -> None:
    rel = p.relative_to(ROOT).as_posix()
    if git("rev-parse", "HEAD:" + rel) != git("hash-object", str(p)):
        raise ValueError("Previously accepted document changed: " + rel)

def main() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("Wrong writer branch")
    lease = read(LEASE)
    if lease["status"] != "active" or lease["owned_branch"] != BRANCH:
        raise ValueError("Writer lease missing or inactive")
    if any(x.exists() for x in (NEW, LATEST, REC, RECEIPT)):
        raise ValueError("Existing interrupted V23 append: inspect rather than overwrite")
    for p, expected in ((OLD, PREV_SHA), (RAW, RAW_SHA), (WEST, WEST_SHA)):
        if sha(p) != expected:
            raise ValueError("Pinned source SHA changed: " + str(p))
    for p in (OLD, RAW, WEST, PRIOR, CURRENT):
        unchanged(p)
    old = read(OLD)
    doc = read(NOTES)
    witness = read(WIT)
    accept = read(B / "ACCEPTANCE.json")
    archive = read(B / "SOURCE_RELEASE_RECEIPT_20261021.json")
    if old["sum_source_annotations"] != 1120 or old["original_chinese_source_anchors_checked_against_revision"] != 1048:
        raise ValueError("Expected accepted V22 source count differs")
    if old["accepted_batches"][-1]["id"] != "ChineseAstro-22SRC-Travel":
        raise ValueError("Old source batch identity changed")
    if [(x["accepted_source_annotations"], x["next_id"]) for x in old["systems"]] != [(210, "BZI-R0211"), (910, "ZWD-R0911")]:
        raise ValueError("Accepted prior BaZi/Zi Wei frontier changed")
    if len(doc["records"]) != 26 or len(witness["records"]) != 26:
        raise ValueError("Historical source records or witness incomplete")
    if [x["id"] for x in doc["records"]] != [f"ZWD-R{i:04d}" for i in range(911, 937)]:
        raise ValueError("Duplicate/gapped historical record IDs")
    if doc["source_excerpt_cp_range"] != [43499, 44429] or doc["next_id"] != "ZWD-R0937":
        raise ValueError("Source section boundary misaligned")
    if any(x["human_predictive_validations"] or x["runtime_promotions"] for x in doc["records"]):
        raise ValueError("Historical source promoted as human prediction")
    digests = (sha(NOTES), sha(WIT), sha(EXCERPT))
    if (accept["source_notes_sha256"], accept["source_witness_sha256"], accept["original_excerpt_sha256"]) != digests:
        raise ValueError("Frozen source SHA mismatch")
    if not archive["ZIP_CRC_verified"] or not archive["all_members_SHA256_bytes_verified"] or archive["cold_extracted_source_tests_green"] != 7:
        raise ValueError("Independent archive proof incomplete")
    destination = Path(archive["local_archive_path"])
    if not destination.is_file() or sha(destination) != archive["archive_SHA256"]:
        raise ValueError("Original source ZIP changed since verified")
    REC.mkdir(exist_ok=False)
    for p, filename in ((OLD, "CHINESE_V22_BEFORE_23.json"),
                        (CURRENT, "CHINESE_CURRENT_BEFORE_23.md"),
                        (WEST, "WESTERN_B07bc_BEFORE_23.json")):
        (REC / filename).write_bytes(p.read_bytes())
    new = copy.deepcopy(old)
    new.update({
        "schema": "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V23",
        "status": "ZIWEI_SERVANTS_ORIGINAL_ONLINE_TEXT_DOCUMENTED_NEXT_CAREER",
        "as_of_utc": "2026-10-21",
        "prior_index": "CHINESE_SOURCE_AUDIT_INDEX_V22.json",
        "prior_index_sha256": PREV_SHA,
        "sum_source_annotations": 1146,
        "original_chinese_source_anchors_checked_against_revision": 1074,
        "full_ziwei_original_text_collation_finished": False,
        "ziwei_complete_natal_calendar_engine_verified": False,
        "chinese_bazi_solar_term_engine_verified": False,
        "independently_validated_real_human_claims": 0,
        "runtime_promotions": 0,
    })
    new["accepted_batches"].append({
        "id": "ChineseAstro-23SRC-Servants",
        "added_bazi_source_annotations": 0,
        "added_ziwei_source_annotations": 26,
        "original_heading_lines": 1,
        "historical_star_or_combination_lines": 24,
        "following_Career_navigation_only": 1,
        "start": "ZWD-R0911", "end": "ZWD-R0936",
        "path": NOTES.relative_to(T).as_posix(),
        "rules_sha256": digests[0],
        "witness_path": WIT.relative_to(T).as_posix(),
        "witness_sha256": digests[1],
        "original_excerpt_path": EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256": digests[2],
        "source_oldid": 1963110,
        "original_raw_full_Wikitext_SHA256": RAW_SHA,
        "source_original_codepoint_range": [43499, 44429],
        "next_original_source_heading": "===九官禄===",
        "historical_class_servitude_stereotypes_are_unverified": True,
        "original_Ming_woodblock_printing_independently_authenticated": False,
        "source_cold_tests_green": 7,
        "independent_real_human_pred_validations": 0,
        "runtime_astrological_promotions": 0,
    })
    ziwei = new["systems"][1]
    ziwei["accepted_source_annotations"] = 936
    ziwei["current_ids"] = "ZWD-R0001–ZWD-R0936"
    ziwei["next_id"] = "ZWD-R0937"
    ziwei["current_batch"] = "ChineseAstro-23SRC-Servants"
    ziwei["source_files"].append(NOTES.relative_to(T).as_posix())
    ziwei["chapter_coverage"] = (
        "Transmitted Zi Wei Volume II Wikitext oldid1963110 source-covered Life, Brothers, "
        "Spouses, Children, Wealth, Disease, Travel and now Servants 奴仆 cp43499–44429: "
        "25 literal original lines (heading + 24 conditional star-group passages) and "
        "a subsequent Career navigation-only marker. The master/servant hierarchy, "
        "trustworthiness and theft accusations are historical social stereotypes "
        "not observed modern personnel behavior, diagnostic facts or predictions. "
        "Original Ming printing, whole twelve-palace critical collation, "
        "traditional natal engine and untouched person studies unverified."
    )
    new["next"] = (
        "Next original Zi Wei Career/Officials 官禄 cp44429, first source ZWD-R0937. "
        "BaZi original Di Tian Sui section19 BZI-R0211 remains pending. "
        "Independent early source comparison, natal-engine parity and human tests still OPEN."
    )
    new["historical_glyph_and_translator_limits"] = (
        "Online original transmitted Wikitext oldid1963110 is not authenticated "
        "classical Ming woodblock; Servants claims about class, labor, "
        "loyalty and stealing are period narrative not modern psychological data."
    )
    if new["systems"][0] != old["systems"][0] or new["accepted_batches"][:-1] != old["accepted_batches"]:
        raise ValueError("Prior Chinese/BaZi accepted source changed")
    if sum(x["accepted_source_annotations"] for x in new["systems"]) != 1146:
        raise ValueError("Cumulative Chinese documentary count inconsistent")
    write(NEW, new)
    heading = (
        "# Chinese V23 — original Zi Wei Servants historical source\n\n"
        "**26 new source-only notes ZWD-R0911–R0936**, from online transmitted "
        "Wikitext Servants section cp43499–44429; original class/trustworthiness "
        "stereotypes documented without modern personnel advice. "
        "**BaZi210 + ZiWei936 =1146 historical text annotations**, not humans. "
        "Seven focused original-source tests and seven independent ZIP replay tests "
        "were verified. Next **ZWD-R0937 Career/Officials cp44429** and "
        "**BZI-R0211 Di Tian Sui section19**. Historical printed edition "
        "authenticity, natal-chart engine and genuine blinded human validation all "
        "OPEN. Human predictive validations **0**; runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(
        heading + "## Previous accepted Chinese V22 source checkpoint\n\n"
        + (REC/"CHINESE_CURRENT_BEFORE_23.md").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    LATEST.write_text(
        heading + (B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    receipt = {
        "batch": "ChineseAstro-23SRC-Servants",
        "status": "GUARDED_V23_ORIGINAL_WIKITEXT_SOURCE_LOCAL_ACCEPTANCE",
        "Chinese_before": 1120,
        "Chinese_after": 1146,
        "BaZi_unchanged": 210,
        "ZiWei_before": 910,
        "ZiWei_after": 936,
        "first_ZWD": "ZWD-R0911",
        "last_ZWD": "ZWD-R0936",
        "next_ZWD": "ZWD-R0937",
        "next_BaZi": "BZI-R0211",
        "previous_index_V22_SHA256": PREV_SHA,
        "new_index_V23_SHA256": sha(NEW),
        "full_online_source_SHA256": RAW_SHA,
        "source_notes_SHA256": digests[0],
        "source_witness_SHA256": digests[1],
        "original_excerpt_SHA256": digests[2],
        "portable_archive_SHA256": archive["archive_SHA256"],
        "cold_extracted_source_tests_green": 7,
        "old_inherited_Western_B07bc_SHA256": WEST_SHA,
        "original_printed_Ming_source_authenticated": False,
        "human_blind_predictive_validations": 0,
        "runtime_astrology_promotions": 0,
    }
    write(RECEIPT, receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
