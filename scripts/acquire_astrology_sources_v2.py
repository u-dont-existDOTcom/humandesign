#!/usr/bin/env python3
"""Resume explicitly listed public downloads; never purchase or bypass access controls.

Raw books stay outside Git. This checks file identity/structure, not chapter-level
completeness or the correctness of a source's astrological claims.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest',required=True,type=Path)
    ap.add_argument('--dest',required=True,type=Path)
    ap.add_argument('--ids',nargs='+',required=True)
    ap.add_argument('--max-mb',type=int,default=220)
    args=ap.parse_args()
    d=json.loads(args.manifest.read_text());lookup={s['id']:s for s in d['sources']}
    if set(args.ids)-set(lookup):raise SystemExit('Unknown source IDs')
    args.dest.mkdir(parents=True,exist_ok=True)
    results=[]
    for sid in args.ids:
        source=lookup[sid];url=source.get('download_url');name=source.get('filename')
        row={'id':sid,'status':'PENDING'}
        if not url or not name:
            row.update(status='NO_VERIFIED_DIRECT_DOWNLOAD',next_action='Use source_url and edition contract; no automatic purchase')
            results.append(row);continue
        if Path(name).name != name or not url.startswith('https://'):
            raise SystemExit('Unsafe filename or non-HTTPS URL in manifest')
        p=args.dest/name
        try:
            if not p.exists():
                req=Request(url,headers={'User-Agent':'HumanDesign-Source-Audit/2.0'})
                with urlopen(req,timeout=90) as response:
                    tmp=p.with_suffix(p.suffix+'.part');size=0
                    with tmp.open('wb') as f:
                        while True:
                            b=response.read(1024*256)
                            if not b:break
                            size+=len(b)
                            if size>args.max_mb*1024*1024:raise ValueError('File exceeds configured size limit')
                            f.write(b)
                    if tmp.read_bytes()[:5]!=b'%PDF-':raise ValueError('Downloaded body is not PDF')
                    tmp.replace(p)
            content=p.read_bytes()
            if content[:5]!=b'%PDF-':raise ValueError('Existing file is not PDF')
            row.update(status='DOWNLOADED_NOT_SOURCE_AUDITED',filename=name,bytes=len(content),sha256=hashlib.sha256(content).hexdigest())
            expected=source.get('downloaded_sha256')
            if expected and expected!=row['sha256']:raise ValueError('Previously verified hash changed; inspect new edition before use')
            try:
                check=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,timeout=30)
                row['pdfinfo_ok']=check.returncode==0
                for line in check.stdout.splitlines():
                    if line.startswith('Pages:'):row['pdf_pages']=int(line.split(':',1)[1])
            except (FileNotFoundError,subprocess.TimeoutExpired):row['pdfinfo_ok']=None
        except (HTTPError,URLError,ValueError,OSError) as exc:
            row.update(status='ACCESS_OR_INTEGRITY_FAILURE',error=str(exc)[:240])
        results.append(row)
        print(sid,row['status'])
    out=args.dest/'resumed_download_receipt.json'
    out.write_text(json.dumps(results,indent=2)+'\n')
    print(out)


if __name__=='__main__':main()
