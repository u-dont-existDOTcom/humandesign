#!/usr/bin/env python3
"""Guarded append-only closing of physical original first CLXVII source span.

The source chapter's physical pages are covered, but 1647 table glyphs and
human predictive accuracy are emphatically NOT independently verified.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ao_CLXVII_END.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ao-clxvii-midheaven-20261019"
PARENT = "87e7fd74d43281c473ca3d293055d0f6ed9ad784"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ao.json"):
    assert not f.exists(), f"Detected an earlier/interrupted admission, reconcile: {f}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
old = j(INDEX)
chi = j(CHINA)
source = j(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["root_owner_outcome"] == "OPEN"
assert old["records_count"] == accept["Lilly_before"] == 12649
assert old["batches"][-1]["id"] == "B07an"
assert sum(x["records_count"] for x in old["batches"]) == 12649
assert old["next"]["chapter"] == "CLXVII" and old["next"]["pdf_page"] == 759
assert old["read_numbered_chapters"] == list(range(1, 167))
assert old["read_headed_units_count"] == 82
assert len(old["partial_numbered_chapters"]) == 1
assert old["partial_numbered_chapters"][0]["complete"] is False
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert chi["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chi["independently_validated_real_human_claims"] == chi["runtime_promotions"] == 0
assert old["source_sha256"] == source["source_full_first_1647_Wellcome_PDF_SHA256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert len(source["record_rows"]) == rules["record_count"] == 22
assert [x["record_number"] for x in rules["rules"]] == list(range(12650, 12672))
assert all(not x["runtime_astrology_promoted"] for x in source["record_rows"])
assert all(not x["original_historical_human_event_outcome_observed"] for x in source["record_rows"])
assert source["original_source_CLXVII_physical_span_fully_covered_as_pages"]
assert source["original_printed_CLXVIII_begins_pdf760"]
assert not source["original_source_p725_full_row_by_row_critical_comparison_complete"]
assert not source["original_CLXVII_source_critical_diplomatic_validation_complete"]
assert accept["Lilly_if_accepted"] == 12671
assert accept["Western_if_accepted"] == 13737
assert accept["next_R"] == "R12672" and accept["next_pdf_page"] == 760
assert accept["next_original_chapter"] == "CLXVIII"
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["records_sha256"] == sha(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")
assert release["CRC_passed"] and release["all_member_SHA256_sizes_passed"]
assert release["extracted_test_replay_passed"]
assert release["portable_source_tests"] == 33
assert release["source_SHA256"] == accept["records_sha256"]
assert release["rules_SHA256"] == accept["rules_sha256"]
assert release["old_Western_SHA256"] == sha(INDEX)
assert release["old_Chinese_V7_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for p in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07an/RULES.json",
    ROOT / T / "integration/CROSS_LANE_MERGE_RECEIPT_20261019.json",
):
    rel = str(p.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(p)), rel

BACK.mkdir(exist_ok=False)
for p, n in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ao.json"),
    (CURRENT, "CURRENT_BEFORE_B07ao.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ao.json"),
):
    (BACK / n).write_bytes(p.read_bytes())

old["batches"].append(
    {
        "id": "B07ao",
        "path": "batches/B07ao/RULES.json",
        "records_count": 22,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Original first 1647 CLXVII final Midheaven, Sun and Moon "
            "profection timing chart printed725/PDF759 with corresponding "
            "independently typeset 1659 p725; the following distinct "
            "printed CHAP CLXVIII How to judge upon a Figure of Profections "
            "begins 1647 p726/PDF760. Twenty-two source-only historical "
            "annotations R12650–R12671, one-reader source example "
            "sightings. Physical previous CLXVII source pages718–725 "
            "are now covered; the earlier 30-degree/60-minute/day-of-year "
            "tables are NOT completely source-critically read, and original "
            "B07an 6deg23-vs-minute37 arithmetic discrepancy persists. "
            "No actual historic or forward-blind person outcomes validated."
        ),
    }
)
old["records_count"] = 12671
old["status"] = "BOOK_III_FIRST_CLXVII_PROFECTIONS_SOURCE_PHYSICAL_END_NEXT_CLXVIII"
prior = old["partial_numbered_chapters"].pop()
assert prior["printed_chapter"] == "CLXVII"
assert prior["next_record"] == "R12650"
assert prior["accepted_through_pdf"] == 758
prior["accepted_through_pdf"] = 759
prior["next_unaccepted_pdf"] = 760
prior["first_original_CLXVII_physical_source_pages_covered"] = True
prior["complete"] = True
prior["closed_by_batch"] = "B07ao"
prior["critical_source_edition_all_table_cells_verified"] = False
prior["source_1647_vs_1659_comparison_all_rows_verified"] = False
prior["actual_human_predictions_validated"] = 0
prior["runtime_model_promoted"] = False
old.setdefault("completed_original_source_units_with_uncertainty", []).append(prior)
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [167]
old["read_headed_units_count"] = 83
old["next"] = {
    "pdf_page": 760,
    "printed_page": 726,
    "chapter": "CLXVIII",
    "printed_chapter_numeral": "CLXVIII",
    "editorial_source_sequence_ordinal": 168,
    "heading": "How to judge upon a Figure of Profections",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Physical original 1647 printed726/PDF760 begins a NEW CHAP "
        "CLXVIII after the ending Mid-heaven/Sun/Moon table from "
        "prior CLXVII p725/PDF759. This original profection-judgment "
        "source describes radical natal house sign classifications, "
        "angles/succedents/cadents, sign ruler, benefic/malefic "
        "context and five rhetorical health conditions. "
        "Next source-only historical record R12672."
    ),
    "research_scope": (
        "Original interpretive profection rules, natal-house and annual "
        "figure contextual predicates and conditional exceptions. "
        "Medical/character claims from 1647 are documentary history "
        "only, not modern person-level prognoses."
    ),
}
old["original_CLXVII_physical_coverage_not_critical_editor_note"] = (
    "B07am–B07ao cover original printed CLXVII pp718–725/PDF752–759. "
    "All 30 degree and 60 minute conversion table rows and full "
    "nativity-specific day-of-year grid NOT independently collation "
    "complete. Old printed worked case uses minute37 instead of "
    "subtracted minute23, original human outcome not validated. "
    "Physical next new CHAP CLXVIII p726/PDF760."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ao_CLXVII_END.md"
assert old["records_count"] == sum(a["records_count"] for a in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 168))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly 1647 CLXVII physical source span completed (B07ao)\n\n"
    "**22 new historical annotations R12650–R12671** document the "
    "original final CLXVII Mid-heaven/Sun/Moon promittor time tables "
    "on printed725/PDF759 and the new **CHAP CLXVIII** source heading "
    "on printed726/PDF760, both seen in separately typeset first "
    "1647 and second 1659 original printings. Prior CLXVII original "
    "physical source pp718–725 are COVERED, but not all 30-degree, "
    "60-minute and calendar-day original table glyphs are independently "
    "critically verified, and B07an source 6deg23 vs 37-minute "
    "lookup discrepancy remains. **Lilly 12,671 + Ptolemy 1,066 = "
    "Western historical 13,737**; Chinese V7 **154 BaZi +201 Zi Wei=355** "
    "unchanged. Next **R12672** at printed726/PDF760 beginning new "
    "CLXVIII How to judge upon a Figure of Profections. "
    "No human-outcome validation or astrological runtime promotion.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier source checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ao",
    "status": "GUARDED_FIRST_CLXVII_PHYSICAL_SOURCE_COVERED_REMOTE_PENDING",
    "Lilly_before": 12649,
    "Lilly_after": 12671,
    "Ptolemy_retained": 1066,
    "Western_after": 13737,
    "Chinese_V7_retained": 355,
    "new_source_annotations": 22,
    "CLXVII_physical_source_covered": True,
    "full_expert_critical_numeric_collation_complete": False,
    "next_R": "R12672",
    "next_pdf": 760,
    "next_chapter": "CLXVIII",
    "prior_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ao.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "source_records_SHA256": accept["records_sha256"],
    "rules_SHA256": accept["rules_sha256"],
    "source_archive_SHA256": release["archive_sha256"],
    "portable_tests_replayed": 33,
    "Chinese_V7_SHA256": sha(CHINA),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
