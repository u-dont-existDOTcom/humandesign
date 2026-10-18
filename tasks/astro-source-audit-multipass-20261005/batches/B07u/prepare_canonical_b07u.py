#!/usr/bin/env python3
"""One-time guarded acceptance of original Lilly CLXIIII lunar-promittor source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07u_MOON_PROMITTORS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def download_dir():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


for file in (RECEIPT, LATEST, BACK / "INDEX_BEFORE_B07u.json"):
    assert not file.exists(), f"Already partly prepared or accepted. Reconcile {file}"
assert git("branch", "--show-current") == "research/astro-b07u-moon-promittors-20261018"
idx = load(INDEX)
window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
acc = load(B / "ACCEPTANCE.json")
auth = load(B / "SOURCE_FIRST_AUTHORING_20261018.json")
mapping = load(B / "SOURCE_TO_RECORD_MAP.json")
witness = load(B / "ORIGINAL_SOURCE_WITNESS.json")
guard = load(B / "HISTORICAL_NONPROMOTION_GUARD_V1.json")
archive = load(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
china = load(CHINA)

assert sha(INDEX) == window["previous_index_sha256"] == archive["prior_index_sha256"]
assert idx["records_count"] == acc["prior_lilly"] == window["accepted_lilly_before"] == 11825
assert idx["batches"][-1]["id"] == "B07t"
assert idx["next"]["chapter"] == "CLXIIII"
assert idx["next"]["pdf_page"] == 725
assert idx["read_numbered_chapters"] == list(range(1, 163))
assert idx["source_sha256"] == window["full_source_pdf_sha256"]
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(b["id"] == "B07u" for b in idx["batches"])
assert rules["record_count"] == acc["new_historical_annotations"] == 343
assert (rules["substantive"], rules["following_navigation"]) == (341, 2)
assert [r["record_number"] for r in rules["rules"]] == list(range(11826, 12169))
assert [r["role"] for r in rules["rules"][-2:]] == [
    "next_unnumbered_moon_stars",
    "next_moon_rigel",
]
assert len(auth["groups"]) == len(mapping["source_groups"]) == acc["source_group_count"] == 41
assert len(witness["photos"]) == acc["source_images_count"] == 12
assert witness["body_original_pdf_frames"] == list(range(725, 736))
assert witness["following_unnumbered_heading_pdf"] == 735
assert window["following_heading_numbered"] is False
assert sha(B / "RULES.json") == acc["rules_sha256"] == archive["rules_sha256"]
assert guard["printed_numbered_chapter_separated_from_unnumbered_star_section"] is True
assert guard["individual_human_predictions_validated"] == guard["runtime_model_promotions"] == 0
assert archive["crc_passed"] and archive["sha256_and_bytes_passed"]
assert archive["independent_extraction_passed"]
assert archive["replayed_documentary_tests"] == 80
assert archive["replayed_source_window_tests"] == 28
assert archive["total_replayed_tests"] == 108
assert sha(download_dir() / archive["filename"]) == archive["archive_sha256"]
assert china["sum_source_annotations"] == 97
assert china["independently_validated_real_human_claims"] == 0
assert china["runtime_promotions"] == 0
for file in (
    INDEX,
    CHINA,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07t/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file))
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"])

BACK.mkdir(exist_ok=False)
for file, basename in (
    (INDEX, "INDEX_BEFORE_B07u.json"),
    (CURRENT, "CURRENT_BEFORE_B07u.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07u.md"),
    (CHINA, "CHINESE_V2_BEFORE_B07u.json"),
):
    (BACK / basename).write_bytes(file.read_bytes())

idx["batches"].append(
    {
        "id": "B07u",
        "path": "batches/B07u/RULES.json",
        "records_count": 343,
        "sha256": acc["rules_sha256"],
        "scope": (
            "Original 1647 first-edition printed CHAP CLXIIII Directions of "
            "the Moon to PROMITTORS starts BELOW CLXIII divider PDF725/printed691 "
            "and ends PDF735/printed701 ABOVE the independent UNNUMBERED Moon "
            "Directed to FIXED STARRES heading on SAME page. Exactly 343 "
            "source-only historical annotations R11826-R12168, 341 substantive "
            "and 2 unnumbered next-unit navigation, in 41 reversible original "
            "photo-anchored passage groups. Original image witnesses PDF725-736 "
            "hash/bytes and Poppler provenance preserved. Moon to Saturn, "
            "Jupiter, Mars, Sun, Venus and Mercury bodies, original aspects "
            "and planetary terms where printed; lunar North and South Nodes, "
            "Part Fortune, all 12 individual house cusps. Natal/radix/class/"
            "gender/family, Hyleg/Anareta, old stellar, sign and occupation "
            "conditions and favorable/adverse alternatives kept explicit. "
            "Original disease, crime, death, finances and moral claims are "
            "historical-only: no real-human prediction, no direction calendar "
            "engine and no live runtime promotions. The owner ZIP archive "
            "CRC/SHA/bytes and 108 independently extracted source tests pass. "
            "Separate Chinese V2 97 notes and 1,066 Ptolemy retained."
        ),
    }
)
idx["records_count"] = 12168
idx["read_numbered_chapters"].append(163)
idx["status"] = "BOOK_III_PRINTED_CLXIIII_MOON_PROMITTORS_NEXT_UNNUMBERED_MOON_FIXED_STARS"
idx["next"] = {
    "pdf_page": 735,
    "printed_page": 701,
    "chapter": "UNNUMBERED_MOON_FIXED_STARRES",
    "printed_chapter_numeral": None,
    "numbered": False,
    "heading": "The Moon Directed to FIXED STARRES",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Unnumbered centered Moon Directed to FIXED STARRES heading starts "
        "PDF735/printed701 BELOW final twelfth-house cusp paragraph of "
        "numbered CLXIIII. Beginning Rigel passage on same page and "
        "continuation PDF736 already photographed. Locate its exact "
        "following heading/page before source acceptance. Do NOT invent "
        "CHAP CLXV at this boundary. Next first historical ID R12169."
    ),
    "research_scope": (
        "Lunar directions to historical fixed stars only, followed by "
        "separate direction-annual-measure numerical table source; zero "
        "verified modern stellar epoch/time engine or human prediction."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CLXIIII_moon_promittors_source_acceptance_note"] = (
    "B07u original-1647 343 historical source notes R11826-R12168, "
    "41 groups, PDF725-735. The next Moon-to-Fixed-Stars heading PDF735 "
    "is genuinely unnumbered and preserved, not fake CLXV. 108 archive "
    "replayed source/window tests, zero human predictive validation, "
    "zero runtime promotions. Chinese V2 97 remains separate."
)
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"]) == 12168
assert idx["read_numbered_chapters"] == list(range(1, 164))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Latest original 1647 Lilly source checkpoint: printed CLXIIII Moon directions\n\n"
    "**343 historical documentary source annotations R11826–R12168** "
    "(341 substantive, 2 next-unit navigation) across 41 reversible "
    "original 1647 photo-anchored groups PDF725–735. "
    "**12,168 Lilly +1,066 Ptolemy=13,234 Western historical annotations**, "
    "and independent **97 Chinese BaZi/Zi Wei documentary annotations**. "
    "Next source **R12169**, the **unnumbered Moon Directed to FIXED STARRES** "
    "heading starts PDF735/printed701 below the CLXIIII twelfth-house text. "
    "Original annual-measure table near PDF745 is a later separate numerical "
    "source unit. **108 independently extracted ZIP CRC/sha/source tests pass**. "
    "Historical medical, death, legal, religion, sexual, personality or money "
    "claims are NOT verified human predictions. No modern chart-time "
    "engine parity or runtime inference rules have been promoted.\n\n"
)
for file in (CURRENT, PROGRESS):
    prior = file.read_text(encoding="utf-8")
    file.write_text(summary + "## Earlier retained research state\n\n" + prior, encoding="utf-8")
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07u",
    "status": "CANONICAL_INDEX_PREPARED_REMOTE_READBACK_PENDING",
    "previous_lilly": 11825,
    "accepted_lilly": 12168,
    "added_source_records": 343,
    "ptolemy_retained": 1066,
    "western_total": 13234,
    "chinese_v2_retained": 97,
    "prior_index_sha256": window["previous_index_sha256"],
    "new_index_sha256": sha(INDEX),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "archive_replayed_tests": 108,
    "next": "R12169 UNNUMBERED_MOON_FIXED_STARRES PDF735",
    "real_human_predictive_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
