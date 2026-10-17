#!/usr/bin/env python3
"""Guarded append-only canonical acceptance for first-edition printed CHAP CIX."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05h_WIT.md"
BACK = B / "recovery"
REC = B / "CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"


def H(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def J(p):
    return json.loads(Path(p).read_text())


for p in (LATEST, BACK / "INDEX_BEFORE_B05h.json", REC):
    assert not p.exists(), f"Already integrated or partial integration, inspect before retry: {p}"
idx = J(IDX)
accepted = J(B / "ACCEPTANCE.json")
rules = J(B / "RULES.json")
z = J(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert idx["records_count"] == accepted["prior_lilly"] == 6591
assert idx["read_numbered_chapters"] == list(range(1, 110))
assert idx["batches"][-1]["id"] == "B05g"
assert idx["next"]["chapter"] == "CX" and idx["next"]["pdf_page"] == 577
assert idx["source_sha256"] == "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(q["id"] == "B05h" for q in idx["batches"])
assert accepted["historical_source_annotations_added"] == rules["record_count"] == 53
assert accepted["lilly_if_published"] == 6644 and accepted["combined_if_published"] == 7710
assert [r["record_number"] for r in rules["rules"]] == list(range(6592, 6645))
assert sum(r["role"] == "next_chapter_navigation" for r in rules["rules"]) == 3
assert rules["empirical_validations"] == rules["runtime_promotions"] == 0
assert H(B / "RULES.json") == accepted["accepted_rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_ok"] and z["per_member_sha256_ok"] and z["full_extraction_ok"]
assert z["extracted_tests_passed"] == 18 and H(z["archive_path"]) == z["archive_sha256"]
rel = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05h.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05h.md").write_bytes(CUR.read_bytes())
(BACK / "PROGRESS_BEFORE_B05h.md").write_bytes(PROGRESS.read_bytes())
idx["batches"].append(
    {
        "id": "B05h",
        "path": "batches/B05h/RULES.json",
        "records_count": 53,
        "sha256": accepted["accepted_rules_sha256"],
        "scope": (
            "Original 1647 first-edition printed CHAP CIX/editorial CX Wit or "
            "Understanding: PDF577-580 "
            "body, PDF581 next heading context; 12 original groups, 50 substantive "
            "historical clauses "
            "and 3 following-navigation items. Mercury-Moon relative strength/aspect "
            "hierarchies, Mercury "
            "motion/position/reception, planetary mixtures and humoral "
            "study-attributions, multiple "
            "contradictory conditional inferences. Original PDF580 folio misprinted 538 "
            "after 545; PDF581 "
            "folio 539, but source/text uninterrupted. Unvalidated intelligence, disability and "
            "moral/personality historical stereotypes must never be treated as human "
            "prediction proof."
        ),
    }
)
idx["records_count"] = 6644
idx["read_numbered_chapters"].append(110)
idx["status"] = "BOOK_III_WIT_UNDERSTANDING_HISTORICAL_DOCUMENTARY_NEXT_STATURE"
idx["next"] = {
    "pdf_page": 580,
    "printed_page": 538,
    "sequential_printed_page_expected": 546,
    "source_printed_pagination_anomaly": True,
    "chapter": "CXI",
    "printed_chapter_numeral": "CX",
    "heading": "Of the Stature, Forme, or shape of the Body",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Following original CHAP CX starts below divider PDF580, page folio visibly 538 "
        "(expected sequential 546) after printed545. Page PDF581 visibly 539, with next "
        "CHAP CXI heading. Preserve actual scan order; do not relabel original image folios."
    ),
    "research_scope": (
        "Historical stature, bodily form and appearance rules; preserve all conditions and "
        "do not treat them as medical, racial, intelligence or forensic evidence."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CX_source_acceptance_note"] = (
    "53 historical source annotations R6592-R6644, 50 substantive CIX clauses and 3 "
    "next-header/opening navigation records, PDF577-581 witnesses, 18 replayed artifact "
    "checks, 12 source groups. No validated actual human intelligence/disability/"
    "moral predictions or runtime promotions."
)
assert idx["records_count"] == sum(z["records_count"] for z in idx["batches"]) == 6644
assert idx["read_numbered_chapters"] == list(range(1, 111))
IDX.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n")
review = (B / "ORIGINAL_SOURCE_FIRST_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# First-edition Lilly understanding/intellect historical documentary accepted\n\n"
    "2026-10-17 — Africa/Dakar UTC+0.\n\n"
    + review
    + "\n## Publication/corpus checkpoint\n\nHistorical-only records **R6592–R6644** "
    "(50 source-claim annotations, 3 navigation). Subject to authenticated publication, "
    "**6,644 Lilly + 1,066 retained Ptolemy = 7,710 documentary annotations**. "
    "Not 7,710 verified predictions. Source-images SHA256-checked, archive "
    "fully extracted and 18 acceptance tests replayed. "
    "No new independently validated intelligence, character, medical, neurological, "
    "or criminal predictions; zero runtime promotions.\n"
)
PROGRESS.write_text(
    "# First-edition Lilly source study through intellect, 2026-10-17\n\n"
    "**7,710 historical source annotations after authenticated publication** (6,644 Lilly "
    "+ 1,066 Ptolemy), first-edition frontier PDF580 of 894 scans (**64.9% positional**). "
    "Printed CHAP CIX on Wit/Understanding source-first preserved, 53 new documentary "
    "units; none independently predictive. Page folios 538 and 539 after printed545 "
    "are apparent 1647 pagination misprints, not missing/reordered pages. Next printed "
    "CHAP CX stature starts original PDF580. Outstanding dense numeric table transcription, "
    "rule implementation, frozen human control tests, and validation unaffected.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05h.md").read_text()
)
CUR.write_text(
    "# Lilly first-edition Wit/Understanding historical source complete; Stature next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. R6592–R6644 historical-only accepted; "
    "6,644 Lilly + 1,066 Ptolemy = 7,710 annotations after verified publication. "
    "Intelligence/study and harmful disability/moral labels remain 1647 stereotypes, "
    "no independent validation. 18 local and portable acceptance tests passed. "
    "Next printed CHAP CX begins original PDF580; original folio visually 538 after 545. "
    "No clinical/cognitive/racial/moral classification promoted into runtime.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05h.md").read_text()
)
rec = {
    "batch": "B05h",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "prior_index_blob_sha1": blob,
    "prior_index_sha256": H(BACK / "INDEX_BEFORE_B05h.json"),
    "updated_index_sha256": H(IDX),
    "latest_review_sha256": H(LATEST),
    "current_sha256": H(CUR),
    "progress_sha256": H(PROGRESS),
    "rules_sha256": H(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6644,
    "ptolemy_retained": 1066,
    "combined_if_published": 7710,
    "original_pdf_frontier": 580,
    "next_original_pdf": 580,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
REC.write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
