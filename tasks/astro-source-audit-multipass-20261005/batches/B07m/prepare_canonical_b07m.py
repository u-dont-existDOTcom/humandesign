#!/usr/bin/env python3
"""Guard original first-edition unnumbered directions source in historical index."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07m_EFFECTS_DIRECTIONS.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07m.json"):
    assert not path.exists(), f"Duplicate/interrupted source index preparation: {path}"

index = read(INDEX)
acc = read(B / "ACCEPTANCE.json")
rules = read(B / "RULES.json")
photos = read(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = read(B / "SOURCE_TO_RECORD_MAP.json")
issues = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
firewall = read(B / "DIRECTIONS_EMPIRICAL_FIREWALL_V1.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = read(CHINESE)

assert index["records_count"] == acc["prior_lilly"] == 10468
assert index["batches"][-1]["id"] == "B07l"
assert index["read_numbered_chapters"] == list(range(1, 156))
assert index["next"]["chapter"] == "THE_EFFECTS_OF_DIRECTIONS"
assert index["next"]["pdf_page"] == 685
assert index["next"]["printed_chapter_numeral"] is None
assert index["next"]["following_printed_chapter_numeral"] == "CLVII"
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B07m" for x in index["batches"])
assert rules["record_count"] == acc["new_historical_annotations"] == 127
assert [x["record_number"] for x in rules["rules"]] == list(range(10469, 10596))
assert [x["id"] for x in rules["rules"] if x["role"] == "next_printed_navigation"] == [
    "R10594",
    "R10595",
]
assert rules["substantive"] == acc["substantive"] == 125
assert acc["numbered_chapters_added"] == 0
assert acc["lilly_if_published"] == 10595
assert acc["combined_if_published"] == 11661
assert photos["body_original_pdf_frames"] == [685, 686, 687, 688]
assert photos["following_printed_CLVII_heading_pdf"] == 688
assert photos["following_printed_CLVIII_heading_pdf"] == 690
assert len(mapdata["source_groups"]) == mapdata["source_group_count"] == 8
assert not issues["source_direction_geometry_and_year_key_verified"]
assert not issues["authorial_five_vs_ten_number_ambiguity_resolved"]
assert not issues["all_original_technical_sources_cross_collated"]
assert not firewall["full_mathematical_calculator_parity_verified"]
assert firewall["independently_tested_real_humans"] == 0
assert firewall["runtime_model_promotions"] == 0
assert rules["empirical_validations"] == acc["empirical_validations"] == 0
assert rules["runtime_promotions"] == acc["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in rules["rules"])
assert sha(B / "RULES.json") == acc["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "DIRECTIONS_EMPIRICAL_FIREWALL_V1.json") == acc["firewall_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 36
assert sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
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
for path, name in (
    (INDEX, "INDEX_BEFORE_B07m.json"),
    (CURRENT, "CURRENT_BEFORE_B07m.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07m.md"),
):
    (BACK / name).write_bytes(path.read_bytes())

index["batches"].append(
    {
        "id": "B07m",
        "path": "batches/B07m/RULES.json",
        "records_count": 127,
        "sha256": acc["rules_sha256"],
        "scope": (
            "First edition original 1647 Lilly major UNNUMBERED "
            "THE EFFECTS OF DIRECTIONS original PDF685–688 "
            "printed651–654 after death chapter CLVI "
            "and BEFORE independently printed CLVII "
            "on original PDF688. Eight reversible "
            "photographed source groups, 125 substantive "
            "historical clauses and two CLVII navigation "
            "R10469–R10595. Direction encounter between "
            "Significator and Promittor, alleged calendar "
            "year/month/week/day forecasts of office/"
            "marriage/journey/property, mathematically "
            "attributed Regiomontanus, Argolus and others "
            "but NO COMPLETE direction calculator in Lilly. "
            "CRITICAL source admission timing misses, "
            "blaming operator and inadequate natal "
            "rectification; two/three Ascendant degrees "
            "allegedly move events by YEARS. "
            "Freeze fitting events separately from untouched "
            "holdout forecasts, no post-hoc corrections. "
            "Five-places wording followed by TEN explicitly "
            "numbered Asc/Moon/Sun/MC/Fortuna/Saturn/"
            "Jupiter/Mars/Venus/Mercury objects. "
            "Sun/Moon, MC, Fortune and planets each "
            "have numerous alternate event topics; "
            "Lilly explicitly REJECTS Part of Fortune "
            "bodily-effects source. ZERO independent "
            "actual human timed-event validity, "
            "zero executable runtime source promotions."
        ),
    }
)
index["records_count"] = 10595
index["status"] = "BOOK_III_UNNUMBERED_EFFECTS_OF_DIRECTIONS_NEXT_PRINTED_CLVII"
index["next"] = {
    "pdf_page": 688,
    "printed_page": 654,
    "chapter": "CLVII",
    "printed_chapter_numeral": "CLVII",
    "heading": "How long the Effects of a Direction shall last",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Separately printed CHAP CLVII starts below "
        "divider original first-edition PDF688/"
        "printed654, AFTER substantive unnumbered "
        "Effects of Directions source ends. "
        "Continues PDF689/printed655 and ends "
        "before separate CHAP CLVIII on original "
        "PDF690/printed656. Verify complete original "
        "CLVII conditions before advancing."
    ),
    "research_scope": (
        "Historical duration/strength and size of "
        "effects of a direction by distinct "
        "Significator and Promittor essential dignity, "
        "angles and accidental strength, and relative "
        "strength/weakness. No validated human "
        "predictions, numerical date conversion or "
        "actual-life medical/mortality inference."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["unnumbered_effects_directions_source_acceptance_note"] = (
    "B07m historical R10469–R10595, "
    "127 source-only notes/8 reversible "
    "photo groups PDF685–690 image SHA/bytes, "
    "36 standalone ZIP-extracted tests. "
    "Author explicitly says 2–3 Ascendant "
    "degrees can shift events YEARS and "
    "external tables/math required. "
    "Five-versus-ten source wording and "
    "Fortuna body effect rejection preserved. "
    "No real life-event predictive accuracy "
    "or runtime source promotions; Chinese "
    "72 source-only notes separate."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 10595
assert index["read_numbered_chapters"] == list(range(1, 156))
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly 1647 Effects of Directions source documented\n\n"
    + review
    + "\nAfter authenticated GitHub publication "
    + "10,595 Lilly +1,066 Ptolemy=11,661 "
    + "documentary source notes, 36 photo/ZIP "
    + "archive tests pass. None of the human "
    + "event timing, medical or morality "
    + "predictions validated, no executable "
    + "source scorer promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 directions effects through PDF688 — 2026-10-18\n\n"
    "After verified publication 11,661 historical "
    "original-source annotations (10,595 Lilly "
    "+1,066 Ptolemy), original PDF688/894 "
    "(~77.0% physical scanned position ONLY, "
    "not total research/predictive completion). "
    "B07m 127 source-only notes preserve "
    "Significator/Promittor timing claims, "
    "Lilly's acknowledged misses and critical "
    "2–3° Ascendant rectification shifting "
    "alleged event timing by YEARS. "
    "No original numerical Regiomontanus/"
    "Argolus parity, no frozen prospective "
    "event tests, zero human successes or "
    "source runtime promotions. "
    "Next printed CLVII effects-duration "
    "PDF688–689, printed CLVIII from PDF690. "
    "Separate Chinese BaZi46, ZiWei26 "
    "historic source-only notes remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07m.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly unnumbered Effects of Directions documented; CLVII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07m source R10469–R10595 locally "
    "admitted pending verified GitHub push; "
    "then 10,595 Lilly+1,066 Ptolemy=11,661 "
    "source-only historical notes. "
    "36 original photo/ZIP tests pass, "
    "no actual human event prediction "
    "accuracy or runtime promotion. "
    "Critical original warning about birth-time "
    "rectification/forecast drift by years. "
    "Next printed CLVII duration of directions "
    "from PDF688. Chinese historical BaZi46/"
    "ZiWei26 remain independently indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07m.md").read_text()
)
receipt = {
    "batch": "B07m",
    "status": "GUARDED_ORIGINAL_EFFECTS_DIRECTIONS_SOURCE_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B07m.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "directions_firewall_sha256": sha(B / "DIRECTIONS_EMPIRICAL_FIREWALL_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10595,
    "ptolemy_retained": 1066,
    "combined_if_published": 11661,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
