#!/usr/bin/env python3
"""Bundle one committed owner comparison with its unchanged source companions."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
BASE='experiments/numerology/owner_comparison_20261004/'
AUDIT='artifacts/numerology/20261004/Numerology-Four-Book-Audit-V2-20261004-151f48c9.zip'


def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--revision',required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--acceptance',type=Path,required=True);a=p.parse_args()
 rev=git('rev-parse','--verify',a.revision+'^{commit}').decode().strip()
 acceptance=json.loads(a.acceptance.read_text())
 if acceptance['status']!='PASS' or acceptance['head']!=rev:raise ValueError('Acceptance must name the exact committed revision')
 old=git('show',rev+':'+AUDIT)
 with zipfile.ZipFile(io.BytesIO(old)) as z:
  data={f:z.read(f) for f in z.namelist() if f not in ['PACKET_MANIFEST.json','README_START_HERE.md','SUMMARY.html','NUMEROLOGY_AUDIT_READER.html']}
 files=git('ls-tree','-r','--name-only',rev,'--',BASE,'scripts/numerology_owner_comparison.py','scripts/numerology_owner_context_checks.py','scripts/numerology_owner_ancillary.py','scripts/numerology_owner_reconciliation.py','scripts/numerology_owner_verify.py','scripts/numerology_owner_bundle.py','tests/test_numerology_owner_comparison.py','tests/test_numerology_owner_reconciliation.py').decode().splitlines()
 for f in files:data[f]=git('show',rev+':'+f)
 data['verification/OWNER_COMPARISON_ACCEPTANCE.json']=a.acceptance.read_bytes()
 try:
  from markdown_it import MarkdownIt
  md=MarkdownIt('commonmark',{'html':False}).enable('table');render=md.render
 except ImportError:render=lambda t:'<pre>'+html.escape(t)+'</pre>'
 sections=[('report','Findings and historical comparison','OWNER_COMPARISON_REPORT.md'),('events','Computed states at every event','EVENT_TABLE.md'),('scope','Source and layer coverage','LAYER_COVERAGE_AND_SOURCE_NOTES.md'),('review','Independent check and reconciliation','REVIEW.md')]
 style='''body{font:17px/1.65 system-ui,sans-serif;margin:0;background:#f7f8fa;color:#222d3a}main{max-width:1120px;margin:auto;padding:36px 24px}h1,h2,h3{line-height:1.25;color:#172b42}h1{font-size:2rem}h2{margin-top:1.8em}p,li{max-width:94ch}section,nav{background:white;border:1px solid #dfe4e9;border-radius:8px;padding:22px 28px;margin:24px 0}a{color:#16557c}small{color:#5c6977}table{border-collapse:collapse;min-width:650px;font-size:14px}td,th{padding:10px;border:1px solid #d6dde5;text-align:left;vertical-align:top}th{background:#edf1f5}.scroll{overflow:auto;margin:20px 0}code{overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f4f7;padding:15px;font-size:13px}@media print{body{background:white}main{padding:0}section{border:0;padding:0;break-before:page}table{min-width:0;font-size:10px}.scroll{overflow:visible}}'''
 nav=''.join(f'<li><a href="#{ident}">{title}</a></li>' for ident,title,_ in sections)
 body=''.join(f'<section id="{ident}"><small>{html.escape(BASE+fn)}</small>'+render(data[BASE+fn].decode())+'</section>' for ident,_,fn in sections)
 body=body.replace('<table>','<div class="scroll"><table>').replace('</table>','</table></div>')
 page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Joel — Numerology comparison</title><style>{style}</style></head><body><main><h1>Numerology and your reported life</h1><p>Separate author systems, explicit combination tests, and preserved counterexamples.</p><small>Retrospective development • Source revision {rev}</small><nav><ol>{nav}</ol></nav>{body}</main></body></html>'.encode()
 for tag in [b'<script',b'<iframe',b'<object',b'<embed',b'<img',b'<link']:
  if tag in page.lower():raise ValueError('Unexpected active/external element')
 data['OWNER_COMPARISON_READER.html']=page
 data['README_START_HERE.md']=f'''# Numerology owner-history comparison

Source revision: {rev}

Open OWNER_COMPARISON_READER.html for the report, coverage ledger and independent check. The JSON files under {BASE} contain exact core calculations, event intervals,36coarse adapters, separate post-result hypotheses and transparency controls. The calculation companions and reconciliation script reproduce these outputs.

This is a retrospective DEVELOPMENT result. It identifies specific correspondence candidates, not an established full-author winner. Original author systems remain unchanged. Unknown periods are not negatives;2008 remains moderate;2029 remains unobserved. A source audit, arithmetic tests and this review are not human predictive validation.

The full derived source-audit companions are included under reference/research/, including the mandatory V2.1 errata and immutable V1 baselines. No raw books, private Library behavioral profiles, credentials or private reviewer runtime logs are included. The old verification receipt describes its own historical source revision; verification/OWNER_COMPARISON_ACCEPTANCE.json describes this comparison revision.

Portable tests, from the extracted directory, require Python3.10+ and the standard library:

```
python3 -m unittest discover -s tests -p 'test_numerology_owner*.py' -v
python3 -m unittest discover -s tests -p 'test_numerology_book_*.py'
```

The full Git/task acceptance commands additionally need the canonical checkout and its history; this ZIP is not a Git repository. PACKET_MANIFEST.json binds payload SHA-256 hashes and excludes itself.
'''.encode()
 manifest={'schema_version':1,'source_revision':rev,'classification':'RETROSPECTIVE_OWNER_DEVELOPMENT','raw_books_included':False,'full_author_predictive_superiority_established':False,'files':{f:hashlib.sha256(v).hexdigest() for f,v in sorted(data.items())}}
 data['PACKET_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
 out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 zip_path=out/f'Numerology-Owner-Comparison-20261004-{rev[:8]}.zip';html_path=out/f'Numerology-Owner-Comparison-20261004-{rev[:8]}.html'
 if zip_path.exists() or html_path.exists():raise FileExistsError('Refusing to overwrite a previous exact-revision delivery')
 with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f,v in sorted(data.items()):
   info=zipfile.ZipInfo(f,(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,v)
 with zipfile.ZipFile(zip_path) as z:
  if z.testzip():raise ValueError('ZIP CRC failed')
  for f,h in manifest['files'].items():
   if hashlib.sha256(z.read(f)).hexdigest()!=h:raise ValueError('Payload mismatch:'+f)
 html_path.write_bytes(page)
 print(json.dumps({'source_revision':rev,'archive_path':str(zip_path),'archive_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'archive_bytes':zip_path.stat().st_size,'reader_path':str(html_path),'reader_sha256':hashlib.sha256(page).hexdigest(),'payload_file_count':len(data),'crc_and_payload_hashes':'PASS'},indent=2))

if __name__=='__main__':main()
