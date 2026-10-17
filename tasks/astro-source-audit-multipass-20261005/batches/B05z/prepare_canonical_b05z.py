#!/usr/bin/env python3
"""Original 1647 father estate source; guarded canonical documentary append."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05z_FATHER_ESTATE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(file):
    return json.loads(Path(file).read_text())


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05z.json"):
    assert not p.exists(), f"Duplicate or partial source index: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7440
assert i["read_numbered_chapters"] == list(range(1, 125))
assert i["batches"][-1]["id"] == "B05y"
assert i["next"]["chapter"] == "CXXV"
assert i["next"]["printed_chapter_numeral"] == "CXXIIII"
assert i["next"]["pdf_page"] == 606
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B05z" for x in i["batches"])
assert a["new_historical_records"] == r["record_count"] == 33
assert [x["record_number"] for x in r["rules"]] == list(range(7441, 7474))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert a["lilly_if_published"] == 7473 and a["combined_if_published"] == 8539
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_inheritance_validated"]
        or x["family_finances_or_management_predicted"]
        or x["legal_or_financial_advice_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 14 and sha(z["archive_path"]) == z["archive_sha256"]
relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05z.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05z.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05z.md").write_bytes(PROGRESS.read_bytes())
i["batches"].append(
    {
        "id": "B05z",
        "path": "batches/B05z/RULES.json",
        "records_count": 33,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly printed CHAP CXXIIII/editorial CXXV, "
            "whether native inherits, improves or consumes father's estate, "
            "first-edition PDF606 lower to PDF607 upper. Eight original "
            "source groups, 31 substantive natal clauses and two "
            "following printed CXXV parents' agreement navigation. "
            "Conjunction/aspects Sun/benefics by day, Saturn/Moon by "
            "night, placement/rulership in second/fourth; Mars "
            "sect-based affliction without beneficial relief; "
            "nocturnal weak Moon plus second/fourth conditions, "
            "Saturn peregrine twelfth plus fourth lord, "
            "unfortunate fourth/first lord, Sun-Mars peregrine "
            "and second harm. No real inheritance success, "
            "financial/character validity or promoted runtime rules."
        ),
    }
)
i["records_count"] = 7473
i["read_numbered_chapters"].append(125)
i["status"] = "BOOK_III_PATERNAL_INHERITANCE_SOURCE_COMPLETE_NEXT_PARENT_AGREEMENT"
i["next"] = {
    "pdf_page": 607,
    "printed_page": 573,
    "chapter": "CXXVI",
    "printed_chapter_numeral": "CXXV",
    "heading": "Of the mutuall agreement of Parents",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXV on parent-to-parent agreement begins "
        "below divider mid original PDF607/folio573, "
        "finishes before separate printed CHAP CXXVI at top "
        "original PDF608/folio574. Preserve the chapter seam."
    ),
    "research_scope": (
        "Historical day Sun/Venus and night Saturn/Moon "
        "parental aspects, reception, disagreement, alternative "
        "gendered character stereotypes; no validation as "
        "actual relationships or moral diagnoses."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXV_source_acceptance_note"] = (
    "B05z R7441–R7473, 33 historical source clauses and "
    "navigation, original PDF606–609 SHA, 14 standalone "
    "source tests; no independent actual financial outcomes, "
    "human conduct classifications or runtime source promotion."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7473
assert i["read_numbered_chapters"] == list(range(1, 126))
INDEX.write_text(json.dumps(i, indent=2, ensure_ascii=False) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original first-edition paternal estate historical source accepted\n\n"
    + review
    + "\n## Independent validation status\n\n"
    + "After verified remote publication **7,473 Lilly + 1,066 "
    + "Ptolemy = 8,539 historical source notes**. Fourteen "
    + "source/ZIP replay tests pass, zero independent estate "
    + "transfer or loss validations, no runtime scoring promotion.\n"
)
PROGRESS.write_text(
    "# First-edition Lilly source through father's inherited estate — 2026-10-17\n\n"
    "After authenticated publication **8,539 historical source "
    "annotations** (7,473 Lilly + 1,066 Ptolemy), original "
    "frontier PDF607 of 894 (**~67.9% scanned page position only**). "
    "33 new original father-inheritance source clauses/navigation, "
    "conditional day/night and opposite losses. No real estate "
    "outcome validation or scoring rules promoted. "
    "Next printed CXXV parental agreement at PDF607. "
    "Numerical tables, runtime implementation and blind "
    "human research remain separate/open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05z.md").read_text()
)
CURRENT.write_text(
    "# Lilly paternal-inheritance documentary source complete, parent agreement next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source-only B05z "
    "R7441–R7473 prepared: after verified GitHub push "
    "7,473 Lilly + 1,066 Ptolemy = 8,539 historical "
    "annotations. No actual human inheritance predictions "
    "validated, no scoring rules. Next printed CHAP CXXV "
    "parents' agreement lower PDF607.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B05z.md").read_text()
)
receipt = {
    "batch": "B05z",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_git_blob": blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B05z.json"),
    "new_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7473,
    "ptolemy_retained": 1066,
    "combined_if_published": 8539,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
