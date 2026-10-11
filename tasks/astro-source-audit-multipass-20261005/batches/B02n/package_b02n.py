"""Accepted B02n packet packaging, byte manifest and actual extracted test replay."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
B=Path(__file__).resolve().parent;ROOT=B.parent
NAME='Astrology-Lilly-Physician-Aphorisms-Records-20261011.zip'
EXCLUDE={'ARCHIVE_CONTENT_MANIFEST.json','DELIVERABLES_MANIFEST.json','PACKET_USABILITY.json','TEST_PACKET_USABILITY.log','PUBLICATION_RECEIPT.json','DELIVERY_RECEIPT.json','FINAL_PRESERVATION_CHECK.json','FINAL_RESPONSE.md'}
def H(raw):return hashlib.sha256(raw).hexdigest()
def save(name,obj):(B/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
a=json.loads((B/'ACCEPTANCE.json').read_text())
assert a['accepted'] and a['rules_sha256']==H((B/'RULES.json').read_bytes()) and a['report_sha256']==H((B/'AUDIT_REPORT.md').read_bytes())
tests=json.loads((B/'TEST_RUN_SUMMARY.json').read_text())
assert tests['successful'] and tests['tests_run']==tests['distinct_test_count']
assert tests['source_file_sha256']['RULES.json']==a['rules_sha256']
items=[]
for p in sorted(B.rglob('*')):
 rel=p.relative_to(B)
 if not p.is_file() or p.name in EXCLUDE or '__pycache__' in rel.parts:continue
 raw=p.read_bytes();items.append({'path':str(rel),'bytes':len(raw),'sha256':H(raw)})
manifest={'batch':'B02n','file_count':len(items),'files':items,'self_excluded':True}
save('ARCHIVE_CONTENT_MANIFEST.json',manifest)
dest=ROOT/'deliverables';dest.mkdir(exist_ok=True);archive=dest/NAME
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for x in items:z.write(B/x['path'],'B02n/'+x['path'])
 z.write(B/'ARCHIVE_CONTENT_MANIFEST.json','B02n/ARCHIVE_CONTENT_MANIFEST.json')
temp=Path(tempfile.mkdtemp(prefix='lilly-b02n-extracted-'))
with zipfile.ZipFile(archive) as z:
 expected={'B02n/'+x['path'] for x in items}|{'B02n/ARCHIVE_CONTENT_MANIFEST.json'}
 assert set(z.namelist())==expected and len(z.namelist())==len(expected) and z.testzip() is None
 z.extractall(temp)
extracted=temp/'B02n'
assert json.loads((extracted/'ARCHIVE_CONTENT_MANIFEST.json').read_text())==manifest
h=subprocess.run([sys.executable,'verify_archive_contents.py'],cwd=extracted,capture_output=True,text=True)
assert h.returncode==0,(h.stdout,h.stderr)
e=subprocess.run([sys.executable,'run_verification.py'],cwd=extracted,capture_output=True,text=True)
(B/'TEST_PACKET_USABILITY.log').write_text(h.stdout+h.stderr+e.stdout+e.stderr)
assert e.returncode==0,(e.stdout,e.stderr)
replay=json.loads((extracted/'TEST_RUN_SUMMARY.json').read_text())
assert replay['successful'] and replay['discovered_test_ids']==tests['discovered_test_ids']
save('PACKET_USABILITY.json',{'batch':'B02n','zip_filename':NAME,'bytes':archive.stat().st_size,'sha256':H(archive.read_bytes()),'crc_ok':True,'actual_extraction':True,'manifest_payload_matches':len(items),'extracted_tests_run':replay['tests_run'],'distinct_test_ids':replay['distinct_test_count'],'same_test_identities':True,'added_distinct_tests':0,'clinical_or_predictive_validation':False})
report=dest/'Astrology-Lilly-Physician-Aphorisms-Report-20261011.md'
handoff=dest/'Astrology-Lilly-Physician-Aphorisms-Continue-20261011.md'
shutil.copy2(B/'AUDIT_REPORT.md',report);shutil.copy2(B/'CONTINUE_HANDOFF.md',handoff)
files=[archive,report,handoff]
save('DELIVERABLES_MANIFEST.json',{'files':[{'filename':p.name,'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in files],'owner_target':'xdg-user-dir DOWNLOAD; actual delivery separate'})
print(json.dumps({'archive':archive.name,'archive_bytes':archive.stat().st_size,'payloads':len(items),'extracted_tests':replay['tests_run'],'sha256':H(archive.read_bytes())}))
