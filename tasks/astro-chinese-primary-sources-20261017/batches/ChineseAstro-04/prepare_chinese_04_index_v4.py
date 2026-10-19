#!/usr/bin/env python3
"""Guarded append-only Chinese historical source V4: 65 exact classic quotes.

Zero overwrites of previously accepted Chinese V1-V3, BaZi records or Western
Lilly/Ptolemy. Historical attribution & natal predictive validity unresolved.
"""

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
V4 = P / "CHINESE_SOURCE_AUDIT_INDEX_V4.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_04.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-chinese-04-ziwei-volume2-20261019"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


for f in (V4, RECEIPT, LATEST, BACK / "CHINESE_V3_BEFORE_04.json"):
    assert not f.exists(), f"Interrupted/previous admission; reconcile {f}"
assert git("branch", "--show-current") == BRANCH
old = j(V3)
notes = j(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_20261019.json")
western = j(WEST)
assert j(V1)["sum_source_annotations"] == 72
assert j(V2)["sum_source_annotations"] == 97
assert old["sum_source_annotations"] == 142
assert old["original_chinese_source_anchors_checked_against_revision"] == 70
assert old["systems"][0]["accepted_source_annotations"] == 46
assert old["systems"][1]["accepted_source_annotations"] == 96
assert old["systems"][1]["next_id"] == "ZWD-R0097"
assert old["accepted_batches"][-1]["id"] == "ChineseAstro-03"
assert old["independently_validated_real_human_claims"] == old["runtime_promotions"] == 0
assert notes["count"] == notes["short_chinese_quote_direct_match_count"] == 65
assert notes["first_id"] == "ZWD-R0097"
assert notes["last_id"] == "ZWD-R0161"
assert notes["next_id"] == "ZWD-R0162"
assert notes["wikisource_revision_id"] == witness["source_revision_id"] == 1963110
assert notes["raw_source_sha256"] == witness["original_full_raw_source_sha256"]
assert witness["original_quote_count"] == 65
assert witness["all_65_short_anchor_exact_matches"]
assert [r["id"] for r in notes["records"]] == [f"ZWD-R{i:04d}" for i in range(97, 162)]
assert all(r["original_revision_quote_match_confirmed"] for r in notes["records"])
assert all(r["rule_status"] == "SOURCE_ONLY_DOCUMENTED" for r in notes["records"])
assert all(not r["runtime_promoted"] for r in notes["records"])
assert notes["independent_human_prediction_validations"] == notes["runtime_promotions"] == 0
assert witness["independent_actual_human_outcome_validations"] == witness["runtime_promotions"] == 0
assert release["crc_passed"] and release["member_SHA256_and_bytes_passed"]
assert release["independent_ZIP_extract_passed"]
assert release["total_replayed_tests"] == 249
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
assert (
    sha(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
    == release["new_65_source_notes_SHA256"]
)
assert (
    sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
    == release["original_revision_source_witness_SHA256"]
)
assert sha(V3) == release["old_Chinese_V3_index_SHA256"]
assert western["records_count"] == release["unchanged_Western_Lilly_count"] == 12472
assert western["batches"][-1]["id"] == "B07w"
assert western["next"]["chapter"] == "CLXVI"

for f in (
    V1,
    V2,
    V3,
    P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P / "ziwei/quan_shu_vol2_placements.py",
    P / "ziwei/quan_shu_vol2_aux_placements.py",
    P / "batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json",
    WEST,
):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

BACK.mkdir(exist_ok=False)
for f, name in (
    (V3, "CHINESE_V3_BEFORE_04.json"),
    (CURRENT, "CHINESE_CURRENT_BEFORE_04.md"),
    (WEST, "WESTERN_LILLY_INDEX_BEFORE_CHINESE04.json"),
):
    (BACK / name).write_bytes(f.read_bytes())

v4 = copy.deepcopy(old)
v4["schema"] = "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V4"
v4["status"] = "ZIWEI_VOLUME2_LIFE_BODY_LORDS_EIGHTEEN_SOURCE_STARS_DOCUMENTED"
v4["as_of_utc"] = "2026-10-19"
v4["prior_index"] = "CHINESE_SOURCE_AUDIT_INDEX_V3.json"
v4["prior_index_sha256"] = sha(V3)
v4["sum_source_annotations"] = 207
v4["original_chinese_source_anchors_checked_against_revision"] = 135
v4["accepted_batches"].append(
    {
        "id": "ChineseAstro-04",
        "added_bazi_source_annotations": 0,
        "added_ziwei_source_annotations": 65,
        "start": "ZWD-R0097",
        "end": "ZWD-R0161",
        "path": "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
        "rules_sha256": sha(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"),
        "witness_path": "batches/ChineseAstro-04/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
        "witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
        "wikisource_revision_id": 1963110,
        "original_raw_sha256": notes["raw_source_sha256"],
        "portable_tests_replayed": 249,
        "independent_human_predictions_validated": 0,
        "runtime_rules_promoted": 0,
    }
)
z = v4["systems"][1]
z["accepted_source_annotations"] = 161
z["current_ids"] = "ZWD-R0001–ZWD-R0161"
z["next_id"] = "ZWD-R0162"
z["current_batch"] = "ChineseAstro-04"
z["source_files"].append(
    "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"
)
z["chapter_coverage"] = (
    "Selected transmitted Zi Wei vol1–3 with pinned Volume II exact 135 "
    "short Chinese quote anchors (previous 70 plus new 65), including "
    "Life and Body Lords, historical sex-coded palace strengths, eight "
    "idle-star classes, annual Ji-Chou example, historically mixed "
    "element taxonomy and source eighteen-star list. Not the full "
    "ancient codex, not a Gregorian-to-lunar calendar or actual 14 "
    "principal-star natal engine, and not empirically predictive."
)
v4["separate_lilly_source_count_at_this_revision"] = 12472
v4["separate_ptolemy_source_count_at_this_revision"] = 1066
v4["full_ziwei_original_text_collation_finished"] = False
v4["all_14_principal_stars_verified"] = False
v4["ziwei_complete_natal_calendar_engine_verified"] = False
v4["chinese_bazi_solar_term_engine_verified"] = False
v4["independently_validated_real_human_claims"] = 0
v4["runtime_promotions"] = 0
v4["historical_glyph_and_translator_limits"] = (
    "135 exact short original Chinese phrases from transmitted online "
    "simplified source oldid1963110 across B02–B04, not an independently "
    "authenticated Ming woodblock original. Original life/body lord "
    "ambiguous 火玲星 preserved; source lists 18 regular stars and mixed "
    "five-element labels, not proof of actual modern chart engine. "
    "Infant death and sex-coded historical classifications are never "
    "person-level facts, zero human predictive validation."
)
v4["next"] = (
    "Original Zi Wei Volume II ZWD-R0162 onward: continue remaining "
    "minor star element classification and water/wood/metal/fire/earth "
    "bureau tables from pinned primary source with reversible old-format "
    "chart diagrams. Independent original BaZi BZI-R0047 from traditional "
    "Chinese source edition. Separately finish original Lilly CLXVI "
    "numeric direction source, genuine astronomical age engine and "
    "pre-registered human blinded decoy tests."
)
assert sum(s["accepted_source_annotations"] for s in v4["systems"]) == 207
assert [b["id"] for b in v4["accepted_batches"]] == (
    [b["id"] for b in old["accepted_batches"]] + ["ChineseAstro-04"]
)
V4.write_text(json.dumps(v4, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Zi Wei source-only Volume II Life/Body Lords and original elemental taxonomy (V4)\n\n"
    "**65 historically documented source notes ZWD-R0097–ZWD-R0161**, "
    "each of 65 phrases and original section names exact SHA/offset pinned "
    "to the same Wikisource Volume II revision oldid1963110, raw SHA256 "
    "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72. "
    "Chinese accepted **46 BaZi +161 Zi Wei =207 historical notes**, "
    "former V1 72, V2 97, V3 142 retained byte-exact. "
    "**249 source/placement and previous Chinese regression tests** replayed "
    "in independently extracted archive, CRC/hash/bytes verified. "
    "Separate **12,472 Lilly +1,066 Ptolemy=13,538 Western** unchanged; "
    "next original Lilly CLXVI source R12473 still provisional. "
    "Next Zi Wei **ZWD-R0162**, BaZi **BZI-R0047**. "
    "The transmitted Chinese has textual star labels and old period "
    "illness/gender/morality categories with no independent original Ming "
    "imprint, birth calendar, 14-main-star chart or verified actual people. "
    "**Zero empirical human predictive tests passed; no live model promotions.**\n\n"
)
old_current = CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    summary + "## Earlier accepted progress retained verbatim\n\n" + old_current, encoding="utf-8"
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "ChineseAstro-04",
    "status": "HISTORICAL_CHINESE_SOURCE_V4_PREPARED_REMOTE_PUBLICATION_PENDING",
    "Chinese_before": 142,
    "Chinese_after": 207,
    "BaZi_retained": 46,
    "ZiWei_before": 96,
    "ZiWei_after": 161,
    "new_documented_source_notes": 65,
    "prior_chinese_V3_sha256": sha(V3),
    "new_chinese_V4_sha256": sha(V4),
    "new_original_Chinese_notes_sha256": sha(
        B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"
    ),
    "original_source_quote_witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "archive_sha256": release["archive_sha256"],
    "portable_test_replays": 249,
    "Western_Lilly_retained": 12472,
    "Ptolemy_retained": 1066,
    "next_ZiWei": "ZWD-R0162",
    "next_BaZi": "BZI-R0047",
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
