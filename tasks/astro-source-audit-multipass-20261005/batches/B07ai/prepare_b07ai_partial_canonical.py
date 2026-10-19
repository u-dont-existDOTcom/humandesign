#!/usr/bin/env python3
"""Guarded PARTIAL original Lilly CLXVI printed712 Maginus source admission.

Separate original printed numbers from arithmetic diagnostics; original
chapter is NOT complete, Chinese source index and prior Lilly history unchanged.
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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ai_MAGINUS_PARTIAL.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ai-table-use-maginus-p746-20261019"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ai.json"):
    assert not f.exists(), f"Interrupted or prior preparation: {f}"
assert git("branch", "--show-current") == BRANCH
prior = j(INDEX)
china = j(CHINESE)
source = j(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert prior["records_count"] == accept["prior_Lilly"] == 12515
assert prior["batches"][-1]["id"] == "B07ah"
assert prior["next"]["chapter"] == "CLXVI"
assert prior["next"]["pdf_page"] == 746
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert len(prior["partial_numbered_chapters"]) == 1
assert prior["partial_numbered_chapters"][0]["complete"] is False
assert sum(b["records_count"] for b in prior["batches"]) == 12515
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
assert prior["source_sha256"] == source["source_original_1647_full_PDF_sha256"]
assert prior["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["prior_Ptolemy"] == 1066
assert china["sum_source_annotations"] == accept["Chinese_V5_retained"] == 262
assert china["runtime_promotions"] == china["independently_validated_real_human_claims"] == 0
assert rules["record_count"] == source["new_historical_annotation_count"] == 31
assert len(source["records"]) == 31 and len(source["original_24_years_source_table"]) == 24
assert [r["record_number"] for r in rules["rules"]] == list(range(12516, 12547))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert rules["empirical_real_person_validations"] == rules["runtime_promotions"] == 0
assert not rules["original_CLXVI_complete"]
assert source["original_54_arcminutes_per_year_worked_simplification"] == 54
assert [
    v["true_arithmetic_remaining_arcminutes"] for v in source["historical_arithmetic_cases"]
] == [13, 4]
assert [
    v["original_printed_fraction_arcminutes"] for v in source["historical_arithmetic_cases"]
] == [42, 48]
assert source["exact_54_arcminutes_times_6d18h_is_364_point_5_days"]
assert source["source_first_second_printing_not_independent_human_test"]
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["original_source_records_SHA256"] == sha(
    B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"
)
assert accept["Lilly_if_accepted"] == 12546
assert accept["Western_if_accepted"] == 13612
assert accept["next_R"] == "R12547" and accept["next_PDF"] == 747
assert release["CRC_passed"] and release["member_hashes_and_byte_sizes_passed"]
assert release["independent_archive_extracted_test_replay_passed"]
assert release["source_tests_replayed"] == 70
assert release["records_SHA256"] == accept["original_source_records_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert sha(downloads() / release["filename"]) == release["archive_SHA256"]
assert release["prior_Western_index_SHA256"] == sha(INDEX)
assert release["Chinese_V5_SHA256"] == sha(CHINESE)
for file in (
    INDEX,
    CHINESE,
    ROOT / TASK / "batches/B07ah/RULES.json",
    ROOT / TASK / "batches/B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json",
    ROOT / TASK / "batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg",
    ROOT / TASK / "batches/B07ae/evidence/first_edition_1647_printed712_pdf746.jpg",
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ai.json"),
    (CURRENT, "CURRENT_BEFORE_B07ai.md"),
    (CHINESE, "CHINESE_V5_BEFORE_B07ai.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

prior["batches"].append(
    {
        "id": "B07ai",
        "path": "batches/B07ai/RULES.json",
        "records_count": 31,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "PARTIAL original first Lilly printed CLXVI time directions, "
            "original printed711 bottom/PDF745 table-use instructions and "
            "printed712/PDF746 original Maginus worked 24-year 54' accumulation "
            "and introduction of Naibod. Source-only 31 historical notes "
            "R12516–R12546 with actual 1647 and separately typeset original "
            "1659 photos, one-reader 24-year source table and reversible "
            "mathematical diagnostics: 42/48' printed fraction versus 13/4' "
            "actual target residual; original 6d18h per minute yields 364.5 "
            "nominal days per 54' rather than exactly365. Do not silently fix "
            "original printing, verify original natal engine or claim events."
        ),
    }
)
prior["records_count"] = 12546
prior["status"] = "BOOK_III_CLXVI_TIME_MEASURE_PARTIAL_TABLE_USE_MAGINUS_NEXT_NAIBOD"
unit = prior["partial_numbered_chapters"][0]
assert unit["latest_accepted_batch"] == "B07ah"
unit["accepted_through_pdf"] = 746
unit["next_unaccepted_pdf"] = 747
unit["next_record"] = "R12547"
unit["latest_accepted_batch"] = "B07ai"
unit["Maginus_print_vs_target_fraction_problem_open"] = True
unit["source_one_arcminute_6d18h_approximation_open"] = True
assert unit["complete"] is False
prior["next"] = {
    "pdf_page": 747,
    "printed_page": 713,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "heading": "Of the measure of time in DIRECTIONS — Naibod exact table continued",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "First original CLXVI direction-time chapter, next original "
        "printed713/PDF747 begins Naibod source table for conversion "
        "of equatorial degrees into years/days/hours, continued across "
        "printed714/PDF748 minute source table. Naibod minute27 source "
        "missing and other early print discrepancies preserved; next "
        "Lilly historical source R12547. The distinct later physically "
        "printed duplicated CLXVI annual Profections chapter begins "
        "around PDF749, not the same source unit."
    ),
    "research_scope": (
        "Source-first numerical original Naibod 90 degree and 60 nominal "
        "minute entries, first and independently typeset second original "
        "editions, exact sexagesimal arithmetic and unresolved cells; "
        "real-human forecasts and natal true astronomic engine not verified."
    ),
}
prior["chapter_CLXVI_partial_original_maginus_table_use_note"] = (
    "B07ai 31 source-only notes document original Sun zodiac degree "
    "selection, 54'25\" Libra7 source to 54' simplified annual table, "
    "24 source accumulated-year entries, original printed 42'/48' "
    "fractions contrasted with exact 13'/4' target residuals, "
    "and Naibod introduction. Both independently typeset 1647/1659 "
    "paper sources carried original arithmetic; cause and correct "
    "prognostic method unverified. Same first printed CLXVI remains "
    "PARTIAL; later duplicated CLXVI annual profections distinct."
)
prior["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ai_MAGINUS_PARTIAL.md"
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert prior["partial_numbered_chapters"][0]["complete"] is False
assert prior["records_count"] == sum(v["records_count"] for v in prior["batches"])
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
INDEX.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly 1647 first CLXVI original worked table and Maginus source (B07ai, PARTIAL)\n\n"
    "**31 original historical annotations R12516–R12546** include the "
    "printed711/PDF745 end of annual-table instructions and printed712/PDF746 "
    "24-year 54' annual source table, Maginus two actual first-and-second "
    "edition worked examples and Naibod introduction. Original exact "
    "table lookup Sun6°37′ Libra -> Libra7=54′25″, omit seconds to 54′. "
    "Source **42′→284days and48′→324days** disagrees with arithmetic "
    "residual **13′ and4′**; source explicitly 6d18h per arcminute implies "
    "54' accumulates 364.5 nominal days. Both original print and calculation "
    "are preserved, neither is validated predictive astronomy. "
    "**Lilly 12,546 + Ptolemy 1,066 =13,612 Western historical notes**; "
    "Chinese historical V5 **101 BaZi +161 Zi Wei=262** unchanged. "
    "The first printed CLXVI remains PARTIAL; next **R12547** at original "
    "PDF747/printed713 Naibod table. Human prediction validations zero, "
    "runtime promotions zero.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted historical checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ai",
    "status": "LILLY_ORIGINAL_MAGINUS_PARTIAL_PREPARED_REMOTE_PUBLISH_PENDING",
    "Lilly_before": 12515,
    "Lilly_after": 12546,
    "Ptolemy_retained": 1066,
    "Western_after": 13612,
    "Chinese_V5_retained": 262,
    "new_source_only_records": 31,
    "source_24_year_rows": 24,
    "original_printed_fraction_minutes": [42, 48],
    "true_target_residual_minutes": [13, 4],
    "next_R": "R12547",
    "next_PDF": 747,
    "partial_first_CLXVI_still_open": True,
    "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ai.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_records_SHA256": accept["original_source_records_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "release_archive_SHA256": release["archive_SHA256"],
    "portable_replayed_tests": 70,
    "Chinese_V5_SHA256": sha(CHINESE),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
