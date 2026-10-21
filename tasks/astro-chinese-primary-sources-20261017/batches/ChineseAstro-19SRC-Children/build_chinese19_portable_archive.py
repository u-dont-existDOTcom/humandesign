#!/usr/bin/env python3
"""Build independent cold-extractable V19 source evidence package and verify it."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=Path("tasks/astro-chinese-primary-sources-20261017")
BATCH=TASK/"batches/ChineseAstro-19SRC-Children"
DEST=Path("/home/joel/Téléchargements/Astrology-ZiWei-Children-34-Original-Source-Notes-V19-20261021.zip")
FILES=[
    TASK/"CHINESE_SOURCE_AUDIT_INDEX_V18.json",
    TASK/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    TASK/"batches/ChineseAstro-18SRC-Spouses/ZIWEI_SPOUSES_25_SOURCE_NOTES_V1.json",
    Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
]+[BATCH/x for x in (
    "WORKING_CHECKPOINT_20261021.md",
    "SOURCE_1963110_CHILDREN_EXACT_EXCERPT.txt",
    "ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json",
    "SOURCE_CHILDREN_34_EXACT_OFFSET_WITNESS_V1.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_ziwei_children_original.py",
    "test_chinese19_original_children.py",
    "build_chinese19_portable_archive.py",
)]


def sha(raw:bytes)->str:
    return sha256(raw).hexdigest()


def main():
    if DEST.exists():
        raise ValueError(f"Archive already exists, reconcile prior receipt before rewriting: {DEST}")
    if not DEST.parent.is_dir():
        raise ValueError("French owner Downloads directory does not exist")
    checks={}
    for rel in FILES:
        p=ROOT/rel
        if not p.is_file():
            raise ValueError(f"Missing intended archive member: {rel}")
        raw=p.read_bytes()
        checks[rel.as_posix()]={"sha256":sha(raw),"size_bytes":len(raw)}
    manifest={
        "schema":"ZIWEI_V19_COLD_SOURCE_ARCHIVE_MEMBER_MANIFEST",
        "source_oldid":1963110,
        "original_source_raw_SHA256":"1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        "role":"source-only historical Wikitext records; not a critical original book or humans",
        "human_predictive_validations":0,"runtime_promotions":0,
        "members":checks
    }
    entry=(
        "# Historical Zi Wei V19 Children original source evidence\n\n"
        "Entrypoint: tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-19SRC-Children/ORIGINAL_SOURCE_REVIEW_20261021.md\n\n"
        "To replay from extracted ZIP root:\n"
        "python3 -m unittest discover -s tasks/astro-chinese-primary-sources-20261017/"
        "batches/ChineseAstro-19SRC-Children -p test_chinese19_original_children.py -v\n\n"
        "Source is a transmitted online 1963110 Wikitext original wording, "
        "not authenticated historical Ming original, validated human predictions, "
        "or medical/family/child-rearing advice.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILES:
            z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",entry)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
            raise ValueError("Archive CRC or member count mismatch")
        for name,expected in checks.items():
            raw=z.read(name)
            if sha(raw)!=expected["sha256"] or len(raw)!=expected["size_bytes"]:
                raise ValueError("Incorrect zip SHA or byte length: "+name)
    with tempfile.TemporaryDirectory(prefix="ziwei-v19-original-cold-") as scratch:
        unpack=Path(scratch)/"archive_root"
        unpack.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(unpack)
        for rel,x in checks.items():
            blob=(unpack/rel).read_bytes()
            if sha(blob)!=x["sha256"] or len(blob)!=x["size_bytes"]:
                raise ValueError("Cold-extracted SHA/bytes mismatch")
        test=subprocess.run([
            sys.executable,"-m","unittest","discover",
            "-s",BATCH.as_posix(),
            "-p","test_chinese19_original_children.py","-v"
        ],cwd=unpack,capture_output=True,text=True)
        log=test.stdout+test.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if test.returncode!=0:
            raise ValueError("Extracted source tests failed: "+log[-1800:])
        passed=test.stderr.count(" ... ok")
        if passed!=13 or "Ran 13 tests" not in test.stderr:
            raise ValueError(f"Unexpected cold test count: {passed}")
    receipt={
        "batch":"ChineseAstro-19SRC-Children",
        "status":"PORTABLE_ARCHIVE_CRC_SHA_MEMBER_AND_COLD_13_TEST_PASS",
        "local_archive_path":str(DEST),"archive_filename":DEST.name,
        "archive_sha256":sha(DEST.read_bytes()),"archive_bytes":DEST.stat().st_size,
        "archived_member_count":len(FILES)+2,
        "ZIP_CRC_verified":True,"all_members_SHA256_and_bytes_verified":True,
        "cold_extracted_member_checks_complete":True,
        "independent_cold_source_tests_green":13,
        "source_original_Ming_woodblock_authenticated":False,
        "actual_real_human_predictive_validations":0,"runtime_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
