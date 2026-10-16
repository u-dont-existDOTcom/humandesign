#!/usr/bin/env python3
"""Read-only independent scan/record verification for accepted source batches."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'tasks/astro-source-audit-multipass-20261005'
J=lambda f:json.loads(Path(f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
idx=J(BASE/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json')
assert idx['records_count']==4446
assert idx['batches'][-1]['id']=='B03v'
assert idx['empirical_validations']==idx['runtime_promotions']==0
assert sum(b['records_count'] for b in idx['batches'])==4446
results={}
for name,first,last in [('B03u',4324,4384),('B03v',4385,4446)]:
 b=BASE/'batches'/name
 r=J(b/'RULES.json')
 w=J(b/'SOURCE_WINDOW_MANIFEST.json')
 assert [x['record_number'] for x in r['rules']]==list(range(first,last+1))
 assert r['record_count']==last-first+1
 assert H(b/'RULES.json')==next(x['sha256'] for x in idx['batches'] if x['id']==name)
 imgs=w.get('original_images') or w.get('images')
 assert imgs
 for im in imgs:
  raw=(b/im['path']).read_bytes()
  assert H(b/im['path'])==im['sha256']
  assert len(raw)==im.get('bytes',im.get('size_bytes'))
 assert all(not x.get('empirically_validated_prediction',False) and
                not x.get('runtime_rule_promoted',False) for x in r['rules'])
 results[name]={'accepted_documentary_records':r['record_count'],
  'record_range':[first,last],'scans_sha256_verified':len(imgs)}
w=J(BASE/'batches/B03u/SOURCE_WINDOW_MANIFEST.json')
assert w['original_imprinted_page_numerals']==[429,431,430,432]
audit=(BASE/'batches/B03u/SOURCE_FIRST_IMAGE_AUDIT_20261016.md').read_text()
assert 'not a scan-order problem' in audit
assert 'sentence' in audit.lower()
print(json.dumps({'result':'PASS','accepted_lilly':4446,
 'literal_printed_folios':[429,431,430,432],
 'original_pdf_sequence_preserved':True,'new_empirical_predictions':0,
 'batches':results},indent=2))
