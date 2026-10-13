"""Package only accepted B02t historical source; prove extracted archive usability."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
B=Path(__file__).resolve().parent;ROOT=B.parent
NAME='Astrology-Lilly-Lost-Goods-Fugitives-L-Phase1-Records-20261013.zip'
EXCLUDE={'ARCHIVE_CONTENT_MANIFEST.json','DELIVERABLES_MANIFEST.json','PACKET_USABILITY.json','TEST_PACKET_USABILITY.log','PUBLICATION_RECEIPT.json','DELIVERY_RECEIPT.json','FINAL_RESPONSE.md'}
def H(raw):return hashlib.sha256(raw).hexdigest()
def save(n,j):(B/n).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
a=json.loads((B/'ACCEPTANCE.json').read_text())
assert a['accepted'] and a['rules_sha256']==H((B/'RULES.json').read_bytes()) and a['report_sha256']==H((B/'AUDIT_REPORT.md').read_bytes())
t=json.loads((B/'TEST_RUN_SUMMARY.json').read_text())
assert t['successful'] and t['tests_run']==t['distinct_test_count'] and t['failures']==t['errors']==0
assert t['source_file_sha256']['RULES.json']==a['rules_sha256']
files=[]
for p in sorted(B.rglob('*')):
 rel=p.relative_to(B)
 if not p.is_file() or p.name in EXCLUDE or '__pycache__' in rel.parts:continue
 raw=p.read_bytes();files.append({'path':str(rel),'bytes':len(raw),'sha256':H(raw)})
manifest={'batch':'B02t','file_count':len(files),'files':files,'self_excluded':True}
save('ARCHIVE_CONTENT_MANIFEST.json',manifest)
out=ROOT/'deliverables';out.mkdir(exist_ok=True);archive=out/NAME
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:z.write(B/f['path'],'B02t/'+f['path'])
 z.write(B/'ARCHIVE_CONTENT_MANIFEST.json','B02t/ARCHIVE_CONTENT_MANIFEST.json')
tmp=Path(tempfile.mkdtemp(prefix='lilly-fugitives-phase1-1647-extracted-'))
with zipfile.ZipFile(archive) as z:
 expected={'B02t/'+f['path'] for f in files}|{'B02t/ARCHIVE_CONTENT_MANIFEST.json'}
 assert len(z.namelist())==len(expected) and set(z.namelist())==expected and z.testzip() is None
 z.extractall(tmp)
target=tmp/'B02t'
assert json.loads((target/'ARCHIVE_CONTENT_MANIFEST.json').read_text())==manifest
v=subprocess.run([sys.executable,'verify_archive_contents.py'],cwd=target,capture_output=True,text=True)
assert v.returncode==0,(v.stdout,v.stderr)
re=subprocess.run([sys.executable,'run_verification.py'],cwd=target,capture_output=True,text=True)
(B/'TEST_PACKET_USABILITY.log').write_text(v.stdout+v.stderr+re.stdout+re.stderr)
assert re.returncode==0,(re.stdout,re.stderr)
ret=json.loads((target/'TEST_RUN_SUMMARY.json').read_text())
assert ret['successful'] and ret['discovered_test_ids']==t['discovered_test_ids']
save('PACKET_USABILITY.json',{'batch':'B02t','archive':NAME,'bytes':archive.stat().st_size,'sha256':H(archive.read_bytes()),'crc_verified':True,'actual_extraction':True,'payload_hashes_verified':len(files),'extracted_tests_run':ret['tests_run'],'distinct_test_ids':ret['distinct_test_count'],'identical_test_identities':True,'additional_distinct_from_replay':0,'clinical_or_predictive_validation':False})
report=out/'Astrology-Lilly-Lost-Goods-Fugitives-L-Phase1-Report-20261013.md'
handoff=out/'Astrology-Lilly-Lost-Goods-Fugitives-L-Phase1-Continue-20261013.md'
shutil.copy2(B/'AUDIT_REPORT.md',report);shutil.copy2(B/'CONTINUE_HANDOFF.md',handoff)
deliver=[archive,report,handoff]
save('DELIVERABLES_MANIFEST.json',{'files':[{'filename':f.name,'bytes':f.stat().st_size,'sha256':H(f.read_bytes())} for f in deliver],'local_delivery_receipt_separate':True})
print(json.dumps({'archive':NAME,'zip_bytes':archive.stat().st_size,'payload_files':len(files),'extracted_tests':ret['tests_run'],'sha256':H(archive.read_bytes())}))
