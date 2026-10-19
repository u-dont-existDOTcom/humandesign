#!/usr/bin/env python3
"""Source-only guarded B07am partial CLXVII append-only canonical admission."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07am_CLXVII_PARTIAL.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07am-clxvii-use-profections-20261019"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    path = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if path is not None and path.is_dir() and path.resolve() != Path.home().resolve():
        return path
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07am.json"):
    assert not f.exists(), f"Interrupted/old acceptance requires reconciliation: {f}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
chinese = j(CHINA)
original = j(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
rules = j(B / "RULES.json")
a = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert old["records_count"] == a["prior_Lilly"] == 12611
assert old["batches"][-1]["id"] == "B07al"
assert old["next"]["editorial_source_sequence_ordinal"] == 167
assert old["next"]["chapter"] == "CLXVII" and old["next"]["pdf_page"] == 752
assert old["read_numbered_chapters"] == list(range(1, 167))
assert old["partial_numbered_chapters"] == []
assert old["runtime_promotions"] == old["empirical_validations"] == 0
assert old["source_sha256"] == original["original_1647_pdf_SHA256"]
assert chinese["sum_source_annotations"] == a["Chinese_V5_retained"] == 262
assert a["Ptolemy_retained"] == 1066
assert rules["record_count"] == a["historical_source_annotations_added"] == 14
assert [r["record_number"] for r in rules["rules"]] == list(range(12612, 12626))
assert not rules["chapter_complete"]
assert original["source_printed_721_table_not_yet_accepted"]
assert a["Lilly_if_accepted"] == 12625 and a["next_R"] == "R12626"
assert a["next_PDF"] == 755
assert a["notes_SHA256"] == sha(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
assert a["rules_SHA256"] == sha(B / "RULES.json")
assert release["CRC_passed"] and release["member_shas_and_sizes_passed"]
assert release["independent_archive_replayed_24_tests"]
assert release["source_sha256"] == a["notes_SHA256"]
assert release["rules_sha256"] == a["rules_SHA256"]
assert release["original_index_sha256"] == sha(INDEX)
assert release["Chinese_V5_sha256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07al/RULES.json",
    ROOT / TASK / "batches/B07al/evidence/1647_original_pdf-752.jpg",
):
    path = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + path) == git("hash-object", str(f)), path

BACK.mkdir(exist_ok=False)
for p, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07am.json"),
    (CURRENT, "CURRENT_BEFORE_B07am.md"),
    (CHINA, "CHINESE_V5_BEFORE_B07am.json"),
):
    (BACK / name).write_bytes(p.read_bytes())

old["batches"].append(
    {
        "id": "B07am",
        "path": "batches/B07am/RULES.json",
        "records_count": 14,
        "sha256": a["rules_SHA256"],
        "scope": (
            "Original 1647 printed CLXVII Use of Profections and Effects "
            "begins lower printed718/PDF752 and continues printed719–720 "
            "PDF753–754. 14 source-only historical annotations R12612–R12625 "
            "on corroborating directions, differing profectional effects, "
            "lord-of-year sign ruler, within-sign degree limits, and "
            "instructions to use future degree/minute calendar table. "
            "P721/PDF755 tabular cells not yet transcribed; full CLXVII "
            "physically open, no measured human predictive validity."
        ),
    }
)
old["records_count"] = 12625
old["status"] = "BOOK_III_CLXVII_USE_OF_PROFECTIONS_PARTIAL_TO_P720_NEXT_TIME_TABLE"
old["partial_numbered_chapters"].append(
    {
        "printed_chapter": "CLXVII",
        "editorial_source_ordinal": 167,
        "source_unit": "Of the Use of Profections, and their Effects",
        "physical_source_start_pdf": 752,
        "accepted_through_pdf": 754,
        "next_unaccepted_pdf": 755,
        "next_record": "R12626",
        "accepted_batch": "B07am",
        "complete": False,
        "next_calendar_table_original_glyphs_read": False,
        "independent_original_edition_critically_verified": False,
        "genuine_real_human_event_predictions_validated": 0,
    }
)
old["next"] = {
    "pdf_page": 755,
    "printed_page": 721,
    "chapter": "CLXVII",
    "printed_chapter_numeral": "CLXVII",
    "editorial_source_sequence_ordinal": 167,
    "heading": "Of the Use of Profections, and their Effects — degree and minute time tables",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 printed721/PDF755 contains two tabular physical "
        "conversions for profectional degrees and minutes into day/hour/minute "
        "intervals; the original 1647 source has unusual printed entries. "
        "Do not infer accurate natal calendar dates or all source cells "
        "before source-critical collation. Next R12626. "
        "Original CLXVII chapter remains PARTIAL."
    ),
    "research_scope": (
        "Original historical 1647 degree and minute time tabulation, "
        "print/edition fidelity; later actual ephemeris and human forecasts separate."
    ),
}
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07am_CLXVII_PARTIAL.md"
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["partial_numbered_chapters"][-1]["complete"] is False
assert old["read_numbered_chapters"] == list(range(1, 167))
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Original Lilly CLXVII opening PARTIAL p718–720 (B07am)\n\n"
    "**14 new source-only historical annotations R12612–R12625**, "
    "physically anchored to original printed718–720/PDF752–754 "
    "after prior original CLXVI annual Profections chapter. "
    "Lilly discusses concordance/contradiction of directions and "
    "profections, lord-of-year, separate fifteen-degree segments "
    "and use of a following conversion table. These are historically "
    "conditional interpretive statements, not measured life predictions. "
    "Lilly source count **12,625** + Ptolemy **1,066** = Western **13,691**; "
    "parallel Chinese V5 **101 BaZi+161 Zi Wei=262** unchanged. "
    "Chapter CLXVII remains PARTIAL, next original **R12626 PDF755 "
    "printed721** two original conversion tables. No full birth-era "
    "calendar/astronomy proof, human prediction validation or runtime promotion.\n\n"
)
CURRENT.write_text(
    summary + "## Earlier accepted checkpoint retained\n\n" + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07am",
    "status": "ORIGINAL_CLXVII_SOURCE_PARTIAL_PREPARED_GITHUB_PENDING",
    "Lilly_before": 12611,
    "Lilly_after": 12625,
    "Ptolemy_retained": 1066,
    "Western_after": 13691,
    "Chinese_V5_retained": 262,
    "new_history_annotations": 14,
    "next_R": "R12626",
    "next_original_PDF": 755,
    "chapter_complete": False,
    "old_index_sha256": sha(BACK / "LILLY_INDEX_BEFORE_B07am.json"),
    "new_index_sha256": sha(INDEX),
    "source_sha256": a["notes_SHA256"],
    "rules_sha256": a["rules_SHA256"],
    "archive_sha256": release["archive_sha256"],
    "source_zip_tests": 24,
    "Chinese_V5_sha256": sha(CHINA),
    "real_person_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
