from pathlib import Path
import hashlib,json,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent
d=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/'Téléchargements';DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-CIX-Planetary-Manners-Documentary-20261017.zip'
names=['SOURCE_BOUNDARY_CHECKPOINT_20261017.json','SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json',
'SOURCE_FIRST_PROVISIONAL_20261017.json','PROVISIONAL_IMAGE_PROOF_20261017.json','RULES.json','ACCEPTANCE.json','test_b05g_documentary.py','freeze_b05g_documentary.py','prepare_b05g_provisional.py']+[f'evidence/pdf_1647-{n}.jpg' for n in range(573,579)]
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m={f:{'sha256':H(B/f),'bytes':(B/f).stat().st_size} for f in names}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
 for f in names:z.write(B/f,'B05g/'+f)
 z.writestr('B05g/MANIFEST.json',json.dumps(m,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory() as tmp:
 assert z.testzip() is None;z.extractall(tmp);p=Path(tmp)/'B05g'
 for f,x in m.items():assert H(p/f)==x['sha256'] and (p/f).stat().st_size==x['bytes']
 t=subprocess.run(['python3','-m','unittest','-q','test_b05g_documentary'],cwd=p,capture_output=True,text=True)
 assert t.returncode==0 and 'Ran 5 tests' in t.stderr,t.stderr
receipt={'batch':'B05g','archive_path':str(OUT),'archive_sha256':H(OUT),'files':len(names),'CRC':True,'SHA256':True,'extracted_tests_passed':5,'remote_published':False}
(B/'SOURCE_RELEASE_RECEIPT_20261017.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
