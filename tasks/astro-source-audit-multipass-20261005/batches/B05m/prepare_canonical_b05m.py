#!/usr/bin/env python3
"""Guarded append-only historical acceptance of Lilly's UNNUMBERED wealth introduction."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05m_SECOND_HOUSE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05m.json"):
    assert not path.exists(), f"Duplicate or interrupted source admission: {path}"

index = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
zipreceipt = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
window = j(B / "SOURCE_WINDOW_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 6808
assert index["read_numbered_chapters"] == list(range(1, 115))
assert index["batches"][-1]["id"] == "B05l"
assert index["next"]["chapter"] == "UNNUMBERED_SECOND_HOUSE_RICHES"
assert index["next"]["pdf_page"] == 586
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(row["id"] == "B05m" for row in index["batches"])
assert window["accepted_lilly_before_extraction"] == 6808
assert window["new_documentary_records"] == 0
assert r["record_count"] == a["new_historical_records"] == 45
assert a["lilly_if_published"] == 6853 and a["combined_if_published"] == 7919
assert [row["record_number"] for row in r["rules"]] == list(range(6809, 6854))
assert sum(row["role"] == "next_chapter_navigation" for row in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        row["independent_human_economic_prediction"]
        or row["actual_inheritance_prediction_validated"]
        or row["runtime_scoring_rule_promoted"]
        or row["source_attribution_verified_against_ptolemy"]
    )
    for row in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == zipreceipt["accepted_rules_sha256"]
assert zipreceipt["crc_pass"] and zipreceipt["all_member_hashes_pass"]
assert zipreceipt["full_extraction_pass"] and zipreceipt["replayed_tests"] == 20
assert sha(zipreceipt["archive_path"]) == zipreceipt["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05m.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05m.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05m.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05m",
        "path": "batches/B05m/RULES.json",
        "records_count": 45,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly 1647 first-edition UNNUMBERED second-house "
            "Riches or Goods of Fortune, original PDF586-587 body; "
            "PDF587 lower begins next numbered CXIIII Whether Rich. "
            "Six image-anchored source passage groups, 43 substantive "
            "source annotations and 2 chapter navigation units. "
            "Second house cusp five-degree interval, ruler/interceptions, "
            "Part of Fortune and dispositor, Jupiter, occupying planets "
            "and degree-to-cusp qualifications. Ptolemy attribution "
            "preserved as attributed, not independently text-verified; "
            "planetary acquisition routes, qualified inheritances, "
            "conditional wealth survival/loss, timing by angles, "
            "Leovitius and Origanus contributions distinguished. "
            "Zero human financial predictive successes, no runtime rules."
        ),
    }
)
index["records_count"] = 6853
# IMPORTANT: This was an unnumbered section; do not increase chapter counter.
assert index["read_numbered_chapters"] == list(range(1, 115))
index["status"] = "BOOK_III_UNNUMBERED_SECOND_HOUSE_SOURCE_COMPLETE_NEXT_NUMBERED_RICH"
index["next"] = {
    "pdf_page": 587,
    "printed_page": 553,
    "chapter": "CXV",
    "printed_chapter_numeral": "CXIIII",
    "heading": "Whether the Native shall be Rich",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 PDF587 below divider starts printed "
        "CHAP CXIIII. Its first group of wealth- and poverty-significator "
        "outcome statements continues through PDF588, where next "
        "CHAP CXV opens below divider. Do not duplicate unnumbered "
        "second-house introduction already admitted as B05m."
    ),
    "following_printed_chapter_numeral": "CXV",
    "following_original_pdf_page": 588,
    "research_scope": (
        "First-edition specific wealth/poverty conditions, "
        "necessary significators, essential strength, strength "
        "of angles and fixed stars; preserve contrary branches "
        "and avoid unvalidated financial predictions."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["unnumbered_second_house_source_acceptance_note"] = (
    "45 historical records R6809-R6853, 43 source claims "
    "and 2 next numbered chapter navigation. Six source groups, "
    "3 physical original images, Ptolemy-as-Lilly-attribution "
    "not verified against Ptolemy. No independent wealth prediction "
    "success and no promoted runtime rule."
)
assert index["records_count"] == sum(row["records_count"] for row in index["batches"]) == 6853
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly unnumbered second house: historical source accepted\n\n"
    + review
    + "\n## Canonical publication boundary\n\n"
    + "**R6809–R6853** source notes admitted separately from printed "
    + "CXIIII. After verified publication: **6,853 Lilly + 1,066 "
    + "Ptolemy = 7,919 historical documentary annotations**. "
    + "Not human economic outcomes or scientifically validated "
    + "forecast accuracy; none are promoted into runtime. "
    + "Original SHA256, release ZIP and 20 archive-replayed tests "
    + "verify documentary integrity only.\n"
)
PROGRESS.write_text(
    "# Lilly original 1647 historical study through unnumbered second house — 2026-10-17\n\n"
    "After publication **7,919 source annotations** "
    "(6,853 Lilly + 1,066 Ptolemy), original first-edition PDF587/894 "
    "(**65.7% scanned-page position proxy**), not empirical "
    "research progress or rule-table completeness. Unnumbered "
    "second house of riches extracted with 45 historical notes. "
    "Original printed CHAP CXIIII begins lower PDF587; no "
    "independent actual-person wealth prediction has been "
    "tested, no source-lane runtime promotions. Outstanding "
    "dense numerical tables, rule coding and blinded tests.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05m.md").read_text()
)
CURRENT.write_text(
    "# Lilly unnumbered natal second-house riches historical documentation accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. R6809-R6853 accepted as "
    "43 historical source clauses and 2 following-chapter "
    "navigation. Archive after remote verification: 6,853 Lilly "
    "+ 1,066 Ptolemy = 7,919. Ptolemy source attribution "
    "preserved as unverified, no financial/outcome blind "
    "predictive success or runtime promotion. Next original "
    "printed CXIIII Whether Rich begins PDF587.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05m.md").read_text()
)
receipt = {
    "batch": "B05m",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "old_index_git_blob": old_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05m.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": zipreceipt["archive_sha256"],
    "lilly_if_published": 6853,
    "ptolemy_retained": 1066,
    "combined_if_published": 7919,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
