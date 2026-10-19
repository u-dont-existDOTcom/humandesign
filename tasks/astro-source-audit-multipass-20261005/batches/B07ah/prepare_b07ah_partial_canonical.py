#!/usr/bin/env python3
"""Guarded partial source admission of original annual-rate table in CLXVI.

Only 14 table-level historical annotations, 372 separate source cells (365
one-reader legible, seven null/ambiguous), previous source registry unchanged,
printed CLXVI remains partially read and prognostic validity remains zero.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ah_ANNUAL_TABLE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ah-annual-rate-p745-20261019"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    if french.is_dir():
        return french
    return Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ah.json"):
    assert not f.exists(), f"Preexisting or interrupted admission: {f}"
assert git("branch", "--show-current") == BRANCH
prior = j(INDEX)
china = j(CHINESE)
source = j(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH
assert task["parent_outcome"] == "OPEN"
assert prior["records_count"] == accept["prior_Lilly"] == 12501
assert prior["batches"][-1]["id"] == "B07ag"
assert sum(x["records_count"] for x in prior["batches"]) == 12501
assert prior["next"]["chapter"] == "CLXVI" and prior["next"]["pdf_page"] == 745
assert len(prior["partial_numbered_chapters"]) == 1
assert prior["partial_numbered_chapters"][0]["complete"] is False
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert prior["runtime_promotions"] == prior["empirical_validations"] == 0
assert prior["source_sha256"] == source["source_original_1647_full_pdf_sha256"]
assert china["sum_source_annotations"] == accept["Chinese_V5_parallel"] == 262
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert prior["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["prior_Ptolemy"] == 1066
assert len(source["rows"]) == 372
assert source["original_1647_one_reader_legible"] == 365
assert source["original_1647_unresolved"] == 7
assert source["original_glyphs_without_any_photographic_attempt"] == 0
assert source["original_vs_derived_searchable_text_disagreements"] == 14
assert not source["historical_annual_measure_arithmetic_validated"]
assert rules["record_count"] == accept["new_historical_source_note_records"] == 14
assert [r["record_number"] for r in rules["rules"]] == list(range(12502, 12516))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert not rules["full_CLXVI_historical_source_chapter_complete"]
assert accept["source_rate_crosswalk_SHA256"] == sha(
    B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"
)
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["source_b07ad_overlay_sha256"] == sha(
    B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
)
assert accept["Lilly_if_accepted"] == 12515
assert accept["Western_with_Ptolemy_if_accepted"] == 13581
assert accept["next_original_R"] == "R12516" and accept["next_original_PDF"] == 746
assert release["crc_passed"] and release["member_SHA256_and_sizes_passed"]
assert release["independent_archive_extracted_test_replay_passed"]
assert release["portable_test_count"] == 386
assert release["source_rate_crosswalk_SHA256"] == accept["source_rate_crosswalk_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
archive = downloads() / release["archive_filename"]
assert sha(archive) == release["archive_sha256"]
assert release["prior_Lilly_index_SHA256"] == sha(INDEX)
assert release["Chinese_V5_index_SHA256"] == sha(CHINESE)
for file in (
    INDEX,
    CHINESE,
    ROOT / TASK / "batches/B07ag/RULES.json",
    ROOT / TASK / "batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json",
    ROOT / TASK / "batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ah.json"),
    (CURRENT, "CURRENT_BEFORE_B07ah.md"),
    (CHINESE, "CHINESE_V5_BEFORE_B07ah.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

prior["batches"].append(
    {
        "id": "B07ah",
        "path": "batches/B07ah/RULES.json",
        "records_count": 14,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "PARTIAL continuation of original first printed CHAP CLXVI: "
            "annual equatorial direction-rate table on PDF745/printed711. "
            "14 historical table-level notes R12502–R12515: header, degree "
            "index and twelve 31-degree zodiac sign columns. Separate reversible "
            "source-cell table holds all 372 positions previously one-reader "
            "photographed B07y–B07ad, 365 legible, seven source glyphs unknown "
            "and 14 differences versus modern searchable derivative. "
            "1647 full critical edition and mathematical/year-to-event "
            "ephemeris parity unresolved; neither 1659 hints nor trend smoothing "
            "are promoted, zero independent actual-person predictive results."
        ),
    }
)
prior["records_count"] = 12515
prior["status"] = "BOOK_III_CLXVI_TIME_MEASURE_PARTIAL_ANNUAL_RATE_TABLE_P711"
unit = prior["partial_numbered_chapters"][0]
assert unit["accepted_batch"] == "B07ag" and unit["physical_source_start_pdf"] == 742
unit["accepted_through_pdf"] = 745
unit["next_unaccepted_pdf"] = 746
unit["next_record"] = "R12516"
unit["latest_accepted_batch"] = "B07ah"
unit["annual_1647_rate_table_documented_with_unresolved_glyphs"] = True
unit["original_1647_full_372_source_glyphs_critically_verified"] = False
assert unit["complete"] is False
prior["next"] = {
    "pdf_page": 746,
    "printed_page": 712,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "heading": "Of the measure of time in DIRECTIONS — continued worked time examples",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Following original first CLXVI table printed711, turn to first-edition "
        "printed712/PDF746: The use of the Table (Sun degrees+more than "
        "30 minutes advances row), 7 Libra=54'25\", annual time accumulation, "
        "and Maginus remainder discrepancy 42/48 vs 13/4; Naibod tables "
        "follow. Next historical record R12516. Preserve following separate "
        "duplicated printed CHAP CLXVI annual profections."
    ),
    "research_scope": (
        "Historic table lookup and competing source timing calculation, "
        "Naibod source degree/minute table and actual source-specific "
        "errors; real chart ephemeris and human predictive validity unverified."
    ),
}
prior["chapter_CLXVI_partial_annual_rate_table_acceptance_note"] = (
    "B07ah adds fourteen source-only table-level notes with 372 reversible "
    "historical table cells (365 first-edition one-reader legible and "
    "seven original glyphs unresolved). No independent classic print second "
    "reader, no complete numeric direction-time engine, no real-person "
    "predictive outcome. First printed CLXVI chapter remains PARTIAL and "
    "later duplicated CLXVI annual profections a separate heading."
)
prior["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ah_ANNUAL_TABLE.md"
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert prior["partial_numbered_chapters"][0]["complete"] is False
assert sum(b["records_count"] for b in prior["batches"]) == 12515
assert prior["runtime_promotions"] == prior["empirical_validations"] == 0
INDEX.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly 1647 CLXVI annual-rate source table accepted PARTIALLY (B07ah)\n\n"
    "**14 historical source-only annotations R12502–R12515** document "
    "the original PDF745/printed711 table of 12 zodiac signs×31 degrees. "
    "Full reversible source crosswalk preserves 372 cells, 365 one-reader "
    "legible original first edition and seven unresolved, with 14 "
    "contradictions to the modern derivative searchable transcription. "
    "No inferred repaired glyph and no calendar/event model promotion. "
    "**12,515 Lilly +1,066 Ptolemy =13,581 Western historical notes**; "
    "Chinese V5 **101 BaZi +161 Zi Wei =262** unchanged. "
    "The first physically printed directions CLXVI remains PARTIAL, "
    "not another completed numbered chapter. Next **R12516** begins "
    "PDF746/printed712 original Table Use and Maginus examples; "
    "a separate later CHAP CLXVI concerns annual Profections. "
    "Empirical human predictions validated zero, runtime promotions zero.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted source checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ah",
    "status": "PARTIAL_ORIGINAL_1647_CLXVI_ANNUAL_TABLE_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12501,
    "Lilly_after": 12515,
    "Ptolemy_retained": 1066,
    "Western_after": 13581,
    "Chinese_V5_retained": 262,
    "source_table_cells": 372,
    "source_one_reader_legible": 365,
    "source_unknown_original_glyphs": 7,
    "new_historical_source_annotations": 14,
    "next_R": "R12516",
    "next_PDF": 746,
    "original_chapter_complete": False,
    "prior_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ah.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "source_crosswalk_SHA256": accept["source_rate_crosswalk_SHA256"],
    "new_rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_tests": 386,
    "Chinese_V5_SHA256": sha(CHINESE),
    "real_human_prediction_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
