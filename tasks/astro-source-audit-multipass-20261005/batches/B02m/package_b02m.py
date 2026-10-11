"""Build the accepted historical-source packet and test an actual fresh extraction."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
NAME='Astrology-Lilly-Hermes-Records-20261011.zip'
EXCLUDE={'ARCHIVE_CONTENT_MANIFEST.json','DELIVERABLES_MANIFEST.json','PACKET_USABILITY.json','TEST_PACKET_USABILITY.log','PUBLICATION_RECEIPT.json','DELIVERY_RECEIPT.json','FINAL_PRESERVATION_CHECK.json','FINAL_RESPONSE.md'}
def H(raw):return hashlib.sha256(raw).hexdigest()
def save(name,value):(ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
    acceptance=json.loads((ROOT/'ACCEPTANCE.json').read_text())
    if not acceptance.get('accepted'):raise RuntimeError('No accepted source/claim review')
    summary=json.loads((ROOT/'TEST_RUN_SUMMARY.json').read_text())
    if not summary['successful']:raise RuntimeError('Source-data suite did not pass')
    payload=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or p.name in EXCLUDE or any(x in {'__pycache__','rerender','deliverables','.git'} for x in rel.parts):continue
        raw=p.read_bytes();payload.append({'path':str(rel),'bytes':len(raw),'sha256':H(raw)})
    manifest={'batch':'B02m','payload_count':len(payload),'files':payload,'manifest_self_excluded':True,'test_entrypoint':'python3 run_verification.py'}
    save('ARCHIVE_CONTENT_MANIFEST.json',manifest)
    dest=ROOT.parent/'deliverables';dest.mkdir(exist_ok=True);archive=dest/NAME
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for x in payload:z.write(ROOT/x['path'],'B02m/'+x['path'])
        z.write(ROOT/'ARCHIVE_CONTENT_MANIFEST.json','B02m/ARCHIVE_CONTENT_MANIFEST.json')
    extracted=Path(tempfile.mkdtemp(prefix='lilly-hermes-packet-'))
    with zipfile.ZipFile(archive) as z:
        expected={'B02m/'+x['path'] for x in payload}|{'B02m/ARCHIVE_CONTENT_MANIFEST.json'}
        if len(z.namelist())!=len(expected) or set(z.namelist())!=expected:raise RuntimeError('Archive members differ')
        if z.testzip() is not None:raise RuntimeError('CRC failure')
        z.extractall(extracted)
    working=extracted/'B02m'
    h=subprocess.run([sys.executable,'verify_archive_contents.py'],cwd=working,capture_output=True,text=True)
    if h.returncode:raise RuntimeError(h.stdout+h.stderr)
    run=subprocess.run([sys.executable,'run_verification.py'],cwd=working,capture_output=True,text=True)
    (ROOT/'TEST_PACKET_USABILITY.log').write_text(run.stdout+run.stderr)
    fresh=json.loads((working/'TEST_RUN_SUMMARY.json').read_text())
    if run.returncode or not fresh['successful']:raise RuntimeError('Extracted tests failed')
    if fresh['discovered_test_ids']!=summary['discovered_test_ids']:raise RuntimeError('Test identity mismatch')
    save('PACKET_USABILITY.json',{'batch':'B02m','archive':NAME,'bytes':archive.stat().st_size,'sha256':H(archive.read_bytes()),'crc':'PASS','actual_extraction':True,'exact_archive_member_set':True,'payload_hashes_verified':len(payload),'manifest_verified_separately':True,'hash_verifier_exit':h.returncode,'test_exit':run.returncode,'tests_run':fresh['tests_run'],'failures':fresh['failures'],'errors':fresh['errors'],'same_test_identities':True,'new_test_identities_from_repeat':0,'clinical_or_predictive_validation':False})
    shutil.copy2(ROOT/'AUDIT_REPORT.md',dest/'Astrology-Lilly-Hermes-20261011.md')
    shutil.copy2(ROOT/'CONTINUE_HANDOFF.md',dest/'Astrology-Lilly-Handoff-B02m-20261011.md')
    outputs=[archive,dest/'Astrology-Lilly-Hermes-20261011.md',dest/'Astrology-Lilly-Handoff-B02m-20261011.md']
    save('DELIVERABLES_MANIFEST.json',{'files':[{'filename':p.name,'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in outputs],'source_stage':'accepted source/claim packet; publication and owner delivery recorded separately'})
    print(json.dumps({'archive_bytes':archive.stat().st_size,'payload_hashes':len(payload),'extracted_tests':fresh['tests_run'],'archive_sha256':H(archive.read_bytes())}))
if __name__=='__main__':main()
