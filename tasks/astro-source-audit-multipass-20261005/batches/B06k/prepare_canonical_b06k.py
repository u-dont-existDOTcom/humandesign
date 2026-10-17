#!/usr/bin/env python3
"""Guarded original Lilly first-edition source admission of spouse geography."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06k_SPOUSE_ORIGIN.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06k.json"):
    assert not p.exists(), f"Previous or partial archive admission: {p}"
idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert idx["records_count"] == a["prior_lilly"] == 8106
assert idx["read_numbered_chapters"] == list(range(1, 134))
assert idx["batches"][-1]["id"] == "B06j"
assert idx["next"]["chapter"] == "CXXXIV"
assert idx["next"]["printed_chapter_numeral"] == "CXXXIII"
assert idx["next"]["pdf_page"] == 626
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(item["id"] == "B06k" for item in idx["batches"])
assert r["record_count"] == a["new_historical_records"] == 35
assert a["lilly_if_published"] == 8141
assert a["combined_if_published"] == 9207
assert a["numbered_chapters_added"] == 1
assert [x["record_number"] for x in r["rules"]] == list(range(8107, 8142))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8140", "R8141"]
assert w["following_printed_CXXXIIII_heading_frame"] == 627
assert limits["county_vs_country_ambiguity_preserved"]
assert not limits["source_glyph_fully_resolved"]
assert not limits["private_partner_character_or_origin_claims_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_spouse_birthplace_validated"]
        or x["actual_spouse_character_religion_or_wealth_validated"]
        or x["independent_geographical_distance_validated"]
        or x["real_person_spouse_origin_prediction_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 15 and sha(z["archive_path"]) == z["archive_sha256"]

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
previous_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True
).strip()
assert (
    previous_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06k.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06k.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06k.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06k",
        "path": "batches/B06k/RULES.json",
        "records_count": 35,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly first edition 1647 printed CHAP CXXXIII/"
            "editorial CXXXIV On from whence/what Quarter Native shall "
            "have his Wife, original PDF626-627 upper, before CHAP "
            "CXXXIIII on appearance mid PDF627. Six original source "
            "groups, 33 historical substantive annotations and two "
            "following numbered chapter navigation, R8107-R8141. "
            "Marriage indicators in ninth or third or peregrine, "
            "explicit first rule says COUNTY (I say not COUNTRY); "
            "seventh lord ninth or ninth lord seventh alleges "
            "spouse born elsewhere and period religious/rich/"
            "virtuous stereotype with benefic strength qualifier; "
            "Venus as ninth ruler in first or tenth alleges spouse "
            "in another COUNTRY; Sun-plus-uncertain glyph seventh "
            "or Sun third allege stranger wife; source weighs "
            "seventh sign, seventh ruler's sign, Venus/Moon signs "
            "and sky quarters by most testimonies without "
            "quantitative distance or direction metric. "
            "None of these are independently confirmed real "
            "spouse location/wealth/faith/moral predictions; "
            "zero executable scoring rule promotions."
        ),
    }
)
idx["records_count"] = 8141
idx["read_numbered_chapters"].append(134)
idx["status"] = "BOOK_III_SPOUSE_ORIGIN_HISTORICAL_NEXT_APPEARANCE"
idx["next"] = {
    "pdf_page": 627,
    "printed_page": 593,
    "chapter": "CXXXV",
    "printed_chapter_numeral": "CXXXIIII",
    "heading": "What manner of Wife or Wives the Native shall have, if Faire or Deformed",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXXIIII on physical fairness/deformity "
        "starts after independent divider in middle original "
        "PDF627/printed593; its source continues into PDF628+ "
        "and next printed numbered heading must be checked."
    ),
    "research_scope": (
        "Historical gender/appearance classifications using "
        "seventh sign, Venus/Moon, face/body descriptions, "
        "Saturn/Mars historical attractiveness stereotypes, "
        "benefic configurations and original sign-category lists; "
        "these are not evidence of an actual partner's body, "
        "identity, medical condition or beauty."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXIV_source_acceptance_note"] = (
    "B06k R8107–R8141, 35 historical source-only "
    "annotations with explicit COUNTY-not-COUNTRY limitation "
    "contrasted with separate another-Country rule; "
    "unknown solar companion glyph quarantined. "
    "Original PDF626–627 witnesses and 15 archive-replayed "
    "tests, zero real spouse-origin validation or runtime rules."
)
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"]) == 8141
assert idx["read_numbered_chapters"] == list(range(1, 135))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly spouse birthplace versus county/country source accepted\n\n"
    + review
    + "\n## Archival history, not geographical prediction\n\n"
    + "After verified GitHub publication **8,141 Lilly + 1,066 "
    + "Ptolemy = 9,207 historical documentary notes**. "
    + "15 source-photo and archive-extraction integrity "
    + "tests passed; no human spouse identity, geographic "
    + "location or private character forecast validated. "
    + "No runtime source scoring promotion.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 original source through spouse birthplace/origin — 2026-10-17\n\n"
    "After verified publication **9,207 historical documentary "
    "annotations** (8,141 Lilly + 1,066 Ptolemy), physical "
    "first-edition frontier PDF627/894 (**70.1% scanned-page "
    "position only, not empirical/computational completion**). "
    "CXXXIII adds 35 historical spouse-origin annotations, "
    "preserving an explicit COUNTY not COUNTRY restriction "
    "versus another rule alleging foreign COUNTRY and an "
    "unresolved original glyph, plus zodiac/quarter testimony "
    "without geographical metric. No real human predictions "
    "validated and zero promoted scoring rules. Next printed "
    "CXXXIIII spouse appearance begins middle PDF627. "
    "Numerical astrology and untouched human blind tests remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06k.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly spouse county/country source accepted; physical appearance next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06k source "
    "R8107–R8141 guarded canonical prepared. After verified "
    "GitHub push/readback total 8,141 Lilly + 1,066 "
    "Ptolemy = 9,207 historical annotations. "
    "No actual spouse origin, morality or "
    "geographical distances independently validated. "
    "Zero runtime promotions. NEXT printed "
    "CXXXIIII spouse appearance on original PDF627.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06k.md").read_text()
)
receipt = {
    "batch": "B06k",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "previous_git_index_blob": previous_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06k.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8141,
    "ptolemy_retained": 1066,
    "combined_if_published": 9207,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
