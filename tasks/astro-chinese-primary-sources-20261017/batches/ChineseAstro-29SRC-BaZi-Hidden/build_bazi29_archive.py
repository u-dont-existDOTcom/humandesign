#!/usr/bin/env python3
"""Portable original Di Tian Sui23 Wikitext source and independent cold replay."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, ZIP_DEFLATED
import json,subprocess,sys,tempfile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=Path("tasks/astro-chinese-primary-sources-20261017")
REL=T/"batches/ChineseAstro-29SRC-BaZi-Hidden"
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-Hidden-2-Original-Notes-V29-20261021.zip")
FILES=[T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json",
 T/"batches/ChineseAstro-28SRC-BaZi-Truth/BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json",
]+[REL/name for name in (
 "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
 "PINNED_DITIAN_SUI_23_SOURCE_MANIFEST_V1.json",
 "evidence/DiTianSui_23_oldid844373.wikitext",
 "BAZI_DITIAN_SUI_23_2_SOURCE_NOTES_V1.json",
 "SOURCE_DTS23_2_EXACT_OFFSET_WITNESS_V1.json","ACCEPTANCE.json",
 "ORIGINAL_SOURCE_REVIEW_20261021.md","UNRESOLVED_SOURCE_LIMITS.json",
 "freeze_bazi23_source.py","test_bazi29_original.py","build_bazi29_archive.py"
)]
def sha(b):return sha256(b).hexdigest()
def main():
 if DEST.exists():raise ValueError("Owner archive exists, inspect prior receipt before overwriting")
 w={}
 for rel in FILES:
  p=ROOT/rel
  if not p.is_file():raise ValueError("Expected source archive member missing "+str(rel))
  raw=p.read_bytes();w[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
 manifest={"schema":"BAZI_DTS23_HIDDEN_VISIBLE_ORIGINAL_ONLINE_SOURCE_ARCHIVE",
  "original_oldid":844373,"source_sha256":"a883ddf8509bda86e3ecadcb9a8d1bfdf7b6cc8901fe20044c64f3b730e54ac1",
  "historical_source_verse_count":1,"complete_commentary_paragraph_count":1,
  "source_only_annotations":2,"original_printing_authenticated":False,
  "human_blind_predictions_validated":0,"runtime_promotions":0,
  "file_witnesses":w}
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md","Historic Di Tian Sui chapter23 source only. "
  "Cold replay: python3 -m unittest discover -s "
  "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-29SRC-BaZi-Hidden "
  "-p test_bazi29_original.py -v. No human prediction validation.\n")
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
   raise ValueError("Original source ZIP CRC/member inventory mismatch")
  for name,proof in w.items():
   raw=z.read(name)
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Archived source member SHA/size mismatch "+name)
 with tempfile.TemporaryDirectory(prefix="bazi-dts23-cold-") as tmp:
  root=Path(tmp)/"replay";root.mkdir()
  with ZipFile(DEST) as z:z.extractall(root)
  for name,proof in w.items():
   raw=(root/name).read_bytes()
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Cold original source member hash differs "+name)
  proc=subprocess.run([sys.executable,"-m","unittest","discover","-s",REL.as_posix(),
   "-p","test_bazi29_original.py","-v"],cwd=root,capture_output=True,text=True)
  log=proc.stdout+proc.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
  if proc.returncode or proc.stderr.count(" ... ok")!=9 or "Ran 9 tests" not in proc.stderr:
   raise ValueError("Independent original source tests failed "+log[-1600:])
 receipt={"batch":"ChineseAstro-29SRC-BaZi-Hidden",
  "status":"SOURCE_ZIP_CRC_SHA_AND_COLD_NINE_TESTS_PASSED",
  "owner_archive_path":str(DEST),"archive_SHA256":sha(DEST.read_bytes()),
  "archive_bytes":DEST.stat().st_size,"archive_members":len(FILES)+2,
  "ZIP_CRC_verified":True,"every_member_sha_size_verified":True,
  "independent_cold_source_tests_green":9,"historical_original_print_authenticated":False,
  "human_blind_predictive_validations":0,"runtime_promotions":0}
 (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
