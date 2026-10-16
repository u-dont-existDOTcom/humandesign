import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03m_CHAPTER_LXVII_COMPLETE.md"
I=J(IDX)
A=J(B/"ACCEPTANCE.json")
R=J(B/"RULES.json")
P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Canonical(unittest.TestCase):
    def test_untouched_original_predecessor(self):
        older=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03m_CANONICAL.json"
        self.assertEqual(H(older),P["previous_index_sha256"])
        p=J(older)
        self.assertEqual(p["records_count"],3746)
        self.assertEqual(p["batches"][-1]["id"],"B03l")
        self.assertEqual(p["next"]["chapter"],"LXVII")
        self.assertEqual(p["source_sha256"],I["source_sha256"])
    def test_source_only_contiguous_append(self):
        self.assertEqual(I["records_count"],3932)
        self.assertEqual(sum(x["records_count"] for x in I["batches"]),3932)
        self.assertEqual(I["read_numbered_chapters"],list(range(1,68)))
        self.assertEqual(I["batches"][-1]["id"],"B03m")
        self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
        self.assertEqual(I["batches"][-1]["records_count"],186)
        self.assertEqual([r["record_number"] for r in R["rules"]],list(range(3747,3933)))
    def test_next_original_boundary(self):
        self.assertEqual(I["next"]["chapter"],"LXVIII")
        self.assertEqual(I["next"]["pdf_page"],446)
        self.assertEqual(I["next"]["printed_page"],412)
        self.assertTrue(all(r["chapter"]=="LXVIII_NAVIGATION_ONLY" for r in R["rules"][-2:]))
    def test_no_person_cases_or_model_promotions(self):
        self.assertEqual(I["empirical_validations"],0)
        self.assertEqual(I["runtime_promotions"],0)
        self.assertEqual(R["independent_absent_person_return_outcomes"],0)
        self.assertEqual(R["independent_medical_cause_of_death_outcomes"],0)
        self.assertFalse(R["allowed_for_real_person_prediction"])
    def test_exact_state_and_archive_hashes(self):
        self.assertEqual(H(IDX),P["new_index_sha256"])
        self.assertEqual(H(CUR),P["new_current_state_sha256"])
        self.assertEqual(H(LATEST),P["new_latest_source_state_sha256"])
        z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
        self.assertEqual(H(z["owner_os_download_path"]),P["accepted_owner_archive_zip_sha256"])
        self.assertEqual(z["extracted_source_tests_passed"],25)
        self.assertEqual(z["extracted_test_exit_code"],0)
        self.assertFalse(P["remotely_published"])
if __name__=="__main__":unittest.main(verbosity=2)
