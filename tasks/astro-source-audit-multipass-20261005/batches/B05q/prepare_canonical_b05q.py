#!/usr/bin/env python3
"""Append-only canonical source acceptance: original Lilly wealth durability."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05q_ESTATE_DURABILITY.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05q.json"):
    assert not p.exists(), f"Prior/interrupted admission detected: {p}"
index = j(INDEX)
accepted = j(B / "ACCEPTANCE.json")
rules = j(B / "RULES.json")
archive = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")

assert index["records_count"] == accepted["previous_lilly"] == 7051
assert index["read_numbered_chapters"] == list(range(1, 118))
assert index["batches"][-1]["id"] == "B05p"
assert index["next"]["chapter"] == "CXVIII"
assert index["next"]["printed_chapter_numeral"] == "CXVII"
assert index["next"]["pdf_page"] == 596
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(row["id"] == "B05q" for row in index["batches"])
assert rules["record_count"] == accepted["new_records"] == 75
assert accepted["lilly_if_published"] == 7126
assert accepted["combined_historical_if_published"] == 8192
assert [r["record_number"] for r in rules["rules"]] == list(range(7052, 7127))
assert sum(r["role"] == "next_section_navigation" for r in rules["rules"]) == 3
assert rules["empirical_validations"] == accepted["empirical_validations"] == 0
assert rules["runtime_promotions"] == accepted["runtime_promotions"] == 0
assert all(
    not (
        r["independent_human_financial_validation"]
        or r["actual_wealth_timing_accuracy_verified"]
        or r["real_person_moral_or_legal_inference_authorized"]
        or r["runtime_model_promoted"]
    )
    for r in rules["rules"]
)
assert sha(B / "RULES.json") == accepted["rules_sha256"] == archive["source_rules_sha256"]
assert archive["crc_passed"] and archive["per_member_sha256_passed"]
assert archive["full_extraction_passed"] and archive["replayed_source_tests"] == 26
assert sha(archive["archive_path"]) == archive["archive_sha256"]

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05q.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05q.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05q.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05q",
        "path": "batches/B05q/RULES.json",
        "records_count": 75,
        "sha256": accepted["rules_sha256"],
        "scope": (
            "Original first-edition Lilly printed CHAP CXVII/editorial CXVIII "
            "'If the Estate of the Native shall continue, or be Durable', "
            "source body PDF596–598, and following unnumbered third-house "
            "kinred intro plus next printed CXVIII opening on PDF598. "
            "13 image-anchored groups and 75 historical annotations "
            "(72 claims, 3 navigation). Benefic/malefic in second house "
            "with strength and essential dignity, fluctuation and "
            "overthrow alternatives, strongest occupant ranking, "
            "empty house fallback to second ruler/Fortune dispositor, "
            "directed Wealth timings, broad age and house quadrants, "
            "orientation/speed/lifespan modifiers, fixed stars and "
            "contrary economic conditions. No independently observed "
            "human income, property outcome or timing success and "
            "no runtime promotions."
        ),
    }
)
index["records_count"] = 7126
index["read_numbered_chapters"].append(118)
index["status"] = "BOOK_III_WEALTH_DURABILITY_HISTORICAL_COMPLETE_NEXT_UNNUMBERED_THIRD_HOUSE"
index["next"] = {
    "pdf_page": 598,
    "printed_page": 564,
    "chapter": "UNNUMBERED_THIRD_HOUSE_KINRED",
    "printed_chapter_numeral": None,
    "heading": "Judgments upon the third House. Of Kinred, viz. Brethren and Sisters",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original PDF598 printed564 after decorative separator "
        "begins the unnumbered third-house introduction. "
        "Printed CHAP CXVIII 'If have Brethren or Sisters' "
        "opens lower on the same PDF598 and continues PDF599. "
        "Preserve both substantive source segments separately."
    ),
    "following_printed_chapter_numeral": "CXVIII",
    "following_editorial_chapter": "CXIX",
    "following_chapter_pdf_page": 598,
    "research_scope": (
        "Historical sibling relationships and family-size signification, "
        "distinct from wealth and from empirical relationship research. "
        "Preserve independent chart/age prerequisites and exceptions."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXVIII_source_acceptance_note"] = (
    "B05q R7052–R7126, 75 historical documentary units: "
    "72 substantive clauses and 3 next-section navigation. "
    "Original source PDF596–600 SHA256-verified; 26 "
    "archive-replayed source tests. Age/timing flexibility "
    "and non-predictive status preserved; no runtime rules."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7126
assert index["read_numbered_chapters"] == list(range(1, 119))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly estate durability — historical source accepted\n\n"
    + review
    + "\n## Source versus science\n\n"
    + "After verified GitHub publication **7,126 Lilly + 1,066 Ptolemy "
    + "= 8,192 historical documentary records**, not real "
    + "economic predictions. Original SHA scans and "
    + "26 extracted-archive source tests passed. No "
    + "independent financial or timing validations "
    + "and no runtime-rule promotions.\n"
)
PROGRESS.write_text(
    "# Lilly original first edition through wealth durability — 2026-10-17\n\n"
    "After verified remote publication **8,192 historical source "
    "annotations** (7,126 Lilly + 1,066 Ptolemy). "
    "Physical first-edition frontier PDF598 of 894 "
    "(**66.9% positional**, not predictive-science progress). "
    "Original printed CHAP CXVII durability has "
    "75 historical clauses/navigation, with alternative "
    "life-period timing, family wealth, conflicting economic "
    "fortunes and uncalibrated directions. "
    "Next UNNUMBERED third-house sibling intro starts "
    "mid frame598 before printed CXVIII. "
    "No verified real-person financial predictions, "
    "table-digitization completion, or new runtime rules.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05q.md").read_text()
)
CURRENT.write_text(
    "# First-edition Lilly wealth durability historical study accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. R7052–R7126 "
    "added as original historical annotations, "
    "7,126 Lilly + 1,066 retained Ptolemy = 8,192 "
    "after remote verification. All 26 source "
    "integrity/coverage tests passed, no financial "
    "success evidence, no model promotion. "
    "NEXT original PDF598 unnumbered third-house "
    "kinship introduction before numbered CXVIII.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05q.md").read_text()
)
receipt = {
    "batch": "B05q",
    "status": "CANONICAL_PREPARED_PENDING_PUBLISHED_REMOTE",
    "prior_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B05q.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "portable_archive_sha256": archive["archive_sha256"],
    "lilly_if_published": 7126,
    "ptolemy_retained": 1066,
    "combined_if_published": 8192,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
