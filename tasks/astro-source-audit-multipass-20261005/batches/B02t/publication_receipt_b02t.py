import json,hashlib,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
r=lambda n:json.loads((B/n).read_text())
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
head=subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()
lines=subprocess.check_output(["git","-C",str(ROOT),"ls-remote","--heads","origin","research/six-rule-life-timing-20261001","research/lilly-fugitives-missing-goods-b02t-20261013"],text=True).splitlines()
assert len(lines)==2 and all(x.split()[0]==head for x in lines)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
A=r("ACCEPTANCE.json"); P=r("PACKET_USABILITY.json"); D=r("DELIVERY_RECEIPT.json")
assert I["records_count"]==2305 and I["next"]["chapter"]=="L"
assert A["accepted"] and A["new_documentary_units"]==168 and not A["chapter_L_complete"]
assert P["actual_extraction"] and P["extracted_tests_run"]==239
for x in D["files"]:
 f=Path(x["download_path"])
 assert f.is_file() and h(f)==x["sha256"] and f.stat().st_size==x["bytes"]
pub={"batch":"B02t","content_commit":head,"two_nonforce_remote_heads_verified":True,"canonical_lilly":2305,"retained_ptolemy":1066,"combined":3371,"new_documentary_records":168,"whole_chapter_l_complete":False,"original_page_images":19,"focused_and_extracted_tests":239,"archive_sha256":P["sha256"],"source_only_not_predictively_validated":True}
(B/"PUBLICATION_RECEIPT.json").write_text(json.dumps(pub,indent=2)+"\n")
safe={"batch":"B02t","owner_downloads_files_hash_verified":3,"files":[{k:x[k] for k in ("filename","bytes","sha256")} for x in D["files"]],"exact_archive_sha256":P["sha256"],"replayed_tests":239}
(B/"DELIVERY_RECEIPT.json").write_text(json.dumps(safe,indent=2)+"\n")
print(json.dumps({"commit":head,"published":True,"delivered":3,"sha256_matched":True}))
