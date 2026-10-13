"""Source-bounded edits after the original-image-first B02r Opus review.

Preserve original draft in recovery, never silently modify the source images,
and keep every reviewer finding separately adjudicated. One-time operation:
refuse running again if frozen original snapshot exists.
"""
from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent
O=B/"recovery"/"original_draft"
assert not (O/"RULES.json").exists(), "One-time repair already invoked; inspect first."
O.mkdir(parents=True,exist_ok=True)
originals=["RULES.json","UNRESOLVED.json","SECTION_COVERAGE.json","AUDIT_REPORT.md",
           "CLAIM_LEDGER.json","TEST_RUN_SUMMARY.json","TEST_RUN.log",
           "SOURCE_FIRST_NOTES.md","WORKING_CHECKPOINT.md"]
for name in originals:
    shutil.copy2(B/name,O/name)
review=B/"independent_review"/"OPUS_INITIAL_DIAGNOSIS.md"
assert review.is_file() and hashlib.sha256(review.read_bytes()).hexdigest()=="76e1516b5ed919abde128f341f6286d13a5be56dc5a2c499c1f920278641bce0"
def rd(n):return json.loads((B/n).read_text())
def wr(n,data):(B/n).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
obj=rd("RULES.json")
rules={v["record_number"]:v for v in obj["rules"]}
assert list(rules)==list(range(1852,1921))
def fix(n,statement=None,pre=None,limit=None):
    r=rules[n]
    if statement is not None:r["source_statement"]=statement
    if pre is not None:r["preconditions"]=[pre]
    if limit is not None:r["exceptions_and_evidence_limits"]=[limit]
def caveat(n,s):
    if s not in rules[n]["exceptions_and_evidence_limits"]:
        rules[n]["exceptions_and_evidence_limits"].append(s)

# F1 high: original PDF335 reads "going to WARRE", not lunar "WANE".
fix(1907,
 "When the Moon is impeded, Lilly says there is delay or hindrance and 'seldome good end' to the inquiry. If the question is about going to WAR, he says to fear for the querent's life; for a journey, ill success; for marriage, an ill end of wooing.",
 "Moon impeded; war, journey and marriage are three separate kinds of question, not lunar-phase conditions.",
 "The source says going to WARRE, not a waning Moon; no independent harm, travel, clinical or relationship forecast is established.")

# F2 high: Moon MUST be part of mutual reception with Saturn/Mars.
fix(1882,
 "Saturn and Mars are said to bring delays through excessive cold and heat in their 'vertue and operation' (not literal physical coldness or dryness), unless THE MOON and Saturn/Mars mutually receive each other in the signification.",
 "Saturn or Mars influences the question; specific relief is mutual reception between the Moon and those planets, not merely any mutual reception between significators.",
 "The original explicitly reads 'unlesse the ☽ and they receive each other'; do not drop the Moon or turn the cold/heat symbolism into thermodynamics.")

# F3 high: accidental misclassification of UNFORTUNATE as MALefic by nature.
fix(1916,
 "For a marriage question, an UNFORTUNATE (afflicted) planet in the seventh is said to threaten ill agreement, UNLESS that same planet was a significator AT BIRTH.",
 "Seventh-house planet with source-defined unfortunate condition; the same planet's natal-significator role is an explicit exception.",
 "Unfortunate is a condition of a planet, not necessarily the natural malefic class 'infortunes'; no verified marriage prediction.")

# F4 medium: conflicting printed catchword at page turn.
fix(1896,
 "In general, Saturn or Mars in house, exaltation, or triplicity 'and Angles' are said to perform a desired matter despite their otherwise adverse character.",
 "The PDF334 running continuation reads 'and Angles', while a printed PDF333 catchword at the end of the prior page says 'or'; the exact conjunction of essential dignity and angularity is therefore source-qualified.",
 "The mismatch between printed catchword 'or' (p299) and next-body 'and Angles' (p300) is unresolved. The body phrase is kept, but do not silently force the condition into a certainty.")
# F5 medium: contradictory or/nor and direct angular prohibitions.
fix(1862,
 "The printed conditional on p296 reads 'or is in aspect with any Planet in an Angle', or with a planet beholding ascendant; the author later says some of these indicate freedom.",
 "The original prints 'or', but a reading equivalent to 'nor' is possible in light of the previous 'no aspect', and the later DIRECT angular-planet clause R1865 predicts NO release. Do not treat an angular aspect alone as deterministically sufficient.",
 "There is a source-level contradiction with R1865 for direct angular planets; the manuscript/errata do not resolve whether the first conjunction is a positive alternative or continuation of a negative condition.")
caveat(1865,"Cross-reference R1862: first paragraph's 'or' positive indication conflicts under some direct-angular configurations with this explicit no-release clause.")

