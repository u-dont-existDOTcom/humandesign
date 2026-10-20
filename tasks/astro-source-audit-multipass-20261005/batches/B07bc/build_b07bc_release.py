#!/usr/bin/env python3
"""Archive 4 original-image witnesses + portable independent 44-test playback."""
import hashlib,json,os,re,subprocess,tempfile,zipfile
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
T='tasks/astro-source-audit-multipass-20261005';R=T+'/batches/B07bc/'
WEST=T+'/LILLY_SOURCE_EXTRACTION_INDEX_V1.json';CHINA='tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json'
NAME='Astrology-Lilly-Sicknesse-Servants-1647-1659-27-Historical-Sources-B07bc-20261020.zip'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def downloads():
 p=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if p.returncode==0 and p.stdout.strip() and Path(p.stdout.strip()).is_dir() and Path(p.stdout.strip()).resolve()!=Path.home().resolve():return Path(p.stdout.strip())
 return Path.home()/'Téléchargements'
source=read(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json');rules=read(B/'RULES.json');accept=read(B/'ACCEPTANCE.json');old=read(ROOT/WEST);china=read(ROOT/CHINA)
assert old['records_count']==13017 and old['batches'][-1]['id']=='B07bb'
assert china['sum_source_annotations']==355 and len(source['records'])==len(rules['rules'])==27
assert source['next_R']=='R13045' and source['next_chapter']=='CLXXXI'
assert sha(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json')==accept['source_notes_sha256']
assert sha(B/'RULES.json')==accept['rules_sha256']
files={}
for n in ('build_b07bc_sicknesse_source.py','test_b07bc_original_sicknesse.py','test_b07bc_post_index.py','prepare_b07bc_canonical.py','build_b07bc_release.py','ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json','RULES.json','ACCEPTANCE.json','TASK_SCOPE.json','WORKING_CHECKPOINT_20261020.md','ORIGINAL_SOURCE_REVIEW_20261020.md','SOURCE_IMAGE_1659_754_RETRIEVAL.json'):
 files[R+n]=B/n
files[T+'/batches/B07bb/ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json']=B.parent/'B07bb/ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json'
for folio,editions in source['original_photographic_witnesses'].items():
 for ed,meta in editions.items():
  p=ROOT/meta['original_source_repo_relative_file'];assert p.is_file() and sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes'];files[meta['original_source_repo_relative_file']]=p
files[WEST]=ROOT/WEST;files[CHINA]=ROOT/CHINA
assert all(p.is_file() for p in files.values())
manifest={'batch':'B07bc','provenance':'Original original-printing 1647 and distinct original printing 1659 page photos; complete DjVu original checksum not checked','old_lilly':13017,'new_historical_notes':27,'new_lilly_if_admitted':13044,'Ptolemy_retained':1066,'Western_if_admitted':14110,'Chinese_V7_untouched':355,'next':'R13045 CLXXXI Of Marriage','real_human_predictive_validations':0,'runtime_promotions':0,'source_only':True,'original_first_pdf_sha256':source['source_full_original_Wellcome_1647_PDF_sha256'],'members':{name:{'sha256':sha(p),'bytes':p.stat().st_size} for name,p in files.items()}}
out=downloads();out.mkdir(parents=True,exist_ok=True);target=out/NAME;tmp=out/(NAME+'.building')
assert not tmp.exists(), 'Interrupted previous archive build: inspect before retry'
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in files.items():z.write(p,'B07bc-root/'+n)
 z.writestr('B07bc-root/RELEASE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(tmp) as z,tempfile.TemporaryDirectory() as td:
 assert z.testzip() is None
 z.extractall(td);root=Path(td)/'B07bc-root';assert read(root/'RELEASE_MANIFEST.json')==manifest
 for name,meta in manifest['members'].items():
  p=root/name;assert p.stat().st_size==meta['bytes'],name;assert sha(p)==meta['sha256'],name
 proc=subprocess.run(['python3','-m','unittest','discover','-s',str(root/R),'-p','test_b07bc_original_sicknesse.py','-q'],capture_output=True,text=True,timeout=100)
 assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
 m=re.search(r'Ran (\d+) tests',proc.stderr);assert m and int(m.group(1))==44,proc.stderr
 assert 'skipped' not in proc.stderr
os.replace(tmp,target)
receipt={'batch':'B07bc','status':'ORIGINAL_CLXXX_SOURCE_27_NOTES_44_PORTABLE_TESTS_PASS_CANONICAL_PENDING','filename':NAME,'archive_sha256':sha(target),'archive_bytes':target.stat().st_size,'ZIP_CRC_verified':True,'member_SHA256_and_bytes_verified':True,'independently_extracted_test_replays':44,'archived_members':len(files),'original_page_images_verified':4,'source_notes_sha256':accept['source_notes_sha256'],'rules_sha256':accept['rules_sha256'],'original_index_sha256':sha(ROOT/WEST),'Chinese_V7_index_sha256':sha(ROOT/CHINA),'historical_notes_if_admitted':27,'independent_person_outcomes_validated':0,'runtime_model_promotions':0,'remote_published':False}
(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
