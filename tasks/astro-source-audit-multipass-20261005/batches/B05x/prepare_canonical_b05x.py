#!/usr/bin/env python3
"""Guarded append-only publication of first-edition Lilly maternal historical source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05x_MOTHER.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(file):
    return json.loads(Path(file).read_text())


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


for file in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05x.json"):
    assert not file.exists(), f"Interrupted or duplicate source admission: {file}"
idx = j(IDX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert idx["records_count"] == a["previous_lilly"] == 7357
assert idx["read_numbered_chapters"] == list(range(1, 123))
assert idx["batches"][-1]["id"] == "B05w"
assert idx["next"]["chapter"] == "CXXIII"
assert idx["next"]["printed_chapter_numeral"] == "CXXII"
assert idx["next"]["pdf_page"] == 604
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B05x" for x in idx["batches"])
assert a["new_source_records"] == r["record_count"] == 53
assert [x["record_number"] for x in r["rules"]] == list(range(7358, 7411))
assert a["lilly_if_published"] == 7410 and a["combined_if_published"] == 8476
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert all(
    not (
        x["independent_human_maternal_health_validated"]
        or x["reliable_human_birth_death_prediction"]
        or x["validated_maternal_wealth_or_ancestry"]
        or x["clinical_or_moral_actions_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 17 and sha(z["archive_path"]) == z["archive_sha256"]
relative = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
prior_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    prior_blob
    == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05x.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05x.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05x.md").write_bytes(PROGRESS.read_bytes())
idx["batches"].append(
    {
        "id": "B05x",
        "path": "batches/B05x/RULES.json",
        "records_count": 53,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original first-edition Lilly printed CHAP CXXII/editorial CXXIII "
            "'Of the Mother', body original PDF604-605, succeeding printed "
            "CXXIII on childbirth difficulty begins PDF606. Eleven source "
            "groups, 51 historic maternal social/medical conditional clauses "
            "plus two next heading navigation. Tenth house and ruler, Venus "
            "day/Moon night, tenth occupants, majority strong versus "
            "afflicted, parental comparative welfare, benefit/harm "
            "planetary and house sources, orientality/occidentality, "
            "fortified mother Moon health/longevity, servant status "
            "stereotype, differing sickness/death paths under "
            "qualified malefic aspects. Unresolved original glyph "
            "scope and premodern disease language quarantined; "
            "no actual woman medical/socioeconomic accuracy or model promotion."
        ),
    }
)
idx["records_count"] = 7410
idx["read_numbered_chapters"].append(123)
idx["status"] = "BOOK_III_PRINTED_MOTHER_SOURCE_COMPLETE_NEXT_CHILDBIRTH"
idx["next"] = {
    "pdf_page": 606,
    "printed_page": 572,
    "chapter": "CXXIV",
    "printed_chapter_numeral": "CXXIII",
    "heading": "If the Mother had difficult Travell in the Natives Birth, or may live after it",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original printed CHAP CXXIII starts at upper first-edition "
        "PDF606/folio572. Maternal childbirth labour rules end "
        "near the middle of that same frame; separate printed "
        "CHAP CXXIIII 'Whether the Native will enjoy the Estate "
        "of his Father' begins after divider lower PDF606."
    ),
    "following_printed_chapter_numeral": "CXXIIII",
    "following_original_pdf_page": 606,
    "research_scope": (
        "Period 1647 childbirth difficulty, oblique/long rising "
        "signs, natal aspects, malefics, Moon speed/retrograde "
        "and tenth ruler in eighth; all medical/mortality claims "
        "are not clinical evidence or modern treatment advice."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXIII_source_acceptance_note"] = (
    "B05x R7358-R7410, 53 historical source annotations, "
    "51 substantive and two next-heading. Original frame604-606 "
    "SHA source, 17 portable tests; no clinical prediction "
    "validity, no runtime scoring promotion."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 7410
assert idx["read_numbered_chapters"] == list(range(1, 124))
IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first edition maternal chapter documented as historical source\n\n"
    + review
    + "\n## Independent validity remains unestablished\n\n"
    + "After verified remote admission **7,410 Lilly + 1,066 "
    + "Ptolemy = 8,476 documentary historical annotations**. "
    + "Seventeen original-image/reverse-mapping and hermetic "
    + "ZIP source tests passed. No person-level maternal "
    + "health, death, estate or medical advice validated. "
    + "No runtime source scoring promotion.\n"
)
PROGRESS.write_text(
    "# First-edition Lilly historical source study through mother, 2026-10-17\n\n"
    "After authenticated publication **8,476 historical notes** "
    "(7,410 Lilly + 1,066 Ptolemy); original first-edition "
    "body frontier PDF605 of 894 (**67.7% scanned page position "
    "proxy only**). 53 notes preserve printed CHAP CXXII "
    "mother significators, sect, favorable and conflicting "
    "health/estate conditions and archaic disease claims. "
    "Zero independently validated person-level predictions "
    "and zero promoted scoring rules. Printed CHAP CXXIII "
    "childbirth difficulty is next at PDF606, followed by "
    "CXXIIII paternal inheritance later that page. "
    "Historical numeric tables and human blind-study "
    "lanes remain open.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B05x.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly mother source historically accepted; childbirth next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B05x mother R7358-R7410 "
    "source-only accepted; after GitHub readback 7,410 Lilly "
    "+ 1,066 Ptolemy = 8,476 historical annotations. "
    "No actual mother disease/mortality predictions "
    "validated, no runtime source rules. "
    "Next printed CXXIII first edition PDF606.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05x.md").read_text()
)
receipt = {
    "batch": "B05x",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": prior_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B05x.json"),
    "new_index_sha256": sha(IDX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7410,
    "ptolemy_retained": 1066,
    "combined_if_published": 8476,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
