#!/usr/bin/env python3
"""Guarded append-only historical source admission of original printed CHAP CXV."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05o_WEALTH_SOURCES.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05o.json"):
    assert not path.exists(), f"Already/partially admitted, inspect before retry: {path}"
index = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")

assert index["records_count"] == a["previous_lilly"] == 6910
assert index["read_numbered_chapters"] == list(range(1, 116))
assert index["batches"][-1]["id"] == "B05n"
assert index["next"]["chapter"] == "CXVI"
assert index["next"]["pdf_page"] == 588
assert index["next"]["printed_chapter_numeral"] == "CXV"
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(p["id"] == "B05o" for p in index["batches"])
assert r["record_count"] == a["new_source_annotations"] == 84
assert r["source_normalized_items"] == a["normalized_cell_items"] == 316
assert [item["record_number"] for item in r["rules"]] == list(range(6911, 6995))
assert sum(item["role"] == "next_chapter_navigation" for item in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert a["lilly_if_published"] == 6994
assert a["combined_if_published"] == 8060
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["per_member_hash_passed"] and z["full_extraction_passed"]
assert z["replayed_source_tests"] == 28
assert sha(z["archive_path"]) == z["archive_sha256"]
assert all(
    not (
        rec["independently_validated_human_financial_result"]
        or rec["validated_person_occupational_or_moral_inference"]
        or rec["clinical_or_economic_action_authorized"]
        or rec["promoted_as_executable_runtime_rule"]
    )
    for rec in r["rules"]
)
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05o.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05o.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05o.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05o",
        "path": "batches/B05o/RULES.json",
        "records_count": 84,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 William Lilly printed CHAP CXV/editorial CXVI "
            "From whence or by what means Estate/Poverty, source body "
            "PDF588-594 with printed CXVI opening PDF594 and context "
            "PDF595-596. 84 historical documentary records R6911-R6994: "
            "46 prose claims, 36 structured classification cells, 2 following "
            "chapter navigation. Exactly 316 normalized original-source "
            "category items: seven planets x matters and persons, four elemental "
            "sign classifications, six planetary sign nature categories, twelve "
            "house correspondence cells; full source-to-record reverse mapping. "
            "Rules select planetary nature, sign, house, partile aspect, and "
            "count strong vs weak testimony; all-strong rare, majority-strong "
            "allows episodes of loss, majority-weak permits temporary gains, "
            "equal-strength produces variation relative to ancestor baseline. "
            "Original PDF594 and PDF595 both show printed folio561, with "
            "physical scan/text continuous. Period social/moral/vocational "
            "stereotypes are history only. No human financial results "
            "verified or scoring runtime promotion."
        ),
    }
)
index["records_count"] = 6994
index["read_numbered_chapters"].append(116)
index["status"] = "BOOK_III_WEALTH_ORIGIN_HISTORICAL_SOURCE_COMPLETE_NEXT_LAWFUL_GAIN"
index["next"] = {
    "pdf_page": 594,
    "printed_page_as_seen": 561,
    "source_folio_duplicate": True,
    "chapter": "CXVII",
    "printed_chapter_numeral": "CXVI",
    "heading": ("If the Native shall attaine his Estate by just meanes, or indirect dealing"),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Separate printed CHAP CXVI begins below original divider in "
        "lower PDF594/printed561, continues PDF595 also printed561, "
        "and ends before CHAP CXVII heading in PDF596/printed562. "
        "Original PDF594 and 595 share a 561 folio misprint; "
        "source image order and body paragraphs are continuous."
    ),
    "following_printed_chapter": "CXVII",
    "following_editorial_chapter": "CXVIII",
    "following_original_pdf_frame": 596,
    "research_scope": (
        "Historical lawful/unlawful wealth acquisition qualifiers, "
        "mutual aspects, benefic/malefic state, combustion/retrograde "
        "and directional timing; all are unvalidated and must not "
        "be used for allegations about a living person's ethics."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXVI_source_acceptance_note"] = (
    "B05o records R6911–R6994, 84 historical annotations, "
    "316 normalized source-list items in 36 planet, element, "
    "planetary-nature and house classification cells plus "
    "48 prose/navigation records. Original witness frames588-596 "
    "SHA256-checked, 28 portable tests replayed; no actual "
    "financial/career/cause-of-estate success or runtime promotion."
)
assert index["records_count"] == sum(item["records_count"] for item in index["batches"]) == 6994
assert index["read_numbered_chapters"] == list(range(1, 117))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# William Lilly first edition: how wealth is acquired — historical source accepted\n\n"
    + review
    + "\n## Accepted archival corpus, not predictive validity\n\n"
    + "After verified publication, **6,994 Lilly + 1,066 Ptolemy = "
    + "8,060 historical source annotations** (not 8,060 independent "
    + "predictions). Original page images, source-cell completeness "
    + "and 28 replayed integrity tests verified. No new independent "
    + "economic/occupational forecasts, no real-world causality "
    + "claims and zero promoted runtime source rules.\n"
)
PROGRESS.write_text(
    "# Lilly first edition original source study through wealth origins — 2026-10-17\n\n"
    "8,060 historical annotations after authenticated publication "
    "(6,994 Lilly, 1,066 Ptolemy); first-edition source "
    "frontier PDF594 of 894 scans (**~66.4% physical page position only**). "
    "Printed CHAP CXV wealth-origins study preserves seven planet "
    "matters/persons matrices, four elements, six planetary-nature "
    "categories, twelve houses, 316 normalized source terms plus "
    "48 prose/navigation records, totaling 84 annotations. "
    "The original printed folio 561 is duplicated on PDF594/595. "
    "Next printed CHAP CXVI begins PDF594 and ends before CXVII on "
    "PDF596. Numeric tables elsewhere and prospective blind "
    "evaluation remain OPEN; no new validated economic successes, "
    "model promotions or individual forecasts.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05o.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly wealth-origin historical source admitted; lawful acquisition next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05o records R6911–R6994 "
    "prepared for source-only acceptance. After authenticated "
    "GitHub readback the historical corpus totals 6,994 Lilly "
    "+ 1,066 retained Ptolemy = 8,060. 36 structured "
    "planet/sign/house cells and 316 normalized source-list items "
    "from original printed CHAP CXV preserved, including a "
    "period folio numbering anomaly. No independent human "
    "economic success and no runtime rule. Following printed "
    "CHAP CXVI, whether wealth was acquired by lawful or "
    "indirect dealing, begins original PDF594.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05o.md").read_text()
)
receipt = {
    "batch": "B05o",
    "status": "GUARDED_CANONICAL_SOURCE_PREPARED_PENDING_GITHUB",
    "old_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B05o.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_report_sha256": sha(LATEST),
    "progress_report_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "owner_archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6994,
    "ptolemy_retained": 1066,
    "combined_if_published": 8060,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
