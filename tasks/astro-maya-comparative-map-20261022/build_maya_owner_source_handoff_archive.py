#!/usr/bin/env python3
"""Copyright-safe owner book intake and next-chat handoff archive.

Only metadata, reading windows, tests, source-selection guidance and provenance.
No actual PDF/EPUB full text or historical manuscripts are included.
"""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json,os,subprocess,sys,tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
TASK=Path("tasks/astro-maya-comparative-map-20261022")
DEST=Path("/home/joel/Téléchargements/Astrology-Maya-Owner-Books-Verified-Handoff-20261022.zip")
FILES=[
 Path("tasks/astro-multitradition-source-coverage-20261022/BOOK_AND_MAYAN_COVERAGE_STATUS_20261022.md"),
]+[TASK/name for name in (
  "WORKING_CHECKPOINT_20261022.md",
  "WRITER_LEASE.json",
  "MAYA_LOCAL_SOURCE_INVENTORY_V1.json",
  "build_maya_source_inventory.py",
  "test_maya_source_intake.py",
  "MAYA_SOURCE_FIRST_READING_AND_PARALLEL_MAP_ALIGNMENT_20261022.md",
  "EXACT_BOOK_TITLES_TO_SEARCH_20261022.md",
  "CONTINUATION_HANDOFF_ACCEPTED_20261022.md",
  "build_maya_owner_source_handoff_archive.py",
)]

def sha(raw:bytes)->str:return sha256(raw).hexdigest()

def main():
 if DEST.exists():raise ValueError("Owner delivery exists: inspect, do not overwrite")
 if not DEST.parent.is_dir():raise ValueError("Owner Downloads directory absent")
 roster={}
 for rel in FILES:
  path=ROOT/rel
  if not path.is_file():raise ValueError("Source handoff companion missing "+str(rel))
  raw=path.read_bytes()
  roster[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
 manifest={
  "schema":"MAYA_OWNER_LOCAL_BOOKS_CROSS_TRADITION_HANDOFF_PACK_V1",
  "source_book_count":5,
  "relevant_owner_local_books":4,
  "fiction_book_excluded":1,
  "owner_original_PDF_EPUB_books_or_images_included":False,
  "owner_original_book_input_folder":"~/Documents/astrology, remains outside repository",
  "owner_local_book_checksum_inventory_SHA256":"2a4af2c69ba6c19935984c8a725bf3b23af5efa81ab803a1aaaaa8c80a13c089",
  "cross_tradition_map_already_in_other_isolated_branch":True,
  "existing_separate_cross_tradition_source_map_zip_verified":True,
  "preregistered_real_human_prediction_or_experiment_added":False,
  "actual_blinded_human_validations":0,
  "astrology_runtime_promotions":0,
  "file_sha256_and_sizes":roster,
 }
 readme=(
   "# Verified Maya books on owner's laptop + other title search / next-chat continuation\n\n"
   "Open tasks/astro-maya-comparative-map-20261022/"
   "CONTINUATION_HANDOFF_ACCEPTED_20261022.md first. "
   "Exact other-systems search titles are in EXACT_BOOK_TITLES_TO_SEARCH_20261022.md; "
   "MAYA_SOURCE_FIRST_READING_AND_PARALLEL_MAP_ALIGNMENT_20261022.md "
   "notes original page windows and existing sibling maps.\n\n"
   "This ZIP does NOT contain any copyrighted full book files or images. "
   "Owner originals remain under ~/Documents/astrology. "
   "It requires those files for the original exact-byte intake integrity tests.\n"
   "For cold replay from extracted root on that owner machine:\n"
   "python3 -m unittest discover -s tasks/astro-maya-comparative-map-20261022 "
   "-p test_maya_source_intake.py -v\n\n"
   "No actual Maya natal prediction accepted; no human validation.\n"
 )
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md",readme)
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
   raise ValueError("ZIP CRC/source handoff inventory wrong")
  for name,proof in roster.items():
   raw=z.read(name)
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("ZIP member source hash changed "+name)
 with tempfile.TemporaryDirectory(prefix="maya-actual-owner-intake-cold-") as t:
  out=Path(t)/"unpacked";out.mkdir()
  with ZipFile(DEST) as z:z.extractall(out)
  for name,proof in roster.items():
   raw=(out/name).read_bytes()
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Cold-extracted source SHA incorrect "+name)
  proc=subprocess.run([sys.executable,"-m","unittest","discover","-s",TASK.as_posix(),
                       "-p","test_maya_source_intake.py","-v"],
                      cwd=out,capture_output=True,text=True,env=os.environ.copy())
  log=proc.stdout+proc.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261022.txt").write_text(log,encoding="utf-8")
  if proc.returncode or proc.stderr.count(" ... ok")!=12 or "Ran 12 tests" not in proc.stderr:
   raise ValueError("Source intake cold regression not green: "+log[-2300:])
 receipt={"schema":"MAYA_OWNER_SOURCE_INTAKE_ARCHIVE_RELEASE_RECEIPT_V1",
  "status":"ALL_LOCAL_ORIGINAL_SHA_AND_12_COLD_SOURCE_TESTS_GREEN",
  "archive_path":str(DEST),"archive_bytes":DEST.stat().st_size,
  "archive_SHA256":sha(DEST.read_bytes()),
  "archive_members":len(FILES)+2,
  "source_member_hash_and_byte_sizes_verified":True,
  "ZIP_CRC_verified":True,
  "focused_source_tests_green":12,"independent_cold_source_tests_green":12,
  "full_copyrighted_original_books_included":False,
  "owner_local_4_relevant_books_plus_1_excluded_fiction":True,
  "cross_tradition_existing_map_reused_instead_of_overwritten":True,
  "Maya_classical_calendar_to_human_prediction_engine_accepted":False,
  "real_human_blind_predictive_validations":0,"runtime_astrology_promotions":0}
 (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261022.json").write_text(
     json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
