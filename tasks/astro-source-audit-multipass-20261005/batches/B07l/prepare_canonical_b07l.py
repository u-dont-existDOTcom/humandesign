#!/usr/bin/env python3
"""Guarded first-edition original CLVI historical death-source append only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07l_DEATH_HISTORY.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07l.json"):
    assert not p.exists(), f"Duplicate or interrupted archive admission: {p}"

i = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
mapping = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
guard = read(B / "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json")
stars = read(B / "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = read(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10246
assert i["read_numbered_chapters"] == list(range(1, 155))
assert i["batches"][-1]["id"] == "B07j"
assert i["next"]["chapter"] == "CLVI"
assert i["next"]["printed_chapter_numeral"] == "CLVI"
assert i["next"]["pdf_page"] == 678
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07l" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 222
assert [x["record_number"] for x in r["rules"]] == list(range(10247, 10469))
assert [x["id"] for x in r["rules"] if x["role"] == "next_section_navigation"] == [
    "R10467",
    "R10468",
]
assert r["substantive"] == a["substantive"] == 220
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 10468
assert a["combined_if_published"] == 11534
assert w["body_pdf_frames"] == list(range(678, 685))
assert w["next_unnumbered_directions_starts_pdf"] == 685
assert len(mapping["source_groups"]) == mapping["source_group_count"] == 11
assert len(stars["table"]) == 6
assert not stars["modern_star_identity_parity_verified"]
assert not limits["person_mortality_medical_crime_or_self_harm_inference_authorized"]
assert not guard["nonpromotion"]["individual_death_timing_inference_allowed"]
assert not guard["nonpromotion"]["individual_death_type_inference_allowed"]
assert guard["real_human_deaths_predicted_or_validated"] == 0
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json") == a["star_source_table_sha256"]
assert sha(B / "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json") == a["nonpromotion_guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 36 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

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
for src, name in (
    (INDEX, "INDEX_BEFORE_B07l.json"),
    (CURRENT, "CURRENT_BEFORE_B07l.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07l.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07l",
        "path": "batches/B07l/RULES.json",
        "records_count": 222,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly first-edition printed CHAP CLVI "
            "'Of Death whether Violent or Natural', PDF678–684/"
            "printed644–650, ends before independent "
            "UNNUMBERED THE EFFECTS OF DIRECTIONS on TOP PDF685. "
            "11 reversible source-photo groups: 220 substantive "
            "historical clauses/conditions and 2 next source navigation "
            "R10247–R10468. Old violent versus natural death "
            "categories, Sun/Moon, Saturn/Mars, Ascendant/eighth "
            "rulers, violent-sign taxonomy, six historically "
            "positioned fixed stars, strong malefic configurations, "
            "Saturn/Mars house/sign/quality/official-class modes "
            "and dozens of alternative causes and even nonfatal "
            "eye injuries. CRITICAL source limitations: two benefics "
            "Asc/8th supposedly negate violent-death testimony; "
            "benevolent planet mitigates Saturn conditions; "
            "Mars aphorisms INVALID without luminary contact; "
            "aphorisms DO NOT independently operate apart from "
            "principal significators; if no violent indicators "
            "present author alleges natural death; Lilly expressly "
            "warns astrologers not to be POSITIVE about time of death. "
            "Ptolemy/Haly/Albubater/Cardanus/Schoner/Origanus "
            "attributions not independently cross-collated; "
            "period astrology/empyric certainty unsupported. "
            "ZERO real human death/medical/crime/injury accuracy "
            "and NO production or runtime rule promotion."
        ),
    }
)
i["records_count"] = 10468
i["read_numbered_chapters"].append(155)
i["status"] = "BOOK_III_CLVI_DEATH_HISTORICAL_SOURCE_NEXT_UNNUMBERED_DIRECTIONS"
i["next"] = {
    "pdf_page": 685,
    "printed_page": 651,
    "chapter": "THE_EFFECTS_OF_DIRECTIONS",
    "printed_chapter_numeral": None,
    "heading": "THE EFFECTS OF DIRECTIONS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "following_printed_chapter_numeral": "CLVII",
    "following_original_pdf_page": 688,
    "position": (
        "A substantive MAJOR UNNUMBERED source "
        "'THE EFFECTS OF DIRECTIONS' starts TOP "
        "original first-edition PDF685/printed651 "
        "following CLVI death text terminal on PDF684. "
        "It continues original PDF686–688 upper, "
        "BEFORE distinct numbered CHAP CLVII "
        "'How long the Effects of a Direction shall last' "
        "starts PDF688 mid/lower. Another numbered CLVIII "
        "begins PDF690. Preserve all original "
        "source boundaries, accept directions "
        "introduction separately with +0 chapter count."
    ),
    "research_scope": (
        "Historical Regiomontanus, Argolus and older "
        "directions methods: Significator, Promittor, "
        "period mathematical houses, years/months/"
        "weeks/days allegedly derived from directed "
        "arcs. CRUCIAL source 2–3 zodiac degree "
        "birth-Ascendant error allegedly moves "
        "event timing by YEARS, creating "
        "retrospective rectification/overfitting "
        "risk. Separate life events used to "
        "fit birth time from untouched events "
        "testing it; verify Swiss ephemeris "
        "and original Regiomontanus numerics."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLVI_historical_mortality_acceptance_note"] = (
    "B07l R10247–R10468, 222 first-edition original "
    "source-only historical notes photo PDF678–685 "
    "SHA/bytes and 36 separately ZIP-extracted test "
    "replays. Six period fixed-star source positions, "
    "strong source mitigation and author explicit "
    "against certain death timing. No actual "
    "human violent/natural-death or date accuracy, "
    "no diagnostic/criminal classification, "
    "no runtime rules. Chinese 72 separate."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10468
assert i["read_numbered_chapters"] == list(range(1, 156))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly first edition printed CLVI on mortality documented\n\n"
    + review
    + "\nAfter verified GitHub publication **10,468 Lilly + "
    + "1,066 Ptolemy =11,534 historical source annotations**. "
    + "All 36 first-edition photo/ZIP archive tests pass. "
    + "Zero real human mortality, violence/medical "
    + "predictions or executable source rules promoted.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 through printed CLVI historical mortality — 2026-10-18\n\n"
    "Following remote verified publication **11,534 "
    "historical documentary annotations** "
    "(10,468 Lilly +1,066 Ptolemy), original "
    "first-edition photograph frontier PDF685/894 "
    "(**76.6% physical scanned-page position ONLY, "
    "not scientific research/predictive completion**). "
    "B07l adds 222 source-only CLVI records, 6 period "
    "fixed-star source coordinates, dozens of compound "
    "fatal/nonfatal outcomes but MAIN original caveats "
    "that aphorisms cannot operate alone and astrologers "
    "must not state certain time of death. Zero human "
    "mortality outcomes tested, no runtime scorer "
    "promotions. NEXT major UNNUMBERED original "
    "`THE EFFECTS OF DIRECTIONS` PDF685–688 before "
    "printed CLVII later PDF688. Directions timing/"
    "birth-time uncertainty crucial to independent blind "
    "research. Chinese 46 BaZi +26 Zi Wei source-only "
    "notes remain separate.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07l.md").read_text()
)
CURRENT.write_text(
    "# Lilly original CLVI historical death source admitted; directions source next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07l R10247–R10468 locally accepted and pending "
    "authenticated GitHub remote SHA. After publication "
    "10,468 Lilly +1,066 Ptolemy =11,534 "
    "historical source notes, 36 first-edition/"
    "portable ZIP source checks pass. NO human "
    "death prediction, dates, injury risk or actual "
    "legal/moral classifications, no runtime source "
    "scoring promotions. Next UNNUMBERED `THE EFFECTS "
    "OF DIRECTIONS` original PDF685–688, then "
    "printed CLVII and CLVIII separate. Chinese "
    "BaZi46 +ZiWei26 sources separately preserved.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07l.md").read_text()
)
receipt = {
    "batch": "B07l",
    "status": "GUARDED_FIRST_EDITION_CLVI_SOURCE_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07l.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "star_table_sha256": sha(B / "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json"),
    "mortality_nonpromotion_guard_sha256": sha(
        B / "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json"
    ),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10468,
    "ptolemy_retained": 1066,
    "combined_if_published": 11534,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
