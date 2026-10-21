#!/usr/bin/env python3
"""Cold archive of pinned BaZi DTS22 source, no real-human claims."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,subprocess,sys,tempfile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=Path("tasks/astro-chinese-primary-sources-20261017")
REL=T/"batches/ChineseAstro-28SRC-BaZi-Truth"
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-Truth-4-Original-Notes-V28-20261021.zip")
FILES=[T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json",
 T/"batches/ChineseAstro-27SRC-BaZi-Clarity/BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json",
]+[REL/name for name in (
 "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
 "PINNED_DITIAN_SUI_22_SOURCE_MANIFEST_V1.json",
 "evidence/DiTianSui_22_oldid844372.wikitext",
 "BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json",
 "SOURCE_DTS22_4_EXACT_OFFSET_WITNESS_V1.json",
 "ACCEPTANCE.json","ORIGINAL_SOURCE_REVIEW_20261021.md",
 "UNRESOLVED_SOURCE_LIMITS.json","freeze_bazi22_source.py",
 "test_bazi28_original.py","build_bazi28_archive.py")]
def sha(b):return sha256(b).hexdigest()
def main():
 if DEST.exists():raise ValueError("Prior archive exists, inspect receipt and do not overwrite")
 members={}
 for rel in FILES:
  p=ROOT/rel
  if not p.is_file():raise ValueError("Missing original source archive member "+str(rel))
  x=p.read_bytes();members[rel.as_posix()]={"sha256":sha(x),"bytes":len(x)}
 man={"schema":"BAZI_DTS22_PINNED_ORIGINAL_ONLINE_WIKITEXT_ARCHIVE",
  "oldid":844372,"original_source_sha256":"50779be0d79b31711371bca6669a85c36110d4f5c25937d5e794c5c8c7515333",
  "source_verses":2,"full_commentaries":2,"records":4,"authentic_old_print":False,
  "real_human_blind_predictive_validations":0,"runtime_promotions":0,"file_witnesses":members}
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(man,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md","Original Di Tian Sui chapter22 source-only. "
     "Cold replay: python3 -m unittest discover -s "
     "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-28SRC-BaZi-Truth "
     "-p test_bazi28_original.py -v. No human predictive validation or printed-edition authority.\n")
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
   raise ValueError("Source archive ZIP CRC/member inventory mismatch")
  for name,proof in members.items():
   x=z.read(name)
   if (sha(x),len(x))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("ZIP member SHA/byte mismatch "+name)
 with tempfile.TemporaryDirectory(prefix="bazi-dts22-cold-") as temp:
  root=Path(temp)/"unpacked";root.mkdir()
  with ZipFile(DEST) as z:z.extractall(root)
  for name,proof in members.items():
   x=(root/name).read_bytes()
   if (sha(x),len(x))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Cold extracted source mismatch "+name)
  run=subprocess.run([sys.executable,"-m","unittest","discover","-s",REL.as_posix(),
   "-p","test_bazi28_original.py","-v"],cwd=root,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
  if run.returncode or run.stderr.count(" ... ok")!=9 or "Ran 9 tests" not in run.stderr:
   raise ValueError("Source cold replay 9/9 failed: "+log[-1900:])
 receipt={"batch":"ChineseAstro-28SRC-BaZi-Truth",
  "status":"ORIGINAL_SOURCE_ZIP_CRC_SHA_COLD_9_TESTS_PASS",
  "owner_archive_path":str(DEST),"archive_SHA256":sha(DEST.read_bytes()),
  "archive_bytes":DEST.stat().st_size,"archive_members":len(FILES)+2,
  "ZIP_CRC_verified":True,"every_member_SHA256_and_bytes_verified":True,
  "cold_extracted_source_tests_green":9,"original_ancient_print_verified":False,
  "real_human_blind_validations":0,"runtime_promotions":0}
 (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
