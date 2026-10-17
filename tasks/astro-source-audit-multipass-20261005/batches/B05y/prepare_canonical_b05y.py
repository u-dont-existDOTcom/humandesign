#!/usr/bin/env python3
"""Guarded canonical append of historic childbirth hypotheses only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05y_CHILDBIRTH.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05y.json"):
    assert not path.exists(), f"Interrupted/duplicate index admission: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert i["records_count"] == a["previous_lilly"] == 7410
assert i["read_numbered_chapters"] == list(range(1, 124))
assert i["batches"][-1]["id"] == "B05x"
assert i["next"]["chapter"] == "CXXIV"
assert i["next"]["printed_chapter_numeral"] == "CXXIII"
assert i["next"]["pdf_page"] == 606
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(row["id"] == "B05y" for row in i["batches"])
assert a["new_records"] == r["record_count"] == 30
assert a["lilly_if_published"] == 7440
assert a["combined_if_published"] == 8506
assert [x["record_number"] for x in r["rules"]] == list(range(7411, 7441))
assert sum(x["role"] == "next_chapter_navigation" for x in r["rules"]) == 2
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["human_pregnancy_complication_validated"]
        or x["human_maternal_mortality_predicted"]
        or x["human_neonatal_outcome_predicted"]
        or x["medical_advice_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert h(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 13 and h(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05y.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B05y.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B05y.md").write_bytes(PROGRESS.read_bytes())
i["batches"].append(
    {
        "id": "B05y",
        "path": "batches/B05y/RULES.json",
        "records_count": 30,
        "sha256": a["rules_sha256"],
        "scope": (
            "Lilly original first edition printed CHAP CXXIII/editorial CXXIV "
            "on maternal childbirth difficulty/survival, original PDF606 "
            "upper section. Seven source groups, 28 original historical "
            "claims plus 2 navigation to separate printed CHAP CXXIIII "
            "on father's inherited estate on same PDF606. Oblique versus "
            "long ascendant signs, malefic square/opposition/node, "
            "benefic Moon aspects, sign groups sex-based, 12th malefics, "
            "slow Moon/retrograde/stationary alternatives, tenth ruler "
            "eighth and qualified maternal death conjecture. "
            "These are premodern unsupported historical medical claims, "
            "not actual maternal or neonatal predictive accuracy "
            "or clinical guidance, no runtime source promotion."
        ),
    }
)
i["records_count"] = 7440
i["read_numbered_chapters"].append(124)
i["status"] = "BOOK_III_CHILDBIRTH_HISTORICAL_ONLY_NEXT_PATERNAL_INHERITANCE"
i["next"] = {
    "pdf_page": 606,
    "printed_page": 572,
    "chapter": "CXXV",
    "printed_chapter_numeral": "CXXIIII",
    "heading": (
        "Whether the Native will enjoy the Estate of his Father, "
        "and whether he shall waste or consume it"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXIIII begins lower original PDF606/folio572 "
        "below divider, continues upper original PDF607/folio573 "
        "before separate printed CHAP CXXV Of the mutuall agreement "
        "of Parents starts mid PDF607."
    ),
    "research_scope": (
        "Historical paternal inheritance transfer/growth versus "
        "estate destruction, Sun or Saturn according to sect, "
        "fortunes vs malefic affliction, fourth/second lords and "
        "retrogradation/combustion/mixed testimonies, historical only."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXXIV_source_acceptance_note"] = (
    "B05y R7411–R7440, 30 historic records, 28 substantive "
    "childbirth/labor mortality clauses, 2 following "
    "patrimony navigation; source PDF606-608 SHA and "
    "13 archive-replayed source integrity tests, zero "
    "independent clinical validations or runtime rules."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 7440
assert i["read_numbered_chapters"] == list(range(1, 125))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original 1647 Lilly childbirth difficulty historically documented\n\n"
    + review
    + "\n## Archival/source integrity, not medical prediction\n\n"
    + "After verified publication **7,440 Lilly + 1,066 Ptolemy "
    + "= 8,506 historical source records**. 13 hermetic "
    + "source integrity tests, SHA, and original chapter "
    + "boundary verified; zero real human obstetric "
    + "forecast validity, no medical advice and "
    + "no runtime source-model promotions.\n"
)
PROGRESS.write_text(
    "# Lilly first edition through historical childbirth chapter — 2026-10-17\n\n"
    "After verified remote publication **8,506 documentary "
    "historical annotations** (7,440 Lilly + 1,066 Ptolemy). "
    "Original source frontier PDF606/894 (**~67.8% page-position "
    "proxy only**, not program validation). Printed CHAP CXXIII "
    "childbirth source records 30 historic clauses/navigation; "
    "no independent human pregnancy outcomes, no runtime rules. "
    "Following printed CXXIIII parental patrimony begins "
    "lower PDF606; source numeric tables and blind human "
    "validation remain open.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B05y.md").read_text()
)
CURRENT.write_text(
    "# Lilly childbirth first-edition source historically documented\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source-only B05y "
    "R7411–R7440 accepted locally; 7,440 Lilly and "
    "1,066 Ptolemy = 8,506 after GitHub readback. "
    "All medical/labor/mortality claims are historical "
    "unvalidated text, zero clinical evidence or model rules. "
    "NEXT printed CHAP CXXIIII father inheritance PDF606.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05y.md").read_text()
)
receipt = {
    "batch": "B05y",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_git_blob": blob,
    "old_index_sha256": h(BACK / "INDEX_BEFORE_B05y.json"),
    "new_index_sha256": h(INDEX),
    "latest_sha256": h(LATEST),
    "progress_sha256": h(PROGRESS),
    "current_sha256": h(CURRENT),
    "rules_sha256": h(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7440,
    "ptolemy_retained": 1066,
    "combined_if_published": 8506,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
