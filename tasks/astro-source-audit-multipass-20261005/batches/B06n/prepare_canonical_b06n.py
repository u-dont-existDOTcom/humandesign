#!/usr/bin/env python3
"""Guarded append-only 1647 Lilly source: spouse survival-order claims."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06n_SPOUSE_SURVIVAL.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06n.json"):
    assert not path.exists(), f"Duplicate or interrupted source admission: {path}"

idx = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
archive = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
chinese = read(CHINESE)

assert idx["records_count"] == a["prior_lilly"] == 8343
assert idx["read_numbered_chapters"] == list(range(1, 137))
assert idx["batches"][-1]["id"] == "B06m"
assert idx["next"]["chapter"] == "CXXXVII"
assert idx["next"]["printed_chapter_numeral"] == "CXXXVI"
assert idx["next"]["pdf_page"] == 633
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06n" for x in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 54
assert [x["record_number"] for x in r["rules"]] == list(range(8344, 8398))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8396", "R8397"]
assert a["new_numbered_chapters"] == 1
assert r["substantive"] == a["substantive"] == 52
assert a["lilly_if_published"] == 8397
assert a["combined_if_published"] == 9463
assert len(m["source_groups"]) == 6
assert w["body_pdf_frames"] == [633, 634]
assert w["following_printed_CXXXVII_heading_pdf"] == 634
assert not limits["real_person_lifespan_danger_or_illness_predictions_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_spousal_mortality_accuracy_validated"]
        or x["independent_spousal_illness_accuracy_validated"]
        or x["independent_pair_survival_order_validated"]
        or x["real_human_danger_or_abuse_label_authorized"]
        or x["medical_lifespan_forecast_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == archive["accepted_rules_sha256"]
assert archive["crc_passed"] and archive["sha256_passed"] and archive["extraction_passed"]
assert archive["replayed_tests"] == 17
assert sha(archive["archive_path"]) == archive["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
assert chinese["runtime_promotions"] == 0
assert chinese["independently_validated_real_human_claims"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06n.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06n.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06n.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06n",
        "path": "batches/B06n/RULES.json",
        "records_count": 54,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original first-edition William Lilly printed CHAP CXXXVI/editorial "
            "CXXXVII Whether Native or his Wife shall dye first, mid "
            "PDF633/printed599 through upper PDF634/printed600. "
            "Six reversible source photo groups, 52 substantive historical "
            "claims/qualifiers and two next chapter navigation, R8344–R8397. "
            "Historical source alleges wife death OR long infirmities from "
            "seventh ruler afflicted/in cadent houses; source surprisingly "
            "singles out SECOND as cadent although second is not cadent. "
            "Exactly one lunar companion plus strength of Moon or planet "
            "allegedly reverses husband/wife death-order. Moon fourth, "
            "Moon separated Mars applying Venus in west, Moon/Venus "
            "conjunct Saturn in seventh, Venus fourth under Mars/Saturn "
            "aspects and movable sign, Moon seventh harsh malefic contact "
            "with explicit absence of Jupiter/Venus help; Venus "
            "occidental/peregrine malefic, ruler cadent or eighth and "
            "peregrine malefic variants. Source also claims multiple "
            "wives, difficulty marrying, alleged spouse mistreatment "
            "and enemy deaths as alternative outcomes. "
            "No single real-person mortality or dangerous-partner forecast "
            "authorized and zero independently validated human predictions "
            "or executable scoring promotions."
        ),
    }
)
idx["records_count"] = 8397
idx["read_numbered_chapters"].append(137)
idx["status"] = "BOOK_III_HISTORIC_SPOUSE_MORTALITY_NEXT_WOMENS_MARRIAGE"
idx["next"] = {
    "pdf_page": 634,
    "printed_page": 600,
    "chapter": "CXXXVIII",
    "printed_chapter_numeral": "CXXXVII",
    "heading": "Of the Marriage of Women",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "First edition printed CHAP CXXXVII begins after distinct "
        "horizontal divider middle original PDF634/printed600. "
        "Continues across subsequent photos; verify physical "
        "ending and next printed chapter before accepting. "
        "Historical source intentionally changes women-specific "
        "significators to Sun and Mars versus earlier male natal "
        "Venus/Moon. Do not conflate outcomes or modern identities."
    ),
    "research_scope": (
        "Claims of women's marriage occurrence, gender-coded "
        "marriage signifiers, fertile/barren signs and houses, "
        "desire/aversion and multiple prospective partners, "
        "with original negative exceptions and source timing. "
        "Historical social/sexual stereotypes only, never "
        "verified private life or medically actionable advice."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXVII_source_acceptance_note"] = (
    "B06n source R8344–R8397, 54 original period claims, "
    "original PDF633–634 SHA photographs and 17 archive-replayed "
    "tests. Explicit second house/cadent anomaly and "
    "wife death OR illness, multiple wife and alleged abuse "
    "alternatives remain quarantined. Chinese 72 source notes "
    "separate; zero human mortality validation and runtime promotions."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8397
assert idx["read_numbered_chapters"] == list(range(1, 138))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Original Lilly spouse death-order chapter: period text, never prognosis\n\n"
    + review
    + "\n## Historical document integrity only\n\n"
    + "After authenticated GitHub publication **8,397 Lilly + "
    + "1,066 Ptolemy = 9,463 historical documentary notes**. "
    + "17 source image and replayed ZIP integrity tests pass. "
    + "No independently validated real spouse deaths, illness "
    + "or treatment risk, and no promoted runtime model "
    + "rules. Separate Chinese BaZi and Zi Wei "
    + "source notes are preserved.\n"
)
PROGRESS.write_text(
    "# Lilly original 1647 through spouse survival order — 2026-10-17\n\n"
    "After verified source publication **9,463 historical "
    "documentary notes** (8,397 Lilly + 1,066 Ptolemy), "
    "first-edition source frontier PDF634/894 "
    "(**70.9% physical scanned-position only**). "
    "Source batch B06n adds 54 period assertions including "
    "a second-house cadent contradiction and high-stakes "
    "death/illness, marriage count and conduct alternatives. "
    "No real human death, medical, or couple-safety "
    "predictive accuracy demonstrated or model promoted. "
    "NEXT printed CXXXVII on women's marriage PDF634 onward. "
    "Parallel independent Chinese source lanes "
    "BaZi 46 + Zi Wei 26 annotations and partial mechanics "
    "remain open; do not add them to Western counts.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06n.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly spouse death-order source documented; women's marriage next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06n accepted "
    "original period-source R8344–R8397. After remote "
    "verification Lilly 8,397 + Ptolemy 1,066 = "
    "9,463 historic notes. No verified human mortality, "
    "partner abuse or health forecasts and no source "
    "runtime promotions. Chinese source-only 46 BaZi "
    "+ 26 Zi Wei remain independent. NEXT printed "
    "CXXXVII women's marriage, original PDF634 onward.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06n.md").read_text()
)
receipt = {
    "batch": "B06n",
    "status": "GUARDED_SOURCE_CANONICAL_PREPARED_PENDING_REMOTE",
    "old_index_git_blob": old_blob,
    "old_index_sha256": sha(BACK / "INDEX_BEFORE_B06n.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "lilly_if_published": 8397,
    "ptolemy_retained": 1066,
    "combined_if_published": 9463,
    "separate_chinese_historical_notes": 72,
    "human_mortality_accuracy_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
