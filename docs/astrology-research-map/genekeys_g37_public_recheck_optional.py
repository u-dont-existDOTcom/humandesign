"""OPTIONAL bounded public-source recheck of the 64 Gene Keys preview pages.

Independent local researcher command, NEVER run by unit tests or production.
Requires system Python requests + beautifulsoup4 (not project dependencies).
Only unauthenticated, publicly accessible 64 key pages are fetched.
Long Rudd preview quotations are held temporarily IN MEMORY and NEVER saved.
Only the short headings/partner and source hashes are serialized with
genekeys_g37_public_source_catalog.build. Source version changes require
new research record; do not overwrite accepted G37 snapshot.

Example:
  python3 genekeys_g37_public_recheck_optional.py \
       --out /tmp/independent-new-64-short-source-review.json
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import re
import time

from genekeys_g37_public_source_catalog import build


def fetch_public_short_page(number:int)->dict:
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError("optional researcher needs system requests and bs4") from exc
    if type(number) is not int or not 1<=number<=64:
        raise ValueError("key 1..64 required")
    url=f"https://genekeys.com/gene-key-{number}/"
    error=None
    for attempt in range(2):
        try:
            resp=requests.get(url,timeout=18,
                              headers={"User-Agent":"Mozilla/5.0 (public-source-audit)"})
            resp.raise_for_status()
            if resp.url.rstrip("/") != url.rstrip("/"):
                raise ValueError("unexpected publisher redirect")
            soup=BeautifulSoup(resp.content,"lxml")
            headings=[x.get_text(" ",strip=True)
                      for x in soup.select("h3")
                      if x.get_text(" ",strip=True).count("–")==2]
            if not headings:
                raise ValueError("publisher short Shadow/Gift/Siddhi heading missing")
            trio=[s.strip() for s in headings[0].split("–")]
            partner=[x for x in soup.find_all("a")
                     if "Travel to Programming Partner"
                     in x.get_text(" ",strip=True)]
            if len(partner)!=1:
                raise ValueError("partner navigation source absent/duplicate")
            match=re.search(r"Partner\s*[–-]\s*(\d+)",
                            partner[0].get_text(" ",strip=True))
            if not match:
                raise ValueError("programming partner number absent")
            quote=[x for x in soup.stripped_strings
                   if re.search(r"Richard Rudd,\s*(?:The\s+)?64 Ways",x)]
            if len(quote)!=1:
                raise ValueError("missing or multiple public attributed short previews")
            q=quote[0].strip()
            return {
                "key":number, "status":"OK", "url":url,
                "heading":trio,
                "programming_partner":int(match.group(1)),
                "public_html_sha256":sha256(resp.content).hexdigest(),
                "html_bytes":len(resp.content),
                "public_rudd_quote":q,
                "quote_sha256":sha256(q.encode()).hexdigest(),
                "quote_length_chars":len(q),
                "quote_flags_heuristic":{},
            }
        except Exception as exc:
            error=str(exc)
            time.sleep(.5*(attempt+1))
    return {"key":number,"status":"ERROR","url":url,"error":error}


def recheck(*,out:Path)->dict:
    with ThreadPoolExecutor(max_workers=5) as pool:
        pending={pool.submit(fetch_public_short_page,i):i for i in range(1,65)}
        interim={f.result()["key"]:f.result() for f in as_completed(pending)}
    readings=[interim[i] for i in range(1,65)]
    data=build({"results":readings})
    if out.exists():
        raise FileExistsError("never overwrite an accepted or earlier snapshot")
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    return data


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=recheck(out=args.out)
    print("OPTIONAL_DIRECT_PUBLIC_RECHECK",len(result["rows"]),
          "published_partner_exceptions",
          [(x["key"],x["official_published_partner"])
           for x in result["site_partner_discrepancies"]])
    print("SOURCE_VERSION_SHA256",result["canonical_registry_sha256"])
