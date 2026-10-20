#!/usr/bin/env python3
"""Fetch bounded source page facsimiles from actual independent 1647/1659 printings.

1647 from Wellcome IIIF manifest b30338724, whose 894 canvases are indexed
by printed folio+33 zero-based; printed 755 => b30338724_0789.jp2.
1659 from Wikimedia Commons hosted page renders of a scan of independent
Lilly 1659 printing. Those images are NOT a hash of the whole DjVu.
Source-only task; no predictive evidence.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import urllib.request
import time

B = Path(__file__).resolve().parent
OUT = B / "evidence"
OUT.mkdir(exist_ok=True)
MANIFEST = B / "ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json"
USER_AGENT = "Mozilla/5.0 (public-domain-original-astrological-manuscript-study)"
ORIG1647 = "https://iiif.wellcomecollection.org/image/"
ORIG1659 = (
 "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/"
 "Christian_Astrology_%28Lilly%2C_1659%29.djvu/"
)

def records_for_printed_folio(folio):
    return [
        (folio, "1647", f"1647-original-folio{folio}-iiif.jpg",
         f"{ORIG1647}b30338724_{folio+34:04d}.jp2/full/1800,/0/default.jpg",
         folio+34, "Wellcome Collection original 1647, 894-canvas IIIF"),
        (folio, "1659", f"1659-original-folio{folio}-thumb.jpg",
         (f"{ORIG1659}page{folio+29}-1280px-"
          "Christian_Astrology_%28Lilly%2C_1659%29.djvu.jpg"),
         folio+29, "Wikimedia Commons 1659 separately typeset edition DjVu thumbnail"),
    ]

def retrieve(spec):
    folio, ed, filename, url, frame, collection = spec
    target = OUT / filename
    source_status = "reused_verified_local_original"
    if not target.is_file():
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read()
            if resp.headers.get("content-type","").lower().find("image") < 0:
                raise ValueError("Original scan did not return an image content-type")
        if len(raw)<100000 or not raw.startswith(b"\xff\xd8\xff"):
            raise ValueError("Original scan invalid, not JPEG")
        target.write_bytes(raw)
        source_status="first_retrieval"
    blob=target.read_bytes()
    if len(blob)<100000 or not blob.startswith(b"\xff\xd8\xff"):
        raise ValueError("Pre-existing page invalid")
    return str(folio), ed, {
        "edition": int(ed), "physical_printed_folio": folio, "source_scan_frame": frame,
        "original_printing": collection, "exact_source_url":url,
        "path":str(target.relative_to(B.parents[3])),
        "sha256":sha256(blob).hexdigest(), "bytes":len(blob),
        "source_retrieval_status":source_status,
        "entire_book_binary_sha256_claimed":False,
        "human_observed_prediction_validated":False,
    }

def main():
    # Partial fetch in tightly scoped phases (avoid entire gigantic book).
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--first",type=int,required=True)
    parser.add_argument("--last",type=int,required=True)
    opts=parser.parse_args()
    if not 754<=opts.first<=opts.last<=764 or opts.last-opts.first>5:
        raise ValueError("Bounded printed folio range754..764, max six pages per operation")
    existing={"schema":"B07bd original pages v1","folios":{}}
    if MANIFEST.exists():
        existing=json.loads(MANIFEST.read_text())
    specs=[x for folio in range(opts.first,opts.last+1) for x in records_for_printed_folio(folio)]
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures={ex.submit(retrieve,spec):spec for spec in specs}
        for fut in as_completed(futures):
            folio,ed,meta=fut.result()
            existing["folios"].setdefault(folio,{})[ed]=meta
            print(folio,ed,meta["bytes"],meta["sha256"],flush=True)
            MANIFEST.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+"\n")
    print("DONE",opts.first,opts.last,len(specs),MANIFEST)

if __name__=="__main__":
    main()
