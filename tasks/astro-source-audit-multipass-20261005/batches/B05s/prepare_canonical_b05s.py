#!/usr/bin/env python3
"""Guarded append-only first-edition Lilly historical sibling count accession."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05s_SIBLING_NUMBER.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05s.json"):
    assert not p.exists(), f"Duplicate or interrupted source index admission: {p}"
index = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 7138
assert index["read_numbered_chapters"] == list(range(1, 119))
assert index["batches"][-1]["id"] == "B05r"
assert index["next"]["chapter"] == "CXIX"
assert index["next"]["printed_chapter_numeral"] == "CXVIII"
assert index["next"]["pdf_page"] == 598
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B05s" for x in index["batches"])
assert r["record_count"] == a["new_historical_source_records"] == 48
assert a["lilly_if_published"] == 7186 and a["combined_if_published"] == 8252
assert [x["record_number"] for x in r["rules"]] == list(range(7139, 7187))
assert sum(x["role"] == "sign_source" for x in r["rules"]) == 12
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_sibling_number_validation"]
        or x["human_sex_or_fertility_prediction_validated"]
        or x["clinical_or_family_planning_advice_authorized"]
        or x["runtime_rule_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["source_rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 20 and sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
prior_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True
).strip()
assert (
    prior_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05s.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05s.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05s.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05s",
        "path": "batches/B05s/RULES.json",
        "records_count": 48,
        "sha256": a["source_rules_sha256"],
        "scope": (
            "Original 1647 William Lilly printed CHAP CXVIII/editorial CXIX "
            "'If have Brethren or Sisters', original PDF598-600 body "
            "with separate following CXIX heading lower PDF600. "
            "48 historical records: 46 substantive sibling presence/"
            "number and classification conditions, two navigation. "
            "Third-house cusp/ruler/interceptions, Mars-brothers and "
            "Moon-sisters, fruitful/barren planet-sign conjunctions "
            "with mixed middle cases, optional lunar nodes, conditional "
            "Sun/Moon/Mercury, ranked aspects and partile/platick "
            "distinction, twelve separate zodiac sign attributions "
            "including Scorpio exception. No demographic or clinical "
            "validity, no person-level family prediction and "
            "no source rule promoted into runtime."
        ),
    }
)
index["records_count"] = 7186
index["read_numbered_chapters"].append(119)
index["status"] = "BOOK_III_NUMBERED_SIBLINGS_HISTORICAL_SOURCE_COMPLETE_NEXT_SIBLING_CONDITION"
index["next"] = {
    "pdf_page": 600,
    "printed_page": 566,
    "chapter": "CXX",
    "printed_chapter_numeral": "CXIX",
    "heading": "Of the Fortune and condition of Brethren",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXIX begins after the divider roughly "
        "mid original PDF600/folio566. Its sibling-condition "
        "testimonies end on that page; next printed CHAP CXX "
        "on familial concord begins at top of original PDF601/folio567."
    ),
    "following_printed_chapter_numeral": "CXX",
    "following_pdf_page": 601,
    "research_scope": (
        "Historical sibling fortune/relative conditions, "
        "whether strong versus weak testimonies and claimed "
        "gender asymmetry, without medical/social validity "
        "or any real relationship outcome claim."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXIX_source_acceptance_note"] = (
    "B05s R7139-R7186: 48 historical source units, 12 zodiac "
    "sign source claims, 46 substantive + two next-chapter "
    "navigation; original 1647 PDF598-602 SHA and 20 "
    "archive-replayed source tests. Zero human demographic "
    "validations and zero runtime promotions."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7186
assert index["read_numbered_chapters"] == list(range(1, 120))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly first edition sibling-number chapter accepted as history\n\n"
    + review
    + "\n## Documentary record total\n\n"
    + "After authenticated publication **7,186 Lilly + 1,066 "
    + "Ptolemy = 8,252 historical source records**, not "
    + "validated human birth counts. Source image hash "
    + "and 20 extracted ZIP replay tests pass; all "
    + "human sibling/fertility accuracy and "
    + "runtime promotions remain zero.\n"
)
PROGRESS.write_text(
    "# Lilly source through numbered sibling-count chapter — 2026-10-17\n\n"
    "8,252 historical source units after remote publication "
    "(7,186 Lilly + 1,066 Ptolemy), original 1647 "
    "source frontier PDF600 of 894 (**~67.1% scanned position "
    "only, not completion of astrology validation**). "
    "Printed CHAP CXVIII sibling presence/number recorded "
    "as 48 historically asserted source notes including "
    "12 zodiac categories and numerous contrary/optional "
    "conditions. Next printed CHAP CXIX sibling fortune "
    "begins on same PDF600. No real birth/fertility "
    "prediction validation or new runtime rules.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05s.md").read_text()
)
CURRENT.write_text(
    "# Source study: Lilly numbered siblings historical annotations accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05s "
    "R7139-R7186 source documentation accepted; after "
    "GitHub readback 7,186 Lilly + 1,066 Ptolemy "
    "= 8,252 original source annotations. 12 sign "
    "classifications, planet/sign mixtures and "
    "partile priority preserved. Human birth-count "
    "validation zero, no runtime rules. NEXT original "
    "printed CXIX sibling condition on PDF600.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05s.md").read_text()
)
receipt = {
    "batch": "B05s",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "prior_git_blob": prior_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B05s.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7186,
    "ptolemy_retained": 1066,
    "combined_if_published": 8252,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
