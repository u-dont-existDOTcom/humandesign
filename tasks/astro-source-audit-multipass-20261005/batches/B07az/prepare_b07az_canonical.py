#!/usr/bin/env python3
"""Guarded historical-only Riches chapter admission; retrospective claims remain untested."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07az_RICHES.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH = "research/astro-b07az-clxxvii-riches-source-20261020"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    result = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07az.json"):
    assert not f.exists(), f"Prior or interrupted admission; reconcile: {f}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
chinese = j(CHINA)
source = j(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert old["records_count"] == accept["Lilly_before"] == 12940
assert old["batches"][-1]["id"] == "B07ay"
assert old["next"]["chapter"] == "CLXXVII" and old["next"]["pdf_page"] == 783
assert old["read_numbered_chapters"] == list(range(1, 177))
assert old["read_headed_units_count"] == 92
assert not old["partial_numbered_chapters"]
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == source["original_full_1647_PDF_sha256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert rules["record_count"] == source["historical_documentary_annotation_count"] == 29
assert [r["record_number"] for r in rules["rules"]] == list(range(12941, 12970))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert source["independent_biographical_wealth_predicted_outcomes_validated"] == 0
assert source["subject_was_already_known_to_original_author"]
assert source["next_original_CLXXVIII_starts_shared_folio751"]
assert accept["Lilly_after_if_accepted"] == 12969
assert accept["Western_if_accepted"] == 14035
assert accept["next_R"] == "R12970"
assert accept["next_chapter"] == "CLXXVIII" and accept["next_original_PDF_frame"] == 785
assert not accept["all_source_early_print_critical_expert_review"]
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["source_photo_witness_SHA256"] == sha(
    B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"
)
assert release["CRC_passed"] and release["member_SHA256_exact_bytes_passed"]
assert release["independent_archive_extracted_test_replay_passed"] == 41
assert release["source_notes_sha256"] == accept["source_photo_witness_SHA256"]
assert release["source_rules_sha256"] == accept["rules_SHA256"]
assert release["prior_Lilly_index_sha256"] == sha(INDEX)
assert release["Chinese_V7_index_sha256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (
    INDEX,
    CHINA,
    T / "batches/B07ay/RULES.json",
    T / "batches/B07ay/ORIGINAL_PHOTO_WITNESS_V1.json",
):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

BACK.mkdir(exist_ok=False)
for f, n in (
    (INDEX, "LILLY_INDEX_BEFORE_B07az.json"),
    (CURRENT, "CURRENT_BEFORE_B07az.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07az.json"),
):
    (BACK / n).write_bytes(f.read_bytes())

old["batches"].append(
    {
        "id": "B07az",
        "path": "batches/B07az/RULES.json",
        "records_count": 29,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Original first Lilly 1647 CLXXVII Of Riches printed folios749–751 "
            "PDF783–785 with independently typeset 1659 comparator. "
            "29 historical source-only annotations R12941–R12969 from an "
            "already known merchant's second-house/property/wealth and family "
            "inheritance/lawsuit narrative, with detailed conditional source "
            "factors and separate physical CLXXVIII Of Brethren boundary. "
            "Original Aquarius cusp prints 23°30′ versus modern derivative "
            "23.3 truncation. Historic forecast-like statements and retroactive "
            "descriptions are NOT verified human wealth/personality results; "
            "source expert critical edition and era natal astrology engine unverified."
        ),
    }
)
old["records_count"] = 12969
old["status"] = "ORIGINAL_LILLY_CLXXVII_RICHES_SOURCE_PHYSICAL_CHAPTER_COVERED_NEXT_CLXXVIII"
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [177]
old["read_headed_units_count"] = 93
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXVII",
        "editorial_ordinal": 177,
        "chapter_heading": "Of Riches",
        "physical_source_start_pdf": 783,
        "accepted_through_pdf": 785,
        "original_printed_folios": [749, 750, 751],
        "source_batch": "B07az",
        "historical_start": "R12941",
        "historical_end": "R12969",
        "complete": True,
        "physical_source_span_covered": True,
        "all_original_early_print_critical_expert_collation_finished": False,
        "source_person_case_known_to_author": True,
        "independently_verified_real_person_financial_predictions": 0,
        "runtime_model_promoted": False,
    }
)
old["next"] = {
    "pdf_page": 785,
    "printed_page": 751,
    "chapter": "CLXXVIII",
    "printed_chapter_numeral": "CLXXVIII",
    "editorial_source_sequence_ordinal": 178,
    "heading": "Of BRETHREN",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 physical CHAP CLXXVIII begins BELOW p751/PDF785 "
        "Riches ending and horizontal divider, under 'Judgments upon "
        "the third house'. Next historical source R12970. Preserve "
        "the nearby retrospective merchant context and all source caveats."
    ),
    "research_scope": (
        "Historical claims about number, conditions and longevity of "
        "siblings; source-level nulls and uncertainty, unblinded case "
        "limitations and no verified actual person outcome."
    ),
}
old["chapter_CLXXVII_source_case_not_a_blind_person_prediction"] = (
    "B07az original 1647/1659 Of Riches case for a merchant already known "
    "to Lilly, 29 documentary annotations; predictions about wealth before "
    "age35, later property/inheritance, relatives and lawsuits are "
    "historical source claims and no actual human outcomes validated. "
    "Second-house Aquarius 23°30 source versus shortened secondary 23.3. "
    "First CLXXVII chapter physically ends p751 above new CLXXVIII Brethren."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07az_RICHES.md"
assert old["read_numbered_chapters"] == list(range(1, 178))
assert old["records_count"] == sum(b["records_count"] for b in old["batches"])
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Lilly original Riches chapter CLXXVII source-covered (B07az)\n\n"
    "**29 source-only documentary annotations R12941–R12969** record "
    "a known merchant's historical riches, age-related wealth, "
    "property, family/inheritance and lawsuit claims from original "
    "1647 and separately typeset 1659 folios749–751. "
    "These are **not independently verified outcomes**. "
    "The first 1647 Aquarius second-house cusp prints **23°30′** "
    "versus shortened secondary transcript 23.3; original source "
    "retained without assuming chart-era calculation parity. "
    "Chapter ends above printed751/PDF785 horizontal divider; "
    "next distinct **CLXXVIII Of Brethren begins same page**. "
    "**12,969 Lilly+1,066 Ptolemy=14,035 Western** historical "
    "annotations; Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. "
    "Next historical source **R12970**, PDF785/printed751. "
    "Critical expert collation, measured human prediction success "
    "and runtime astrology model promotion remain zero/unverified.\n\n"
)
CURRENT.write_text(
    summary + "## Earlier accepted historical checkpoint\n\n" + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "RECOVERY_CHECKPOINT_20261020.md").read_text(encoding="utf-8"), encoding="utf-8"
)
receipt = {
    "batch": "B07az",
    "status": "ORIGINAL_RICHES_HISTORICAL_SOURCE_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12940,
    "Lilly_after": 12969,
    "Ptolemy_retained": 1066,
    "Western_after": 14035,
    "Chinese_V7_retained": 355,
    "new_documentary_annotations": 29,
    "source_physical_original_CLXXVII_folios": [749, 750, 751],
    "next_source_original_PDF": 785,
    "next_printed_chapter": "CLXXVIII",
    "next_historical_R": "R12970",
    "prior_Western_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07az.json"),
    "new_Western_SHA256": sha(INDEX),
    "Chinese_V7_SHA256": sha(CHINA),
    "source_notes_SHA256": accept["source_photo_witness_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_archive_tests_replayed": 41,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
