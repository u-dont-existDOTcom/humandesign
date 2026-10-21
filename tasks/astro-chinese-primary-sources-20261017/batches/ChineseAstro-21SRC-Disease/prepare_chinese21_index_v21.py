#!/usr/bin/env python3
"""Guarded append of V21 historical Chinese Disease text, not human predictions."""
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V20.json"
NEW = T / "CHINESE_SOURCE_AUDIT_INDEX_V21.json"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR = T / "batches/ChineseAstro-20SRC-Wealth/ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_21SRC_DISEASE.md"
REC = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"
SOURCE = B / "ZIWEI_DISEASE_25_SOURCE_NOTES_V1.json"
WIT = B / "SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_DISEASE_EXACT_EXCERPT.txt"
LEASE = B / "WRITER_LEASE.json"
BRANCH = "research/astro-chinese-v21-ziwei-disease-original-source-20261021"
OLD_SHA = "a6b051ed03f19f663d5a363af9a5c4efbf2ca2aea4997e94920023fdcf32f9b5"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def write(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def assert_previously_accepted_unchanged(p: Path) -> None:
    rel = p.relative_to(ROOT).as_posix()
    if git("rev-parse", "HEAD:" + rel) != git("hash-object", str(p)):
        raise ValueError("Prior accepted source mutated: " + rel)


def accept() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("Wrong isolated branch for V21 original source")
    lease = load(LEASE)
    if lease["status"] != "active" or lease["owned_branch"] != BRANCH:
        raise ValueError("V21 writer ownership not active")
    if any(p.exists() for p in (NEW, REC, LATEST, RECEIPT)):
        raise ValueError("Existing interrupted V21 admission; inspect before retry")
    for p, expected in ((OLD, OLD_SHA), (RAW, RAW_SHA), (WEST, WEST_SHA)):
        if sha(p) != expected:
            raise ValueError("Original online or accepted index SHA drift: " + str(p))
    for p in (OLD, RAW, WEST, PRIOR, CURRENT):
        assert_previously_accepted_unchanged(p)
    index = load(OLD)
    doc = load(SOURCE)
    witness = load(WIT)
    source_accept = load(B / "ACCEPTANCE.json")
    archive = load(B / "SOURCE_RELEASE_RECEIPT_20261021.json")
    if (index["sum_source_annotations"],
        index["original_chinese_source_anchors_checked_against_revision"]) != (1069, 997):
        raise ValueError("Old V20 Chinese counters do not match frozen parent")
    if index["accepted_batches"][-1]["id"] != "ChineseAstro-20SRC-Wealth":
        raise ValueError("Prior Chinese source head unexpected")
    if [(r["accepted_source_annotations"], r["next_id"]) for r in index["systems"]] != [
        (210, "BZI-R0211"), (859, "ZWD-R0860")
    ]:
        raise ValueError("Prior Chinese source sequence changed")
    if index["independently_validated_real_human_claims"] or index["runtime_promotions"]:
        raise ValueError("Source text is not clinical prediction data")
    if len(doc["records"]) != 25 or len(witness["source_quotes"]) != 25:
        raise ValueError("All V21 source notes and witnesses required")
    if [r["id"] for r in doc["records"]] != [f"ZWD-R{x:04d}" for x in range(860,885)]:
        raise ValueError("V21 R record IDs not consecutive")
    if doc["source_excerpt_codepoints"] != [41672, 42541] or doc["next_id"] != "ZWD-R0885":
        raise ValueError("Original chapter source boundaries changed")
    if not (doc["yangling_variant_preserved_not_emended"] and
        doc["yangling_literal_occurrences"] == 2 and
        doc["same_glyph_apparent_context_dependent_adverse_vs_favorable_tension_unresolved"]):
        raise ValueError("Original variant and qualifier not preserved")
    if doc["human_blind_predictions_validated"] or doc["runtime_astrology_promotions"] or doc["authentic_original_Ming_woodblock_collated"]:
        raise ValueError("Original text is neither authenticated older printing nor human outcome")
    digests = (sha(SOURCE), sha(WIT), sha(EXCERPT))
    if (source_accept["new_source_notes_sha256"], source_accept["source_witness_sha256"],
        source_accept["source_excerpt_sha256"]) != digests:
        raise ValueError("Source quote/excerpt hashes inconsistent")
    if witness["original_full_Wikitext_SHA256"] != RAW_SHA or witness["source_excerpt_SHA256"] != digests[2]:
        raise ValueError("Exact source witness drift")
    if not archive["ZIP_CRC_verified"] or not archive["all_member_SHA256_and_bytes_verified"] or archive["independent_cold_original_source_tests_green"] != 12:
        raise ValueError("Original source cold-archive tests not verified")
    p = Path(archive["archive_path_on_owner_computer"])
    if not p.is_file() or sha(p) != archive["archive_sha256"]:
        raise ValueError("Owner's reproducible archive SHA changed/missing")
    if any(r["real_human_predictions_validated"] or r["runtime_astrology_promotions"] for r in doc["records"]):
        raise ValueError("Unvalidated claims promoted")
    REC.mkdir(exist_ok=False)
    for p,name in (
        (OLD, "CHINESE_V20_BEFORE_21.json"),
        (CURRENT, "CHINESE_CURRENT_BEFORE_21.md"),
        (WEST, "WESTERN_B07bc_BEFORE_21.json")
    ):
        (REC / name).write_bytes(p.read_bytes())
    nxt = copy.deepcopy(index)
    nxt.update({
        "schema": "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V21",
        "status": "ZIWEI_DISEASE_ONLINE_SOURCE_ONLY_NEXT_TRAVEL_ALL_HOUSES_OPEN",
        "as_of_utc": "2026-10-21",
        "prior_index": "CHINESE_SOURCE_AUDIT_INDEX_V20.json",
        "prior_index_sha256": OLD_SHA,
        "sum_source_annotations": 1094,
        "original_chinese_source_anchors_checked_against_revision": 1022,
        "full_ziwei_original_text_collation_finished": False,
        "ziwei_complete_natal_calendar_engine_verified": False,
        "chinese_bazi_solar_term_engine_verified": False,
        "independently_validated_real_human_claims": 0,
        "runtime_promotions": 0,
    })
    nxt["accepted_batches"].append({
        "id": "ChineseAstro-21SRC-Disease",
        "added_bazi_source_annotations": 0,
        "added_ziwei_source_annotations": 25,
        "historical_source_heading_lines": 1,
        "general_historical_source_preamble_lines": 1,
        "source_continued_star_profile_lines": 1,
        "other_historical_star_source_lines": 21,
        "following_Travel_navigation_only": 1,
        "start": "ZWD-R0860", "end": "ZWD-R0884",
        "path": SOURCE.relative_to(T).as_posix(),
        "rules_sha256": digests[0],
        "witness_path": WIT.relative_to(T).as_posix(),
        "witness_sha256": digests[1],
        "original_excerpt_path": EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256": digests[2],
        "original_online_source_oldid": 1963110,
        "source_raw_SHA256": RAW_SHA,
        "source_original_codepoint_range": [41672,42541],
        "next_source_heading": "===七迁移===",
        "source_yangling_ambiguous_two_contexts_preserved": True,
        "source_historic_health_claims_not_advice": True,
        "original_ancient_printed_book_authenticity_unverified": True,
        "original_source_cold_tests_replayed": 12,
        "independent_real_human_blind_forecasts_validated": 0,
        "runtime_astrological_promotions": 0,
    })
    ziwei = nxt["systems"][1]
    ziwei["accepted_source_annotations"] = 884
    ziwei["current_ids"] = "ZWD-R0001–ZWD-R0884"
    ziwei["next_id"] = "ZWD-R0885"
    ziwei["current_batch"] = "ChineseAstro-21SRC-Disease"
    ziwei["source_files"].append(SOURCE.relative_to(T).as_posix())
    ziwei["chapter_coverage"] = (
        "Transmitted original Zi Wei Wikitext oldid1963110 Life palace and Brothers, "
        "Spouses, Children, Wealth, now Disease/Illness 疾厄 cp41672–42541, "
        "24 literal source lines (including heading, preamble, one continued "
        "Tai Yin and 21 other historical star lines) plus only following Travel "
        "navigation marker. Two exact 羊铃 uses with different conditional scopes "
        "preserved; medical, age/sex and bodily claims untested. Original Ming "
        "printing, independent natal chart and other palace texts not complete."
    )
    nxt["next"] = (
        "Next original Zi Wei Travel/Migration 迁移 heading cp42541, next ZWD-R0885; "
        "following Servants/Friends 奴仆 cp43499. BaZi original Di Tian Sui section19 "
        "BZI-R0211 unchanged. Maintain source-only health limitations and independent "
        "historical edition, natal calendar and untouched blind-human validation work."
    )
    nxt["historical_glyph_and_translator_limits"] = (
        "Online transmitted Wikitext oldid1963110 not authenticated ancient woodblock "
        "or expert critically collated translation. Disease passage has two exact 羊铃 "
        "contexts with differing apparent polarity; Tai Yin source physical continuation. "
        "Old disability/health/mortality claims not evidence, prognosis or advice."
    )
    if nxt["systems"][0] != index["systems"][0] or nxt["accepted_batches"][:-1] != index["accepted_batches"]:
        raise ValueError("Old BaZi or previously accepted Chinese batches changed")
    if sum(x["accepted_source_annotations"] for x in nxt["systems"]) != 1094:
        raise ValueError("Wrong cumulative Chinese annotation arithmetic")
    write(NEW, nxt)
    heading = (
        "# Chinese V21 — historical Zi Wei Disease/Illness source only\n\n"
        "**25 new online source-only documentary records ZWD-R0860–ZWD-R0884**, "
        "Disease cp41672–42541 in frozen Wikitext oldid1963110. Two occurrences "
        "of the original glyph group 羊铃 have divergent context and are preserved "
        "without medical or predictive endorsement. Exact text/CP/UTF8 quote SHA, "
        "12 focused tests, 12 cold-extracted tests and CRC/member SHA ZIP verified. "
        "**BaZi210 + ZiWei884 =1094 Chinese historical source records**, not people. "
        "Next **ZWD-R0885 Travel cp42541**, **BZI-R0211 Di Tian Sui section19**. "
        "Original critical printed book, independent chart engine and actual human "
        "predictive tests all OPEN. Human validations **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(
        heading + "## Previous accepted Chinese V20 source checkpoint\n\n" +
        (REC / "CHINESE_CURRENT_BEFORE_21.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    LATEST.write_text(
        heading + (B / "ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    proof = {
        "batch": "ChineseAstro-21SRC-Disease",
        "status": "GUARDED_V21_ORIGINAL_ONLINE_SOURCE_LOCAL_ACCEPTANCE",
        "Chinese_before": 1069, "Chinese_after": 1094,
        "BaZi_unchanged": 210, "ZiWei_before": 859, "ZiWei_after": 884,
        "first": "ZWD-R0860", "last": "ZWD-R0884", "next": "ZWD-R0885",
        "next_BaZi": "BZI-R0211",
        "old_index_V20_SHA256": OLD_SHA,
        "new_index_V21_SHA256": sha(NEW),
        "original_full_source_SHA256": RAW_SHA,
        "source_notes_SHA256": digests[0], "source_witness_SHA256": digests[1],
        "source_excerpt_SHA256": digests[2],
        "archive_SHA256": archive["archive_sha256"],
        "cold_extracted_source_tests_green": 12,
        "older_Western_B07bc_SHA256_unchanged": WEST_SHA,
        "real_human_blind_predictive_validations": 0,
        "runtime_astrological_promotions": 0,
    }
    write(RECEIPT, proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    accept()
