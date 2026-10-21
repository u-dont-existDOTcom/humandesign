#!/usr/bin/env python3
"""Cold-extractable Zi Wei V15 source ZIP with SHA/CRC and independent tests."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = Path("tasks/astro-chinese-primary-sources-20261017")
BATCH = TASK / "batches/ChineseAstro-15SRC-Life"
DEST = Path("/home/joel/Téléchargements/Astrology-ZiWei-Life-Auxiliary-Second-Four-54-Original-Sources-V15-20261021.zip")


def sha(v: bytes) -> str:
    return hashlib.sha256(v).hexdigest()


def main() -> None:
    names = [
        TASK / "CHINESE_SOURCE_AUDIT_INDEX_V14.json",
        TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
        TASK / "batches/ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json",
        Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
    ]
    names += [BATCH / x for x in [
        "WORKING_CHECKPOINT_20261021.md",
        "SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt",
        "ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json",
        "SOURCE_LIFE_SECOND_FOUR_AUXILIARY_EXACT_OFFSET_WITNESS_V1.json",
        "ACCEPTANCE.json",
        "ORIGINAL_SOURCE_REVIEW_20261021.md",
        "UNRESOLVED_SOURCE_LIMITS.json",
        "freeze_ziwei_life_second_four_aux_original.py",
        "test_chinese15src_original_auxiliaries.py",
        "build_chinese15src_portable_archive.py",
    ]]
    assert not DEST.exists(), "Existing owner archive: check prior receipt, do not overwrite"
    assert DEST.parent.is_dir()
    for rel in names:
        assert (ROOT / rel).is_file(), str(rel)
    checks = {p.as_posix(): {"sha256": sha((ROOT / p).read_bytes()),"bytes": (ROOT / p).stat().st_size} for p in names}
    manifest = {
        "schema": "CHINESE_V15_COLD_SOURCE_ZIP_MANIFEST_V1",
        "role": "Exact transmitted online Zi Wei source excerpts, not independently authenticated old printing or human predictions",
        "source_oldid": 1963110, "human_predictive_validations": 0,
        "runtime_astrology_promotions": 0, "source_file_checks": checks
    }
    readme = (
        "# Zi Wei original source V15 historical archive\n\n"
        "Entrypoint: tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-15SRC-Life/ORIGINAL_SOURCE_REVIEW_20261021.md\n\n"
        "After extraction at archive root, replay source checks with:\n"
        "python3 -m unittest discover -s tasks/astro-chinese-primary-sources-20261017/"
        "batches/ChineseAstro-15SRC-Life -p test_chinese15src_original_auxiliaries.py -v\n\n"
        "Read SOURCE_ARCHIVE_MANIFEST.json for byte hashes. "
        "Prior Chinese V14 and Western source snapshots are included only to verify no drift.\n"
        "No actual human predictive validations, old printed edition authenticity, "
        "or natal chart engine certification.\n"
    )
    with ZipFile(DEST, "w", compression=ZIP_DEFLATED, compresslevel=9) as zipf:
        for rel in names:
            zipf.write(ROOT / rel, arcname=rel.as_posix())
        zipf.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        zipf.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        assert z.testzip() is None, "Failed ZIP CRC"
        assert len(z.namelist()) == len(names) + 2
        for name,expected in checks.items():
            blob=z.read(name)
            assert sha(blob)==expected["sha256"] and len(blob)==expected["bytes"],name
    with tempfile.TemporaryDirectory(prefix="ziwei-v15-cold-source-") as scratch:
        out = Path(scratch) / "archive_root"
        out.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(out)
        for name, expected in checks.items():
            blob=(out / name).read_bytes()
            assert sha(blob)==expected["sha256"] and len(blob)==expected["bytes"]
        completed=subprocess.run([
            sys.executable,"-m","unittest","discover","-s",BATCH.as_posix(),
            "-p","test_chinese15src_original_auxiliaries.py","-v"
        ],cwd=out,capture_output=True,text=True)
        (B / "COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(
            completed.stdout + completed.stderr, encoding="utf-8")
        if completed.returncode:
            raise RuntimeError("Cold source tests failed: "+completed.stderr[-1800:])
        tests=completed.stderr.count(" ... ok")
        assert tests==13,(tests,completed.stderr)
    receipt = {
        "batch":"ChineseAstro-15SRC-Life","status":"COLD_ARCHIVE_SOURCE_13_TESTS_PASSED",
        "archive_path_on_owner_computer":str(DEST),
        "archive_filename":DEST.name,"archive_sha256":sha(DEST.read_bytes()),
        "archive_bytes":DEST.stat().st_size,"members":len(names)+2,
        "ZIP_CRC_verified":True,"each_member_hash_and_size_verified":True,
        "independent_cold_source_tests_executed":13,"independent_cold_source_tests_green":13,
        "original_chinese_online_source_revision":1963110,
        "ancient_Ming_original_imprint_authenticated":False,
        "real_human_blind_forecast_tests":0,"runtime_model_promotions":0
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
