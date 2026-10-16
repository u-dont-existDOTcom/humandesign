from pathlib import Path
import requests,hashlib
out=Path(__file__).resolve().parent/'evidence'
for n in range(448,458):
    dest=out/f'pdf_1647-{n}.jpg'
    if dest.exists():
        print('exists',n,dest.stat().st_size);continue
    url=f'https://iiif.wellcomecollection.org/image/b30338724_{n:04d}.jp2/full/1600,/0/default.jpg'
    r=requests.get(url,timeout=45);r.raise_for_status()
    assert r.headers.get('content-type','').startswith('image/jpeg')
    dest.write_bytes(r.content)
    print(n,n-34,len(r.content),hashlib.sha256(r.content).hexdigest())
