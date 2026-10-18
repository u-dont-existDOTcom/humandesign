#!/usr/bin/env python3
"""Append authenticated original first-edition CLIX source and preserve CLX boundary."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07p_ASCENDANT_DIRECTIONS.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07p.json"):
    assert not p.exists(), f"Duplicate or partial archival admission {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
stars = j(B / "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json")
guard = j(B / "CLIX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10732
assert i["read_numbered_chapters"] == list(range(1, 158))
assert i["batches"][-1]["id"] == "B07o"
assert i["next"]["chapter"] == "CLIX"
assert i["next"]["printed_chapter_numeral"] == "CLIX"
assert i["next"]["pdf_page"] == 691
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07p" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 335
assert [x["record_number"] for x in r["rules"]] == list(range(10733, 11068))
assert [x["id"] for x in r["rules"] if x["role"].startswith("next_CLX")] == [
    "R11065",
    "R11066",
    "R11067",
]
assert r["substantive"] == a["substantive"] == 332
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 11067
assert a["combined_if_published"] == 12133
assert w["body_original_pdf_frames"] == list(range(691, 703))
assert w["following_printed_CLX_heading_pdf"] == 702
assert len(m["source_groups"]) == m["source_group_count"] == 17
assert len(stars["entries"]) == 16 and not stars["calculational_parity_verified"]
assert not limits["original_all_glyphs_verified"]
assert not limits["original_primary_directions_time_engine_verified"]
assert not guard["primary_directions_arc_time_engine_verified"]
assert guard["independent_human_outcomes_validated"] == 0
assert guard["runtime_rules_promoted"] == 0
assert not limits["real_person_medical_criminal_religious_or_safety_advice_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_real_event_timing_accuracy_validated"]
        or x["independent_health_or_death_prediction_validated"]
        or x["independent_relationship_or_financial_prediction_validated"]
        or x["independent_faith_personality_or_crime_label_validated"]
        or x["original_directions_angle_date_conversion_verified"]
        or x["original_1647_fixed_star_modern_epoch_parity_verified"]
        or x["real_person_health_safety_social_status_advice_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert (
    sha(B / "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json") == a["fixed_star_source_table_sha256"]
)
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 38 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B07p.json"),
    (CURRENT, "CURRENT_BEFORE_B07p.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07p.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07p",
        "path": "batches/B07p/RULES.json",
        "records_count": 335,
        "sha256": a["rules_sha256"],
        "scope": (
            "Lilly original Christian Astrology 1647 printed CLIX "
            "'The Ascendant directed to the Body of Jupiter, and "
            "his Aspects' from original PDF691 lower/printed657 "
            "through PDF702 upper/printed668, then independent "
            "printed CLX Mid-heaven Directions begins after divider "
            "SAME PDF702. 335 historical annotations R10733–R11067 "
            "(332 substantive and 3 following CLX navigation) "
            "in 17 reversible original source/photo groups. "
            "CLIX contains separate Ascendant body, sextile/trine, "
            "square/opposition and terms directions to Jupiter, "
            "Mars, Sun, Venus, Mercury and Moon; also lunar nodes, "
            "Part Fortune and varying planetary dispositor, "
            "2nd/3rd/4th house cusps, 16 original epoch-unknown "
            "star/asterism directions with first-edition zodiac "
            "coordinates. Numerous contradictory favorable and "
            "dangerous historic health, mortality, class-specific "
            "wealth/office, marriage, parenthood, legal and "
            "personality claims with essential radix/hyleg/anareta/"
            "promittor/aspect/old zodiac exceptions. "
            "Original fixed star identification/precession and "
            "directions arc-to-age engine unverified. "
            "Zero human empirical validation, no real person "
            "medical/safety/faith/morality inference and "
            "no executable runtime model promotions. "
            "Parallel Chinese source index untouched."
        ),
    }
)
i["records_count"] = 11067
i["read_numbered_chapters"].append(158)
i["status"] = "BOOK_III_CLIX_ASCENDANT_DIRECTIONS_NEXT_CLX_MIDHEAVEN"
i["next"] = {
    "pdf_page": 702,
    "printed_page": 668,
    "chapter": "CLX",
    "printed_chapter_numeral": "CLX",
    "heading": "Directions of the Mid-heaven to PROMITTORS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Distinct original printed CHAP CLX starts "
        "after divider midway through PDF702/printed668, "
        "following 16 original old-stellar Ascendant "
        "direction categories from previous CLIX. "
        "The Mid-heaven source continues PDF703 onward. "
        "Original first-edition PDF702–710 scanned photos "
        "have been staged for new CLX task. Determine "
        "the genuine following printed chapter seam "
        "before claiming any complete CLX extraction."
    ),
    "research_scope": (
        "Medieval directions of Mid-heaven to Saturn, "
        "Jupiter, Mars, Sun, Venus, Mercury, Moon, "
        "lunar nodes, fixed stars and house contexts "
        "as actually found in original PDF pages, "
        "on official honor, occupation, patronage, "
        "inheritance, risk, alleged sickness and class "
        "relative social effects. Source text only. "
        "No verified angular date arithmetic "
        "or actual human predictions."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLIX_directions_source_acceptance_note"] = (
    "B07p 335 original historic annotations R10733–R11067, "
    "17 reversible source groups, first-edition PDF691–703 "
    "SHA/byte photos and 38 independent archive replay tests. "
    "Separate planet/aspect/terms/cusps and 16 period "
    "stellar longitudes preserved, epoch and actual "
    "primary-direction date engines unverified, "
    "medical/harm/morality labels not real forecasts. "
    "Chinese BaZi46/ Zi Wei26 source notes separately indexed."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 11067
assert i["read_numbered_chapters"] == list(range(1, 159))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly 1647 printed CLIX Ascendant directions original source documented\n\n"
    + review
    + "\nFollowing authenticated remote publication **11,067 Lilly "
    + "+1,066 retained Ptolemy =12,133 historic source notes**, "
    + "38 original photo/archive tests pass, not actual "
    + "human clinical/mortality/economic or relationship "
    + "predictive accuracy. Zero runtime promotions.\n"
)
PROGRESS.write_text(
    "# Lilly original first edition through CLIX Ascendant directions — 2026-10-18\n\n"
    "After GitHub remote publication **12,133 "
    "original source annotations** (11,067 Lilly "
    "+1,066 Ptolemy). Source frontier original PDF702/894 "
    "(**78.5% scanned physical page position ONLY**, "
    "not predictive or mathematical research completion). "
    "B07p 335 period-source clauses of separate Ascendant "
    "directions to 6 planets, nodes, Part Fortune, house "
    "cusps and 16 fixed stars; requires original radix "
    "and age/time calculations not done. "
    "No independent human life outcomes, disease/"
    "mortality or personal safety accuracy "
    "and no executable natal scoring. "
    "NEXT printed CLX directions of Midheaven "
    "starts same original PDF702 after divider. "
    "Chinese BaZi46+ZiWei26 source-only separate.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07p.md").read_text()
)
CURRENT.write_text(
    "# Lilly CLIX original Ascendant directions documented, CLX next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "Original B07p historical source R10733–R11067 "
    "accepted locally; after GitHub remote readback "
    "11,067 Lilly +1,066 Ptolemy =12,133 "
    "documentary records. Original PDF702/894 "
    "78.5% physical source frontier, "
    "38 original-source plus extracted ZIP tests pass. "
    "No actual people or real-world danger/health/"
    "career outcomes validated and zero model "
    "promotions. Next separately printed CLX "
    "Mid-heaven directions at PDF702; Chinese "
    "BaZi46 + ZiWei26 remain independent.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07p.md").read_text()
)
receipt = {
    "batch": "B07p",
    "status": "GUARDED_ORIGINAL_CLIX_ASCENDANT_DIRECTIONS_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07p.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "source_fixed_star_table_sha256": sha(B / "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json"),
    "historical_directions_guard_sha256": sha(
        B / "CLIX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json"
    ),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 11067,
    "ptolemy_retained": 1066,
    "combined_if_published": 12133,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
