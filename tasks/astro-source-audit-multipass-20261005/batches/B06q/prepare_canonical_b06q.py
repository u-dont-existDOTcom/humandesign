#!/usr/bin/env python3
"""Guarded first-edition child-count source admission: original and unverified."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06q_CHILDREN_COUNT.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06q.json"):
    assert not p.exists(), f"Duplicate or interrupted source admission: {p}"

idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
chinese = j(CHINESE)

assert idx["records_count"] == a["previous_lilly"] == 8602
assert idx["read_numbered_chapters"] == list(range(1, 139))
assert idx["batches"][-1]["id"] == "B06p"
assert idx["next"]["chapter"] == "CXXXIX"
assert idx["next"]["printed_chapter_numeral"] == "CXXXVIII"
assert idx["next"]["pdf_page"] == 638
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06q" for x in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 78
assert [x["record_number"] for x in r["rules"]] == list(range(8603, 8681))
assert [x["id"] for x in r["rules"] if x["role"] == "next_section_navigation"] == ["R8679", "R8680"]
assert r["substantive"] == a["substantive"] == 76
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 8680
assert a["combined_if_published"] == 9746
assert w["body_pdf_frames"] == [638, 639, 640]
assert w["following_unnumbered_ninth_house_start_pdf"] == 640
assert w["following_printed_CXXXIX_heading_pdf"] == 640
assert len(mapdata["source_groups"]) == mapdata["source_groups_count"] == 6
assert not limits["original_glyphs_fully_verified"]
assert not limits["original_ptolemy_disagreement_collated"]
assert not limits["medical_or_child_mortality_advice_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_actual_live_birth_count_validated"]
        or x["independent_child_sex_accuracy_validated"]
        or x["independent_child_survival_age_validated"]
        or x["independent_parent_child_emotional_accuracy_validated"]
        or x["clinical_health_or_child_mortality_forecast_authorized"]
        or x["person_level_moral_or_gender_label_authorized"]
        or x["ptolemy_source_attribution_independently_verified"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 25 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06q.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06q.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06q.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06q",
        "path": "batches/B06q/RULES.json",
        "records_count": 78,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly first edition 1647 printed "
            "CHAP CXXXVIII/editorial CXXXIX How many Children "
            "Native may have, original PDF638 lower through "
            "PDF640 upper, 6 original source passage groups. "
            "76 substantive historical annotated clauses, "
            "two next unnumbered/numbered source navigation "
            "R8603–R8680. Historic count predicts plurality "
            "from fruitful planets fifth/eleventh fertile signs, "
            "bicorporeal doubling vs fertile tripling with "
            "unresolved overlap and baseline. Historical male "
            "planet vs female Moon/Venus and signs/houses/degrees "
            "claims, child lifespan/behavior/social standing and "
            "parent-child love from first/fifth ruler aspects. "
            "ALBUBATER-attributed unverified original mortality "
            "aphorisms are retained with multivalued child "
            "death/no child/fewer children effects and glyph "
            "uncertainty, never clinical or mortal forecasts. "
            "Critically Lilly says others departed Ptolemy's "
            "child judgments, which he attributes to 10th, "
            "11th, 4th and 5th houses, signs and planets: "
            "NOT corroboration and original Ptolemy not collated. "
            "Distinct immediate UNNUMBERED ninth-house introduction "
            "starts mid original PDF640, while next printed CXXXIX "
            "travel chapter starts on SAME frame. ZERO human "
            "child count, sex, mortality, parental affection "
            "validations and zero scoring model promotions."
        ),
    }
)
idx["records_count"] = 8680
idx["read_numbered_chapters"].append(139)
idx["status"] = "BOOK_III_CHILD_NUMBER_SOURCE_NEXT_UNNUMBERED_NINTH_HOUSE"
idx["next"] = {
    "pdf_page": 640,
    "printed_page": 606,
    "chapter": "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS",
    "printed_chapter_numeral": None,
    "heading": "Judgments upon the ninth House. Of Journeys and Religions",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "This substantive UNNUMBERED ninth-house introduction "
        "begins after a double divider in the MIDDLE of "
        "original first-edition PDF640/printed606, "
        "following the last paragraphs of child counts. "
        "It ends on SAME PDF640 before a new divider "
        "and printed CHAP CXXXIX Whether Native shall "
        "travel or not. Do NOT advance the numbered "
        "chapter counter for the unnumbered introduction."
    ),
    "following_printed_chapter_numeral": "CXXXIX",
    "following_original_pdf_page": 640,
    "research_scope": (
        "Historical ninth house, ruler/occupants, Moon/Mercury "
        "and possible Mars, alleged journey frequency, "
        "distance, destinations, cause, fortunes/dangers and "
        "religious questions. Source only, not verified "
        "travel plans, risk, faith or individual predictions."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXIX_source_acceptance_note"] = (
    "B06q R8603–R8680 78 historic source records, "
    "six image-anchored groups original PDF638–643 "
    "photo SHA+bytes, 25 standalone ZIP replay tests. "
    "Preserved double/triple child-count sign "
    "multiplier overlap, unvalidated offspring "
    "sex and mortality, Ptolemy house-method disagreement. "
    "No human forecast or runtime promotion. "
    "Chinese 72 independent source notes."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8680
assert idx["read_numbered_chapters"] == list(range(1, 140))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original CXXXVIII child count historically documented\n\n"
    + review
    + "\n## Historical archive only, no child health claims validated\n\n"
    + "After verified GitHub publication **8,680 Lilly + "
    + "1,066 Ptolemy = 9,746 documentary source notes**. "
    + "25 original photo/standalone ZIP source-integrity tests "
    + "pass. Child count, sex, health, parent-child affection "
    + "and child lifespan are NOT validated forecasts. "
    + "No promoted runtime source rules. Chinese original "
    + "source tracks BaZi and Zi Wei retained separately.\n"
)
PROGRESS.write_text(
    "# Lilly original first edition through historic child count — 2026-10-17\n\n"
    "After remote verified publication **9,746 original historical "
    "source notes** (8,680 Lilly + 1,066 Ptolemy), first-edition "
    "physical scan frontier PDF640/894 (**71.6% by scanned-page "
    "position ONLY, not project or scientific completion**). "
    "Printed CXXXVIII adds 78 historic assertions, including "
    "unresolved twofold versus threefold child-count multipliers, "
    "gender-coded and high-stakes offspring longevity predictions, "
    "and Lilly's explicit disagreement with purported Ptolemy "
    "10/11/4/5-house method. No human predictive validation or "
    "runtime scoring promotion. NEXT original UNNUMBERED ninth "
    "house travel/religion introduction on PDF640, then printed "
    "CXXXIX travel also PDF640. Parallel Chinese BaZi 46 and "
    "Zi Wei 26 source-only notes independently indexed; full "
    "chart engines, blind tests, comparative baselines remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06q.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly child-count historical chapter documented; ninth-house intro next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source B06q R8603–R8680 "
    "accepted locally; after verified GitHub remote readback "
    "8,680 Lilly + 1,066 Ptolemy = 9,746 historical "
    "documentary notes. Original PDF640 of 894 scanned "
    "frames (71.6% physical position only). "
    "All 25 photo/source/archive replay checks pass. "
    "No verified offspring count, sex, health, mortality "
    "or parent-child relationship outcomes. "
    "Zero executable runtime model promotions. "
    "NEXT UNNUMBERED ninth-house journeys/religion "
    "introduction starts mid PDF640, next separately "
    "printed CXXXIX also PDF640. Chinese 72 source notes "
    "preserved in a separate index.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06q.md").read_text()
)
receipt = {
    "batch": "B06q",
    "status": "GUARDED_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06q.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8680,
    "ptolemy_retained": 1066,
    "combined_if_published": 9746,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
