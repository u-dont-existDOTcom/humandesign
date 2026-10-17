#!/usr/bin/env python3
"""Guarded append of original unnumbered ninth-house travel/religion source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06r_NINTH_HOUSE_INTRO.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06r.json"):
    assert not p.exists(), f"Duplicate or interrupted original-source admission: {p}"

idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
chinese = j(CHINESE)

assert idx["records_count"] == a["previous_lilly"] == 8680
assert idx["read_numbered_chapters"] == list(range(1, 140))
assert idx["batches"][-1]["id"] == "B06q"
assert idx["next"]["chapter"] == "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS"
assert idx["next"]["pdf_page"] == 640
assert idx["next"]["printed_chapter_numeral"] is None
assert idx["next"]["following_printed_chapter_numeral"] == "CXXXIX"
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06r" for x in idx["batches"])
assert r["record_count"] == a["new_historical_records"] == 25
assert [x["record_number"] for x in r["rules"]] == list(range(8681, 8706))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8704", "R8705"]
assert r["substantive"] == a["substantive"] == 23
assert a["numbered_chapters_added"] == 0
assert a["lilly_if_published"] == 8705
assert a["combined_if_published"] == 9771
assert w["unnumbered"] and w["body_pdf_frames"] == [640]
assert w["next_printed_CXXXIX_heading_pdf"] == 640
assert len(m["source_groups"]) == m["source_group_count"] == 5
assert not limits["religious_personality_judgment_in_this_section"]
assert not limits["original_ptolemy_mars_attribution_verified"]
assert not limits["real_person_safety_or_faith_predictions_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_travel_occurrence_or_frequency_validated"]
        or x["independent_travel_destination_or_cause_validated"]
        or x["independent_travel_success_or_danger_validated"]
        or x["real_person_faith_religion_or_safety_claim_authorized"]
        or x["ptolemy_travel_attribution_independently_verified"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 15 and sha(z["archive_path"]) == z["archive_sha256"]
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
(BACK / "INDEX_BEFORE_B06r.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06r.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06r.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06r",
        "path": "batches/B06r/RULES.json",
        "records_count": 25,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly Christian Astrology first edition "
            "UNNUMBERED ninth-house long Journeys and Religions "
            "introduction, original PDF640/printed606 middle, "
            "separate next printed CHAP CXXXIX travel also "
            "begins lower SAME page. 5 reversible source "
            "photo groups, 23 substantive historical questions "
            "and two next-printed navigation R8681–R8705. "
            "Ninth house/ruler, its occupants, Moon and Mercury, "
            "Lilly's unverified Ptolemy attribution of Mars. "
            "Enumerated outcomes: far travel yes/no, once/many, "
            "lifelong overseas vs rare, destination in relation "
            "to natal country and multiple destinations, "
            "motives, objective success and danger of death. "
            "Despite Religion heading no religion forecasts "
            "are supplied in this introductory passage. "
            "No independent human travel or life-risk success "
            "or executable source runtime rule."
        ),
    }
)
idx["records_count"] = 8705
# Unnumbered section must not increment numbered printed chapters.
assert idx["read_numbered_chapters"] == list(range(1, 140))
idx["status"] = "BOOK_III_UNNUMBERED_NINTH_TRAVEL_INTRO_NEXT_PRINTED_CXXXIX"
idx["next"] = {
    "pdf_page": 640,
    "printed_page": 606,
    "chapter": "CXL",
    "printed_chapter_numeral": "CXXXIX",
    "heading": "Whether the Native shall travell or not",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "The printed CHAP CXXXIX begins after a distinct "
        "horizontal divider toward bottom of original "
        "PDF640/printed606. It follows the UNNUMBERED "
        "ninth-house introduction on the SAME page and "
        "continues original PDF641 onward. Verify exact "
        "next printed chapter boundary before extraction."
    ),
    "research_scope": (
        "Original ninth-house travel yes/no rules, "
        "reciprocal ninth/first house lords and Moon/Mercury "
        "configuration, mutable vs fixed signs, travel "
        "frequency and geographic directions, with "
        "historic hazards and wealth outcomes unvalidated."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["unnumbered_ninth_house_source_acceptance_note"] = (
    "B06r R8681–R8705, 25 original historic source "
    "notes, 5 reversible source groups original "
    "PDF640–642 photo SHA, 15 original and ZIP-extracted "
    "replay tests. Religions heading but only travel "
    "questions specified, Ptolemy Mars attribution "
    "unverified and no real-person faith, travel or "
    "danger predictions. Numbered chapter count "
    "unchanged; Chinese 72 annotations separate."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8705
assert idx["read_numbered_chapters"] == list(range(1, 140))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original unnumbered ninth-house travel introduction documented\n\n"
    + review
    + "\n## Documentary source, not travel or faith predictive validity\n\n"
    + "After verified source publication **8,705 Lilly + "
    + "1,066 Ptolemy = 9,771 historical documentary notes**. "
    + "15 original photo and independently ZIP-extracted "
    + "source tests pass. No human travel, geographical "
    + "direction, faith or personal hazard result "
    + "independently validated. Zero executable "
    + "runtime source rules promoted.\n"
)
PROGRESS.write_text(
    "# Lilly first edition through unnumbered ninth-house intro — 2026-10-17\n\n"
    "After authenticated publication **9,771 historical "
    "source records** (8,705 Lilly + 1,066 Ptolemy). "
    "Physical book frontier PDF640/894 (**71.6% scanned "
    "page position ONLY, not whole scientific project**). "
    "25 original source annotations include 9th house "
    "travel indicators and four separate question groups, "
    "no religion classification in the source body, "
    "and purported Mars-attribution to Ptolemy unverified. "
    "Numbered chapter counter unchanged because this "
    "section has no original printed chapter numeral. "
    "Next separately printed CHAP CXXXIX travel begins "
    "lower on SAME PDF640. No predictive human "
    "success or runtime rules. Independent Chinese "
    "BaZi 46 and Zi Wei 26 source-only records remain "
    "separate and full chart engines/blinded studies OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06r.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly ninth-house travel introduction documented; CXXXIX next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06r unnumbered "
    "original ninth-house source R8681–R8705 accepted locally. "
    "After remote readback 8,705 Lilly +1,066 Ptolemy "
    "= 9,771 historical source annotations. "
    "15 source and independent ZIP replay tests pass; "
    "no travel/faith/life-safety real-world prediction "
    "validated, no runtime model promotions. "
    "Printed numbered chapter total unchanged. "
    "Next printed CXXXIX on travel from PDF640 lower. "
    "Chinese BaZi 46 and Zi Wei 26 historical "
    "source records independently indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06r.md").read_text()
)
receipt = {
    "batch": "B06r",
    "status": "GUARDED_UNNUMBERED_SOURCE_PREPARED_PENDING_REMOTE",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06r.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8705,
    "ptolemy_retained": 1066,
    "combined_if_published": 9771,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
