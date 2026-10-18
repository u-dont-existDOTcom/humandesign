#!/usr/bin/env python3
"""One-time guarded original Lilly CLXI archival index admission (source only)."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX_PATH = (
    ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07r_MIDHEAVEN_FIXED_STARS.md"
CHINESE_V1 = (
    ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
)
CHINESE_V2 = (
    ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
)
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07r.json"):
    assert not path.exists(), f"Already partially updated: {path}; reconcile first"
idx = load(INDEX_PATH)
win = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
map_ = load(B / "SOURCE_TO_RECORD_MAP.json")
photos = load(B / "ORIGINAL_SOURCE_WITNESS.json")
stars = load(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json")
guard = load(B / "HIGH_STAKES_NONPROMOTION_GUARD_V1.json")
zipreceipt = load(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
china = load(CHINESE_V2)

assert git("branch", "--show-current") == "research/astro-b07r-midheaven-fixedstars-20261018"
assert git("rev-parse", "HEAD") == "f2fa2b4c83db6c6ac5ce5d3f3561217050a2f7ed"
assert sha(INDEX_PATH) == win["prior_index_sha256"] == zipreceipt["prior_canonical_index_sha256"]
assert idx["records_count"] == accept["prior_lilly"] == 11325
assert idx["read_numbered_chapters"] == list(range(1, 160))
assert idx["batches"][-1]["id"] == "B07q"
assert idx["next"]["chapter"] == "CLXI" and idx["next"]["pdf_page"] == 711
assert idx["source_sha256"] == win["original_full_pdf_sha256"]
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(b["id"] == "B07r" for b in idx["batches"])
assert len(rules["rules"]) == accept["new_historical_annotations"] == 90
assert [r["record_number"] for r in rules["rules"]] == list(range(11326, 11416))
assert [r["role"] for r in rules["rules"][-2:]] == ["next_clxii", "next_sun_intro"]
assert rules["substantive"] == accept["substantive"] == 88
assert rules["following_navigation"] == accept["following_navigation"] == 2
assert (
    len(map_["source_groups"])
    == len(load(B / "SOURCE_FIRST_AUTHORING_20261018.json")["groups"])
    == 12
)
assert len(stars["entries"]) == 14
assert stars["entries_count"] == accept["period_star_entries"]
assert sha(B / "RULES.json") == accept["rules_sha256"] == zipreceipt["rules_sha256"]
assert sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json") == accept["table_sha256"]
assert photos["body_frames"] == [711, 712, 713]
assert photos["following_heading_frame"] == 713
assert len(photos["photos"]) == 4
assert not guard["violence_crime_capital_punishment_health_safety_predictions_allowed"]
assert not guard["runtime_rules_promoted"] and not guard["independent_human_outcomes_validated"]
assert zipreceipt["crc_passed"] and zipreceipt["member_hashes_verified"]
assert zipreceipt["portable_test_replay"] == 50
assert sha(zipreceipt["archive_path"]) == zipreceipt["archive_sha256"]
assert china["sum_source_annotations"] == 97
assert china["independently_validated_real_human_claims"] == 0
assert load(CHINESE_V1)["sum_source_annotations"] == 72
for protected in (
    INDEX_PATH,
    CHINESE_V1,
    CHINESE_V2,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07q/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    rel = str(protected.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(protected)), rel
assert idx["records_count"] == sum(batch["records_count"] for batch in idx["batches"])

BACK.mkdir(exist_ok=False)
for source, name in (
    (INDEX_PATH, "INDEX_BEFORE_B07r.json"),
    (CURRENT, "CURRENT_BEFORE_B07r.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07r.md"),
    (CHINESE_V2, "CHINESE_V2_BEFORE_B07r.json"),
):
    (BACK / name).write_bytes(source.read_bytes())

idx["batches"].append(
    {
        "id": "B07r",
        "path": "batches/B07r/RULES.json",
        "records_count": 90,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Original 1647 printed CHAP CLXI, The Mid-heaven Directed "
            "to FIXED STARRES, physically PDF711 lower/printed677 "
            "through PDF713 upper/printed679, then independent CLXII "
            "Sun-direction heading after divider SAME PDF713. "
            "90 historical source notes R11326-R11415, 88 substantive "
            "+2 CLXII navigation, 12 original photo-anchored reversible "
            "source groups, 14 original period stellar designations/"
            "coordinates including right Orion shoulder ut supra with "
            "NO source coordinate here, and degrees-only MINUTES NULL. "
            "Original epoch, star identifications, directional time "
            "conversion and human claims unvalidated. Highly "
            "stigmatizing violence, imprisonment, mortality, "
            "religious/gender/class claims historical ONLY. "
            "50 independent extracted ZIP replay tests; zero "
            "individual empirical validations and runtime promotions. "
            "Chinese V2 97 source records separately preserved."
        ),
    }
)
idx["records_count"] = 11415
idx["read_numbered_chapters"].append(160)
idx["status"] = "BOOK_III_CLXI_FIXED_STAR_MIDHEAVEN_NEXT_CLXII_SUN_DIRECTIONS"
idx["next"] = {
    "pdf_page": 713,
    "printed_page": 679,
    "chapter": "CLXII",
    "printed_chapter_numeral": "CLXII",
    "heading": "The Sunne directed to PROMITTORS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Distinct original first-edition printed CHAP CLXII "
        "begins lower original PDF713/printed679 below rule "
        "after Algol paragraph ending printed CLXI. "
        "Original PDF714-720 contextual photos already in B07q "
        "but CLXII TRUE following numbered chapter seam NOT "
        "yet located; extend original photo window before acceptance."
    ),
    "research_scope": (
        "Sun body/sextile/trine/square/opposition/terms and following "
        "source cases as printed; source-only until complete original seam verified."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CLXI_original_fixed_star_source_acceptance_note"] = (
    "B07r original source-only R11326-R11415, 90 historic notes "
    "in 12 groups, 14 period stellar entries, original PDF711-714 "
    "SHA/bytes, 50 independent archive tests. No high-stakes "
    "forecast, source epoch/modern stars and angle-date engines "
    "unverified. Separate Chinese V2 97 retained."
)
assert idx["records_count"] == sum(batch["records_count"] for batch in idx["batches"]) == 11415
assert idx["read_numbered_chapters"] == list(range(1, 161))
INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Latest original Lilly 1647 source acceptance: printed CLXI fixed stars\n\n"
    "**90 historical documentary annotations R11326–R11415** "
    "(88 substantive +2 following CLXII navigation), "
    "14 period fixed-star entries across 12 photo-anchored "
    "groups PDF711–713, 50 focused independently replayed source tests. "
    "**11,415 Lilly +1,066 Ptolemy=12,481 Western documentary "
    "source annotations** and separate **97 Chinese historic annotations**. "
    "Next original printed CHAP CLXII Sun directions starts lower "
    "PDF713/printed679, **next R11416**. This source count does "
    "NOT validate astrology; directions arc/date/old stellar epoch "
    "and individual human medical, mortality, class, crime, "
    "economic or relationship predictions remain unverified.\n\n"
)
for file in (CURRENT, PROGRESS):
    old = file.read_text(encoding="utf-8")
    file.write_text(summary + "## Earlier retained research state\n\n" + old, encoding="utf-8")
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
r = {
    "batch": "B07r",
    "status": "CANONICAL_PREPARED_NOT_YET_REMOTE",
    "prior_lilly": 11325,
    "now_lilly": 11415,
    "ptolemy": 1066,
    "western_total": 12481,
    "chinese_v2_preserved": 97,
    "new_historic_annotations": 90,
    "previous_index_sha256": win["prior_index_sha256"],
    "new_index_sha256": sha(INDEX_PATH),
    "rules_sha256": sha(B / "RULES.json"),
    "period_star_table_sha256": sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json"),
    "archive_sha256": zipreceipt["archive_sha256"],
    "replayed_tests": 50,
    "next": "R11416 CLXII PDF713 lower",
    "human_predictive_validation": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(r, indent=2))
