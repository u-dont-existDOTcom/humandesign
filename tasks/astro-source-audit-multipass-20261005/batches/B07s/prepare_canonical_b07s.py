#!/usr/bin/env python3
"""Guarded one-time canonical source index admission of printed Lilly CLXII (1647)."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX_PATH = (
    ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07s_SUN_DIRECTIONS.md"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"
BACK = B / "recovery"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for target in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07s.json"):
    assert not target.exists(), f"Possibly already accepted/interrupted: {target}"

source = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
idx = j(INDEX_PATH)
rules = j(B / "RULES.json")
accepted = j(B / "ACCEPTANCE.json")
author = j(B / "SOURCE_FIRST_AUTHORING_20261018.json")
mapped = j(B / "SOURCE_TO_RECORD_MAP.json")
witness = j(B / "ORIGINAL_SOURCE_WITNESS.json")
guard = j(B / "SUN_DIRECTION_HISTORICAL_NONPROMOTION_GUARD_V1.json")
archive = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
china = j(CHINA)
assert git("branch", "--show-current") == "research/astro-b07s-sun-directions-20261018"
assert sha(INDEX_PATH) == source["prior_index_sha256"]
assert sha(INDEX_PATH) == archive["prior_canonical_index_sha256"]
assert idx["records_count"] == accepted["prior_lilly"] == 11415
assert idx["read_numbered_chapters"] == list(range(1, 161))
assert idx["batches"][-1]["id"] == "B07r"
assert idx["next"]["chapter"] == idx["next"]["printed_chapter_numeral"] == "CLXII"
assert idx["next"]["pdf_page"] == 713
assert idx["source_sha256"] == source["original_pdf_sha256"]
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B07s" for x in idx["batches"])
assert accepted["new_historical_annotations"] == rules["record_count"] == 306
assert (rules["substantive"], rules["following_navigation"]) == (304, 2)
assert (accepted["substantive"], accepted["following_navigation"]) == (304, 2)
assert [r["record_number"] for r in rules["rules"]] == list(range(11416, 11722))
assert [r["role"] for r in rules["rules"][-2:]] == ["next_clxiii", "next_rigel"]
assert (len(author["groups"]), len(mapped["source_groups"])) == (40, 40)
assert sha(B / "RULES.json") == accepted["rules_sha256"] == archive["rules_sha256"]
assert witness["body_original_pdf_frames"] == list(range(713, 724))
assert witness["following_printed_clxiii_heading_frame"] == 723
assert len(witness["photos"]) == 13
for photo in witness["photos"].values():
    file = B / photo["file"]
    assert file.stat().st_size == photo["bytes"] and sha(file) == photo["sha256"]
assert guard["original_sun_venus_opposition_doubted_by_lilly"]
assert guard["original_sun_mercury_opposition_doubted_by_lilly"]
assert not guard["natal_forecasting_at_the_person_level_authorized"]
assert not guard["runtime_rules_promoted"]
assert guard["independent_human_outcomes_validated"] == 0
assert archive["crc_passed"] and archive["member_hashes_verified"]
assert archive["independent_extract_replay"]
assert archive["replayed_documentary_tests"] == 81
assert archive["replayed_source_window_tests"] == 24
assert archive["portable_test_replay"] == 105
assert sha(archive["archive_path"]) == archive["archive_sha256"]
assert china["sum_source_annotations"] == 97
assert china["independently_validated_real_human_claims"] == 0
assert china["runtime_promotions"] == 0
for protected in (
    INDEX_PATH,
    CHINA,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07r/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    rel = str(protected.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(protected)), rel
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"])
BACK.mkdir(exist_ok=False)
for sourcefile, out in (
    (INDEX_PATH, "INDEX_BEFORE_B07s.json"),
    (CURRENT, "CURRENT_BEFORE_B07s.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07s.md"),
    (CHINA, "CHINESE_V2_BEFORE_B07s.json"),
):
    (BACK / out).write_bytes(sourcefile.read_bytes())

idx["batches"].append(
    {
        "id": "B07s",
        "path": "batches/B07s/RULES.json",
        "records_count": 306,
        "sha256": accepted["rules_sha256"],
        "scope": (
            "Original 1647 Lilly Christian Astrology printed CHAP CLXII, "
            "Sunne directed to Promittors PDF713 lower/printed679 through "
            "PDF723 upper/printed689, distinct CHAP CLXIII Sun directed "
            "to Fixed Starres begins after divider SAME PDF723. "
            "306 historical-only source annotations R11416–R11721, "
            "304 substantive and 2 CLXIII navigation; 40 reversible "
            "photo-anchored source groups, original PDF713-725 SHA/bytes "
            "and PDF restoration from exact original immutable full scan. "
            "Sun to Saturn Jupiter Mars Venus Mercury Moon body and aspects "
            "and period terms, lunar North/South Nodes, Part Fortune, "
            "all 12 house cusps. Lilly's original objection to feasible "
            "Sun-Venus and Sun-Mercury opposition preserved without "
            "date engine, along with radix, hyleg, anareta, profection, "
            "revolution, age, rank, office and planetary mitigating "
            "conditions. Medical, mortality, violence, criminality, "
            "religion, class and relationship stereotyping source ONLY. "
            "105 source/window focused tests independently extracted "
            "ZIP replayed with CRC+SHA/member byte equality. "
            "ZERO human validation, ZERO runtime promotions; Chinese "
            "V2 97 source notes untouched."
        ),
    }
)
idx["records_count"] = 11721
idx["read_numbered_chapters"].append(161)
idx["status"] = "BOOK_III_CLXII_SUN_PROMITTORS_NEXT_CLXIII_FIXED_STARS"
idx["next"] = {
    "pdf_page": 723,
    "printed_page": 689,
    "chapter": "CLXIII",
    "printed_chapter_numeral": "CLXIII",
    "heading": "The Sunne Directed to Fixed Starres",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original first-edition CHAP CLXIII starts after divider mid "
        "PDF723/printed689; source includes original PDF724 and "
        "ends above next divider PDF725/printed691, where printed "
        "CHAP CLXIIII Directions of the Moon to Promittors begins. "
        "Original source photos PDF723–725 are preserved in B07s. "
        "Next historic source annotation R11722."
    ),
    "research_scope": (
        "Source collation Sun directions to fixed stars, original "
        "first-edition star coordinates and conditional cases. "
        "Modern ephemeris and human predictive parity unverified."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CLXII_original_sun_directions_source_acceptance_note"] = (
    "B07s original first-edition source-only 306 clauses "
    "R11416-R11721, 40 reversible groups with PDF713-723, "
    "13 original/correctly sourced photographic images 713-725; "
    "105 archive replay tests. Sun-Venus and Sun-Mercury opposition "
    "feasibility caveats recorded. Solar direction time engine, "
    "human clinical/danger/financial or personality validity "
    "unverified. 97 Chinese historical notes separate."
)
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"]) == 11721
assert idx["read_numbered_chapters"] == list(range(1, 162))
INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Latest original 1647 Lilly source checkpoint: printed CLXII Sun directions\n\n"
    "**306 historical-only source annotations R11416–R11721** "
    "across 40 reversible photo-anchored first-edition passage groups; "
    "11-body-frame printed 679–689 Sun-to-Promittors source and 2 "
    "overlapping next-chapter photograph frames. **11,721 Lilly "
    "+1,066 Ptolemy=12,787 Western historical source records**, "
    "independent **46 BaZi+51 Zi Wei=97 Chinese source notes**. "
    "Next distinct printed **CHAP CLXIII Sunne to FIXED STARRES** "
    "starts lower **PDF723/printed689, R11722**; its following "
    "CHAP CLXIIII Moon Promittors starts lower PDF725/printed691. "
    "**105 verified independently ZIP-extracted documentary/photo "
    "tests**, zero empirical real-human prediction validations and "
    "zero executable runtime promotions. Historical mortality, "
    "medical, crime, sexual/moral, legal and economic assertions "
    "are NOT valid real-person forecasts.\n\n"
)
for file in (CURRENT, PROGRESS):
    original = file.read_text(encoding="utf-8")
    file.write_text(
        summary + "## Earlier retained research state\n\n" + original,
        encoding="utf-8",
    )
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07s",
    "status": "CANONICAL_PREPARED_NOT_REMOTE_PUBLISHED",
    "previous_lilly": 11415,
    "now_lilly": 11721,
    "historical_source_annotations_added": 306,
    "ptolemy_still": 1066,
    "western_source_total": 12787,
    "chinese_v2_source_notes_unchanged": 97,
    "prior_index_sha256": source["prior_index_sha256"],
    "accepted_index_sha256": sha(INDEX_PATH),
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "portable_tests_replayed": 105,
    "following": "CLXIII PDF723 R11722",
    "individual_human_predictive_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
