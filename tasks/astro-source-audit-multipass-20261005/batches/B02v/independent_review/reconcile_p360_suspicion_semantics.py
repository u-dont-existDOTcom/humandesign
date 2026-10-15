"""One-time original-1647 witness correction, printed p360/PDF394.

The original source makes an ill-planet-reception accusation conditional,
and uses the ambiguous phrase 'truth is said of him' about a configuration.
Do NOT interpret that phrase as a demonstrated honesty claim.
All source claims are unverified historical astrology, not real accusations.
"""
from pathlib import Path
import json, hashlib

B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P393_395.json"
FROZEN=B/"recovery/producer_p393_395_before_20261015_U61_U63_p360.json"
assert not FROZEN.exists(), "Already attempted: compare existing original backup"
original=SRC.read_bytes()
doc=json.loads(original)
by={x["local_id"]:x for x in doc["units"]}
a,b,c=(by[x] for x in ("P393C035","P393C036","P393C037"))
assert [x["pdf_pages"] for x in (a,b,c)]==[[394],[394],[394]]
assert a["kind"]=="most_strength_first_moon_ill_from"
assert b["kind"]=="first_angular_to_cadent_truth_claim"
assert c["kind"]=="moon_angular_conjunction_truth"
assert a["source_statement"]=="Lilly asks reader to compare strength of first lord and Moon and any virtue received/separated from evil planets to decide who acted."
assert b["source_statement"]=="Ascendant lord angular applying or separating to a planet in cadent house is said to tell truth about the theft."
assert c["source_statement"]=="Moon joined to an angular planet, especially in tenth, is offered as parallel truthfulness testimony."

a["kind"]="suspect_stronger_lord1_moon_separation_evil_conditional"
a["source_statement"]="Under the historical suspicion inquiry, Lilly compares the first-house lord and Moon, takes the stronger, and *conditionally* alleges involvement if that significator has received 'vertue' from an evil planet, glossed by separation from it; receipt from the second-house lord is a further strengthening qualifier."
a["preconditions"]=["Compare strength of first-house lord and Moon and select stronger; that selected significator has received virtue from evil planet(s), 'viz. separated from them' in original PDF394/printed360."]
a["exceptions_and_uncertainty"]=["The claimed conclusion is that the selected significator's represented party 'hath played the Thiefe', with stronger assertion when virtue was received from lord of second. This is historical astrology, not verified culpability or a usable investigative method.","Whether 'received virtue' indicates technical reception or transfer of virtue needs independent philological and astrological-context review; do not manufacture a calculable recipe."]
a["original_page_anchor"]="who if he have received any vertue from evill Planets, viz. separated from them, he hath played the Thiefe"

b["kind"]="first_angular_cadent_truth_said_ambiguous_referent"
b["source_statement"]="Lilly states that the first lord in an angle, applying to or separating from a planet in a cadent house, yields the printed consequence 'truth is said of him'; the meaning of 'truth' in this suspicion passage is not specified as honest speech."
b["preconditions"]=["First lord in an angle AND applying/separating with a planet in a cadent house, as in original PDF394/printed360."]
b["exceptions_and_uncertainty"]=["The author says 'truth is said of him' without explicitly stating that the person tells the truth. Whether this evaluates a suspicion, accusation, or another attribution remains unresolved; do not replace it with a character assessment."]
b["original_page_anchor"]="Lord of the ascendant in an angle, applying or separating to a Planet in a cadent house, truth is said of him"

c["kind"]="moon_angular_joins_same_ambiguous_truth_consequent"
c["source_statement"]="The Moon joined to a planet in an angle, especially in the tenth, is said to 'signifie the same' as the preceding first-lord/angular-cadent 'truth is said of him' clause, whose precise referent remains unresolved."
c["preconditions"]=["Moon joined to a planet in an angle, particularly the tenth; source links to the immediately preceding clause rather than independently defining the outcome."]
c["exceptions_and_uncertainty"]=["Preserve the author's cross-reference and unresolved 'truth is said of him' semantics; it does not independently establish truthful testimony or real-world guilt."]
c["original_page_anchor"]="or ☽ conjoyned to a Planet in an angle, especially in the tenth, signifies the same"

issues_path=B/"UNRESOLVED_DRAFT.json"
issues=json.loads(issues_path.read_text())
assert issues["retained_count"]==60 and len(issues["issues"])==60
assert not {x["id"] for x in issues["issues"]}.intersection({"U61","U62","U63"})
issues["issues"].extend([
 {"id":"U61","status":"SOURCE_IMAGE_CONSEQUENT_AND_ANTECEDENT_CORRECTED","description":"Printed p360 R2828: compare lord1 and Moon, stronger receiving virtue from evil planet(s) by separation gives authorial conditional accusation; further second-lord qualification. Earlier draft omitted explicit antecedent and alleged consequent. No real accusation supported."},
 {"id":"U62","status":"SOURCE_SEMANTIC_AMBIGUITY_RETAINED","description":"Printed p360 R2829 says 'truth is said of him' after first lord angular applying/separating cadent planet. Earlier draft reinterpreted as person telling truth; now preserved literal expression and unresolved referent."},
 {"id":"U63","status":"SOURCE_CROSS_REFERENCE_AMBIGUITY_RETAINED","description":"Printed p360 R2830 says Moon joined to angular planet, especially tenth, 'signifies the same' as R2829. Previous draft asserted truthfulness, now preserves ambiguous cross-reference."}
])
issues["retained_count"]=len(issues["issues"])
FROZEN.parent.mkdir(parents=True,exist_ok=True)
FROZEN.write_bytes(original)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
issues_path.write_text(json.dumps(issues,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"source_page":"PDF394/printed360","changed_record_ids":[2828,2829,2830],"original_producer_sha256":hashlib.sha256(original).hexdigest(),"corrected_producer_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issues":issues["retained_count"],"newly_accepted":0},indent=2))
