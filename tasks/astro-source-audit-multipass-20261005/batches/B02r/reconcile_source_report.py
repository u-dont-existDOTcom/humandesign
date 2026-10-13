"""Update B02r documentary report after an original-image independent source review.

Must be run after reconcile_independent_source.py. Replaces only spans
recorded in the original report and documents all material corrections.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
original=B/"recovery"/"original_draft"/"AUDIT_REPORT.md"
assert original.is_file()
report=original.read_text()
def replace(before,after):
 global report
 if before not in report:
  raise AssertionError("Missing original span: "+before[:140])
 report=report.replace(before,after)
replace(
 "An exact conjunction **by degree and minute** means quick, easy freedom in the source; separation by a few minutes suggests it is virtually accomplished already.",
 "An exact conjunction **by degree and minute** means quick, easy freedom in the source; separation by a few minutes is only **'an argument'** the person is **'as good as freed already'**, not a recorded liberation."
)
replace(
 "Next Lilly contrasts what he calls a **determinate and not absolute** question, exemplifying freedom from this particular current master and freedom from the master's power.",
 "Next Lilly gives **two examples under the same 'determinate and not absolute'** question: release from this present master and release from his power at any time. The text does not separately define an absolute question."
)
replace(
 "The ascendant lord **cadent from an angle and without aspect to the ascendant**, or in aspect to a planet **in an angle** or to a planet **beholding the ascendant**, or in **third/ninth** (or joined to a planet there), supplies separate conditional routes he associates with departure.",
 "The ascendant lord **cadent from an angle and without aspect to ascendant**, or the printed alternative **'or is in aspect with any Planet in an Angle'**, or to a planet beholding ascendant, or in **third/ninth** (or joined to a planet there), appears in his freedom examples. However, the **'or'** might continue the earlier **'no aspect'** as **'nor'**; interpreted positively, it may also conflict with the subsequent no-release prediction for a **direct** angular planet. R1862 therefore records this **unresolved textual contradiction** instead of treating the angular aspect alone as a reliable positive rule."
)
replace(
 "Malefic corporeal conjunction, square or opposition afflicting the angular ascendant lord, or its **entering combustion**, are further negatives.",
 "Malefic corporeal conjunction, square or opposition afflicting the angular ascendant lord, and a separate **'or if he is entring combustion'**, are further negatives. Whether the combustion clause inherits all earlier **angular-position prerequisites** is **not** explicit."
)
replace(
 "Saturn/Mars as symbolically cold/hot, with mutual-reception qualification (6)",
 "Saturn/Mars as symbolically cold/hot, with the explicit exception requiring **mutual reception between the Moon and Saturn/Mars**, not merely generic significator reception (6)"
)
replace(
 "The general hopes/fears by benefic/infortune significators in (8) are only defaults",
 "The author's instruction to **'hope well'** for fortune significators and to fear the worst for infortune significators in (8) is only a default, not a guaranteed favourable outcome"
)
replace(
 "**Moon separating** from a planet marks the past (10), while **applying** marks the present question's direction under specified good house/aspect/planet conditions (11)",
 "**Moon separating** from a planet marks the past (10), while **applying by good aspect from a good house to a good planet** helps assess the question's present direction (11)—the good-house clause applies to **the Moon herself**, not automatically to the receiving planet"
)
replace(
 "A favourable Jupiter/Venus aspect may mitigate evil shown by infortunes, with a final elliptical qualification when the **fortunes themselves are significators** (16). Its wording is retained rather than manufacturing a symmetrical rule.",
 "Aphorism16 actually prints **'cast not any aspect unto them'** before a purported lessening of evil. The negative **not** is source-explicit but yields an ambiguous or paradoxical rationale; it cannot be silently replaced by a **favourable aspect** rule. The last phrase concerning the fortunes themselves as significators is also elliptical, so no repaired symmetrical algorithm is invented."
)
replace(
 "The next aphorism (20), crossing printed299–300, supplies a notable **exception**: Saturn/Mars in **house, exaltation, or triplicity AND an angle** can perform the desired matter.",
 "The next aphorism (20), crossing printed299–300, supplies a notable **exception**: Saturn/Mars in **house, exaltation, or triplicity and an angle** can perform the desired matter, **as the continuation body reads**. However, the original printed **page299 catchword is 'or'**, conflicting with page300's **'and Angles'**. The precise conjunction of status and angularity is therefore **source-qualified**, not silently resolved."
)
replace(
 "A **peregrine/no dignity**",
 "A **peregrine/no dignity**"
)
replace(
 "A question's significator **combust or in solar opposition** is called unable to perfect (23); two infortunes joined produce weak good or intensified evil (24);",
 "A question's significator **combust or in solar opposition** is said to signify 'no good', unable to perfect (23); two infortunes **joined** by source-broad contact/aspect wording produce weak good or probably intensified evil (24);"
)
replace(
 "Aphorism (26) gives two specific source thresholds: a planet **within twelve degrees of the Sun** is **under the beams** and weak, whereas **within sixteen arcminutes of the Sun** it is **cazimi** and strong.",
 "Aphorism (26) gives two specific source thresholds: a planet **within twelve degrees of the Sun** is **under the beams** and weak **'let it be in what Signe it will'**, whereas **within sixteen arcminutes of the Sun** it is **cazimi** and strong."
)
replace(
 "(31) qualifies an impeded Moon with a **waning-Moon life warning** and separate journey and wooing examples.",
 "(31) says an **impeded Moon** often makes the question difficult. Its **life warning is specifically when the question is about 'going to WARRE'**, not a lunar waning phase. Separate journey and marriage/wooing cases are negative examples. The earlier draft incorrectly transcribed **WARRE as WANE**; the printed source, retained in R1907, governs the correction."
)
replace(
 "An infortune aspecting a significator while adverse planetary statuses hold may produce severe impediments (36)",
 "An infortune aspecting the significator while **both** are peregrine, retrograde, cadent or in contrary-nature signs may suggest serious impediments (36), but the author's status-list grammar and 'it may then be doubted' remain qualified"
)
replace(
 "On PDF336, the final four rules specify a seventh-house infortune threatening marital disagreement **unless it is a significator at birth** (40)",
 "On PDF336, the final four rules specify an **'unfortunate Planet' (afflicted, not necessarily a naturally malefic planet)** in the seventh threatening marital disagreement **unless the same planet is a significator at birth** (40)"
)
replace(
 "a Dragon-tail-like glyph indicates alleged harm/scandal/slander through that house (43).",
 "a Dragon-tail-like glyph indicates alleged harm/scandal/slander through that house, with Lilly's explicit strong phrase **'it seldome failes'** retained as **his unverified assertion** (43)."
)
replace(
 "There are **35 explicitly retained textual and implementation uncertainties**",
 "There are **39 explicitly retained textual and implementation uncertainties**"
)
old="## Next reading boundary"
assert old in report
new="""## Independent source review and verified corrections

