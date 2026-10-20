#!/usr/bin/env python3
"""Guarded historical CLXXVI source admission, not human predictive validation."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07ay_MANNERS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH = "research/astro-b07ay-clxxvi-manners-opening-20261019"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def load(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ay.json"):
    assert not f.exists(), f"Prior or interrupted admission: {f}"
assert git("branch", "--show-current") == BRANCH
old = load(INDEX)
china = load(CHINA)
photos = load(B / "ORIGINAL_PHOTO_WITNESS_V1.json")
correction = load(B / "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json")
candidate = load(B / "MANNERS_SOURCE_CANDIDATES_V1.json")
notes = load(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
assert old["records_count"] == accept["prior_Lilly"] == 12900
assert old["batches"][-1]["id"] == "B07ax"
assert old["next"]["chapter"] == "CLXXVI" and old["next"]["pdf_page"] == 779
assert old["read_numbered_chapters"] == list(range(1, 176))
assert old["read_headed_units_count"] == 91 and not old["partial_numbered_chapters"]
assert sum(x["records_count"] for x in old["batches"]) == 12900
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert photos["source_full_Wellcome_1647_original_PDF_SHA256"] == old["source_sha256"]
assert len(photos["source_1647_1659_page_photos"]) == 10
assert correction["user_historical_count_unchanged"] == 12900
assert candidate["proposed_count"] == notes["historical_annotations_added_if_accepted"] == 40
assert [r["record_number"] for r in rules["rules"]] == list(range(12901, 12941))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert (
    notes["independent_actual_human_forecast_validations"] == notes["runtime_model_promotions"] == 0
)
assert notes["source_author_already_knows_subject_of_example"]
assert notes["negative_observation_historical_literal"] == "I can find none."
assert notes["source_negative_throat_mark_observation_count"] == 1
assert accept["next_original_R"] == "R12941" and accept["next_original_pdf_frame"] == 783
assert accept["next_original_physically_distinct_chapter"] == "CLXXVII"
assert accept["Lilly_after_if_accepted"] == 12940 and accept["Western_after_if_accepted"] == 14006
assert accept["source_critical_expert_collation_completed"] is False
assert accept["source_merchant_true_chart_independently_verified"] is False
assert accept["photo_witness_SHA256"] == sha(B / "ORIGINAL_PHOTO_WITNESS_V1.json")
assert accept["source_data_SHA256"] == sha(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json")
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["original_chapter_boundary_correction_SHA256"] == sha(
    B / "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json"
)
assert release["archive_CRC_passed"] and release["archive_exact_SHA256_and_byte_size_passed"]
assert release["independent_extracted_source_tests_passed"] == 52
assert release["photo_witness_SHA256"] == accept["photo_witness_SHA256"]
assert release["original_notes_SHA256"] == accept["source_data_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert release["old_Western_SHA256"] == sha(INDEX)
assert release["Chinese_V7_SHA256"] == sha(CHINA)
assert sha(downloads() / release["archive_filename"]) == release["archive_SHA256"]
for f in (
    INDEX,
    CHINA,
    TASK / "batches/B07ax/RULES.json",
    TASK / "batches/B07ax/ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json",
):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

BACK.mkdir(exist_ok=False)
for f, n in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ay.json"),
    (CURRENT, "CURRENT_BEFORE_B07ay.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ay.json"),
):
    (BACK / n).write_bytes(f.read_bytes())
old["batches"].append(
    {
        "id": "B07ay",
        "path": "batches/B07ay/RULES.json",
        "records_count": 40,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Original first Lilly printed CHAP CLXXVI Manners of the Native "
            "physically printed folios745–749/PDF779–783, with one-reader "
            "witness to independently typeset 1659 same folios. Source-only "
            "40 historical notes R12901–R12940, including Wit and Understanding, "
            "Form/Stature, general fortune through top of printed749, and "
            "Lilly's explicit Saturn/throat mark negative '(I can find none.)'. "
            "Lilly knew the merchant; all are retrospective claims and cannot "
            "be prospective independent human forecast validation. Original "
            "CLXXVI actually ENDS on printed749 before separate CHAP CLXXVII "
            "Riches heading on same page. Unverified critical edition, natal "
            "epoch astronomical chart engine and real-person accuracy."
        ),
    }
)
old["records_count"] = 12940
old["status"] = "ORIGINAL_LILLY_CLXXVI_MANNERS_PHYSICAL_SOURCE_SPAN_DOCUMENTED_NEXT_CLXXVII_RICHES"
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [176]
old["read_headed_units_count"] = 92
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXVI",
        "editorial_ordinal": 176,
        "chapter_heading": "Of the Manners of the Native",
        "physical_source_start_pdf": 779,
        "accepted_through_pdf": 783,
        "physical_printed_folios": [745, 746, 747, 748, 749],
        "source_batch": "B07ay",
        "historical_start": "R12901",
        "historical_end": "R12940",
        "physical_source_span_covered": True,
        "complete": True,
        "full_independent_classical_critical_edition_verified": False,
        "source_case_author_knew_subject": True,
        "one_explicit_negative_observation": "I can find none.",
        "empirical_human_predictions_validated": 0,
        "runtime_model_promoted": False,
    }
)
old["next"] = {
    "pdf_page": 783,
    "printed_page": 749,
    "chapter": "CLXXVII",
    "printed_chapter_numeral": "CLXXVII",
    "editorial_source_sequence_ordinal": 177,
    "heading": "Of Riches",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "First original printed CHAP CLXXVII Of Riches begins BELOW "
        "horizontal divider on same 1647 PDF783/printed749 after CLXXVI "
        "general-fortune prose. Next source historical R12941. "
        "1647/1659 photos preserved in B07ay; skip preceding manners material."
    ),
    "research_scope": (
        "Source-first Lilly conditions for wealth/riches with original "
        "planetary dignity and place/age/house/context qualifiers, "
        "not verified actual human financial prediction."
    ),
}
old["source_CLXXVI_negative_evidence_and_original_boundary_note"] = (
    "B07ay covers all five printed pages745–749 of first CHAP CLXXVI, "
    "with 1659 independent printing witnesses, and explicitly preserves "
    "the historical Saturn throat blemish conjecture followed by "
    "'I can find none.' as negative evidence. Physical chapter ends "
    "on p749 above separate CLXXVII. Single-reader source documentation "
    "does not verify natal chart epoch, human traits, predictive accuracy "
    "or independent expert textual collation."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07ay_MANNERS.md"
assert len(old["read_numbered_chapters"]) == 176
assert old["read_numbered_chapters"] == list(range(1, 177))
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Lilly original Manners chapter source coverage completed (B07ay)\n\n"
    "**40 historical source annotations R12901–R12940** preserve all "
    "five physical printed folios745–749 (PDF779–783) from first 1647 "
    "CLXXVI on Manners, supported by separately typeset original 1659 "
    "source images. Lilly knew the subject; this is retrospective text, "
    "**not an independent person forecast**. The original conjecture "
    "about a throat blemish ends **'I can find none.'**, a negative "
    "observation preserved rather than coded as success. Original CLXXVI "
    "ends above physical divider on printed749; CLXXVII Of Riches begins "
    "on same page. **12,940 Lilly+1,066 Ptolemy=14,006 Western historical "
    "notes**, Chinese V7 **154 BaZi+201 Zi Wei=355**, unchanged. "
    "Next source **R12941**, CLXXVII PDF783/printed749. "
    "Original critical text expertise, epoch ephemeris and genuine "
    "prospective blind human prediction remain unverified; zero "
    "human forecast validations and zero runtime promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted source progress preserved\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "RECOVERY_CHECKPOINT_20261019_LATEST.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
out = {
    "batch": "B07ay",
    "status": "GUARDED_ORIGINAL_CLXXVI_SOURCE_ADMISSION_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12900,
    "Lilly_after": 12940,
    "Ptolemy_retained": 1066,
    "Western_historical_after": 14006,
    "Chinese_V7_retained": 355,
    "new_documentary_source_annotations": 40,
    "negative_author_observations": 1,
    "first_original_CLXXVI_physical_source_span_complete": True,
    "all_original_text_critical_expert_review_complete": False,
    "next_R": "R12941",
    "next_source_original_PDF": 783,
    "next_original_chapter": "CLXXVII",
    "next_original_printed_folio": 749,
    "original_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ay.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "parallel_Chinese_V7_SHA256": sha(CHINA),
    "portable_source_archive_SHA256": release["archive_SHA256"],
    "source_test_replays": 52,
    "human_prospective_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
