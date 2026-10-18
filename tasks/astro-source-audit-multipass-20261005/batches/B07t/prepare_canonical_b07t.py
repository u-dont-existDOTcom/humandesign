#!/usr/bin/env python3
"""One-time source-only admission of printed first-edition Lilly CLXIII to canonical index."""

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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07t_SUN_FIXED_STARS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    proc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return (
        Path(proc.stdout.strip())
        if proc.returncode == 0 and proc.stdout.strip()
        else Path.home() / "Téléchargements"
    )


for file in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07t.json"):
    assert not file.exists(), f"Interrupted/prepared existing index! Reconcile: {file}"

assert git("branch", "--show-current") == "research/astro-b07t-sun-fixed-stars-20261018"
original = load(INDEX)
window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
map_ = load(B / "SOURCE_TO_RECORD_MAP.json")
photos = load(B / "ORIGINAL_SOURCE_WITNESS.json")
stars = load(B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json")
guard = load(B / "HISTORICAL_NONPROMOTION_GUARD_V1.json")
release = load(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
china = load(CHINA)

assert sha(INDEX) == window["parent_lilly_index_sha256"] == release["previous_index_sha256"]
assert original["records_count"] == accepted["prior_lilly"] == 11721
assert original["batches"][-1]["id"] == "B07s"
assert original["read_numbered_chapters"] == list(range(1, 162))
assert original["next"]["chapter"] == "CLXIII"
assert original["next"]["pdf_page"] == 723
assert original["source_sha256"] == window["full_source_894_frame_pdf_sha256"]
assert original["empirical_validations"] == original["runtime_promotions"] == 0
assert not any(b["id"] == "B07t" for b in original["batches"])
assert rules["record_count"] == accepted["new_historical_annotations"] == 104
assert (rules["substantive"], rules["following_navigation"]) == (102, 2)
assert [r["record_number"] for r in rules["rules"]] == list(range(11722, 11826))
assert [r["role"] for r in rules["rules"][-2:]] == [
    "next_clxiiii_heading",
    "next_moon_saturn",
]
assert len(map_["source_groups"]) == accepted["source_group_count"] == 13
assert len(stars["entries"]) == accepted["stellar_entries"] == 13
assert len(photos["photos"]) == accepted["source_photo_frames"] == 3
assert sha(B / "RULES.json") == accepted["rules_sha256"] == release["original_record_rule_sha256"]
assert (
    sha(B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json")
    == accepted["fixed_star_table_sha256"]
    == release["original_stellar_table_sha256"]
)
assert not guard["original_star_epoch_parity_verified"]
assert not guard["primary_directions_arc_age_date_engine_verified"]
assert not guard[
    "crime_mortality_disease_religion_gender_morality_real_person_predictions_permitted"
]
assert guard["independent_human_outcomes_validated"] == guard["runtime_rules_promoted"] == 0
assert release["crc_passed"] and release["sha256_and_bytes_passed"]
assert release["independent_extraction_passed"] and release["total_replayed"] == 62
assert sha(downloads() / release["owner_archive_filename"]) == release["archive_sha256"]
assert china["sum_source_annotations"] == 97
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0

for file in (
    INDEX,
    CHINA,
    ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07s/RULES.json",
    ROOT
    / (
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
    ),
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative
assert original["records_count"] == sum(b["records_count"] for b in original["batches"])

BACK.mkdir(exist_ok=False)
for file, backup in (
    (INDEX, "INDEX_BEFORE_B07t.json"),
    (CURRENT, "CURRENT_BEFORE_B07t.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07t.md"),
    (CHINA, "CHINESE_V2_BEFORE_B07t.json"),
):
    (BACK / backup).write_bytes(file.read_bytes())

original["batches"].append(
    {
        "id": "B07t",
        "path": "batches/B07t/RULES.json",
        "records_count": 104,
        "sha256": accepted["rules_sha256"],
        "scope": (
            "William Lilly Christian Astrology original 1647 first-edition CHAP "
            "CLXIII The Sunne Directed to FIXED STARRES from PDF723 lower/"
            "printed689 through PDF725 upper/printed691, next CHAP CLXIIII Moon "
            "to Promittors below divider same PDF725. Exactly 104 historical "
            "documentary annotations R11722-R11825 (102 substantive, 2 next "
            "chapter navigation), 13 reversible source/photo groups, 11 shared "
            "fixed-star effects headings, 13 historical named entries including "
            "paired Cheles and two Asses without assigning unprinted individual "
            "coordinates. Original 1647 photos 723-725 SHA/byte witnesses and "
            "62 independently extracted archive CRC/SHA test replays. Preserves "
            "Lion-heart nonfatal family illness, Bull-eye early-honor tragedy, "
            "Cheles military-benefit exception, Spica culmination conditions, "
            "two Asses avoidance and Cratch/Praesepe prudence provisos. Period "
            "medical/crime/violence/mortality/class and morality statements "
            "historical only. Modern star identity/epoch and arc-date engine "
            "UNVERIFIED, human empirical validations ZERO, executable runtime "
            "promotions ZERO. Chinese V2 97 retained separately."
        ),
    }
)
original["records_count"] = 11825
original["read_numbered_chapters"].append(162)
original["status"] = "BOOK_III_CLXIII_SUN_FIXED_STARS_NEXT_CLXIIII_MOON_PROMITTORS"
original["next"] = {
    "pdf_page": 725,
    "printed_page": 691,
    "chapter": "CLXIIII",
    "printed_chapter_numeral": "CLXIIII",
    "heading": "Directions of the Moon to PROMITTORS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Distinct printed CHAP CLXIIII starts below divider middle original "
        "PDF725/printed691, immediately after CLXIII Cratch/Praesepe "
        "source. Moon to Saturn body begins below heading. "
        "The true end boundary of CLXIIII has not yet been located; "
        "search further original first-edition photos before extraction "
        "acceptance, not by counting an assumed number of pages."
    ),
    "research_scope": (
        "Moon directions to promittors: keep original natal and annual "
        "conditions, planetary aspects, terms, nodes, houses and exceptions "
        "as printed; not a real-person forecast or verified math engine."
    ),
}
original["current_state"] = str(LATEST.relative_to(ROOT))
original["chapter_CLXIII_original_sun_fixed_stars_acceptance_note"] = (
    "B07t 104 historical-only annotations R11722-R11825 across 13 original "
    "reversible photo groups, 11 printed star effects and 13 old stellar "
    "entries, PDF723-725. Archive 62 independent replay tests. Modern star "
    "identity/epoch and direction-time engines unverified, zero predictive "
    "human successes or runtime promotions. Separate Chinese V2 97 retained."
)
assert original["records_count"] == sum(x["records_count"] for x in original["batches"]) == 11825
assert original["read_numbered_chapters"] == list(range(1, 163))
INDEX.write_text(json.dumps(original, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

headline = (
    "# Lilly original 1647 printed CLXIII Sun fixed-stars source accepted\n\n"
    "**104 historical documentary annotations R11722–R11825**, 102 "
    "substantive and two following CLXIIII navigation, 13 original "
    "photo-anchored reversible source groups across PDF723–725/printed689–691; "
    "11 old-star effects passages / 13 period stellar entries. "
    "**11,825 Lilly +1,066 Ptolemy=12,891 Western historical source notes**, "
    "plus separate **97 Chinese BaZi+Zi Wei source annotations**. "
    "Next printed **CHAP CLXIIII Moon to Promittors** begins below a "
    "divider on PDF725/printed691, **next R11826**. "
    "**62 ZIP-extracted CRC/hash/documentary tests passed**. All period "
    "mortality, clinical, violence, criminal, faith, class, gender, money, "
    "and moralizing claims are historic text, NOT validated predictions. "
    "No modern epoch/directions-time engine parity; zero human empirical "
    "forecast validations and zero model promotions.\n\n"
)
for file in (CURRENT, PROGRESS):
    previous = file.read_text(encoding="utf-8")
    file.write_text(headline + "## Earlier retained state\n\n" + previous, encoding="utf-8")
LATEST.write_text(
    headline + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07t",
    "status": "CANONICAL_PREPARED_PENDING_REMOTE_PUBLICATION",
    "lilly_before": 11721,
    "lilly_accepted": 11825,
    "added_historical_source_records": 104,
    "ptolemy_retained": 1066,
    "western_total": 12891,
    "chinese_v2_retained": 97,
    "next_record": "R11826",
    "next_chapter": "CLXIIII",
    "old_index_sha256": window["parent_lilly_index_sha256"],
    "new_index_sha256": sha(INDEX),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": release["archive_sha256"],
    "portable_replay_tests": 62,
    "human_prediction_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
