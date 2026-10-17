#!/usr/bin/env python3
"""Append-only archive admission of original Lilly sibling-fortune text."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05t_SIBLING_CONDITION.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05t.json"):
    assert not p.exists(), f"Potential interrupted or duplicate acceptance: {p}"
index = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 7186
assert index["read_numbered_chapters"] == list(range(1, 120))
assert index["batches"][-1]["id"] == "B05s"
assert index["next"]["chapter"] == "CXX"
assert index["next"]["printed_chapter_numeral"] == "CXIX"
assert index["next"]["pdf_page"] == 600
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(v["id"] == "B05t" for v in index["batches"])
assert r["record_count"] == a["new_source_records"] == 22
assert [v["record_number"] for v in r["rules"]] == list(range(7187, 7209))
assert sum(v["role"] == "next_chapter_navigation" for v in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert a["lilly_if_published"] == 7208 and a["combined_if_published"] == 8274
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 13 and sha(z["archive_path"]) == z["archive_sha256"]
assert all(
    not (
        row["actual_human_sibling_outcome_validated"]
        or row["sibling_longevity_validated"]
        or row["runtime_model_promoted"]
    )
    for row in r["rules"]
)
relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
prior_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    prior_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05t.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05t.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05t.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05t",
        "path": "batches/B05t/RULES.json",
        "records_count": 22,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly 1647 first edition original printed CHAP CXIX/editorial "
            "CXX 'Of the Fortune and condition of Brethren' begins lower "
            "original PDF600/printed566; next separate printed CHAP CXX opens "
            "top PDF601/printed567. Six page-anchored passage groups, "
            "20 substantive historical conditional claims and 2 next-chapter "
            "navigation entries. All/majority strong predicts favorable "
            "siblings, weak contrary, mixed permits different fortunes, "
            "conditional Moon-strong/Mars-weak sister comparison, reversed "
            "Mars-strong/Moon-weak brother comparison. These are historical "
            "sibling, class, longevity and gender stereotypes only, "
            "no real-person predictive validations or runtime promotions."
        ),
    }
)
index["records_count"] = 7208
index["read_numbered_chapters"].append(120)
index["status"] = "BOOK_III_SIBLING_FORTUNES_DOCUMENTARY_NEXT_SIBLING_HARMONY"
index["next"] = {
    "pdf_page": 601,
    "printed_page": 567,
    "chapter": "CXXI",
    "printed_chapter_numeral": "CXX",
    "heading": "Of the unity or concord of the Native with his Brethren and Sisters",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXX on sibling unity/concord starts at top original "
        "PDF601/printed567, continues most of that page. Next printed "
        "CHAP CXXI 'Number of Brethren' starts on original PDF602/printed568. "
        "A stronger primary-source check of the end seam is required "
        "before accepting printed CXX's source clauses."
    ),
    "following_printed_chapter_numeral": "CXXI",
    "following_original_pdf_page": 602,
    "research_scope": (
        "Original 1647 conditional sibling concord and conflict, third "
        "and first lords, beneficial versus hard aspects, reception, "
        "and disputed planetary stereotypes. Historical only: "
        "no real family relationship forecast or clinical claim."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXX_source_acceptance_note"] = (
    "B05t historical R7187–R7208, 20 conditional source statements "
    "plus 2 next-chapter navigation. Original scanned PDF600–602 "
    "SHA256 and 13 hermetic-replay documentary tests. Zero "
    "validated actual sibling fortunes or runtime promotions."
)
assert index["records_count"] == sum(v["records_count"] for v in index["batches"]) == 7208
assert index["read_numbered_chapters"] == list(range(1, 121))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly sibling fortunes documented: source only\n\n"
    + review
    + "\n## Canonical historical archive\n\n"
    + "After authenticated publication **7,208 Lilly + 1,066 "
    + "Ptolemy = 8,274 historical source records**, not "
    + "empirically validated sibling outcomes. "
    + "Thirteen original-source and standalone archive integrity "
    + "checks passed; no source runtime rule promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly historical study through sibling fortunes — 2026-10-17\n\n"
    "After verified publication the archive contains 8,274 "
    "historical notes (7,208 Lilly + 1,066 Ptolemy). "
    "Physical first-edition source-body frontier PDF600/894 "
    "(67.1% of scanned page position, not full predictive-research "
    "completion). Printed CHAP CXIX sibling fortune/condition "
    "recorded with 22 annotations, source pass/fail and mixed "
    "outcome cases and two contrary gender-attributed comparisons. "
    "No actual sibling wealth, longevity or welfare "
    "evidence verified, no new runtime rules. "
    "Next printed CHAP CXX sibling concord starts PDF601.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05t.md").read_text()
)
CURRENT.write_text(
    "# First-edition sibling fortune historical-source study accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source-only records "
    "R7187–R7208 historically admitted, after verified GitHub "
    "publication 7,208 Lilly + 1,066 retained Ptolemy = 8,274. "
    "Printed CHAP CXIX sibling conditions, strong/weak, "
    "mixed and gender-coded comparisons retained without "
    "human evidence or model promotion. "
    "NEXT original printed CXX on sibling harmony PDF601.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05t.md").read_text()
)
receipt = {
    "batch": "B05t",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_git_blob": prior_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05t.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7208,
    "ptolemy_retained": 1066,
    "combined_if_published": 8274,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
