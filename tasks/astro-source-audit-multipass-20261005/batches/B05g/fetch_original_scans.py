#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, requests, sys
D=Path(__file__).resolve().parent/'evidence'
D.mkdir(exist_ok=True)
a=int(sys.argv[1]) if len(sys.argv)>1 else 480
b=int(sys.argv[2]) if len(sys.argv)>2 else 486
assert 478 <= a <= b <= 894 and b-a <= 15
def fetch(n):
    f=D/f'pdf_1647-{n}.jpg'
    if not f.is_file():
        u=f'https://iiif.wellcomecollection.org/image/b30338724_{n:04d}.jp2/full/1600,/0/default.jpg'
        r=requests.get(u,timeout=45)
        r.raise_for_status()
        assert r.headers.get('content-type','').startswith('image/jpeg')
        f.write_bytes(r.content)
    return n, f.stat().st_size, hashlib.sha256(f.read_bytes()).hexdigest()
with ThreadPoolExecutor(max_workers=3) as p:
    for entry in p.map(fetch,range(a,b+1)):
        print(entry,flush=True)
