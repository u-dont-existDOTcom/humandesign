#!/usr/bin/env python3
"""Append first-edition historical curability source, never medical efficacy."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06f_CURABILITY.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06f.json"):
    assert not p.exists(), f"Duplicate/interrupted source admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
assert i["records_count"] == a["previous_lilly"] == 7808
assert i["read_numbered_chapters"] == list(range(1, 130))
assert i["batches"][-1]["id"] == "B06e"
assert i["next"]["chapter"] == "CXXX"
assert i["next"]["printed_chapter_numeral"] == "CXXIX"
assert i["next"]["pdf_page"] == 619
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06f" for x in i["batches"])
assert r["record_count"] == a["new_source_annotations"] == 27
assert a["lilly_if_published"] == 7835
assert a["combined_if_published"] == 8901
assert [x["record_number"] for x in r["rules"]] == list(range(7809, 7836))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert not limits["medical_or_treatment_advice_authorized"]
assert all(
    not (
        x["independent_disease_recovery_forecast_validated"]
        or x["real_patient_diagnosis_or_prognosis_validated"]
        or x["medicine_or_magic_treatment_authorized"]
        or x["runtime_rule_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 14 and sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06f.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06f.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06f.md").write_bytes(PROGRESS.read_bytes())
i["batches"].append(
    {
        "id": "B06f",
        "path": "batches/B06f/RULES.json",
        "records_count": 27,
        "sha256": a["rules_sha256"],
        "scope": (
            "Lilly original first edition 1647 printed CHAP CXXIX/"
            "editorial CXXX, Whether Disease the Native "
            "is subject unto be curable or not, source lower "
            "original PDF619/printed585 through upper "
            "PDF620/printed586, before printed CHAP CXXX "
            "on servants and small cattle also PDF620. "
            "Six passage groups, 25 substantive historical "
            "curability clauses and 2 next-numbered chapter "
            "navigation. Favorable sextile/trine to disease "
            "signifiers in moveable signs versus fixed and "
            "no benefic aspect, exact partile versus remote "
            "alleged time to recovery, Jupiter money/counsel, "
            "Mercury medicine, Venus magic/divine/chance, "
            "contrary own house/exaltation poor-remedy "
            "claim. Original medical statements only; "
            "zero clinical predictions and runtime promotions."
        ),
    }
)
i["records_count"] = 7835
i["read_numbered_chapters"].append(130)
i["status"] = "BOOK_III_HISTORICAL_CURABILITY_SOURCE_COMPLETE_NEXT_SERVANTS"
i["next"] = {
    "pdf_page": 620,
    "printed_page": 586,
    "chapter": "CXXXI",
    "printed_chapter_numeral": "CXXX",
    "heading": "Of Servants or small Cattle",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXX on servants/small cattle begins "
        "after new heading in original PDF620/printed586 "
        "below curability chapter. Continues PDF621+; "
        "the next numbered heading must be located before "
        "a complete source batch is accepted."
    ),
    "research_scope": (
        "Historical servant/cattle livelihood and alleged "
        "trustworthiness rules: sixth house and lord, "
        "Mercury, occupants, malefics benefic aspect, "
        "combustion/retrograde, profit/thieving stereotypes. "
        "Never infer actual persons' criminality."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXX_source_acceptance_note"] = (
    "B06f R7809–R7835, 27 historical documentary "
    "notes and separate CXXX navigation, original "
    "PDF619–621 SHA images, 14 archive-replayed "
    "source checks. No real patient recovery "
    "or runtime rules validated."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7835
assert i["read_numbered_chapters"] == list(range(1, 131))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly CXXIX curability: documentary source accepted\n\n"
    + review
    + "\n## Actual clinical validation\n\n"
    + "After remote verification **7,835 Lilly + 1,066 "
    + "Ptolemy = 8,901 historical annotations**. "
    + "Original page/SHA/ZIP source tests pass; "
    + "no actual disease or cure outcomes validated, "
    + "no care advice and no runtime source rule.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 study through historic disease-curability claims — 2026-10-17\n\n"
    "After authenticated publication **8,901 "
    "historical source annotations** (7,835 "
    "Lilly + 1,066 Ptolemy), original scanned "
    "position PDF620/894 (**69.4% page-position "
    "only, NOT program completion**). Printed "
    "CHAP CXXIX curability has 27 historical "
    "claims and navigation; no real clinical "
    "validation, no runtime promotions. Following "
    "CHAP CXXX servants/small cattle starts "
    "original PDF620 and should be studied next. "
    "Source numeric reference and blind human "
    "studies remain OPEN.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06f.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CXXIX curability historical chapter accepted, servants next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06f "
    "R7809–R7835 historically prepared. After "
    "GitHub SHA confirmation 7,835 Lilly plus "
    "1,066 Ptolemy = 8,901 historic documentary "
    "annotations. No medical diagnosis/curability "
    "prediction verified and zero model promotions. "
    "NEXT original printed CHAP CXXX on servants "
    "and small cattle from PDF620/printed586.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06f.md").read_text()
)
rec = {
    "batch": "B06f",
    "status": "GUARDED_HISTORICAL_SOURCE_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06f.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7835,
    "ptolemy_retained": 1066,
    "combined_if_published": 8901,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
