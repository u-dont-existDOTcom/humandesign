#!/usr/bin/env python3
"""Guard append-only 1647 unnumbered twelfth enemies source without chapter increment."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07g_TWELFTH_ENEMIES.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07g.json"):
    assert not p.exists(), f"Duplicate or partially prepared source: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10019
assert i["read_numbered_chapters"] == list(range(1, 152))
assert i["batches"][-1]["id"] == "B07f"
assert i["next"]["chapter"] == "UNNUMBERED_TWELFTH_HOUSE_ENEMIES"
assert i["next"]["printed_chapter_numeral"] is None
assert i["next"]["pdf_page"] == 673
assert i["next"]["following_printed_chapter_numeral"] == "CLIII"
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07g" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 23
assert [x["record_number"] for x in r["rules"]] == list(range(10020, 10043))
assert [x["id"] for x in r["rules"] if x["role"] == "next_numbered_navigation"] == [
    "R10041",
    "R10042",
]
assert r["substantive"] == a["substantive"] == 21
assert a["numbered_chapters_added"] == 0
assert a["lilly_if_published"] == 10042
assert a["combined_if_published"] == 11108
assert w["unnumbered"]
assert w["body_original_pdf_frames"] == [673, 674]
assert w["following_printed_CLIII_heading_pdf"] == 674
assert not w["intervening_original_CLII_heading_present"]
assert len(m["source_groups"]) == m["source_group_count"] == 3
assert not limits["printed_CLII_heading_observed"]
assert not limits["person_level_crime_danger_or_legal_prediction_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 13 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B07g.json"),
    (CURRENT, "CURRENT_BEFORE_B07g.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07g.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07g",
        "path": "batches/B07g/RULES.json",
        "records_count": 23,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly 1647 first-edition substantive "
            "UNNUMBERED twelfth-house Of Enemies introduction "
            "lower PDF673/printed639 through upper PDF674/"
            "printed640, before independently printed CHAP CLIII "
            "on quality of enemies later SAME PDF674. "
            "Three reversible first-edition photo groups "
            "and 21 substantive historical claims plus "
            "two future navigation R10020–R10042. "
            "The source targets enemy/adversary COUNT, "
            "via seventh/twelfth occupants, planets opposed "
            "to luminaries, alternative high/low conditions "
            "and first/seventh/twelfth lord mutual placements; "
            "lack of twelfth-lord aspect to Ascendant lord "
            "allegedly yields few rather than many. "
            "North Node compared to benefics and South "
            "Node to malefics, glyph parity unverified. "
            "Printed CLII heading not observed in source; "
            "no synthetic printed chapter invented. "
            "No human enemies, conflict, crime, danger "
            "or legal forecasts validated or promoted."
        ),
    }
)
i["records_count"] = 10042
assert i["read_numbered_chapters"] == list(range(1, 152))
i["status"] = "BOOK_III_UNNUMBERED_TWELFTH_ENEMIES_NEXT_CLIII_ENEMY_QUALITY"
i["next"] = {
    "pdf_page": 674,
    "printed_page": 640,
    "chapter": "CLIII",
    "printed_chapter_numeral": "CLIII",
    "heading": "What manner of Enemies? their Quality",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CLIII What manner of Enemies? "
        "their Quality begins after divider in original "
        "PDF674/printed640, after the UNNUMBERED "
        "twelfth-house enemy COUNT introduction ends "
        "on the same source page. No printed CLII "
        "heading appears in the scanned CLI–CLIII "
        "transition. Chapter CLIII continues PDF675 "
        "onward; inspect its own true next numbered "
        "heading before accepting."
    ),
    "research_scope": (
        "Historical source assertions about alleged "
        "type, visibility, strength, motives and effects "
        "of antagonists from seventh/twelfth occupants "
        "and their rulers and aspects, plus social "
        "status and adverse dispositions; no "
        "actual person danger, psychological "
        "character or criminality forecast."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["unnumbered_twelfth_enemies_source_acceptance_note"] = (
    "B07g R10020–R10042, 23 historic first edition "
    "source notes with original PDF673–676 photo SHA/bytes "
    "and 13 independent ZIP-extracted source tests. "
    "Explicit positive/negative enemy-count source "
    "claims, reciprocal rulers and unnumbered "
    "section source seam, printed CLII heading absent, "
    "Chinese 72 source notes separate. "
    "Zero actual human predictive accuracy "
    "and zero runtime rule promotion."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10042
assert i["read_numbered_chapters"] == list(range(1, 152))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly twelfth-house enemies-count introduction documented\n\n"
    + review
    + "\nAfter GitHub verified publication **10,042 Lilly "
    + "+1,066 Ptolemy=11,108 historical source notes**. "
    + "13 first-edition photo/ZIP replay tests pass; "
    + "no actual person's adversaries or danger predictions "
    + "verified and zero executable rule promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly through unnumbered twelfth-house enemies — 2026-10-18\n\n"
    "After remote verified publication **11,108 historical "
    "source annotations** (10,042 Lilly +1,066 Ptolemy). "
    "First-edition source frontier PDF674/894 "
    "(**75.4% scanned physical page position ONLY, "
    "not full historical/computational/human validity**). "
    "B07g records 23 old alternatives for number of "
    "enemies and nonoccurrence, after CLI two-nativity "
    "source, before separate printed CLIII quality "
    "on SAME PDF674. No printed CLII heading observed; "
    "numbered chapter counter unchanged for this "
    "UNNUMBERED section. No human danger or "
    "adversary accuracy tested, no runtime scorer "
    "promoted. Chinese BaZi46/Zi Wei26 separate.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07g.md").read_text()
)
CURRENT.write_text(
    "# Original twelfth-house unnumbered enemy-count source documented; CLIII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07g original R10020–R10042 locally accepted "
    "pending GitHub remote verification. After "
    "verified source publication 10,042 Lilly "
    "+1,066 Ptolemy=11,108 historical notes. "
    "13 first-edition photo/ZIP integrity tests pass; "
    "no real human enemies/moral/danger forecasts "
    "or runtime promotions. Section unnumbered "
    "(chapter counter unchanged); next printed "
    "CLIII from PDF674, original CLII heading "
    "absent. Chinese 72 notes separately indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07g.md").read_text()
)
receipt = {
    "batch": "B07g",
    "status": "GUARDED_UNNUMBERED_TWELFTH_ENEMIES_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07g.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10042,
    "ptolemy_retained": 1066,
    "combined_if_published": 11108,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
