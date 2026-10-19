#!/usr/bin/env python3
"""Archive original CLXX primary photo source and 30 independent test replays."""

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
REL = T + "/batches/B07ar/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXX-Sun-Midheaven-12-Houses-B07ar-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


source = j(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert j(ROOT / WEST)["records_count"] == 12725
assert j(ROOT / CHINA)["sum_source_annotations"] == 355
assert len(source["records"]) == len(rules["rules"]) == 17
assert len(source["all_four_original_first_second_printed_photo_sha256s"]) == 4
assert source["source_record_count"] == 17
assert not source["personal_astrological_predictive_accuracy_verified"]
assert accept["source_notes_SHA256"] == sha(
    B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json"
)
assert accept["rules_SHA256"] == sha(B / "RULES.json")
names = [
    "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "SECONDARY_CLXX_SOURCE_NAVIGATOR.txt",
    ".gitattributes",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_original_clxx_source.py",
    "test_b07ar_clxx_original.py",
    "build_b07ar_release.py",
    "prepare_b07ar_canonical.py",
]
files = {REL + name: B / name for name in names}
for info in source["all_four_original_first_second_printed_photo_sha256s"].values():
    files[info["source_relative_path"]] = ROOT / info["source_relative_path"]
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [p for p, f in files.items() if not f.is_file()]
for info in source["all_four_original_first_second_printed_photo_sha256s"].values():
    f = ROOT / info["source_relative_path"]
    assert sha(f) == info["file_sha256"]
    assert f.stat().st_size == info["file_bytes"]
manifest = {
    "batch": "B07ar",
    "source": (
        "Lilly Christian Astrology actual first 1647 and separately "
        "typeset 1659 original CLXX p731-732"
    ),
    "primary_source_original_1647_full_book_sha256": source["original_book_full_1647_pdf_sha256"],
    "four_original_printed_full_page_images": True,
    "all_twelve_mid_heaven_sun_source_houses": True,
    "new_historical_documentary_notes": 17,
    "Lilly_if_admitted": 12742,
    "Chinese_V7_history_retained": 355,
    "next_original_source_CLXXI": "R12743",
    "independent_critical_edition_full_proof": False,
    "calendar_natal_chart_human_predictive_accuracy_established": False,
    "human_prediction_success_count": 0,
    "runtime_model_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
tmp = folder / (NAME + ".building")
assert not tmp.exists()
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ar-root/" + name)
    z.writestr(
        "B07ar-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ar-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = root / name
        assert sha(f) == meta["sha256"]
        assert f.stat().st_size == meta["bytes"]
    q = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ar_clxx_original.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert q.returncode == 0, q.stdout + "\n" + q.stderr
    n = re.search(r"Ran (\d+) tests", q.stderr)
    assert n and int(n.group(1)) == 30, q.stderr
    assert "skipped" not in q.stderr
os.replace(tmp, archive)
rec = {
    "batch": "B07ar",
    "status": "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_30_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "CRC_passed": True,
    "all_member_SHA256_bytes_passed": True,
    "independent_extraction_test_replay_passed": True,
    "portable_tests": 30,
    "notes_sha256": sha(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "prior_Western_index_sha256": sha(ROOT / WEST),
    "prior_Chinese_V7_index_sha256": sha(ROOT / CHINA),
    "new_historical_rules_if_accepted": 17,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(rec, indent=2))
