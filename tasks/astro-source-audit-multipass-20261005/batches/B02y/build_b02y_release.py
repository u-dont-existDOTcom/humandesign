#!/usr/bin/env python3
"""Make reproducible original-image documentary archive and verify extracted tests."""
import hashlib,json,pathlib,subprocess,tempfile,zipfile
B=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path.home()/'Téléchargements'/'Astrology-Lilly-Chapter-LIII-Documentary-20261015.zip'
H=lambda data:hashlib.sha256(data).hexdigest()
CORE=[
 'build_b02y_source_first.py','test_b02y_source_first.py',
 'freeze_b02y_documentary_source.py','test_b02y_documentary_admission.py',
 'build_b02y_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'CLAIM_LEDGER.json','UNRESOLVED_SOURCE_LIMITS.json',
 'LIII_SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
]+[f'evidence/pdf_1647-{n}.jpg' for n in range(405,411)]
for rel in CORE:
 assert (B/rel).is_file(),rel
hashes={rel:{"sha256":H((B/rel).read_bytes()),"bytes":(B/rel).stat().st_size} for rel in CORE}
data={"kind":"B02y_DOCUMENTARY_LOCAL_RELEASE_NOT_EMPIRICAL_VALIDATION",
      "source":"William Lilly Christian Astrology 1647 Wellcome b30338724",
      "body_pdf_pages":list(range(405,411)),
      "source_claim_rows":76,"source_spans":27,
      "local_historical_admission":True,"global_publication_pending":True,
      "empirical_predictions_validated":0,"new_runtime_rules":0,
      "files":hashes}
manifest=(json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode()
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for rel in sorted(CORE):z.write(B/rel,arcname='B02y/'+rel)
 z.writestr('B02y/RELEASE_SHA256_MANIFEST.json',manifest)
with zipfile.ZipFile(OUT,'r') as z, tempfile.TemporaryDirectory(prefix='lilly-b02y-replay-') as temp:
 assert z.testzip() is None
 z.extractall(temp)
 E=pathlib.Path(temp)/'B02y'
 chk=json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_bytes())
 assert chk==data
 for rel,info in hashes.items():
  body=(E/rel).read_bytes()
  assert H(body)==info['sha256'] and len(body)==info['bytes'],rel
 proc=subprocess.run(['python3','-m','unittest','-v',
                       'test_b02y_source_first','test_b02y_documentary_admission'],
                      cwd=E,capture_output=True,text=True)
 print(proc.stderr[-2200:])
 assert proc.returncode==0 and 'Ran 19 tests' in proc.stderr
receipt={"batch":"B02y","status":"LOCAL_DOCUMENTARY_RELEASE_ARCHIVED_AND_REPLAY_VERIFIED",
 "archive_os_downloads":str(OUT),"archive_sha256":H(OUT.read_bytes()),
 "archive_bytes":OUT.stat().st_size,"zip_integrity_pass":True,
 "extracted_all_file_sha256_pass":True,"extracted_focused_source_test_count":19,
 "extracted_source_tests_exit_code":proc.returncode,
 "source_first_rules_sha256":hashes['RULES.json']['sha256'],
 "new_historical_documentary_units_if_published":76,
 "empirical_predictions_validated":0,"runtime_promotions":0,
 "canonical_published":False}
(B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
