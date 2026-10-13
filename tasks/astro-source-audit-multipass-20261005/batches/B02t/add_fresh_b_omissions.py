"""Append six genuinely missing original printed clauses; source-only."""
import json,copy,shutil
from pathlib import Path
B=Path(__file__).resolve().parent
bk=B/"recovery/pre_fresh_B_six"
assert not (bk/"PHASE1_RULES_DRAFT.json").exists(),"already inserted"
bk.mkdir(parents=True,exist_ok=True)
for n in ["PHASE1_RULES_DRAFT.json","UNRESOLVED.json","COUNTS.json"]:shutil.copy2(B/n,bk/n)
p=B/"PHASE1_RULES_DRAFT.json";d=json.loads(p.read_text());a=d["rules"]
assert len(a)==162 and a[-1]["record_number"]==2299
items=[
("saturn_four_places_long_pound",[361,362],2227,"When sheep were stolen, SATURN in ASCENDANT, FOURTH, EIGHTH or TWELFTH is said to mean LONG IN POUND, with no separate Saturn-unfortunate premise."),
("news_moon_first_to_seventh",[363],2248,"MOON separating from FIRST LORD then joined immediately to SEVENTH LORD or SEVENTH HOUSE is said to bring NEWS of the fugitive."),
("distance_same_quadrant_town_hundred",[360],2211,"SIGNIFICATOR OF THING LOST, or MOON, in SAME QUADRANT means same TOWN OR HUNDRED as querent, a separate location rule."),
("airy_cadent_left_departure",[360,361],2218,"AIRY-sign SIXTH LORD CADENT means cattle on LEFT, GOING AWAY and STRAYING FURTHER from right owner, not necessarily west."),
("sixth_to_moon_good_bad",[362],2232,"SIXTH LORD beholding MOON or its DISPOSITOR by SEXTILE/TRINE signifies animals had again; by SQUARE/OPPOSITION stopped in VILLAGE OR TOWN."),
("unfortunate_twelve_lord_in_pound",[361],2225,"MOON unfortunate OR TWELFTH LORD and PRINCIPAL SIGNIFICATOR unfortunate signify cattle TO POUND or kept obscurely in close place.")
]
for kind,pages,after,s in items:
 n=2138+len(a);q=copy.deepcopy(a[0]);q.update(id=f"LI.1647.II.L.PHASE1.R{n}",record_number=n,source_record_kind=kind,source_statement=s,source_draft_part="FRESH_WINDOW_B_MISSING_SOURCE",source_order_after=after,source_review_inserted=True,preconditions=["Preserve printed house, planet, aspect and role conditions."],exceptions_and_evidence_limits=["Historical unvalidated source assertion only; not an observed person, animal or retrieval."])
 q["source_locator"]={"pdf_pages":pages,"printed_pages":[v-34 for v in pages],"page_images":[f"evidence/pdf-{v}.png" for v in pages],"source_statement_is_verbatim":False}
 a.append(q)
d["record_count"]=len(a);d["provisional_end"]=f"R{a[-1]['record_number']}";d["status"]="CORRECTED_PENDING_SOURCE_ACCEPTANCE"
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
print("SOURCE_UNITS",len(a),"LAST",a[-1]["record_number"])
