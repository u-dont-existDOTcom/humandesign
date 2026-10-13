"""Rewrite only the report from preserved original, source-corrected B02r review."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/"recovery/original_draft/AUDIT_REPORT.md").read_text()
pairs=[
 ("separation by a few minutes suggests it is virtually accomplished already",
  "separation by a few minutes is only **'an argument'** the person is **'as good as freed already'**, not a recorded release"),
 ("The next question contrasts a **determinate versus not absolute** request, with examples of release from the present master versus ever being free from his power.",
  "The text groups **both examples** under a **'determinate and not absolute'** question: release from the present master and ever gaining freedom from his power. It does **not** contrast the two examples or define an absolute question."),
 ("related to a planet **in an angle** or a planet that **beholds ascendant**",
  "the printed alternative **'or is in aspect with any Planet in an Angle'**, or to a planet beholding the ascendant. That **'or'** may instead continue **'no aspect'** as a negative **'nor'** and, read positively, may contradict the direct-angular no-release clause; the source condition is unresolved"),
 ("Malefic corporeal conjunction, square or opposition afflicting the angular ascendant lord, or its **entering combustion**, are further negatives.",
  "Malefic corporeal conjunction, square or opposition afflicting the angular ascendant lord, or **'if he is entring combustion'**, are further negatives. Whether **entering combustion** inherits the preceding angle restriction remains unclear."),
 ("with mutual-reception qualification (6)",
  "with the explicitly Moon-involved **mutual reception of Moon and Saturn/Mars**, not just any significators (6)"),
 ("and give only a general benefic/malefic default (8)",
  "and instruct **'hope well'**, not guaranteed success, with fortunate significators while fearing worse with infortunes (8)"),
 ("**applying** marks the present question's direction under specified good house/aspect/planet conditions (11)",
  "**applying** by a good aspect **from the Moon's good house to a good planet** marks the matter's present prospects (11)"),
 ("beneficial aspects mitigate an infortune's evil but rule16 ends with an ambiguous extension concerning fortunes as significators, so no new symmetrical algorithm is invented.",
  "aphorism16 actually reads **'cast not any aspect unto them'** before claiming the indicated evil is lessened; this printed negative is **not** silently corrected to favourable aspects. Its further clause concerning fortune significators is also ambiguous, so no symmetric algorithm is invented."),
 ("describe **peregrine/no dignity** as negative (19); then provide a crucial **Saturn/Mars essential dignity AND angular position** positive exception (20, crossing PDF333–334).",
  "call a peregrine planet **'malicious beyond expression'**, with an analogy of a noble person **scorning to hurt** his opponent (19); then give a Saturn/Mars dignity-and-angular-position positive exception **as the continuation's body reads** (20). At the page333–334 join, however, the printed page333 **catchword is 'or'** while the next body reads **'and Angles'**. The exact conjunctive condition is therefore uncertain."),
 ("an afflicted question significator combust or in solar opposition cannot perfect (23), joined malefics show poor good or intensified evil (24)",
  "an afflicted question significator combust or in solar opposition allegedly signifies **no good and cannot perfect** (23); two infortunes **'joyned'** by a broadly worded contact/aspect produce little good or probably intensified evil (24)"),
 ("Rule (26) specifies **within twelve degrees** of Sun as under the beams and weak, but **within sixteen arcminutes** as **cazimi**, strong.",
  "Rule (26) specifies **within twelve degrees** of Sun as under the beams and weak **'let it be in what Signe it will'**, but **within sixteen arcminutes** as **cazimi**, strong."),
 ("(31) qualifies an impeded Moon with a **waning-Moon life warning** and separate journey and wooing examples.",
  "(31) treats an impeded Moon as generally difficult and warns about the querent's life specifically **'if it be in going to WARRE'**, then offers separate journey and wooing examples. The initial draft **wrongly read WARRE as a lunar WANE condition**; this has been corrected against PDF335."),
 ("(36) gives a compound negative infortune-aspect status whose exact grammar remains unsettled;",
  "(36) discusses an infortune and a significator when **BOTH** have stated negative conditions, while the grammar of those conditions remains unsettled;"),
 ("a seventh-house infortune threatens marriage disagreement **unless it is a significator at birth** (40)",
  "an **'unfortunate Planet' (afflicted, not automatically a natural malefic)** in the seventh threatens marriage disagreement **unless that same planet is a significator at birth** (40)"),
 ("a Dragon-tail-like glyph indicates alleged harm/scandal/slander through that house (43)",
  "a Dragon-tail-like glyph is said to signify harm, scandal or slander through its house, with the author's strong **'it seldome failes'** preserved as a claim, not an observed frequency (43)"),
 ("The **35-item uncertainty register**","The **39-item uncertainty register**"),
]
for i,(a,b) in enumerate(pairs,1):
 n=s.count(a)
 if n!=1:raise AssertionError(f"report replacement {i}, count={n}, span={a[:130]}")
 s=s.replace(a,b)
section="""## Original-image independent review: corrections and unresolved contradictions

A fresh source-image reviewer read all **nine** original-page/errata images and all **69** draft records, producing **FINDS_ERROR**. Three meaning-changing corrections were supported by the original: **aphorism31 = 'going to WARRE', not a waning Moon** (original PDF335/printed301); **aphorism6's reception exception names the Moon and Saturn/Mars** (PDF332/printed298); and **aphorism40 says 'unfortunate Planet' rather than necessarily a naturally malefic one** (PDF336/printed302). Two additionally unresolved source conflicts are now recorded: the **'or' catchword on PDF333 versus 'and Angles' body on PDF334** in aphorism20, and the positive-sounding **angular 'or is in aspect'** in XLVIII which can contradict an angular/direct no-release clause. Aphorism16's source-literal **'cast not any aspect'** is preserved even though the author then describes mitigation of evil. Smaller exact-qualification and page-scope repairs are recorded against original page images. The reviewer initially saw section identities for image navigation before reading the images, so independence was substantial but not absolute. One reviewer comment that \`evidence/\` paths were unavailable was limited to the intentionally isolated \`source_images/\` staging folder and is NOT a defect in repository sources. This documentary review makes no test of whether the astrology predicts reality. [PDF330–336; independent_review/OPUS_INITIAL_DIAGNOSIS.md; independent_review/FINAL_RECONCILIATION.json]

"""
marker="## Source limits and continuation\n"
assert s.count(marker)==1
s=s.replace(marker,section+marker)
(B/"AUDIT_REPORT.md").write_text(s)
print("REPORT_ADJUDICATED_REPLACEMENTS",len(pairs),"chars",len(s))
