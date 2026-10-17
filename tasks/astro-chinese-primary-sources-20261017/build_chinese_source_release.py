#!/usr/bin/env python3
"""Public-safe portable source research evidence packet: NO copyrighted ebook bytes."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


names = [
    "SOURCE_MANIFEST_V1.json",
    "CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    "RESEARCH_PLAN_20261017.md",
    "SOURCE_REVIEW_20261017.md",
    "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    "bazi/bazi_source_mechanics.py",
    "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    "ziwei/ziwei_source_mechanics.py",
    "tests/test_chinese_source_mechanics.py",
    "build_chinese_source_release.py",
]
assert all((B / n).is_file() for n in names)
assert not list(B.rglob("*.epub")) and not list(B.rglob("*.pdf"))
a = json.loads((B / names[4]).read_text())
z = json.loads((B / names[6]).read_text())
inventory = json.loads((B / names[0]).read_text())
assert a["count"] == 46 and z["count"] == 26
assert inventory["authoring_contract"]["actual_predictions_verified"] == 0
assert inventory["authoring_contract"]["runtime_promotions"] == 0
manifest = {
    "schema": "ASTRO_CHINESE_SOURCE_ARCHIVE_V1",
    "scope": (
        "2005/2006 authored BaZi and transmitted Zi Wei original Chinese first-source paraphrases"
    ),
    "research_records": 72,
    "bazi_records": 46,
    "ziwei_records": 26,
    "focused_tests_replayed": 38,
    "full_birth_chart_engine_validated": False,
    "human_prediction_validations": 0,
    "runtime_source_promotions": 0,
    "owner_ebook_bytes_embedded": False,
    "members": {n: {"bytes": (B / n).stat().st_size, "sha256": sha(B / n)} for n in names},
}
r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
downloads = (
    Path(r.stdout.strip())
    if r.returncode == 0 and r.stdout.strip()
    else Path.home() / "Téléchargements"
)
downloads.mkdir(parents=True, exist_ok=True)
out = downloads / "Astrology-Chinese-BaZi-ZiWei-Source-Research-20261017.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for name in names:
        archive.write(B / name, "ChineseAstro/" + name)
    archive.writestr(
        "ChineseAstro/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as archive, tempfile.TemporaryDirectory() as t:
    assert archive.testzip() is None
    archive.extractall(t)
    root = Path(t) / "ChineseAstro"
    assert json.loads((root / "RELEASE_MANIFEST.json").read_text()) == manifest
    for name, fields in manifest["members"].items():
        p = root / name
        assert p.stat().st_size == fields["bytes"]
        assert sha(p) == fields["sha256"]
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / "tests"),
            "-p",
            "test_chinese_source_mechanics.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert run.returncode == 0 and "Ran 38 tests" in run.stderr, run.stderr
receipt = {
    "schema": "ASTRO_CHINESE_SOURCE_RELEASE_RECEIPT_V1",
    "batch": "ChineseAstro-01",
    "status": "SOURCE_ONLY_EVIDENCE_ARCHIVE_ZIP_CRC_SHA_38_TESTS_PASS",
    "archive_path": str(out),
    "archive_bytes": out.stat().st_size,
    "archive_sha256": sha(out),
    "source_manifest_sha256": sha(B / "SOURCE_MANIFEST_V1.json"),
    "bazi_rules_sha256": sha(B / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json"),
    "ziwei_rules_sha256": sha(B / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json"),
    "crc_passed": True,
    "all_members_sha256_passed": True,
    "extraction_passed": True,
    "focused_tests_replayed": 38,
    "historical_notes": 72,
    "complete_chart_engines": 0,
    "independent_human_prediction_validations": 0,
    "runtime_promotions": 0,
    "copyrighted_book_bytes_included": False,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
