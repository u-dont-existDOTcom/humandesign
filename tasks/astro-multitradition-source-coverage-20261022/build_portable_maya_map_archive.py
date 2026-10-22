#!/usr/bin/env python3
"""Portable, source-linked Maya book shortlist and multi-astrology map.

Includes only own research prose/metadata, small normative repo companion files
and tests. No copyrighted books, original codex images, private data or vendor
font files are bundled. Independent cold extraction reruns source-map checks.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
TASK=Path("tasks/astro-multitradition-source-coverage-20261022")
DEST=Path("/home/joel/Téléchargements/Astrology-Maya-Books-CrossTradition-Map-20261022.zip")
FILES=[
 Path("ARCHITECTURE.md"),
 Path("reference/core/MAPPING_V2_EVIDENCE_PROTOCOL.md"),
 Path("reference/core/survey_v2_behavioral_domains.json"),
 Path("reference/core/survey_v2_field_dependency_map_v1_0_0.json"),
 Path("docs/20_forward_blind_prospective_validation.md"),
]+[TASK/name for name in (
 "BOOK_AND_MAYAN_COVERAGE_STATUS_20261022.md",
 "WORKING_CHECKPOINT_20261022.md",
 "WRITER_LEASE.json",
 "INDEX.md",
 "MAYA_BOOKS_OTHER_SYSTEMS_AND_METHOD_20261022.md",
 "MAYA_RANKED_SOURCE_REGISTER_V1.json",
 "ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json",
 "TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json",
 "MULTITRADITION_SOURCE_TO_TEST_MAP.md",
 "build_astro_source_map_registers.py",
 "build_tradition_survey_crosswalk.py",
 "test_multitradition_source_map.py",
 "build_portable_maya_map_archive.py",
)]
def sha(b):return sha256(b).hexdigest()

def main():
 if DEST.exists():
  raise ValueError("Owner's Maya source map ZIP already exists; inspect prior evidence before overwriting")
 if not DEST.parent.is_dir():
  raise ValueError("Owner's exact Downloads directory not available")
 manifest_members={}
 for rel in FILES:
  p=ROOT/rel
  if not p.is_file():raise ValueError("Expected source map companion missing: "+str(rel))
  raw=p.read_bytes()
  manifest_members[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
 manifest={
  "schema":"HUMANDESIGN_MAYA_SOURCE_AND_MULTITRADITION_MAP_ARCHIVE_V1",
  "purpose":"Original source-book ranking + typed research map, NOT original book text or behavior/astrology validation",
  "previous_book_status_audit_SHA256":"dcdeffc1f5f76cbb12b3851b205404f40ed7249b197a8f89c882b74545d1c105",
  "maya_source_leads":15,"other_tradition_classes":7,
  "existing_HD_only_behavior_domains":6,"unmapped_non_HD_claim_classes":14,
  "source_original_codex_folios_ingested":0,
  "cross_tradition_software_scoring_activated":False,
  "source_to_human_blind_predictive_validations":0,
  "copyrighted_full_books_and_codex_facsimiles_included":False,
  "source_member_provenance":manifest_members,
 }
 readme=(
  "# Astrology books and cross-tradition source-to-test map, 2026-10-22\n\n"
  "Open tasks/astro-multitradition-source-coverage-20261022/INDEX.md first.\n"
  "The ranked Maya study + other traditions report and Mermaid maps are in the "
  "same directory. No books, Maya glyph originals or vendor materials were "
  "downloaded or placed in this ZIP; catalog URLs may require library access.\n"
  "To run independent no-dependency structural checks after extraction:\n"
  "python3 -m unittest discover -s tasks/astro-multitradition-source-coverage-20261022 "
  "-p test_multitradition_source_map.py -v\n"
  "These validate source-register integrity only; no real people were tested.\n"
 )
 with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
  for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
  z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  z.writestr("README_READ_ME_FIRST.md",readme)
 with ZipFile(DEST) as z:
  if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
   raise ValueError("ZIP CRC or expected archive inventory failed")
  for name,proof in manifest_members.items():
   raw=z.read(name)
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Source/map artifact changed in zip "+name)
 with tempfile.TemporaryDirectory(prefix="maya-source-map-cold-") as tmp:
  cold=Path(tmp)/"unpacked";cold.mkdir()
  with ZipFile(DEST) as z:z.extractall(cold)
  for name,proof in manifest_members.items():
   raw=(cold/name).read_bytes()
   if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
    raise ValueError("Cold-extracted source-map artifact changed "+name)
  run=subprocess.run([sys.executable,"-m","unittest","discover",
   "-s",TASK.as_posix(),"-p","test_multitradition_source_map.py","-v"],
   cwd=cold,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (B/"COLD_ARCHIVE_TEST_LOG_20261022.txt").write_text(log,encoding="utf-8")
  if run.returncode or run.stderr.count(" ... ok")!=15 or "Ran 15 tests" not in run.stderr:
   raise ValueError("Cold source-map tests must pass 15/15: "+log[-2200:])
 receipt={
  "schema":"MAYA_BOOKS_AND_MULTITRADITION_MAP_COLD_EVIDENCE_RECEIPT_V1",
  "status":"ORIGINAL_MAP_AND_MANIFEST_ZIP_SHA_CRC_COLD_15_TESTS_GREEN",
  "owner_local_archive_path":str(DEST),
  "archive_sha256":sha(DEST.read_bytes()),
  "archive_bytes":DEST.stat().st_size,
  "archive_members":len(FILES)+2,
  "all_original_source_member_SHA256_and_sizes_verified":True,
  "ZIP_CRC_verified":True,
  "source_integrity_tests_green":15,
  "independent_cold_extraction_source_tests_green":15,
  "maya_source_leads":15,"other_traditions":7,
  "human_design_specific_survey_domains_reused_as_evidence_design_only":6,
  "source_to_observable_provisional_non_HD_constructs":14,
  "books_fully_read_during_task":0,
  "original_maya_codex_divination_rules_validated":0,
  "real_human_blinded_predictive_validations":0,
  "runtime_astrology_promotions":0
 }
 (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261022.json").write_text(
  json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
 main()
