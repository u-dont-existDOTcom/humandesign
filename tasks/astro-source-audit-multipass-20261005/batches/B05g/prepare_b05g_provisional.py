from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
g=json.loads((B/'SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json').read_text())
w=json.loads((B/'SOURCE_BOUNDARY_CHECKPOINT_20261017.json').read_text())
assert g['source_units']==sum(len(z['claims']) for z in g['source_groups'])==31
assert len(g['source_groups'])==8
assert w['accepted_prior_lilly']==6560 and w['next_source_record']==6561
assert w['following_heading_original_pdf']==577
s=[];records=[]
for x in g['source_groups']:
 sid=f'B05g-S{len(s)+1:03}';ids=[]
 for role,anchor,meaning,caveat in x['claims']:
  lid=f'B05g-C{len(records)+1:03}';ids.append(lid)
  records.append({'id':lid,'source_span':sid,'pdf_pages':x['pages'],'role':role,
   'anchor_not_diplomatic':anchor,'meaning_historical_only':meaning,'source_limit':caveat,
   'accepted':False,'validated_personality_prediction':False})
 s.append({'id':sid,'pdf_pages':x['pages'],'mapped_claim_ids':ids,'label':x['label']})
assert len(records)==31 and len({r['id'] for r in records})==31
out={'batch':'B05g','status':'PROVISIONAL_NOT_ADMITTED','source_passages':s,'provisional_annotations':records,'accepted_historical_records_added':0,'independent_personality_validations':0}
(B/'SOURCE_FIRST_PROVISIONAL_20261017.json').write_text(json.dumps(out,indent=2)+'\n')
images=[]
for n in range(573,579):
 p=B/'evidence'/f'pdf_1647-{n}.jpg'
 images.append({'page':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert all(images[i]['sha256']==w['source_page_sha256'][str(images[i]['page'])] for i in range(6))
(B/'PROVISIONAL_IMAGE_PROOF_20261017.json').write_text(json.dumps({'batch':'B05g','images':images,'provisional_claims':31,'accepted_new':0},indent=2)+'\n')
print('31 provisional claims, 8 source groups, 6 image hashes verified; no admission')
