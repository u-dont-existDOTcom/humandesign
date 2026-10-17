#!/usr/bin/env python3
"""Guarded append-only original unnumbered fourth-house historical source acceptance."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05w_FATHER_PATRIMONY.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(file):
    return json.loads(Path(file).read_text())


def h(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05w.json"):
    assert not p.exists(), f"Prior/partial source admission detected: {p}"
index = j(IDX)
accept = j(B / "ACCEPTANCE.json")
rules = j(B / "RULES.json")
zipreceipt = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == accept["previous_lilly"] == 7295
assert index["read_numbered_chapters"] == list(range(1, 123))
assert index["batches"][-1]["id"] == "B05v"
assert index["next"]["chapter"] == "UNNUMBERED_FOURTH_HOUSE_PARENTS"
assert index["next"]["pdf_page"] == 603
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B05w" for x in index["batches"])
assert rules["record_count"] == accept["new_records"] == 62
assert accept["lilly_if_published"] == 7357
assert accept["combined_if_published"] == 8423
assert [x["record_number"] for x in rules["rules"]] == list(range(7296, 7358))
assert sum(x["role"] == "next_chapter_navigation" for x in rules["rules"]) == 2
assert rules["empirical_validations"] == accept["empirical_validations"] == 0
assert rules["runtime_promotions"] == accept["runtime_promotions"] == 0
assert accept["numbered_chapters_added"] == 0
assert all(
    not (
        x["independent_human_parent_status_validated"]
        or x["human_lifespan_or_death_cause_validated"]
        or x["human_socioeconomic_ancestry_validated"]
        or x["runtime_model_promoted"]
    )
    for x in rules["rules"]
)
assert h(B / "RULES.json") == accept["rules_sha256"] == zipreceipt["accepted_rules_sha256"]
assert zipreceipt["crc_passed"] and zipreceipt["sha256_passed"]
assert zipreceipt["extraction_passed"] and zipreceipt["replayed_tests"] == 17
assert h(zipreceipt["archive_path"]) == zipreceipt["archive_sha256"]
relative = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05w.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05w.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05w.md").write_bytes(PROGRESS.read_bytes())
index["batches"].append(
    {
        "id": "B05w",
        "path": "batches/B05w/RULES.json",
        "records_count": 62,
        "sha256": accept["rules_sha256"],
        "scope": (
            "William Lilly 1647 original unnumbered fourth-house "
            "Parents/Patrimony of the Father introduction, PDF603–604 "
            "before printed CXXII 'Of the Mother' starting mid PDF604. "
            "12 original source groups, 60 substantive source clauses "
            "and 2 next-chapter navigation, including four paternal "
            "significator categories, day Sun/night Saturn, all/majority "
            "fortunate and afflicted/mixed assessments, father's own "
            "nativity preferred, strongest occupied planet priority, "
            "reception/trine/sextile and relative father/mother status, "
            "ambiguous mortality/planetary glyphs, opposite/contrary "
            "testimonies. Period social, ancestry and mortality language "
            "historical only: no actual parent life-event validation "
            "and no runtime scoring rule promoted."
        ),
    }
)
index["records_count"] = 7357
assert index["read_numbered_chapters"] == list(range(1, 123))
index["status"] = "BOOK_III_UNNUMBERED_FOURTH_HOUSE_FATHER_SOURCE_NEXT_MOTHER"
index["next"] = {
    "pdf_page": 604,
    "printed_page": 570,
    "chapter": "CXXIII",
    "printed_chapter_numeral": "CXXII",
    "heading": "Of the Mother",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXII Of the Mother starts after a horizontal "
        "divider around lower mid original PDF604/printed570. "
        "Mother's tenth house and ruler, Venus by day/Moon by "
        "night, occupying planets and complementary health/status "
        "conditions continue original PDF605/printed571. "
        "Next printed chapter/source seam must be located."
    ),
    "research_scope": (
        "Original 1647 mother significators, fortunes and "
        "harm/mortality claims, day/night alternatives, "
        "planetary strength and house configurations; "
        "retain nonvalidated high-stakes health statements "
        "strictly as historical text."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["unnumbered_fourth_house_acceptance_note"] = (
    "B05w R7296–R7357, 62 source-only annotations with 60 father/"
    "parent clauses and 2 mother-chapter navigation. 12 original "
    "groups, original frames603–605 sha, 17 archived tests. "
    "No independent actual parent survival or socioeconomic "
    "prediction validation, no runtime promotions."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7357
IDX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first-edition fourth-house father/patrimony historical source accepted\n\n"
    + review
    + "\n## Documentary acceptance, not empirical validation\n\n"
    + "**7,357 Lilly + 1,066 retained Ptolemy = 8,423 "
    + "historical annotations** after remote verification. "
    + "No father's lifespan, occupation, ancestry, class "
    + "or medical claims independently validated. "
    + "17 portable archived source tests replayed, "
    + "zero runtime rules promoted.\n"
)
PROGRESS.write_text(
    "# Lilly source through unnumbered fourth-house father/patrimony — 2026-10-17\n\n"
    "Once remotely accepted **8,423 historical documentary "
    "annotations** (7,357 Lilly + 1,066 Ptolemy), "
    "original first-edition source PDF604/894 (**67.6% scanned "
    "position only**). Historical father fourth-house source "
    "62 annotations, sect-specific Sun/Saturn, own father chart "
    "preference, conflicting welfare and uncertain glyphs. "
    "No real parent socioeconomic, medical or mortality forecasts "
    "have been independently verified; no runtime promotions. "
    "Next printed CHAP CXXII mother PDF604–605. "
    "Numeric tables and blind independent research remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05w.md").read_text()
)
CURRENT.write_text(
    "# Original 1647 father/patrimony source accepted historically, mother next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05w first-edition "
    "R7296–R7357 locally prepared; after GitHub verification "
    "7,357 Lilly + 1,066 Ptolemy = 8,423 historical records. "
    "Unnumbered fourth house did not increment chapter "
    "count. No genuine human mortality/paternity/ancestry "
    "prediction success or runtime rule promotion. "
    "NEXT printed CXXII Of the Mother on PDF604.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05w.md").read_text()
)
receipt = {
    "batch": "B05w",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_git_blob": old_blob,
    "old_index_sha256": h(BACK / "INDEX_BEFORE_B05w.json"),
    "new_index_sha256": h(IDX),
    "latest_sha256": h(LATEST),
    "progress_sha256": h(PROGRESS),
    "current_sha256": h(CURRENT),
    "rules_sha256": h(B / "RULES.json"),
    "archive_sha256": zipreceipt["archive_sha256"],
    "lilly_if_published": 7357,
    "ptolemy_retained": 1066,
    "combined_if_published": 8423,
    "numbered_chapters_added": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
