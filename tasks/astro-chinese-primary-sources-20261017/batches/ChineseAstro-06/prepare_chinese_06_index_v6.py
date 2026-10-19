#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete repository source references.
"""Guarded append-only Chinese historical source V6: 53 Di Tian Sui notes.

This commits source observations, NOT predictive validated astrology. The
Western source branch is pinned to B07al; concurrent later Western work is
a distinct Git branch and must be separately reconciled, not invented here.
"""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
V5 = P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json"
V6 = P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_06.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-chinese-06-ditiansui-original-20261019"
PINNED_PARENT = "38fd127fe675323f44ae40da5167a549420779dd"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for p in (V6, LATEST, RECEIPT, BACK / "CHINESE_V5_BEFORE_06.json"):
    assert not p.exists(), f"Interrupted or earlier index mutation; reconcile first: {p}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PINNED_PARENT
old = j(V5)
west = j(WEST)
source = j(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json")
witness = j(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json")
manifest = j(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert old["sum_source_annotations"] == 262
assert old["accepted_batches"][-1]["id"] == "ChineseAstro-05"
assert old["systems"][0]["accepted_source_annotations"] == 101
assert old["systems"][0]["next_id"] == "BZI-R0102"
assert old["systems"][1]["accepted_source_annotations"] == 161
assert old["systems"][1]["next_id"] == "ZWD-R0162"
assert old["original_chinese_source_anchors_checked_against_revision"] == 190
assert old["independently_validated_real_human_claims"] == old["runtime_promotions"] == 0
assert west["records_count"] == 12611
assert west["batches"][-1]["id"] == "B07al"
assert west["empirical_validations"] == west["runtime_promotions"] == 0
assert source["source_annotations_added"] == 53
assert source["first_id"] == "BZI-R0102"
assert source["last_id"] == "BZI-R0154"
assert source["next_id"] == "BZI-R0155"
assert [r["id"] for r in source["records"]] == [f"BZI-R{n:04d}" for n in range(102, 155)]
assert source["historical_original_verse_anchors"] == 15
assert source["later_transmitted_commentary_anchor_quotes"] == 38
assert source["independent_real_human_prediction_validations"] == source["runtime_promotions"] == 0
assert witness["matched_independently_pinned_source_quotes"] == 53
assert witness["actual_real_person_outcome_validation_count"] == witness["runtime_promotions"] == 0
assert len(manifest) == 6
assert source["pinned_source_manifest_SHA256"] == sha(
    B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"
)
assert witness["original_source_manifest_SHA256"] == source["pinned_source_manifest_SHA256"]
for _chapter, data in manifest.items():
    file = B / "evidence" / data["raw_file_local"]
    assert file.stat().st_size == data["source_bytes"]
    assert sha(file) == data["source_sha256"]
assert all(r["original_quote_directly_matched"] for r in source["records"])
assert all(not r["runtime_promoted"] for r in source["records"])
assert release["archive_crc_passed"]
assert release["all_file_SHA256_and_exact_bytes_passed"]
assert release["independently_extracted_archive_tests_passed"]
assert release["source_focused_tests_replayed"] == 69
assert release["old_Chinese_V5_index_SHA256"] == sha(V5)
assert release["old_Western_source_branch_index_SHA256"] == sha(WEST)
assert release["source_notes_SHA256"] == sha(
    B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"
)
assert release["original_source_anchor_witness_SHA256"] == sha(
    B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"
)
archive = downloads() / release["filename"]
assert archive.is_file() and sha(archive) == release["archive_sha256"]

for p in (
    V5,
    P / "CHINESE_SOURCE_AUDIT_INDEX_V4.json",
    P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json",
    P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json",
    P / "CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P / "bazi/bazi_source_mechanics.py",
    P / "bazi/ditiansui_historical_conventions.py",
    P / "batches/ChineseAstro-05/BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json",
    WEST,
):
    relative = str(p.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(p)), relative

BACK.mkdir(exist_ok=False)
for p, n in (
    (V5, "CHINESE_V5_BEFORE_06.json"),
    (CURRENT, "CHINESE_CURRENT_BEFORE_06.md"),
    (WEST, "WESTERN_INDEX_B07al_BEFORE_06.json"),
):
    (BACK / n).write_bytes(p.read_bytes())

v6 = copy.deepcopy(old)
v6["schema"] = "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V6"
v6["status"] = "BAZI_SIX_DITIAN_SUI_FORMATIONS_TRUE_FALSE_CAVEATS_DOCUMENTED"
v6["as_of_utc"] = "2026-10-19"
v6["prior_index"] = "CHINESE_SOURCE_AUDIT_INDEX_V5.json"
v6["prior_index_sha256"] = sha(V5)
v6["sum_source_annotations"] = 315
v6["original_chinese_source_anchors_checked_against_revision"] = 243
v6["accepted_batches"].append(
    {
        "id": "ChineseAstro-06",
        "added_bazi_source_annotations": 53,
        "added_ziwei_source_annotations": 0,
        "start": "BZI-R0102",
        "end": "BZI-R0154",
        "path": "batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json",
        "rules_sha256": sha(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"),
        "witness_path": "batches/ChineseAstro-06/PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json",
        "witness_sha256": sha(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"),
        "source_manifest_path": "batches/ChineseAstro-06/DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json",
        "source_manifest_sha256": sha(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"),
        "source_pinned_multiple_revision_ids": {
            chapter: row["wikisource_oldid"] for chapter, row in manifest.items()
        },
        "raw_source_evidence_preserved_in_repository": True,
        "portable_new_source_focused_tests_replayed": 69,
        "unmodified_older_historical_suites_replayed": False,
        "independent_human_predictions_validated": 0,
        "runtime_rules_promoted": 0,
    }
)
bazi = v6["systems"][0]
bazi["accepted_source_annotations"] = 154
bazi["current_ids"] = "BZI-R0001–BZI-R0154"
bazi["next_id"] = "BZI-R0155"
bazi["current_batch"] = "ChineseAstro-06"
bazi["source_files"].append(
    "batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"
)
bazi["chapter_coverage"] = (
    "Earlier 101 BaZi historical annotations plus 53 pinned exact "
    "Chinese verse/commentary observations from transmitted Di Tian Sui "
    "04/05/07/08/11/12: form-versus-group, genuine-versus-apparent "
    "following and transformation, full-source context for strength "
    "exceptions and essence/spirit metaphor. Six exact original raw "
    "Wikitext page SHA and quote byte offsets are preserved; author, "
    "early woodblock and actual prognostic accuracy unresolved."
)
v6["separate_lilly_source_count_at_this_revision"] = 12611
v6["separate_ptolemy_source_count_at_this_revision"] = 1066
v6["full_ziwei_original_text_collation_finished"] = False
v6["all_14_principal_stars_verified"] = False
v6["ziwei_complete_natal_calendar_engine_verified"] = False
v6["chinese_bazi_solar_term_engine_verified"] = False
v6["independently_validated_real_human_claims"] = 0
v6["runtime_promotions"] = 0
v6["historical_glyph_and_translator_limits"] = (
    "The exact Di Tian Sui online source snapshot is not authenticated "
    "early printed source or expert classical Chinese translation; "
    "15 historical verse records and 38 commentary spans are distinct "
    "text layers, and appearance/fortune/moralizing claims are historical "
    "claims only. A strong composition can contain weakness and vice "
    "versa; no binary source-strength-to-outcome rule is validated. "
    "Original Zi Wei 火玲 ambiguity persists unaltered. No chart "
    "calendar parity or actual-person prospective test."
)
v6["source_parallel_western_history_binding"] = (
    "This ChineseAstro-06 branch derives from published B07al Lilly count "
    "12611, not any concurrently edited B07am CLXVII branch. Merge "
    "later Western progress only after reading its independent history; "
    "Chinese source notes never overwrite Western registry."
)
v6["next"] = (
    "Continue exact pinned Di Tian Sui BaZi BZI-R0155 in chapters 13 "
    "onward; independently authenticate old physical print, authorship "
    "and commentary layers, genuine BaZi year/month/day/hour solar-term "
    "calendar. Resume Zi Wei ZWD-R0162 at original source diagrams. "
    "Separately reconcile newer Lilly CLXVII Western source branch. "
    "Human forward-blind and reverse-match trials only after chart/model "
    "freeze, unmatched controls and held-out data."
)
assert [x["id"] for x in v6["accepted_batches"]] == (
    [x["id"] for x in old["accepted_batches"]] + ["ChineseAstro-06"]
)
assert sum(x["accepted_source_annotations"] for x in v6["systems"]) == 315
assert v6["systems"][1] == old["systems"][1]
V6.write_text(json.dumps(v6, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Chinese source-first V6: six pinned Di Tian Sui chapters with 53 original Chinese anchors\n\n"
    "**53 new historical BaZi source annotations BZI-R0102–BZI-R0154** "
    "are each verified against exact raw Chinese Wikitext and SHA/offset "
    "from six pinned transmitted Di Tian Sui pages: 15 old verses and "
    "38 undated commentary excerpts. The source distinguishes eastern "
    "wood direction vs wood triad, actual vs apparent following or "
    "transformation, and explicitly requires exceptions to simple "
    "strong/weak rules. Moralizing historic predictions are NOT "
    "verified real-person evidence. "
    "Chinese historical records **154 BaZi +161 Zi Wei=315**, "
    "previous V1–V5 retained byte-identical. "
    "**69 focused tests replayed from source-carrying independently "
    "extracted ZIP with CRC/SHA/exact-byte verification**; earlier "
    "unchanged suites not needlessly rerun on a different West-era fixture. "
    "Separate Western source branch pinned **12,611 Lilly +1,066 "
    "Ptolemy=13,677**, while other Western CLXVII work is continuing "
    "independently. Next **BZI-R0155**, **ZWD-R0162**. "
    "No completed BaZi birth calendar/actual chart engine, no independently "
    "blinded human outcome validations and no live model promotions.\n\n"
)
previous_state = CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    summary + "## Earlier accepted checkpoint retained verbatim\n\n" + previous_state,
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_BAZI_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "ChineseAstro-06",
    "status": "BAZI_53_EXACT_SOURCE_VERSES_COMMENTARY_V6_PREPARED_REMOTE_PENDING",
    "Chinese_before": 262,
    "Chinese_after": 315,
    "BaZi_before": 101,
    "BaZi_after": 154,
    "ZiWei_retained": 161,
    "new_Chinese_primary_source_notes": 53,
    "historical_verses": 15,
    "historical_commentary": 38,
    "prior_Chinese_V5_SHA256": sha(BACK / "CHINESE_V5_BEFORE_06.json"),
    "new_Chinese_V6_SHA256": sha(V6),
    "source_notes_SHA256": sha(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"),
    "source_witness_SHA256": sha(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"),
    "original_six_pinned_pages_manifest_SHA256": sha(
        B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"
    ),
    "archive_SHA256": release["archive_sha256"],
    "portable_focused_test_replays": 69,
    "Western_Lilly_branch_B07al_retained": 12611,
    "Ptolemy_retained": 1066,
    "next_BaZi": "BZI-R0155",
    "next_ZiWei": "ZWD-R0162",
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
