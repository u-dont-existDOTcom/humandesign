#!/usr/bin/env python3
"""Guarded append-only canonical historical admission of Lilly mature body-build source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05k_BODY_BUILD.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05k.json"):
    assert not p.exists(), f"Possible duplicate or interrupted source admission: {p}"
index = j(IDX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 6733
assert index["read_numbered_chapters"] == list(range(1, 113))
assert index["batches"][-1]["id"] == "B05j"
assert index["next"]["chapter"] == "CXIII" and index["next"]["pdf_page"] == 583
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(row["id"] == "B05k" for row in index["batches"])
assert a["new_records"] == r["record_count"] == 31
assert a["lilly_if_published"] == 6764
assert a["total_historical_if_published"] == 7830
assert [row["record_number"] for row in r["rules"]] == list(range(6734, 6765))
assert r["empirical_validations"] == r["runtime_promotions"] == 0
assert a["empirical_validations"] == a["runtime_promotions"] == 0
assert sha(B / "RULES.json") == a["rules_sha256"] == z["rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["tests_replayed"] == 17 and sha(z["archive_path"]) == z["archive_sha256"]

path_rel = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", path_rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + path_rel], cwd=ROOT, text=True
).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05k.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05k.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05k.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05k",
        "path": "batches/B05k/RULES.json",
        "records_count": 31,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original 1647 printed CHAP CXII/editorial CXIII "
            "Of the grossenesse or leannesse of Bodies, PDF583-584 body and "
            "PDF585 next printed heading. Mature-age (~30+) frame; five "
            "zodiacal sign groups with early/latter part reversals and "
            "late Aquarius exception; Ascendant-sign/planet-dignity "
            "selection, partile aspects, Almuten unoccupied half-sign "
            "fallback, Sun conjunction within orb moiety and absent "
            "Mars, explicit agreement and domicile-over-exaltation "
            "tiebreakers. Historic atypical-body judgment explicitly "
            "declined by author. 29 documentary claims + 2 following "
            "navigation, no independently validated human weight/body "
            "mass/outcome predictions, no runtime promotion."
        ),
    }
)
index["records_count"] = 6764
index["read_numbered_chapters"].append(113)
index["status"] = "BOOK_III_MATURE_BODY_SIZE_HISTORICAL_DOCUMENTARY_NEXT_GENERAL_FORTUNE"
index["next"] = {
    "pdf_page": 585,
    "printed_page_as_seen": 543,
    "chapter": "CXIV",
    "printed_chapter_numeral": "CXIII",
    "heading": "Of the generall Fortune or Misery of the Native",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Separate printed CHAP CXIII starts at the top of first-edition "
        "original frame585, folio printed 543 after prior frame584 "
        "printed 542; original frame586 has printed552. The end of "
        "the general fortune chapter and the unnumbered following "
        "second-house riches section require independent boundary review."
    ),
    "research_scope": (
        "Historical whole-chart fortune/misfortune testimonies, "
        "strength/debility qualifications, timing by directions, "
        "conditional counterexamples. Do not treat biography fitted "
        "after reading a chart as independently valid prediction."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXIII_source_acceptance_note"] = (
    "R6734-R6764, 31 historical source clauses: 29 body-size "
    "and conditional qualifications, 2 next chapter navigation. "
    "13 original source image groups, original frames583-586 SHA-locked. "
    "No independently measured weight, anatomy, health or ancestry "
    "predictions; no runnable runtime scoring promotion."
)
assert index["records_count"] == sum(row["records_count"] for row in index["batches"]) == 6764
assert index["read_numbered_chapters"] == list(range(1, 114))
IDX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original first-edition Lilly body-size: documentary accepted only\n\n"
    + review
    + "\n## Accepted historical corpus\n\n"
    + "**R6734–R6764** added as original first-edition source notes. "
    + "After authenticated publication: **6,764 Lilly + 1,066 "
    + "Ptolemy = 7,830 historical/documentary annotations**. "
    + "Not real-person measurements or successful predictive rules. "
    + "No independent source-lane human, metabolic, medical or "
    + "anthropometric validation and no executable runtime promotion.\n"
)
PROGRESS.write_text(
    "# Lilly source study after mature body-build, 2026-10-17\n\n"
    "7,830 historical/documentary source units after publication "
    "(6,764 Lilly + 1,066 Ptolemy), through first-edition frame584 "
    "of 894 scans, **65.3% scanned-position proxy only**. 31 source "
    "annotations from printed CHAP CXII, two next-heading witnesses, "
    "explicit age-after-thirty and mutually qualified planetary "
    "conditions retained. No actual human body mass, medical or "
    "prospective results validated. Next printed CHAP CXIII "
    "General Fortune/Misery begins original PDF585. Numeric tables, "
    "historical astrology coding and blind empirical tests remain "
    "open.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B05k.md").read_text()
)
CURRENT.write_text(
    "# Source-first Lilly original mature-body-build historic chapter complete\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Local R6734–R6764 "
    "historical source acceptance: 6,764 Lilly + 1,066 Ptolemy "
    "= 7,830 after remote readback. 29 substantive clauses, 2 "
    "following chapter navigation; no independent person height/weight, "
    "clinical or predictive validity and no runtime promotions. "
    "First-edition PDF584 completes printed CHAP CXII. Next printed "
    "CXIII General Fortune begins PDF585, no actual source annotations "
    "admitted for it.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B05k.md").read_text()
)
receipt = {
    "batch": "B05k",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_git_blob": old_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05k.json"),
    "new_index_sha256": sha(IDX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6764,
    "ptolemy_retained": 1066,
    "combined_if_published": 7830,
    "new_empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
