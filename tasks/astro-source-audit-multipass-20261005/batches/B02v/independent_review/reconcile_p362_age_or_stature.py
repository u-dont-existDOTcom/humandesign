"""One-time original-page-362 source correction, no empirical promotion.

R2871 omitted thief significator as OR alternative; R2876 conflated
two explicitly disjunct stature tests into a conjunction.
Freeze exact producer JSON before changing these two source units.
"""
from pathlib import Path
import hashlib, json

B=Path(__file__).resolve().parents[1]
src=B/"PRODUCER_SOURCE_DRAFT_P396_397.json"
back=B/"recovery/producer_p396_397_pre_U59_U60_20261015.json"
assert not back.exists(),"U59/U60 correction already attempted; inspect frozen source."
original=src.read_bytes()
doc=json.loads(original)
by={x["local_id"]:x for x in doc["units"]}
age=by["P396C014"]
stature=by["P396C019"]
assert age["pdf_pages"]==stature["pdf_pages"]==[396]
assert age["kind"]=="age_applying_planet"
assert age["source_statement"]=="A further method compares the age implied by the planet to which Moon applies."
assert stature["kind"]=="stature_small_occidental_signs"
assert stature["source_statement"]=="A significator with much occidentality in Cancer, Scorpio or Pisces is assigned smaller stature."

age["kind"]="age_moon_applying_planet_or_thief_significator"
age["source_statement"]="Lilly offers the age of the planet to which Moon applies, OR the age of the thief's significator, as alternative age-estimation testimonies."
age["preconditions"]=["A Moon-applying planet OR the separately chosen thief significator may provide the age testimony; neither is necessarily the other."]
age["exceptions_and_uncertainty"]=["Two textual alternatives, not a requirement that the Moon apply to the thief's significator; historical age taxonomy has no verified demographic accuracy."]
age["printed_source_anchor"]="Or see the age of the Planet to whom the Moon applyes, or the Significator of the Thief"

stature["kind"]="stature_small_occidental_or_water_signs"
stature["source_statement"]="Lilly assigns a smaller bodily proportion if the significator has much occidentality, OR if it is in Cancer, Scorpio or Pisces: distinct alternative tests."
stature["preconditions"]=["Either significant occidentality OR significator in one of Cancer/Scorpio/Pisces; the printed grammar says OR, not AND."]
stature["exceptions_and_uncertainty"]=["The earlier producer incorrectly required both occidentality and a water sign. Scorpio also appears in the large-proportion list under a different conjunction; no empirical measurement is established."]
stature["printed_source_anchor"]="Proportion little, if his Occidentality be much, or the Significator in"

ledgerpath=B/"UNRESOLVED_DRAFT.json"
ledger=json.loads(ledgerpath.read_text())
assert ledger["retained_count"]==58 and len(ledger["issues"])==58
assert not {"U59","U60"}.intersection({x["id"] for x in ledger["issues"]})
ledger["issues"].extend([
 {"id":"U59","status":"SOURCE_IMAGE_CORRECTION_RETAINED","description":"Original PDF396/printed362 age alternatives: use age of Moon-applying planet OR thief significator. Earlier R2871 omitted the second alternative. Restored without treating it as an observed age."},
 {"id":"U60","status":"SOURCE_BOOLEAN_OPERATOR_CORRECTION_RETAINED","description":"Original PDF396/printed362 small stature: significator high occidentality OR one of Cancer/Scorpio/Pisces. Earlier R2876 erroneously made both conditions conjunctive. Corrected disjunction."}
])
ledger["retained_count"]=len(ledger["issues"])
back.parent.mkdir(parents=True,exist_ok=True)
back.write_bytes(original)
src.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
ledgerpath.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"corrected":["R2871","R2876"],"source_pdf_page":396,"original_sha256":hashlib.sha256(original).hexdigest(),"current_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"issues":ledger["retained_count"],"new_accepted":0},indent=2))
