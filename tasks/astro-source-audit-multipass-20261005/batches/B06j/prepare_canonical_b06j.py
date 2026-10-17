#!/usr/bin/env python3
"""Guarded append-only historical source admission for competing wife counts."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06j_NUMBER_OF_WIVES.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06j.json"):
    assert not path.exists(), f"Previous or partial archival admission: {path}"

idx = read(INDEX)
accepted = read(B / "ACCEPTANCE.json")
rules = read(B / "RULES.json")
method = read(B / "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
witness = read(B / "ORIGINAL_SOURCE_WITNESS.json")
archive = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")

assert idx["records_count"] == accepted["previous_lilly"] == 8026
assert idx["read_numbered_chapters"] == list(range(1, 133))
assert idx["batches"][-1]["id"] == "B06i"
assert idx["next"]["chapter"] == "CXXXIII"
assert idx["next"]["printed_chapter_numeral"] == "CXXXII"
assert idx["next"]["pdf_page"] == 624
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(item["id"] == "B06j" for item in idx["batches"])
assert rules["record_count"] == accepted["new_historical_annotations"] == 80
assert [r["record_number"] for r in rules["rules"]] == list(range(8027, 8107))
assert [r["id"] for r in rules["rules"] if r["role"] == "next_chapter_navigation"] == [
    "R8105",
    "R8106",
]
assert accepted["lilly_if_published"] == 8106
assert accepted["combined_if_published"] == 9172
assert accepted["numbered_chapters_added"] == 1
assert witness["following_printed_CXXXIII_heading_frame"] == 626
assert rules["substantive_historical"] == 78
assert rules["empirical_validations"] == accepted["empirical_validations"] == 0
assert rules["runtime_promotions"] == accepted["runtime_promotions"] == 0
assert len(method["methods"]) == rules["competing_counting_methods"] == 10
assert method["empirical_validations"] == 0
assert not method["actual_person_partner_claims_authorized"]
assert not limits["private_intimate_or_survival_forecasts_authorized"]
assert not limits["verified_ptolemy_original_comparison"]
assert all(
    not (
        r["independent_legal_spouse_count_validated"]
        or r["independent_nonmarital_partner_count_validated"]
        or r["marital_survival_order_validated"]
        or r["original_ptolemy_text_independently_verified"]
        or r["private_partner_or_sexual_claim_authorized"]
        or r["runtime_model_promoted"]
    )
    for r in rules["rules"]
)
assert sha(B / "RULES.json") == accepted["rules_sha256"] == archive["accepted_rules_sha256"]
assert (
    sha(B / "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json")
    == accepted["competing_methods_sha256"]
)
assert archive["crc_passed"] and archive["sha256_passed"] and archive["extraction_passed"]
assert archive["replayed_tests"] == 25
assert sha(archive["archive_path"]) == archive["archive_sha256"]
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
(BACK / "INDEX_BEFORE_B06j.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06j.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06j.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06j",
        "path": "batches/B06j/RULES.json",
        "records_count": 80,
        "sha256": accepted["rules_sha256"],
        "scope": (
            "William Lilly first-edition printed CHAP CXXXII/editorial CXXXIII "
            "On number of Wives original PDF624 lower through PDF626 upper, "
            "before printed CHAP CXXXIII on wife's origin/quarter. "
            "Eleven image-anchored source groups with 78 substantive "
            "historical claims and two chapter navigation, R8027–R8106. "
            "Ten historically competing counting methods: watery/fecund "
            "vs barren signs, Moon seventh and severe Saturn/Sun exceptions; "
            "one-planet Moon conjunction, spouse death-order strength "
            "allegations, direction-specific applying partile counts "
            "excluding Sun with fruitfulness multiplier, "
            "author-attributed Ptolemy one-form vs bicorporeal signs, "
            "Midheaven-Venus arc eligible-planet count including retro/combust "
            "dignity/reception exceptions; fallback partile aspects to seventh "
            "ruler; Lilly's preferred Moon-sign applying planet count and "
            "fallback; two/three wife combinations with fertile seventh. "
            "Original author explicitly switches from legal wife count "
            "to concubines/sweethearts or wooing and admits no guaranteed "
            "two legal wives; anecdotal never-failed assertion lacks cases. "
            "These are source-only gender/social stereotypes and historic "
            "method descriptions, not independently validated spouse or "
            "mortality forecasts and no promoted runtime rules."
        ),
    }
)
idx["records_count"] = 8106
idx["read_numbered_chapters"].append(133)
idx["status"] = "BOOK_III_HISTORIC_COMPETING_WIFE_COUNTS_NEXT_SPOUSE_ORIGIN"
idx["next"] = {
    "pdf_page": 626,
    "printed_page": 592,
    "chapter": "CXXXIV",
    "printed_chapter_numeral": "CXXXIII",
    "heading": "From whence, or from what Quarter the Native shall have his Wife",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original printed CHAP CXXXIII begins beneath a divider "
        "mid original PDF626/printed592 after CXXXII wife counts, "
        "continues upper original PDF627/printed593 until "
        "separate printed CHAP CXXXIIII on what manner of Wife "
        "fair or deformed starts later PDF627. "
        "Verify source image seam before extraction."
    ),
    "following_printed_chapter_numeral": "CXXXIIII",
    "following_original_pdf_page": 627,
    "research_scope": (
        "Historical alleged birthplace/direction/location of spouse, "
        "ninth/third house signifiers, seventh/ninth ruler exchange, "
        "Venus Moon and house quadrant classification, "
        "qualifying dignities, majority testimony. "
        "No real spouse identity, ethnicity, faith, geographic "
        "location or marital prediction validated."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXIII_source_acceptance_note"] = (
    "B06j R8027–R8106, 80 source-only historical records, "
    "ten contradictory wife-count methods, explicit nonmarital-partner "
    "outcome switching, Ptolemy uncorroborated attribution and author "
    "never-failed anecdote unverified. Original PDF624–627 SHA witnesses, "
    "25 independent extracted ZIP tests, zero human marriage, "
    "survival, legal registration or runtime predictive validity."
)
assert idx["records_count"] == sum(item["records_count"] for item in idx["batches"]) == 8106
assert idx["read_numbered_chapters"] == list(range(1, 134))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly wife-number source historically documented: ten competing methods\n\n"
    + review
    + "\n## Archival but not predictive validity\n\n"
    + "After independently verified publication **8,106 Lilly "
    + "+ 1,066 Ptolemy = 9,172 historical annotations**. "
    + "25 original-source ZIP-extracted tests passed; ten "
    + "contradictory algorithms and legal-versus-concubine "
    + "outcome switching are explicitly preserved. "
    + "No legal spouse count, intimate, mortality, "
    + "or runtime forecast independently validated.\n"
)
PROGRESS.write_text(
    "# Lilly first edition source through historical spouse count — 2026-10-17\n\n"
    "After remote verified publication **9,172 historical source "
    "annotations** (8,106 Lilly + 1,066 Ptolemy), physical "
    "first-edition scan frontier PDF626/894 (**70.0% physical "
    "page-position only, NOT completion of source algorithm "
    "digitization or empirical research**). Printed CXXXII wife "
    "number source adds 80 documentary clauses and ten "
    "incompatible alternative rules; legal wives and "
    "nonmarital female acquaintances cannot be conflated. "
    "Ptolemy source attribution and author private anecdote "
    "not independently verified; zero empirical human "
    "marriage/longevity result and zero runtime promotions. "
    "Next printed CXXXIII on spouse origin/quarter from PDF626 "
    "through upper PDF627. Numeric astronomy and untouched "
    "human matching/decoys remain separate OPEN lanes.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06j.md").read_text()
)
CURRENT.write_text(
    "# Lilly CXXXII historical wife counting source accepted; geographic spouse origin next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06j historical "
    "R8027–R8106 prepared for verified GitHub remote readback; "
    "accepted archive 8,106 Lilly + 1,066 retained "
    "Ptolemy = 9,172 documentary source records. "
    "Ten mutually competing wife/partner counting "
    "methods preserved without treating author "
    "success anecdote as verification. "
    "Zero real people spouse count, private conduct, "
    "spouse mortality or runtime promotions. "
    "NEXT original printed CXXXIII spouse origin PDF626.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06j.md").read_text()
)
receipt = {
    "batch": "B06j",
    "status": "GUARDED_APPEND_ONLY_ORIGINAL_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": prior_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06j.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "competing_methods_sha256": sha(B / "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json"),
    "archive_sha256": archive["archive_sha256"],
    "lilly_if_published": 8106,
    "ptolemy_retained": 1066,
    "combined_if_published": 9172,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
