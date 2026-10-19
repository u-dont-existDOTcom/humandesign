#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve original source metadata and exact paths.
"""Independently replay original CLXXIII 42-case photo-source ZIP archive."""

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
REL = T + "/batches/B07av/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-CLXXIII-1647-1659-42-Planetary-Returns-B07av-20261019.zip"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


data = j(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json")
rules = j(B / "RULES.json")
photos = j(B / "SOURCE_PHOTO_CHECKPOINT_V1.json")
proof = j(B / "SOURCE_RULE_PROVENANCE_V1.json")
accept = j(B / "ACCEPTANCE.json")
prior = j(ROOT / WEST)
chinese = j(ROOT / CHINA)
assert prior["records_count"] == 12803
assert prior["batches"][-1]["id"] == "B07au"
assert chinese["sum_source_annotations"] == 355
assert len(data["records"]) == 42
assert len(rules["rules"]) == 43
assert len(proof["source_rule_locators"]) == 42
assert accept["next_original_source_R"] == "R12847"
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["source_matrix_sha256"] == sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json")
assert accept["source_provenance_sha256"] == sha(B / "SOURCE_RULE_PROVENANCE_V1.json")
assert accept["original_next_heading_variant_witness_sha256"] == sha(
    B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"
)
assert data["actual_real_human_forecasts_validated"] == 0
assert data["runtime_model_promotions"] == 0

names = [
    ".gitattributes",
    "CONTINUATION_PHOTO_CHECKPOINT_20261019.md",
    "CONTINUATION_MATRIX_CHECKPOINT_20261019.md",
    "SOURCE_PHOTO_CHECKPOINT_V1.json",
    "CLXXIII_42_SOURCE_CANDIDATES_V1.json",
    "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json",
    "SOURCE_RULE_PROVENANCE_V1.json",
    "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json",
    "SECONDARY_FINDING_AID_CLXXIII.txt",
    "RULES.json",
    "ACCEPTANCE.json",
    "build_b07av_photo_checkpoint.py",
    "build_b07av_source_matrix.py",
    "test_b07av_source_matrix.py",
    "build_b07av_release.py",
    "prepare_b07av_canonical.py",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
]
files = {REL + name: B / name for name in names}
for version, entries in photos["source_original_visual_evidence"].items():
    for rec in entries:
        relative = rec["repo_relative_file"]
        f = ROOT / relative
        assert f.is_file(), (version, f)
        assert sha(f) == rec["sha256"]
        assert f.stat().st_size == rec["bytes"]
        files[relative] = f
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert len(files) == len(names) + 8 + 2
assert all(f.is_file() for f in files.values()), [
    name for name, f in files.items() if not f.is_file()
]
manifest = {
    "batch": "B07av",
    "status": "COVERED_AS_HISTORICAL_SOURCE_NOT_CHART_OR_HUMAN_PREDICTIVE_VALIDATION",
    "source_Wellcome_1647_full_pdf_sha256": photos["full_1647_first_edition_pdf_sha256"],
    "source_first_original_1647_and_second_typeset_1659_photo_count": 8,
    "physical_printed_folios": [738, 739, 740, 741],
    "historical_returning_planets_six": rules["original_source_heading_stars"],
    "source_natal_target_count": 7,
    "historic_return_to_radix_source_cases": 42,
    "historical_first_to_last": ["R12804", "R12846"],
    "source_boundary_to_CLXXIV": True,
    "new_historical_annotation_count": 43,
    "Lilly_history_if_accepted": 12846,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "expert_diplomatic_all_glyphs_source_review": False,
    "era_accurate_birth_and_solar_return_engine_verified": False,
    "independent_human_life_event_predictions_validated": 0,
    "runtime_promotions": 0,
    "member_records": {k: {"sha256": sha(f), "bytes": f.stat().st_size} for k, f in files.items()},
}
d = downloads()
d.mkdir(parents=True, exist_ok=True)
archive = d / NAME
temp = d / (NAME + ".building")
assert not temp.exists()
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07av-root/" + name)
    z.writestr(
        "B07av-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    restored = Path(td) / "B07av-root"
    assert j(restored / "RELEASE_MANIFEST.json") == manifest
    for name, rec in manifest["member_records"].items():
        f = restored / name
        assert f.stat().st_size == rec["bytes"]
        assert sha(f) == rec["sha256"]
    test = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(restored / REL),
            "-p",
            "test_b07av_source_matrix.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert test.returncode == 0, test.stdout + "\n" + test.stderr
    m = re.search(r"Ran (\d+) tests", test.stderr)
    assert m and int(m.group(1)) == 54, test.stderr
    assert "skipped" not in test.stderr
os.replace(temp, archive)
receipt = {
    "batch": "B07av",
    "status": "ORIGINAL_CLXXIII_42_SOURCE_CASES_54_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "source_member_count": len(files),
    "CRC_passed": True,
    "all_member_sha256_and_exact_bytes_passed": True,
    "independent_archive_extracted_test_replays": 54,
    "source_matrix_sha256": sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "source_provenance_sha256": sha(B / "SOURCE_RULE_PROVENANCE_V1.json"),
    "original_photo_checkpoint_sha256": sha(B / "SOURCE_PHOTO_CHECKPOINT_V1.json"),
    "prior_Lilly_history_source_index_sha256": sha(ROOT / WEST),
    "Chinese_V7_source_index_sha256": sha(ROOT / CHINA),
    "new_source_historical_records_if_accepted": 43,
    "old_CLXXIII_physically_covered": True,
    "complete_source_critical_historical_expert_review": False,
    "actual_human_life_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_canonical_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
