import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
class Evidence(unittest.TestCase):
 def test_local_sequence(self):
  r=j('RULES.json')['rules']
  self.assertEqual([x['record_number'] for x in r],list(range(6561,6592)))
 def test_no_personality_proof(self):
  self.assertTrue(all(not x['validated_personality_prediction'] and not x['runtime_model_promoted'] for x in j('RULES.json')['rules']))
 def test_source_hashes(self):
  w=j('SOURCE_BOUNDARY_CHECKPOINT_20261017.json')
  for k,v in w['source_page_sha256'].items():
   p=B/'evidence'/f'pdf_1647-{k}.jpg'
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),v)
 def test_source_mapping(self):
  d=j('SOURCE_FIRST_PROVISIONAL_20261017.json')
  ids=[z for s in d['source_passages'] for z in s['mapped_claim_ids']]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(len(ids),31)
 def test_next_chapter_boundary(self):
  self.assertEqual(j('ACCEPTANCE.json')['next_heading_page'],577)
  self.assertEqual(j('ACCEPTANCE.json')['combined_if_published'],7657)
if __name__=='__main__':unittest.main()
