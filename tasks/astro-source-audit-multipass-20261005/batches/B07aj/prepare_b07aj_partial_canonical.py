#!/usr/bin/env python3
"""Guarded B07aj original Naibod first/second edition source index append.

Accepted as 21 historical source annotations, NOT 149 fake independent rules,
NOT true original-time chart math, NOT a complete original first CLXVI chapter.
"""

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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aj_NAIBOD.md"
BACK = B / "recovery"
REC = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07aj-naibod-original-tables-20261019"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for p in (LATEST, REC, BACK / "LILLY_INDEX_BEFORE_B07aj.json"):
    assert not p.exists(), f"Possible prior/interrupted canonical admission: {p}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
china = j(CHINA)
data = j(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")
rules = j(B / "RULES.json")
a = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert old["records_count"] == a["Lilly_before"] == 12546
assert old["batches"][-1]["id"] == "B07ai"
assert sum(x["records_count"] for x in old["batches"]) == 12546
assert old["next"]["chapter"] == "CLXVI" and old["next"]["pdf_page"] == 747
assert old["read_numbered_chapters"] == list(range(1, 165))
assert len(old["partial_numbered_chapters"]) == 1
assert old["partial_numbered_chapters"][0]["complete"] is False
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert china["sum_source_annotations"] == a["Chinese_V5_retained"] == 262
assert old["source_sha256"] == a["original_first_edition_1647_full_pdf_SHA256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert a["Ptolemy_retained"] == 1066
assert len(data["rows"]) == 149
assert data["source_degree_rows"] == 90
assert data["source_minute_rows_visible"] == 59
assert data["missing_original_1647_printed_minute_labels"] == [27]
assert data["human_prediction_validations"] == data["runtime_promotions"] == 0
assert rules["record_count"] == a["source_note_count"] == 21
assert [r["record_number"] for r in rules["rules"]] == list(range(12547, 12568))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert a["Lilly_after_if_accepted"] == 12567
assert a["Western_after_if_accepted"] == 13633
assert a["next_record_id"] == "R12568" and a["next_original_pdf_frame"] == 749
assert a["source_crosswalk_SHA256"] == sha(
    B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"
)
assert a["rules_SHA256"] == sha(B / "RULES.json")
assert release["archive_crc_passed"] and release["archive_members_sha_bytes_verified"]
assert release["extracted_test_replay_passed"] and release["test_count"] == 160
assert release["source_crosswalk_sha256"] == a["source_crosswalk_SHA256"]
assert release["rules_sha256"] == a["rules_SHA256"]
assert release["old_Western_source_SHA256"] == sha(INDEX)
assert release["Chinese_V5_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]

for f in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07x/NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json",
    ROOT / TASK / "batches/B07x/NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json",
    ROOT / TASK / "batches/B07ai/RULES.json",
):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

BACK.mkdir(exist_ok=False)
for f, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07aj.json"),
    (CURRENT, "CURRENT_BEFORE_B07aj.md"),
    (CHINA, "CHINESE_V5_BEFORE_B07aj.json"),
):
    (BACK / name).write_bytes(f.read_bytes())
old["batches"].append(
    {
        "id": "B07aj",
        "path": "batches/B07aj/RULES.json",
        "records_count": 21,
        "sha256": a["rules_SHA256"],
        "scope": (
            "PARTIAL original first Lilly printed CLXVI time directions, "
            "Naibod original printed713/PDF747 degree and printed714/PDF748 "
            "minute time-conversion tables. 21 source-only documentary "
            "R12547–R12567 annotate 90 first-edition degree rows and 59 "
            "visibly numbered minute rows, original minute27 label missing "
            "and minute1-day glyph undeciphered. Preserve printed degree69 "
            "year70, degree80 24h, minute8 44d10h, minute44 differing "
            "1647/1659, minute60 374d14h, and 11deg/55min terms lookup. "
            "Two separately typeset source-edition photos witnessed, "
            "not complete expert 149-cell critical collation. No original "
            "astrological birth time engine or human event validation."
        ),
    }
)
old["records_count"] = 12567
old["status"] = "BOOK_III_CLXVI_TIME_MEASURE_PARTIAL_NAIBOD_TABLES_NEXT_PRINT715"
p = old["partial_numbered_chapters"][0]
assert p["latest_accepted_batch"] == "B07ai"
p["accepted_through_pdf"] = 748
p["next_unaccepted_pdf"] = 749
p["next_record"] = "R12568"
p["latest_accepted_batch"] = "B07aj"
p["original_Naibod_table_90_degree_59_visible_minute_source_documented"] = True
p["minute_27_print_label_omitted"] = True
p["naibod_full_critical_edition_finished"] = False
assert not p["complete"]
old["next"] = {
    "pdf_page": 749,
    "printed_page": 715,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "heading": (
        "Of the measure of time in DIRECTIONS — final Naibod worked "
        "example and physical chapter divider"
    ),
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Continue first printed CLXVI p715/PDF749: original Naibod "
        "365-day carry, Mars opposition worked result, then locate "
        "physically distinct second printed CHAP CLXVI annual-profections "
        "heading. Next historical annotation R12568; separately document "
        "historic source vs arithmetic and incomplete expert 1647 glyphs."
    ),
    "research_scope": (
        "Finish original printed time-directions section without merging "
        "the duplicate numbered annual Profections; source-only historical "
        "time conversion and real human predictive validity separate."
    ),
}
old["chapter_CLXVI_partial_Naibod_tables_note"] = (
    "B07aj accepted 21 source-only observations of 90 degree and "
    "59 visibly numbered minute Naibod table values, preserving "
    "minute27 absent, minute1 glyph uncertainty, degree69 year70 "
    "rollover, minute44 inter-edition difference and 60-minute anomaly. "
    "First printed CLXVI still PARTIAL; no natal predictive validation."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aj_NAIBOD.md"
assert old["records_count"] == sum(v["records_count"] for v in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 165))
assert not old["partial_numbered_chapters"][0]["complete"]
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly 1647 Naibod tables accepted as PARTIAL source (B07aj)\n\n"
    "**21 historical documentary notes R12547–R12567** preserve "
    "original printed713–714 first/second-edition Naibod tables, "
    "90 degree source rows plus 59 explicitly labeled minute rows "
    "(minute27 missing). Source first-minute day digit unresolved; "
    "degree69 printed year70, degree80 24 hours, minute8 44days, "
    "minute44 first/second-edition difference, minute60 374days14hours "
    "all retained, not math-corrected. **12,567 Lilly+1,066 Ptolemy "
    "=13,633 Western historical records**, independent Chinese V5 "
    "**101 BaZi+161 Zi Wei=262**, unchanged. First original physically "
    "printed CLXVI directions-time chapter remains PARTIAL; next "
    "**R12568 original PDF749 printed715** Naibod calculations and "
    "separate following duplicate-numbered annual Profections. "
    "Zero real-person predictions or runtime model promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted historical checkpoint preserved\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07aj",
    "status": "GUARDED_NAIBOD_TABLE_SOURCE_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12546,
    "Lilly_after": 12567,
    "Ptolemy_retained": 1066,
    "Western_after": 13633,
    "Chinese_V5_retained": 262,
    "new_source_notes": 21,
    "original_degree_rows": 90,
    "original_minute_labels_visible": 59,
    "next_R": "R12568",
    "next_PDF": 749,
    "full_CLXVI_complete": False,
    "prior_Western_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07aj.json"),
    "new_Western_SHA256": sha(INDEX),
    "source_crosswalk_SHA256": a["source_crosswalk_SHA256"],
    "rules_SHA256": a["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_tests_replayed": 160,
    "Chinese_V5_SHA256": sha(CHINA),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
REC.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
