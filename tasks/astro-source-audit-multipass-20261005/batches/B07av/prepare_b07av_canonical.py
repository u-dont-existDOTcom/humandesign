#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve original bibliographic source references.
"""Guarded append-only Lilly B07av original CLXXIII source admission.

Real historical phrase documentation is separate from chart-era astronomy,
real human predictive validity, original source editions' printed glyphs
and high-stakes social/moral claims. One reader, two type-set printings.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07av_CLXXIII.md"
BACK = B / "recovery"
PREP = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07av-clxxiii-planetary-returns-20261019"
PARENT_CHECKPOINT = "079d5083601e8e660af024537d4b5e2b548d06d8"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for file in (LATEST, PREP, BACK / "LILLY_INDEX_BEFORE_B07av.json"):
    assert not file.exists(), f"Admission already in progress? Reconcile first: {file}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT_CHECKPOINT
old = j(INDEX)
chinese = j(CHINESE)
matrix = j(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json")
proof = j(B / "SOURCE_RULE_PROVENANCE_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
heading = j(B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json")
photos = j(B / "SOURCE_PHOTO_CHECKPOINT_V1.json")
receipt = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["branch"] == BRANCH and task["root_owner_goal"] == "OPEN"
assert old["records_count"] == accept["prior_Lilly_source_annotations"] == 12803
assert old["batches"][-1]["id"] == "B07au"
assert old["next"]["chapter"] == "CLXXIII"
assert old["next"]["pdf_page"] == 772 and old["next"]["editorial_source_sequence_ordinal"] == 173
assert old["read_numbered_chapters"] == list(range(1, 173))
assert old["read_headed_units_count"] == 88
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == photos["full_1647_first_edition_pdf_sha256"]
assert (
    chinese["sum_source_annotations"] == accept["Chinese_V7_historical_annotations_retained"] == 355
)
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["prior_Ptolemy_source_annotations"] == 1066
assert rules["record_count"] == 43
assert len(matrix["records"]) == 42
assert len(proof["source_rule_locators"]) == 42
assert len(rules["rules"]) == 43
assert [r["record_number"] for r in rules["rules"]] == list(range(12804, 12847))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert rules["last_record"] == "R12846" and accept["next_original_source_R"] == "R12847"
assert heading["original_1647_literal_chapter_heading"] == "CHAP. CLXXIIII."
assert heading["independently_typeset_1659_literal_chapter_heading"] == "CHAP. CLXXIV."
assert heading["editorial_normalized_chapter_numeral"] == "CLXXIV"
assert accept["next_original_printed_chapter"] == "CLXXIIII"
assert accept["next_second_edition_printed_chapter"] == "CLXXIV"
assert accept["next_editorial_normalized_chapter"] == "CLXXIV"
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["source_matrix_sha256"] == sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json")
assert accept["source_provenance_sha256"] == sha(B / "SOURCE_RULE_PROVENANCE_V1.json")
assert accept["original_next_heading_variant_witness_sha256"] == sha(
    B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"
)
assert receipt["CRC_passed"] and receipt["all_member_sha256_and_exact_bytes_passed"]
assert receipt["independent_archive_extracted_test_replays"] == 54
assert receipt["source_matrix_sha256"] == accept["source_matrix_sha256"]
assert receipt["source_provenance_sha256"] == accept["source_provenance_sha256"]
assert receipt["rules_sha256"] == accept["rules_sha256"]
assert receipt["prior_Lilly_history_source_index_sha256"] == sha(INDEX)
assert receipt["Chinese_V7_source_index_sha256"] == sha(CHINESE)
archive = downloads() / receipt["filename"]
assert archive.is_file() and archive.stat().st_size == receipt["archive_bytes"]
assert sha(archive) == receipt["archive_sha256"]
for file in (
    INDEX,
    CHINESE,
    ROOT / T / "batches/B07au/RULES.json",
    ROOT / T / "batches/B07au/SOURCE_EVIDENCE_PREP_ONLY_V1.json",
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07av.json"),
    (CURRENT, "CURRENT_BEFORE_B07av.md"),
    (CHINESE, "CHINESE_V7_BEFORE_B07av.json"),
):
    (BACK / name).write_bytes(file.read_bytes())
old["batches"].append(
    {
        "id": "B07av",
        "path": "batches/B07av/RULES.json",
        "records_count": 43,
        "sha256": accept["rules_sha256"],
        "scope": (
            "First-edition original Lilly CLXXIII printed738–741/PDF772–775 "
            "planetary returns to radix positions, verified against actual "
            "separately typeset original second 1659 printed738–741/DjVu767–770 "
            "source photographs. Exactly six returning planet headings "
            "Saturn/Jupiter/Mars/Venus/Mercury/Moon times seven natal target "
            "planet places, 42 distinct historical conditional statements "
            "plus one distinct next-chapter physical boundary, R12804–R12846. "
            "No Sun returning-planet list exists in this chapter. Explicit "
            "natal/return conditionals preserved. Next first-edition "
            "heading literally CLXXIIII while independently typeset 1659 "
            "literally CLXXIV, both editorial chapter174 'Transit'. "
            "All high stakes, morality, health, crimes, relationships "
            "and fortune claims remain documentary only, not validated "
            "humans or horoscope engine."
        ),
    }
)
old["records_count"] = 12846
old["status"] = "BOOK_III_CLXXIII_PLANETARY_RETURNS_PHYSICAL_CHAPTER_COVERED_NEXT_CLXXIV_TRANSITS"
old["read_numbered_chapters"].append(173)
old["read_headed_units_count"] = 89
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXIII",
        "editorial_ordinal": 173,
        "chapter_heading": "Of the Returne of the Planets to their owne Places, and to the places of other Planets in the Radix",
        "first_edition_original_pdf_from": 772,
        "first_edition_original_pdf_through": 775,
        "first_edition_original_printed_folios": [738, 739, 740, 741],
        "separate_second_typeset_edition_DjVu_folios": [767, 768, 769, 770],
        "historical_source_returning_planet_headings_six": True,
        "seven_natal_planet_targets_per_heading": True,
        "all_historical_source_rule_pairs_documented": 42,
        "physical_source_span_covered": True,
        "full_independent_expert_diplomatic_edition_review": False,
        "original_1647_birth_calendar_and_solar_revolution_engine_validated": False,
        "blind_real_people_predictions_validated": 0,
        "runtime_astrological_rules_promoted": False,
        "accepted_batch": "B07av",
    }
)
old["next"] = {
    "pdf_page": 775,
    "printed_page": 741,
    "chapter": "CLXXIV",
    "printed_chapter_numeral": "CLXXIIII",
    "second_1659_edition_printed_chapter_numeral": "CLXXIV",
    "editorial_source_sequence_ordinal": 174,
    "heading": "Of the TRANSIT of the Planets",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "New physical transit chapter after last CLXXIII Moon-on-Moon "
        "paragraph and horizontal divider on original first-edition "
        "printed741/PDF775, source first chapter-heading roman numeral "
        "literally CLXXIIII, 1659 second type-set chapter printed CLXXIV. "
        "Normalize only editorial sequence as174. Next source R12847. "
        "A single physically same-page heading locator already admitted "
        "in B07av and must not be repeated as a new substantive transit rule."
    ),
    "research_scope": (
        "Original first and separately typeset second editions define "
        "transits by ephemeris, natal house cusps/natal planet or Nodes/"
        "Fortune, benefic and malefic aspects and claimed favorable days; "
        "actual date/time ephemeris parity and out-of-sample human predictions "
        "remain entirely unverified."
    ),
}
old["source_CLXXIII_printed_variation_research_note"] = (
    "The first original printed CLXXIII was traversed in B07av but not "
    "expert-critically collated. At printed741/PDF775 first printing "
    "the next physically distinct chapter is headed CHAP. CLXXIIII. "
    "The 1659 independently typeset printing reads CHAP. CLXXIV. "
    "Both editorially mean 174. Preserve literal original headings, "
    "unknown astrological birthday/solar return mathematics and "
    "zero actually measured human predictions."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07av_CLXXIII.md"
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 174))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly original 1647 CLXXIII return-to-radix source physically covered (B07av)\n\n"
    "**43 historical source-only records R12804–R12846** document "
    "six returning-planet headings Saturn/Jupiter/Mars/Venus/Mercury/Moon "
    "to seven actual natal planets/places, 42 conditional source "
    "claims plus one next physical divider, original 1647 printed738–741 "
    "and separately typeset original 1659 same printed folios. "
    "Old conditionals preserved; none are independently tested actual "
    "people's illness, finances, marriage, birth, morality, law or character. "
    "At the following printed741 divider the first edition literally "
    "prints **CHAP. CLXXIIII.**, separately typeset 1659 **CHAP. CLXXIV.**; "
    "these normalize only for editorial ordinal174, *Of the Transit of "
    "the Planets*. **Lilly 12,846+Ptolemy1,066=13,912 Western historical "
    "annotations**, parallel Chinese V7 **154 BaZi +201 Zi Wei=355** "
    "unchanged. First physical CLXXIII source span covered but not "
    "expert-diplomatically collated or validated birth-era solar return "
    "method. Next **R12847** printed741/PDF775 within distinct transit "
    "chapter. **Zero blinded real-person predictive validations, zero "
    "runtime model promotions.**\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous historical source checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
canon = {
    "batch": "B07av",
    "status": "ORIGINAL_CLXXIII_43_HISTORICAL_SOURCE_RECORDS_GUARDED_PENDING_REMOTE_PUSH",
    "Lilly_before": 12803,
    "Lilly_after": 12846,
    "Ptolemy_retained": 1066,
    "Western_after": 13912,
    "Chinese_V7_retained": 355,
    "original_return_to_radix_documentary_matrix_cases": 42,
    "next_R": "R12847",
    "next_first_edition_original_pdf_frame": 775,
    "next_original_printed_chapter_1647": "CLXXIIII",
    "next_original_printed_chapter_1659": "CLXXIV",
    "normalized_next_editorial_ordinal": 174,
    "prior_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07av.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "Chinese_V7_SHA256": sha(CHINESE),
    "source_matrix_SHA256": accept["source_matrix_sha256"],
    "source_provenance_SHA256": accept["source_provenance_sha256"],
    "source_original_cross_edition_next_heading_SHA256": accept[
        "original_next_heading_variant_witness_sha256"
    ],
    "original_source_archive_SHA256": receipt["archive_sha256"],
    "portable_archive_tests_replayed": 54,
    "real_human_outcome_predictions_validated": 0,
    "runtime_promotions": 0,
}
PREP.write_text(json.dumps(canon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(canon, indent=2))
