#!/usr/bin/env python3
"""Guarded append-only Lilly 1647 Parents source admission after portable tests.

The 26 Parents notes document old claims and chart conventions only; do NOT
assert that a parent was a verified human prediction or actual birth chart.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bb_PARENTS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH = "research/astro-b07bb-clxxix-parents-source-20261020"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for p in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07bb.json"):
    assert not p.exists(), f"Possible interrupted prior admission; reconcile first: {p}"
assert git("branch", "--show-current") == BRANCH
index = load(INDEX)
chinese = load(CHINA)
source = load(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
scope = load(B / "TASK_SCOPE.json")
assert scope["branch"] == BRANCH and scope["root_outcome"] == "OPEN"
assert index["records_count"] == accept["Lilly_before"] == 12991
assert sum(row["records_count"] for row in index["batches"]) == 12991
assert index["batches"][-1]["id"] == "B07ba"
assert index["next"]["chapter"] == "CLXXIX"
assert index["next"]["pdf_page"] == 786
assert index["read_numbered_chapters"] == list(range(1, 179))
assert index["read_headed_units_count"] == 94
assert index["partial_numbered_chapters"] == []
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert index["source_sha256"] == source["source_full_original_Wellcome_1647_PDF_sha256"]
assert index["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert len(source["records"]) == rules["record_count"] == 26
assert [r["record_number"] for r in rules["rules"]] == list(range(12992, 13018))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert source["independently_validated_real_human_outcomes"] == 0
assert source["independently_reconstructed_parent_natal_charts"] == 0
assert source["independently_validated_mother_outlived_father_history"] == 0
assert source["next_record"] == accept["next_historical_R"] == "R13018"
assert source["next_printed_chapter"] == accept["next_printed_chapter"] == "CLXXX"
assert accept["next_original_PDF_frame"] == 787
assert accept["Lilly_after_if_accepted"] == 13017
assert accept["Western_after_if_accepted"] == 14083
assert (
    sha(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json") == (accept["source_notes_sha256"])
)
assert sha(B / "RULES.json") == accept["rules_sha256"]
assert release["CRC_passed"] and release["member_SHA256_and_exact_bytes_passed"]
assert release["independent_archive_extraction_tests_passed"]
assert release["portable_test_replays"] == 42
assert release["source_notes_sha256"] == accept["source_notes_sha256"]
assert release["rules_sha256"] == accept["rules_sha256"]
assert release["old_Lilly_index_sha256"] == sha(INDEX)
assert release["Chinese_V7_index_sha256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]

for f in (
    INDEX,
    CHINA,
    T / "batches/B07ba/RULES.json",
    T / "batches/B07ba/ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json",
):
    relative = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(f)), relative

BACK.mkdir(exist_ok=False)
for f, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07bb.json"),
    (CURRENT, "CURRENT_BEFORE_B07bb.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07bb.json"),
):
    (BACK / name).write_bytes(f.read_bytes())

index["batches"].append(
    {
        "id": "B07bb",
        "path": "batches/B07bb/RULES.json",
        "records_count": 26,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Original first-edition Lilly CLXXIX Of Parents printed752–753 "
            "PDF786–787, compared with independently typeset 1659 printed752–753. "
            "26 source-only annotations R12992–R13017. Lilly conjectures "
            "parental character, stature, property, parental marriage, affection "
            "and possible mother longer lived without independent observation. "
            "He attributes to Ptolemy a derived hypothetical parent chart from "
            "firstborn child's chart with day/night significator conditions, "
            "40-degree parent significator pole, plus30-degree solar oblique "
            "ascension house technique, example father 6°37 Libra. No actual "
            "parent birth time, checked horoscope/ephemeris, external Ptolemy "
            "original corroboration or successful human out-of-sample prediction. "
            "Separate following CLXXX Sicknesse, Servants begins printed753 "
            "after physical divider; zero human validations and model promotions."
        ),
    }
)
index["records_count"] = 13017
index["status"] = "BOOK_III_CLXXIX_PARENTS_PHYSICAL_SOURCE_COVERED_NEXT_CLXXX_SICKNESSE_SERVANTS"
index["read_numbered_chapters"] = index["read_numbered_chapters"] + [179]
index["read_headed_units_count"] = 95
index.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXIX",
        "editorial_ordinal": 179,
        "chapter_heading": "Of PARENTS",
        "physical_source_start_pdf": 786,
        "accepted_through_pdf": 787,
        "printed_folios": [752, 753],
        "source_batch": "B07bb",
        "historical_start": "R12992",
        "historical_end": "R13017",
        "complete": True,
        "physical_source_span_covered": True,
        "source_expert_diplomatic_collation_complete": False,
        "historical_parental_lifespan_verified": False,
        "derived_parent_birth_chart_independently_verified": False,
        "independent_human_predictions_validated": 0,
        "runtime_model_promoted": False,
    }
)
index["next"] = {
    "pdf_page": 787,
    "printed_page": 753,
    "chapter": "CLXXX",
    "printed_chapter_numeral": "CLXXX",
    "editorial_source_sequence_ordinal": 180,
    "heading": "Sicknesse, Servants",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "First original Lilly 1647 printed p753/PDF787, below the "
        "Parents chapter divider begins distinct CHAP CLXXX Sicknesse, "
        "Servants. Next historical source R13018. Prior Parents source "
        "contains unverified mortality, family affection and hypothetical "
        "parent chart; do not re-extract that accepted chapter."
    ),
    "research_scope": (
        "Historical sixth-house conditions, diseases and servitude "
        "of known native chart; document old health rhetoric only, "
        "without clinical inferences, prescriptions or real human "
        "medical prediction validity."
    ),
}
index["chapter_CLXXIX_historical_parent_claims_not_empirically_tested"] = (
    "B07bb prints historical source conjectures about real parents of "
    "a previously known merchant, but neither father/mother actual "
    "birth chart, independent parents' lifespan, affection, property "
    "or other outcomes are validated. Ptolemy-derived hypothetical "
    "parent chart is not a natal chart with independently sourced "
    "real birth data; not a human predictive success."
)
index["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bb_PARENTS.md"
assert index["records_count"] == sum(x["records_count"] for x in index["batches"])
assert index["read_numbered_chapters"] == list(range(1, 180))
assert index["partial_numbered_chapters"] == []
assert index["empirical_validations"] == index["runtime_promotions"] == 0
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Lilly 1647 original CLXXIX Of Parents: physical source covered (B07bb)\n\n"
    "**26 historical documentary records R12992–R13017** from "
    "original 1647 printed752–753/PDF786–787 and separately typeset "
    "1659 originals. The text conjectures parents' character, "
    "affection, finances and relative lifespan in a known merchant "
    "case and reports a Ptolemy-attributed technique to derive a "
    "hypothetical parent's chart from the firstborn's natal chart. "
    "No independent parent's actual birth time, real natal horoscope "
    "or observed family outcome has been verified. **13,017 Lilly + "
    "1,066 Ptolemy = 14,083 Western historical annotations**; "
    "Chinese V7 **154 BaZi + 201 Zi Wei = 355**, unchanged. "
    "CLXXIX original source span covered but critical textual "
    "verification and predictive outcomes remain unproven. "
    "Next **R13018**, original PDF787/printed753 **CLXXX Sicknesse, Servants**, "
    "below the distinct physical divider. Zero actual human predictive "
    "validations and no model runtime promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted historical checkpoint retained\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07bb",
    "status": "GUARDED_PARENT_SOURCE_26_NOTES_PREPARED_REMOTE_PUBLISH_PENDING",
    "Lilly_before": 12991,
    "Lilly_after": 13017,
    "Ptolemy_retained": 1066,
    "Western_after": 14083,
    "Chinese_V7_retained": 355,
    "new_historical_annotations": 26,
    "original_source_photographic_pages": 4,
    "next_R": "R13018",
    "next_original_PDF": 787,
    "next_printed_chapter": "CLXXX",
    "original_index_sha256": sha(BACK / "LILLY_INDEX_BEFORE_B07bb.json"),
    "new_index_sha256": sha(INDEX),
    "source_notes_sha256": accept["source_notes_sha256"],
    "rules_sha256": accept["rules_sha256"],
    "archive_sha256": release["archive_sha256"],
    "portable_tests_replayed": 42,
    "Chinese_V7_sha256": sha(CHINA),
    "empirical_real_person_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
