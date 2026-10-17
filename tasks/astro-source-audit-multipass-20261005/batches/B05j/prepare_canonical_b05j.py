#!/usr/bin/env python3
"""Guarded append-only historical documentation acceptance for Lilly CXI."""

import hashlib
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05j_FACE_HAIR.md"
BACKUP = BASE / "recovery"
RECEIPT = BASE / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACKUP / "INDEX_BEFORE_B05j.json"):
    assert not path.exists(), f"Existing or partial source-index update: {path}"

index = load(INDEX)
accept = load(BASE / "ACCEPTANCE.json")
rules = load(BASE / "RULES.json")
release = load(BASE / "SOURCE_RELEASE_RECEIPT_20261017.json")
source_window = load(BASE / "SOURCE_WINDOW_20261017.json")

assert index["records_count"] == accept["previous_lilly"] == 6671
assert index["read_numbered_chapters"] == list(range(1, 112))
assert index["batches"][-1]["id"] == "B05i"
assert index["next"]["chapter"] == "CXII"
assert index["next"]["pdf_page"] == 581
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert source_window["baseline_accepted_lilly"] == 6671
assert source_window["admission"]["historical_records_added"] == 0
assert not any(row["id"] == "B05j" for row in index["batches"])
assert rules["record_count"] == accept["new_historical_records"] == 62
assert [row["record_number"] for row in rules["rules"]] == list(range(6672, 6734))
assert sum(row["role"] == "next_chapter_navigation" for row in rules["rules"]) == 2
assert accept["lilly_if_published"] == 6733
assert accept["historical_corpus_if_published"] == 7799
assert digest(BASE / "RULES.json") == accept["records_sha256"]
assert release["accepted_rules_sha256"] == accept["records_sha256"]
assert digest(release["archive_path"]) == release["archive_sha256"]
assert release["crc_passed"] and release["per_member_sha256_passed"]
assert release["full_extraction_passed"] and release["replayed_tests"] == 23
assert accept["empirical_validations"] == accept["runtime_promotions"] == 0
assert rules["empirical_validations"] == rules["runtime_promotions"] == 0
assert all(
    not (
        r["independent_human_biometric_validation"]
        or r["validated_ancestry_or_ethnicity_prediction"]
        or r["validated_medical_or_disability_prediction"]
        or r["runtime_model_promoted"]
    )
    for r in rules["rules"]
)
index_rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", index_rel], cwd=ROOT).returncode == 0
old_git_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + index_rel], cwd=ROOT, text=True
).strip()
assert (
    old_git_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)

