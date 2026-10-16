from pathlib import Path
import requests,hashlib
base=Path(__file__).resolve().parent/"evidence"
for n in range(439,448):
 p=base/("pdf_1647-%d.jpg"%n)
 if p.is_file():
  print(n,"EXISTS",hashlib.sha256(p.read_bytes()).hexdigest());continue
 url="https://iiif.wellcomecollection.org/image/b30338724_%04d.jp2/full/1600,/0/default.jpg"%n
 r=requests.get(url,timeout=40);r.raise_for_status()
 assert r.headers.get("content-type","").startswith("image/jpeg"),str(n)
 p.write_bytes(r.content)
 print(n,n-34,len(r.content),hashlib.sha256(r.content).hexdigest())
