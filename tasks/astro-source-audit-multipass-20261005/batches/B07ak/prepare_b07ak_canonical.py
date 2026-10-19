#!/usr/bin/env python3
"""Close PHYSICAL first printed CLXVI source span, not critical or model parity."""

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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ak_CLXVI_PHYSICAL_END.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ak-clxvi-naibod-final-20261019"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ak.json"):
    assert not f.exists(), f"Possible interrupted checkpoint: {f}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
china = j(CHINA)
data = j(B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["parent_outcome"] == "OPEN"
assert old["records_count"] == accept["Lilly_before"] == 12567
assert old["batches"][-1]["id"] == "B07aj"
assert sum(v["records_count"] for v in old["batches"]) == 12567
assert old["next"]["chapter"] == "CLXVI" and old["next"]["pdf_page"] == 749
assert len(old["partial_numbered_chapters"]) == 1
assert old["partial_numbered_chapters"][0]["complete"] is False
assert old["read_numbered_chapters"] == list(range(1, 165))
assert old["read_headed_units_count"] == 80
assert old["runtime_promotions"] == old["empirical_validations"] == 0
assert china["sum_source_annotations"] == accept["Chinese_V5_retained"] == 262
assert (
    old["source_sha256"]
    == data["source_photographic_first_and_second_edition_witnesses"]["original_1647"][
        "original_full_1647_pdf_sha256"
    ]
)
assert len(data["records"]) == len(rules["rules"]) == 14
assert [r["record_number"] for r in rules["rules"]] == list(range(12568, 12582))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert accept["Lilly_after_if_accepted"] == 12581
assert accept["Western_after_if_accepted"] == 13647
assert accept["next_original_R"] == "R12582"
assert accept["next_original_pdf_frame"] == 749
assert accept["next_printed_chapter_label"] == "CLXVI"
assert accept["next_editorial_distinct_chapter_ordinal"] == 166
assert data["source_first_printed_CLXVI_directions_time_text_physically_ends_PDF749"]
assert data["second_distinct_original_PRINTED_CLXVI_starts_same_PDF749"]
assert data["source_all_1647_numbered_chapter_physical_pages_attempted"]
assert not data["source_first_CLXVI_full_expert_diplomatic_critical_edition_complete"]
assert not data["source_old_astrological_chart_time_engine_mathematically_verified"]
assert data["cases"][0]["after_365day_year_carry"] == [12, 33, 14]
assert data["cases"][1]["after_365day_year_carry"] == [20, 57, 21]
assert accept["source_record_SHA256"] == sha(
    B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json"
)
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert release["portable_test_replays"] == 26
assert release["CRC_passed"] and release["all_member_SHA256_bytes_passed"]
assert release["independent_archive_extraction_tests_passed"]
assert release["original_source_SHA256"] == accept["source_record_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert release["old_Western_index_SHA256"] == sha(INDEX)
assert release["Chinese_V5_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json",
    ROOT / T / "batches/B07x/evidence/pdf_1647-749.jpg",
):
    relative = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(f)), relative

BACK.mkdir(exist_ok=False)
for f, n in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ak.json"),
    (CURRENT, "CURRENT_BEFORE_B07ak.md"),
    (CHINA, "CHINESE_V5_BEFORE_B07ak.json"),
):
    (BACK / n).write_bytes(f.read_bytes())
