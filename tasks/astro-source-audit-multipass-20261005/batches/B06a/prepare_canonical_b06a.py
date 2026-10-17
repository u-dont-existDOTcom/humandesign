#!/usr/bin/env python3
"""Guarded append-only accession of original 1647 parental-concord source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06a_PARENTS_AGREEMENT.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06a.json"):
    assert not path.exists(), f"Duplicate/interrupted original source admission: {path}"
i = read(INDEX)
a = read(B / "ACCEPTANCE.json")
rules = read(B / "RULES.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7473
assert i["read_numbered_chapters"] == list(range(1, 126))
assert i["batches"][-1]["id"] == "B05z"
assert i["next"]["chapter"] == "CXXVI"
assert i["next"]["printed_chapter_numeral"] == "CXXV"
assert i["next"]["pdf_page"] == 607
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(row["id"] == "B06a" for row in i["batches"])
assert rules["record_count"] == a["new_historical_records"] == 29
assert a["lilly_if_published"] == 7502
assert a["combined_historical_if_published"] == 8568
assert [row["record_number"] for row in rules["rules"]] == list(range(7474, 7503))
assert sum(row["role"] == "next_chapter_navigation" for row in rules["rules"]) == 2
assert rules["empirical_validations"] == a["empirical_validations"] == 0
assert rules["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        row["actual_parental_marriage_harmony_validated"]
        or row["verified_personal_ethics_or_behavior"]
        or row["clinical_or_family_actions_authorized"]
        or row["promoted_to_runtime"]
    )
    for row in rules["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 13
assert sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06a.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06a.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06a.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B06a",
        "path": "batches/B06a/RULES.json",
        "records_count": 29,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly first-edition printed CHAP CXXV/editorial "
            "CXXVI 'Of the mutuall agreement of Parents', body lower "
            "original PDF607/printed573; following printed CXXVI "
            "at PDF608/printed574. Nine original source groups, 27 "
            "substantive historical condition clauses and 2 following "
            "navigation. Sun/Venus aspect or mutual reception by day, "
            "positive Venus applying combustion versus negative "
            "retrograde/peregrine/separating from Sun, Saturn/Moon "
            "friendly aspects versus square/opposition by night, "
            "tenth/fourth-ruler opposition, tenth/fourth malefic "
            "alleged maternal/paternal blame. These are unvalidated "
            "seventeenth-century gender stereotypes and natal methods "
            "with no demonstrated relationship validity or "
            "promoted executable runtime rule."
        ),
    }
)
i["records_count"] = 7502
i["read_numbered_chapters"].append(126)
i["status"] = "BOOK_III_PARENTAL_CONCORD_HISTORICAL_NEXT_NATIVE_PARENT_RELATION_RECTIFICATION"
i["next"] = {
    "pdf_page": 608,
    "printed_page": 574,
    "chapter": "CXXVII",
    "printed_chapter_numeral": "CXXVI",
    "heading": (
        "Of the Parents mutuall love to the Native, and which of his Parents shall best love him"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXVI begins at top original PDF608/printed574. "
        "After parent-child harmony criteria, the same chapter "
        "introduces Regiomontanus Problem 24 reconstruction of "
        "a father's nativity from a son's via solar RA, poles "
        "and house cusp arithmetic. Original pages PDF608 onward "
        "require complete boundary and numerical review before "
        "admission; do not split unnumbered continuation unseen."
    ),
    "research_scope": (
        "Original historic parental affection as separate personal "
        "relationship claims and Regiomontanus astrological "
        "father-birth-time reconstruction. Separate nonvalidated "
        "human prediction claims from reproducible numerical "
        "historical source arithmetic and original reference tables."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXVI_source_acceptance_note"] = (
    "B06a R7474–R7502: 29 first-edition documentary clauses, "
    "27 historical sources and 2 navigation; PDF607–609 original "
    "images hashes and 13 portable integrity tests. No actual "
    "relationship judgments validated or runtime promotions."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7502
assert i["read_numbered_chapters"] == list(range(1, 127))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly parents' mutual agreement: historical source accepted\n\n"
    + review
    + "\n## Historical corpus, not family outcome data\n\n"
    + "After verified publication **7,502 Lilly + 1,066 "
    + "Ptolemy = 8,568 historical documentary annotations**. "
    + "Thirteen focused and portable source tests pass; "
    + "zero empirically verified parental harmony predictions "
    + "and zero executable source rules promoted.\n"
)
PROGRESS.write_text(
    "# Original Lilly study through mutual parental agreement — 2026-10-17\n\n"
    "After authenticated publication **8,568 historical source "
    "annotations** (7,502 Lilly + 1,066 Ptolemy). "
    "Physical original source-body frontier PDF607 of 894 "
    "(**67.9% page position, not empirical program progress**). "
    "Printed CHAP CXXV parent-to-parent agreement adds "
    "29 source-only records with daytime Sun/Venus, night "
    "Saturn/Moon and contradictory ethical stereotypes. "
    "Next CHAP CXXVI parent-to-native love and Regiomontanus "
    "father chart reconstruction starts PDF608. "
    "No independent outcomes or runtime promotions. "
    "Historical astronomical reference numerics and "
    "untouched human tests remain unfinished.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06a.md").read_text()
)
CURRENT.write_text(
    "# First-edition parental-agreement source complete; Regiomontanus method next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06a R7474–R7502 "
    "first-edition source-only locally prepared, after verified "
    "remote publication 7,502 Lilly + 1,066 Ptolemy = 8,568 "
    "historical notes. No real family concord predictions "
    "or runtime rule promotions. NEXT printed CXXVI original "
    "PDF608 containing parent-native affection and "
    "Regiomontanus astronomical geometry.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06a.md").read_text()
)
receipt = {
    "batch": "B06a",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06a.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7502,
    "ptolemy_retained": 1066,
    "combined_if_published": 8568,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
