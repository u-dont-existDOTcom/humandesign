#!/usr/bin/env python3
"""Guarded admission of original 1647 medical CXXVIII, no clinical promotion."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06e_MEDICAL_CHAP_CXXVIII.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06e.json"):
    assert not path.exists(), f"Duplicate/partial first-edition admission: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
bounds = j(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")

assert i["records_count"] == a["previous_lilly"] == 7695
assert i["read_numbered_chapters"] == list(range(1, 129))
assert i["batches"][-1]["id"] == "B06d"
assert i["next"]["chapter"] == "CXXIX"
assert i["next"]["printed_chapter_numeral"] == "CXXVIII"
assert i["next"]["pdf_page"] == 615
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(row["id"] == "B06e" for row in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 113
assert r["substantive_historical_conditions"] == a["substantive"] == 111
assert a["lilly_if_published"] == 7808
assert a["combined_if_published"] == 8874
assert [row["record_number"] for row in r["rules"]] == list(range(7696, 7809))
assert sum(row["role"] == "next_chapter_navigation" for row in r["rules"]) == 2
assert len(m["source_groups"]) == 11
assert bounds["last_chapter_text_pdf_frame"] == 619
assert bounds["following_printed_chapter"] == "CXXIX"
assert not limits["clinical_medical_advice_authorized"]
assert not limits["actual_person_psychological_labels_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        row["independent_human_medical_result_validated"]
        or row["modern_ophthalmic_neurological_diagnosis_validated"]
        or row["reliable_falls_disability_or_lifespan_prediction"]
        or row["person_level_moral_or_psychiatric_label_authorized"]
        or row["clinical_or_medical_treatment_advice_authorized"]
        or row["runtime_model_promoted"]
    )
    for row in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert (
    sha(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json")
    == a["boundary_sha256"]
    == z["source_boundary_sha256"]
)
assert z["crc_passed"] and z["full_extraction_passed"]
assert z["all_member_sha256_and_bytes_verified"]
assert z["independent_replayed_tests"] == 24
assert sha(z["archive_path"]) == z["archive_sha256"]

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06e.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06e.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06e.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B06e",
        "path": "batches/B06e/RULES.json",
        "records_count": 113,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 printed CHAP CXXVIII/editorial CXXIX, "
            "On weaknesse in Sight or casualties portended to Eyes, "
            "with unnumbered ear, speech, dental, falling-sickness/"
            "madness, stone/strangury, gout and violent fall "
            "subsections throughout original PDF615–619 upper. "
            "Separate printed CXXIX on curability begins lower PDF619 "
            "and printed CXXX servants begins PDF620. Eleven source "
            "groups, 111 substantive historic claims and 2 following "
            "numbered chapter navigation, 113 total R7696–R7808. "
            "Historic luminary-malefic aspects, cloudy fixed stars/"
            "Milky Way degrees, auditory Mercury/Saturn and benefic "
            "exceptions, tongue and dental sign sources, 4 alleged "
            "epilepsy causes and archaic mental illness stereotype "
            "conditions, urinary stone, gout and bodily falls with "
            "source actor anecdotes. All original 1647 medical and "
            "psychological assertions are historical only, with "
            "zero actual patient validity or promoted scoring rules."
        ),
    }
)
i["records_count"] = 7808
i["read_numbered_chapters"].append(129)
i["status"] = "BOOK_III_MEDICAL_CHAP_CXXVIII_DOCUMENTARY_NEXT_CURABILITY_CXXIX"
i["next"] = {
    "pdf_page": 619,
    "printed_page": 585,
    "chapter": "CXXX",
    "printed_chapter_numeral": "CXXIX",
    "heading": "Whether the Disease the Native is subject unto be curable or not",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXIX begins below divider in lower "
        "original PDF619/printed585 and continues into upper "
        "PDF620/printed586. It ends immediately before separate "
        "printed CHAP CXXX 'Of Servants or small Cattle', "
        "which starts at a new heading on PDF620. "
        "Original PDF620–627 retained as following context."
    ),
    "following_printed_chapter_numeral": "CXXX",
    "following_original_pdf_page": 620,
    "research_scope": (
        "Historical cure/non-cure from benefic sextile/trine "
        "to sickness significators in moveable/fixed signs, "
        "planetary dignity and alternative claimed money/"
        "medicine/magic recovery paths. These are "
        "not clinical curability predictions or advice."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXIX_source_acceptance_note"] = (
    "B06e R7696–R7808, 113 historical notes across eight "
    "medical subtopics and two following heading navigation. "
    "Original photos PDF615–627 SHA/bytes, 24 original-source "
    "archive replay tests. No real patient, seizure, "
    "vision, psychiatric, injury or disease outcomes "
    "validated, no runtime rule promotion."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7808
assert i["read_numbered_chapters"] == list(range(1, 130))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first-edition eye, neurologic, dental and gout source documented\n\n"
    + review
    + "\n## No clinical prediction validity\n\n"
    + "After GitHub readback **7,808 Lilly + 1,066 "
    + "Ptolemy = 8,874 historical source annotations**. "
    + "All 24 documentary checks and portable-archive "
    + "replays pass. No verified patient outcome and "
    + "no clinical, psychiatric or astrological scoring "
    + "promotion. These are seventeenth-century source "
    + "statements only.\n"
)
PROGRESS.write_text(
    "# Original Lilly source through printed medical chapter CXXVIII — 2026-10-17\n\n"
    "After verified publication **8,874 historical source "
    "annotations** (7,808 Lilly + 1,066 Ptolemy). "
    "First-edition physical source frontier PDF619/894 "
    "(**69.2% scanned page position only**). "
    "Printed CXXVIII adds 113 historic subchapter "
    "annotations on sight, hearing, speech, teeth, "
    "neurological stigma, urinary stone, gout and falls. "
    "Next printed CXXIX on historical disease curability "
    "begins lower PDF619 and ends upper PDF620. "
    "No human clinical or astrological predictions "
    "independently validated and no runtime rules promoted. "
    "Numerical tables and untouched blind tests remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06e.md").read_text()
)
CURRENT.write_text(
    "# Original 1647 printed CXXVIII historical medical source accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06e source "
    "R7696–R7808 accepted locally, after remote SHA readback "
    "7,808 Lilly + 1,066 Ptolemy = 8,874 original "
    "documentary annotations. Eight history-only "
    "medical topic groups preserved; no clinical accuracy "
    "or scoring promotions. NEXT original printed "
    "CXXIX curability on PDF619–620, followed by "
    "printed CXXX servants PDF620.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06e.md").read_text()
)
receipt = {
    "batch": "B06e",
    "status": "GUARDED_CANONICAL_DOCUMENTARY_PREPARED_PENDING_REMOTE",
    "old_index_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06e.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_report_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "original_source_boundary_sha256": sha(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7808,
    "ptolemy_retained": 1066,
    "combined_if_published": 8874,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