old["batches"].append(
    {
        "id": "B07ak",
        "path": "batches/B07ak/RULES.json",
        "records_count": 14,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Source-only original 1647 first printed CLXVI final folio715/PDF749 "
            "Naibod 365day+24hour carries, independently typeset original 1659 "
            "comparand, physical horizontal divider before separate annual "
            "Profections chapter repeating printed CLXVI numeral. Historical "
            "source notes R12568–R12581. First directions-time chapter now "
            "PHYSICALLY COVERED, not expert diplomatically verified because "
            "seven annual-rate print glyphs unresolved, Naibod minute27 absent, "
            "original inter-edition discrepancies and Maginus residual unresolved. "
            "True 1647 natal astronomy and human predictive accuracy zero."
        ),
    }
)
old["records_count"] = 12581
old["status"] = (
    "BOOK_III_FIRST_PHYSICAL_CLXVI_DIRECTIONS_TIME_SOURCE_SPAN_COVERED_NEXT_SEPARATE_CLXVI_PROFECTIONS"
)
p = old["partial_numbered_chapters"].pop()
assert p["chapter_heading"] == "Of the measure of time in DIRECTIONS"
assert p["physical_source_start_pdf"] == 742
assert p["accepted_through_pdf"] == 748
assert p["next_record"] == "R12568"
p["accepted_through_pdf"] = 749
p["first_printed_clxvi_source_physically_covered"] = True
p["complete"] = True
p["closed_by_batch"] = "B07ak"
p["full_source_critical_edition_complete"] = False
p["real_event_predictions_validated"] = 0
p["runtime_model_promoted"] = False
old.setdefault("completed_original_source_units_with_uncertainty", []).append(p)
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [165]
old["read_headed_units_count"] = 81
old["next"] = {
    "pdf_page": 749,
    "printed_page": 715,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "editorial_source_sequence_ordinal": 166,
    "heading": (
        "Of annual Profections, and by what means to find out the Profectionall Signe of every yeer"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Start below original physical horizontal divider p715/PDF749. "
        "A DISTINCT following physical heading also prints CHAP CLXVI "
        "but concerns annual Profections, not the prior 1647 annual "
        "direction-time chapter. Next historical source R12582. "
        "Do not infer original human event accuracy from source checks."
    ),
    "research_scope": (
        "Original printed annual Profections source definitions, 30-degree "
        "yearly movement and subsequent types; preserve repeated literal "
        "Roman numeral and independent source edition/context."
    ),
}
old["first_printed_CLXVI_source_span_covered_not_verified_note"] = (
    "B07ag–B07ak collectively traverse original PDF742–749 printed708–715 "
    "first physically printed CLXVI directions-time text. Source still "
    "contains seven one-reader unresolved zodiac annual-rate glyphs, "
    "missing original Naibod minute27, cross-edition table variants, "
    "Maginus 42/48-vs-13/4 residual arithmetic issue. Full critical "
    "edition, birth-era ephemeris/time model, human forecast validation "
    "and runtime promotion remain unresolved. Next printed distinct "
    "CLXVI annual Profections editorial ordinal166."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ak_CLXVI_PHYSICAL_END.md"
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["partial_numbered_chapters"] == []
assert old["read_numbered_chapters"] == list(range(1, 166))
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly first printed CLXVI physically covered (B07ak)\n\n"
    "**14 historical source-only records R12568–R12581** attest to "
    "original Naibod end-of-chapter p715/PDF749 and duplicate original "
    "next printed **CHAP CLXVI annual Profections** heading after "
    "the physical divider. Independently typeset 1647 and1659 "
    "originals agree: Mars terms **12y33d14h**, Mars opposition "
    "**20y57d21h** under 365day nominal carry. "
    "**12,581 Lilly+1,066 Ptolemy=13,647 Western historical source notes**, "
    "Chinese V5 101 BaZi+161 Zi Wei=262 unchanged. First physical "
    "directions-time CLXVI source pages708–715 COVERED (editorial ordinal165), "
    "NOT fully source-critically verified (seven rate glyphs/Naibod "
    "missing minute27 and original mathematical errors). New distinct "
    "printed CLXVI **annual Profections** begins **R12582** on same "
    "PDF749 printed715 (editorial ordinal166). Zero actual human "
    "predictive validations and zero runtime promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier historical checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ak",
    "status": "GUARDED_FIRST_PHYSICAL_CLXVI_COVERAGE_PREPARED_REMOTE_PUBLICATION_PENDING",
    "Lilly_before": 12567,
    "Lilly_after": 12581,
    "Ptolemy_retained": 1066,
    "Western_after": 13647,
    "Chinese_V5_retained": 262,
    "new_historical_source_notes": 14,
    "first_CLXVI_source_physical_coverage": True,
    "first_CLXVI_source_critical_expert_verification": False,
    "next_historical_R": "R12582",
    "next_original_PDF": 749,
    "next_printed_chapter": "CLXVI",
    "next_editorial_ordinal": 166,
    "prior_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ak.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "source_record_SHA256": accept["source_record_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_test_replays": 26,
    "Chinese_V5_SHA256": sha(CHINA),
    "empirical_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
