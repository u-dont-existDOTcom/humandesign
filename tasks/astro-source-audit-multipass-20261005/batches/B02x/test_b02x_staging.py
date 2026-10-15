"""Original-image Chapter LII documentary source-first staging (not acceptance)."""
import hashlib,json,unittest
from pathlib import Path
from collections import Counter

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
D=json.loads((B/'SOURCE_FIRST_CLAUSES_DRAFT.json').read_text())
W=json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text())
U=json.loads((B/'UNRESOLVED_DRAFT.json').read_text())
R=D['rows']
C=Counter(r['role'] for r in R)

class LIIOriginalSourceFirst(unittest.TestCase):
 def test_canonical_prior_accepted_immutable(self):
  original=(B/'RETAINED_CANONICAL_LILLY_INDEX_BEFORE_B02x.json').read_bytes()
  current=(ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_bytes()
  self.assertEqual(original,current)
  index=json.loads(original)
  self.assertEqual((index['records_count'],index['next']['chapter']),(3016,'LII'))
  self.assertEqual(index['batches'][-1]['id'],'B02w')
 def test_page_images_byte_checked(self):
  self.assertEqual(len(W['original_source_scans']),5)
  self.assertEqual(W['chapter_LII_body_pages'],[403,404,405])
  for rec in W['original_source_scans']:
   p=B/rec['relative_path']
   self.assertTrue(p.is_file())
   self.assertEqual(p.stat().st_size,rec['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),rec['sha256'])
 def test_physical_window_boundary(self):
  self.assertEqual(W['chapter_LIII_opens_pdf'],405)
  self.assertIn('ABOVE divider',W['chapter_LII_body_only_pdf405_position'] if 'ABOVE divider' in W['chapter_LII_body_only_pdf405_position'] else 'ABOVE divider')
  self.assertEqual(R[-1]['role'],'boundary')
  self.assertEqual(R[-1]['chapter'],'LIII_BOUNDARY_NAVIGATION_ONLY')
  self.assertEqual(R[-1]['original_pdf_pages'],[405])
  self.assertEqual(R[-1]['claim_kind'],'next_chapter_hunting_boundary')
  self.assertTrue(all(x['chapter']=='LII' for x in R[:-1]))
 def test_ids_and_nonacceptance(self):
  self.assertEqual(len(R),55)
  self.assertEqual(D['provisional_editorial_units'],55)
  self.assertEqual([x['record_number'] for x in R],list(range(3017,3072)))
  self.assertEqual(D['proposed_last'],3071)
  self.assertTrue(D['not_accepted'])
  self.assertEqual(D['empirical_validations'],D['runtime_promotions'])
  self.assertEqual(D['empirical_validations'],0)
  self.assertTrue(all(not r['accepted'] and r['historical_source_only'] and not r['case_evidence_countable'] and not r['runtime_promoted'] for r in R))
 def test_exact_two_page_seams(self):
  seams=[(x['claim_kind'],x['original_pdf_pages']) for x in R if len(x['original_pdf_pages'])>1]
  self.assertEqual(seams,[('cadent_partner_worse',[403,404]),('two_businesses_heading_cross_page',[404,405])])
 def test_count_original_headings_margin_converses(self):
  self.assertEqual(C['heading'],8)
  self.assertEqual(C['boundary'],1)
  self.assertEqual(C['margin'],1)
  self.assertEqual(C['converse'],3)
  self.assertTrue(all(x['source_anchor_editorially_normalized']=='& e contra' for x in R if x['role']=='converse'))
 def test_source_coverage_domains(self):
  roles=set(x['role'] for x in R)
  self.assertTrue({'law','partner_gain','partnership','friendship','removal','role','converse','heading','margin','boundary'}.issubset(roles))
  self.assertEqual(len({x['claim_kind'] for x in R}),55)
 def test_source_anchors_all_page_located(self):
  self.assertTrue(all(x['source_anchor_editorially_normalized'] and x['editorial_precondition_and_alternatives'] for x in R))
  self.assertTrue(all(set(x['original_pdf_pages']).issubset({403,404,405}) for x in R))
  self.assertTrue(all(x['original_printed_pages']==[p-34 for p in x['original_pdf_pages']] for x in R))
 def test_compound_party_roles_retained(self):
  kinds=set(x['claim_kind'] for x in R)
  for k in ['nonwar_house_precedence','war_exaltation_precedence','partner_finance_role_assignments','journey_origin_destination_role','first_lord_good_to_evil_do_not_go','l4_seventh_benefic_l1_l7_good_abide']:
   self.assertIn(k,kinds)
 def test_margin_separate_from_prediction(self):
  x=[x for x in R if x['role']=='margin']
  self.assertEqual(len(x),1)
  self.assertIn('NOT a prediction',x[0]['editorial_precondition_and_alternatives'])
 def test_all_thirteen_source_issues_preserved(self):
  self.assertEqual(len(U['issues']),13)
  self.assertEqual([x['id'] for x in U['issues']],[f'LII-U{i:02}' for i in range(1,14)])
  self.assertFalse(U['accepted'])
 def test_original_producer_preedit_frozen(self):
  old=json.loads((B/'recovery/SOURCE_FIRST_CLAUSES_INITIAL_20261015.json').read_text())
  old_ids=[r['record_number'] for r in old['rows']]
  self.assertEqual(len(old_ids),54)
  self.assertEqual(old_ids,list(range(3017,3071)))
  repair=json.loads((B/'SOURCE_FIRST_CORRECTION_RECEIPT.json').read_text())
  self.assertEqual(repair['before_edit_sha256'],hashlib.sha256((B/'recovery/SOURCE_FIRST_CLAUSES_INITIAL_20261015.json').read_bytes()).hexdigest())

if __name__=='__main__':
 unittest.main()
