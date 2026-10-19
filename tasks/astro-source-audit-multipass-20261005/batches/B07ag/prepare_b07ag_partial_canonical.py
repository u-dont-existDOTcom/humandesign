#!/usr/bin/env python3
"""Guarded PARTIAL 1647 printed CLXVI source acceptance: 29 original notes.

Append only; leave CLXVI incomplete, no new completed numbered chapter;
preserve previous original source files and Chinese V5 unchanged.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ag_PARTIAL_CLXVI.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ag-maginus-sun-longitude-20261019"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


for file in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ag.json"):
    assert not file.exists(), f"Already prepared or interrupted; reconcile: {file}"
assert git("branch", "--show-current") == BRANCH
prior = load(INDEX)
chinese = load(CHINA)
notes = load(B / "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json")
witness = load(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = load(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH
assert task["parent_outcome"] == "OPEN"
assert prior["records_count"] == accepted["prior_Lilly"] == 12472
assert sum(b["records_count"] for b in prior["batches"]) == 12472
assert prior["batches"][-1]["id"] == "B07w"
assert prior["next"]["chapter"] == "CLXVI"
assert prior["next"]["pdf_page"] == 742
assert prior["partial_numbered_chapters"] == []
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
assert prior["source_sha256"] == witness["full_1647_original_pdf_sha256"]
assert chinese["sum_source_annotations"] == accepted["parallel_Chinese_V5"] == 262
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert prior["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accepted["prior_Ptolemy"] == 1066
assert rules["record_count"] == notes["historical_source_claim_count"] == 29
assert len(rules["rules"]) == len(witness["photographic_source_note_receipts"]) == 29
assert [r["record_number"] for r in rules["rules"]] == list(range(12473, 12502))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert accepted["rules_sha256"] == sha(B / "RULES.json")
assert accepted["source_witness_sha256"] == sha(
    B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"
)
assert accepted["lilly_after"] == 12501
assert accepted["western_after"] == 13567
assert accepted["next_original_source_id"] == "R12502"
assert witness["source_edition_comparison_status"] == (
    "FIRST_AND_SECOND_PHYSICAL_PRINT_CONFIRM_7_36"
)
assert release["crc_passed"] and release["all_member_SHA256_and_sizes_passed"]
assert release["independently_extracted_tests_passed"] and release["portable_test_replays"] == 43
assert release["rules_sha256"] == accepted["rules_sha256"]
assert release["source_witness_sha256"] == accepted["source_witness_sha256"]
assert sha(downloads() / release["archive_filename"]) == release["archive_sha256"]
assert sha(INDEX) == release["prior_Lilly_source_index_sha256"]
assert sha(CHINA) == release["parallel_Chinese_V5_source_index_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07w/RULES.json",
    ROOT / T / "batches/B07x/ORIGINAL_SOURCE_WINDOW_V1.json",
    ROOT / T / "batches/B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ag.json"),
    (CURRENT, "CURRENT_BEFORE_B07ag.md"),
    (CHINA, "CHINESE_V5_BEFORE_B07ag.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

prior["batches"].append(
    {
        "id": "B07ag",
        "path": "batches/B07ag/RULES.json",
        "records_count": 29,
        "sha256": sha(B / "RULES.json"),
        "scope": (
            "PARTIAL printed first original Lilly CHAP CLXVI directions time "
            "method, PDF742–744 printed708–710, only first three source pages. "
            "29 historical source annotations R12473–R12501, three original "
            "1647 source photo frames plus separately typeset 1659 print p710. "
            "Both original editions read next-day Sun 7°36' Libra, conflicting "
            "with modern derivative 7°37'; 54 arcmin annual RA example otherwise "
            "unchanged. Annual 372 source-rate cells, Naibod printed tables, "
            "Maginus residual and true directional chronology are NOT accepted. "
            "Numbered first CLXVI remains PARTIAL; no additional completed chapter; "
            "zero predictive human validations or runtime promotions."
        ),
    }
)
prior["records_count"] = 12501
prior["status"] = "BOOK_III_CLXVI_TIME_MEASURE_PARTIAL_SOURCE_PAGES708_710_NEXT_ANNUAL_TABLE"
prior["partial_numbered_chapters"].append(
    {
        "printed_chapter": "CLXVI",
        "source_unit": "first of two physically separate headings printed CLXVI",
        "chapter_heading": "Of the measure of time in DIRECTIONS",
        "physical_source_start_pdf": 742,
        "accepted_through_pdf": 744,
        "next_unaccepted_pdf": 745,
        "next_record": "R12502",
        "accepted_batch": "B07ag",
        "complete": False,
        "original_numerical_tables_exhaustively_verified": False,
    }
)
prior["next"] = {
    "pdf_page": 745,
    "printed_page": 711,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "heading": "Of the measure of time in DIRECTIONS — continued original annual rate table",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Same first printed CLXVI, source annual zodiac 12 signs×31 rows "
        "original PDF745/printed711; original one-reader 365 legible, "
        "seven ambiguous and 1659 hints do not resolve 1647 print. "
        "Then follow printed 712–715 Maginus and Naibod time calculations "
        "until separate duplicated-number CLXVI annual-profections heading. "
        "Next historical source R12502; do not accept full chapter yet."
    ),
    "research_scope": (
        "First-edition literal rate table, printed Maginus and Naibod "
        "work examples, independent 1659 comparator and exact historical "
        "arithmetic; source-epoch chart/time engine and real-human validity "
        "unverified."
    ),
}
prior["chapter_CLXVI_partial_original_opening_acceptance_note"] = (
    "B07ag accepts only 29 source-only first three page annotations, "
    "Ptolemaic and Maginus competing time method descriptions and corrected "
    "modern derivative 7°37' versus actual first+second editions 7°36'. "
    "The physically distinct subsequent duplicated heading CHAP CLXVI "
    "on annual profections is not merged. Complete time chapter not yet "
    "accepted, historical engine unverified, human evaluations zero."
)
assert prior["read_numbered_chapters"] == list(range(1, 165))
assert prior["partial_numbered_chapters"][-1]["complete"] is False
assert prior["records_count"] == sum(x["records_count"] for x in prior["batches"])
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
assert chinese["sum_source_annotations"] == 262
prior["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ag_PARTIAL_CLXVI.md"
INDEX.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly 1647 original historical CLXVI opening accepted PARTIALLY (B07ag)\n\n"
    "**29 new historical source-only rules R12473–R12501** on printed "
    "folios708–710/PDF742–744; source photo SHA and modern derivative "
    "phrase-locator witnesses recorded. Physical original 1647 and "
    "separately typeset 1659 printed p710 both read next-day Sun "
    "**7°36′ Libra**, against modern searchable text 7°37′; original "
    "Maginus Sun right ascension values remain 186°04′→186°58′ = 54′. "
    "**12,501 accepted Lilly historical notes +1,066 Ptolemy =13,567 Western**. "
    "Independent Chinese historical V5 **101 BaZi +161 Zi Wei=262**, unchanged. "
    "Original printed CLXVI numerical directions-time chapter remains "
    "**PARTIAL** (not counted as a completed chapter); next R12502 "
    "original PDF745/printed711 annual direction rate table, followed by "
    "Maginus/Naibod unresolved mathematics. No real-person predictive "
    "validations and no runtime model promotions.\n\n"
)
oldcurrent = CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    summary + "## Previous accepted historical checkpoint retained verbatim\n\n" + oldcurrent,
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ag",
    "status": "GUARDED_PARTIAL_ORIGINAL_LILLY_INDEX_PREPARED_PUBLICATION_PENDING",
    "lilly_before": 12472,
    "lilly_after": 12501,
    "ptolemy_retained": 1066,
    "Western_historical_after": 13567,
    "Chinese_V5_retained": 262,
    "new_source_only_records": 29,
    "next_original_R": "R12502",
    "next_original_PDF": 745,
    "CLXVI_complete": False,
    "original_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ag.json"),
    "new_index_SHA256": sha(INDEX),
    "Chinese_V5_SHA256": sha(CHINA),
    "release_archive_SHA256": release["archive_sha256"],
    "portable_archive_replayed_tests": 43,
    "empirical_human_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
