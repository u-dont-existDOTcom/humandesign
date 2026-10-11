"""Create packet from frozen local B02m files; extract and independently execute actual ZIP."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,zipfile,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
DOWNLOAD=Path(subprocess.check_output(['xdg-user-dir','DOWNLOAD'],text=True).strip())
NAME='Astrology-Lilly-Hermes-Records-20261011.zip'
IGNORED={'ARCHIVE_CONTENT_MANIFEST.json','DELIVERABLES_MANIFEST.json','PACKET_USABILITY.json','TEST_PACKET_USABILITY.log','SOURCE_REVIEW_STATUS.json','DELIVERY_RECEIPT.json','PRESERVATION_CHECK.json','GITHUB_PUBLICATION_READBACK.json'}
def H(raw):return hashlib.sha256(raw).hexdigest()
def save(name,ob):(ROOT/name).write_text(json.dumps(ob,indent=2,ensure_ascii=False)+'\n')
readme="""# B02m — Hermes in Lilly's Christian Astrology, printed 268–282
This is a historical-source packet, not medicine, diagnosis or validated prediction.
The complete original-page reading was undertaken in this research session; no separate model-family, original Hermes edition, external specialist or empirical clinical validation is claimed.
This packet includes fifteen locating PNG renderings from exact original Lilly PDF302–316, the 52 canonical source records and their conditions, historical materia medica, 14 retained uncertainties, source identity, and reproducible software integrity tests.
  
From the extracted B02m directory run:
  
    python3 run_verification.py
  
Tests and their hashes check data continuity, bounded source scope and packet integrity; they do not establish that source assertions are true. A fresh execution overwrites TEST_RUN.log and TEST_RUN_SUMMARY.json, so run archive hash verification first if comparing exact published ZIP bytes.
  
The next source entry is PDF316 below the divider, Astrologicall Aphorismes beneficiall for Physicians, next record R1703. Chapter XLIV and the multipass research audit remain open.
"""
(ROOT/'README.md').write_text(readme)
save('SOURCE_REVIEW_STATUS.json',{'batch':'B02m','source_pages_visited_in_original_scan':15,
   'source_first_before_compilation':True,
   'cross_family_or_independent_model_review':False,
   'source_passage_semantic_validation_by_independent_specialist':False,
   'full_ancient_Hermes_original_edition_collation':False,
   'tested_runtime':True,'clinical_or_predictive_validation':False,
   'scope':'Text and page-image source observations compiled in current chat; mechanical integrity tests; no blind validation.'})
# Build ZIP after core tests have already passed
payload=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or p.name in IGNORED or '__pycache__' in p.parts:
  continue
 rel=str(p.relative_to(ROOT));payload.append({'path':rel,'bytes':p.stat().st_size,'sha256':H(p.read_bytes())})
manifest={'batch':'B02m','source_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'file_count':len(payload),'files':payload,'manifest_self_hash_excluded':True,'test_entrypoint':'python run_verification.py'}
save('ARCHIVE_CONTENT_MANIFEST.json',manifest)
dest=PARENT/'deliverables';dest.mkdir(exist_ok=True)
z=dest/NAME
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as a:
 for item in payload:a.write(ROOT/item['path'],'B02m/'+item['path'])
 a.write(ROOT/'ARCHIVE_CONTENT_MANIFEST.json','B02m/ARCHIVE_CONTENT_MANIFEST.json')
temp=Path(tempfile.mkdtemp(prefix='lilly-b02m-extracted-'))
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 a.extractall(temp)
ind=temp/'B02m'
observed=json.loads((ind/'ARCHIVE_CONTENT_MANIFEST.json').read_text())
assert observed==manifest
for item in payload:
 f=ind/item['path'];assert f.stat().st_size==item['bytes'] and H(f.read_bytes())==item['sha256'],item['path']
exe=subprocess.run([sys.executable,'run_verification.py'],cwd=ind,text=True,capture_output=True)
(ROOT/'TEST_PACKET_USABILITY.log').write_text(exe.stdout+exe.stderr)
summ=json.loads((ind/'TEST_RUN_SUMMARY.json').read_text())
orig=json.loads((ROOT/'TEST_RUN_SUMMARY.json').read_text())
assert exe.returncode==0 and summ['successful'] and summ['discovered_test_ids']==orig['discovered_test_ids']
save('PACKET_USABILITY.json',{'batch':'B02m','zip_filename':NAME,'bytes':z.stat().st_size,
 'sha256':H(z.read_bytes()),'crc_ok':True,'actual_extraction':True,
 'manifest_payload_matches':len(payload),'extracted_tests_run':summ['tests_run'],
 'distinct_test_ids':len(orig['discovered_test_ids']),'same_identities':True,
 'added_distinct_tests':0,'clinical_or_predictive_validation':False})
paths=[(ROOT/'AUDIT_REPORT.md',dest/'Astrology-Lilly-Hermes-20261011.md'),
       (ROOT/'CONTINUE_HANDOFF.md',dest/'Astrology-Lilly-Handoff-B02m-20261011.md')]
for a,b in paths:shutil.copyfile(a,b)
files=[z]+[x[1] for x in paths]
save('DELIVERABLES_MANIFEST.json',{'files':[{'filename':p.name,'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in files],
      'owner_target':'xdg-user-dir DOWNLOAD; actual delivery checked separately'})
print(json.dumps({'archive':str(z),'archive_bytes':z.stat().st_size,'payloads':len(payload),
   'extracted_tests':summ['tests_run'],'sha256':H(z.read_bytes()),
   'prepared_files':[p.name for p in files],'download_dir_exists':DOWNLOAD.is_dir()}))
