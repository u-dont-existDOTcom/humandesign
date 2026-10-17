#!/usr/bin/env python3
"""Guarded append-only integration of Lilly first-edition CHAP CXIIII, historical only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05n_WHETHER_RICH.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (BACK / "INDEX_BEFORE_B05n.json", LATEST, RECEIPT):
    assert not path.exists(), f"Possible duplicate/partly applied admission: {path}"

i = load(INDEX)
a = load(B / "ACCEPTANCE.json")
r = load(B / "RULES.json")
z = load(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 6853
assert i["read_numbered_chapters"] == list(range(1, 115))
assert i["batches"][-1]["id"] == "B05m"
assert i["next"]["chapter"] == "CXV" and i["next"]["pdf_page"] == 587
assert i["next"]["printed_chapter_numeral"] == "CXIIII"
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(item["id"] == "B05n" for item in i["batches"])
assert r["record_count"] == a["new_source_annotations"] == 57
assert a["lilly_if_published"] == 6910 and a["combined_if_published"] == 7976
assert [row["record_number"] for row in r["rules"]] == list(range(6854, 6911))
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert sum(row["role"] == "next_chapter_navigation" for row in r["rules"]) == 2
assert all(
    not (
        row["independent_economic_outcome_validated"]
        or row["tested_wealth_prediction_success"]
        or row["financial_advice_authorized"]
        or row["runtime_model_promoted"]
    )
    for row in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_pass"] and z["per_member_hashes_pass"]
assert z["full_extraction_pass"] and z["replayed_source_tests"] == 24
assert sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05n.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05n.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05n.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B05n",
        "path": "batches/B05n/RULES.json",
        "records_count": 57,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original 1647 printed CHAP CXIIII/editorial CXV "
            "'Whether the Native shall be Rich', lower original PDF587 "
            "to above next heading PDF588. 12 first-edition page-anchored "
            "source groups, 55 selective historical source claims and "
            "2 next numbered chapter navigation. Preserves prerequisite "
            "significators from prior unnumbered second-house section, "
            "angular vs majority angular plus essential dignity, "
            "graduated testimonies and poverty/moderate class, Regulus "
            "and Spica operator ambiguities, benefit from both benefic "
            "and malefic source planets, joint Sun/Moon and Jupiter/Moon "
            "placement alternatives, 3 conditional inheritance patterns, "
            "Saturn land accumulation, negative configurations, "
            "unverified glyph and the 'contrary' exception. "
            "No independently measured real wealth or verified forecasts "
            "and no runtime scoring promotion."
        ),
    }
)
i["records_count"] = 6910
i["read_numbered_chapters"].append(115)
i["status"] = "BOOK_III_NUMBERED_WEALTH_HISTORICAL_COMPLETE_NEXT_SOURCE_OF_WEALTH"
i["next"] = {
    "pdf_page": 588,
    "printed_page": 554,
    "chapter": "CXVI",
    "printed_chapter_numeral": "CXV",
    "heading": ("From whence, or by what meanes the Native shall come to an Estate or to Poverty"),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXV begins after divider in lower PDF588/printed554, "
        "continues PDF589–591 and possibly later. The lower PDF589 opens "
        "planet-by-planet tables separating matters from persons, while "
        "PDF591 transitions to zodiac sign and house categories. "
        "Actual next boundary must be verified before extraction closes."
    ),
    "research_scope": (
        "Cause and channel of wealth/poverty from original 1647 "
        "planet/person/matter, sign-element, and house correspondence "
        "tables. Preserve complete original semantic coverage and "
        "historical attribution; do not conflate these with validated "
        "human occupational, financial or mortality predictions."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXV_source_acceptance_note"] = (
    "R6854-R6910: 57 historical source records (55 body claims, "
    "2 next-heading navigation), 12 page-anchored groups and 5 "
    "original scanned witness frames; 24 portable tests. "
    "No successful economic forecast, financial evidence or new "
    "model promotion. Following printed CXV's matter/person "
    "and sign/house source tables remain open."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 6910
assert i["read_numbered_chapters"] == list(range(1, 116))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original first edition — Whether Rich, documentary accepted\n\n"
    + review
    + "\n## Canonical accepted source\n\n"
    + "R6854–R6910: 57 historical original-source clauses and "
    + "navigation. Upon authenticated GitHub publication, "
    + "**6,910 Lilly + 1,066 Ptolemy = 7,976 historical "
    + "documentary records**, not 7,976 independently correct "
    + "wealth predictions. ZIP CRC/SHA and 24 replayed original "
    + "source integrity tests passed. No new empirical results "
    + "or runtime promotions. Next printed CXV starts lower PDF588.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 historical source through numbered Whether Rich — 2026-10-17\n\n"
    "**7,976 historical annotations** after authenticated "
    "publication (6,910 Lilly + 1,066 Ptolemy). Original first "
    "edition source-body frontier PDF588 of 894 (~65.8% "
    "scanned-position proxy, NOT science completion). "
    "Printed CHAP CXIIII Whether Rich: 57 documentary records "
    "with explicit testimony strength tiers, qualified wealth "
    "and poverty branches, uncertain fixed-star/operator and "
    "glyph conditions, separate causes of inheritance. "
    "Following printed CHAP CXV begins PDF588 and has extensive "
    "planet-person-matter, zodiac-sign and house correspondence "
    "tables to preserve. No new independent human economic "
    "outcomes, source-lane runtime promotion or new rule validity. "
    "Numeric astronomy and blind comparisons remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05n.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly 1647 Whether Rich historic source admitted; source-of-estate next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. R6854–R6910 source-first "
    "accepted locally with 55 historic claims and 2 following "
    "navigation. After verified publication 6,910 Lilly + 1,066 "
    "Ptolemy = 7,976 documentary records. Regulus/Spica, "
    "glyph and contrary-outcome ambiguity retained. "
    "No independent financial/inheritance success and no "
    "scoring runtime promotions. NEXT printed CHAP CXV "
    "From whence estate or poverty, lower original PDF588.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05n.md").read_text()
)
receipt = {
    "batch": "B05n",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B05n.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6910,
    "retained_ptolemy": 1066,
    "combined_if_published": 7976,
    "next_original_pdf_frame": 588,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
