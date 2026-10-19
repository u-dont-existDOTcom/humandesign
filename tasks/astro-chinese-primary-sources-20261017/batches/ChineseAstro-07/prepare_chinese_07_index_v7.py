#!/usr/bin/env python3
"""Guarded Chinese source index V7: Zi Wei auxiliary star and five raw bureau grids.

This is append-only historical source documentation; previous V1-V6 remain
byte-identical. Actual chart algorithms, historical authorship, human
predictions and Western concurrent research are not promoted.
"""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
OLD = P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
NEW = P / "CHINESE_SOURCE_AUDIT_INDEX_V7.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_07.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-chinese-07-ziwei-auxiliary-bureaus-20261019"
BASE_COMMIT = "2b3aeb3a1efb429566f362ca8c208a83015217ee"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    resolved = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if resolved is not None and resolved.is_dir() and resolved.resolve() != Path.home().resolve():
        return resolved
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for file in (NEW, LATEST, RECEIPT, BACK / "CHINESE_V6_BEFORE_07.json"):
    assert not file.exists(), f"Possible interrupted prior canonical admission {file}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == BASE_COMMIT
old = j(OLD)
notes = j(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
western = j(WEST)
assert task["required_branch"] == BRANCH and task["root_outcome"] == "OPEN"
assert old["sum_source_annotations"] == 315
assert old["systems"][0]["accepted_source_annotations"] == 154
assert old["systems"][1]["accepted_source_annotations"] == 161
assert old["systems"][1]["next_id"] == "ZWD-R0162"
assert old["accepted_batches"][-1]["id"] == "ChineseAstro-06"
assert old["original_chinese_source_anchors_checked_against_revision"] == 243
assert old["independently_validated_real_human_claims"] == old["runtime_promotions"] == 0
assert western["records_count"] == 12611 and western["batches"][-1]["id"] == "B07al"
assert notes["pinned_original_volume2_full_raw_SHA256"] == (
    "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
)
assert (
    sha(B / "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt")
    == (notes["pinned_original_volume2_full_raw_SHA256"])
)
assert notes["source_historical_annotation_count"] == 40
assert [r["id"] for r in notes["record_rows"]] == [f"ZWD-R{i:04d}" for i in range(162, 202)]
assert notes["next_id"] == "ZWD-R0202"
assert len(witness["quote_receipts"]) == 40
assert witness["diagram_count"] == 5
assert witness["whole_raw_original_SHA256"] == notes["pinned_original_volume2_full_raw_SHA256"]
assert (
    sha(B / "SOURCE_1963110_AUXILIARY_AND_BUREAU_EXCERPT.txt")
    == (notes["full_original_excerpt_SHA256"])
)
assert notes["independent_real_person_predictions_validated"] == notes["runtime_promotions"] == 0
assert all(not row["runtime_promoted"] for row in notes["record_rows"])
assert release["CRC_passed"] and release["all_member_SHA256_exact_bytes_passed"]
assert release["extracted_original_source_tests_passed"] == 58
assert release["prior_Chinese_V6_SHA256"] == sha(OLD)
assert release["parallel_Western_index_B07al_SHA256"] == sha(WEST)
assert release["source_notes_SHA256"] == sha(
    B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"
)
assert release["source_witness_SHA256"] == sha(
    B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json"
)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for file in [
    OLD,
    P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json",
    P / "CHINESE_SOURCE_AUDIT_INDEX_V4.json",
    P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json",
    P / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P / "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
    P / "batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json",
    WEST,
]:
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

BACK.mkdir(exist_ok=False)
for file, name in (
    (OLD, "CHINESE_V6_BEFORE_07.json"),
    (CURRENT, "CHINESE_CURRENT_BEFORE_07.md"),
    (WEST, "WESTERN_INDEX_B07al_BEFORE_07.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

updated = copy.deepcopy(old)
updated["schema"] = "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V7"
updated["status"] = "ZIWEI_VOLUME2_AUXILIARY_STARS_AND_FIVE_SOURCE_BUREAU_DIAGRAMS_DOCUMENTED"
updated["prior_index"] = "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
updated["prior_index_sha256"] = sha(OLD)
updated["as_of_utc"] = "2026-10-19"
updated["sum_source_annotations"] = 355
updated["original_chinese_source_anchors_checked_against_revision"] = 283
updated["accepted_batches"].append(
    {
        "id": "ChineseAstro-07",
        "added_bazi_source_annotations": 0,
        "added_ziwei_source_annotations": 40,
        "start": "ZWD-R0162",
        "end": "ZWD-R0201",
        "path": (
            "batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"
        ),
        "rules_sha256": sha(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"),
        "witness_path": "batches/ChineseAstro-07/SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json",
        "witness_sha256": sha(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json"),
        "source_original_raw_path": (
            "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
        ),
        "source_original_raw_sha256": notes["pinned_original_volume2_full_raw_SHA256"],
        "source_excerpt_sha256": notes["full_original_excerpt_SHA256"],
        "source_revisions": [1963110],
        "frozen_unparsed_five_bureau_diagrams": True,
        "source_focused_archive_test_replays": 58,
        "original_calendar_or_diagram_decoder_validated": False,
        "independent_real_person_predictions_validated": 0,
        "runtime_promotions": 0,
    }
)
zwd = updated["systems"][1]
zwd["accepted_source_annotations"] = 201
zwd["current_ids"] = "ZWD-R0001–ZWD-R0201"
zwd["next_id"] = "ZWD-R0202"
zwd["current_batch"] = "ChineseAstro-07"
zwd["source_files"].append(
    "batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"
)
zwd["chapter_coverage"] = (
    "Transmitted Zi Wei Volume II through auxiliary star classifications "
    "and original five elemental-bureau poems/diagrams after the eighteen "
    "regular star taxonomy. The five diagrams preserve exact original "
    "Wikitext bytes but are not validated palace placement algorithms. "
    "B07 contributes 40 source observations, 29 auxiliary star lines, "
    "5 source verses and 5 unreconstructed palace/day grids with full "
    "online oldid1963110 provenance. Neither source-era physical edition "
    "nor full original traditional calendar/14-star chart parity verified."
)
assert updated["systems"][0] == old["systems"][0]
assert sum(s["accepted_source_annotations"] for s in updated["systems"]) == 355
assert [b["id"] for b in updated["accepted_batches"]] == [
    b["id"] for b in old["accepted_batches"]
] + ["ChineseAstro-07"]
updated["separate_lilly_source_count_at_this_revision"] = 12611
updated["separate_ptolemy_source_count_at_this_revision"] = 1066
updated["ziwei_complete_natal_calendar_engine_verified"] = False
updated["chinese_bazi_solar_term_engine_verified"] = False
updated["full_ziwei_original_text_collation_finished"] = False
updated["all_14_principal_stars_verified"] = False
updated["independently_validated_real_human_claims"] = 0
updated["runtime_promotions"] = 0
updated["historical_glyph_and_translator_limits"] = (
    "Wikisource oldid1963110 is a transmitted online simplified text, "
    "not authenticated Ming original nor independently reviewed translation. "
    "Auxiliary stars must not be conflated with 18 regular star list; "
    "five old palace/day source diagrams are SHA preserved but not "
    "deciphered to a verified natal placement engine. Earlier Body Lord "
    "ambiguous 火玲 remains. Historical morality, health, status, wealth "
    "assertions remain documentary rhetoric, not verified actual people."
)
updated["source_parallel_western_history_binding"] = (
    "ChineseAstro-07 descends from Chinese V6 and parallel Lilly B07al "
    "index 12611; separately published B07am Western research is not "
    "merged into this source branch. Reconcile histories explicitly."
)
updated["next"] = (
    "Continue Zi Wei Volume II source after Fire-six bureau diagram at "
    "ZWD-R0202. Reconstruct remaining original bureau diagrams from "
    "full raw source with independently verified day/calendar positions. "
    "BaZi BZI-R0155 pinned further Di Tian Sui chapters. "
    "Lilly CLXVII next original source through separate Western branch. "
    "Full Chinese calendar/historical astronomical engine and prospective "
    "human blinded decoy tests remain the actual parent outcome."
)
NEW.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Chinese original-source progress V7: auxiliary Zi Wei stars and "
    "five original bureau diagrams\n\n"
    "**40 new exact Chinese source annotations ZWD-R0162–ZWD-R0201** from "
    "transmitted Zi Wei Quan Shu Volume II oldid1963110: 29 auxiliary "
    "star lines, the distinction from the eighteen regular stars, "
    "five original elemental-bureau verses and five exact preserved "
    "source palace/day diagrams. Pinned full raw document, original "
    "text excerpt, 40 SHA/offset witnesses and five diagram hashes "
    "retained with **58 independent ZIP replay source tests**. "
    "**Chinese historical annotations: 154 BaZi +201 Zi Wei =355**, "
    "old versions V1–V6 byte-preserved. Independent Western source "
    "branch at B07al **12611 Lilly+1066 Ptolemy=13677** unchanged; "
    "parallel later B07am must be reconciled separately. "
    "Actual bureau day-to-palace decodings, old print author authenticity, "
    "lunar calendar/time-zone engine and real-human forecast validity "
    "unverified. **Zero human predictive validations; no runtime promotions.** "
    "Next **ZWD-R0202** and **BZI-R0155**.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted historical checkpoint retained\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_ZIWEI_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "ChineseAstro-07",
    "status": "PINNED_ZIWEI_AUX_STARS_FIVE_BUREAU_DIAGRAMS_V7_INDEX_PREPARED_REMOTE_PENDING",
    "Chinese_before": 315,
    "Chinese_after": 355,
    "BaZi_retained": 154,
    "ZiWei_before": 161,
    "ZiWei_after": 201,
    "new_source_notes": 40,
    "next_ZiWei": "ZWD-R0202",
    "next_BaZi": "BZI-R0155",
    "original_raw_revision": 1963110,
    "original_raw_source_sha256": notes["pinned_original_volume2_full_raw_SHA256"],
    "prior_Chinese_V6_sha256": sha(BACK / "CHINESE_V6_BEFORE_07.json"),
    "new_Chinese_V7_sha256": sha(NEW),
    "new_notes_sha256": sha(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"),
    "new_witness_sha256": sha(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json"),
    "portable_archive_sha256": release["archive_sha256"],
    "portable_tests_replayed": 58,
    "Western_Lilly_pinned": 12611,
    "Ptolemy_pinned": 1066,
    "separate_parallel_Western_B07am_not_merged": True,
    "empirical_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
