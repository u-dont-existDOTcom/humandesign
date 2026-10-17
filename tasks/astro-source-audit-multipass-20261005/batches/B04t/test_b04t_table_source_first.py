import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
S=J("TABLE_PAGE_SOURCE_SCHEMA_20261017.json")
def check(rows,spans):
 assert len(rows)==10 and len(spans)==9
 assert [r["source_local_id"] for r in rows]==[f"TABLE-C{i:03}" for i in range(1,11)]
 ids=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==10
 assert set(ids)=={r["source_local_id"] for r in rows}
 assert [r["kind"] for r in rows[:8]]==["TABLE_ORIGINAL_IMAGE_PAGE"]*8
 assert rows[8]["kind"]=="NEXT_PRINTED_CHAPTER"
 assert all(not r["source_numeric_cells_fully_transcribed"] and not r["empirically_validated_prediction"] for r in rows)
class Source(unittest.TestCase):
 def test_complete_page_mapping(self):check(D,M)
 def test_exact_original_scan_hashes(self):
  self.assertEqual([w["original_pdf_page"] for w in W["original_images"]],list(range(508,517)))
  for w in W["original_images"]:
   p=B/w["path"];v=p.read_bytes()
   self.assertEqual(w["bytes"],len(v))
   self.assertEqual(w["sha256"],hashlib.sha256(v).hexdigest())
 def test_all_pages_numeric_incomplete(self):
  self.assertFalse(S["numeric_hours_all_cells_digitized"])
  self.assertEqual(S["physical_numeric_hour_cells_estimated"],8*31*6)
  self.assertTrue(W["original_image_table_page_witnesses_complete"])
  self.assertFalse(W["machine_readable_numeric_table_values_complete"])
 def test_first_row_boundary_labels(self):
  for r in S["table_pages"]:
   first=r["single_table_row_first_equinoctial_anchor"]
   self.assertEqual(first["solar_event_clock"],"6:00")
   time=r["time_block"]
   want="7:00" if time in ("DAY_BEFORE_NOON","NIGHT_BEFORE_MIDNIGHT") else "1:00"
   self.assertEqual(first["reported_hour_boundaries_hhmm"][0],want)
   self.assertEqual(len(first["reported_hour_boundaries_hhmm"]),6)
 def test_exact_table_four_day_four_night_blocks(self):
  self.assertEqual(len([r for r in S["table_pages"] if r["solar_event"]=="SUN_RISING"]),4)
  self.assertEqual(len([r for r in S["table_pages"] if r["solar_event"]=="SUN_SETTING"]),4)
  self.assertEqual([r["table_page_number"] for r in S["table_pages"]],list(range(1,9)))
 def test_parent_still_esex(self):
  self.assertEqual(W["prior_lilly_accepted"],5629)
  self.assertEqual(W["next_global_record"],5630)
  self.assertEqual(W["following_heading_pdf"],516)
 def test_mutant_duplicate_mapping_fails(self):
  x=copy.deepcopy(M);x[0]["mapped_local_ids"].append(x[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,x)
 def test_mutant_false_numeric_completion_fails(self):
  x=copy.deepcopy(D);x[0]["source_numeric_cells_fully_transcribed"]=True
  with self.assertRaises(AssertionError):check(x,M)
if __name__=="__main__":unittest.main(verbosity=2)
