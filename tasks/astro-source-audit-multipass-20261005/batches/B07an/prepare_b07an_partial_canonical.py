#!/usr/bin/env python3
"""Guarded source-only original 1647 CLXVII table and three example acceptance.

Only 24 historical annotations; nine selected one-reader table cells and a
two-edition arithmetic discrepancy. Do NOT declare entire printed time table
or natal calendar or any individual's astrological forecast verified.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07an_PROFECTION_TIMING.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07an-clxvii-original-time-tables-20261019"
PARENT = "4bb03e8394ffd22b5693874dc4bfe89f3d372e20"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    resolved = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if resolved is not None and resolved.is_dir() and resolved.resolve() != Path.home().resolve():
        return resolved
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07an.json"):
    assert not f.exists(), f"Potential interrupted earlier preparation, reconcile first: {f}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
old = j(INDEX)
china = j(CHINA)
source = j(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json")
witness = j(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
scope = j(B / "TASK_SCOPE.json")
assert scope["required_branch"] == BRANCH and scope["root_owner_outcome"] == "OPEN"
assert old["records_count"] == accept["prior_Lilly"] == 12625
assert old["batches"][-1]["id"] == "B07am"
assert old["next"]["pdf_page"] == 755 and old["next"]["chapter"] == "CLXVII"
assert old["next"]["editorial_source_sequence_ordinal"] == 167
assert old["read_numbered_chapters"] == list(range(1, 167))
assert len(old["partial_numbered_chapters"]) == 1
assert old["partial_numbered_chapters"][0]["complete"] is False
assert old["partial_numbered_chapters"][0]["accepted_batch"] == "B07am"
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert old["source_sha256"] == source["original_full_1647_PDF_sha256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert len(source["source_sample_one_reader_table_rows"]) == 9
assert len(source["source_images"]) == 8
assert source["proposed_source_record_count"] == len(rules["rules"]) == 24
assert [r["record_number"] for r in rules["rules"]] == list(range(12626, 12650))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert (
    source["original_printed_1647_date_table_and_examples"][-1]["printed_minute_row_actually_used"][
        0
    ]
    == 37
)
assert (
    source["original_printed_1647_date_table_and_examples"][-1][
        "mathematically_corresponding_minute_row"
    ][0]
    == 23
)
assert not source["source_full_30_and_60_digit_columns_critically_collated"]
assert not source["source_365day_month_table_all_cells_critically_collated"]
assert rules["empirical_human_prediction_validations"] == rules["runtime_promotions"] == 0
assert accept["Lilly_if_accepted"] == 12649
assert accept["Western_if_accepted"] == 13715
assert accept["next_R"] == "R12650" and accept["next_original_PDF"] == 759
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["historical_photographic_data_SHA256"] == sha(
    B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"
)
assert accept["source_photo_and_arithmetic_witness_SHA256"] == sha(
    B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json"
)
assert release["CRC_passed"] and release["member_SHA256_bytes_passed"]
assert release["independent_ZIP_extraction_test_replay_passed"]
assert release["source_tests_replayed"] == 40
assert release["source_SHA256"] == accept["historical_photographic_data_SHA256"]
assert release["witness_SHA256"] == accept["source_photo_and_arithmetic_witness_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert release["old_Western_index_SHA256"] == sha(INDEX)
assert release["Chinese_V7_source_index_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07am/RULES.json",
    ROOT / TASK / "batches/B07ai/RULES.json",
    ROOT / TASK / "integration/CROSS_LANE_MERGE_RECEIPT_20261019.json",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07an.json"),
    (CURRENT, "CURRENT_BEFORE_B07an.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07an.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

old["batches"].append(
    {
        "id": "B07an",
        "path": "batches/B07an/RULES.json",
        "records_count": 24,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Partial original printed CLXVII Use of Profections source first "
            "edition folios721–724/PDF755–758. Twenty-four source-only "
            "historical annotations R12626–R12649 from two physical "
            "degree/minute time tables, nativity-specific calendar date "
            "chart, 1640 nativity and three worked timing examples; "
            "actual 1647 and independently typeset original 1659 print "
            "images with per-file SHA witnesses retained. Nine sampled "
            "first-edition table cells manually checked; full 30-degree, "
            "60-minute and year/month table glyph census NOT complete. "
            "Third worked 6°23 target erroneously looks up minute37 "
            "instead of minute23 (source 80d13h21 versus reconstructed "
            "77d17h11); original both editions retain this discrepancy. "
            "One-degree and minute60 table cells differ by one clock minute. "
            "Source academic validity, full birth calendar, real people's "
            "life outcomes and runtime model promotion remain unvalidated."
        ),
    }
)
old["records_count"] = 12649
old["status"] = "BOOK_III_CLXVII_PROFECTION_TIME_TABLES_PARTIAL_THREE_SOURCE_EXAMPLES"
unit = old["partial_numbered_chapters"][0]
unit["accepted_through_pdf"] = 758
unit["next_unaccepted_pdf"] = 759
unit["next_record"] = "R12650"
unit["latest_accepted_batch"] = "B07an"
unit["next_calendar_table_original_glyphs_read"] = False
unit["all_original_degree_minute_table_glyphs_critically_verified"] = False
unit["third_worked_profection_minute_lookup_discrepancy_documented"] = True
assert unit["complete"] is False
old["next"] = {
    "pdf_page": 759,
    "printed_page": 725,
    "chapter": "CLXVII",
    "printed_chapter_numeral": "CLXVII",
    "editorial_source_sequence_ordinal": 167,
    "heading": (
        "Of the Use of Profections, and their Effects — mid-heaven and other Hylegical places"
    ),
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 printed725/PDF759 continues the Mid-heaven "
        "examples from p724 after three Ascendant examples and "
        "1647/1659 source-proven 6°23 vs 37-minute lookup conflict. "
        "The first CLXVII remains PARTIAL and original 30-degree/60-minute "
        "and calendar day tables not fully source-critically collated. "
        "Next historical source R12650."
    ),
    "research_scope": (
        "Original source calculations of Midheaven, Sun, Moon and "
        "other hylegical place prosectional directions, source "
        "edition and numerical errors versus calendar parity; "
        "no real-person test or actual birthday ephemeris inferred."
    ),
}
old["chapter_CLXVII_partial_1647_source_table_issue_note"] = (
    "B07an 24 historic source-only observations of original 1647/1659 "
    "profection date tables p721-724. Full original tabular data not "
    "independently collated: only nine literal rows manually checked. "
    "The printed third 6°23 angle source uses minute37 not minute23, "
    "yielding 80d13h21 versus 77d17h11 under the printed table. "
    "No actual-person outcome, natal ephemeris or full calendar engine "
    "verified; first physical CLXVII remains PARTIAL."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07an_PROFECTION_TIMING.md"
assert old["records_count"] == sum(b["records_count"] for b in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 167))
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["partial_numbered_chapters"][0]["complete"] is False
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly original printed CLXVII profection timing sources partially accepted (B07an)\n\n"
    "**24 new historical documentary records R12626–R12649** from "
    "original first 1647 printed721–724/PDF755–758 and independently "
    "typeset 1659 print, source photos and hashes preserved. Degree "
    "and minute conversion tables plus old nativity calendar-day "
    "table remain only sampled, not fully critically collated. "
    "Original two examples produce **17d20h34m / October6** "
    "and **29d10h08m / October17**. Original third example "
    "prints arc **6°23′** but uses **37′** row, giving **80d13h21m** "
    "instead of the printed table's 23′ row giving **77d17h11m**. "
    "Do not repair original document, claim verified natal engine "
    "or treat the dates as observed human predictions. "
    "**12,649 Lilly +1,066 Ptolemy=13,715 Western historical notes**, "
    "Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. "
    "The first original CLXVII chapter stays PARTIAL; next "
    "**R12650 original PDF759/printed725 Mid-heaven examples**. "
    "Zero independently verified human predictions and zero runtime "
    "model promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted original-source checkpoint retained\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
rec = {
    "batch": "B07an",
    "status": "GUARDED_ORIGINAL_PROFECTION_TIMING_PARTIAL_SOURCE_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12625,
    "Lilly_after": 12649,
    "Ptolemy_retained": 1066,
    "Western_after": 13715,
    "Chinese_V7_retained": 355,
    "new_source_only_records": 24,
    "source_selected_cells": 9,
    "original_full_table_critical_read_completed": False,
    "actual_original_third_case_minute37_source_error_retained": True,
    "next_R": "R12650",
    "next_original_PDF": 759,
    "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07an.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_SHA256": accept["historical_photographic_data_SHA256"],
    "witness_SHA256": accept["source_photo_and_arithmetic_witness_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_tests_replayed": 40,
    "Chinese_V7_SHA256": sha(CHINA),
    "independent_real_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rec, indent=2))
