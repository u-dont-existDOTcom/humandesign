#!/usr/bin/env python3
"""Portable hermetic Di Tian Sui source set with 53 exact citations and tests.

Packs six pinned Chinese Wikisource Wikitext page bytes, not just lossy
secondary glosses. The zip is independently extracted and the exact 69
source checks replayed offline, with per-file sha, length and CRC.
"""

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = "tasks/astro-chinese-primary-sources-20261017"
REL = P + "/batches/ChineseAstro-06/"
WEST = "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME = "Astrology-DiTianSui-53-Pinned-Chinese-Formations-B06-20261019.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    result = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    downloaded = (
        Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    )
    if (
        downloaded is not None
        and downloaded.is_dir()
        and downloaded.resolve() != Path.home().resolve()
    ):
        return downloaded
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


notes = j(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json")
witness = j(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json")
manifest = j(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json")
old = j(ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json")
western = j(ROOT / WEST)
assert old["sum_source_annotations"] == 262
assert old["systems"][0]["next_id"] == "BZI-R0102"
assert old["systems"][1]["next_id"] == "ZWD-R0162"
assert notes["source_annotations_added"] == 53
assert notes["historical_original_verse_anchors"] == 15
assert notes["later_transmitted_commentary_anchor_quotes"] == 38
assert witness["matched_independently_pinned_source_quotes"] == 53
assert notes["pinned_source_manifest_SHA256"] == sha(
    B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"
)
assert western["records_count"] == 12611
assert western["batches"][-1]["id"] == "B07al"
assert notes["independent_real_human_prediction_validations"] == notes["runtime_promotions"] == 0

names = [
    "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json",
    "SOURCE_CANDIDATES_UNVERIFIED_V1.json",
    "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json",
    "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json",
    "ORIGINAL_BAZI_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "freeze_ditiansui_original_53_source.py",
    "test_chinese06_pinned_original.py",
    "build_chinese_06_release.py",
    "prepare_chinese_06_index_v6.py",
]
names += [str(path.relative_to(B)) for path in sorted((B / "evidence").iterdir()) if path.is_file()]
files = {REL + name: B / name for name in names}
files[P + "/bazi/ditiansui_source_formations.py"] = ROOT / P / "bazi/ditiansui_source_formations.py"
files[P + "/bazi/bazi_source_mechanics.py"] = ROOT / P / "bazi/bazi_source_mechanics.py"
files[P + "/CHINESE_SOURCE_AUDIT_INDEX_V5.json"] = ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json"
files[WEST] = ROOT / WEST
assert all(file.is_file() for file in files.values()), [
    name for name, file in files.items() if not file.is_file()
]
for section, row in manifest.items():
    original = B / "evidence" / row["raw_file_local"]
    assert original.stat().st_size == row["source_bytes"], section
    assert sha(original) == row["source_sha256"], section

bundle = {
    "batch": "ChineseAstro-06",
    "historical_text": "Transmitted Di Tian Sui Wikitext 04/05/07/08/11/12 pinned original oldids",
    "source_early_Ming_edition_or_classical_authorship_verified": False,
    "original_chinese_page_sha256s": {key: row["source_sha256"] for key, row in manifest.items()},
    "original_Wikitext_page_revisions": {
        key: row["wikisource_oldid"] for key, row in manifest.items()
    },
    "source_annotations_verbatim_exact_anchor_count": 53,
    "verse_source_notes": 15,
    "commentary_source_notes": 38,
    "BZI_source_next_if_accepted": "BZI-R0155",
    "BaZi_source_after_if_accepted": 154,
    "ZiWei_historical_source_retained": 161,
    "Chinese_V6_source_after_if_accepted": 315,
    "separate_Western_Lilly_branch_snapshot_count": 12611,
    "source_first_edition_1647_lilly_branch_is_parallel_not_merged": True,
    "true_four_pillars_birth_calendar_and_human_predictions_verified": False,
    "independent_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "source_members": {
        name: {"sha256": sha(path), "bytes": path.stat().st_size} for name, path in files.items()
    },
}
dest = downloads()
dest.mkdir(parents=True, exist_ok=True)
archive = dest / NAME
temporary = dest / (NAME + ".building")
assert not temporary.exists()
with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "ChineseAstro-06-root/" + name)
    z.writestr(
        "ChineseAstro-06-root/RELEASE_MANIFEST.json",
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temporary) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "ChineseAstro-06-root"
    assert j(root / "RELEASE_MANIFEST.json") == bundle
    for name, record in bundle["source_members"].items():
        f = root / name
        assert f.stat().st_size == record["bytes"], name
        assert sha(f) == record["sha256"], name
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_chinese06_pinned_original.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    count = re.search(r"Ran (\d+) tests", p.stderr)
    assert count and int(count.group(1)) == 69, p.stderr
    assert "skipped" not in p.stderr
os.replace(temporary, archive)
receipt = {
    "batch": "ChineseAstro-06",
    "status": "PINNED_SIX_ORIGINAL_BAZI_PAGES_53_QUOTE_69_TEST_PORTABLE_REPLAY_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "archive_crc_passed": True,
    "all_file_SHA256_and_exact_bytes_passed": True,
    "independently_extracted_archive_tests_passed": True,
    "source_focused_tests_replayed": 69,
    "unmodified_historical_Chinese_earlier_test_suites_replayed": False,
    "old_Chinese_V5_index_SHA256": sha(ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json"),
    "old_Western_source_branch_index_SHA256": sha(ROOT / WEST),
    "source_notes_SHA256": sha(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"),
    "original_source_anchor_witness_SHA256": sha(
        B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"
    ),
    "pinned_source_original_six_Wikitext_SHA256s": [
        manifest[k]["source_sha256"] for k in sorted(manifest)
    ],
    "new_BaZi_historical_annotations_if_admitted": 53,
    "independent_actual_people_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
