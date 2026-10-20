#!/usr/bin/env python3
"""Portable exact-source original BaZi six-chapter archive, 75 independent tests."""
import hashlib,json,os,re,subprocess,tempfile,zipfile
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T='tasks/astro-chinese-primary-sources-20261017';R=T+'/batches/ChineseAstro-09/';OLD=T+'/CHINESE_SOURCE_AUDIT_INDEX_V8.json';WEST='tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json';PREV=T+'/batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json'
NAME='Astrology-BaZi-DiTianSui-13-18-56-Historical-Sources-ChineseAstro09-20261020.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def downloads():
 r=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if r.returncode==0 and r.stdout.strip() and Path(r.stdout.strip()).is_dir() and Path(r.stdout.strip()).resolve()!=Path.home().resolve():return Path(r.stdout.strip())
 return Path.home()/'Téléchargements'
notes=read(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json');witness=read(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json');manifest=read(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json');idx=read(ROOT/OLD)
assert idx['sum_source_annotations']==374 and len(notes['record_rows'])==56
assert notes['source_verses']==7 and witness['quote_count']==56
files={}
for file in ('freeze_bazi_ditiansui_13_18_source.py','test_chinese09_pinned_bazi_original.py','test_chinese09_post_index.py','build_chinese09_release.py','prepare_chinese09_index_v9.py','PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json','TASK_SCOPE.json','WORKING_CHECKPOINT_20261020.md','ORIGINAL_SOURCE_REVIEW_20261020.md','BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json','PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json'):files[R+file]=B/file
for c,m in manifest.items():files[R+m['raw_local_relative']]=B/m['raw_local_relative']
files[OLD]=ROOT/OLD;files[WEST]=ROOT/WEST;files[PREV]=ROOT/PREV
assert all(p.is_file() for p in files.values())
manifest_release={'batch':'ChineseAstro-09','original_sources':'Chinese 2017 pinned Wikisource raw Wikitext chapters 13-18, no independent ancient original edition witness','source_oldids':{c:m['pinned_oldid'] for c,m in manifest.items()},'Chinese_old':374,'Chinese_if_accepted':430,'BaZi_before':154,'BaZi_if_accepted':210,'ZiWei_unchanged':220,'Western_Lilly_unchanged':13044,'Ptolemy_unchanged':1066,'new_exact_source_notes':56,'source_verses':7,'source_commentary_quotes':49,'real_human_predictions_validated':0,'runtime_promotions':0,'members':{name:{'sha256':sha(p),'bytes':p.stat().st_size} for name,p in files.items()}}
out=downloads();out.mkdir(parents=True,exist_ok=True);target=out/NAME;tmp=out/(NAME+'.building');assert not tmp.exists(), 'Interrupted prior ZIP build must be reconciled'
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name,p in files.items():z.write(p,'ChineseAstro09-root/'+name)
 z.writestr('ChineseAstro09-root/RELEASE_MANIFEST.json',json.dumps(manifest_release,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(tmp) as z,tempfile.TemporaryDirectory() as td:
 assert z.testzip() is None;z.extractall(td);root=Path(td)/'ChineseAstro09-root';assert read(root/'RELEASE_MANIFEST.json')==manifest_release
 for name,meta in manifest_release['members'].items():
  p=root/name;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],name
 p=subprocess.run(['python3','-m','unittest','discover','-s',str(root/R),'-p','test_chinese09_pinned_bazi_original.py','-q'],capture_output=True,text=True,timeout=100)
 assert p.returncode==0,p.stdout+'\n'+p.stderr
 m=re.search(r'Ran (\d+) tests',p.stderr);assert m and int(m.group(1))==75,p.stderr
 assert 'skipped' not in p.stderr
os.replace(tmp,target)
receipt={'batch':'ChineseAstro-09','status':'PINNED_13_18_ORIGINAL_BAZI_56_NOTES_75_PORTABLE_TESTS_PASS_CANONICAL_PENDING','filename':NAME,'archive_sha256':sha(target),'archive_bytes':target.stat().st_size,'files_with_exact_bytes_and_sha':len(files),'ZIP_CRC_verified':True,'member_SHA256_and_exact_bytes_passed':True,'independent_original_quote_tests_replayed':75,'Chinese_V8_index_sha256':sha(ROOT/OLD),'parallel_Western_B07bc_index_sha256':sha(ROOT/WEST),'original_manifest_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json'),'source_notes_sha256':sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json'),'source_witness_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json'),'unverified_nine_in_ten_original_author_claim':True,'real_human_predictions_validated':0,'runtime_promotions':0,'remotely_published':False}
(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,indent=2))
