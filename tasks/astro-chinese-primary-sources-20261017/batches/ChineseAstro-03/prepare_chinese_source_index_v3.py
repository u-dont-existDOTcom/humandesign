#!/usr/bin/env python3
"""Guarded append-only Chinese V3 source registry admission, 45 original anchors."""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
V1 = P / "CHINESE_SOURCE_AUDIT_INDEX_V1.json"
V2 = P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json"
V3 = P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json"
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261018_03.md"
BACKUP = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


for file in (V3, RECEIPT, LATEST, BACKUP / "CHINESE_V2_BEFORE_03.json"):
    assert not file.exists(), f"Preexisting or interrupted admission: {file}"
assert git("branch", "--show-current") == ("research/astro-chinese-03-ziwei-auxiliary-20261018")
old = j(V2)
notes = j(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
western = j(WESTERN)
assert j(V1)["sum_source_annotations"] == 72
assert old["sum_source_annotations"] == 97
assert (
    old["systems"][0]["accepted_source_annotations"],
    old["systems"][1]["accepted_source_annotations"],
) == (46, 51)
assert old["systems"][1]["next_id"] == "ZWD-R0052"
assert old["accepted_batches"][-1]["id"] == "ChineseAstro-02"
assert notes["count"] == 45
assert notes["next_id"] == "ZWD-R0097"
assert notes["wikisource_revision_id"] == witness["pinned_wikisource_revision_id"] == 1963110
assert notes["raw_source_sha256"] == witness["raw_source_sha256"]
assert witness["short_exact_chinese_anchor_matches"] == 45
assert [r["id"] for r in notes["records"]] == [f"ZWD-R{n:04d}" for n in range(52, 97)]
assert all(r["original_revision_quote_match_confirmed"] for r in notes["records"])
assert all(r["rule_status"] == "SOURCE_ONLY_DOCUMENTED" for r in notes["records"])
assert all(not r["runtime_promoted"] for r in notes["records"])
assert (
    sha(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
    == release["new_chinese_records_sha256"]
)
assert sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json") == release["witness_sha256"]
assert sha(V2) == release["prior_chinese_index_sha256"]
assert release["crc_passed"] and release["member_sha256_bytes_verified"]
assert release["independent_archive_extraction_passed"]
assert release["total_portable_test_replays"] == 160
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
assert old["independently_validated_real_human_claims"] == old["runtime_promotions"] == 0
assert notes["independent_human_prediction_validations"] == notes["runtime_promotions"] == 0
assert western["records_count"] == release["western_lilly_records_unchanged"] == 12472
assert western["batches"][-1]["id"] == "B07w"
assert western["next"]["chapter"] == "CLXVI"
for protected in (
    V1,
    V2,
    P / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P / "ziwei/quan_shu_vol2_placements.py",
    P / "batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
    P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    WESTERN,
):
    rel = str(protected.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(protected)), rel

BACKUP.mkdir(exist_ok=False)
for path, name in (
    (V2, "CHINESE_V2_BEFORE_03.json"),
    (CURRENT, "CHINESE_CURRENT_BEFORE_03.md"),
    (WESTERN, "WESTERN_INDEX_BEFORE_CHINESE_03.json"),
):
    (BACKUP / name).write_bytes(path.read_bytes())

v3 = copy.deepcopy(old)
v3["schema"] = "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V3"
v3["status"] = "SOURCE_FIRST_ZIWEI_VOLUME2_AUXILIARY_TIMING_SOURCE_VERIFIED"
v3["as_of_utc"] = "2026-10-18"
v3["prior_index"] = "CHINESE_SOURCE_AUDIT_INDEX_V2.json"
v3["prior_index_sha256"] = sha(V2)
v3["sum_source_annotations"] = 142
v3["original_chinese_source_anchors_checked_against_revision"] = 70
v3["accepted_batches"].append(
    {
        "id": "ChineseAstro-03",
        "added_bazi_source_annotations": 0,
        "added_ziwei_source_annotations": 45,
        "start": "ZWD-R0052",
        "end": "ZWD-R0096",
        "path": "batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json",
        "rules_sha256": sha(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json"),
        "witness_path": "batches/ChineseAstro-03/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
        "witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
        "wikisource_revision_id": 1963110,
        "original_raw_sha256": notes["raw_source_sha256"],
        "portable_tests_replayed": 160,
        "independent_human_predictions_validated": 0,
        "runtime_rules_promoted": 0,
    }
)
z = v3["systems"][1]
z["accepted_source_annotations"] = 96
z["current_ids"] = "ZWD-R0001–ZWD-R0096"
z["next_id"] = "ZWD-R0097"
z["current_batch"] = "ChineseAstro-03"
z["source_files"].append("batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
z["chapter_coverage"] = (
    "Selected transmitted Vol1–3 historical records plus pinned oldid1963110 "
    "Volume II 70 short-original quote anchors across earlier placements, "
    "Feng Ge/Tai Fu/Feng Gao, Chang Sheng bureaux, Hong Luan/Tian Xi, "
    "annual auxiliary stars, xun void branches and Da/Xiao Xian timing. "
    "NOT exhaustive; Chinese solar/lunar birth calendar, primary 14 stars, "
    "sihua school/epoch parity and human predictive accuracy unverified."
)
v3["separate_lilly_source_count_at_this_revision"] = 12472
v3["separate_ptolemy_source_count_at_this_revision"] = 1066
v3["full_ziwei_original_text_collation_finished"] = False
v3["all_14_principal_stars_verified"] = False
v3["ziwei_complete_natal_calendar_engine_verified"] = False
v3["chinese_bazi_solar_term_engine_verified"] = False
v3["independently_validated_real_human_claims"] = 0
v3["runtime_promotions"] = 0
v3["historical_glyph_and_translator_limits"] = (
    "All 70 volume II original short anchors in V2+V3 match exact simplified "
    "Chinese raw Wikisource pinned oldid1963110. This is an online transmitted "
    "text, NOT authenticated Ming woodblock printing or independent expert "
    "translation. Historical gender/illness/death or supernatural terms are "
    "NOT real-person facts. Bounded placements are not full calendar parity."
)
v3["next"] = (
    "Zi Wei original Volume II from ZWD-R0097, next child-period subsequent "
    "ages, Life/Body Lords, idle/strong palace, Five Elements star attributes "
    "and original bureau-specific principal-star tables. BaZi continues "
    "BZI-R0047 from independently sourced traditional Chinese primary books. "
    "Actual human validity and complete chart engines unverified."
)
assert sum(s["accepted_source_annotations"] for s in v3["systems"]) == 142
assert v3["accepted_batches"][-1]["id"] == "ChineseAstro-03"
V3.write_text(json.dumps(v3, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Zi Wei original Volume II Chinese source-only progress (V3)\n\n"
    "**45 newly anchored historical Zi Wei records ZWD-R0052–ZWD-R0096**, "
    "45/45 exact original Simplified Chinese section/quote matches against "
    "Wikisource pinned revision 1963110, raw SHA256 "
    "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72. "
    "**46 BaZi +96 Zi Wei =142 Chinese documentary annotations**; "
    "original Chinese V1 72 and V2 97 preserved unchanged. "
    "160 source/placement/prior-Chinese tests replayed after standalone archive "
    "extraction with CRC and SHA/bytes proof. "
    "**12,472 Lilly +1,066 Ptolemy =13,538 Western history notes unchanged**; "
    "printed Lilly CLXVI numerical methods remain PROVISIONAL. "
    "Next Chinese Zi Wei **ZWD-R0097**, BaZi **BZI-R0047**. "
    "No independently established classical edition provenance, full birth "
    "calendar/14-main-star engine or blind human accuracy; "
    "zero model runtime promotions.\n\n"
)
old_current = CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    summary + "## Earlier accepted checkpoint retained verbatim\n\n" + old_current, encoding="utf-8"
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "ChineseAstro-03",
    "status": "CHINESE_SOURCE_V3_PREPARED_REMOTE_PUBLICATION_PENDING",
    "Chinese_before": 97,
    "Chinese_after": 142,
    "BaZi_retained": 46,
    "ZiWei_before": 51,
    "ZiWei_after": 96,
    "new_historical_source_notes": 45,
    "original_index_v2_sha256": sha(V2),
    "new_index_v3_sha256": sha(V3),
    "source_notes_sha256": sha(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json"),
    "original_revision_witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "archive_sha256": release["archive_sha256"],
    "portable_tests": 160,
    "Western_Lilly_retained": 12472,
    "Ptolemy_retained": 1066,
    "next_ZiWei": "ZWD-R0097",
    "next_BaZi": "BZI-R0047",
    "human_accuracy_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
