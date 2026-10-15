"""Guarded integration check: documentary-only B02w against accepted canonical predecessor."""
import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02w_CHAPTER_LI_COMPLETE.md'
idx=read(I)
old=read(B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02w_CANONICAL_20261015.json')
a=read(B/'ACCEPTANCE.json')
rec=read(B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json')
rules=read(B/'RULES.json')
u=read(B/'UNRESOLVED.json')

class CanonicalIndexSourceOnly(unittest.TestCase):
 def test_predecessor_exactly_preserved(self):
  self.assertEqual(old,read(B/'RETAINED_LILLY_INDEX_BEFORE_B02w.json'))
  self.assertEqual(old['records_count'],2974)
  self.assertEqual(old['batches'][-1]['id'],'B02v')
  self.assertEqual(idx['batches'][:-1],old['batches'])
 def test_nonduplicated_contiguous_canonical_inventory(self):
  self.assertEqual(idx['records_count'],3016)
  self.assertEqual(sum(b['records_count'] for b in idx['batches']),3016)
  self.assertEqual(idx['batches'][-1]['id'],'B02w')
  self.assertEqual(idx['batches'][-1]['records_count'],42)
  self.assertEqual(idx['batches'][-1]['sha256'],sha(B/'RULES.json'))
  self.assertEqual([x['record_number'] for x in rules['rules']],list(range(2975,3017)))
  self.assertEqual(idx['read_numbered_chapters'],list(range(1,52)))
 def test_next_chapter_boundary(self):
  self.assertEqual(idx['next']['chapter'],'LII')
  self.assertEqual((idx['next']['pdf_page'],idx['next']['printed_page']),(403,369))
  self.assertEqual(rules['rules'][-1]['source_record_role'],'boundary')
  self.assertEqual(rules['rules'][-1]['source_locator']['pdf_pages'],[403])
  self.assertTrue(all(403 not in x['source_locator']['pdf_pages'] for x in rules['rules'][:-1]))
 def test_documentary_claim_and_uncertainties(self):
  self.assertTrue(a['accepted'])
  self.assertEqual(len(u['issues']),11)
  self.assertEqual(a['literal_e_contra_count'],5)
  self.assertEqual(a['other_contrary_statement_count'],1)
  self.assertEqual(a['runtime_promotions'],0)
  self.assertFalse(rules['accepted_as_empirical_astro_prediction'])
  self.assertTrue(all(not r['independently_authenticated_outcome'] for r in rules['rules']))
  self.assertEqual(idx['runtime_promotions'],0)
  self.assertEqual(idx['empirical_validations'],0)
 def test_delivery_and_producer_hashes(self):
  self.assertEqual(sha(rec['archive_os_downloads']),rec['archive_sha256'])
  self.assertEqual(Path(rec['archive_os_downloads']).stat().st_size,rec['archive_bytes'])
  self.assertEqual(rec['extracted_original_source_test_count'],22)
  self.assertTrue(rec['zip_crc_pass'] and rec['per_file_sha256_pass'] and rec['actual_extraction_pass'])
  for fn,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('CLAIM_LEDGER.json','claim_ledger_sha256'),('INDEPENDENT_IMAGE_FIRST_REVIEW_20261015.md','audit_report_sha256'),('ORIGINAL_TO_RECORD_COVERAGE_V1.json','coverage_sha256')]:
   self.assertEqual(sha(B/fn),a[k])
 def test_state_prepend_only_and_recovery(self):
  former=(B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02w_20261015.md').read_bytes()
  now=CUR.read_bytes()
  self.assertTrue(now.endswith(former))
  self.assertEqual(now.count(former),1)
  self.assertIn('3,016',LATEST.read_text())
  self.assertIn('4,082',LATEST.read_text())

if __name__=='__main__':
 unittest.main()
