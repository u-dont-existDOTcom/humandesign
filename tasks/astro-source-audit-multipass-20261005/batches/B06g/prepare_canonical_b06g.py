#!/usr/bin/env python3
"""Guarded append-only 1647 source acceptance, servants and small cattle."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06g_SERVANTS_CATTLE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06g.json"):
    assert not p.exists(), f"Prior/partial acceptance, inspect first: {p}"
index = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
assert index["records_count"] == a["prior_lilly"] == 7835
assert index["read_numbered_chapters"] == list(range(1, 131))
assert index["batches"][-1]["id"] == "B06f"
assert index["next"]["chapter"] == "CXXXI"
assert index["next"]["printed_chapter_numeral"] == "CXXX"
assert index["next"]["pdf_page"] == 620
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B06g" for x in index["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 42
assert a["lilly_if_published"] == 7877
assert a["combined_if_published"] == 8943
assert [x["record_number"] for x in r["rules"]] == list(range(7836, 7878))
assert sum(x["role"] == "next_section_navigation" for x in r["rules"]) == 2
assert len(m["source_groups"]) == 8
assert a["numbered_chapters_added"] == 1
assert not limits["criminality_classification_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_worker_ethics_accuracy_validated"]
        or x["worker_criminality_or_dishonesty_allegation_authorized"]
        or x["actual_livestock_economic_outcome_validated"]
        or x["employment_or_financial_advice_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 15 and sha(z["archive_path"]) == z["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06g.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06g.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06g.md").write_bytes(PROGRESS.read_bytes())
index["batches"].append(
    {
        "id": "B06g",
        "path": "batches/B06g/RULES.json",
        "records_count": 42,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly printed CHAP CXXX/editorial CXXXI, "
            "Of Servants or small Cattle, lower original PDF620 "
            "printed586, ending before following unnumbered "
            "seventh-house marriage introduction across PDF620–621. "
            "Eight source-image passage groups, 40 substantive "
            "historical claims and two next-section navigation. "
            "Sixth house/ruler Mercury and occupying planets "
            "servant indicators, benefic or fortunate majority "
            "versus unfortunate, economy/cattle alternative "
            "outcomes, essentially dignified malignant planet "
            "with good Ascendant-lord aspect can yield good "
            "servant despite rough character, sixth ruler in "
            "angle/tenth, Mercury retrograde/combust plus malefic "
            "fixed signs and Saturn peregrine or South Node/Mars "
            "in air/fire sixth house historical theft allegations. "
            "All ethical and criminal labels are unsupported "
            "seventeenth-century stereotypes. No human "
            "worker-criminality, livelihood or cattle forecast "
            "validated, zero runtime rule promotions."
        ),
    }
)
index["records_count"] = 7877
index["read_numbered_chapters"].append(131)
index["status"] = "BOOK_III_SERVANTS_HISTORICAL_NEXT_UNNUMBERED_SEVENTH_HOUSE_MARRIAGE"
index["next"] = {
    "pdf_page": 621,
    "printed_page": 587,
    "chapter": "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE",
    "printed_chapter_numeral": None,
    "heading": (
        "The seventh House, and the Judgments appertaining unto it. "
        "Of Marriage: and first of Mens Marriages"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "A trailing 'The' at original PDF620 page bottom "
        "opens the unnumbered substantive seventh-house "
        "intro heading beginning PDF621/printed587. "
        "Its discussion of male marriage and probability "
        "of marriage continues PDF622/printed588 and "
        "upper PDF623/printed589 before separate printed "
        "CHAP CXXXI starts mid PDF623. "
        "The entire unnumbered introduction must be "
        "extracted before printed CXXXI, without "
        "double counting adjoining text."
    ),
    "following_printed_chapter_numeral": "CXXXI",
    "following_original_pdf_page": 623,
    "research_scope": (
        "Historical sex-coded seventh-house marriage "
        "significators Venus/Moon, seventh/ruler/occupants, "
        "barren/fruitful signs and house conditions, "
        "support/malefic retrogradation and contrary "
        "testimonies, purported social/marital outcomes. "
        "No actual couple prediction validity, sexuality "
        "or human diagnostic assertions."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXXXI_source_acceptance_note"] = (
    "B06g R7836–R7877, 42 original historical "
    "annotation records, 40 substantive and 2 "
    "unnumbered seventh-house navigation, "
    "source PDF620–627 SHA/bytes and 15 hermetic "
    "replay documentary tests, human theft "
    "and labor outcomes validated 0, "
    "scoring rules promoted 0."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7877
assert index["read_numbered_chapters"] == list(range(1, 132))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original servants and cattle: documentary source accepted\n\n"
    + review
    + "\n## No human wrongdoing or financial validity\n\n"
    + "After remote verification **7,877 Lilly + 1,066 "
    + "Ptolemy = 8,943 historical source annotations**. "
    + "Original-image/integrity and portable extracted "
    + "tests pass, no verified criminality, employment "
    + "or livestock predictions and no runtime "
    + "model promotion.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 original source through servants and small cattle — 2026-10-17\n\n"
    "After authenticated GitHub publication **8,943 "
    "historical source annotations** (7,877 Lilly "
    "+ 1,066 Ptolemy), original source page position "
    "PDF620/894 (**69.4% physical scan proxy only**). "
    "Printed CHAP CXXX servants/cattle source "
    "adds 42 historical notes including essential "
    "dignity exception to malefic worker and "
    "unsupported worker theft stereotypes. "
    "Next UNNUMBERED seventh-house marriage intro "
    "starts across PDF620–621 and substantive "
    "text continues until first numbered CXXXI "
    "from PDF623. Actual human relationship/labor "
    "validations zero, no scoring runtime rules; "
    "numeric astronomy and blind-testing lanes open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06g.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly servants/cattle history accepted, seventh house intro next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06g source "
    "R7836–R7877 prepared; after GitHub SHA readback "
    "7,877 Lilly + 1,066 Ptolemy = 8,943 "
    "original historical annotations. "
    "No human criminality, worker loyalty "
    "or animal-profit predictive validity, "
    "no promoted scoring rules. Next "
    "unnumbered seventh-house marriage "
    "source PDF621–623.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06g.md").read_text()
)
receipt = {
    "batch": "B06g",
    "status": "GUARDED_CANONICAL_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06g.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7877,
    "ptolemy_retained": 1066,
    "combined_if_published": 8943,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
