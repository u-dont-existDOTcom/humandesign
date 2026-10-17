#!/usr/bin/env python3
"""Append original mining-source documentary annotations to canonical index."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06c_MINES.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06c.json"):
    assert not path.exists(), f"Duplicate or partial source index: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7548
assert i["read_numbered_chapters"] == list(range(1, 128))
assert i["batches"][-1]["id"] == "B06b"
assert i["next"]["chapter"] == "CXXVIII"
assert i["next"]["printed_chapter_numeral"] == "CXXVII"
assert i["next"]["pdf_page"] == 609
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06c" for x in i["batches"])
assert r["record_count"] == a["new_historical_records"] == 35
assert a["lilly_if_published"] == 7583
assert a["combined_if_published"] == 8649
assert [x["record_number"] for x in r["rules"]] == list(range(7549, 7584))
assert sum(x["role"] == "next_section_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_mining_finance_prediction_validated"]
        or x["actual_ore_or_mineral_deposit_validated"]
        or x["modern_legal_financial_or_mining_advice_authorized"]
        or x["runtime_rule_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 15 and sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06c.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06c.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06c.md").write_bytes(PROGRESS.read_bytes())
i["batches"].append(
    {
        "id": "B06c",
        "path": "batches/B06c/RULES.json",
        "records_count": 35,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly first edition printed CHAP CXXVII/editorial CXXVIII "
            "on speculative Fortune to be obtained out of mines, "
            "source original PDF609/printed575. Nine source-first "
            "groups, 33 historic mining wealth conditions plus "
            "two next-source navigation. Saturn fourth ruler or "
            "occupant, essential dignity, direct/swift and benefic "
            "aspects, power grading, reception with luminaries or "
            "their dispositor, Jupiter in fourth in Libra as tin/estate, "
            "Saturn fourth Aquarius plus Jupiter Libra, "
            "Mars fourth Leo plus Sun Aries as iron/silver/gold, "
            "Saturn earth sign with Sun/Mars/Mercury and fourth "
            "house contact as coal/lead. Source-only economic "
            "stereotypes, no tested deposits, commercial returns, "
            "investment validity or runtime source rule promotion."
        ),
    }
)
i["records_count"] = 7583
i["read_numbered_chapters"].append(128)
i["status"] = "BOOK_III_MINING_HISTORICAL_NEXT_UNNUMBERED_SIXTH_HOUSE"
i["next"] = {
    "pdf_page": 610,
    "printed_page": 576,
    "chapter": "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES",
    "printed_chapter_numeral": None,
    "heading": (
        "The sixt House, and the Judgments appertaining unto it. "
        "Of the Infirmities and Diseases of Bodyes"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original first edition unnumbered sixth-house substantive "
        "introduction begins at top PDF610/printed576 after decorative "
        "separator, then continues PDF611/printed577 with 'Aphorismes "
        "usefull for this House', and beyond. Original PDF610–617 "
        "source context was retained in the prior B06b source "
        "branch; locate actual following numbered chapter "
        "boundary before declaring completeness."
    ),
    "research_scope": (
        "Historical illness/temperament and sixth-house natal "
        "significators, the first/sixth/seventh house and lords, "
        "Sun/Moon, malefic aspects, natal health aphorisms, "
        "body illnesses and premodern humoral categories. "
        "These are not actual clinical evidence; no medical advice."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXVIII_source_acceptance_note"] = (
    "B06c R7549–R7583, 35 original mining-source "
    "annotations, 33 substantive and 2 following-sixth "
    "navigation, PDF609–612 source SHA and 15 archive tests, "
    "zero mining return predictions or runtime rules."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7583
assert i["read_numbered_chapters"] == list(range(1, 129))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original 1647 mines/minerals wealth source historically accepted\n\n"
    + review
    + "\n## Source-only acceptance\n\n"
    + "After verified publication **7,583 Lilly + 1,066 "
    + "Ptolemy = 8,649 historical source notes**, not "
    + "independent mining outcome forecasts. Fifteen "
    + "source integrity and extracted-archive tests pass; "
    + "no financial validity or model promotion.\n"
)
PROGRESS.write_text(
    "# Lilly original source study through mining fortunes — 2026-10-17\n\n"
    "After verified GitHub publication **8,649 historical "
    "source annotations** (7,583 Lilly + 1,066 Ptolemy). "
    "Original first-edition source-body frontier PDF609 "
    "of 894 (**68.1% physical page position only**). "
    "Printed CHAP CXXVII mineral fortunes recorded as "
    "35 historical conditions and following-source "
    "navigation. No real mine discovery/investment outcome "
    "evidence, no scoring source promotions. "
    "Next unnumbered sixth-house intro and medical "
    "aphorisms starts original PDF610. "
    "Historic numerical pole tables and independent "
    "human testing remain OPEN.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06c.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly mine wealth historical chapter accepted; sixth-house medical section next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source-only B06c "
    "R7549–R7583 prepared, total 7,583 Lilly plus 1,066 "
    "Ptolemy = 8,649 archival notes after remote verification. "
    "No mined minerals or financial return predictions "
    "validated and no runtime rules. NEXT original PDF610 "
    "unnumbered sixth-house infirmities and aphorisms.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06c.md").read_text()
)
receipt = {
    "batch": "B06c",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06c.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7583,
    "ptolemy_retained": 1066,
    "combined_if_published": 8649,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
