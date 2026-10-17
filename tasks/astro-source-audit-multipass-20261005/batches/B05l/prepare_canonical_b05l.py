#!/usr/bin/env python3
"""Guarded append-only admission of first-edition general fortune as source history."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05l_GENERAL_FORTUNE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for file in (BACK / "INDEX_BEFORE_B05l.json", LATEST, RECEIPT):
    assert not file.exists(), f"Existing or partially prepared source index: {file}"

i = j(IDX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")

assert i["records_count"] == a["prior_lilly"] == 6764
assert i["read_numbered_chapters"] == list(range(1, 114))
assert i["batches"][-1]["id"] == "B05k"
assert i["next"]["chapter"] == "CXIV"
assert i["next"]["pdf_page"] == 585
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(batch["id"] == "B05l" for batch in i["batches"])
assert r["record_count"] == a["historical_records_added"] == 44
assert a["lilly_if_published"] == 6808
assert a["combined_historical_if_published"] == 7874
assert [x["record_number"] for x in r["rules"]] == list(range(6765, 6809))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 3
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert h(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["per_member_sha256_passed"] and z["full_extraction_passed"]
assert z["extracted_tests_passed"] == 18 and h(z["archive_path"]) == z["archive_sha256"]
rel = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05l.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05l.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05l.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B05l",
        "path": "batches/B05l/RULES.json",
        "records_count": 44,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly Christian Astrology 1647 printed CHAP "
            "CXIII/editorial CXIV General Fortune or Misery of the Native. "
            "PDF585-586 original text with following unnumbered second-house "
            "wealth section mid-PDF586 and next printed CHAP CXIIII on PDF587. "
            "41 substantive historical source clauses and 3 navigation items "
            "in 10 source groups: 3-4 dignified planets or mutual reception "
            "for favorable general fortune; planetary debilities for claimed "
            "misfortune; luminary corroboration, variable life states, "
            "explicit promising-chart-but-delayed-outcomes exception, "
            "directions of five Hylegical places and promittors for timing, "
            "adverse lights/benefic/malefic configurations and house-cause "
            "labels. Historic period source only; no independently verified "
            "life-event dates, predictive success or scoring promotion."
        ),
    }
)
i["records_count"] = 6808
i["read_numbered_chapters"].append(114)
i["status"] = "BOOK_III_GENERAL_FORTUNE_HISTORICAL_COMPLETE_NEXT_UNNUMBERED_SECOND_HOUSE"
i["next"] = {
    "pdf_page": 586,
    "printed_page_as_seen": 552,
    "chapter": "UNNUMBERED_SECOND_HOUSE_RICHES",
    "printed_chapter_numeral": None,
    "heading": "The second House of RICHES, or the Goods of FORTUNE",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Source starts below decorated separator in middle of original "
        "PDF586/folio552; runs into PDF587/folio553. Subsequent printed "
        "CHAP CXIIII 'Whether the Native shall be Rich' begins lower "
        "PDF587. Do not skip this unnumbered substantive source unit."
    ),
    "following_printed_chapter_numeral": "CXIIII",
    "following_editorial_chapter": "CXV",
    "following_printed_chapter_pdf_page": 587,
    "research_scope": (
        "Unnumbered second-house estate and wealth significators, "
        "source references to Ptolemy and Leovitius/Origanus, "
        "inheritance vs earning channels, and historical timing; "
        "no proven financial predictions or runtime promotion."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXIV_source_acceptance_note"] = (
    "R6765–R6808 historical-only, 41 source clauses and 3 "
    "next-section navigation, 10 first-edition source groups, "
    "4 original frames and ZIP 18 replayed source tests. "
    "No independent life-event prediction or human outcome validation."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 6808
assert i["read_numbered_chapters"] == list(range(1, 115))
IDX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original 1647 general fortune — historical source accepted\n\n"
    + review
    + "\n## Scientific and runtime separation\n\n"
    + "After authenticated publication **6,808 Lilly + 1,066 Ptolemy "
    + "= 7,874 historical/documentary annotations**. The original "
    + "source images, first-edition pagination and ZIP-source hashes "
    + "are verified. These are historical clauses and countercases, "
    + "not 7,874 independent life events or validated forecasts. "
    + "No independently verified Hylegical timing accuracy or "
    + "personal/financial/moral outcome. Zero source-lane "
    + "runtime promotions.\n"
)
PROGRESS.write_text(
    "# Original-source Lilly 1647 General Fortune complete — 2026-10-17\n\n"
    "After publication **7,874 documentary annotations** "
    "(6,808 Lilly + 1,066 retained Ptolemy), source-body frontier "
    "PDF586/894 (~65.5% physical page position only). Printed "
    "CHAP CXIII general fortune covered with 44 source-only clauses "
    "and explicit delayed-positive-natal condition. Next unnumbered "
    "second-house wealth section begins mid-original PDF586, "
    "prior to printed CHAP CXIIII on PDF587; no unnumbered material "
    "has been silently skipped. Actual event-timing predictive "
    "accuracy, numerical tables, human controls and runtime rules "
    "remain incomplete/untested.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B05l.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly General Fortune historical source accepted; wealth next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Local acceptance R6765–R6808: "
    "41 first-edition historical clauses plus 3 following-section "
    "navigation. Authenticated publication target: 6,808 Lilly "
    "+ 1,066 Ptolemy = 7,874 historic annotations. Broad claimed "
    "positive/negative natal life categories, delayed outcomes and "
    "directions of 5 Hylegical places preserved as hypotheses, "
    "not tested forecasts. No empirical validations/runtime promotions. "
    "NEXT PDF586 unnumbered second House of Riches.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05l.md").read_text()
)
receipt = {
    "batch": "B05l",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "old_index_git_blob": old_blob,
    "old_index_sha256": h(BACK / "INDEX_BEFORE_B05l.json"),
    "new_index_sha256": h(IDX),
    "latest_sha256": h(LATEST),
    "progress_sha256": h(PROGRESS),
    "current_sha256": h(CURRENT),
    "rules_sha256": h(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6808,
    "ptolemy_retained": 1066,
    "combined_if_published": 7874,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