# F6: Keep strange negative 'cast NOT any aspect'.
fix(1892,
 "When infortunes signify evil, Lilly asks whether fortunate Jupiter or Venus 'cast NOT any aspect unto them', then says the evil formerly intended is lessened; the ensuing 'do so when the Fortunes are Significators' is elliptical.",
 "The original p299 literally includes 'cast not any aspect', even though it seems at odds with a simple protective-aspect interpretation.",
 "Do not silently delete the NOT, reword it as favourable aspects, or fabricate a symmetric last clause. The printed logic is unresolved and must remain only source documentation.")
# F7: two examples under determinate question, not opposing types.
fix(1860,
 "Under what Lilly calls a 'determinate and not absolute' question, he offers BOTH asking to be freed from the current particular master's service and asking whether one shall ever be freed from that master's power.",
 "Both quoted questions are given as examples under the same determinate scope; 'absolute' is not separately defined on this page.",
 "The printed category labels remain historical and partially ambiguous; don't make these two examples opposing categories.")
# F8: entering combustion may not inherit all four-angle clause.
fix(1869,
 "The closing negative continues 'or if he is entring combustion', which Lilly says prevents the servant from being freed.",
 "The word 'he' refers in context to the ascendant lord, but whether the previous four-angle placement remains an essential precondition for entering combustion is unresolved.",
 "Entering combustion is a dynamic condition, not simply a planet currently combust. Scope of previous angular constraint is unsettled.")
# F9: retain BOTH harmed parties.
fix(1912,
 "Where an infortune aspects the significator and BOTH are peregrine, retrograde, cadent, or in signs contrary to their natures, the author expresses doubt about severe, perhaps unavoidable mischief under natural causes.",
 "The malefic and the desired significator are BOTH subject to the source's adverse-status checks; conjunction/disjunction among the four categories remains grammatically ambiguous.",
 "Source language is 'it may then be doubted' and 'according to natural causes', rather than a categorically inevitable forecast.")

# F10: repair narrower source terms and hedges.
fix(1884,
 "Where the fortunes are significators, Lilly instructs 'hope well'; where infortunes are significators, he says to fear the worst and govern one's conduct accordingly.",
 "Nature of main significator in a horary question.",
 "Source's 'hope well' is not a calibrated chance or an assured favourable result.")
fix(1857,
 "If the ascendant lord is separated by a few minutes from the tenth lord, Lilly calls it 'an argument' the servant is already 'as good as freed'.",
 "Recent separation of some few minutes between first-house lord and tenth lord.",
 "This is an authorial inference/argument, not evidence the person was actually freed.")
fix(1902,
 "A planet within TWELVE DEGREES of the Sun is under its beams and weak 'let it be in what Signe it will'; within SIXTEEN MINUTES of the Sun it is cazimi, in the Sun's heart, and said to be exceptionally strong.",
 "Two distinct angular thresholds: 12° under beams and 16 arcminutes for cazimi; the under-beams statement is independent of zodiac sign.",
 "Use the original 16-minute source wording rather than silently substituting another authorial threshold.")
fix(1919,
 "If the source's Dragon-Tail-like glyph occupies a given house, Lilly says beware men and things of that house; 'it seldome failes', he predicts damage, scandal or slander from house-associated people and matters.",
 "Printed glyph's house determines the associated domain.",
 "The author's strong 'seldome failes' certainty is a historical claim, not independent observed frequency.")
fix(1895,
 "A peregrine planet lacking essential dignity is said to be 'malicious beyond expression'; with essential dignity, less so. Lilly compares it to a noble person holding an enemy in his clutches but scornfully refusing to hurt him.",
 "Compare absence and presence of essential dignity in the relevant planetary significator.",
 "Historical analogy, not a verified diagnosis of a real person's moral disposition.")
fix(1889,
 "A retrograde planet or one in its FIRST station, if significator, 'denotes ill in the Question, discord and much contradiction'.",
 "Question significator either retrograde or at its first station.",
 "First station is distinct from second station and from slow direct motion.")
fix(1899,
 "A question's significator combust or in opposition to the Sun is said to 'signifie nothing of the matter, no good', and be unable to bring the thing to perfection.",
 "Combustion OR opposition with Sun, with that planet as question's significator.",
 "Not a rule about arbitrary non-significator Sun oppositions.")
fix(1906,
 "If the ascendant degree or significator position is the place of an eclipse at hand, the matter is said to receive prejudice 'when least is expected' and 'hardly be concluded', even though otherwise in a fair way to completion.",
 "The eclipse must concern the current ascendant degree or significator's zodiac location.",
 "This is a source's unexpected-impediment claim; no modern eclipse forecast or observed outcome.")
fix(1881,
 "Give particular regard to Moon's strength or debility. Lilly prefers an unfortunate ascendant lord over an unfortunate Moon because the Moon allegedly conveys the virtue and strength of other planets from one planet to another.",
 "Moon and ascendant lord are two distinct significators; the Moon is described as a transmitter BETWEEN planets.",
 "Source metaphysics, not independent evidence of transmission or quantitative strength.")
