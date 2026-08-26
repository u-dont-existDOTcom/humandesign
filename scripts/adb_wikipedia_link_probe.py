#!/usr/bin/env python3
"""Engineering probe for ADB-provided Wikipedia link representation.

No research data are scored. Records only compact raw-line contexts containing
'wikipedia' from a few already identity-resolved ADB pages.
"""
from __future__ import annotations
import json, urllib.parse, urllib.request
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
OUT=REPO/'reference'/'research'/'adb_wikipedia_link_probe_v1.json'
API='https://www.astro.com/wiki/astro-databank/api.php'
UA='humandesign-adb-wikipedia-link-probe/1.0'
TITLES=['Hefner, Hugh','Coppola, Sofia','Bardot, Brigitte','Presley, Lisa Marie']

def fetch(title):
    q=urllib.parse.urlencode({'action':'query','prop':'revisions','rvprop':'content','rvslots':'main','titles':title,'formatversion':2,'format':'json'})
    req=urllib.request.Request(API+'?'+q,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=15) as r:
        d=json.loads(r.read().decode('utf-8','replace'))
    p=d['query']['pages'][0]; rev=p['revisions'][0]
    return (rev.get('slots',{}).get('main',{}) or {}).get('content') or rev.get('content') or rev.get('*') or ''

def main():
    rows=[]
    for title in TITLES:
        wt=fetch(title); lines=wt.splitlines(); hits=[]
        for i,s in enumerate(lines):
            if 'wikipedia' in s.casefold() or 'wiki' in s.casefold() and 'http' in s.casefold():
                hits.append({'line':i+1,'context':lines[max(0,i-2):min(len(lines),i+3)]})
        rows.append({'title':title,'hits':hits[:20]})
    OUT.write_text(json.dumps({'status':'engineering_probe','pages':rows},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if __name__=='__main__': main()