A fresh original-image-first independent reviewer inspected all nine supplied page/errata images and all 69 candidate source units. The first review reported **FINDS_ERROR**, chiefly three meaning-changing inaccuracies: **aphorism31 concerns 'going to WARRE', not a waning Moon**; **aphorism6's exception names reception between the Moon and Saturn/Mars**, not generic significator reception; **aphorism40 says 'unfortunate Planet'**, not necessarily naturally malefic Saturn/Mars. Original PDF335,332,336 respectively govern those repairs. Two further unresolved text issues were recorded: **p299 catchword 'or' versus p300 body 'and Angles'** in aphorism20; and **p296 'or is in aspect with any Planet in an Angle'** potentially contradicting the direct-angular negative on p297. Another source-critical negation in aphorism16, **'cast not any aspect'**, is preserved as printed rather than corrected to an assumed favourable aspect. Lesser qualification, aspect-order, page-range and terminological repairs are preserved in R1852–R1920, U01–U39 and independent_review/FINAL_RECONCILIATION.json. The review staging folder used a different image path; the canonical original images actually exist under \`evidence/\`, so that staging-specific path objection was not a repository defect. No independent empirical validation occurred. [PDF330–336; OPUS_INITIAL_DIAGNOSIS.md; FINAL_RECONCILIATION.json]

## Next reading boundary"""
report=report.replace(old,new)
(B/"AUDIT_REPORT.md").write_text(report)
S=B/"SOURCE_FIRST_NOTES.md"
notes=S.read_text()+"""
## Fresh independent source review — B02r corrections

- Original reader verified **43 sequential general horary aphorisms** and **nine original images**, independent first pass with minor image-navigation authority seen before images.
- HIGH: #31 printed **'going to WARRE'**, not waning Moon; #6 Moon–Saturn/Mars mutual reception, not generic significator reception; #40 **unfortunate (afflicted) planet** instead of natural infortune.
- MEDIUM: #20 p299 catchword **'or'** conflicts with body p300 **'and Angles'**; XLVIII R1862 positive angular-aspect *or* potentially conflicts with R1865's direct-angular no-release.
- Source-literal aphorism16 **'cast NOT any aspect'** must not be silently repaired to positive; remaining editorial hedges and seven page-range overlaps corrected.
- All actual original source PNGs exist under \`evidence/\`; isolated evaluator staged them under \`source_images/\`, so stage path discrepancy was a false positive for the repository.
"""
S.write_text(notes)
print(json.dumps({"report_words":len(report.split()),"notes_words":len(notes.split()),
                  "review_corrections":11}))
