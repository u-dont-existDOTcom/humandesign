from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
schema=J("TABLE_PAGE_SOURCE_SCHEMA_20261017.json")
assert len(schema["table_pages"])==8 and schema["numeric_hours_all_cells_digitized"] is False
original_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==5629 and idx["batches"][-1]["id"]=="B04s" and idx["next"]["chapter"]=="PLANETARY_HOUR_TABLE"
rows=[];spans=[];img=[]
for r in schema["table_pages"]:
 n=r["original_pdf_page"]; p=B/"evidence"/f"pdf_1647-{n}.jpg"
 raw=p.read_bytes();sid=f"TABLE-S{len(spans)+1:03}"
 lid=f"TABLE-C{len(rows)+1:03}"
 hdr=r["solar_event"].replace("_"," ").lower()
 segment=r["time_block"].replace("_"," ").lower()
 meaning=f"Table leaf {r['table_page_number']} on original PDF{n} gives {hdr} and six printed {segment} clock boundaries for Sun position rows in {r['left_sun_positions']}; mirrored right-column solar signs appear in {r['right_sun_positions']}. All original numeric values are preserved as hashed scan, NOT fully machine-transcribed."
 rows.append({"batch":"B04t","source_local_id":lid,"source_span_id":sid,"kind":"TABLE_ORIGINAL_IMAGE_PAGE",
   "original_pdf_pages":[n],"original_table_leaf":r["table_page_number"],"printed_chapter":None,
   "historical_author_paraphrase":meaning,"source_table_semantics":r,
   "source_numeric_cells_fully_transcribed":False,
   "global_record_number":None,"historical_documentary_accepted":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":[n],"passage_label":f"Planetary hours table leaf {r['table_page_number']}", "mapped_local_ids":[lid]})
 img.append({"original_pdf_page":n,"table_leaf_number":r["table_page_number"],"path":p.relative_to(B).as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
n=516;f=B/"evidence/pdf_1647-516.jpg";raw=f.read_bytes()
img.append({"original_pdf_page":516,"table_leaf_number":None,"path":f.relative_to(B).as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
for kind,meaning in [
 ("NEXT_PRINTED_CHAPTER","Original PDF516 begins printed CHAP. XCVII, an explanatory method for the preceding table."),
 ("NEXT_CHAPTER_TOPIC","The following chapter assigns planetary rulership to each day and variable-length planetary hour. Its rules are not imported as verified numeric table data.")]:
 lid=f"TABLE-C{len(rows)+1:03}"
 rows.append({"batch":"B04t","source_local_id":lid,"source_span_id":"TABLE-S009","kind":kind,"original_pdf_pages":[516],
 "historical_author_paraphrase":meaning,"source_numeric_cells_fully_transcribed":False,
 "global_record_number":None,"historical_documentary_accepted":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
spans.append({"span_id":"TABLE-S009","original_pdf_pages":[516],"passage_label":"Next printed Chapter XCVII","mapped_local_ids":[rows[-2]["source_local_id"],rows[-1]["source_local_id"]]})
assert len(rows)==10 and len(spans)==9 and len(img)==9
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04t","status":"ORIGINAL_NUMERIC_TABLE_IMAGES_SOURCE_ANNOTATIONS_NOT_FULL_DIGITIZATION",
 "source_units":10,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04t","source_spans":spans,"span_count":9,"mapped_source_units":10})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04t","original_full_pdf_sha256":original_sha,"original_images":img,
 "original_body_pdf_pages":list(range(508,516)),"following_heading_pdf":516,
 "prior_lilly_accepted":5629,"next_global_record":5630,
 "machine_readable_numeric_table_values_complete":False,
 "original_image_table_page_witnesses_complete":True,
 "source_numeric_hour_boundary_cells_estimated":1488})
print(json.dumps({"batch":"B04t","draft_source_page_records":10,"page_images":9,"numeric_complete":False}))
