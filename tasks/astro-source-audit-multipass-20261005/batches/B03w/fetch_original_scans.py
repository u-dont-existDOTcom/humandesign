#!/usr/bin/env python3
from pathlib import Path
import requests,hashlib
D=Path(__file__).resolve().parent/'evidence'
D.mkdir(parents=True,exist_ok=True)
for n in range(469,479):
 p=D/f'pdf_1647-{n}.jpg'
 if p.is_file():
  print(n,'PRESERVED',p.stat().st_size,flush=True);continue
 url=f'https://iiif.wellcomecollection.org/image/b30338724_{n:04d}.jp2/full/1600,/0/default.jpg'
 r=requests.get(url,timeout=45)
 r.raise_for_status()
 assert r.headers.get('content-type','').startswith('image/jpeg')
 p.write_bytes(r.content)
 print(n,n-34,len(r.content),hashlib.sha256(r.content).hexdigest(),flush=True)
