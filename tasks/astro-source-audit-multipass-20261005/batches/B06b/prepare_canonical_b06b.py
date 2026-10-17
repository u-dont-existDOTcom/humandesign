#!/usr/bin/env python3
"""Guarded historical source accession for original Lilly Regiomontanus text."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06b_PARENT_NATIVE_REGIOMONTANUS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(p):
    return json.loads(Path(p).read_text())


def h(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06b.json"):
    assert not p.exists(), f"Duplicate or partial historical source admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
proc = j(B / "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json")
assert i["records_count"] == a["previous_lilly"] == 7502
assert i["read_numbered_chapters"] == list(range(1, 127))
assert i["batches"][-1]["id"] == "B06a"
assert i["next"]["chapter"] == "CXXVII"
assert i["next"]["printed_chapter_numeral"] == "CXXVI"
assert i["next"]["pdf_page"] == 608
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06b" for x in i["batches"])
assert a["new_historical_records"] == r["record_count"] == 46
assert a["lilly_if_published"] == 7548
assert a["combined_if_published"] == 8614
assert [x["record_number"] for x in r["rules"]] == list(range(7503, 7549))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert not r["regiomontanus_procedure_executable"]
assert not proc["attributions_verified_against_original_regiomontanus"]
assert proc["procedure_status"] == "SOURCE_RECONSTRUCTION_ONLY_NON_EXECUTABLE"
assert all(
    not (
        x["independent_human_parental_affection_validated"]
        or x["independent_father_birth_time_recovery_validated"]
        or x["regiomontanus_original_independently_verified"]
        or x["runtime_algorithm_promoted"]
    )
    for x in r["rules"]
)
assert h(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert h(B / "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json") == a["regiomontanus_source_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 18 and h(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06b.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06b.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06b.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B06b",
        "path": "batches/B06b/RULES.json",
        "records_count": 46,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 printed CHAP CXXVI/editorial CXXVII "
            "Of the Parents mutual love to Native and which parent "
            "shall best love him, original PDF608-609, next separate "
            "mines CHAP CXXVII later PDF609 and unnumbered Sixth "
            "House PDF610. Ten original page source groups, 44 "
            "substantive annotations and 2 following navigation. "
            "Parent-child friendly versus hostile first lord/ascendant "
            "aspects, Moon/Venus asymmetric favor vs Sun/Saturn "
            "and reception, then Regiomontanus Problem 24 historical "
            "father-nativity extraction: day nativity, Sun not on "
            "MC/IC, Sun positional circle/pole, proposed father "
            "Ascendant at Sun longitude, MC RA = Sun pole OA -90 degrees, "
            "Regiomontanus house poles, 30-degree RA increment and "
            "inverse oblique ascent to ecliptic cusps 11/12/2/3. "
            "Structured incomplete historical procedure in "
            "batches/B06b/REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json. "
            "No independently reconstructed actual father birth, "
            "no validated family affection or promoted runtime rules."
        ),
    }
)
i["records_count"] = 7548
i["read_numbered_chapters"].append(127)
i["status"] = "BOOK_III_PARENT_CHILD_REGIOMONTANUS_DOCUMENTARY_NEXT_MINES"
i["next"] = {
    "pdf_page": 609,
    "printed_page": 575,
    "chapter": "CXXVIII",
    "printed_chapter_numeral": "CXXVII",
    "heading": "Of the significations in a Nativity, of great Fortune to be obtained out of Mines",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXVII on mines begins after divider "
        "upper/middle original PDF609/printed575 and concludes "
        "before decorated unnumbered Sixth House heading "
        "at PDF610/printed576. Source window must verify "
        "precise seam and all mining-material alternatives."
    ),
    "following_unnumbered_section": "THE_SIXT_HOUSE_INFIRMITIES",
    "following_section_pdf_page": 610,
    "research_scope": (
        "Historical mineral/coal/lead/silver/gold mining "
        "economic fortune configurations through Saturn/Jupiter, "
        "fourth lord and luminous reception, essential dignities, "
        "planet speed/directness, no actual mining/property "
        "predictive data."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXVII_source_acceptance_note"] = (
    "B06b R7503-R7548 historical source-only records (44 "
    "substantive, 2 next chapter navigation), Regiomontanus "
    "12-step incomplete non-executable geometry, 18 standalone "
    "source tests and original 608-611 SHA images. Zero "
    "father chart birth-time recoveries and runtime promotions."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7548
assert i["read_numbered_chapters"] == list(range(1, 128))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first-edition Regiomontanus parent nativity method documented\n\n"
    + review
    + "\n## Historical procedural source, not real birth-time recovery\n\n"
    + "After remote verification **7,548 Lilly + 1,066 "
    + "Ptolemy = 8,614 historical documentary records**. "
    + "18 source integrity/portable archive checks passed. "
    + "Historic math source recipe is incomplete and "
    + "non-executable, no natal father time recovered, "
    + "zero empirical validation and runtime promotions.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 historical study through Regiomontanus father figure — 2026-10-17\n\n"
    "After authenticated publication the archive contains "
    "**8,614 historical source annotations** (7,548 Lilly + "
    "1,066 Ptolemy); original first-edition source frontier "
    "PDF609 of 894 (**68.1% by physical page only**, NOT "
    "program/empirical completion). Printed CHAP CXXVI "
    "parent-native affection plus Regiomontanus attributed "
    "father chart construction: 46 source annotations and "
    "a separate frozen, structurally tested, incomplete "
    "12-step mathematical-source template. Original "
    "Problem 24 and house-pole tables remain unverified; "
    "no actual father birth-time recoveries, natal relationship "
    "predictions or promoted models. Next printed CXXVII "
    "mines on PDF609, unnumbered sixth-house medical source "
    "begins PDF610. Numerical references and blind human "
    "research separate/open.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06b.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly parent-native/Regiomontanus historical source accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06b source "
    "R7503–R7548 guarded index prepared; after remote "
    "verification 7,548 Lilly + 1,066 Ptolemy = 8,614 "
    "historical documentary notes. The historical 90-/30-degree "
    "Regiomontanus procedure is preserved but non-executable "
    "until missing pole/table and mathematical parity checked. "
    "No actual father birth-time recovery. NEXT printed CXXVII "
    "mineral/coal mines first-edition PDF609.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06b.md").read_text()
)
receipt = {
    "batch": "B06b",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": h(BACK / "INDEX_BEFORE_B06b.json"),
    "new_index_sha256": h(INDEX),
    "latest_sha256": h(LATEST),
    "progress_sha256": h(PROGRESS),
    "current_sha256": h(CURRENT),
    "rules_sha256": h(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "historical_procedure_sha256": h(B / "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json"),
    "lilly_if_published": 7548,
    "ptolemy_retained": 1066,
    "combined_if_published": 8614,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
