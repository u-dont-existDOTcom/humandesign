#!/usr/bin/env python3
"""Cold-extractable V27 original-source archive; source integrity is not human validity."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, ZIP_DEFLATED
import json, subprocess, sys, tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=Path("tasks/astro-chinese-primary-sources-20261017")
REL=TASK/"batches/ChineseAstro-27SRC-BaZi-Clarity"
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-Clarity-4-Original-Notes-V27-20261021.zip")
INPUTS=[TASK/"CHINESE_SOURCE_AUDIT_INDEX_V26.json",
        TASK/"batches/ChineseAstro-26SRC-BaZi-Obstruction/BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"]+[
        REL/name for name in (
         "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
         "PINNED_DITIAN_SUI_21_SOURCE_MANIFEST_V1.json",
         "evidence/DiTianSui_21_oldid844371.wikitext",
         "BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json",
         "SOURCE_DTS21_4_EXACT_OFFSET_WITNESS_V1.json",
         "ACCEPTANCE.json","ORIGINAL_SOURCE_REVIEW_20261021.md",
         "UNRESOLVED_SOURCE_LIMITS.json","DTS21_TRANSMISSION_VARIANTS_20261021.md",
         "freeze_bazi21_source.py","test_bazi27_original.py",
         "build_bazi27_archive.py",
         "PYTHON_INDEPENDENT_SOURCE_RECEIPT_20261021.json"
        )]
def sha(b):return sha256(b).hexdigest()
def main():
    if DEST.exists():
        raise ValueError("Archive already exists; inspect prior release receipt rather than overwrite")
    checks={}
    for rel in INPUTS:
        p=ROOT/rel
        if not p.is_file():raise ValueError("Missing original source archive member "+str(rel))
        raw=p.read_bytes()
        checks[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
    manifest={"schema":"BAZI_DTS21_PINNED_ONLINE_SOURCE_COLD_ARCHIVE_V1",
              "original_Wikitext_oldid":844371,
              "original_raw_SHA256":"9ff7673e7a7a8af1cace52457d801d631ca117f5923e8e3433f7b1d05729be0f",
              "original_verses":2,"complete_commentary_paragraphs":2,
              "source_note_count":4,"early_print_authenticated":False,
              "human_predictive_validations":0,"runtime_promotions":0,
              "source_file_checks":checks}
    readme=("Di Tian Sui section21 清濁論 historical Wikitext source V27. "
            "Original oldid844371 is not authenticated Ming print. "
            "From extracted root run: python3 -m unittest discover -s "
            "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-27SRC-BaZi-Clarity "
            "-p test_bazi27_original.py -v. These tests check original source fidelity only.\n")
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in INPUTS:z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(INPUTS)+2:
            raise ValueError("ZIP member count / CRC source check failed")
        for name,proof in checks.items():
            content=z.read(name)
            if (sha(content),len(content))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Archived member differs from source: "+name)
    with tempfile.TemporaryDirectory(prefix="bazi-dts21-cold-") as tmp:
        out=Path(tmp)/"archive";out.mkdir()
        with ZipFile(DEST) as z:z.extractall(out)
        for name,proof in checks.items():
            content=(out/name).read_bytes()
            if (sha(content),len(content))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Cold-extracted member changed: "+name)
        result=subprocess.run([sys.executable,"-m","unittest","discover",
            "-s",REL.as_posix(),"-p","test_bazi27_original.py","-v"],
            cwd=out,capture_output=True,text=True)
        log=result.stdout+result.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if result.returncode or result.stderr.count(" ... ok")!=10 or "Ran 10 tests" not in result.stderr:
            raise ValueError("Cold source suite did not pass 10/10: "+log[-1700:])
    receipt={"batch":"ChineseAstro-27SRC-BaZi-Clarity",
             "status":"SOURCE_ZIP_SHA_CRC_10_INDEPENDENT_COLD_TESTS_GREEN",
             "archive_path":str(DEST),"archive_SHA256":sha(DEST.read_bytes()),
             "archive_bytes":DEST.stat().st_size,
             "archive_members":len(INPUTS)+2,
             "ZIP_CRC_verified":True,
             "all_members_SHA256_and_bytes_verified":True,
             "independent_cold_source_tests_green":10,
             "ancient_print_authenticated":False,
             "independent_real_human_blind_forecasts":0,"runtime_promotions":0}
    (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
