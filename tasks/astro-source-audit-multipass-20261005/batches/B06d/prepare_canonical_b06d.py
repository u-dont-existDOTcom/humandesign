#!/usr/bin/env python3
"""Guarded historical source admission of Lilly's unnumbered sixth house."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06d_SIXTH_HOUSE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06d.json"):
    assert not path.exists(), f"Previous or interrupted source admission: {path}"

index = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
reverse = j(B / "SOURCE_TO_RECORD_MAP.json")
tables = j(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")

assert index["records_count"] == a["previous_lilly"] == 7583
assert index["read_numbered_chapters"] == list(range(1, 129))
assert index["batches"][-1]["id"] == "B06c"
assert index["next"]["chapter"] == "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES"
assert index["next"]["pdf_page"] == 610
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(batch["id"] == "B06d" for batch in index["batches"])
assert r["record_count"] == a["new_historical_source_annotations"] == 112
assert r["normalized_historical_table_items"] == a["normalized_source_items"] == 150
assert a["lilly_if_published"] == 7695
assert a["combined_if_published"] == 8761
assert a["numbered_chapters_added"] == 0
assert [x["record_number"] for x in r["rules"]] == list(range(7584, 7696))
assert len(reverse["source_groups"]) == 27
assert sum(x["role"] == "planet_body_region_cell" for x in r["rules"]) == 7
assert sum(x["role"] == "planet_historic_ailment_cell" for x in r["rules"]) == 7
assert sum(x["role"] == "zodiac_body_region_cell" for x in r["rules"]) == 12
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R7694", "R7695"]
assert len(tables["planetary_rows"]) == 7
assert len(tables["zodiac_rows"]) == 12
assert not tables["medical_evidence"]
assert not limits["medical_or_treatment_inference_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_health_accuracy_validated"]
        or x["actual_disease_cause_verified"]
        or x["clinical_diagnosis_or_treatment_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert (
    sha(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json")
    == a["source_matrix_sha256"]
    == z["matrix_sha256"]
)
assert z["crc_passed"] and z["full_extraction_passed"]
assert z["all_member_sha256_and_byte_sizes_passed"]
assert z["independent_extracted_documentary_tests_replayed"] == 29
assert sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)

BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06d.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06d.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06d.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B06d",
        "path": "batches/B06d/RULES.json",
        "records_count": 112,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original first-edition 1647 unnumbered "
            "sixth-house 'Of the Infirmities and Diseases of Bodyes', "
            "original PDF610–615 upper. 84 historic prose/aphorism "
            "conditions, 26 original structured table cells "
            "(seven planets x body parts/ailments plus 12 zodiac "
            "body region rows), 150 conservatively normalized "
            "historic source-list items, two following numbered "
            "CXXVIII eye chapter navigation; total 112 historical "
            "annotations R7584–R7695. Five significator types, "
            "three source considerations, strength/affliction, "
            "four elemental humors, health aphorisms, apparent "
            "disease cause vs mere significator, combined "
            "severity modifiers, horizon placement and book-two "
            "house-disease cross-reference preserved. 1647 "
            "medical/gender/mortality claims are historic only; "
            "no clinically validated disease, actual outcomes "
            "or promoted scoring rules."
        ),
    }
)
index["records_count"] = 7695
# An unnumbered introduction does NOT increase read_numbered_chapters.
assert index["read_numbered_chapters"] == list(range(1, 129))
index["status"] = "BOOK_III_SIXTH_HOUSE_UNNUMBERED_HISTORICAL_COMPLETE_NEXT_EYES"
index["next"] = {
    "pdf_page": 615,
    "printed_page": 581,
    "chapter": "CXXIX",
    "printed_chapter_numeral": "CXXVIII",
    "heading": "Of weaknesse in the Sight, or casualties portended to the Eyes",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXVIII starts after a horizontal divider "
        "in middle/lower original PDF615 printed581. "
        "It continues into subsequent original frames 616+, "
        "including eye sight and fixed-star qualifiers. "
        "Following named hearing/speech/teeth source "
        "boundaries must be separately verified."
    ),
    "research_scope": (
        "Original 1647 historical eyes/vision impairment "
        "planetary aspects and fixed stars, later hearing/speech/"
        "teeth aphorisms. No modern clinical diagnosis, "
        "ophthalmic risk prediction or health guidance."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["unnumbered_sixth_house_source_acceptance_note"] = (
    "B06d R7584–R7695 original 1647, 112 historic "
    "annotations including 14 planetary and 12 zodiac "
    "source cells with 150 normalized historic list items; "
    "all seven original planetary and twelve sign "
    "rows mapped and 29 archive-replayed SHA integrity "
    "tests passed. No real clinical accuracy or scoring."
)
assert index["records_count"] == sum(item["records_count"] for item in index["batches"]) == 7695
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original sixth-house infirmities: historical source accepted\n\n"
    + review
    + "\n## Documentary, never clinical evidence\n\n"
    + "After verified GitHub publication **7,695 Lilly + 1,066 Ptolemy "
    + "= 8,761 historical source notes**. Twenty-nine standalone "
    + "archive-replayed source tests, 26 complete structured "
    + "original table cells with 150 normalized source terms. "
    + "No human diagnosis/treatment/lifespan predictions validated, "
    + "no scoring rule promoted.\n"
)
PROGRESS.write_text(
    "# Lilly original medical source through unnumbered sixth house — 2026-10-17\n\n"
    "After verified remote publication **8,761 historical "
    "annotations** (7,695 Lilly + 1,066 Ptolemy), "
    "first-edition scan position PDF615/894 (**68.8% physical "
    "page-position proxy only**, not predictive program "
    "completion). The unnumbered sixth-house source "
    "adds 112 documentary notes including 26 planetary/"
    "zodiac table cells with 150 historically named terms. "
    "No clinical validation and zero runtime source rules. "
    "The next printed CHAP CXXVIII on eyesight begins on "
    "PDF615 after the sixth-house source; hearing, "
    "speech and teeth questions follow later. "
    "Historic numeric tables, exact rule implementation "
    "and independent blinded human tests remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06d.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly sixth-house historical taxonomy accepted; eyesight next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. First-edition B06d "
    "R7584–R7695 (112 historic records, 150 semantic "
    "source-list items) source-only accepted locally. "
    "After verified remote readback 7,695 Lilly plus "
    "1,066 Ptolemy = 8,761 historical annotations. "
    "No genuine clinical diagnoses or life-event "
    "forecasts validated; zero scoring promotions. "
    "NEXT original printed CXXVIII on eye infirmities "
    "starts PDF615/printed581.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06d.md").read_text()
)
receipt = {
    "batch": "B06d",
    "status": "GUARDED_CANONICAL_DOCUMENTARY_PREPARED_PENDING_GITHUB",
    "old_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06d.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_report_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "source_matrix_sha256": sha(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7695,
    "ptolemy_retained": 1066,
    "combined_if_published": 8761,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
