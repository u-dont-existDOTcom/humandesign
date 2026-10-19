#!/usr/bin/env python3
"""Guarded append-only source-only CLXX profections historical notes."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
WEST = ROOT / T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ar_CLXX_SUN_MIDHEAVEN.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ar-clxx-midheaven-sun-20261019"
PARENT = "128db491c2928b44f0176f48a31e4864e8bae679"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for p in (LATEST, RECEIPT, RECOVERY / "LILLY_INDEX_BEFORE_B07ar.json"):
    assert not p.exists(), f"Interrupted or previous source acceptance: {p}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
old = j(WEST)
chinese = j(CHINA)
source = j(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert old["records_count"] == accept["Lilly_before"] == 12725
assert old["batches"][-1]["id"] == "B07aq"
assert sum(row["records_count"] for row in old["batches"]) == 12725
assert old["next"]["chapter"] == "CLXX" and old["next"]["pdf_page"] == 765
assert old["read_numbered_chapters"] == list(range(1, 170))
assert old["read_headed_units_count"] == 85
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert old["source_sha256"] == source["original_book_full_1647_pdf_sha256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert source["source_record_count"] == rules["record_count"] == len(rules["rules"]) == 17
assert [row["record_number"] for row in rules["rules"]] == list(range(12726, 12743))
assert all(not row["runtime_model_promoted"] for row in rules["rules"])
assert [row["profection_house"] for row in source["records"][:12]] == list(range(1, 13))
assert source["original_CLXX_chapter_primary_physical_frames"] == [765, 766]
assert source["next_CLXXI_chapter_starts_on_pdf_frame"] == 766
assert not source["source_original_1647_full_critical_diplomatic_second_reader_complete"]
assert source["actual_human_forecasts_validated"] == source["runtime_promotions"] == 0
assert accept["Lilly_after_if_accepted"] == 12742
assert accept["Western_after_if_accepted"] == 13808
assert accept["next_historical_R"] == "R12743"
assert accept["next_printed_chapter"] == "CLXXI"
assert accept["next_original_PDF"] == 766
assert accept["source_notes_SHA256"] == sha(
    B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json"
)
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert release["CRC_passed"] and release["all_member_SHA256_bytes_passed"]
assert release["independent_extraction_test_replay_passed"] and release["portable_tests"] == 30
assert release["notes_sha256"] == accept["source_notes_SHA256"]
assert release["rules_sha256"] == accept["rules_SHA256"]
assert release["prior_Western_index_sha256"] == sha(WEST)
assert release["prior_Chinese_V7_index_sha256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (WEST, CHINA, ROOT / T / "batches/B07aq/RULES.json"):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

RECOVERY.mkdir(exist_ok=False)
for f, name in (
    (WEST, "LILLY_INDEX_BEFORE_B07ar.json"),
    (CURRENT, "CURRENT_BEFORE_B07ar.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ar.json"),
):
    (RECOVERY / name).write_bytes(f.read_bytes())

old["batches"].append(
    {
        "id": "B07ar",
        "path": "batches/B07ar/RULES.json",
        "records_count": 17,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "First original William Lilly CLXX printed731–732/PDF765–766 "
            "Midheaven and Sun profectional twelve house descriptions, "
            "separate printed 1659 edition p731–732. 17 documentary "
            "annotations R12726–R12742 (12 source house roles, "
            "four contextual exceptions and source next CLXXI boundary). "
            "Historical trigger explicitly Midheaven OR solar natal sign; "
            "secondary transcription misspells 'hosue', not original quote. "
            "No verified real-life health, reputation or financial "
            "outcomes, independent 1647 birth calendar, or runtime "
            "astrological model."
        ),
    }
)
old["records_count"] = 12742
old["status"] = "BOOK_III_CLXX_MIDHEAVEN_SUN_PROFECTIONS_PHYSICAL_SOURCE_COVERED"
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [170]
old["read_headed_units_count"] = 86
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXX",
        "source_unit": "Original Midheaven and Sun profections",
        "chapter_heading": (
            "Of the Profection of Mid-heaven and the Sunne, and their Significations"
        ),
        "physical_source_start_pdf": 765,
        "accepted_through_pdf": 766,
        "next_unaccepted_pdf": 766,
        "next_record": "R12743",
        "accepted_batch": "B07ar",
        "first_edition_source_physically_covered": True,
        "complete": True,
        "full_source_critical_edition_complete": False,
        "actual_real_person_predictive_accuracy_validated": 0,
        "runtime_promoted": False,
    }
)
old["next"] = {
    "pdf_page": 766,
    "printed_page": 732,
    "chapter": "CLXXI",
    "printed_chapter_numeral": "CLXXI",
    "editorial_source_sequence_ordinal": 171,
    "heading": (
        "The significations of the Profectionall Signe of "
        "Part of Fortune, and Signe of the second house"
    ),
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Following CLXX Midheaven and Sun, a new distinct CLXXI "
        "chapter begins BELOW a horizontal divider on original "
        "printed732/PDF766. The heading was recorded as B07ar "
        "source boundary and must not be duplicated as an "
        "interpretation note. Next substantive record R12743."
    ),
    "research_scope": (
        "Historical Part of Fortune/second-house sign profections "
        "by twelve houses; then source annual Alfridary lord "
        "sequence and CLXXII solar revolution calculations. "
        "Human chart and event predictive validation separate."
    ),
}
old["CLXX_Midheaven_Sun_source_only_coverage_note"] = (
    "B07ar physically covers first original CLXX Midheaven and Sun "
    "profections through all twelve original houses and historical "
    "conditional geometry/children/capability claims. Original "
    "separately typeset 1659 print p731–732 corroborated by a "
    "single source reader; not expert edition or predictive truth."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ar_CLXX_SUN_MIDHEAVEN.md"
assert old["records_count"] == sum(row["records_count"] for row in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 171))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
WEST.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly CLXX Midheaven and Sun profection houses covered (B07ar)\n\n"
    "**17 source-only historical annotations R12726–R12742** cover "
    "twelve Midheaven/Sun profection house descriptions, four "
    "specific historic conditional predicates and a physical "
    "divider to CLXXI. Original 1647 first and separate typeset "
    "1659 second printing pp731–732 are SHA witnessed. "
    "The source explicitly uses natal Midheaven **or Sun**, "
    "not general Sun-sign-only predictions. Conditional "
    "case descriptions are historical, not validated "
    "human health, status or finance observations. "
    "**Lilly 12,742 + Ptolemy 1,066 =13,808 Western historical notes**; "
    "separate Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. "
    "Next substantive **R12743**, CLXXI Part of Fortune and "
    "second-house sign profections below the physical divider "
    "on original printed732/PDF766. Empirical human "
    "prediction validations zero; runtime promotions zero.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier source checkpoint preserved verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ar",
    "status": "GUARDED_LILLY_CLXX_SOURCE_HISTORICAL_REGISTRY_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12725,
    "Lilly_after": 12742,
    "Ptolemy_retained": 1066,
    "Western_after": 13808,
    "Chinese_V7_retained": 355,
    "new_documentary_notes": 17,
    "source_original_CLXX_physical_span_covered": True,
    "independent_original_edition_critical_verification_complete": False,
    "next_historical_R": "R12743",
    "next_original_pdf": 766,
    "next_chapter": "CLXXI",
    "old_Western_index_sha256": sha(RECOVERY / "LILLY_INDEX_BEFORE_B07ar.json"),
    "new_Western_index_sha256": sha(WEST),
    "source_notes_sha256": accept["source_notes_SHA256"],
    "rules_sha256": accept["rules_SHA256"],
    "archive_sha256": release["archive_sha256"],
    "portable_tests_replayed": 30,
    "Chinese_V7_sha256": sha(CHINA),
    "real_human_predictive_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
