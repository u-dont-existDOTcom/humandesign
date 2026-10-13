from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
def read(x):return json.loads((B/x).read_text())
def put(x,v):(B/x).write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n")
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
R=read("RULES.json")["rules"]
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert I["records_count"]==1920 and I["next"]["chapter"]=="XLIX"
assert [x["record_number"] for x in R]==list(range(1921,1921+len(R)))
put("RETAINED_LILLY_INDEX_BEFORE.json",I)
s="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
put("SOURCE_IDENTITY.json",{"author":"William Lilly","work":"Christian Astrology","year":1647,"pdf_pages":894,"original_pdf_sha256":s,"original_pdf_bytes":141842963,"page_scope":[336,353],"printed_scope":[302,319],"next_chapter":"L","verified_outcomes":0})
z=[]
for n in [*range(336,354),888]:
 f="errata-888.png" if n==888 else f"pdf-{n}.png";p=B/"evidence"/f
 assert p.is_file(),p
 z.append({"pdf_page":n,"path":"evidence/"+f,"sha256":sha(p),"bytes":p.stat().st_size})
put("SOURCE_IMAGE_MANIFEST.json",{"original_sha256":s,"content_pages":list(range(336,354)),"images":z})
pages=[{"pdf_page":n,"printed_page":n-34,"records":[x["id"] for x in R if n in x["source_locator"]["pdf_pages"]]} for n in range(336,354)]
assert all(p["records"] for p in pages)
put("SECTION_COVERAGE.json",{"start":"PDF336 below divider","end":"PDF353 above divider","pages":pages,"all_pages_present":True,"chapter_L_excluded":True})
put("COUNTS.json",{"batch":"B02s","lilly_before":1920,"records":len(R),"lilly_if_accepted":1920+len(R),"ptolemy_retained":1066,"combined_if_accepted":2986+len(R),"verified_couple_outcomes":0,"frozen_predictions":0,"runtime_promotions":0,"empirical_validation":False})
print("SUPPORT",len(R),len(z))
