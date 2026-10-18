#!/usr/bin/env python3
"""Guarded one-time canonical acceptance of original Lilly 1647 printed CLXV."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07w_PART_FORTUNE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


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


for file in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07w.json"):
    assert not file.exists(), f"Already partially accepted; reconcile {file}"

assert git("branch", "--show-current") == "research/astro-b07w-fortuna-directions-20261018"
index = load(INDEX)
win = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
author = load(B / "SOURCE_FIRST_AUTHORING_20261018.json")
mapping = load(B / "SOURCE_TO_RECORD_MAP.json")
witness = load(B / "ORIGINAL_SOURCE_WITNESS.json")
stars = load(B / "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json")
guard = load(B / "HISTORICAL_NONPROMOTION_GUARD_V1.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
china = load(CHINESE)

assert sha(INDEX) == win["parent_index_sha256"] == release["previous_index_sha256"]
assert index["records_count"] == accept["prior_lilly"] == 12268
assert index["read_numbered_chapters"] == list(range(1, 164))
assert index["batches"][-1]["id"] == "B07v"
assert index["next"]["chapter"] == index["next"]["printed_chapter_numeral"] == "CLXV"
assert index["next"]["pdf_page"] == 737
assert index["source_sha256"] == win["full_pdf_original_sha256"]
assert index["runtime_promotions"] == index["empirical_validations"] == 0
assert not any(b["id"] == "B07w" for b in index["batches"])
assert rules["record_count"] == accept["new_historical_annotations"] == 204
assert [x["record_number"] for x in rules["rules"]] == list(range(12269, 12473))
assert (rules["substantive"], rules["following_navigation"]) == (201, 3)
assert [x["role"] for x in rules["rules"][-3:]] == [
    "next_clxvi",
    "next_age_relevance",
    "next_ptolemy_methods",
]
assert len(author["groups"]) == len(mapping["source_groups"]) == accept["source_groups"] == 35
assert len(witness["photos"]) == accept["original_photos"] == 7
assert witness["body_pdf_frames"] == list(range(737, 743))
assert stars["historical_headings"] == len(stars["entries"]) == 3
assert all(e["original_printed_longitude_degree"] is None for e in stars["entries"])
assert sha(B / "RULES.json") == accept["rules_sha256"] == release["rules_sha256"]
assert sha(B / "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json") == accept["star_table_sha256"]
assert not guard["original_direction_numerical_math_verified"]
assert not guard["independent_real_person_predictive_accuracy_validated"]
assert not guard["real_person_crime_sex_gender_class_health_safety_money_inference_permitted"]
assert guard["runtime_rules_promoted"] == 0
assert release["crc_passed"] and release["sha256_and_bytes_passed"]
assert release["independent_extraction_passed"] and release["total_replayed_tests"] == 62
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
assert china["sum_source_annotations"] == 97
assert china["runtime_promotions"] == china["independently_validated_real_human_claims"] == 0
for path in (
    INDEX,
    CHINESE,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07v/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    rel = str(path.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(path)), rel
assert index["records_count"] == sum(x["records_count"] for x in index["batches"])

BACK.mkdir(exist_ok=False)
for path, name in (
    (INDEX, "INDEX_BEFORE_B07w.json"),
    (CURRENT, "CURRENT_BEFORE_B07w.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07w.md"),
    (CHINESE, "CHINESE_V2_BEFORE_B07w.json"),
):
    (BACK / name).write_bytes(path.read_bytes())

index["batches"].append(
    {
        "id": "B07w",
        "path": "batches/B07w/RULES.json",
        "records_count": 204,
        "sha256": accept["rules_sha256"],
        "scope": (
            "William Lilly original 1647 Christian Astrology numbered CHAP CLXV "
            "The Directions of the PART OF FORTUNE, PDF737 lower/printed703 through "
            "PDF742 upper/printed708, physical divider before independently printed "
            "CLXVI numeric directions time chapter. 204 archival source annotations "
            "R12269-R12472 (201 substantive plus 3 following-chapter navigation), "
            "35 reversible first-edition photo-anchored passage groups, 7 original "
            "JPEG source witnesses with CRC/hash/byte archive replay 62/62. Source "
            "planetary combined aspects preserved; twelve Part Fortune house cusps; "
            "three period fixed-star headings Spica Lion-heart South Balance with "
            "NO printed coordinates, null rather than invented degrees. Period "
            "mortality/crime/gender/class/religion and moralizing allegations are "
            "historical source claims only, no human predictive successes or runtime "
            "model promotions. 97 independent Chinese source notes preserved."
        ),
    }
)
index["records_count"] = 12472
index["read_numbered_chapters"].append(164)
index["status"] = "BOOK_III_CLXV_FORTUNE_NEXT_CLXVI_NUMERICAL_TIME_MEASURE"
index["next"] = {
    "pdf_page": 742,
    "printed_page": 708,
    "chapter": "CLXVI",
    "printed_chapter_numeral": "CLXVI",
    "heading": "Of the measure of time in DIRECTIONS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Distinct numbered CHAP CLXVI begins BELOW the horizontal Part Fortune "
        "divider mid PDF742/printed708. It compares competing timing methods "
        "Ptolemy, Antonius Maginus and annual-measure table after PDF744. "
        "Independently locate its ending chapter boundary, audit source "
        "numerical worked examples and table cells. Next R12473."
    ),
    "research_scope": (
        "Quantitative angular directions to event-time conversions, period "
        "astronomy and 1647 sexagesimal tables, explicit historical alternatives "
        "and corrected worked examples, not human predictive validation."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CLXV_fortuna_directions_source_acceptance_note"] = (
    "B07w original source R12269-R12472, 204 archival notes in 35 reversible "
    "groups PDF737-742; three unlocated-as-numbers star headings and 12 "
    "individual house cusps. 62 independently ZIP-extracted source tests pass. "
    "Next CLXVI original numerical arc/year method starts PDF742, R12473. "
    "No predictive human accuracy or model promotions."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 12472
assert index["read_numbered_chapters"] == list(range(1, 165))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
headline = (
    "# Original Lilly 1647 printed CLXV Part Fortune source accepted\n\n"
    "**204 historical source annotations R12269–R12472** (201 substantive "
    "plus three next CLXVI navigation) in 35 reversible original photo "
    "groups across PDF737–742. Original ecliptic longitudes for the "
    "three fixed-star headings were not printed and remain null. "
    "**12,472 Lilly +1,066 Ptolemy=13,538 Western historic notes**, "
    "separate **97 Chinese BaZi/Zi Wei historical source notes**. "
    "Next **R12473 original printed CLXVI Of the measure of time "
    "in DIRECTIONS** begins PDF742/printed708, with competing methods "
    "and an annual-direction numerical table. 62 ZIP-extracted "
    "photo/source CRC/sha tests passed; this proves documentary mapping, "
    "not event-time accuracy or personally valid health, money, moral, "
    "crime or mortality predictions. No runtime promotions.\n\n"
)
for file in (CURRENT, PROGRESS):
    old = file.read_text(encoding="utf-8")
    file.write_text(headline + "## Earlier retained research state\n\n" + old, encoding="utf-8")
LATEST.write_text(
    headline + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07w",
    "status": "CANONICAL_PREPARED_NOT_REMOTE_PUBLISHED",
    "prior_lilly": 12268,
    "accepted_lilly": 12472,
    "new_history": 204,
    "ptolemy_retained": 1066,
    "western_total": 13538,
    "Chinese_v2_retained": 97,
    "old_index_sha256": win["parent_index_sha256"],
    "new_index_sha256": sha(INDEX),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": release["archive_sha256"],
    "replayed_original_documentary_tests": 62,
    "next": "R12473 CLXVI source PDF742 below divider",
    "actual_human_predictions_verified": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