BACKUP.mkdir(exist_ok=True)
(BACKUP / "INDEX_BEFORE_B05j.json").write_bytes(INDEX.read_bytes())
(BACKUP / "CURRENT_BEFORE_B05j.md").write_bytes(CURRENT.read_bytes())
(BACKUP / "PROGRESS_BEFORE_B05j.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05j",
        "path": "batches/B05j/RULES.json",
        "records_count": 62,
        "sha256": accept["records_sha256"],
        "scope": (
            "William Lilly original first-edition printed CHAP CXI/editorial CXII "
            "Nature of Signs, Colour of Face and Hair. Source PDF581-583 body, PDF583 "
            "next printed CHAP CXII start, later context PDF584-586. 60 selective "
            "source-faithful historical clauses and two next chapter navigation records; "
            "11 source groups. Five zodiac stature categories, six complexion source "
            "classes, four humours, seasonal complexion and hair, planets, fixed stars "
            "and sign/Ascendant ruler fallback. Explicit climate/country exception "
            "given by the author, majority/mixing discretion, earlier-Book-I cross-refs "
            "and stigmatizing historic disability/appearance characterizations "
            "preserved without human verification. Ambiguous glyphs held unresolved; "
            "not promoted to any biometric, medical or ancestry model."
        ),
    }
)
index["records_count"] = 6733
index["read_numbered_chapters"].append(112)
index["status"] = "BOOK_III_FACE_HAIR_HISTORIC_DOCUMENTARY_NEXT_BODY_BULK_LEANNESS"
index["next"] = {
    "pdf_page": 583,
    "printed_page_as_seen": 549,
    "chapter": "CXIII",
    "printed_chapter_numeral": "CXII",
    "heading": "Of the grossenesse or leannesse of Bodies",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "First-edition printed CHAP CXII starts beneath horizontal divider "
        "on original PDF frame583, printed folio549. Continues frame584 "
        "with printed folio542 (typographical page-number regression). "
        "Next printed CHAP CXIII begins PDF585, printed folio543, "
        "despite continuous scan/text order."
    ),
    "research_scope": (
        "Age-specific historical corpulence/leanness rules, first-edition "
        "conditions, qualifications and methods. Distinguish source annotations "
        "from validated weight or medical predictions."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXII_source_acceptance_note"] = (
    "R6672-R6733, 62 historical documentary annotations: 60 source clauses, "
    "2 next-heading navigation; 11 original-source groups, 6 witness images. "
    "No independently measured facial, hair, complexion, stature, ancestry, "
    "medical or human biometric predictions validated, no runtime promotions."
)
assert index["records_count"] == sum(row["records_count"] for row in index["batches"]) == 6733
assert index["read_numbered_chapters"] == list(range(1, 113))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (BASE / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first-edition Signs/Face/Hair: historic source accepted\n\n"
    + review
    + "\n## Corpus and scientific evidence distinction\n\n"
    + "Documentary records **R6672–R6733** are accepted as descriptions "
    + "of the 1647 source, not confirmed human predictions. Following "
    + "authenticated remote publication: **6,733 Lilly + 1,066 "
    + "Ptolemy = 7,799 documentary records**. All 23 source-focused "
    + "tests replayed from the portable archive, including original "
    + "image hashes. There are zero new independent human, biometric, "
    + "ancestry or medical validations and zero runtime scoring promotions.\n"
)
PROGRESS.write_text(
    "# First-edition Lilly historic source frontier through Face/Hair — 2026-10-17\n\n"
    "**7,799 historical source annotations** after verified publication "
    "(6,733 Lilly + 1,066 Ptolemy). Original 1647 volume source frontier "
    "PDF583/894 (~65.2% of physical scan position only). Printed CHAP CXI "
    "Face/Hair/Sign dispositions preserved with 62 historical annotations, "
    "including explicit country/climate override and uncertain glyphs. "
    "Next printed CHAP CXII begins mid-PDF583, mature-age bulk/leanness. "
    "Original folio misprints do not represent missing pages. No independent "
    "height, complexion, hair or disability predictions were validated. "
    "Numerical tables, runtime rules, strong non-astrological controls and "
    "prospective human tests remain open.\n\n---\n\n"
    + (BACKUP / "PROGRESS_BEFORE_B05j.md").read_text()
)
CURRENT.write_text(
    "# Lilly first-edition Face/Hair source documented; mature body composition next\n\n"
    "2026-10-17 Africa/Dakar UTC+0: accepted locally R6672–R6733, "
    "60 historical source annotations plus 2 next-chapter navigation. "
    "After verified publication: 6,733 Lilly + 1,066 Ptolemy = 7,799. "
    "Explicit climate and country exception, discretionary testimony mixing, "
    "unverified sign glyphs and period stereotypes remain qualified. "
    "Zero independently validated human outcomes and zero runtime promotions. "
    "Next printed CXII starts original PDF583, body bulk/leanness "
    "at full age.\n\n---\n\n" + (BACKUP / "CURRENT_BEFORE_B05j.md").read_text()
)
receipt = {
    "batch": "B05j",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_git_blob": old_git_blob,
    "old_index_sha256": digest(BACKUP / "INDEX_BEFORE_B05j.json"),
    "new_index_sha256": digest(INDEX),
    "latest_sha256": digest(LATEST),
    "progress_sha256": digest(PROGRESS),
    "current_sha256": digest(CURRENT),
    "rules_sha256": digest(BASE / "RULES.json"),
    "archive_sha256": release["archive_sha256"],
    "lilly_if_published": 6733,
    "ptolemy_retained": 1066,
    "combined_if_published": 7799,
    "next_original_pdf_frame": 583,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
