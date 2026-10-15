from pathlib import Path
import requests
base = Path(__file__).parent / "evidence"
prefix = "https://iiif.wellcomecollection.org/image/"
suffix = ".jp2/full/1600,/0/default.jpg"
for n in (425, 426, 427, 428):
    dest = base / ("pdf_1647-%s.jpg" % n)
    if dest.exists():
        continue
    response = requests.get(prefix + ("b30338724_%04d" % n) + suffix, timeout=30)
    response.raise_for_status()
    assert response.headers["content-type"].startswith("image/jpeg")
    dest.write_bytes(response.content)
    print(n, len(response.content))
