#!/usr/bin/env python3
"""Append source-only final four Zi Wei house passages with immutable old-index guards."""
from __future__ import annotations
import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V23.json"
NEW = T / "CHINESE_SOURCE_AUDIT_INDEX_V24.json"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR = T / "batches/ChineseAstro-23SRC-Servants/ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_24SRC_FINAL_FOUR.md"
REC = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"
NOTES = B / "ZIWEI_FINAL_FOUR_123_SOURCE_NOTES_V1.json"
WIT = B / "SOURCE_FINAL_FOUR_123_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_FINAL_FOUR_EXACT_EXCERPT.txt"
LEASE = B / "WRITER_LEASE.json"
BRANCH = "research/astro-chinese-v24-ziwei-career-original-source-20261021"
OLD_SHA = "0bc5836d92c332a458a7d4a74dbb25488705344aa38df256dc721c6c5a673a0e"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"

def sha(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()

def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def save(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args],cwd=ROOT,text=True).strip()

def previously_unchanged(p: Path) -> None:
    rel = p.relative_to(ROOT).as_posix()
    if git("rev-parse","HEAD:"+rel) != git("hash-object",str(p)):
        raise ValueError("Previously accepted source file changed: "+rel)

def main() -> None:
    if git("branch","--show-current") != BRANCH:
        raise ValueError("Wrong isolated original Zi Wei V24 source branch")
    lease = load(LEASE)
    if lease["status"] != "active" or lease["owned_branch"] != BRANCH:
        raise ValueError("V24 owned-writer lease not active")
    if any(p.exists() for p in (NEW,LATEST,REC,RECEIPT)):
        raise ValueError("Interrupted V24 index attempt detected: inspect, do not overwrite")
    for p,expected in ((OLD,OLD_SHA),(RAW,RAW_SHA),(WEST,WEST_SHA)):
        if sha(p) != expected:
            raise ValueError("Immutable original source/prior index SHA changed: "+str(p))
    for p in (OLD,RAW,WEST,PRIOR,CURRENT):
        previously_unchanged(p)
    old = load(OLD)
    notes = load(NOTES)
    witness = load(WIT)
    accept = load(B/"ACCEPTANCE.json")
    archive = load(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
    if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"]) != (1146,1074):
        raise ValueError("Previously accepted V23 Chinese total/anchors changed")
    if old["accepted_batches"][-1]["id"] != "ChineseAstro-23SRC-Servants":
        raise ValueError("Previously accepted final source batch changed")
    if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] != [(210,"BZI-R0211"),(936,"ZWD-R0937")]:
        raise ValueError("Previously accepted BaZi/ZiWei sequence changed")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Original historical text is not human prediction validation")
    if (len(notes["records"]),len(witness["quoted_original_records"])) != (123,123):
        raise ValueError("Four online sections are missing literal notes/witnesses")
    if [x["id"] for x in notes["records"]] != [f"ZWD-R{i:04d}" for i in range(937,1060)]:
        raise ValueError("New original source identifiers duplicate or have gaps")
    if notes["excerpt_source_codepoint_span"] != [44429,48890] or notes["next_documentary_id"] != "ZWD-R1060":
        raise ValueError("Original transmitted Volume II end or next ID wrong")
    if not notes["source_online_volume_II_end_reached"] or len(notes["nonhistorical_Wikitext_footer_records_preserved_not_counted"]) != 2:
        raise ValueError("Original site footer was miscounted as classic textual content")
    if [x["historical_original_line_count"] for x in notes["source_sections"]] != [38,24,28,33]:
        raise ValueError("Original remaining palace literal counts changed")
    if notes["real_human_predictive_validations"] or notes["runtime_astrological_promotions"] or notes["independently_authenticated_early_original_printing"]:
        raise ValueError("Source-only scope must remain unvalidated")
    hashes = (sha(NOTES),sha(WIT),sha(EXCERPT))
    if (accept["source_note_sha256"],accept["source_witness_sha256"],
        accept["source_excerpt_sha256"]) != hashes:
        raise ValueError("Frozen source note/witness/excerpt SHA mismatch")
    if witness["original_full_Wikitext_SHA256"] != RAW_SHA or witness["source_excerpt_SHA256"] != hashes[2]:
        raise ValueError("Full original Wikitext witness differs")
    if not archive["ZIP_CRC_verified"] or not archive["all_members_sha256_and_bytes_verified"] or archive["independent_cold_source_tests_green"] != 14:
        raise ValueError("Independent cold source archive validation missing")
    local_file = Path(archive["archive_path_on_owner_computer"])
    if not local_file.is_file() or sha(local_file) != archive["archive_SHA256"]:
        raise ValueError("Cold source archive no longer identical to verified bytes")
    if any(r["independent_human_blind_forecasts_validated"] or r["runtime_astrology_promotions"] for r in notes["records"]):
        raise ValueError("Historically transmitted line miscounted as actual human prediction")
    REC.mkdir(exist_ok=False)
    for p,name in ((OLD,"CHINESE_V23_BEFORE_24.json"),
                   (CURRENT,"CHINESE_CURRENT_BEFORE_24.md"),
                   (WEST,"WESTERN_B07bc_BEFORE_24.json")):
        (REC/name).write_bytes(p.read_bytes())
    new = copy.deepcopy(old)
    new.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V24",
        "status":"ZIWEI_ONLINE_VOLUME_II_12_PALACE_LITERARY_LINES_DOCUMENTED_NOT_CRITICAL_ANCIENT_EDITION",
        "as_of_utc":"2026-10-21",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V23.json",
        "prior_index_sha256":OLD_SHA,
        "sum_source_annotations":1269,
        "original_chinese_source_anchors_checked_against_revision":1197,
        "online_ZiWei_Volume_II_twelve_house_source_lines_documented":True,
        "online_Volume_II_end_codepoint":48890,
        "Wikitext_site_footer_lines_excluded_from_historical_notes":2,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0,
    })
    new["accepted_batches"].append({
        "id":"ChineseAstro-24SRC-FinalPalaces",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":123,
        "original_source_palaces":["Career","Estate","Fortune","Parents"],
        "original_historical_line_counts":[38,24,28,33],
        "terminal_site_wrapper_metadata_excluded":2,
        "source_text_earlier_online_twelve_houses_through_volume_II_end":True,
        "start":"ZWD-R0937","end":"ZWD-R1059",
        "path":NOTES.relative_to(T).as_posix(),"rules_sha256":hashes[0],
        "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":hashes[1],
        "original_excerpt_path":EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256":hashes[2],
        "source_oldid":1963110,"source_full_raw_SHA256":RAW_SHA,
        "original_source_codepoint_range":[44429,48890],
        "historic_career_rank_land_mental_wellbeing_parental_death_claims_unverified":True,
        "original_Ming_printing_critically_collated":False,
        "independent_cold_source_test_replays_green":14,
        "real_human_blind_predictions_validated":0,"runtime_astrological_promotions":0,
    })
    zw = new["systems"][1]
    zw["accepted_source_annotations"] = 1059
    zw["current_ids"] = "ZWD-R0001–ZWD-R1059"
    zw["next_id"] = "ZWD-R1060"
    zw["current_batch"] = "ChineseAstro-24SRC-FinalPalaces"
    zw["source_files"].append(NOTES.relative_to(T).as_posix())
    zw["chapter_coverage"] = (
        "Source-line audited transmitted Zi Wei Volume II online Wikitext oldid1963110 "
        "all twelve palace sections in accepted V1–V24 lineage, ending cp48890 after "
        "Career, Estate, Fortune and Parents final original sections. V24 adds 123 "
        "historical lines (38/24/28/33), with site-only two Wikitext footer lines "
        "preserved but not counted. Career original has five labelled poems; "
        "other physical descriptions contain conditional carryover. Online editorial "
        "transcription is not authenticated Ming original, entire critical Zi Wei "
        "corpus, traditional natal/calendar engine or empirical human prediction."
    )
    new["next"] = (
        "Pinned online Zi Wei Volume II ends cp48890; to continue this corpus, acquire "
        "and independently pin Volume III original text (first possible next record "
        "ZWD-R1060) without inventing an intervening heading. Separately continue BaZi "
        "Di Tian Sui original section19 first BZI-R0211. Check old early-print/modern "
        "edition Four Transformations variants, independently calculate true natal "
        "Chinese calendar/star placements and preregister real-human blind decoys."
    )
    new["historical_glyph_and_translator_limits"] = (
        "Source is one transmitted online Wikitext Volume II oldid1963110, not "
        "an authenticated Ming-era original or full critical scholarly translation; "
        "last two page footer wrapper lines excluded from 123 historical Career, "
        "Estate, Fortune, Parents physical lines. Historical occupation/status, "
        "property, wellbeing/health/longevity, parents' deaths/family stereotypes "
        "are not measured human observations or high-stakes advice."
    )
    if new["accepted_batches"][:-1] != old["accepted_batches"] or new["systems"][0] != old["systems"][0]:
        raise ValueError("Previously accepted BaZi/source batch history modified")
    if sum(x["accepted_source_annotations"] for x in new["systems"]) != 1269:
        raise ValueError("New Chinese source registry arithmetic mismatch")
    save(NEW,new)
    heading = (
        "# Chinese V24 — transmitted online Zi Wei Volume II twelve-house source lines documented\n\n"
        "**123 new historical Wikitext line records ZWD-R0937–ZWD-R1059** "
        "covering Career38, Property24, Fortune28 and Parents33 original source "
        "lines to the exact end of Volume II cp48890. Two Wikitext-only terminal "
        "footer wrappers retained in witness but NOT counted as historical "
        "astrological content. Prior Life/other house documentation preserved. "
        "**BaZi210 + ZiWei1059 =1269 historical source annotations**, not people. "
        "Four sections' exact Unicode/UTF8 and SHA references independently tested; "
        "14 source and 14 cold-extracted source tests passed. Next original Zi Wei "
        "Volume III requires a separately pinned full source, first possible "
        "ZWD-R1060; BaZi next BZI-R0211 Di Tian Sui section19. "
        "No authenticated classical printed original, verified comprehensive "
        "calendar/natal chart engine, clinical/parental/financial recommendation, "
        "real human blind predictions or runtime astrology promotions.\n\n"
    )
    CURRENT.write_text(
        heading + "## Previous accepted Chinese V23 original source checkpoint\n\n" +
        (REC/"CHINESE_CURRENT_BEFORE_24.md").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    LATEST.write_text(
        heading + (B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    receipt = {
        "batch":"ChineseAstro-24SRC-FinalPalaces",
        "status":"GUARDED_ZIWEI_V24_FINAL_FOUR_ONLINE_SOURCE_LOCAL_ACCEPTANCE",
        "Chinese_before":1146,"Chinese_after":1269,
        "BaZi_retained":210,"ZiWei_before":936,"ZiWei_after":1059,
        "new_source_only_original_text_lines":123,
        "excluded_Wikitext_footer_lines":2,
        "first_ZWD":"ZWD-R0937","last_ZWD":"ZWD-R1059",
        "next_ZWD":"ZWD-R1060","next_BaZi":"BZI-R0211",
        "old_V23_index_SHA256":OLD_SHA,
        "new_V24_index_SHA256":sha(NEW),
        "full_original_online_Wikitext_SHA256":RAW_SHA,
        "source_notes_SHA256":hashes[0],
        "source_witness_SHA256":hashes[1],
        "source_excerpt_SHA256":hashes[2],
        "source_archive_SHA256":archive["archive_SHA256"],
        "cold_independent_source_tests_green":14,
        "inherited_older_Western_B07bc_SHA256":WEST_SHA,
        "online_volume_II_twelve_house_literal_source_complete":True,
        "ancient_woodblock_original_printing_authenticated":False,
        "human_blind_predictive_validations":0,
        "runtime_astrological_promotions":0,
    }
    save(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
