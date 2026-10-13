"""Build B02t first-phase source-cover and uncertainty records WITHOUT acceptance.

William Lilly 1647 chapter L is not complete until original PDF400 above LI.
All source paraphrases remain nonempirical and reference-only.
"""
import collections,hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def save(n,data):(B/n).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
D=rd("PHASE1_RULES_DRAFT.json")
R=D["rules"]
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert I["records_count"]==2137 and I["next"]["chapter"]=="L" and I["batches"][-1]["id"]=="B02s"
assert len(R)==D["record_count"]==129
assert R[0]["record_number"]==2138 and R[-1]["record_number"]==2266
assert [r["record_number"] for r in R]==list(range(2138,2267))
assert [r["source_locator"]["printed_pages"] for r in R]==[[p-34 for p in r["source_locator"]["pdf_pages"]] for r in R]
assert all(r["source_full_pdf_sha256"]==SRC for r in R)
assert all(not r["case_evidence_countable"] and not r["independently_authenticated_outcome"] and not r["prospective_blind_prediction"] and not r["clinical_or_criminal_inference_verified"] for r in R)
assert all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in R)
save("RETAINED_LILLY_INDEX_BEFORE.json",I)
save("SOURCE_IDENTITY.json",{
 "id":"LILLY1647_WELLCOME_B30338724",
 "author":"William Lilly","title":"Christian Astrology","publication_year":1647,
 "scan_provenance":"Wellcome b30338724 original; Archive.org original PDF", "original_pdf_sha256":SRC,
 "original_pdf_pages":894,"original_pdf_bytes":141842963,
 "full_chapter":"Book II Chapter L, Of Servants fled, Beasts strayed, and things lost",
 "chapter_start":"Original PDF353/printed319 below Chapter XLIX divider",
 "chapter_end":"Original PDF400/printed366 above Chapter LI divider",
 "this_phase":"PDF353 lower through PDF364 above Of a Thief and Theft; next phase begins PDF364 at heading",
 "first_phase_pages":list(range(353,365)),
 "next_phase_opening_source":"PDF364/printed330 Of a Thief and Theft",
 "next_numbered_chapter":"LI from original PDF400 below divider",
 "original_observed_patient_charts":0,
 "independent_validated_predictions":0,
 "clinical_or_criminal_validity":False})
slices=[
 (353, "Chapter L begins BELOW Marriage divider; Moon general significatrix for missing thing"),
 (354, "Moon's return/aspect, Moon house lord, position from zodiacal quarter, element, angular distance, house/town distance"),
 (355, "How Goods was Lost: separating first lord from seven traditional planets, special lost-beast setup"),
 (356, "Beast self-departed or taken, eighth-house death conditions, theft vs non-theft indications"),
 (357, "Return indicators and place/direction by houses, signs, Moon dispositors and term lords"),
 (358, "Continuation of eighth-house, success/position, Of Beasts or Strayes size/custody and sign locations"),
 (359, "Another Judgment: competing placement schemes, beasts stolen/dead/in pound, fortune and recovery"),
 (360, "Distance of thing from owner; stolen-versus-strayed by lunar dispositor; sixth lord directional correspondences"),
 (361, "Terrain signs for the beasts, term lord, shall cattle be impounded, illness/death in captivity"),
 (362, "Escape the pound; start Whether the Fugitive shall be taken: seventh/first relations"),
 (363, "Moon return/flight, capture and coercive return, first/seventh/well-dignified contacts"),
 (364, "Distance estimates seventeen/five/one furlongs by sign mode; woman leaving husband; before thief-and-theft heading only")
]
by=collections.defaultdict(list)
for r in R:
 for n in r["source_locator"]["pdf_pages"]:by[n].append(r["record_number"])
assert all(by[n] for n,_ in slices)
save("SECTION_COVERAGE.json",{
 "status":"DRAFT_UNDER_INDEPENDENT_SOURCE_REVIEW",
 "section_name":"Lilly Chapter L / phase 1, missing goods, strays, fugitives and return distance",
 "start_pdf_page":353,"start_position":"below XLIX divider",
 "last_pdf_page":364,"stop_position":"immediately ABOVE separate Of a Thief and Theft subsection heading",
 "full_lilly_chapter_l_complete":False,
 "next_phase_repeats_pdf364_from_heading":True,
 "all_12_first_phase_images_exist":all((B/"evidence"/f"pdf-{p}.png").is_file() for p in range(353,365)),
 "pages":[{"pdf_page":p,"printed_page":p-34,"coverage":description,
            "source_records":len(set(by[p])),
            "first_record":f"R{min(by[p])}","last_record":f"R{max(by[p])}"} for p,description in slices],
 "heading_boundary_records":["R2138","R2149","R2158","R2187","R2196","R2208","R2212","R2220","R2225","R2228","R2233","R2246","R2254","R2260","R2266"],
 "no_next_phase_theft_rules_admitted":True})
