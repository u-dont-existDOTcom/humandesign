#!/usr/bin/env python3
"""Versioned append-only Chinese source registry without changing historic V1 or Lilly."""

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
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LILLY = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
BACKUP = B / "PREVIOUS_CHINESE_STATE_20261018.md"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for file in (V2, BACKUP):
    assert not file.exists(), f"Existing prepared state; reconcile instead of retrying: {file}"

assert git("branch", "--show-current") == (
    "research/astro-chinese-02-ziwei-classical-placements-20261018"
)
assert git("rev-parse", "HEAD") == "7f343c8f544b2dde087998ca1f7cdd8b8208e460"

v1 = j(V1)
note = j(B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
lilly = j(LILLY)
assert (
    v1["sum_source_annotations"],
    v1["systems"][0]["accepted_source_annotations"],
    v1["systems"][1]["accepted_source_annotations"],
) == (72, 46, 26)
assert v1["systems"][1]["next_id"] == "ZWD-R0027"
assert v1["independently_validated_real_human_claims"] == v1["runtime_promotions"] == 0
assert witness["wikitext_sha256"] == note["raw_source_sha256"]
assert witness["accepted_quote_count"] == note["count"] == 25
assert witness["unmatched"] == []
assert all(r["original_revision_quote_match_confirmed"] for r in note["records"])
assert [r["id"] for r in note["records"]] == [f"ZWD-R{n:04d}" for n in range(27, 52)]
assert all(not r["runtime_promoted"] for r in note["records"])
assert lilly["records_count"] == 11325
assert lilly["batches"][-1]["id"] == "B07q"

for protected in (
    V1,
    P / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    LILLY,
):
    rel = str(protected.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(protected))

v2 = {
    "schema": "ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V2",
    "status": "SOURCE_FIRST_ZIWEI_VOLUME2_PART_A_ANCHORS_VERIFIED_NO_MODEL_PROMOTION",
    "as_of_utc": "2026-10-18",
    "prior_index": "CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    "prior_index_sha256": sha(V1),
    "systems": copy.deepcopy(v1["systems"]),
    "sum_source_annotations": 97,
    "source_manifest": v1["source_manifest"],
    "initial_historical_witness": "ZIWEI_SOURCE_FIRST_RULES_V1.json",
    "accepted_batches": [
        {
            "id": "ChineseAstro-01",
            "accepted_bazi_source_annotations": 46,
            "accepted_ziwei_source_annotations": 26,
            "index_snapshot": "CHINESE_SOURCE_AUDIT_INDEX_V1.json",
        },
        {
            "id": "ChineseAstro-02",
            "added_bazi_source_annotations": 0,
            "added_ziwei_source_annotations": 25,
            "start": "ZWD-R0027",
            "end": "ZWD-R0051",
            "path": "batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
            "rules_sha256": sha(B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"),
            "witness_path": "batches/ChineseAstro-02/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
            "witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
            "source_permalink_revision": 1963110,
            "wikitext_sha256": note["raw_source_sha256"],
            "independent_human_predictions_validated": 0,
            "runtime_rules_promoted": 0,
        },
    ],
    "full_ziwei_original_text_collation_finished": False,
    "all_14_principal_stars_verified": False,
    "ziwei_complete_natal_calendar_engine_verified": False,
    "chinese_bazi_solar_term_engine_verified": False,
    "historical_glyph_and_translator_limits": (
        "Wikisource pinned 1963110 raw wikitext is Simplified; Traditional viewer glyphs "
        "are derived rendering. Short source anchors match exact raw bytes, but "
        "no independent expert transcription/translation or edition-critical parity."
    ),
    "original_chinese_source_anchors_checked_against_revision": 25,
    "separate_lilly_source_count_at_this_revision": 11325,
    "separate_ptolemy_source_count_at_this_revision": 1066,
    "independently_validated_real_human_claims": 0,
    "runtime_promotions": 0,
    "next": (
        "Continue Zi Wei Quan Shu volume 2 separate constellation and timing "
        "rules from pinned first-edition witness ZWD-R0052 onward; complete BaZi "
        "and classical source audits separately; independent chart/calendars "
        "and blinded human validation not established."
    ),
}

z = v2["systems"][1]
z["accepted_source_annotations"] = 51
z["current_ids"] = "ZWD-R0001–ZWD-R0051"
z["next_id"] = "ZWD-R0052"
z["current_batch"] = "ChineseAstro-02"
z["source_files"] = [
    "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    "batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
]
z["chapter_coverage"] = (
    "Selected Vol1–3 historical notes plus pinned oldid1963110 Vol2 25 "
    "auxiliary-star, four-transformation and palace/source mechanic notes. "
    "NOT exhaustive, no independently verified star/birth-calendar parity."
)

BACKUP.write_bytes(CURRENT.read_bytes())
V2.write_text(json.dumps(v2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
previous = CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    "# Chinese astrology source study: Zi Wei Volume II source-verified expansion\n\n"
    "2026-10-18 UTC. The current canonical source-only Chinese index is "
    "`CHINESE_SOURCE_AUDIT_INDEX_V2.json`: **46 BaZi +51 Zi Wei=97 "
    "historical documentary annotations**, including **25 new Chinese "
    "source-anchored records ZWD-R0027–ZWD-R0051** against pinned "
    "Wikisource Volume II oldid 1963110/raw SHA256 "
    "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72. "
    "Original retained index V1 remains unchanged at 72. "
    "Source glyph fidelity verified for short raw anchor strings; "
    "independent sinological translation/full-chart parity not established.\n\n"
    "**No full BaZi or Zi Wei chart engine, no blind actual-person "
    "predictive validation, no runtime prediction/claim promotion.** "
    "Bounded auxiliary-star arithmetic is testable but not calendar-correct "
    "across leap months and historical local clocks without further work. "
    "Lilly B07q remains separate at 11,325 and Ptolemy 1,066. "
    "Next Zi Wei ZWD-R0052, BaZi BZI-R0047.\n\n"
    "## Earlier Chinese checkpoint (retained verbatim)\n\n" + previous,
    encoding="utf-8",
)
print(
    json.dumps(
        {
            "prepared_index": "CHINESE_SOURCE_AUDIT_INDEX_V2.json",
            "before": 72,
            "now": 97,
            "bazi": 46,
            "ziwei": 51,
            "next_ziwei": "ZWD-R0052",
            "lilly_unchanged": 11325,
            "source_verified": witness["accepted_quote_count"],
            "index_sha256": sha(V2),
        },
        ensure_ascii=False,
        indent=2,
    )
)
