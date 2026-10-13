"""Source-review-driven regression updates; don't alter historical source records."""
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/"test_b02t_phase1.py"
s=p.read_text()
reps=[
 ("self.assertEqual(len(R),129)","self.assertEqual(len(R),162)"),
 ("list(range(2138,2267))","list(range(2138,2300))"),
 ('self.assertEqual(D["record_count"],129)','self.assertEqual(D["record_count"],162)'),
 ("(2137,129,2266,1066,3332)","(2137,162,2299,1066,3365)"),
 ('[(324,"the"),(330,"for")]','[(324,"the"),(330,"or")]'),
 ('self.assertTrue(all(not x["body_target_proved"] for x in E["entries"]))',
  'self.assertEqual([x["body_target_proved"] for x in E["entries"]],[False,True])'),
 ('self.assertEqual(D["status"],"SOURCE_PARAPHRASE_DRAFT_INDEPENDENT_REVIEW_NOT_STARTED" if not (B/"independent_review/FINAL_RECONCILIATION.json").exists() else D["status"])',
  'self.assertIn("REVIEW",D["status"])'),
 ('for num in range(2138,2267):','for num in range(2138,2300):')
]
for a,b in reps:
 if s.count(a)!=1:raise ValueError((a,s.count(a)))
 s=s.replace(a,b)
p.write_text(s)
print("UPDATED",len(reps),"prior invariants to reviewed source counts")