fix(1887,
 "Moon's application signifies the present matter; when SHE (the Moon) applies by a good aspect FROM a good house TO a good planet, Lilly describes strong hopes of the desired outcome.",
 "Moon herself is in a good house AND applies through favourable aspect to a good planet.",
 "Do not shift the Moon's 'in a good house' requirement onto the receiving planet.")
fix(1900,
 "One infortune 'joyned to another': a favourable signification from their aspect is said to come to nothing, whereas adverse signification may occur with worse malice.",
 "Two infortunes joined by the source's broad joining/aspect language, not necessarily only bodily conjunction.",
 "Bad outcome is stated as probable; no verified actual event or modern probability.")
fix(1872,
 "The seventh-house heading names marriage, open enemies, lawsuits, controversies, contracts, wars, bargains, fugitives and thefts, followed by '&c.' indicating an open-ended source topic list.",
 "Original seventh-house introduction and its examples.",
 "Do not treat the nine named topics as an exhaustive modern legal or social taxonomy.")
fix(1875,
 "The author announces forty-three significant aphorisms, which 'if well understood' are said to illuminate both seventh-house inquiries and the whole body of astrology.",
 "Benefit is explicitly qualified by the reader's correct understanding; application is wider than seventh-house questions.",
 "These are forty-three GENERAL horary aphorisms, distinct from the earlier physician forty-three already indexed in Lilly XLIV.")

wr("RULES.json",obj)
# Additional uncertainty tracker: preserve existing IDs, update changed ones only.
U=rd("UNRESOLVED.json"); m={x["id"]:x for x in U["limits"]}
m["U04"]["description"]="Source groups TWO questions under 'determinate and not absolute'; no separate definition of absolute is provided. Do not reclassify one example as absolute."
m["U06"]["description"]="R1865 direct vs retrograde angular-planet outcomes depend on earlier named significators; R1862 prints an earlier 'or' favourable aspect that may collide, so cross-reference both clauses."
m["U08"]["description"]="Entering combustion is distinct from combust; the source's 'or if he is entring combustion' may or may not inherit the angular-location condition."
m["U15"]["description"]="Saturn/Mars cold/heat refer to operation/virtue; aphorism6's exception expressly requires the MOON and Saturn/Mars receiving each other."
m["U17"]["description"]="Aphorism16 literally prints 'cast not any aspect unto them' followed by mitigation of evil; paradox with aspect-benefit expectations is unresolved. Its 'do so when the Fortunes are Significators' is also elliptical."
m["U18"]["description"]="Aphorism20 page join: PDF333/printed299 CATCHWORD 'or' conflicts with next PDF334/printed300 BODY reading 'and Angles'. The latter is retained, but conjunctive condition is not fully settled. Source says IN angles, not near."
m["U28"]["description"]="Aphorism40 says an UNFORTUNATE planet in seventh, which may describe planetary affliction/condition rather than only natural malefics; natal-significator exception still applies."
add=[
 ("U36","R1862 original 'or is in aspect with any Planet in an Angle' could be an affirmative alternative OR, or a copy error for nor continuing 'no aspect'. Positive reading potentially contradicts R1865 direct-angular denial; no resolution."),
 ("U37","Aphorism31 text says 'going to WARRE', not the Moon's waning phase. Original draft incorrectly interpreted this; correction has been source-bound and regression protected."),
 ("U38","Aphorism16 contains source-negative 'cast NOT any aspect' even where favourable mitigation is claimed. Preserve the literal negative rather than silently rewriting it."),
 ("U39","Source aphorism20 printed cue-word 'or' (PDF333) does not match next body 'and Angles' (PDF334), a copy-level conflict; no original-volume erratum applied to these printed pages."),
]
for id,desc in add:
 assert id not in m
 U["limits"].append({"id":id,"description":desc,"status":"RETAINED"})
U["retained_count"]=len(U["limits"])
assert U["retained_count"]==39
wr("UNRESOLVED.json",U)
# Derive exact per-page record coverage from admitted pages rather than off-by-one approximate ranges.
C=rd("SECTION_COVERAGE.json")
for row in C["partitions"]:
 pg=row["pdf_page"]
 hits=[r["record_number"] for r in obj["rules"] if pg in r["source_locator"]["pdf_pages"]]
 if hits:
  row["first_source_record"]=f"R{min(hits)}"
  row["last_source_record"]=f"R{max(hits)}"
  row["exact_source_record_count"]=len(hits)
  row.pop("approx_first_record",None)
  row.pop("approx_last_record",None)
 else:
  row["first_source_record"]=None;row["last_source_record"]=None;row["exact_source_record_count"]=0
  row.pop("approx_first_record",None);row.pop("approx_last_record",None)
wr("SECTION_COVERAGE.json",C)
print(json.dumps({"records":len(obj["rules"]),"repaired_records":23,
                  "open_uncertainties":U["retained_count"],"exact_pages":len(C["partitions"])}))
