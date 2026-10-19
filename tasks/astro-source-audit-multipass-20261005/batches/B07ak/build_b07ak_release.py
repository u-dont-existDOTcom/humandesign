#!/usr/bin/env python3
"""Portable historical first physical CLXVI end-source ZIP, 26 tests."""

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
REL = T + "/batches/B07ak/"
INDEX = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-1659-First-CLXVI-Naibod-Ending-B07ak-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    f = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if f is not None and f.is_dir() and f.resolve() != Path.home().resolve():
        return f
    d = Path.home() / "Téléchargements"
    return d if d.is_dir() else Path.home()


data = j(B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert j(ROOT / INDEX)["records_count"] == 12567
assert j(ROOT / CHINA)["sum_source_annotations"] == 262
assert len(data["cases"]) == 2 and len(rules["rules"]) == 14
assert data["cases"][0]["after_365day_year_carry"] == [12, 33, 14]
assert data["cases"][1]["after_365day_year_carry"] == [20, 57, 21]
assert data["source_first_printed_CLXVI_directions_time_text_physically_ends_PDF749"]
assert data["second_distinct_original_PRINTED_CLXVI_starts_same_PDF749"]
assert data["independently_blinded_actual_person_predictions"] == 0
assert data["runtime_promotions"] == 0
files = {
    REL + name: B / name
    for name in (
        "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json",
        "RULES.json",
        "ACCEPTANCE.json",
        "ORIGINAL_SOURCE_REVIEW_20261019.md",
        "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
        "TASK_SCOPE.json",
        "build_clxvi_naibod_final.py",
        "test_b07ak_clxvi_boundary.py",
        "build_b07ak_release.py",
        "prepare_b07ak_canonical.py",
    )
}
files[T + "/batches/B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"] = (
    B.parent / "B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"
)
for row in data["source_photographic_first_and_second_edition_witnesses"].values():
    files[row["relative_source"]] = ROOT / row["relative_source"]
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [k for k, v in files.items() if not v.is_file()]
for row in data["source_photographic_first_and_second_edition_witnesses"].values():
    assert sha(ROOT / row["relative_source"]) == row["photo_sha256"]
manifest = {
    "batch": "B07ak",
    "scope": "Original first Lilly printed CLXVI physical chapter ending, printed715",
    "original_source_pdf_sha256": data["source_photographic_first_and_second_edition_witnesses"][
        "original_1647"
    ]["original_full_1647_pdf_sha256"],
    "separate_1647_1659_same_folio715_print_witnesses": True,
    "Naibod_two_example_carry_results": [[12, 33, 14], [20, 57, 21]],
    "new_historical_source_notes": 14,
    "Lilly_if_admitted": 12581,
    "next_distinct_heading_same_printed_CLXVI": True,
    "next_historical_R": "R12582",
    "critical_expert_source_collation_complete": False,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
target = folder / NAME
temp = folder / (NAME + ".building")
assert not temp.exists()
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, f in files.items():
        z.write(f, "B07ak-root/" + name)
    z.writestr(
        "B07ak-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ak-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        p = root / name
        assert p.stat().st_size == meta["bytes"]
        assert sha(p) == meta["sha256"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ak_clxvi_boundary.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    result = re.search(r"Ran (\d+) tests", p.stderr)
    assert result and int(result.group(1)) == 26, p.stderr
    assert "skipped" not in p.stderr
os.replace(temp, target)
receipt = {
    "batch": "B07ak",
    "status": "FIRST_ORIGINAL_PHYSICAL_CLXVI_COVERED_26_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(target),
    "archive_bytes": target.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "all_member_SHA256_bytes_passed": True,
    "independent_archive_extraction_tests_passed": True,
    "portable_test_replays": 26,
    "original_source_SHA256": sha(
        B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json"
    ),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_index_SHA256": sha(ROOT / INDEX),
    "Chinese_V5_SHA256": sha(ROOT / CHINA),
    "new_historical_source_notes_if_admitted": 14,
    "first_physically_printed_CLXVI_source_pages_covered": True,
    "critical_text_verified_without_gaps": False,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
