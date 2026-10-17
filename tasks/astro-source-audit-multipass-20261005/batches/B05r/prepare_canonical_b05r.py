#!/usr/bin/env python3
"""Append-only canonical admission for Lilly unnumbered kinship introduction."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05r_KINRED_INTRO.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05r.json"):
    assert not p.exists(), f"Previously or partially accepted: {p}"
index = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 7126
assert index["read_numbered_chapters"] == list(range(1, 119))
assert index["batches"][-1]["id"] == "B05q"
assert index["next"]["chapter"] == "UNNUMBERED_THIRD_HOUSE_KINRED"
assert index["next"]["pdf_page"] == 598
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B05r" for x in index["batches"])
assert r["record_count"] == a["new_source_records"] == 12
assert a["lilly_if_published"] == 7138 and a["combined_if_published"] == 8204
assert [x["record_number"] for x in r["rules"]] == list(range(7127, 7139))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert sha(B / "RULES.json") == a["source_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 10 and sha(z["archive_path"]) == z["archive_sha256"]
assert all(
    not (
        x["validated_actual_sibling_number"]
        or x["validated_sibling_relationship_quality"]
        or x["promoted_to_runtime_model"]
    )
    for x in r["rules"]
)
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05r.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05r.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05r.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05r",
        "path": "batches/B05r/RULES.json",
        "records_count": 12,
        "sha256": a["source_sha256"],
        "scope": (
            "Original first edition Lilly unnumbered third-house "
            "introduction 'Judgments upon the third House — Of Kinred, "
            "Brethren and Sisters', original PDF598/printed564. "
            "Five source-passage groups, 10 historical introduction "
            "claims plus two following printed CXVIII navigation. "
            "Preference for first-born nativity to assess subsequently "
            "born siblings; fallback when firstborn chart is unavailable; "
            "three future questions: existence, condition, amity/concord. "
            "No independent sibling-count or sibling-relationship evidence, "
            "no runtime source-rule promotion."
        ),
    }
)
index["records_count"] = 7138
# UNNUMBERED section: do not advance numbered-chapter index!
assert index["read_numbered_chapters"] == list(range(1, 119))
index["status"] = "BOOK_III_UNNUMBERED_THIRD_HOUSE_SOURCE_NEXT_NUMBERED_SIBLINGS"
index["next"] = {
    "pdf_page": 598,
    "printed_page": 564,
    "chapter": "CXIX",
    "printed_chapter_numeral": "CXVIII",
    "heading": "If have Brethren or Sisters",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original first edition printed CHAP CXVIII begins lower "
        "PDF598/printed564 after separate divider below the "
        "unnumbered third-house introduction. Continues on "
        "PDF599/565, with additional sign-category descriptions "
        "PDF600/566. Following printed CXIX opens lower PDF600."
    ),
    "following_printed_chapter_numeral": "CXIX",
    "following_original_pdf_page": 600,
    "research_scope": (
        "Historical sibling presence, number and classification "
        "rules, third house ruler, intercepted planets, Mars, Moon, "
        "fruitful/barren planets and signs, aspect hierarchy. "
        "No evidence of human family-size prediction accuracy."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["unnumbered_third_house_source_acceptance_note"] = (
    "R7127–R7138: 12 historic documentary annotations, "
    "10 substantive introduction clauses and 2 next-heading "
    "navigation. Original PDF598–600 JPEG witnesses, "
    "10 archive-replayed tests and no validated family outcome."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7138
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly unnumbered third-house kinship intro accepted\n\n"
    + review
    + "\n## Source-only acceptance\n\n"
    + "After verified publication **7,138 Lilly + 1,066 "
    + "Ptolemy = 8,204 historical annotations**. "
    + "This is source text, not a prediction of actual people "
    + "or a validated siblings survey; zero source-lane "
    + "empirical results and runtime promotions.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 study through kinship introduction — 2026-10-17\n\n"
    "8,204 historical source notes after verified remote acceptance "
    "(7,138 Lilly + 1,066 Ptolemy); source-body position "
    "PDF598/894 **~66.9% scanned-page proxy only**. "
    "Unnumbered third-house firstborn chart prerequisite, "
    "fallback and three sibling questions preserved with 12 "
    "historical annotations, 10 source tests. Next printed "
    "CHAP CXVIII begins lower on PDF598. No human family-size "
    "validation, ephemeris table completion or model promotion.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05r.md").read_text()
)
CURRENT.write_text(
    "# Lilly original kinship intro historical source accepted, sibling chapter next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05r R7127–R7138 "
    "accepted as original historic source: 7,138 Lilly plus "
    "1,066 Ptolemy = 8,204 notes after GitHub readback. "
    "Unnumbered intro does not increment printed-chapter count; "
    "no predictive validation. Next printed CXVIII begins "
    "original PDF598.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B05r.md").read_text()
)
receipt = {
    "batch": "B05r",
    "status": "CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_blob": old_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05r.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7138,
    "ptolemy_retained": 1066,
    "combined_if_published": 8204,
    "numbered_chapters_added": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
