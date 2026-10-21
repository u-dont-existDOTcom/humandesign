#!/usr/bin/env python3
"""Cold extractable exact BaZi Di Tian Sui section20 original-source ZIP."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,subprocess,sys,tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=Path("tasks/astro-chinese-primary-sources-20261017")
REL=T/"batches/ChineseAstro-26SRC-BaZi-Obstruction"
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-Connection-2-Original-Notes-V26-20261021.zip")
INPUTS=[
 T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json",
 T/"batches/ChineseAstro-25SRC-BaZi-SourceFlow/BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json",
]+[REL/name for name in (
 "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
 "PINNED_DITIAN_SUI_20_SOURCE_MANIFEST_V1.json",
 "evidence/DiTianSui_20_oldid844370.wikitext",
 "BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json",
 "SOURCE_DTS20_2_EXACT_OFFSET_WITNESS_V1.json","ACCEPTANCE.json",
 "ORIGINAL_SOURCE_REVIEW_20261021.md","UNRESOLVED_SOURCE_LIMITS.json",
 "freeze_bazi20_source.py","test_bazi26_original.py","build_bazi26_archive.py"
)]
def sha(b):return sha256(b).hexdigest()
def main():
 if DEST.exists():raise ValueError("Existing source archive: inspect before overwrite")
 if not DEST.parent.is_dir():raise ValueError("Owner Downloads path missing")
 witnesses={}
 for rel in INPUTS:
  p=ROOT/rel
  if not p.is_file():raise ValueError("Missing source fixture "+str(rel))
  raw=p.read_bytes()
  witnesses[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
 manifest={"schema":"BAZI_DI_TIAN_SUI_20_COLD_SOURCE_ARCHIVE",
  "original_source_oldid":844370,
  "original_source_sha256":"f646b66d51d6cd69a376e2b4e754c0b872ccbe24879772954579e03ae3639022",
  "verse":1,"complete_commentary_paragraph":1,"records":2,
  "ancient_original_printing_authenticated":False,
  "blinded_human_predictive_validations":0,"runtime_promotions":0,
  "original_member_SHA256_and_size":witnesses}
 readme=("# Di Tian Sui 20 (Connection/Obstruction) source-only archive\n"
   "Do not treat historical symbolic bridging commentary as human outcomes.\n"
   "Run from extracted archive root: python3 -m unittest discover -s "
   "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-26SRC-BaZi-Obstruction "
   "-p test_bazi26_original.py -v\n")
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for rel in INPUTS:z.write(ROOT/rel,arcname=rel.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md",readme)
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(INPUTS)+2:
   raise ValueError("Original source ZIP invalid CRC/inventory")
  for name,w in witnesses.items():
   blob=z.read(name)
   if (sha(blob),len(blob))!=(w["sha256"],w["bytes"]):
    raise ValueError("Source archive member bytes changed "+name)
 with tempfile.TemporaryDirectory(prefix="bazi-dts20-cold-") as tmp:
  output=Path(tmp)/"replay";output.mkdir()
  with ZipFile(DEST) as z:z.extractall(output)
  for name,w in witnesses.items():
   blob=(output/name).read_bytes()
   if (sha(blob),len(blob))!=(w["sha256"],w["bytes"]):
    raise ValueError("Cold-extracted raw source differs "+name)
  run=subprocess.run([sys.executable,"-m","unittest","discover","-s",REL.as_posix(),
   "-p","test_bazi26_original.py","-v"],cwd=output,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
  if run.returncode or run.stderr.count(" ... ok")!=8 or "Ran 8 tests" not in run.stderr:
   raise ValueError("Cold re-extraction original source tests failed "+log[-1600:])
 receipt={"batch":"ChineseAstro-26SRC-BaZi-Obstruction","status":"CRC_SHA_AND_8_COLD_SOURCE_TESTS_GREEN",
  "archive_path":str(DEST),"filename":DEST.name,
  "archive_sha256":sha(DEST.read_bytes()),"archive_bytes":DEST.stat().st_size,
  "archive_members":len(INPUTS)+2,"ZIP_CRC_verified":True,"all_members_sha256_size_verified":True,
  "independent_cold_source_test_count":8,
  "original_ancient_print_authenticated":False,
  "independently_blinded_human_predictions":0,"runtime_astrological_promotions":0}
 (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
