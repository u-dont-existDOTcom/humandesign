#!/usr/bin/env python3
"""Guarded one-time admission of original UNNUMBERED Moon fixed-star source notes."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07v_MOON_FIXED_STARS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


for f in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07v.json"):
    assert not f.exists(), f"Previously prepared/partially accepted; reconcile: {f}"
assert git("branch", "--show-current") == "research/astro-b07v-moon-fixed-stars-20261018"
idx = load(INDEX)
win = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
author = load(B / "SOURCE_FIRST_AUTHORING_20261018.json")
source_map = load(B / "SOURCE_TO_RECORD_MAP.json")
stars = load(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json")
witness = load(B / "ORIGINAL_SOURCE_WITNESS.json")
guard = load(B / "HISTORICAL_NONPROMOTION_GUARD_V1.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = load(CHINA)

assert sha(INDEX) == win["prior_canonical_index_sha256"] == release["prior_index_sha256"]
assert idx["records_count"] == win["prior_lilly_records"] == accept["prior_lilly"] == 12168
assert idx["batches"][-1]["id"] == "B07u"
assert idx["read_numbered_chapters"] == list(range(1, 164))
assert idx["next"]["chapter"] == "UNNUMBERED_MOON_FIXED_STARRES"
assert idx["next"]["pdf_page"] == 735 and idx["next"]["printed_chapter_numeral"] is None
assert idx["source_sha256"] == win["original_full_pdf_sha256"]
assert idx["runtime_promotions"] == idx["empirical_validations"] == 0
assert not any(x["id"] == "B07v" for x in idx["batches"])
assert rules["record_count"] == accept["new_historical_annotations"] == 100
assert rules["substantive"] == accept["substantive"] == 98
assert rules["following_navigation"] == accept["following_navigation"] == 2
assert rules["numbered_chapter_added"] == accept["numbered_chapters_added"] == 0
assert len(author["groups"]) == len(source_map["source_groups"]) == 15
assert len(stars["entries"]) == accept["source_star_entries"] == 13
assert len(witness["photos"]) == accept["source_photo_frames"] == 4
assert witness["body_original_pdf_frames"] == [735, 736, 737]
assert [r["record_number"] for r in rules["rules"]] == list(range(12169, 12269))
assert [r["role"] for r in rules["rules"][-2:]] == [
    "next_clxv_heading",
    "next_fortune_saturn",
]
assert sha(B / "RULES.json") == accept["rules_sha256"] == release["rules_sha256"]
assert (
    sha(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json")
    == (accept["star_table_sha256"])
)
assert not guard["clinical_mortality_crime_gender_religion_morality_human_inference_allowed"]
assert guard["human_predictions_validated"] == guard["runtime_model_promotions"] == 0
assert release["crc_passed"] and release["sha256_and_bytes_passed"]
assert release["independent_extraction_passed"] and release["total_replayed_tests"] == 53
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
assert chinese["sum_source_annotations"] == 97
assert chinese["runtime_promotions"] == 0
assert chinese["independently_validated_real_human_claims"] == 0
for original in (
    INDEX,
    CHINA,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07u/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    relative = str(original.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(original))
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"])

BACK.mkdir(exist_ok=False)
for original, name in (
    (INDEX, "INDEX_BEFORE_B07v.json"),
    (CURRENT, "CURRENT_BEFORE_B07v.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07v.md"),
    (CHINA, "CHINESE_V2_BEFORE_B07v.json"),
):
    (BACK / name).write_bytes(original.read_bytes())

idx["batches"].append(
    {
        "id": "B07v",
        "path": "batches/B07v/RULES.json",
        "records_count": 100,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Original 1647 UNNUMBERED 'The Moon Directed to FIXED STARRES', "
            "source starts PDF735/printed701 below CHAP CLXIIII and ends "
            "above the separately numbered CHAP CLXV Part of Fortune divider "
            "on PDF737/printed703. 100 historical-only annotations "
            "R12169-R12268 (98 substantive, 2 CLXV navigation), "
            "15 reversible original-photo source groups, 13 historical "
            "lunar fixed-star headings and old zodiac coordinates; Swan "
            "tail inherits Hydra effects, original left Orion shoulder "
            "15 Gemini distinguished from prior Midheaven 15.40, period "
            "0°10 Pisces and other explicit minutes retained. Four original "
            "PDF735-738 JPEGs, SHA/byte witness and 53 portable ZIP CRC/sha "
            "tests passed. No increment to numbered-chapter count. "
            "Medical/death/crime, religion, sex and class stereotypes "
            "remain documentary-only: ZERO verified people or model "
            "runtime promotions. Independent Chinese V2 97 unchanged."
        ),
    }
)
idx["records_count"] = 12268
# Intentionally preserve the printed numbered-chapter sequence and legacy
# read_headed_units_count; explicit acceptance note records this new unnumbered unit.
idx["status"] = "BOOK_III_UNNUMBERED_MOON_FIXED_STARS_NEXT_CLXV_FORTUNE_DIRECTIONS"
idx["next"] = {
    "pdf_page": 737,
    "printed_page": 703,
    "chapter": "CLXV",
    "printed_chapter_numeral": "CLXV",
    "heading": "The Directions of the PART OF FORTUNE",
    "numbered": True,
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original printed CHAP CLXV starts BELOW independent divider on "
        "PDF737/printed703 after final unnumbered Moon-to-Hercules stellar "
        "case. Part-of-Fortune directions to planetary bodies and aspects "
        "continue through PDF738-741 and all 12 house cusps to upper "
        "PDF742/printed708. Next printed CHAP CLXVI Of the measure of "
        "time in DIRECTIONS begins below divider PDF742. "
        "Next source annotation R12269; do NOT double count Moon stars."
    ),
    "research_scope": (
        "First-edition Part Fortune directions, interplanetary aspects, "
        "star headings and 12 house cusps, source-only; following "
        "CLXVI contains numeric direction-year calculation methods."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["unnumbered_moon_fixed_starres_source_acceptance_note"] = (
    "B07v original-first-edition unnumbered lunar fixed-star unit R12169-R12268, "
    "100 notes, 13 stellar headings, 15 original photo groups PDF735-737, "
    "53 independently extracted archive tests. Numbered chapter count "
    "unchanged, next printed CHAP CLXV PDF737. No individual empirical "
    "predictions or live model promotion; separate Chinese V2 97 unchanged."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 12268
assert idx["read_numbered_chapters"] == list(range(1, 164))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

headline = (
    "# Original Lilly 1647 unnumbered Moon fixed-star source accepted\n\n"
    "**100 historical-documentary annotations R12169–R12268**, "
    "98 substantive +2 next-chapter navigation, from 15 reversible "
    "original-photo groups PDF735–737/printed701–703 and 13 historic "
    "lunar star headings, with 53 CRC/hash ZIP-extracted tests. "
    "**12,268 Lilly +1,066 Ptolemy=13,334 Western historical notes**; "
    "independent **97 Chinese BaZi and Zi Wei historic-only notes**. "
    "Next printed **CHAP CLXV Part of Fortune Directions** starts "
    "lower PDF737/printed703 at **R12269**; following CHAP CLXVI "
    "original direction time calculation begins PDF742. "
    "No numbered chapter added for this unnumbered source unit. "
    "No empirical human predictive successes, medical or mortality "
    "validity, verified old-to-modern stellar epoch conversion, or "
    "executed model promotions.\n\n"
)
for f in (CURRENT, PROGRESS):
    previous = f.read_text(encoding="utf-8")
    f.write_text(headline + "## Earlier retained research state\n\n" + previous, encoding="utf-8")
LATEST.write_text(
    headline + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07v",
    "status": "CANONICAL_PREPARED_PENDING_REMOTE_READBACK",
    "lilly_before": 12168,
    "lilly_after": 12268,
    "added_unnumbered_historical_annotations": 100,
    "numbered_chapter_count_delta": 0,
    "retained_ptolemy": 1066,
    "western_total": 13334,
    "separate_chinese_v2": 97,
    "old_index_sha256": win["prior_canonical_index_sha256"],
    "new_index_sha256": sha(INDEX),
    "rules_sha256": sha(B / "RULES.json"),
    "source_archive_sha256": release["archive_sha256"],
    "portable_source_tests": 53,
    "next": "R12269 printed CLXV original PDF737 lower",
    "independent_human_forecast_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
