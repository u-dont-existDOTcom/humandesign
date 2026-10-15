"""Release tested Chapter LII documentary source bytes to owner Downloads; no Git action."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib,json,subprocess,tempfile
B=Path(__file__).resolve().parent
root=B.parents[3]
downloads=Path(subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True,check=True).stdout.strip())
assert downloads.is_dir()
archive=downloads/'Astrology-Lilly-Chapter-LII-Documentary-Source-Acceptance-20261015.zip'
receipt=B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json'
assert not archive.exists() and not receipt.exists()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((B/'ACCEPTANCE.json').read_text())
assert a['new_documentary_records']==55 and a['source_uncertainties_retained']==13
items=sorted([p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'])
assert all(p.name not in ['PUBLICATION_RECEIPT.json'] for p in items)
pre=B/'RETAINED_CANONICAL_LILLY_INDEX_BEFORE_B02x.json'
pre_internal='tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
members=[{'path':str(p.relative_to(root)),'sha256':sha(p),'size':p.stat().st_size} for p in items]
members.append({'path':pre_internal,'sha256':sha(pre),'size':pre.stat().st_size})
assert len({x['path'] for x in members})==len(members)
metadata={'kind':'ORIGINAL_1647_CHAPTER_LII_ACCEPTED_DOCUMENTARY_ONLY','batch':'B02x',
'accepted_lilly_if_integrated':3071,'ptolemy_retained':1066,'combined_documentary_if_integrated':4137,
'original_pdf_141mb_not_included':True,'members':members}
metadata_bytes=(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n').encode()
with ZipFile(archive,'x',compression=ZIP_DEFLATED,compresslevel=6) as z:
 for p in items: z.write(p,str(p.relative_to(root)))
 z.write(pre,pre_internal)
 z.writestr('SOURCE_DOCUMENTARY_RELEASE_PACKET_MANIFEST.json',metadata_bytes)
with ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(members)+1
 assert hashlib.sha256(z.read('SOURCE_DOCUMENTARY_RELEASE_PACKET_MANIFEST.json')).hexdigest()==hashlib.sha256(metadata_bytes).hexdigest()
 for rec in members:
  blob=z.read(rec['path'])
  assert len(blob)==rec['size'] and hashlib.sha256(blob).hexdigest()==rec['sha256'],rec['path']
 with tempfile.TemporaryDirectory(prefix='lilly-lii-doc-test-') as td:
  z.extractall(td)
  d=Path(td)/'tasks/astro-source-audit-multipass-20261005/batches/B02x'
  q=subprocess.run(['python3','-m','unittest','-q','test_b02x_staging.py','test_b02x_reverse_coverage.py'],cwd=d,capture_output=True,text=True)
  assert q.returncode==0,(q.stdout,q.stderr)
  assert 'Ran 20 tests' in q.stderr,q.stderr
  for x in members:
   extracted=Path(td)/x['path']
   assert sha(extracted)==x['sha256']
rec={'batch':'B02x','kind':'DOCUMENTARY_SOURCE_ONLY_OWNER_DELIVERY_VERIFIED',
'archive_os_downloads':str(archive),'archive_bytes':archive.stat().st_size,
'archive_sha256':sha(archive),'archive_members_including_manifest':len(members)+1,
'archive_manifest_sha256':hashlib.sha256(metadata_bytes).hexdigest(),
'crc_pass':True,'member_sha256_pass':True,'extracted_file_sha256_pass':True,
'extracted_focused_source_test_count':20,'extracted_source_tests_exit_code':0,
'accepted_new_documentary_units':55,'historical_record_totals_if_canonical':4137,
'prior_accepted_lilly':3016,'retained_ptolemy':1066,
'retained_textual_issues':13,'new_empirical_validations':0,'runtime_promotions':0}
receipt.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(rec,indent=2,ensure_ascii=False))
