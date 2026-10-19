#!/usr/bin/env python3
"""Guarded append-only Lilly first edition transit chapter documentary admission.

The 1647 Mars-Ascendant text explicitly says two/three *days*, while the
independent typeset 1659 says *years*. Neither is an empirically verified
forecast, and source physical chapter coverage is not critical edition
validation, astronomy engine parity, or personal predictive accuracy.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07aw-original-transits-20261019"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads() -> Path:
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


def accept() -> None:
    for path in (
        RECEIPT,
        LATEST,
        BACK / "LILLY_INDEX_BEFORE_B07aw.json",
    ):
        assert not path.exists(), f"Possibly interrupted admission: {path}"
    assert git("branch", "--show-current") == BRANCH

    previous = read(INDEX)
    chinese = read(CHINESE)
    notes = read(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json")
    rules = read(B / "RULES.json")
    candidate = read(B / "ACCEPTANCE.json")
    release = read(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
    scope = read(B / "TASK_SCOPE.json")
    conflict = read(B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json")
    boundary = read(B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json")

    assert scope["active_branch"] == BRANCH
    assert scope["status"] == "OPEN_SOURCE_NOT_YET_ACCEPTED"
    assert previous["records_count"] == 12845
    assert previous["batches"][-1]["id"] == "B07av"
    assert previous["next"]["chapter"] == "CLXXIIII"
    assert previous["next"]["pdf_page"] == 775
    assert previous["next"]["editorial_source_sequence_ordinal"] == 174
    assert previous["read_numbered_chapters"] == list(range(1, 174))
    assert previous["read_headed_units_count"] == 89
    assert previous["partial_numbered_chapters"] == []
    assert sum(v["records_count"] for v in previous["batches"]) == 12845
    assert previous["empirical_validations"] == previous["runtime_promotions"] == 0

    assert chinese["sum_source_annotations"] == 355
    assert chinese["runtime_promotions"] == 0
    assert chinese["independently_validated_real_human_claims"] == 0
    assert previous["source_sha256"] == boundary["original_full_Wellcome_1647_pdf_sha256"]
    assert previous["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"

    assert rules["record_count"] == notes["new_source_documentary_rule_count"] == 25
    assert len(rules["rules"]) == len(notes["records"]) == 25
    assert [r["record_number"] for r in rules["rules"]] == list(range(12846, 12871))
    assert all(not r["runtime_model_promoted"] for r in rules["rules"])
    assert candidate["Lilly_before"] == 12845
    assert candidate["Ptolemy_retained"] == 1066
    assert candidate["Chinese_V7_retained"] == 355
    assert candidate["Lilly_after_if_admitted"] == 12870
    assert candidate["Western_after_if_admitted"] == 13936
    assert candidate["next_record"] == "R12871"
    assert candidate["next_original_pdf_frame"] == 776
    assert candidate["next_source_chapter"] == "CLXXV"
    assert candidate["next_editorial_chapter_ordinal"] == 175
    assert candidate["rules_SHA256"] == sha(B / "RULES.json")
    assert candidate["source_full_document_SHA256"] == sha(
        B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"
    )
    assert conflict["first_edition_quote_exact_span"] == "for two or three dayes"
    assert conflict["second_edition_quote_exact_span"] == "for two or three years"
    assert boundary["first_edition_original_chapter_numeral"] == "CLXXV"

    assert release["CRC_passed"] and release["all_members_SHA256_and_bytes_passed"]
    assert release["independent_archive_test_replay_passed"]
    assert release["focused_source_tests_replayed"] == 42
    assert release["document_SHA256"] == candidate["source_full_document_SHA256"]
    assert release["rules_SHA256"] == candidate["rules_SHA256"]
    assert release["before_Lilly_index_SHA256"] == sha(INDEX)
    assert release["before_Chinese_index_SHA256"] == sha(CHINESE)
    assert sha(downloads() / release["filename"]) == release["archive_sha256"]

    for file in (
        INDEX,
        CHINESE,
        ROOT / TASK / "batches/B07av/RULES.json",
        ROOT / TASK / "batches/B07av/evidence/1647_original-775.jpg",
        ROOT / TASK / "batches/B07av/evidence/1659_original_djvu_770.jpg",
        B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json",
        B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json",
    ):
        relative = str(file.relative_to(ROOT))
        assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

    BACK.mkdir(exist_ok=False)
    for file, name in (
        (INDEX, "LILLY_INDEX_BEFORE_B07aw.json"),
        (CURRENT, "CURRENT_BEFORE_B07aw.md"),
        (CHINESE, "CHINESE_V7_BEFORE_B07aw.json"),
    ):
        (BACK / name).write_bytes(file.read_bytes())

    previous["batches"].append(
        {
            "id": "B07aw",
            "path": "batches/B07aw/RULES.json",
            "records_count": 25,
            "sha256": candidate["rules_SHA256"],
            "scope": (
                "First edition 1647 Lilly original CLXXIIII transit chapter "
                "printed741/PDF775, independently typeset 1659 chapter "
                "CLXXIV same printed folio/DjVu770. 25 historically documented "
                "source conditions R12846-R12870: ephemeris, natal house "
                "cusps, natal planets/nodes/Fortuna, aspect kinds, benefic "
                "Jupiter/Venus vs Mars/Saturn traditional natal transit "
                "event claims, with exact material Mars Ascendant duration "
                "conflict 1647 two or three DAYS vs 1659 two or three YEARS. "
                "Physical next original printed742/PDF776 begins new "
                "chapter CLXXV Merchant Nativity, preserved separately. "
                "Both original documents one reader, not expert critical "
                "editions; historical astro ephemeris/human predictive tests "
                "not verified, no runtime rule promotions."
            ),
        }
    )
    previous["records_count"] = 12870
    previous["status"] = "BOOK_III_ORIGINAL_CLXXIIII_TRANSITS_ONE_PAGE_PHYSICAL_SOURCE_COVERED"
    previous["read_numbered_chapters"].append(174)
    previous["read_headed_units_count"] = 90
    previous["chapter_CLXXIIII_1647_vs_CLXXIV_1659_transit_source_note"] = (
        "B07aw 25 source-only documentary observations R12846-R12870 "
        "cover original printed741/PDF775. Independently typeset "
        "1647 CLXXIIII versus 1659 CLXXIV. 1647 source text prints "
        "'for two or three dayes' for Mars Ascendant, 1659 source text "
        "prints 'for two or three years'; never merge timing windows "
        "without additional editorial original source evidence. "
        "No validated individual anger/melancholy/finance predictions, "
        "no modern ephemeris/natal house engine, no real people tests. "
        "Next Merchant Nativity physically distinct CLXXV source."
    )
    previous["next"] = {
        "pdf_page": 776,
        "printed_page": 742,
        "chapter": "CLXXV",
        "printed_chapter_numeral": "CLXXV",
        "second_edition_1659_printed_chapter_numeral": "CLXXV",
        "editorial_source_sequence_ordinal": 175,
        "heading": "The NATIVITY of an English Merchant Astrologically handled.",
        "include_opening_paragraph": True,
        "extracted": False,
        "boundary_image_read": True,
        "position": (
            "Original first 1647 printed742/PDF776 begins separate "
            "CLXXV Merchant Nativity with a printed source birth chart "
            "and right/oblique ascension and latitude notes. "
            "The transit chapter CLXXIIII was physically complete "
            "on preceding printed741; second edition prints CLXXIV. "
            "Continue historical source R12871 without inventing "
            "genuine merchant birth outcome validation."
        ),
        "research_scope": (
            "Original natal chart, actual historic date and latitude, "
            "era ephemeris and physical house geometry; preserve "
            "one-reader figure uncertainty and independent 1659 edition "
            "comparison. Human events and true birth chart engine unverified."
        ),
    }
    previous["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md"

    assert previous["read_numbered_chapters"] == list(range(1, 175))
    assert previous["read_headed_units_count"] == 90
    assert previous["partial_numbered_chapters"] == []
    assert previous["records_count"] == sum(b["records_count"] for b in previous["batches"])
    assert previous["empirical_validations"] == previous["runtime_promotions"] == 0
    INDEX.write_text(
        json.dumps(previous, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = (
        "# Lilly original printed transit chapter accepted as historical "
        "source-only B07aw\n\n"
        "**25 original historical annotations R12846-R12870** from "
        "first 1647 printed741/PDF775 chapter CLXXIIII and independently "
        "typeset 1659 CLXXIV, with two further original next-page "
        "edition photos proving Merchant Nativity CLXXV starts at "
        "PDF776/printed742. **1647 Mars Ascendant says two or three "
        "dayes, 1659 says two or three years**: real edition conflict "
        "preserved, no timing window chosen as validated. "
        "**Lilly historical 12,870 plus Ptolemy 1,066 = Western 13,936**. "
        "Separate Chinese V7 **154 BaZi+201 Zi Wei=355** untouched. "
        "The one-page original transit chapter is physically covered, "
        "not independently critically collated or predictive validated. "
        "Next **R12871** original PDF776/printed742, separate "
        "CLXXV English Merchant Nativity. Historical genuine-person "
        "prediction validations zero; runtime astrological promotions zero.\n\n"
    )
    CURRENT.write_text(
        summary
        + "## Previous accepted historical checkpoint retained\n\n"
        + CURRENT.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    LATEST.write_text(
        summary + (B / "ORIGINAL_TRANSITS_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    receipt = {
        "batch": "B07aw",
        "status": "SOURCE_ONLY_TRANSITS_CHAPTER_PREPARED_REMOTE_PUBLICATION_PENDING",
        "Lilly_before": 12845,
        "Lilly_after": 12870,
        "Ptolemy_retained": 1066,
        "Western_historical_after": 13936,
        "Chinese_V7_retained": 355,
        "new_transit_documentary_source_notes": 25,
        "original_1647_chapter_numeral": "CLXXIIII",
        "original_1659_chapter_numeral": "CLXXIV",
        "source_mars_duration_days_vs_years": True,
        "next_source_R": "R12871",
        "next_source_pdf": 776,
        "next_original_printed_chapter": "CLXXV",
        "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07aw.json"),
        "new_Lilly_index_SHA256": sha(INDEX),
        "source_document_SHA256": candidate["source_full_document_SHA256"],
        "rules_SHA256": candidate["rules_SHA256"],
        "release_archive_SHA256": release["archive_sha256"],
        "portable_source_tests_replayed": 42,
        "Chinese_V7_SHA256": sha(CHINESE),
        "independent_human_predictions_validated": 0,
        "runtime_promotions": 0,
    }
    RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    accept()
