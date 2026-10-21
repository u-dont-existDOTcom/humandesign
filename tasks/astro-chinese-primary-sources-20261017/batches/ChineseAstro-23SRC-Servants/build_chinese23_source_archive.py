#!/usr/bin/env python3
"""Portable original Wikitext Servants source and cold-extracted tests."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,subprocess,sys,tempfile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=Path("tasks/astro-chinese-primary-sources-20261017")
REL=T/"batches/ChineseAstro-23SRC-Servants"
DEST=Path("/home/joel/Téléchargements/Astrology-ZiWei-Servants-26-Original-Sources-V23-20261021.zip")
INPUTS=[
 T/"CHINESE_SOURCE_AUDIT_INDEX_V22.json",
 T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
 T/"batches/ChineseAstro-22SRC-Travel/ZIWEI_TRAVEL_26_SOURCE_NOTES_V1.json",
 Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
]+[REL/x for x in (
 "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
 "SOURCE_1963110_SERVANTS_EXACT_EXCERPT.txt",
 "ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json",
 "SOURCE_SERVANTS_26_OFFSET_WITNESS_V1.json",
 "ACCEPTANCE.json","ORIGINAL_SOURCE_REVIEW_20261021.md",
 "UNRESOLVED_SOURCE_LIMITS.json","freeze_servants_wikitext.py",
 "test_chinese23_original_servants.py","build_chinese23_source_archive.py"
)]
def sha(b):return sha256(b).hexdigest()
def main():
 if DEST.exists():raise ValueError("Existing archive: inspect before overwrite")
 members={}
 for rel in INPUTS:
  p=ROOT/rel
  if not p.is_file():raise ValueError("Missing source archive member "+str(rel))
  data=p.read_bytes()
  members[rel.as_posix()]={"sha256":sha(data),"bytes":len(data)}
 manifest={"schema":"ZIWEI_V23_SERVANTS_EXACT_WIKITEXT_COLD_ARCHIVE",
  "source_oldid":1963110,"Ming_printing_authentic":False,
  "human_predictions_validated":0,"runtime_promotions":0,"members":members}
 readme=("# Original historical Zi Wei Servants V23 source\n"
  "Archive includes Wikitext original and test_chinese23_original_servants.py.\n"
  "No real-person predictive validations, employment or interpersonal-safety advice.\n")
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for p in INPUTS:z.write(ROOT/p,arcname=p.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md",readme)
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(INPUTS)+2:
   raise ValueError("Original ZIP CRC/member mismatch")
  for name,proof in members.items():
   blob=z.read(name)
   if (sha(blob),len(blob))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("ZIP source member mismatch "+name)
 with tempfile.TemporaryDirectory(prefix="ziwei-v23-servants-cold-") as temp:
  root=Path(temp)/"unpacked"
  root.mkdir()
  with ZipFile(DEST) as z:z.extractall(root)
  for name,proof in members.items():
   blob=(root/name).read_bytes()
   if (sha(blob),len(blob))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Cold member changed "+name)
  run=subprocess.run([sys.executable,"-m","unittest","discover","-s",REL.as_posix(),
   "-p","test_chinese23_original_servants.py","-v"],cwd=root,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
  if run.returncode or run.stderr.count(" ... ok")!=7 or "Ran 7 tests" not in run.stderr:
   raise ValueError("Independent extracted source tests failed "+log[-2000:])
 receipt={"batch":"ChineseAstro-23SRC-Servants",
  "status":"ZIP_CRC_SHA_AND_COLD_7_SOURCE_TESTS_GREEN",
  "local_archive_path":str(DEST),"archive_filename":DEST.name,
  "archive_SHA256":sha(DEST.read_bytes()),"archive_bytes":DEST.stat().st_size,
  "archive_members":len(INPUTS)+2,"ZIP_CRC_verified":True,
  "all_members_SHA256_bytes_verified":True,"cold_extracted_source_tests_green":7,
  "ancient_print_original_authenticated":False,
  "human_blind_forecast_validation_count":0,"runtime_promotions":0}
 (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps(receipt,indent=2))
if __name__=="__main__":main()
