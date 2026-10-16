from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXXVIII-Printed-LXXXVII-Hopes-Documentary-20261016.zip'
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[p for p in B.iterdir() if p.is_file() and p.suffix in ('.json','.py','.md') and p.name not in ('SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json','PUBLICATION_RECEIPT_20261016.json','CONTINUATION_HANDOFF_THROUGH_LXXXVIII_20261016.md')]
files.extend([B/'evidence'/f'pdf_1647-{n}.jpg' for n in (491,492,493)])
assert all(p.is_file() for p in files)
members={str(p.relative_to(B)):{'bytes':p.stat().st_size,'sha256':H(p)} for p in files}
meta={'batch':'B04h','historical_source_annotations':48,'original_printed':'LXXXVII','editorial_sequence':'LXXXVIII','independent_validations':0,'members':members}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in files:z.write(p,'B04h/'+str(p.relative_to(B)))
 z.writestr('B04h/RELEASE_SHA256_MANIFEST.json',json.dumps(meta,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b04h-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/'B04h'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==meta
 for n,v in members.items():
  assert H(E/n)==v['sha256'] and (E/n).stat().st_size==v['bytes']
 t=subprocess.run(['python3','-m','unittest','-q','test_b04h_source_first','test_b04h_documentary_admission'],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and 'Ran 15 tests' in t.stderr
A=json.loads((B/'ACCEPTANCE.json').read_text())
assert H(B/'RULES.json')==A['rules_sha256']
r={'batch':'B04h','status':'CRC_SHA256_FULL_EXTRACT_15_TEST_REPLAY_PASSED','owner_download_path':str(OUT),
'archive_sha256':H(OUT),'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,'member_hashes_pass':True,
'full_extraction_pass':True,'extracted_tests_passed':15,
'accepted_rules_sha256':A['rules_sha256'],'accepted_records_if_published':48,'new_empirical_validations':0}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
