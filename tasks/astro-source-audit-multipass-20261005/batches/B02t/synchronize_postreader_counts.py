"""Refresh source order, count metadata, and source-accurate tests after original readbacks."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
D=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text());rs=D["rules"]
assert len(rs)==168 and rs[-1]["record_number"]==2305
ids={r["record_number"] for r in rs};assert ids==set(range(2138,2306))
p=B/"SOURCE_ORDER.json";o=json.loads(p.read_text());a=o["ids"]
assert len(a)==162 and len(set(a))==162
for r in rs:
 n=r["record_number"]
 if n in a:continue
 anchor=r["source_order_after"]
 a.insert(a.index(anchor)+1,n)
assert len(a)==168 and set(a)==ids
p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
p=B/"COUNTS.json";c=json.loads(p.read_text());c.update(draft_source_units=168,candidate_lilly_after=2305,candidate_combined_after=3371);p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
p=B/"UNRESOLVED.json";u=json.loads(p.read_text())
assert u["retained_count"]==len(u["issues"])
for n,desc in [(51,"Later fresh reviewer A found omitted original Moon-house-lord, location and errata qualifications; all material source assertions were revised."),
(52,"Later fresh reviewer B corrected first/7th/Sun/Moon roles and distinct news versus remorse directions; the original claims remain untested."),
(53,"Original same-volume printed p330 erratum reads OR instead of FOR for three-day news/return line; printed witness remains unchanged."),
(54,"Additional source clauses on impounding, town/hundred, airy cadency and lunar aspects are counted once as source units, not independent outcomes."),
(55,"Later corrections still require semantic verification and a complete Chapter L extraction through PDF400, not merely PDF364."),
(56,"The post-correction readbacks were fresh original-image reviewers but preceded controller's latest fixes; deterministic green tests would not constitute a final independent rereview.")]:
 id=f"U{n:02d}"
 if id not in {x["id"] for x in u["issues"]}:u["issues"].append({"id":id,"description":desc,"status":"RETAINED"})
u["retained_count"]=len(u["issues"]);p.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
p=B/"test_b02t_phase1.py";s=p.read_text()
for old,new in [('len(R),162','len(R),168'),('range(2138,2300)','range(2138,2306)'),('"REVIEW",D["status"]','"PENDING",D["status"]')]:s=s.replace(old,new)
p.write_text(s)
p=B/"test_b02t_source_reader_fidelity.py";s=p.read_text()
s=s.replace('len(R),162','len(R),168').replace('len(set(A)),162','len(set(A)),168').replace('"retained_count"],50','"retained_count"],56')
s=s.replace('"eighth from the moon","radical eighth"','"eighth house from moon","radical eighth"')
s=s.replace('"mars aspects saturn"','"mars aspecting saturn"')
s=s.replace('self.assertIn("loss",t(2169))','self.assertIn("losing",t(2169))')
s=s.replace('self.assertIn("separating from ascendant lord",t(2248))','self.assertIn("separating from first lord",t(2301))')
s=s.replace('self.assertIn("seventh",t(2248))','self.assertIn("seventh",t(2301))')
s=s.replace('self.assertIn("separating from seventh lord",t(2239))','self.assertIn("separating from seventh lord",t(2248))')
s=s.replace('self.assertIn("entreat",t(2239))','self.assertIn("entreat",t(2248))')
s=s.replace('"upon good search"','"good search"')
s=s.replace('"read \'or\'"','"erratum"')
p.write_text(s)
print("SYNCHRONIZED",len(rs),"SOURCE_ORDER",len(a),"LIMITS",u["retained_count"])
