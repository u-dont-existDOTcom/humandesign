#!/usr/bin/env python3
"""Guarded append-only original source documentation of printed Lilly CHAP CXVI."""
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05p_ACQUISITION_METHOD.md"
BACKUP = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACKUP / "INDEX_BEFORE_B05p.json"):
    assert not p.exists(), f"Partial or duplicate historical admission: {p}"
index = j(INDEX)
accepted = j(B / "ACCEPTANCE.json")
records = j(B / "RULES.json")
released = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == accepted["prior_lilly"] == 6994
assert index["read_numbered_chapters"] == list(range(1, 117))
assert index["batches"][-1]["id"] == "B05o"
assert index["next"]["chapter"] == "CXVII"
assert index["next"]["pdf_page"] == 594
assert index["next"]["printed_chapter_numeral"] == "CXVI"
assert index["source_sha256"] == (
    "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
)
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(b["id"] == "B05p" for b in index["batches"])
assert records["record_count"] == accepted["new_historical_annotations"] == 57
assert accepted["lilly_if_published"] == 7051
assert accepted["combined_if_published"] == 8117
assert [row["record_number"] for row in records["rules"]] == list(range(6995, 7052))
assert sum(row["role"] == "next_chapter_navigation" for row in records["rules"]) == 2
assert records["empirical_validations"] == accepted["empirical_validations"] == 0
assert records["runtime_promotions"] == accepted["runtime_promotions"] == 0
assert all(
    not (
        row["actual_criminal_or_ethical_classification_validated"]
        or row["real_person_legal_allegation_authorized"]
        or row["independent_human_financial_accuracy_validated"]
        or row["runtime_rule_promoted"]
    )
    for row in records["rules"]
)
assert sha(B / "RULES.json") == accepted["rules_sha256"] == released["accepted_rules_sha256"]
assert released["crc_passed"] and released["per_member_sha256_passed"]
assert released["full_extraction_passed"] and released["replayed_tests"] == 21
assert sha(released["archive_path"]) == released["archive_sha256"]
rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(
    ["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT
).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True
).strip()
assert old_blob == subprocess.check_output(
    ["git", "hash-object", str(INDEX)], cwd=ROOT, text=True
).strip()
BACKUP.mkdir(exist_ok=True)
(BACKUP / "INDEX_BEFORE_B05p.json").write_bytes(INDEX.read_bytes())
(BACKUP / "CURRENT_BEFORE_B05p.md").write_bytes(CURRENT.read_bytes())
(BACKUP / "PROGRESS_BEFORE_B05p.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append({
    "id": "B05p",
    "path": "batches/B05p/RULES.json",
    "records_count": 57,
    "sha256": accepted["rules_sha256"],
    "scope": (
        "Original 1647 Lilly printed CHAP CXVI/editorial CXVII "
        "'If the Native shall attain his Estate by just means, or "
        "indirect dealing'. Body original PDF594–596, next printed "
        "CXVII heading lower PDF596. Ten original source groups, "
        "55 conditional historical claims and 2 following-chapter "
        "navigation records. Intrinsic benefic or malefic nature, "
        "dignity of sign, combustion, retrogradation, aspects and "
        "plurality of evidence, mutually opposed/mixed cases, "
        "hypothetical Jupiter/Saturn sixth-house example, and "
        "multiple direction/revolution timing candidates. PDF594 "
        "and PDF595 both print folio561; scan order continuous. "
        "Historical ethical and financial stereotypes only, "
        "never real person legality allegations, no independently "
        "validated outcome, no runtime model promotion."
    ),
})
index["records_count"] = 7051
index["read_numbered_chapters"].append(117)
index["status"] = "BOOK_III_ESTATES_CONDUCT_HISTORICAL_ONLY_NEXT_DURABILITY"
index["next"] = {
    "pdf_page": 596,
    "printed_page_as_seen": 562,
    "chapter": "CXVIII",
    "printed_chapter_numeral": "CXVII",
    "heading": "If the Estate of the Native shall continue, or be Durable",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXVII begins lower first-edition PDF596/folio562 "
        "after a divider, continues into further original PDF pages "
        "that require new boundary review. The earlier printed "
        "folio561 is duplicated on original PDF594 and PDF595."
    ),
    "research_scope": (
        "Historical natal wealth durability/persistence, planet "
        "occupying second house and essential dignity, qualified "
        "malefic alternatives and directional change; source "
        "documentary only with no actual financial forecasts."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXVII_source_acceptance_note"] = (
    "B05p records R6995–R7051: 55 historical clause annotations "
    "plus 2 next-chapter navigation; 10 original source groups, "
    "SHA witnesses and 21 source-replay tests. No real-person "
    "legality, criminality, wealth prediction validity or "
    "new runtime scoring rules."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 7051
assert index["read_numbered_chapters"] == list(range(1, 118))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# First-edition Lilly on estate acquisition conduct — original history only\n\n"
    + review
    + "\n## Canonical archive versus human validity\n\n"
    + "After verified publication: **7,051 Lilly + 1,066 "
    + "Ptolemy = 8,117 historical source annotations**. "
    + "The original scans and 21 extracted-archive source tests "
    + "confirm documentary preservation; not a single human "
    + "wealth, criminality or ethical forecast was validated. "
    + "No source-lane runtime rule is promoted.\n"
)
PROGRESS.write_text(
    "# Lilly source through historical means of gaining wealth — 2026-10-17\n\n"
    "After authenticated publication **8,117 historical source "
    "annotations** (7,051 Lilly + 1,066 Ptolemy), first-edition "
    "frontier PDF596/894 (**~66.7% scan-position proxy**, not "
    "the percentage of predictive science complete). Printed "
    "CHAP CXVI lawful/indirect estate acquisition preserved in "
    "57 source notes, with mixed/conflicting planetary testimony "
    "and timing exceptions; no real-world legal, ethical or "
    "financial classifications validated and no runtime "
    "promotions. Following printed CXVII wealth durability "
    "begins lower PDF596. Numerical and blinded test lanes open.\n\n---\n\n"
    + (BACKUP / "PROGRESS_BEFORE_B05p.md").read_text()
)
CURRENT.write_text(
    "# Lilly first-edition historical acquisition-conduct study accepted, durability next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. R6995–R7051 source-first "
    "admitted locally; after GitHub verification 7,051 Lilly "
    "+ 1,066 Ptolemy = 8,117 historical annotations. "
    "Qualifiers on lawful vs indirect acquisition are "
    "unsupported historical judgments and never evidence "
    "about anyone's conduct. 21 archive-replayed documentary "
    "tests, no independent human forecasts, no runtime "
    "source rules promoted. NEXT original printed CXVII "
    "wealth durability on PDF596.\n\n---\n\n"
    + (BACKUP / "CURRENT_BEFORE_B05p.md").read_text()
)
receipt = {
    "batch": "B05p",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "previous_git_blob": old_blob,
    "previous_index_sha256": sha(BACKUP / "INDEX_BEFORE_B05p.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_report_sha256": sha(LATEST),
    "progress_report_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": released["archive_sha256"],
    "lilly_if_published": 7051,
    "ptolemy_retained": 1066,
    "combined_if_published": 8117,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
