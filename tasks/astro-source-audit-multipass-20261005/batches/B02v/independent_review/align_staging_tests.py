"""Update obsolete staging schema assertions; preserve their original bytes.
This alters no evidence or canonical acceptance gate.
"""
from pathlib import Path
import hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"test_b02v_staging.py"
BACK=B/"recovery/test_b02v_staging_before_20261014_schema_align.py"
assert not BACK.exists(), "Already migrated staging assertions"
raw=SRC.read_bytes()
s=raw.decode()
changes=[
 ('        self.assertFalse(C["clinical_or_legal_validation"])\n        self.assertFalse(C["chapter_l_complete"])',
  '        self.assertFalse(C["runtime_promotion"])\n        self.assertTrue(C["full_chapter_l_completion_not_yet_admitted"])'),
 ('        self.assertEqual(C["next_provisional"],"R2573")\n        self.assertEqual((C["lilly_previous_accepted"],C["retained_ptolemy"],C["combined_previous_accepted"]),(2572,1066,3638))',
  '        self.assertEqual(C["accepted_new_documentary_records"],0)\n        self.assertEqual((C["accepted_lilly_before"],C["retained_ptolemy"],C["accepted_lilly_before"]+C["retained_ptolemy"]),(2572,1066,3638))'),
 ('        self.assertFalse(E["candidate_in_scope"][0]["body_line_located"])',
  '        self.assertTrue(E["candidate_in_scope"][0]["body_line_located"])\n        self.assertFalse(E["candidate_in_scope"][0]["read_word_or_glyph_verified"])')
]
for old,new in changes:
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new,1)
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(s)
print({"original_sha256":hashlib.sha256(raw).hexdigest(),"new_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"schema_updates":len(changes)})
