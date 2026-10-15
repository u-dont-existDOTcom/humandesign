"""Non-empirical Chapter LII canonical-index integration tests."""
import unittest,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
S=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
idx=J(ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json')
old=J(B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02x_CANONICAL.json')
r=J(B/'RULES.json');a=J(B/'ACCEPTANCE.json')
u=J(B/'UNRESOLVED.json'); rel=J(B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json')
class AcceptedLIIIndex(unittest.TestCase):
 def test_predecessor_complete_bitwise_retention(self):
  self.assertEqual(old,J(B/'RETAINED_CANONICAL_LILLY_INDEX_BEFORE_B02x.json'))
  self.assertEqual(idx['batches'][:-1],old['batches'])
  self.assertEqual((old['records_count'],old['batches'][-1]['id']),(3016,'B02w'))
 def test_new_canonical_count_chapter_chain(self):
  self.assertEqual(idx['records_count'],3071)
  self.assertEqual(sum(x['records_count'] for x in idx['batches']),3071)
  self.assertEqual(idx['read_numbered_chapters'],list(range(1,53)))
  self.assertEqual((idx['batches'][-1]['id'],idx['batches'][-1]['records_count']),('B02x',55))
  self.assertEqual(idx['batches'][-1]['sha256'],S(B/'RULES.json'))
 def test_legal_chapter_closed_next_hunting_physical_boundary(self):
  self.assertEqual((idx['next']['chapter'],idx['next']['pdf_page'],idx['next']['printed_page']),('LIII',405,371))
  self.assertIn('BELOW horizontal divider',idx['next']['position'])
  self.assertEqual(r['rules'][-1]['claim_kind'],'next_chapter_hunting_boundary')
  self.assertEqual(r['rules'][-1]['original_pdf_pages'],[405])
  self.assertTrue(all(x['chapter']=='LII' for x in r['rules'][:-1]))
 def test_source_only_and_retained_ambiguities(self):
  self.assertTrue(a['documentary_accepted_locally'])
  self.assertTrue(a['whole_chapter_lii_complete_at_documentary_source_level'])
  self.assertEqual(a['new_documentary_records'],r['record_count'])
  self.assertEqual(a['source_uncertainties_retained'],len(u['issues']))
  self.assertEqual(len(u['issues']),13)
  self.assertEqual(idx['empirical_validations'],idx['runtime_promotions'])
  self.assertEqual(idx['runtime_promotions'],0)
  self.assertTrue(all(not x['empirical_accuracy_verified'] and not x['runtime_promoted'] for x in r['rules']))
  self.assertFalse(r['accepted_as_empirical_astro_prediction'])
 def test_archive_real_extraction_staging(self):
  self.assertEqual(S(rel['archive_os_downloads']),rel['archive_sha256'])
  self.assertTrue(rel['crc_pass'] and rel['member_sha256_pass'] and rel['extracted_file_sha256_pass'])
  self.assertEqual(rel['extracted_source_tests_exit_code'],0)
  self.assertEqual(rel['extracted_focused_source_test_count'],20)
  for fn,key in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('CLAIM_LEDGER.json','claim_ledger_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256')]:
   self.assertEqual(S(B/fn),a[key],fn)
 def test_state_prepend_did_not_rewrite_prior_history(self):
  current=(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md').read_bytes()
  old=(B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02x.md').read_bytes()
  self.assertTrue(current.endswith(old))
  latest=(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02x_CHAPTER_LII_COMPLETE.md').read_text()
  self.assertIn('3,071',latest)
  self.assertIn('4,137',latest)
if __name__=='__main__':unittest.main()
