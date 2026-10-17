#!/usr/bin/env python3
"""Guarded append-only original Lilly second sibling-number method accession."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05v_PTOLEMY_CONTRAST.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05v.json"):
    assert not path.exists(), f"Existing or partial source admission: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7252
assert i["read_numbered_chapters"] == list(range(1, 122))
assert i["batches"][-1]["id"] == "B05u"
assert i["next"]["chapter"] == "CXXII"
assert i["next"]["printed_chapter_numeral"] == "CXXI"
assert i["next"]["pdf_page"] == 602
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(q["id"] == "B05v" for q in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 43
assert a["lilly_if_published"] == 7295
assert a["combined_if_published"] == 8361
assert [q["record_number"] for q in r["rules"]] == list(range(7253, 7296))
assert sum(q["role"] == "next_section_navigation" for q in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        q["independent_sibling_birth_count_validated"]
        or q["human_fertility_or_sex_prediction_validated"]
        or q["human_longevity_or_death_prediction_validated"]
        or q["original_ptolemy_text_independently_verified"]
        or q["runtime_model_promoted"]
    )
    for q in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 16 and sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05v.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05v.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05v.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B05v",
        "path": "batches/B05v/RULES.json",
        "records_count": 43,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original first-edition printed CHAP CXXI/editorial "
            "CXXII 'Number of Brethren', PDF602/folio568. Eight "
            "source groups, 41 historical clauses and two following "
            "unnumbered fourth-house navigation records. Third house "
            "and ruler fertility status, aspecting planets by gendered "
            "signs for proposed brothers/sisters number, mutual good "
            "versus adverse aspects for siblings survival, Mars and "
            "third-ruler combustion, Sun placement, Saturn/Jupiter "
            "firstborn or better sibling outcome, superior/inferior "
            "and angular dignity branches. Explicit historical "
            "disagreement with Lilly-attributed Ptolemy method using "
            "Midheaven/mother house, diurnal Venus/nocturnal Moon "
            "and eleventh house; Lilly's same-mother-only qualification "
            "and unverified claims of ancient consensus retained. "
            "Next UNNUMBERED fourth-house introduction begins PDF603. "
            "No independent source verification against Ptolemy, "
            "demographic forecast validity or runtime rules."
        ),
    }
)
i["records_count"] = 7295
i["read_numbered_chapters"].append(122)
i["status"] = "BOOK_III_SIBLING_COUNT_PTOLEMY_CONTRAST_NEXT_UNNUMBERED_FOURTH_HOUSE"
i["next"] = {
    "pdf_page": 603,
    "printed_page": 569,
    "chapter": "UNNUMBERED_FOURTH_HOUSE_PARENTS",
    "printed_chapter_numeral": None,
    "heading": ("Judgements upon the fourth House. Concerning Parents and Patrimony of the Father"),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Unnumbered substantive fourth-house parent/patrimony "
        "introduction starts below ornament in original first edition "
        "PDF603/folio569, continues PDF604/folio570 until a "
        "divider before printed CHAP CXXII Of the Mother on PDF604. "
        "Do not skip the unnumbered parent source or conflate with "
        "the subsequent numbered mother's chapter."
    ),
    "following_printed_chapter_numeral": "CXXII",
    "following_original_pdf_page": 604,
    "research_scope": (
        "Original father/patrimony fourth-house chart indicators, "
        "day/night Sun/Saturn, favorable and afflicted cases, "
        "partial conditions and historical longevity claims; "
        "source archival only, not actual person health or inheritance."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXII_source_acceptance_note"] = (
    "B05v R7253–R7295, 43 historic source annotations, "
    "41 substantive and 2 unnumbered-next navigation, "
    "original PDF602–605 witnesses, 16 standalone tests. "
    "Ptolemy contrast is Lilly's attribution only; no "
    "real sibling/fertility/death predictions validated."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7295
assert i["read_numbered_chapters"] == list(range(1, 123))
INDEX.write_text(json.dumps(i, indent=2, ensure_ascii=False) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original 1647: sibling-count method / Ptolemy dispute historical source\n\n"
    + review
    + "\n## Canonical historical corpus\n\n"
    + "After authenticated publication: **7,295 Lilly + 1,066 "
    + "Ptolemy = 8,361 historical documentary annotations**, "
    + "not independent human sibling forecasts. "
    + "Sixteen original-source and ZIP-replay tests pass. "
    + "No runtime model promotion.\n"
)
PROGRESS.write_text(
    "# Lilly original first edition through sibling-number Ptolemy contrast — 2026-10-17\n\n"
    "After remote publication **8,361 historical documentary "
    "records** (7,295 Lilly + 1,066 Ptolemy), source body "
    "frontier original PDF602/894 (**67.3% scanned page position "
    "only, not research validation completion**). Printed "
    "CHAP CXXI repeated sibling-number technique adds "
    "43 historical source annotations and an explicit "
    "Lilly-attributed Ptolemy dispute, including mother/sect "
    "and eleventh-house factors. Neither compared to "
    "Ptolemy's text independently nor validated on human "
    "birth records. Next UNNUMBERED fourth-house parent/patrimony "
    "introduction original PDF603, before printed CXXII. "
    "Numeric and blind human prediction lanes remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05v.md").read_text()
)
CURRENT.write_text(
    "# Original sibling-number Ptolemy comparison accepted; fourth-house parents next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05v R7253–R7295 "
    "locally source-accepted; after verified GitHub push "
    "7,295 Lilly + 1,066 Ptolemy = 8,361 historic records. "
    "43 clause-level annotations, authorial contrast "
    "of sibling methods not independent replication. "
    "No human birth/death validations and no runtime "
    "source rules. Next unnumbered fourth-house father "
    "and estate introduction PDF603.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B05v.md").read_text()
)
rec = {
    "batch": "B05v",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "old_index_git_blob": old_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05v.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7295,
    "ptolemy_retained": 1066,
    "combined_if_published": 8361,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
