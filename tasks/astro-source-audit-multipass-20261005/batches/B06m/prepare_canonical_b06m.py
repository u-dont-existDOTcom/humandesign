#!/usr/bin/env python3
"""Guarded append-only original 1647 source acceptance: marital concord."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06m_MARITAL_CONCORD.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06m.json"):
    assert not path.exists(), f"Interrupted or duplicate archival admission: {path}"

idx = read(INDEX)
accepted = read(B / "ACCEPTANCE.json")
rules = read(B / "RULES.json")
photos = read(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
archive = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
chinese = read(CHINESE)

assert idx["records_count"] == accepted["previous_lilly"] == 8272
assert idx["read_numbered_chapters"] == list(range(1, 136))
assert idx["batches"][-1]["id"] == "B06l"
assert idx["next"]["chapter"] == "CXXXVI"
assert idx["next"]["printed_chapter_numeral"] == "CXXXV"
assert idx["next"]["pdf_page"] == 631
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06m" for x in idx["batches"])
assert rules["record_count"] == accepted["new_historical_annotations"] == 71
assert [x["record_number"] for x in rules["rules"]] == list(range(8273, 8344))
assert [x["id"] for x in rules["rules"] if x["role"] == "next_chapter_navigation"] == [
    "R8342",
    "R8343",
]
assert rules["substantive"] == 69 and accepted["new_numbered_chapters"] == 1
assert accepted["lilly_if_published"] == 8343
assert accepted["combined_if_published"] == 9409
assert len(mapdata["source_groups"]) == 7
assert photos["body_pdf_frames"] == [631, 632, 633]
assert photos["following_printed_CXXXVI_heading_pdf"] == 633
assert not limits["complete_pair_geometry_engine_verified"]
assert not limits["intimate_or_moral_real_partner_claims_authorized"]
assert rules["empirical_validations"] == accepted["empirical_validations"] == 0
assert rules["runtime_promotions"] == accepted["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_marital_concord_validated"]
        or x["independent_real_couple_pair_chart_accuracy_validated"]
        or x["real_partner_fidelity_morality_jealousy_claim_authorized"]
        or x["private_safety_or_intimate_inference_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in rules["rules"]
)
assert sha(B / "RULES.json") == accepted["rules_sha256"] == archive["accepted_rules_sha256"]
assert archive["crc_passed"] and archive["sha256_passed"] and archive["extraction_passed"]
assert archive["replayed_tests"] == 22
assert sha(archive["archive_path"]) == archive["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
assert chinese["independently_validated_real_human_claims"] == 0
assert chinese["runtime_promotions"] == 0

relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06m.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06m.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06m.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06m",
        "path": "batches/B06m/RULES.json",
        "records_count": 71,
        "sha256": accepted["rules_sha256"],
        "scope": (
            "William Lilly original printed CHAP CXXXV/editorial "
            "CXXXVI On mutual love and concord of Man and Wife, "
            "original PDF631 lower to PDF633 upper, before "
            "separately printed CHAP CXXXVI whether spouse dies first. "
            "Seven reversible photograph passage groups with "
            "69 substantive historical clauses and two "
            "following heading navigation R8273-R8343. "
            "Fortune/malefic planet and friendly/hard aspect "
            "Moon contrast with intermediate mixed-nature outcomes; "
            "original aspect scope restricted to Moon and "
            "Lord Seventh. Stronger mode compares two independently "
            "acquired Genitures, wife's Sun same zodiac sign AND "
            "exact degree as man's Moon or wife's Moon at man's Sun, "
            "not simply same-sign astrology. Sextile/trine versus "
            "square/opposition; period unsupported jealousy, "
            "infidelity, sexual and class stereotypes from "
            "Venus/Saturn/Mars, Venus twelfth, mutable/common signs, "
            "Moon-Mars with waning and source-defined signs; "
            "qualified conjunction of Moon Sun humane signs with "
            "benefic aspects across page seam, and seventh-ruled "
            "waning Moon in eighth. No actual relationship, "
            "private fidelity or pairwise natal predictions "
            "verified; zero runtime promotions."
        ),
    }
)
idx["records_count"] = 8343
idx["read_numbered_chapters"].append(136)
idx["status"] = "BOOK_III_MARITAL_CONCORD_HISTORICAL_NEXT_SPOUSE_DEATH_ORDER"
idx["next"] = {
    "pdf_page": 633,
    "printed_page": 599,
    "chapter": "CXXXVII",
    "printed_chapter_numeral": "CXXXVI",
    "heading": "Whether the Native or his Wife shall dye first",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original printed CHAP CXXXVI on marital death-order "
        "begins after divider middle original PDF633/printed599. "
        "Its text continues into upper PDF634/printed600; "
        "next distinct printed CHAP CXXXVII on women's "
        "marriages starts below divider middle PDF634. "
        "Do not double-count mortality material as CXXXV "
        "source and do not issue real person death predictions."
    ),
    "following_printed_chapter_numeral": "CXXXVII",
    "following_original_pdf_page": 634,
    "research_scope": (
        "High-stakes unsupported first-marital-death source "
        "from Lord Seventh, affliction, stronger Moon versus "
        "one conjunction, lunar fourth and eighth, Venus/Saturn "
        "and duration; explicitly do not infer any individual's "
        "lifespan, death, relationship danger or need for treatment."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXVI_source_acceptance_note"] = (
    "B06m R8273-R8343: 71 historical source notes, "
    "seven groups, original PDF631-634 photographic SHA "
    "and 22 independent archive-extracted documentary "
    "tests; exact two-Geniture Sun/Moon sign+degree "
    "contact preserved apart from vague single-natal "
    "marital stereotypes; no real couples verified "
    "and no runtime rules promoted. Chinese 72 notes separate."
)
assert idx["records_count"] == sum(item["records_count"] for item in idx["batches"]) == 8343
assert idx["read_numbered_chapters"] == list(range(1, 137))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original 1647 mutual marital love source historically documented\n\n"
    + review
    + "\n## Historic source not real human relationship data\n\n"
    + "After remote GitHub publication **8,343 Lilly "
    + "+ 1,066 Ptolemy = 9,409 historical source "
    + "annotations**. Original PDF631-634 photo witnesses "
    + "and 22 archive-replayed integrity tests pass. "
    + "No actual couples' affection, fidelity or marital "
    + "concord predictions independently validated. "
    + "Zero model promotions. Chinese BaZi and Zi Wei "
    + "source study preserved separately.\n"
)
PROGRESS.write_text(
    "# Lilly 1647 original through marriage concord — 2026-10-17\n\n"
    "After verified publication **9,409 historical "
    "source records** (8,343 Lilly + 1,066 Ptolemy), "
    "physical source frontier PDF633/894 "
    "(**70.8% first-edition page-position only**, "
    "not progress of numeric astronomy or predictive science). "
    "Source batch B06m adds 71 historical notes on "
    "marital love, mixed benign/hostile aspect rules, "
    "two independently obtained Genitures and "
    "precise wife-Sun versus husband-Moon same-degree "
    "contact, with extensive period claims about "
    "sexuality, fidelity and satisfaction UNVALIDATED. "
    "No runtime scorer changes. Next printed CXXXVI "
    "on marital death-order from PDF633, high-stakes "
    "source-only, later printed CXXXVII women's "
    "marriage from PDF634. Chinese BaZi 46 and "
    "Zi Wei 26 source-only records separately "
    "indexed and awaiting complete chart engines.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06m.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly mutual marriage concord documented; death-order next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. After "
    "remote publication B06m source R8273-R8343 "
    "makes 8,343 Lilly and 1,066 Ptolemy = 9,409 "
    "historical documents, with zero independent "
    "couple predictions and zero runtime scoring "
    "promotions. Next printed CHAP CXXXVI from "
    "original PDF633. Chinese BaZi 46, Zi Wei 26 "
    "source notes remain independently indexed "
    "under the same HumanDesign branch.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06m.md").read_text()
)
receipt = {
    "batch": "B06m",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06m.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "lilly_if_published": 8343,
    "ptolemy_retained": 1066,
    "combined_if_published": 9409,
    "separate_chinese_source_notes": 72,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
