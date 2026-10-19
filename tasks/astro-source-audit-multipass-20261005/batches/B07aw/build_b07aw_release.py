#!/usr/bin/env python3
"""Produce self-contained B07aw original 1647/1659 transit photographic source ZIP.

Verifies archive CRC, every archived file SHA+size, replays forty source-only
tests after clean extraction. Nothing here validates birth-time ephemeris or
actual-human astrology. Keep canon and previous work immutable.
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
T = "tasks/astro-source-audit-multipass-20261005"
REL = T + "/batches/B07aw/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXXIV-Transits-B07aw-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    x = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(x.stdout.strip()) if x.returncode == 0 and x.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


data = j(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
before = j(ROOT / WEST)
china = j(ROOT / CHINA)
assert before["records_count"] == 12846 and before["batches"][-1]["id"] == "B07av"
assert china["sum_source_annotations"] == 355
assert data["source_historical_record_count"] == 22
assert rules["record_count"] == 22
assert len(rules["rules"]) == 22
assert accept["next_original_R"] == "R12869"
assert not data["source_critical_professional_collation_complete"]
assert data["independent_real_human_predictions_validated"] == 0
assert data["runtime_promotions"] == 0
assert accept["source_SHA256"] == sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
assert accept["rules_SHA256"] == sha(B / "RULES.json")

names = [
    ".gitattributes",
    "RECOVERY_CHECKPOINT.json",
    "CONTINUATION.md",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "SECONDARY_SEARCH_NAVIGATOR_TRANSITS.txt",
    "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "build_b07aw_original_transits.py",
    "test_b07aw_original_transit_source.py",
    "test_b07aw_post_index.py",
    "prepare_b07aw_canonical.py",
    "build_b07aw_release.py",
]
files = {REL + name: B / name for name in names}
for f in sorted((B / "evidence").glob("*.jpg")):
    files[REL + str(f.relative_to(B))] = f

parent = B.parent / "B07av"
for name in ["RULES.json", "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"]:
    files[T + "/batches/B07av/" + name] = parent / name
for name in ["1647_original_775-775.jpg", "independent_1659_djvu770.jpg"]:
    files[T + "/batches/B07av/evidence/" + name] = parent / "evidence" / name
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values()), [x for x, p in files.items() if not p.is_file()]

photos = data["original_photo_witnesses"]
for entry in photos.values():
    p = ROOT / entry["path"]
    assert sha(p) == entry["SHA256"]
    assert p.stat().st_size == entry["exact_bytes"]
manifest = {
    "batch": "B07aw",
    "source": (
        "Original Lilly Christian Astrology 1647 first edition vs separately "
        "typeset 1659 transit chapter"
    ),
    "source_full_1647_scan_SHA256": data["source_original_1647_full_book_pdf_sha256"],
    "first_edition_literal_chapter": "CLXXIIII",
    "second_edition_literal_chapter": "CLXXIV",
    "next_physical_chapter": "CLXXV",
    "source_physical_transit_chapter_one_page": True,
    "source_selected_Jupiter_and_Venus_not_secondary_Mars": True,
    "source_Mars_duration_first_print_dayes_second_print_yeares": True,
    "historical_source_notes": 22,
    "Lilly_after_if_accepted": 12868,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "source_two_reader_professional_collation_complete": False,
    "original_astro_transit_ephemeris_engine_validated": False,
    "actual_human_predictive_validations": 0,
    "runtime_model_promotions": 0,
    "members": {name: {"sha256": sha(p), "bytes": p.stat().st_size} for name, p in files.items()},
}
dest = downloads()
dest.mkdir(parents=True, exist_ok=True)
archive = dest / NAME
temporary = dest / (NAME + ".building")
assert not temporary.exists(), temporary
with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, p in files.items():
        z.write(p, "B07aw-root/" + name)
    z.writestr(
        "B07aw-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temporary) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    base = Path(td) / "B07aw-root"
    assert j(base / "RELEASE_MANIFEST.json") == manifest
    for name, expected in manifest["members"].items():
        p = base / name
        assert p.stat().st_size == expected["bytes"], name
        assert sha(p) == expected["sha256"], name
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(base / REL),
            "-p",
            "test_b07aw_original_transit_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert run.returncode == 0, run.stdout + "\n" + run.stderr
    match = re.search(r"Ran (\d+) tests", run.stderr)
    assert match and int(match.group(1)) == 40, run.stderr
    assert "skipped" not in run.stderr
os.replace(temporary, archive)
receipt = {
    "batch": "B07aw",
    "status": "1647_1659_ORIGINAL_TRANSITS_22_SOURCE_NOTES_40_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "member_hashes_and_bytes_passed": True,
    "independent_ZIP_test_replay_passed": 40,
    "source_SHA256": sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "prior_Lilly_index_SHA256": sha(ROOT / WEST),
    "Chinese_V7_index_SHA256": sha(ROOT / CHINA),
    "historical_source_annotation_count": 22,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
    "remote_canonical_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
