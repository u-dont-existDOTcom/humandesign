#!/usr/bin/env python3
"""Reuse same-hash user Downloads copies; no network, no credential, no overwrite."""
from pathlib import Path
import json,hashlib,shutil,subprocess
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'DRIVE_INTAKE.json').read_text())
src=Path(subprocess.check_output(['xdg-user-dir','DOWNLOAD'],text=True).strip())
dst=Path.home()/'Documents/astrology/source-audit-20261005/drive-20261005';dst.mkdir(parents=True,exist_ok=True)
rows=[]
for r in manifest['files']:
 p=src/r['supplied_filename']; t=dst/r['filename']
 if not p.exists():raise SystemExit('Missing existing file: '+r['source_id'])
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 if sha(p)!=r['sha256']:raise SystemExit('Source changed: '+r['source_id'])
 if t.exists():
  if sha(t)!=r['sha256']:raise SystemExit('Destination conflict: '+r['source_id'])
 else:shutil.copyfile(p,t)
 if sha(t)!=r['sha256']:raise SystemExit('Destination hash failed: '+r['source_id'])
 rows.append({'source_id':r['source_id'],'bytes':t.stat().st_size,'sha256':r['sha256'],'status':'PRIVATE_COPY_HASH_VERIFIED'})
(HERE/'PRIVATE_COPY_VERIFICATION.json').write_text(json.dumps({'directory_convention':'$HOME/Documents/astrology/source-audit-20261005/drive-20261005','files':rows},indent=2)+'\n')
print('Verified',len(rows),'private source copies; no full texts added to Git')
