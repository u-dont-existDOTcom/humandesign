#!/usr/bin/env python3
"""Append ONLY documentary original 1647 CLXXII solar return opening.

Original solar return historical page 734–735 and 1646 worked source timing
are neither complete first CLXXII chapter nor independently validated
astronomy, calendar, birth time, or real human prediction.
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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07at_SOLAR_REVOLUTION.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07at-clxxii-revolutions-opening-20261019"
PARENT = "cea02f3067a67f21569813bde6da0e0cfa811630"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for p in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07at.json"):
    assert not p.exists(), f"Interrupted admission; reconcile exact file before retry {p}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
index = load(INDEX)
chinese = load(CHINA)
doc = load(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert index["records_count"] == accepted["Lilly_before"] == 12764
assert index["batches"][-1]["id"] == "B07as"
assert index["next"]["chapter"] == "CLXXII" and index["next"]["pdf_page"] == 768
assert index["read_numbered_chapters"] == list(range(1, 172))
assert index["partial_numbered_chapters"] == []
assert index["read_headed_units_count"] == 87
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert chinese["sum_source_annotations"] == accepted["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert index["source_sha256"] == doc["original_full_1647_book_PDF_SHA256"]
assert rules["record_count"] == accepted["new_historical_source_records"] == 24
assert [r["record_number"] for r in rules["rules"]] == list(range(12765, 12789))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert not doc["original_CLXXII_full_source_physical_span_read"]
assert not doc["original_Lilly_solar_return_algorithm_ephemeris_correctness_verified"]
assert doc["original_1646_literal_versus_computed_arithmetic"]["source_sum_unrounded_time_hms"] == [
    10,
    8,
    47,
]
assert doc["original_1646_literal_versus_computed_arithmetic"]["source_house_table_final_hm"] == [
    21,
    43,
]
assert accepted["Lilly_after_if_accepted"] == 12788
assert accepted["Western_after_if_accepted"] == 13854
assert accepted["next_original_R"] == "R12789" and accepted["next_original_PDF"] == 770
assert accepted["source_photo_and_arithmetic_SHA256"] == sha(
    B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json"
)
assert accepted["rules_SHA256"] == sha(B / "RULES.json")
assert release["CRC_passed"] and release["member_SHA256_exact_bytes_passed"]
assert release["independent_extraction_source_tests_passed"]
assert release["portable_test_replays"] == 38
assert release["source_sha256"] == accepted["source_photo_and_arithmetic_SHA256"]
assert release["rules_sha256"] == accepted["rules_SHA256"]
assert release["old_Western_index_SHA256"] == sha(INDEX)
assert release["Chinese_V7_index_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07as/RULES.json",
    ROOT / T / "batches/B07as/evidence/1647_original-768.jpg",
    ROOT / T / "batches/B07as/evidence/original_1659_djvu_763.jpg",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07at.json"),
    (CURRENT, "CURRENT_BEFORE_B07at.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07at.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

index["batches"].append(
    {
        "id": "B07at",
        "path": "batches/B07at/RULES.json",
        "records_count": 24,
        "sha256": accepted["rules_SHA256"],
        "scope": (
            "First original Lilly 1647 CHAP CLXXII Of Revolutions, "
            "printed734–735/PDF768–769 compared against actual separately "
            "typeset 1659 original print. 24 historical observations "
            "R12765–R12788 covering exact zodiacal solar return definition, "
            "warning about Sun's natal minute, old Origanus 19Sept1646 "
            "noon 6°12′ Libra vs radix 6°37′ Libra (remaining25′), "
            "source daily motion59′10″ vs Maginus nearby table59′08″, "
            "20′ and5′ entries producing 10h08m47s then source truncates "
            "to10h08m, subtracts westward 1h07m, adds house-table "
            "12h26m and time equation16m yielding 21h43m. No historical "
            "birth-date epoch astronomical validation, real human outcomes "
            "or runtime rule promotions; first CLXXII physically partial."
        ),
    }
)
index["records_count"] = 12788
index["status"] = "BOOK_III_CLXXII_SOLAR_REVOLUTION_SOURCE_OPENING_PARTIAL_1646_EXAMPLE"
index["partial_numbered_chapters"].append(
    {
        "printed_chapter": "CLXXII",
        "editorial_ordinal": 172,
        "chapter_heading": "Of Revolutions",
        "physical_source_start_pdf": 768,
        "accepted_through_pdf": 769,
        "next_unaccepted_pdf": 770,
        "next_record": "R12789",
        "accepted_batch": "B07at",
        "latest_accepted_batch": "B07at",
        "complete": False,
        "source_single_reader_first_and_second_photographs": True,
        "all_original_1646_calendar_and_birth_solar_times_verified": False,
        "source_ephemeris_and_latitude_offset_independent_parity_verified": False,
        "empirical_real_human_predictions_validated": 0,
        "runtime_model_promotions": 0,
    }
)
index["next"] = {
    "pdf_page": 770,
    "printed_page": 736,
    "chapter": "CLXXII",
    "printed_chapter_numeral": "CLXXII",
    "editorial_source_sequence_ordinal": 172,
    "heading": "Of Revolutions — house interpretation and annual return effects continued",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "After original first printed CLXXII source pages734–735, "
        "next substantive source record R12789 on printed736/PDF770. "
        "Original 1647 photos for PDF770–773 were rendered locally "
        "but not critically source-admitted in B07at. Preserve them "
        "for the next independent batch. Complete solar-return "
        "ephemeris/calendar engine and human prediction tests remain open."
    ),
    "research_scope": (
        "Historical interpretation of revolution ascendant relative "
        "to natal radical houses, significators and planetary "
        "configurations. Source-only documentary claim extraction "
        "must not be represented as real-person outcomes."
    ),
}
index["source_1646_solar_revolution_historical_example_note"] = (
    "One-reader physical original 1647/1659 prints agree on source "
    "Sun 6°37′ vs day noon6°12′ in Libra, residual25′, nearest "
    "diurnal rate59′08″ versus 59′10″ observed, Maginus 20′+5′ "
    "fractional times10h08m47s, later truncation to10h08m "
    "for source meridian offset and house-table calculation21h43m. "
    "No verified 1646 astronomical/calendar parity or real life "
    "predictive outcome."
)
index["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07at_SOLAR_REVOLUTION.md"
assert index["records_count"] == sum(b["records_count"] for b in index["batches"])
assert index["read_numbered_chapters"] == list(range(1, 172))
assert index["partial_numbered_chapters"][-1]["complete"] is False
assert index["empirical_validations"] == index["runtime_promotions"] == 0
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly first original CLXXII solar return source partially documented (B07at)\n\n"
    "**24 historical source-only records R12765–R12788** on original "
    "printed734–735/PDF768–769 and distinct original 1659 second "
    "edition. Lilly defines solar return as matching natal Sun "
    "longitude and computes a 19Sep1646 example: Sun radix6°37′ "
    "Libra, noon6°12′, difference25′, old Maginus nearby rate "
    "59′08″, table 20′+5′ =10h08m47s, later printed times "
    "truncate to minute before meridian/house table yielding21h43m. "
    "This is **historic source arithmetic, not verified original "
    "ephemeris, Julian-civil time conversion or human prediction**. "
    "**Lilly 12,788+Ptolemy1,066=13,854 Western historical notes**; "
    "independent Chinese V7 154 BaZi+201 Zi Wei=355 unchanged. "
    "Original CLXXII still PARTIAL. Next **R12789**, original "
    "PDF770/printed736. Real person validations zero, runtime "
    "astrological model promotions zero.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted historical checkpoint preserved\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07at",
    "status": "GUARDED_ORIGINAL_CLXXII_SOLAR_RETURN_PARTIAL_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12764,
    "Lilly_after": 12788,
    "Ptolemy_retained": 1066,
    "Western_after": 13854,
    "Chinese_V7_retained": 355,
    "new_historical_source_only_notes": 24,
    "original_CLXXII_physically_complete": False,
    "next_R": "R12789",
    "next_pdf": 770,
    "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07at.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_sha256": accepted["source_photo_and_arithmetic_SHA256"],
    "rules_sha256": accepted["rules_SHA256"],
    "archive_sha256": release["archive_sha256"],
    "portable_tests": 38,
    "Chinese_V7_sha256": sha(CHINA),
    "independent_real_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
