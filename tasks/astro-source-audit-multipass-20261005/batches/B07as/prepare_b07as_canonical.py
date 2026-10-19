#!/usr/bin/env python3
"""Guarded append-only acceptance of original Lilly 1647 CLXXI source pages."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07as_CLXXI.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07as-clxxi-part-fortune-alfridary-20261019"
PARENT = "085e454ee619e1b52194ab72e9a15cea164a1477"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    loc = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if loc is not None and loc.is_dir() and loc.resolve() != Path.home().resolve():
        return loc
    fr = Path.home() / "Téléchargements"
    return fr if fr.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07as.json"):
    assert not f.exists(), f"Interrupted older acceptance requires reconciliation: {f}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
prior = load(INDEX)
china = load(CHINA)
doc = load(B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert prior["records_count"] == accept["Lilly_before"] == 12742
assert sum(x["records_count"] for x in prior["batches"]) == 12742
assert prior["batches"][-1]["id"] == "B07ar"
assert prior["next"]["chapter"] == "CLXXI"
assert prior["next"]["pdf_page"] == 766
assert prior["read_numbered_chapters"] == list(range(1, 171))
assert prior["read_headed_units_count"] == 86
assert prior["partial_numbered_chapters"] == []
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert doc["source_original_book_Wellcome_1647_full_pdf_SHA256"] == prior["source_sha256"]
assert prior["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert doc["source_twelve_house_cases_documented"]
assert doc["new_source_only_annotations"] == 22
assert rules["record_count"] == accept["new_historical_source_notes"] == 22
assert len(rules["rules"]) == 22
assert [r["record_number"] for r in rules["rules"]] == list(range(12743, 12765))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert doc["source_full_life_cycle_sequence_in_this_chapter"] is False
assert doc["historical_source_Alfridary_day_first_three_7year_lords"] == ["Sun", "Venus", "Mercury"]
assert doc["historical_source_Alfridary_night_first_three_7year_lords"] == [
    "Moon",
    "Saturn",
    "Jupiter",
]
assert accept["Lilly_after_if_accepted"] == 12764
assert accept["Western_after_if_accepted"] == 13830
assert accept["next_R"] == "R12765"
assert accept["next_original_PDF"] == 768
assert accept["next_chapter"] == "CLXXII"
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["source_records_SHA256"] == sha(
    B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json"
)
assert release["CRC_passed"] and release["every_member_SHA256_and_bytes_passed"]
assert release["independent_archive_extraction_34_tests_passed"]
assert release["portable_test_count"] == 34
assert release["source_note_SHA256"] == accept["source_records_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert release["prior_Lilly_index_sha256"] == sha(INDEX)
assert release["Chinese_V7_index_sha256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07ar/RULES.json",
    ROOT / TASK / "batches/B07aq/evidence/original_1647-766.jpg",
    ROOT / TASK / "batches/B07ar/evidence/original_1659_djvu_761.jpg",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07as.json"),
    (CURRENT, "CURRENT_BEFORE_B07as.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07as.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

prior["batches"].append(
    {
        "id": "B07as",
        "path": "batches/B07as/RULES.json",
        "records_count": 22,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Lilly original CLXXI Part of Fortune and second-house annual "
            "profection source printed732–734/PDF766–768, 1647 and separate "
            "1659 original physical editions. Twelve house claim contexts "
            "and ten historical settings, first three septennial alfridary "
            "lords day Sun/Venus/Mercury and night Moon/Saturn/Jupiter; "
            "NO full lifetime order inferred. 22 source-only historical "
            "annotations R12743–R12764. Original 1647 CLXXII begins below "
            "physical divider on printed734/PDF768, not merged into CLXXI. "
            "Human event efficacy, moral/health/wealth predictions and "
            "authentic ephemeris/calendar engine not independently validated."
        ),
    }
)
prior["records_count"] = 12764
prior["status"] = "BOOK_III_CLXXI_FORTUNE_SECOND_HOUSE_SOURCE_PHYSICALLY_COVERED_NEXT_CLXXII"
prior["read_numbered_chapters"].append(171)
prior["read_headed_units_count"] = 87
prior.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXI",
        "editorial_ordinal": 171,
        "heading": (
            "The significations of the Profectionall Signe of Part of Fortune, "
            "and Signe of the second house"
        ),
        "physical_first_edition_pdf_start": 766,
        "physical_first_edition_pdf_end": 768,
        "last_accepted_batch": "B07as",
        "physical_source_span_covered": True,
        "full_diplomatic_critical_source_edition_verified": False,
        "full_lifetime_Alfridary_canonical_planets_proven": False,
        "independent_human_predictive_outcomes_verified": 0,
        "runtime_promotions": 0,
    }
)
prior["next"] = {
    "pdf_page": 768,
    "printed_page": 734,
    "chapter": "CLXXII",
    "printed_chapter_numeral": "CLXXII",
    "editorial_source_sequence_ordinal": 172,
    "heading": "Of Revolutions",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "The separately printed CLXXII begins below a physical "
        "divider on first-edition printed734/PDF768 after the "
        "abbreviated nocturnal Alfridary source. First substantive "
        "new historical record R12765. Lilly describes a return of "
        "the Sun to exact natal zodiacal longitude and a calendar "
        "interpolation method; independent astronomical and actual "
        "birth-era predictive parity remain untested."
    ),
    "research_scope": (
        "Original printed solar revolution, return timing, epoch "
        "and true apparent Sun motion; compare exact first and "
        "separately typeset second printed numerical examples, "
        "never promote self-consistent source as human validation."
    ),
}
prior["chapter_CLXXI_original_source_history_note"] = (
    "B07as 22 documentary annotations covering 12 original Part Fortune/"
    "second-house house contexts and only first three Alfridary septennial "
    "lords by day and night. The CLXXII page734 source physical boundary "
    "is proven in both printed editions; 1647/1659 page transcriptions "
    "and any actual human predictions remain unverified independently."
)
prior["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07as_CLXXI.md"
assert prior["records_count"] == sum(v["records_count"] for v in prior["batches"])
assert prior["read_numbered_chapters"] == list(range(1, 172))
assert prior["partial_numbered_chapters"] == []
assert prior["empirical_validations"] == prior["runtime_promotions"] == 0
INDEX.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly CLXXI physical source covered: Fortune, second house and first Alfridary periods\n\n"
    "**22 historical documentary notes R12743–R12764** from actual 1647 "
    "and independent separately printed 1659 pages 732–734. Twelve "
    "Part Fortune/second-house house cases, author/context qualifiers "
    "and first three seven-year Alfridary lords by day (Sun/Venus/Mercury) "
    "and night (Moon/Saturn/Jupiter). No complete lifetime sequence "
    "assumed. **12,764 Lilly +1,066 Ptolemy=13,830 Western historical "
    "annotations**; parallel Chinese V7 154 BaZi+201 Zi Wei=355 "
    "unchanged. First printed CLXXI is physically covered but not "
    "expert-critically verified or empirically validated. Next "
    "**R12765, CLXXII Of Revolutions**, same printed p734/PDF768 "
    "below physical divider. Zero blinded real-human predictive "
    "validation and zero runtime model promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted source checkpoint preserved verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07as",
    "status": "GUARDED_CLXXI_ORIGINAL_SOURCE_ACCEPTED_LOCAL_REMOTE_PENDING",
    "Lilly_before": 12742,
    "Lilly_after": 12764,
    "Ptolemy_retained": 1066,
    "Western_after": 13830,
    "Chinese_V7_retained": 355,
    "new_historical_source_notes": 22,
    "next_R": "R12765",
    "next_pdf_frame": 768,
    "next_chapter": "CLXXII",
    "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07as.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_record_SHA256": accept["source_records_SHA256"],
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_tests_replayed": 34,
    "Chinese_V7_SHA256": sha(CHINA),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
