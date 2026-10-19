#!/usr/bin/env python3
"""Guarded second printed CLXVI original historical source admission.

Physical 1647 annual-profections source traversed, but source table zodiac
glyphs/era astronomy/full validated chart and actual human predictions NOT.
The duplicate printed CLXVI survives verbatim in index and source records.
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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07al_PROFECTIONS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07al-annual-profections-opening-20261019"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    d = Path.home() / "Téléchargements"
    return d if d.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07al.json"):
    assert not f.exists(), f"Previous/interrupted admission: {f}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
china = j(CHINA)
source = j(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
rel = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert old["records_count"] == accept["prior_Lilly"] == 12581
assert old["batches"][-1]["id"] == "B07ak"
assert old["next"]["editorial_source_sequence_ordinal"] == 166
assert old["next"]["printed_chapter_numeral"] == "CLXVI"
assert old["next"]["pdf_page"] == 749
assert old["read_numbered_chapters"] == list(range(1, 166))
assert old["read_headed_units_count"] == 81
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == source["original_Wellcome_first_edition_full_PDF_SHA256"]
assert china["sum_source_annotations"] == accept["Chinese_V5_retained"] == 262
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert len(source["records"]) == len(rules["rules"]) == 30
assert [r["record_number"] for r in rules["rules"]] == list(range(12582, 12612))
assert source["second_distinct_PRINTED_CLXVI_source_unit"]
assert source["next_PRINTED_CLXVII_starts_on_same_original_PDF752"]
assert source["original_merchant_table_physical_source_rows"] == 72
assert not source["all_merchant_table_zodiac_cells_expert_collated"]
assert source["printed_monthly_profection_parts"] == 13
assert source["printed_diurnal_sign_days_hours_minutes"] == [2, 3, 54]
assert accept["Lilly_if_accepted"] == 12611
assert accept["Western_if_accepted"] == 13677
assert accept["next_source_R"] == "R12612"
assert accept["next_original_pdf_frame"] == 752
assert accept["next_editorial_source_ordinal"] == 167
assert accept["next_printed_numeral"] == "CLXVII"
assert accept["source_SHA256"] == sha(
    B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json"
)
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert rel["test_count"] == 43
assert rel["CRC_passed"] and rel["members_sha256_bytes_passed"]
assert rel["independent_extracted_test_replay_passed"]
assert rel["source_SHA256"] == accept["source_SHA256"]
assert rel["rules_SHA256"] == accept["rules_SHA256"]
assert rel["prior_Western_index_SHA256"] == sha(INDEX)
assert rel["Chinese_V5_SHA256"] == sha(CHINA)
assert sha(downloads() / rel["filename"]) == rel["archive_sha256"]
for f in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07ak/RULES.json",
    ROOT / T / "batches/B07x/evidence/pdf_1647-749.jpg",
    ROOT / T / "batches/B07x/evidence/pdf_1647-750.jpg",
):
    target = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + target) == git("hash-object", str(f)), target

BACK.mkdir(exist_ok=False)
for f, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07al.json"),
    (CURRENT, "CURRENT_BEFORE_B07al.md"),
    (CHINA, "CHINESE_V5_BEFORE_B07al.json"),
):
    (BACK / name).write_bytes(f.read_bytes())

old["batches"].append(
    {
        "id": "B07al",
        "path": "batches/B07al/RULES.json",
        "records_count": 30,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Original SECOND distinct printed CHAP CLXVI on annual Profections, "
            "original 1647 PDF749–752 printed715–718; 30 source-only historical "
            "annotations R12582–R12611. One sign/solar return year with 12year "
            "cycle, annual sign shift preserving natal degrees/minutes, original "
            "monthly 13 equal parts and diurnal 2d3h54min per sign, merchant "
            "example annual table physically shows 72 years 1616–1687 but "
            "individual glyph tracks not critically collated. Year25 uses "
            "24 completed years, example profected ascendant Capricorn6°37, "
            "nominal one degree12d4h12m. Physically new CLXVII heading "
            "starts on PDF752, not merged. Source/old calendar/year mechanics "
            "and human event prediction unvalidated."
        ),
    }
)
old["records_count"] = 12611
old["status"] = (
    "BOOK_III_SECOND_PRINTED_CLXVI_ANNUAL_PROFECTIONS_PHYSICAL_SOURCE_COVERED_NEXT_CLXVII"
)
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [166]
old["read_headed_units_count"] = 82
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXVI",
        "editorial_source_ordinal": 166,
        "source_unit": "SECOND physically separate original printed CLXVI annual Profections",
        "heading": (
            "Of annual Profections, and by what means to find out "
            "the Profectionall Signe of every yeer"
        ),
        "physical_start_pdf": 749,
        "physical_end_pdf": 752,
        "accepted_batch": "B07al",
        "physical_pages_traversed": True,
        "merchant_table_72_historical_years_visible": True,
        "all_merchant_table_zodiac_cells_independently_verified": False,
        "complete": True,
        "full_expert_critical_edition_complete": False,
        "true_original_solar_return_date_and_chart_engine_verified": False,
        "actual_human_prediction_accuracy_validated": False,
    }
)
old["next"] = {
    "pdf_page": 752,
    "printed_page": 718,
    "chapter": "CLXVII",
    "printed_chapter_numeral": "CLXVII",
    "editorial_source_sequence_ordinal": 167,
    "heading": "Of the Use of Profections, and their Effects",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 PDF752/printed718 below horizontal divider "
        "begins CHAP CLXVII of annual Profections' use/effects. "
        "Preceding second printed CLXVI chapter is physically covered, "
        "but merchant chart table individual glyphs not expert "
        "collated and no human predictive validation. Next R12612."
    ),
    "research_scope": (
        "Original historical profection and direction conjunction rules, "
        "timing claims and qualifications, not measured person data."
    ),
}
old["source_duplicate_printed_CLXVI_preservation_note"] = (
    "First distinct physically printed CLXVI original directions-time is "
    "editorial ordinal165 source pages PDF742–749; second distinct "
    "physically printed CLXVI annual Profections editorial ordinal166 "
    "PDF749–752. Original duplicated Roman text preserved. Following "
    "printed CLXVII starts PDF752. Physical reading complete but "
    "critical star table text, proper original natal/calendar engine "
    "and actual-person predictions not verified."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07al_PROFECTIONS.md"
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 167))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly second printed CLXVI Annual Profections physically covered (B07al)\n\n"
    "**30 source-only historical records R12582–R12611** preserve "
    "the separate duplicated printed CHAP CLXVI Annual Profections "
    "p715–718/PDF749–752. 30 degrees/one sign per solar-return year, "
    "12-year cycle, source literal 13 monthly parts, printed "
    "diurnal 2d3h54min/sign, and nominal 12d4h12min per degree. "
    "Merchant example 72 historical year rows 1616–1687 physically "
    "evidenced, but individual chart cells NOT critically collated. "
    "**12,611 Lilly+1,066 Ptolemy =13,677 Western source records**; "
    "Chinese V5 101 BaZi+161 Zi Wei=262 unchanged. The next physical "
    "**CHAP CLXVII Use of Profections and their Effects** begins "
    "original **R12612 PDF752/printed718** after divider. Both printed "
    "CLXVI headings remain separately indexed. No real-person "
    "predictive success, actual original-era chart engine or runtime "
    "promotion verified.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted source checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
rec = {
    "batch": "B07al",
    "status": "SECOND_PRINTED_CLXVI_PHYSICAL_SOURCE_ADMISSION_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12581,
    "Lilly_after": 12611,
    "Ptolemy_retained": 1066,
    "Western_after": 13677,
    "Chinese_V5_retained": 262,
    "new_source_only_records": 30,
    "second_distinct_printed_CLXVI_source_pages_covered": True,
    "merchant_72year_table_all_cells_critically_verified": False,
    "next_R": "R12612",
    "next_original_PDF": 752,
    "next_printed_chapter": "CLXVII",
    "prior_Western_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07al.json"),
    "new_Western_SHA256": sha(INDEX),
    "source_SHA256": accept["source_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": rel["archive_sha256"],
    "portable_tests_replayed": 43,
    "Chinese_V5_SHA256": sha(CHINA),
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rec, indent=2))
