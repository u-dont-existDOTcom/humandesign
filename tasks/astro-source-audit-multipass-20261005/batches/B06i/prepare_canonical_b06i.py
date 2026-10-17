#!/usr/bin/env python3
"""Guarded original Lilly CXXXI marriage directions historical-source accession."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06i_MARRIAGE_TIME.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06i.json"):
    assert not p.exists(), f"Previous or interrupted source admission: {p}"

idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
method = j(B / "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
witness = j(B / "ORIGINAL_SOURCE_WITNESS.json")

assert idx["records_count"] == a["prior_lilly"] == 7943
assert idx["read_numbered_chapters"] == list(range(1, 132))
assert idx["batches"][-1]["id"] == "B06h"
assert idx["next"]["chapter"] == "CXXXII"
assert idx["next"]["printed_chapter_numeral"] == "CXXXI"
assert idx["next"]["pdf_page"] == 623
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06i" for x in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 83
assert a["lilly_if_published"] == 8026
assert a["combined_if_published"] == 9092
assert [x["record_number"] for x in r["rules"]] == list(range(7944, 8027))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8025", "R8026"]
assert a["numbered_chapters_added"] == 1
assert witness["marriage_time_heading_within_CXXXI"]
assert witness["next_printed_CXXXII_heading_frame"] == 624
assert not method["empirical_status"]["dates_predicted"]
assert not method["empirical_status"]["age_years_computed"]
assert not r["direction_algorithm_complete"]
assert not limits["historic_primary_directions_executable"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_marriage_difficulty_validated"]
        or x["independent_marriage_calendar_date_validated"]
        or x["actual_partner_age_or_personal_behavior_validated"]
        or x["source_direction_computation_executable"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert (
    sha(B / "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json") == a["marriage_method_sha256"]
)
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 25 and sha(z["archive_path"]) == z["archive_sha256"]

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06i.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06i.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06i.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06i",
        "path": "batches/B06i/RULES.json",
        "records_count": 83,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 printed CHAP CXXXI/editorial "
            "CXXXII on how easily native obtains a wife, "
            "and internal The time of Marriage subsection, "
            "original PDF623 mid to PDF624 mid/upper. "
            "Next separately printed CXXXII number of wives "
            "starts lower PDF624. 11 original source passage "
            "groups, 81 substantive historic clauses and "
            "two next heading navigation R7944–R8026. "
            "Fortunate/weak-majority marriage difficulty, "
            "Venus-Mars missing aspect, four alternative "
            "retrospective author anecdotes, sudden wedding "
            "vs moral claims; Moon oriental of Sun and "
            "house east/west sector age or spouse-age "
            "alternatives, direct/swift vs retrograde/"
            "slow/stationary delay, discrepancies weighted "
            "to Moon, and primary directions of seventh "
            "degree/ruler Moon/Venus/MC/Sun to natal "
            "and benefic aspects with historical terms "
            "caveat. Separate 14-step non-executable "
            "direction specification preserved in "
            "batches/B06i/MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json. "
            "No verified marriage age/event forecasts "
            "or promoted source algorithm."
        ),
    }
)
idx["records_count"] = 8026
idx["read_numbered_chapters"].append(132)
idx["status"] = "BOOK_III_HISTORIC_MARRIAGE_EASE_AND_DIRECTIONS_NEXT_NUMBER_OF_WIVES"
idx["next"] = {
    "pdf_page": 624,
    "printed_page": 590,
    "chapter": "CXXXIII",
    "printed_chapter_numeral": "CXXXII",
    "heading": "Of the number of Wives",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXXII starts below a divider "
        "in lower original PDF624/printed590, "
        "continues PDF625/printed591 through "
        "upper original PDF626/printed592. "
        "Next printed CHAP CXXXIII, on where or "
        "from which quarter Wife comes, begins "
        "under separate divider PDF626."
    ),
    "research_scope": (
        "Historical number of marriages/wives "
        "from watery fruitful and barren signs, "
        "Moon seventh house, planets applying "
        "partile to Moon, planet-strength relative "
        "lifespan hypotheses, Ptolemy attribution, "
        "Sun beams and alternative Midheaven "
        "to Venus methods. Distinguish partners, "
        "legally married spouses and extramarital "
        "affairs; author anecdotes not validation."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXII_source_acceptance_note"] = (
    "B06i R7944–R8026: 83 historical source "
    "notes, 14-step source mathematical-direction "
    "template frozen NONEXECUTABLE. Original "
    "frames PDF623-627 SHA checks and 25 "
    "archived/extracted documentary tests pass, "
    "no calendar or prospective marriage predictions "
    "or runtime promotions."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8026
assert idx["read_numbered_chapters"] == list(range(1, 133))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original 1647 Lilly CXXXI marriage ease and time documented\n\n"
    + review
    + "\n## Documentary source only, no prospective marriage dates\n\n"
    + "After authenticated GitHub publication **8,026 Lilly "
    + "+ 1,066 Ptolemy = 9,092 historical annotations**. "
    + "Twenty-five ZIP replayed source tests pass. "
    + "Directions template has 14 steps but is "
    + "non-executable without exact astronomical "
    + "algorithms and calendar mapping. No human "
    + "marriage forecast or scoring promotion.\n"
)
PROGRESS.write_text(
    "# Lilly historical source through marriage time directions — 2026-10-17\n\n"
    "After authenticated publication **9,092 historical "
    "annotations** (8,026 Lilly + 1,066 Ptolemy); "
    "physical source frontier PDF624/894 (**69.8% "
    "by original scanned position, not entire science "
    "completion**). Printed CXXXI ease and time "
    "of marriage adds 83 source annotations and "
    "non-executable 14-step primary-directions "
    "specification. No exact historic direction/"
    "arc-to-calendar calculation implemented; no "
    "independent marriage date prediction validated. "
    "Next printed CXXXII number of wives lower "
    "PDF624 through upper PDF626. Numeric "
    "astronomy/Regiomontanus and blind participant "
    "studies remain OPEN.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06i.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly marriage ease/time documentary complete; number of wives next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06i "
    "historical R7944–R8026 admitted locally; "
    "after remote GitHub readback 8,026 Lilly "
    "+ 1,066 Ptolemy = 9,092 historical notes. "
    "Historical primary directions are structurally "
    "retained but no complete clock-year algorithm, "
    "no real marriage timing accuracy and no "
    "runtime scoring rules. NEXT printed CHAP "
    "CXXXII number of Wives source PDF624-626.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06i.md").read_text()
)
receipt = {
    "batch": "B06i",
    "status": "GUARDED_CANONICAL_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06i.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "method_sha256": sha(B / "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8026,
    "ptolemy_retained": 1066,
    "combined_if_published": 9092,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
