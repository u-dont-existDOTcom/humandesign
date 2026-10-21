#!/usr/bin/env python3
"""Cold-source ZIP and independent extracted original source tests for Chinese V20."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=Path("tasks/astro-chinese-primary-sources-20261017")
BATCH=TASK/"batches/ChineseAstro-20SRC-Wealth"
DEST=Path("/home/joel/Téléchargements/Astrology-ZiWei-Wealth-31-Original-Source-Notes-V20-20261021.zip")
FILES=[
    TASK/"CHINESE_SOURCE_AUDIT_INDEX_V19.json",
    TASK/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    TASK/"batches/ChineseAstro-19SRC-Children/ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json",
    Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
]+[BATCH/x for x in (
    "WORKING_CHECKPOINT_20261021.md",
    "SOURCE_1963110_WEALTH_EXACT_EXCERPT.txt",
    "ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json",
    "SOURCE_WEALTH_31_EXACT_OFFSET_WITNESS_V1.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_ziwei_wealth_original.py",
    "test_chinese20_original_wealth.py",
    "build_chinese20_portable_archive.py",
)]


def sha(b:bytes)->str:
    return sha256(b).hexdigest()


def main()->None:
    if DEST.exists():
        raise ValueError("Existing source archive: inspect/reconcile before overwriting")
    if not DEST.parent.is_dir():
        raise ValueError("Owner French Downloads dir unavailable")
    members={}
    for rel in FILES:
        path=ROOT/rel
        if not path.is_file():
            raise ValueError("Required original source/fixture missing: "+str(rel))
        b=path.read_bytes()
        members[rel.as_posix()]={"sha256":sha(b),"bytes":len(b)}
    manifest={
        "schema":"CHINESE_V20_WEALTH_COLD_ORIGINAL_SOURCE_ZIP_MANIFEST",
        "source_oldid":1963110,
        "original_full_Wikitext_SHA256":"1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        "role":"Exact Wikitext source history, not independently authenticated Ming printing or financial forecast",
        "human_predictions_validated":0,"runtime_promotions":0,
        "members":members,
    }
    readme=(
      "# Historical Zi Wei Wealth source V20\n\n"
      "Read tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-20SRC-Wealth/"
      "ORIGINAL_SOURCE_REVIEW_20261021.md first.\n"
      "From extracted root run: python3 -m unittest discover -s "
      "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-20SRC-Wealth "
      "-p test_chinese20_original_wealth.py -v\n"
      "This is old transmitted text, not calibrated person-level finance advice or "
      "independently confirmed ancient original book.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILES:
            z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
            raise ValueError("ZIP member integrity/CRC failed")
        for name,expected in members.items():
            b=z.read(name)
            if (sha(b),len(b))!=(expected["sha256"],expected["bytes"]):
                raise ValueError("Archive member bytes changed: "+name)
    with tempfile.TemporaryDirectory(prefix="ziwei-wealth-v20-cold-") as temp:
        root=Path(temp)/"archive_root"
        root.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(root)
        for path,meta in members.items():
            b=(root/path).read_bytes()
            if (sha(b),len(b))!=(meta["sha256"],meta["bytes"]):
                raise ValueError("Cold-extracted file hash/bytes mismatch: "+path)
        run=subprocess.run([sys.executable,"-m","unittest","discover",
            "-s",BATCH.as_posix(),"-p","test_chinese20_original_wealth.py","-v"],
            cwd=root,capture_output=True,text=True)
        full=run.stdout+run.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(full,encoding="utf-8")
        if run.returncode!=0 or run.stderr.count(" ... ok")!=11 or "Ran 11 tests" not in run.stderr:
            raise ValueError("Cold source integrity test failed: "+full[-1900:])
    receipt={
        "batch":"ChineseAstro-20SRC-Wealth",
        "status":"ZIP_CRC_SHA_EXTRACTED_11_SOURCE_TESTS_PASS",
        "archive_path_on_owner_computer":str(DEST),
        "archive_filename":DEST.name,
        "archive_sha256":sha(DEST.read_bytes()),
        "archive_bytes":DEST.stat().st_size,"archive_members":len(FILES)+2,
        "ZIP_CRC_verified":True,
        "all_member_SHA256_and_bytes_verified":True,
        "independent_cold_extracted_source_tests_green":11,
        "old_original_Ming_woodblock_authenticated":False,
        "actual_blind_real_human_predictions":0,"runtime_astrological_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
