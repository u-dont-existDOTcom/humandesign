#!/usr/bin/env python3
"""Independent cold ZIP archive for source-only original first four auxiliary stars."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
ORIGINAL=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS=T/"batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME="Astrology-ZiWei-Life-Auxiliary-First-Four-58-Original-Sources-V14-20261020.zip"
def checksum(b):return sha256(b).hexdigest()
def run():
    required=[OLD,ORIGINAL,PREVIOUS,WEST]
    local=[p for p in B.rglob("*") if p.is_file() and p.suffix.lower() in (".txt",".md",".json",".py")
           and "__pycache__" not in str(p) and "recovery" not in str(p) and p.name not in
           ("CANONICAL_PREPARE_RECEIPT_20261020.json",
            "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")]
    files=sorted(set(required+local),key=lambda p:str(p.relative_to(ROOT)))
    manifest={}
    for p in files:
        data=p.read_bytes()
        manifest[str(p.relative_to(ROOT))]={"sha256":checksum(data),"bytes":len(data)}
    dest=Path.home()/"Téléchargements"
    dest.mkdir(parents=True,exist_ok=True)
    file=dest/NAME
    with ZipFile(file,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in files:z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(file) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(manifest):
            raise ValueError("Original source ZIP corrupted or incorrect members")
        for name,item in manifest.items():
            data=z.read(name)
            if checksum(data)!=item["sha256"] or len(data)!=item["bytes"]:
                raise ValueError("Original source ZIP member checksum/length mismatch")
    with tempfile.TemporaryDirectory(prefix="ZiWei_original_V14_cold_") as d:
        unpack=Path(d)
        with ZipFile(file) as z:z.extractall(unpack)
        suite=unpack/"tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-14SRC-Life"
        cmd=["/usr/bin/python3","-m","unittest","discover",
             "-s",str(suite),"-p","test_chinese14src_original_auxiliaries.py","-v"]
        r=subprocess.run(cmd,cwd=unpack,capture_output=True,text=True,timeout=45)
        log=r.stdout+r.stderr
        if r.returncode or "Ran 13 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1600:])
            raise ValueError("Original Chinese auxiliary source 13/13 cold replay failed")
    release={
       "batch":"ChineseAstro-14SRC-Life",
       "status":"PORTABLE_SOURCE_EVIDENCE_VERIFIED_NOT_CANONICAL_YET",
       "original_Wikitext_oldid":1963110,
       "filename":NAME,
       "archive_path_on_owner_computer":str(file),
       "archive_sha256":checksum(file.read_bytes()),
       "archive_bytes":file.stat().st_size,
       "ZIP_member_count":len(manifest),
       "source_member_SHA256_and_bytes":manifest,
       "ZIP_CRC_verified":True,
       "each_member_hash_and_size_verified":True,
       "independent_cold_source_tests_executed":13,
       "independent_cold_source_tests_green":13,
       "new_source_documentary_records":58,
       "historical_original_Ming_imprint_authenticated":False,
       "actual_human_predictive_validations":0,
       "runtime_production_rules":0
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(release,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"ZIP":str(file),"bytes":file.stat().st_size,
          "SHA256":release["archive_sha256"],"files":len(manifest),
          "cold_source_tests":13},ensure_ascii=False,indent=2))
if __name__=="__main__":run()