save("ERRATA_COLLATION.json",{
 "original_volume_errata_pdf_page":888,
 "scope":"Printed pages319–330 / original PDF353–364, extracted from same-volume selective errata only",
 "entries":[
  {"printed_page":324,"pdf_page":358,"printed_line_as_listed":10,
   "original_erratum":"p 324 l 10 r the","replacement":"the",
   "body_target_proved":False,"source_witness":"evidence/errata-888.png",
   "note":"Read the original source p324 image; exact original body word and printer line convention not definitively matched. Do not silently rewrite original."},
  {"printed_page":330,"pdf_page":364,"printed_line_as_listed":6,
   "original_erratum":"p 330 l 6 r for","replacement":"for",
   "body_target_proved":False,"source_witness":"evidence/errata-888.png",
   "note":"Original page has the fugitive-distance discussion; actual line target not identified, so retain erratum separately."}
 ],
 "count":2,"other_entries_for_printed_319_to_330_identified":0,
 "list_absence_limitation":"Printed volume gives a selective errata list, not proof of perfect text",
 "source_body_unmodified":True})
issues=[
("U01","Only one original 1647 Wellcome copy and its original errata examined; no independent manuscript or other edition collated."),
("U02","Chapter L as a whole is very long (original PDF353–400); B02t first phase is NOT a complete chapter."),
("U03","Twelve admitted pages end before Of a Thief and Theft at PDF364; same physical page is required in the next phase without double-counting."),
("U04","General Moon/first/second/seventh-twelfth significators vary by whether goods, beasts or fugitive humans are questioned; do not transfer signifiers arbitrarily."),
("U05","Moon's separating-planet indication concerns how something was lost; applying aspects have different prospective meanings."),
("U06","The original source's glyphs for planets, signs, Part of Fortune and lunar nodes can be unclear, especially in narrow 1450-pixel scans."),
("U07","Two errata (printed324 l10 'the', printed330 l6 'for') are legible but the exact body line target remains uncertain; no emendation made."),
("U08","The Moon's sign/house quarter rules include multiple directional schemes; they are NOT necessarily consistent and none is geolocation evidence."),
("U09","The zodiac categories common/movable/fixed can carry house, furlong, hill, field, prison and return-difficulty meanings in distinct passages; preserve local scope."),
("U10","A lost inanimate good, a four-footed beast, a strayed animal and a human fugitive are distinct source classes and should not be pooled as observed success."),
("U11","The source uses enslaved servants, thieves, suspected misconduct and coercive capture notions; these are historical testimonies, not current legal, ethical or policing methods."),
("U12","Animal death, starvation or captivity are unsupported historical divination outcomes, not animal health/veterinary evidence."),
("U13","Different passages allow Moon, Moon-house-lord, second lord or seventh lord as primary/alternate significators; exact fallback hierarchy may be ambiguous."),
("U14","In p321-322 'whether stolen' initially concerns cattle/strays, while p330 later begins a distinct theft subsection; preserve the two headings."),
("U15","No original source ephemeris/calendar worked chart data or independently authenticated lost property has been tested against these claims."),
("U16","Fugitive return can mean voluntary, regretful, forced, detained or captured; never collapse to one positive/negative outcome."),
("U17","The reported 3-day return/news claim has context and possible distance qualification; not universal three-day event."),
("U18","Distance method discusses at least two alternatives: seventh lord/hours lord angular degrees then Moon/significator; Lilly explicitly prefers the latter."),
("U19","17/5/1 furlongs or houses per degree for movable/common/fixed are approximate historical units, not calibrated modern miles or precise GPS."),
("U20","Text may describe degrees by quarter or 'one sign'/30/70/90 separation with overlapping interpretations and unclear bounds."),
("U21","Ownership, theft, motives, drunkenness, messenger, fear and morality are uncorroborated authorial speculations; not accusations."),
("U22","Some referenced ancient authors or source traditions in this chapter are not independently collated with their original texts."),
("U23","The author's 'Another Judgment' announces method variants potentially conflicting with earlier examples; do not silently unify."),
("U24","Astrological 'pound' means impounded cattle enclosure/custody, not currency unit or animal weight."),
("U25","Moon's derived house/term/part-of-fortune glyph locations require a separate fully specified question chart; no chart is calculated in this phase."),
("U26","The 1647 scan can contain printed mistakes and handwriting/annotations of uncertain provenance; later markings are not silently authorial."),
("U27","First-phase 129 candidate source records are documentary units, not 129 experiments, independently observed events or successful forecasts."),
("U28","No participant, synthetic test target, frozen prediction or decoder behavioral mapping has been modified or validated by these source additions."),
("U29","The chapter's eventual theft-focused source pages PDF364–400 are intentionally excluded from first-phase acceptance until separately source-read."),
("U30","Cumulative numbers 2137+129 are candidate only until review, verification, exact-head nonforce publication and owner delivery receipts.")
]
save("UNRESOLVED.json",{"batch":"B02t","phase":"1","retained_count":len(issues),
 "issues":[{"id":a,"description":b,"status":"RETAINED"} for a,b in issues]})
save("COUNTS.json",{
 "batch":"B02t","phase":"1","lilly_before":2137,"ptolemy_retained":1066,
 "draft_source_units":129,"candidate_lilly_after":2266,"candidate_combined_after":3332,
 "new_primary_source_cases":0,"new_human_records":0,"verified_outcomes":0,
 "frozen_predictions":0,"source_page_count":12,"original_page_context_images":7,
 "physical_images_including_errata":19,
 "all_chapter_l_complete":False,"source_only":True,
 "group_counts":dict(collections.Counter(r["source_record_kind"].split("_")[0] for r in R))})
print(json.dumps({"page_count":12,"records":129,"candidate_lilly":2266,"combined":3332,
 "open_issues":len(issues),"full_chapter_l_complete":False}))
