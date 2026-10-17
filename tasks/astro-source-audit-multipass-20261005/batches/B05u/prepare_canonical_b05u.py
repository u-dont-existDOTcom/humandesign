#!/usr/bin/env python3
"""Append-only first edition historic source acceptance of sibling harmony."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05u_SIBLING_CONCORD.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for f in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05u.json"):
    assert not f.exists(), f"Prior or interrupted archival acceptance: {f}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7208
assert i["read_numbered_chapters"] == list(range(1, 121))
assert i["batches"][-1]["id"] == "B05t"
assert i["next"]["chapter"] == "CXXI"
assert i["next"]["printed_chapter_numeral"] == "CXX"
assert i["next"]["pdf_page"] == 601
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(q["id"] == "B05u" for q in i["batches"])
assert r["record_count"] == a["new_records"] == 44
assert a["lilly_if_published"] == 7252 and a["combined_if_published"] == 8318
assert [q["record_number"] for q in r["rules"]] == list(range(7209, 7253))
assert sum(q["role"] == "next_chapter_navigation" for q in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 15 and sha(z["archive_path"]) == z["archive_sha256"]
assert all(
    not (
        q["verified_family_relationship_prediction"]
        or q["validated_financial_or_legal_claim"]
        or q["clinical_or_personal_accusation_authorized"]
        or q["runtime_rule_promoted"]
    )
    for q in r["rules"]
)
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05u.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05u.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05u.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B05u",
        "path": "batches/B05u/RULES.json",
        "records_count": 44,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly first edition printed CHAP CXX/editorial CXXI "
            "Of the unity or concord of the Native with his Brethren "
            "and Sisters, original PDF601/printed567. Source PDF602 "
            "following independent printed CXXI. Eight source-first "
            "passage groups, 42 historical source claims and 2 next "
            "chapter navigation. First/third house lord benevolent "
            "aspects versus square/opposition/no aspect, reception "
            "and trine/Mars exceptions, Saturn/Mars/South Node "
            "anecdote without verifiable cases, favorable/hostile "
            "sibling dyads, alleged kin wealth impacts, ascending "
            "sign groups and Mercury/Mars opposition, explicit "
            "extension to kin and neighbors. No real human "
            "family relationship predictions validated, no "
            "criminal/medical/financial inference permitted, "
            "zero new runtime source rules."
        ),
    }
)
i["records_count"] = 7252
i["read_numbered_chapters"].append(121)
i["status"] = "BOOK_III_SIBLING_HARMONY_HISTORICAL_NEXT_SIBLING_NUMBER_METHOD"
i["next"] = {
    "pdf_page": 602,
    "printed_page": 568,
    "chapter": "CXXII",
    "printed_chapter_numeral": "CXXI",
    "heading": "Number of Brethren",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXI begins at the top original PDF602 "
        "printed568. Its full sibling-count method and "
        "comparison/criticism of Ptolemy run through PDF602; "
        "following independent source boundary must be "
        "verified before archival acceptance."
    ),
    "research_scope": (
        "Historical sign/third-ruler, masculine/feminine "
        "aspect counting, sibling survival/firstborn conditions; "
        "contrasting Ptolemy's Midheaven maternal reference "
        "with Lilly's third house. Do not count earlier "
        "sibling-number chapter as independent experiments."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXI_source_acceptance_note"] = (
    "B05u R7209–R7252 original documentary source claims: "
    "42 substantive historical attributions and 2 "
    "next-chapter navigation, 8 source groups, first-edition "
    "PDF601/602 images and 15 archive-replayed verification "
    "tests. No validated family conflicts or runtime rules."
)
assert i["records_count"] == sum(p["records_count"] for p in i["batches"]) == 7252
assert i["read_numbered_chapters"] == list(range(1, 122))
INDEX.write_text(json.dumps(i, indent=2, ensure_ascii=False) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first edition sibling concord as historical source\n\n"
    + review
    + "\n## Canonical archival checkpoint\n\n"
    + "After authenticated publication **7,252 Lilly + 1,066 "
    + "Ptolemy = 8,318 historical source annotations**. "
    + "Fifteen source integrity tests pass both locally and "
    + "in standalone ZIP. No independent family harm/benefit "
    + "prediction successes, no runtime promotion.\n"
)
PROGRESS.write_text(
    "# Lilly original first-edition source through sibling concord — 2026-10-17\n\n"
    "After verified publication: **8,318 historical source "
    "annotations** (7,252 Lilly + 1,066 Ptolemy), first-edition "
    "frontier original PDF601/894 (**67.2% of physical scan "
    "position only, not overall science completion**). Printed "
    "CHAP CXX sibling-harmony historical study adds 44 source "
    "notes with contradictory favorable/negative/no aspect "
    "categories, reception exceptions, and unverified "
    "author anecdote. No independent social validity. "
    "Next printed CHAP CXXI original PDF602 sibling-count method "
    "and Ptolemy disagreement; empirical validation and "
    "numeric astronomy lanes remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05u.md").read_text()
)
CURRENT.write_text(
    "# Original 1647 Lilly sibling-concord historical chapter accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05u source R7209–R7252 "
    "accepted pending GitHub readback: 7,252 Lilly + 1,066 "
    "Ptolemy = 8,318 historical source notes. "
    "Sibling harmony/conflict are unverified period "
    "characterizations with no person-level applicability. "
    "Original PDF601, following printed CXXI begins PDF602. "
    "No empirical results or runtime promotions.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05u.md").read_text()
)
receipt = {
    "batch": "B05u",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B05u.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7252,
    "ptolemy_retained": 1066,
    "combined_if_published": 8318,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
