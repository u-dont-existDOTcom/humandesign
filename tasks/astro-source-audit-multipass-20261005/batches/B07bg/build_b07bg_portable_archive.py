#!/usr/bin/env python3
"""Cold portable first/second edition original Honours source evidence ZIP."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED,ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
WEST=T/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME="Astrology-Lilly-Original-Honours-1647-1659-B07bg-20261020.zip"

def checksum(blob):return sha256(blob).hexdigest()

def run():
    parent=[
       WEST,CHINA,
       T/"batches/B07bf/ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json",
       T/"batches/B07bf/evidence/1647-original-folio760-IIIF.jpg",
       T/"batches/B07bf/evidence/1659-original-folio760-DjVu.jpg",
       T/"batches/B07bf/evidence/1647-original-folio761-IIIF.jpg",
       T/"batches/B07bf/evidence/1659-original-folio761-DjVu.jpg",
    ]
    local=[p for p in B.rglob("*") if p.is_file()
           and p.suffix.lower() in (".py",".json",".md",".jpg")
           and "__pycache__" not in str(p)
           and "recovery" not in str(p)
           and p.name not in (
               "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
               "CANONICAL_PREPARE_RECEIPT_20261020.json"
           )]
    allfiles=sorted(set(local+parent),key=lambda p:str(p.relative_to(ROOT)))
    manifest={}
    for p in allfiles:
        raw=p.read_bytes()
        manifest[str(p.relative_to(ROOT))]={"sha256":checksum(raw),"bytes":len(raw)}
    downloads=Path.home()/"Téléchargements"
    downloads.mkdir(parents=True,exist_ok=True)
    output=downloads/NAME
    with ZipFile(output,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in allfiles:z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(output) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(manifest):
            raise ValueError("Source ZIP member set/CRC changed")
        for name,evidence in manifest.items():
            raw=z.read(name)
            if checksum(raw)!=evidence["sha256"] or len(raw)!=evidence["bytes"]:
                raise ValueError("Source ZIP original byte/SHA mismatch")
    with tempfile.TemporaryDirectory(prefix="lilly_honours_cold_source_") as d:
        out=Path(d)
        with ZipFile(output) as z:z.extractall(out)
        tests=out/"tasks/astro-source-audit-multipass-20261005/batches/B07bg"
        cmd=["/usr/bin/python3","-m","unittest","discover",
             "-s",str(tests),"-p","test_b07bg_original_honours.py","-v"]
        r=subprocess.run(cmd,cwd=out,text=True,capture_output=True,timeout=35)
        log=r.stdout+r.stderr
        if r.returncode!=0 or "Ran 13 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1600:])
            raise ValueError("Cold extracted source test fixture 13/13 not green")
    receipt={
      "batch":"B07bg",
      "status":"COLD_PORTABLE_SOURCE_VERIFIED_NOT_YET_CANONICAL",
      "archive_filename":NAME,
      "archive_path_on_owner_machine":str(output),
      "archive_sha256":checksum(output.read_bytes()),
      "archive_size_bytes":output.stat().st_size,
      "member_count":len(manifest),
      "original_source_member_exact_sha_bytes":manifest,
      "zip_CRC_check_passed":True,
      "all_members_exact_SHA_and_bytes_check_passed":True,
      "independent_cold_source_tests_executed":13,
      "independent_cold_source_tests_green":13,
      "historical_1647_whole_PDF_binary_copied":False,
      "historical_1659_whole_DjVu_binary_copied":False,
      "genuine_human_predictive_accuracy_validated":0,
      "astrological_production_rules_promoted":0
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("HONOURS SOURCE ZIP",len(manifest),"members",
          output.stat().st_size,"bytes",receipt["archive_sha256"],
          "cold 13/13")
if __name__=="__main__":run()
