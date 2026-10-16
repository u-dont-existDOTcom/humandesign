#!/usr/bin/env python3
from pathlib import Path
import hashlib,requests
B=Path(__file__).resolve().parent/'evidence'
B.mkdir(parents=True,exist_ok=True)
for n in range(458,469):
 p=B/f'pdf_1647-{n}.jpg'
 if p.exists():
  print(n,'EXISTING',len(p.read_bytes()));continue
 url=f'https://iiif.wellcomecollection.org/image/b30338724_{n:04}.jp2/full/1600,/0/default.jpg'
 r=requests.get(url,timeout=35)
 r.raise_for_status()
 assert r.headers.get('content-type','').startswith('image/jpeg')
 p.write_bytes(r.content)
 print(n,n-34,len(r.content),hashlib.sha256(r.content).hexdigest(),flush=True)
