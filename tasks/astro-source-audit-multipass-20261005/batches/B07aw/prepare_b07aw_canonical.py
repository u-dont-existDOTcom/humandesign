#!/usr/bin/env python3
"""Guarded appendix: 22 original first-1647/second-1659 transits source notes.

This is documentary source coverage only. Preserve Roman numeral variants,
Venus vs derivative Mars, days vs years, uncertain outcomes, and older index.
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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07aw-original-transit-planet-glyphs-20261019"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    run = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    path = Path(run.stdout.strip()) if run.returncode == 0 and run.stdout.strip() else None
    if path is not None and path.is_dir() and path.resolve() != Path.home().resolve():
        return path
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for path in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07aw.json"):
    assert not path.exists(), f"Existing/interrupted source-index admission; reconcile {path}"
assert git("branch", "--show-current") == BRANCH
before = j(INDEX)
china = j(CHINA)
source = j(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
rules = j(B / "RULES.json")
accepted = j(B / "ACCEPTANCE.json")
archive = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
checkpoint = j(B / "RECOVERY_CHECKPOINT.json")
assert checkpoint["branch"] == BRANCH
assert checkpoint["parent_outcome"] == "OPEN"
assert before["records_count"] == accepted["Lilly_before"] == 12846
assert sum(b["records_count"] for b in before["batches"]) == 12846
assert before["batches"][-1]["id"] == "B07av"
assert before["next"]["editorial_source_sequence_ordinal"] == 174
assert before["next"]["printed_chapter_numeral"] == "CLXXIIII"
assert before["next"]["pdf_page"] == 775
assert before["read_numbered_chapters"] == list(range(1, 174))
assert before["read_headed_units_count"] == 89
assert before["partial_numbered_chapters"] == []
assert before["empirical_validations"] == before["runtime_promotions"] == 0
assert before["source_sha256"] == source["source_original_1647_full_book_pdf_sha256"]
assert before["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert china["sum_source_annotations"] == accepted["Chinese_V7_retained"] == 355
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert source["source_historical_record_count"] == len(source["records"]) == 22
assert len(rules["rules"]) == 22 and rules["record_count"] == 22
assert [r["record_number"] for r in rules["rules"]] == list(range(12847, 12869))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert source["original_1647_1659_ascendant_planets"] == ["Jupiter", "Venus"]
assert source["1647_printed_Mars_ascendant_duration"] == "2 or 3 days"
assert source["1659_printed_Mars_ascendant_duration"] == "2 or 3 years"
assert source["original_1647_next_distinct_CLXXV_pdf_frame"] == 776
assert not source["source_critical_professional_collation_complete"]
assert accepted["Lilly_after_if_accepted"] == 12868
assert accepted["Western_after_if_accepted"] == 13934
assert accepted["next_original_R"] == "R12869"
assert accepted["next_original_PDF"] == 776
assert accepted["source_SHA256"] == sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
assert accepted["rules_SHA256"] == sha(B / "RULES.json")
assert archive["crc_passed"] and archive["member_hashes_and_bytes_passed"]
assert archive["independent_ZIP_test_replay_passed"] == 40
assert archive["source_SHA256"] == accepted["source_SHA256"]
assert archive["rules_SHA256"] == accepted["rules_SHA256"]
assert archive["prior_Lilly_index_SHA256"] == sha(INDEX)
assert archive["Chinese_V7_index_SHA256"] == sha(CHINA)
assert sha(downloads() / archive["filename"]) == archive["archive_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / T / "batches/B07av/RULES.json",
    ROOT / T / "batches/B07av/SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json",
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07aw.json"),
    (CHINA, "CHINESE_V7_BEFORE_B07aw.json"),
    (CURRENT, "CURRENT_BEFORE_B07aw.md"),
):
    (BACK / name).write_bytes(file.read_bytes())

before["batches"].append(
    {
        "id": "B07aw",
        "path": "batches/B07aw/RULES.json",
        "records_count": 22,
        "sha256": accepted["rules_SHA256"],
        "scope": (
            "Original William Lilly Christian Astrology first 1647 printed741 "
            "original PDF775 transit chapter, independently printed 1659 "
            "folio741/DjVu770. Physical CLXXIIII first-edition numeral "
            "versus CLXXIV second-edition spelling is preserved. "
            "Twenty-two source-only annotations R12847–R12868 cover "
            "ephemeris method, natal cusps/natal planets/nodes/Fortune, "
            "sextile/trine/square/opposition, Ascendant/second/third-house "
            "historic favorable/unfavorable day claims. The original "
            "first+second editions name Jupiter/Venus at Ascendant, "
            "contrary to searchable derivative Jupiter/Mars. For Mars "
            "crossing Ascendant first 1647 prints two/three dayes "
            "but second 1659 two/three yeares. Neither source is "
            "a verified independent human forecast or accurate natal "
            "astronomical time engine. First CLXXIIII transit physical text "
            "ends before next CLXXV English merchant chart on PDF776."
        ),
    }
)
before["records_count"] = 12868
before["status"] = (
    "ORIGINAL_1647_CLXXIIII_TRANSIT_ONE_PAGE_PHYSICAL_SOURCE_COVERED_NEXT_CLXXV_MERCHANT"
)
before["read_numbered_chapters"] = before["read_numbered_chapters"] + [174]
before["read_headed_units_count"] = 90
before.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "original_first_1647_chapter_numeral": "CLXXIIII",
        "second_1659_chapter_numeral": "CLXXIV",
        "editorial_source_ordinal": 174,
        "original_first_edition_pdf_frame": 775,
        "original_first_edition_printed_folio": 741,
        "source_current_batch": "B07aw",
        "source_physically_complete": True,
        "critical_two_reader_source_collation_complete": False,
        "Mars_duration_day_vs_year_edition_variation": True,
        "original_Ascendant_benefics_Jupiter_Venus": True,
        "source_ephemeris_validation_complete": False,
        "independent_actual_human_predictive_successes": 0,
    }
)
before["next"] = {
    "pdf_page": 776,
    "printed_page": 742,
    "chapter": "CLXXV",
    "printed_chapter_numeral": "CLXXV",
    "editorial_source_sequence_ordinal": 175,
    "heading": "The NATIVITY of an English Merchant Astrologically handled",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original first 1647 p742/PDF776 contains nativity chart of "
        "English Merchant born 19 Sept 1616, old-style Gregorian/Julian "
        "date interpretation unverified. Preserve exact original chart "
        "planet degrees, latitude, oblique/right ascension and antiscions "
        "with independently printed 1659 edition; do not infer human "
        "event accuracy or retune scoring. Next R12869."
    ),
    "research_scope": (
        "Historical original 1647 Merchant chart and matched 1659 "
        "printing; detailed natal astronomical source as text before "
        "independent ephemeris epoch/calendrical parity or actual "
        "human forward blind tests."
    ),
}
before["chapter_CLXXIIII_CLXXIV_transits_two_edition_photo_note"] = (
    "B07aw one-page original photo source physically closed CLXXIIII "
    "editorial174; independent 1659 prints CLXXIV. 1647 first edition "
    "writes Mars Ascendant two/three dayes, 1659 second writes "
    "two/three yeares. Both original editions say Jupiter or Venus "
    "on Ascendant, derivative Jupiter or Mars is an error. Historical "
    "book's mood/wealth/health prognoses are neither actual human "
    "evidence nor a validated original natal transit ephemeris."
)
before["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md"
assert before["records_count"] == sum(x["records_count"] for x in before["batches"])
assert before["read_numbered_chapters"] == list(range(1, 175))
assert before["partial_numbered_chapters"] == []
assert before["empirical_validations"] == before["runtime_promotions"] == 0
INDEX.write_text(json.dumps(before, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly transit chapter CLXXIIII/CLXXIV covered (B07aw)\n\n"
    "**22 new historical-source-only records R12847–R12868** span "
    "a single original 1647 printed p741/PDF775 transit chapter, "
    "independently printed second 1659 source p741/DjVu770. First "
    "printing labels it **CLXXIIII**, second prints **CLXXIV**. "
    "Both original editions name **Jupiter or Venus** for Ascendant "
    "benefic transits, not the searchable derivative's Jupiter/Mars. "
    "1647 source Mars Ascendant emotional duration reads **2–3 days**, "
    "1659 original prints **2–3 years**. The duration divergence "
    "cannot prove either effect; source health/wealth/mood outcomes "
    "are old historical claims, not verified events. Source physical "
    "transit chapter is now covered, but not independently critically "
    "expert-collated or proven as accurate ephemeris. "
    "**12,868 Lilly +1,066 Ptolemy=13,934 Western historical notes**, "
    "Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. Next "
    "**R12869** is original p742/PDF776 Chapter **CLXXV** English "
    "Merchant natal chart, with 1659 comparison. Zero genuine human "
    "predictions validated; zero runtime promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted historical checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)

receipt = {
    "batch": "B07aw",
    "status": "ORIGINAL_1647_1659_TRANSITS_22_SOURCE_RECORDS_GUARDED_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12846,
    "Lilly_after": 12868,
    "Ptolemy_retained": 1066,
    "Western_after": 13934,
    "Chinese_V7_retained": 355,
    "added_historical_source_notes": 22,
    "source_one_page_physical_complete": True,
    "independent_critical_edition_completed": False,
    "Mars_duration_original_printings": ["dayes", "yeares"],
    "Ascendant_favorable_planets_original_printings": ["Jupiter", "Venus"],
    "next_R": "R12869",
    "next_PDF": 776,
    "old_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07aw.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_SHA256": accepted["source_SHA256"],
    "rules_SHA256": accepted["rules_SHA256"],
    "archive_SHA256": archive["archive_sha256"],
    "portable_test_replays": 40,
    "Chinese_V7_SHA256": sha(CHINA),
    "empirical_human_outcome_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
