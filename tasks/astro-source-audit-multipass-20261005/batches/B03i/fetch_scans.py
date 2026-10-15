from pathlib import Path
import requests
p=Path(__file__).parent/"evidence"
for n in range(429,439):
  url="https://iiif.wellcomecollection.org/image/b30338724_%04d.jp2/full/1600,/0/default.jpg"%n
  target=p/("pdf_1647-%d.jpg"%n)
  if target.exists():continue
  r=requests.get(url,timeout=45)
  r.raise_for_status()
  assert r.headers.get("content-type","").startswith("image/jpeg")
  target.write_bytes(r.content)
  print(n,len(r.content))
