#!/usr/bin/env python3
"""Guarded append-only original Lilly travel yes/no and directions source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06s_TRAVEL_DIRECTION.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06s.json"):
    assert not path.exists(), f"Duplicate or interrupted source acceptance: {path}"
idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = j(B / "SOURCE_TO_RECORD_MAP.json")
method = j(B / "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
chinese = j(CHINESE)

assert idx["records_count"] == a["previous_lilly"] == 8705
assert idx["read_numbered_chapters"] == list(range(1, 140))
assert idx["batches"][-1]["id"] == "B06r"
assert idx["next"]["chapter"] == "CXL"
assert idx["next"]["printed_chapter_numeral"] == "CXXXIX"
assert idx["next"]["pdf_page"] == 640
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(row["id"] == "B06s" for row in idx["batches"])
assert a["new_historical_annotations"] == r["record_count"] == 101
assert a["lilly_if_published"] == 8806
assert a["combined_if_published"] == 9872
assert a["numbered_chapters_added"] == 1
assert [x["record_number"] for x in r["rules"]] == list(range(8706, 8807))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8805", "R8806"]
assert r["substantive"] == a["substantive"] == 99
assert len(mapdata["groups"]) == mapdata["source_group_count"] == 11
assert w["body_original_pdf_frames"] == [640, 641, 642]
assert w["following_printed_CXL_heading_pdf"] == 643
assert len(method["source_methods"]) == r["travel_direction_methods"] == 7
assert not limits["original_ptolemy_travel_source_collated"]
assert not limits["complete_travel_direction_engine"]
assert not limits["person_geography_profit_faith_or_life_risk_predictions_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert method["human_travel_predictions_verified"] == method["runtime_promotions"] == 0
assert all(
    not (
        x["independent_travel_occurrence_frequency_validated"]
        or x["independent_travel_destination_geography_validated"]
        or x["independent_travel_duration_profit_or_mode_validated"]
        or x["independent_travel_life_hazard_validated"]
        or x["real_person_travel_wealth_or_religion_inference_authorized"]
        or x["source_math_directed_compass_executable"]
        or x["original_ptolemy_source_collated"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json") == a["direction_method_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
assert chinese["independently_validated_real_human_claims"] == 0
assert chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06s.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06s.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06s.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06s",
        "path": "batches/B06s/RULES.json",
        "records_count": 101,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original first-edition William Lilly printed CHAP CXXXIX/"
            "editorial CXL Whether Native shall travel or not "
            "PDF640 lower through PDF642/printed606-608; "
            "new separately printed CHAP CXL Cause of Travels "
            "begins PDF643. 11 original source groups, "
            "99 historic substantive clauses and two following "
            "numbered heading navigation R8706–R8806. "
            "Travel occurrence from Moon/Mercury and reciprocal "
            "house/planet receptions/aspects, first/ninth lord "
            "exchanges, solar contacts, movable signs, "
            "travel frequency/propensity and duration/economic "
            "outcomes kept distinct. Seven non-executable "
            "competing travel direction/mode source methods "
            "stored in TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json: "
            "Sun/Saturn East Venus South Jupiter North Mars/Moon "
            "West, Mercury source-dependent/possibly null; "
            "triplicities Fire East Air West Earth South Water North; "
            "author-attributed Ptolemy luminaries 10/11/12/1/2/3 "
            "oriental East/Southeast vs 9/8/7/6/5/4 occidental "
            "West/North; source Mars/Moon latitude North/South; "
            "unweighted majority; land/water/horse/coach/foot "
            "historic transport and mutable/fixed economic "
            "effects. Original conflicting source methods "
            "retain ambiguity; no real journeys/geography/safety "
            "success and zero promoted runtime source rules."
        ),
    }
)
idx["records_count"] = 8806
idx["read_numbered_chapters"].append(140)
idx["status"] = "BOOK_III_CXXXIX_HISTORIC_TRAVEL_DIRECTION_NEXT_CXL_CAUSES"
idx["next"] = {
    "pdf_page": 643,
    "printed_page": 609,
    "chapter": "CXLI",
    "printed_chapter_numeral": "CXL",
    "heading": "Cause of Travels",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Distinct printed CHAP CXL Cause of Travels begins "
        "original first-edition PDF643/printed609 at upper "
        "page, after original CXXXIX Land/Water mode "
        "passage finishes PDF642. It contains source "
        "travel motive claims and an internal Haly aphorisms "
        "heading near PDF643 bottom and continues PDF644+. "
        "Verify exact next printed chapter heading before "
        "complete substantive archival extraction."
    ),
    "research_scope": (
        "Planet and house significators of travel motives "
        "and source historical Saturn-like mines/estate "
        "versus Jupiter religion/honour/law, ninth lord "
        "in first/second/third and Haly-attributed "
        "house-by-house travel outcomes, financial "
        "profit, hazards and religious or social "
        "stereotypes. Source only, no actual "
        "predictive person's motives or faith."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXL_source_acceptance_note"] = (
    "B06s R8706–R8806, 101 first-edition original "
    "historic source items, 11 bidirectional groups, "
    "photo PDF640–643 hash/bytes, 26 independently "
    "extracted ZIP source tests, seven competing "
    "non-executable direction/mode systems "
    "and explicit Ptolemy methodological disagreement. "
    "Zero human travel accuracy or runtime rules; "
    "Chinese 72 source notes separate."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8806
assert idx["read_numbered_chapters"] == list(range(1, 141))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original CXXXIX travel occurrence, compass and modes documented\n\n"
    + review
    + "\n## Historical source only, not empirically predictive travel model\n\n"
    + "After verified GitHub publication **8,806 Lilly + "
    + "1,066 Ptolemy = 9,872 historical documentary notes**. "
    + "26 first-edition photo/ZIP replayed tests pass. "
    + "Seven incompatible historical travel-direction "
    + "sources preserved without selecting retrospectively. "
    + "No human travel, location, income, dangerous journey "
    + "forecast validated and zero source runtime promotions.\n"
)
PROGRESS.write_text(
    "# Lilly original 1647 through historic travel direction and mode — 2026-10-17\n\n"
    "After verified publication **9,872 historical "
    "records** (8,806 Lilly + 1,066 Ptolemy), "
    "physical first-edition scan frontier PDF643/894 "
    "(**71.9% physical page position ONLY, not project "
    "scientific completion**). Printed CXXXIX added "
    "101 original source historic claims including "
    "seven incompatible/overlapping planet, triplicity, "
    "Ptolemy-quadrant, celestial latitude and "
    "transport/duration/economic source methods "
    "preserved in non-executable companion. "
    "No real person travel accuracy and no runtime "
    "model promotions. NEXT printed CXL `Cause of Travels` "
    "begins PDF643 with Haly aphorisms inside; "
    "Ptolemy original travel source still needs "
    "independent cross-collation. Parallel Chinese "
    "BaZi 46 and Zi Wei 26 source-only records "
    "separately indexed; complete calendars/chart "
    "engines and untouched human validation remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06s.md").read_text()
)
CURRENT.write_text(
    "# Lilly original CXXXIX travel direction source accepted; CXL travel causes next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source B06s "
    "R8706–R8806 locally accepted, after remote "
    "GitHub verification 8,806 Lilly +1,066 Ptolemy "
    "= 9,872 historical source notes. "
    "Photo/extracted source 26 tests pass; "
    "seven historical compass and mode methods "
    "are explicitly competing and non-executable "
    "as real predictions. No independently verified "
    "travels or runtime promotions. "
    "NEXT printed CHAP CXL Cause of Travels "
    "from PDF643; Chinese BaZi 46 and "
    "Zi Wei Dou Shu 26 separately indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06s.md").read_text()
)
receipt = {
    "batch": "B06s",
    "status": "GUARDED_ORIGINAL_TRAVEL_SOURCE_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06s.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "travel_method_sha256": sha(B / "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8806,
    "ptolemy_retained": 1066,
    "combined_if_published": 9872,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
