#!/usr/bin/env python3
"""Guarded one-time acceptance of Lilly's complete printed CLX source batch."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX_PATH = (
    ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07q_MIDHEAVEN_DIRECTIONS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07q.json"):
    assert not path.exists(), f"Already accepted or interrupted: {path}"
idx = j(INDEX_PATH)
window = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
archive = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
source = j(B / "SOURCE_FIRST_AUTHORING_20261018.json")
mapping = j(B / "SOURCE_TO_RECORD_MAP.json")
witness = j(B / "ORIGINAL_SOURCE_WITNESS.json")
guard = j(B / "CLX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json")
chinese = j(CHINA)

assert sha(INDEX_PATH) == window["accepted_index_sha256"] == archive["pre_acceptance_index_sha256"]
assert idx["records_count"] == accept["prior_lilly"] == 11067
assert idx["read_numbered_chapters"] == list(range(1, 159))
assert idx["batches"][-1]["id"] == "B07p"
assert idx["next"]["chapter"] == idx["next"]["printed_chapter_numeral"] == "CLX"
assert idx["next"]["pdf_page"] == 702
assert idx["source_sha256"] == witness["full_original_1647_pdf_sha256"]
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(b["id"] == "B07q" for b in idx["batches"])
assert sha(B / "RULES.json") == accept["rules_sha256"] == archive["rules_sha256"]
assert rules["record_count"] == accept["new_historical_annotations"] == 258
assert rules["substantive"] == accept["substantive"] == 256
assert rules["following_navigation"] == accept["next_navigation"] == 2
assert len(source["groups"]) == len(mapping["source_groups"]) == 27
assert [r["record_number"] for r in rules["rules"]] == list(range(11068, 11326))
assert [r["role"] for r in rules["rules"][-2:]] == ["next_CLXI_divider", "next_fixedstars"]
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert not guard["real_human_predictive_accuracy_demonstrated"]
assert not guard["primary_directions_arc_time_engine_verified"]
assert not guard["runtime_rules_promoted"]
assert chinese["sum_source_annotations"] == 72
assert chinese["runtime_promotions"] == 0
assert archive["crc_passed"] and archive["sha256_passed"] and archive["extraction_passed"]
assert archive["independent_archive_replay_total"] == 71
assert archive["replayed_documentary_tests"] == 62
assert archive["replayed_source_window_tests"] == 9
assert sha(archive["archive_path"]) == archive["archive_sha256"]
assert witness["body_original_pdf_frames"] == list(range(702, 712))
assert witness["following_printed_CLXI_heading_pdf"] == 711
assert len(witness["photos"]) == 12
for value in witness["photos"].values():
    image = B / value["file"]
    assert image.stat().st_size == value["bytes"] and sha(image) == value["sha256"]
assert git("branch", "--show-current") == "research/astro-b07q-midheaven-directions-20261018"
rel = str(INDEX_PATH.relative_to(ROOT))
assert not subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode
assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(INDEX_PATH))
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"])

BACK.mkdir(exist_ok=False)
for source_file, backup in (
    (INDEX_PATH, "INDEX_BEFORE_B07q.json"),
    (CURRENT, "CURRENT_BEFORE_B07q.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07q.md"),
    (CHINA, "CHINESE_INDEX_BEFORE_B07q.json"),
):
    (BACK / backup).write_bytes(source_file.read_bytes())

idx["batches"].append(
    {
        "id": "B07q",
        "path": "batches/B07q/RULES.json",
        "records_count": 258,
        "sha256": sha(B / "RULES.json"),
        "scope": (
            "Original 1647 Lilly first edition printed CHAP CLX "
            "Directions of the Mid-heaven to PROMITTORS from PDF702 lower/"
            "printed668 through PDF711 upper/printed677, distinct CLXI "
            "fixed-star chapter following divider mid PDF711. "
            "258 historical documentary annotations R11068-R11325 "
            "(256 substantive, 2 next-chapter navigational) "
            "across 27 reversible photo-anchored source groups. "
            "Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon body, "
            "sextile/trine, square/opposition and original planetary "
            "terms where printed; 11th/12th house cusp and rare "
            "Midheaven-to-horoscope directions. Preserves social-class "
            "and natal/radix qualifications, conflicting claims, "
            "historically harmful disease, mortality, captivity and "
            "moralizing statements as source ONLY. 19 first-edition "
            "page photos PDF702-720 with SHA/bytes and 71 independently "
            "extracted CRC/hash replay tests. Original time conversion "
            "and astrology empirical predictive validity unverified. "
            "Zero human validation; zero runtime promotions; "
            "independent Chinese BaZi46/ZiWei26 source index unchanged."
        ),
    }
)
idx["records_count"] = 11325
idx["read_numbered_chapters"].append(159)
idx["status"] = "BOOK_III_CLX_MIDHEAVEN_DIRECTIONS_NEXT_CLXI_FIXED_STARS"
idx["next"] = {
    "pdf_page": 711,
    "printed_page": 677,
    "chapter": "CLXI",
    "printed_chapter_numeral": "CLXI",
    "heading": "The Mid-heaven Directed to FIXED STARRES",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 CHAP CLXI starts below independent rule mid "
        "PDF711/printed677 after final CLX rare horoscope paragraph; "
        "continues PDF712 and ends mid PDF713 before another divider "
        "for printed CLXII Sunne directed to Promittors. "
        "Original photo witness PDF711-713 is in B07q; create "
        "a new CLXI source-only batch beginning R11326."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CLX_source_acceptance_note"] = (
    "B07q 258 original first-edition historical source notes "
    "R11068-R11325; 27 reversible groups PDF702-711 and "
    "context to PDF720, 71 portable archive replay checks. "
    "False human forecast, medical/danger validity and runtime "
    "promotion claims prohibited. CLXI starts PDF711. "
    "Chinese 72 separately indexed source notes not changed."
)
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"]) == 11325
assert idx["read_numbered_chapters"] == list(range(1, 160))
INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Latest original Lilly 1647 source acceptance: printed CLX Midheaven\n\n"
    "Original first-edition photographic clauses from printed "
    "PDF702/folio668 through upper PDF711/folio677 accepted as "
    "**258 historical documentary annotations R11068–R11325** "
    "(256 substantive +2 CLXI navigation), **27 reversible groups**; "
    "no empirical human prediction or runtime promotion. "
    "**11,325 Lilly +1,066 retained Ptolemy=12,391 Western "
    "source records**; separate **72 Chinese source annotations**. "
    "Next printed CLXI fixed stars begins mid PDF711; next R11326. "
    "Archive 71 independent extracted tests. "
    "No independently validated predictive forecasting; "
    "direction arc-to-date engine and historical epoch parity unverified.\n\n"
)
for file in (CURRENT, PROGRESS):
    original = file.read_text(encoding="utf-8")
    file.write_text(summary + "## Earlier retained research state\n\n" + original, encoding="utf-8")
review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8")
LATEST.write_text(summary + review, encoding="utf-8")

receipt = {
    "batch": "B07q",
    "state": "PREPARED_NOT_REMOTE_PUBLISHED",
    "previous_lilly": 11067,
    "new_lilly": 11325,
    "added_source_records": 258,
    "ptolemy_still": 1066,
    "western_total": 12391,
    "chinese_source_count_unchanged": 72,
    "prior_index_sha256": window["accepted_index_sha256"],
    "new_index_sha256": sha(INDEX_PATH),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "archive_replayed_tests": 71,
    "next_R": "R11326",
    "next_printed_chapter": "CLXI",
    "human_validation": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
