"""Publish checked owner-local bounded B02w documentary source packet.

This never mutates accepted prior batches, never uploads or pushes Git.
A receipt is emitted only after byte comparison, CRC and extracted suite replay.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,subprocess,tempfile,shutil,os
B=Path(__file__).resolve().parent
root=B.parents[2]
D=Path(subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True,check=True).stdout.strip())
assert D.is_dir(),D
archive=D/'Astrology-Lilly-Chapter-LI-Documentary-Source-Acceptance-20261015.zip'
receipt=B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json'
assert not archive.exists() and not receipt.exists(), 'Do not overwrite an existing archive or receipt'
include=[
 'LI_SOURCE_FIRST_INVENTORY_NOTES_20261015.md','OPENING_AND_HANDOFF_20261015.md',
 'RETAINED_LILLY_INDEX_BEFORE_B02w.json','RULES_DRAFT.json',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','SOURCE_FIRST_OPENING_P400_402_20261015.md',
 'SOURCE_IMAGE_MANIFEST_OPENING_20261015.json','SOURCE_ORDER_DRAFT.json',
 'SOURCE_WINDOW_MANIFEST.json','UNRESOLVED_DRAFT.json',
 'annotate_li_preconditions.py','assemble_li_initial.py','build_b02w_provisional_packet.py',
 'build_b02w_documentary_release.py',
 'recovery/SOURCE_FIRST_CLAUSES_before_precondition_annotation_20261015.json',
 'recovery/BEFORE_SECOND_PASS_20261015_SHA256.json',
 'SOURCE_FIRST_PACKET_MANIFEST.json',
 'test_b02w_staging.py','test_b02w_reverse_coverage.py','verify_source_opening.py',
 'ORIGINAL_TO_RECORD_COVERAGE_V1.json','SECOND_PASS_CORRECTION_RECEIPT_20261015.json',
 'INDEPENDENT_IMAGE_FIRST_REVIEW_20261015.md','HANDOFF_AFTER_DOCUMENTARY_ADMISSION_20261015.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','CLAIM_LEDGER.json','ACCEPTANCE.json'
]
include += sorted(str(x.relative_to(B)) for x in (B/'recovery/BEFORE_SECOND_PASS_20261015').rglob('*') if x.is_file())
include += [f'evidence/pdf-{n}.png' for n in range(400,405)]
assert len(include)==len(set(include))
a=json.loads((B/'ACCEPTANCE.json').read_text())
assert a['accepted'] and a['new_documentary_source_units']==42 and a['runtime_promotions']==0
def sha(b):return hashlib.sha256(b).hexdigest()
payload=[]
for name in include:
    p=B/name
    assert p.is_file(),p
    blob=p.read_bytes()
    payload.append({'path':f'batches/B02w/{name}','source_path':name,'sha256':sha(blob),'bytes':len(blob)})
# Include accepted prior exact original boundary image: required to replay p400=B02v check.
prev=B.parent/'B02v/evidence/pdf-400.png'
assert prev.is_file()
assert sha(prev.read_bytes())==json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text())['source_images'][0]['sha256']
payload.append({'path':'batches/B02v/evidence/pdf-400.png','source_path':'PRIOR_ACCEPTED_B02v_ORIGINAL_IMAGE','sha256':sha(prev.read_bytes()),'bytes':prev.stat().st_size})
manifest={'batch':'B02w','kind':'CHAPTER_LI_DOCUMENTARY_ACCEPTED_SOURCE_RELEASE_NOT_EMPIRICAL',
'accepted_lilly_if_canonical_published':3016,'retained_ptolemy':1066,'combined_after_publication':4082,
'original_pdf_not_embedded':True,'members':payload,'count':len(payload)}
mem=json.dumps(manifest,ensure_ascii=False,indent=2).encode()+b'\n'
with ZipFile(archive,'x',compression=ZIP_DEFLATED,compresslevel=6) as z:
    for item in payload:
        data=(prev if item['source_path']=='PRIOR_ACCEPTED_B02v_ORIGINAL_IMAGE' else B/item['source_path']).read_bytes()
        z.writestr(item['path'],data)
    z.writestr('SOURCE_DOCUMENTARY_RELEASE_PACKET_MANIFEST.json',mem)
with ZipFile(archive) as z:
    assert z.testzip() is None
    names=set(z.namelist())
    assert len(names)==len(payload)+1
    assert sha(z.read('SOURCE_DOCUMENTARY_RELEASE_PACKET_MANIFEST.json'))==sha(mem)
    for item in payload:
        blob=z.read(item['path'])
        assert len(blob)==item['bytes'] and sha(blob)==item['sha256'],item['path']
    with tempfile.TemporaryDirectory(prefix='lilly-li-documentary-check-') as t:
        z.extractall(t)
        td=Path(t)/'batches/B02w'
        assert td.is_dir()
        q=subprocess.run(['python3','-m','unittest','-q','test_b02w_staging.py','test_b02w_reverse_coverage.py'],cwd=td,capture_output=True,text=True)
        assert q.returncode==0,(q.stdout,q.stderr)
        assert 'Ran 22 tests' in q.stderr,(q.stdout,q.stderr)
        for item in payload:
            f=Path(t)/item['path']
            assert sha(f.read_bytes())==item['sha256']
receipt_data={'kind':'DOCUMENTARY_SOURCE_ONLY_OWNER_RELEASE_VERIFIED','batch':'B02w',
'archive_os_downloads':str(archive),'archive_sha256':sha(archive.read_bytes()),
'archive_bytes':archive.stat().st_size,'manifest_sha256':sha(mem),'members':len(payload)+1,
'extracted_original_source_test_count':22,'extracted_test_exit_code':q.returncode,
'zip_crc_pass':True,'per_file_sha256_pass':True,'actual_extraction_pass':True,
'owner_local_archive_bytes_match':True,
'prior_accepted_lilly':2974,'new_documentary_units':42,'lilly_if_published':3016,
'ptolemy_retained':1066,'combined_if_published':4082,'retained_issues':11,
'new_empirical_validations':0,'new_runtime_promotions':0}
receipt.write_text(json.dumps(receipt_data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt_data,indent=2,ensure_ascii=False))
