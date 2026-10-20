#!/usr/bin/env python3
"""Original Zi Wei V2 post-bureau page data, exact ZIP/test replay for 38 source checks."""
import hashlib,json,os,re,subprocess,tempfile,zipfile
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T='tasks/astro-chinese-primary-sources-20261017';R=T+'/batches/ChineseAstro-08/'
ORIG=T+'/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt';OLD=T+'/CHINESE_SOURCE_AUDIT_INDEX_V7.json';WEST='tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
NAME='Astrology-ZiWei-Original-PostBureau-Four-Diagrams-19-Sources-ChineseAstro08-20261020.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def downloads():
 p=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if p.returncode==0 and p.stdout.strip() and Path(p.stdout.strip()).is_dir() and Path(p.stdout.strip()).resolve()!=Path.home().resolve():return Path(p.stdout.strip())
 return Path.home()/'Téléchargements'
source=read(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json');witness=read(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json');old=read(ROOT/OLD)
assert old['sum_source_annotations']==355 and sha(ROOT/ORIG)==source['original_raw_full_SHA256']
assert len(source['record_rows'])==19 and source['next_id']=='ZWD-R0221'
assert sha(B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt')==source['original_excerpt_sha256']
assert len(witness['exact_source_quotes'])==19
files={}
for n in ('freeze_ziwei_original_postbureau_tables.py','test_chinese08_pinned_original.py','test_chinese08_post_index.py','prepare_chinese08_index_v8.py','build_chinese08_release.py','TASK_SCOPE.json','WORKING_CHECKPOINT_20261020.md','ORIGINAL_SOURCE_REVIEW_20261020.md','ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json','SOURCE_1963110_POSTBUREAU_WITNESS_V1.json','SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt'):files[R+n]=B/n
files[ORIG]=ROOT/ORIG;files[T+'/batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json']=ROOT/T/'batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json'
files[OLD]=ROOT/OLD;files[WEST]=ROOT/WEST
assert all(f.is_file() for f in files.values())
manifest={'batch':'ChineseAstro-08','source':'exact pinned transmitted simplified Chinese Wikitext oldid1963110, not authenticated Ming original','original_wikitext_SHA256':sha(ROOT/ORIG),'Chinese_before':355,'BaZi_unchanged':154,'ZiWei_before':201,'new_source_notes':19,'Chinese_if_admitted':374,'ZiWei_if_admitted':220,'West_Lilly_unchanged':13044,'Ptolemy_unchanged':1066,'human_forecasts_validated':0,'engine_parity_verified':False,'runtime_promotions':0,'members':{n:{'sha256':sha(f),'bytes':f.stat().st_size} for n,f in files.items()}}
out=downloads();out.mkdir(exist_ok=True,parents=True);target=out/NAME;temp=out/(NAME+'.building');assert not temp.exists(), 'Interrupted ZIP; check owner Downloads before retry'
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,f in files.items():z.write(f,'ChineseAstro08-root/'+n)
 z.writestr('ChineseAstro08-root/RELEASE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(temp) as z,tempfile.TemporaryDirectory() as td:
 assert z.testzip() is None;z.extractall(td);root=Path(td)/'ChineseAstro08-root';assert read(root/'RELEASE_MANIFEST.json')==manifest
 for n,meta in manifest['members'].items():
  f=root/n;assert f.stat().st_size==meta['bytes'],n;assert sha(f)==meta['sha256'],n
 proc=subprocess.run(['python3','-m','unittest','discover','-s',str(root/R),'-p','test_chinese08_pinned_original.py','-q'],capture_output=True,text=True,timeout=100)
 assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
 m=re.search(r'Ran (\d+) tests',proc.stderr);assert m and int(m.group(1))==38,proc.stderr
 assert 'skipped' not in proc.stderr
os.replace(temp,target)
receipt={'batch':'ChineseAstro-08','status':'CHINESE_V8_ZIWEI_POSTBUREAU_ORIGINAL_SOURCE_ARCHIVE_38_TESTS_PASS_INDEX_PENDING','filename':NAME,'archive_sha256':sha(target),'archive_bytes':target.stat().st_size,'members':len(files),'ZIP_CRC_passed':True,'members_SHA256_and_exact_bytes_verified':True,'independent_extraction_test_replay':38,'Chinese_V7_index_sha256':sha(ROOT/OLD),'Western_B07bc_index_sha256':sha(ROOT/WEST),'source_notes_sha256':sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'),'source_witness_sha256':sha(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json'),'original_source_raw_SHA256':sha(ROOT/ORIG),'independent_real_human_predictions_validated':0,'runtime_astrology_promotions':0,'remote_published':False}
(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
