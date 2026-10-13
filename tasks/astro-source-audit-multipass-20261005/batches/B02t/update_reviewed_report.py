"""Re-bind audit prose to independently corrected chapter-L source rules.

Original report is saved for exact rollback, but findings always explicitly
distinguish copied 1647 evidence from controller interpretation.
"""
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/"AUDIT_REPORT.md"
backup=B/"recovery"/"pre_first_review"/"AUDIT_REPORT.md"
assert backup.is_file()
s=backup.read_text()
def replace(a,b):
 global s
 if s.count(a)!=1:raise AssertionError(("Report span",s.count(a),a[:100]))
 s=s.replace(a,b)
replace("DRAFT, independent source review pending","source review corrected, documentary acceptance pending")
replace(
 "This draft contains **129 numbered documentary candidate source units R2138–R2266** drawn from twelve original PDF pages. It follows accepted Lilly **2,137** and retained Ptolemy **1,066**, combined **3,203**. Only if independently reconciled, accepted and integrated will the inventory become Lilly **2,266**, combined **3,332**. These are *source-description units*, not 129 corroborating historical events, human experiments, animal recoveries or validated outcomes.",
 "After the two first independent original-image reviews and source-grounded corrections, this draft contains **162 numbered documentary candidate source units R2138–R2299** from twelve original source pages. These comprise **129 initially extracted plus 33 additional page-localized clauses and headings** discovered during review. The baseline already accepted corpus remains **2,137 Lilly** plus **1,066 Ptolemy** = **3,203**. Only after source-fidelity acceptance and nonforce remote integration would the inventory become Lilly **2,299**, combined **3,365**. These are *source-description units*, not 162 corroborating historical events, tested searches, animal recoveries or validated outcomes."
)
replace(
 "The initial printed material treats the **Moon as a general significatrix of missing goods** and turns to Moon’s application, ascendant and second-house lords, her **domicile ruler** and, later, rulers of sixth/eighth/twelfth.",
 "The initial printed material treats the **Moon as general significatrix**, including a marginal note that the adjacent indications **principally concern strayed cattle**. It turns to Moon's application, ascendant and second-house lords, her **domicile ruler**, and later the sixth/eighth/twelfth. Moon's own sign is not the same subject as **Moon's house ruler** when selecting the original human signs or animal-sign glyphs."
)
replace(
 "The author proposes directional and proximity judgments from Moon’s **zodiacal quarter** and element, positions relative to the ascendant lord, degree separation and sign category.",
 "The author proposes directional and proximity judgments from the Moon's **quarter/sign and element**, first lord and lunar house lord. The original states **within ONE SIGN** rather than only 'roughly thirty degrees' for one close-home clause, and another says a thing's significator or Moon in the same quadrant is in the **same Town or Hundred**."
)
replace(
 "These are **competing conditional source attributions** depending on one identified separating body.",
 "Some printed planet alternatives also apply when the **ascendant lord is IN the planet's own house**, rather than merely separating from that planet; Jupiter additionally has a printed fast/abstinency example. These are **competing conditional source attributions** depending on the specified prior separation or placement."
)
replace(
 "The draft records those opposing directions separately and retains alternative fallback to the second-house lord when the first testimony is unavailable. Lilly treats Moon’s application to the lord of the **eighth house**, and later the domicile lord’s corresponding aspect, as historical livestock death testimony.",
 "The draft records opposite separating directions separately. **The second-house lord must be checked whenever the Moon's house lord shows no separation; only if neither lord shows it is the animal said to remain in place.** The source's initial alleged death indicator invokes **the eighth counted FROM the Moon**, which is not the radical eighth; the latter appears as a separate last fallback. The domicile lord's counterpart can mean **dead OR dying shortly**. Later PDF358–359 introduces other, explicitly separate radical-eighth/house claims."
)
replace(
 "The positive allegation, negative exception, later contrary evidence and Part-of-Fortune-like glyph must remain separate.",
 "The positive allegation, a separate **planet occupying first and transferring power to a thief significator**, the **lord of the Part-of-Fortune glyph**, a repeated 'Not stolne' branch for beasts, and negative/contrary circumstances must remain separate. An infortune in ascendant or second is a location-specific loss exception."
)
replace(
 "The next pages distinguish location by Moon's **house** (first, fourth, seventh or tenth), **element** (fiery/watery/earthy/airy), **sign** (including late Capricorn and Aquarius-like glyphs), the lunar dispositor and the alleged angular distance to the ascendant lord.",
 "The next pages distinguish location by Moon's **house** (first, fourth, seventh or tenth), **element** (fiery/watery/earthy/airy), **sign** (including readable **Libra/Aquarius exceptions**, and **Capricorn's last FACE on p323** versus **last MOIETY on p324**), the lunar dispositor and angular distance. Moon **IN ascendant** is the case for **return with trouble or pain**, whereas different helpful-finder clauses distinguish a person who *would fain* restore from an asserted *will restore*."
)
replace(
 "Original **PDF359/printed325** opens *Another Judgment*, offering additional placements and even different rules for objects versus animate beasts.",
 "Original **PDF359/printed325** opens *Another Judgment*, offering different readings for inanimate things versus beasts. Its printed *Cattle shall be found againe* clause uses the **second, FIFTH or eleventh house**, **not sixth**; and its lost-beast clause says **chiefly if** cadent, not that cadency is mandatory."
)
replace(
 "Later original PDF360–361 proposes more detailed **terrain/direction** classifications, including watery signs implying northern lowland/watering places, airy signs west/open ground, and fiery signs east/woods or burnt brush.",
 "Later original PDF360–361 separates **terrain/direction** by sixth lord's sign and angularity: watery **angular north/close**, **succedent north/right**, and **cadent left/wet-meadow** are different source outcomes. For airy signs the **cadent** clause is **left and straying farther**, not westward; airy west appears in angular/succedent clauses. Fiery/angular **BUT** replaces the east/woods location with confinement/enclosure."
)
replace(
 "It then discusses **cattle to pound** and alleged risk of starvation, death, imprisonment or later escape.",
 "It then discusses **cattle to pound** and alleged risk of starvation, death, custody or later escape. The source's Mars aspect to Saturn **or Moon in twelfth** is not an invented Moon–Saturn aspect. One Saturn four-house long-impoundment clause has different prerequisites from an ascendant-lord eighth-house probable-death claim."
)
replace(
 "The draft switches to ascendant lord/Sun/Moon for the querent and seventh-house lord for the missing or fugitive party as the source requires",
 "The draft switches to **ascendant/its lord/SUN for querent** and **seventh/its lord for fugitive OR missing thing**, then explicitly identifies **Moon as natural significatrix of the fugitive**, not an additional initial querent significator"
)
replace(
 "Source clauses distinguish a voluntary return, being found/captured against one’s will, being detained by authorities, news coming through another,",
 "Source clauses distinguish **news from Moon separating FIRST-lord and joining SEVENTH**, versus **regret/entreaty from the reverse Moon direction**, a voluntary return, being found/captured against one's will, **detained but NOT imprisoned when both planets lack angularity**, a capture only **upon good search**, news coming through another,"
)
replace(
 "Original **PDF364/printed330** contrasts **two proposed distance methods**",
 "Original **PDF364/printed330** contrasts **two proposed distance methods**"
)
replace(
 "while asking the reader to consider town versus country.",
 "with the movable measure qualified **'at discretion'**, while asking the reader to consider town versus fields and **fugitive versus thing lost**."
)
replace(
 "The original 1647 printed **errata PDF888** appears to contain two directions within this page range: **printed p324 line10 “read the”** and **printed p330 line6 “read for.”** Their existence is recorded separately in ERRATA_COLLATION.json. The exact printed body-word targets and original line-numbering conventions are **not fully proved**",
 "The original 1647 printed **errata PDF888** contains two directions in this phase: **printed p324 line10 'read the'** and **printed p330 line6 'read OR'**. The p330 target is visually localized in the fugitive three-day clause, where the original first letter of '[f]or according to probability' is blotted; the erratum instead makes the three-day **news** statement an **alternative** to the preceding return statement. The original p324 body target and some printer line conventions remain **unproved**. Both witnesses are recorded separately in ERRATA_COLLATION.json. These observations are not universal emendation authority"
)
replace(
 "There are **30 retained first-pass limitations**",
 "There are **50 retained original-text, review and implementation limitations**"
)
replace(
 "Independent image-first review must establish whether source conditions were correctly captured; deterministic tests only assure consistency and stable provenance, not truth of the historical predictions.",
 "Two initial image-first independent windows found **7 MAJOR plus 15 MODERATE** findings (PDF353–359) and **9 HIGH plus 18 MEDIUM** findings (PDF359–364). Their original reports are preserved as separate frozen evidence. Controller source repairs and structural regression checks address those findings but are **not a fresh third blind review**; deterministic tests establish consistency and recorded provenance, not truth or successful predictions."
)
marker="**Next boundary:**"
assert s.count(marker)==1
addition="""## Source-review reconciliation: critical changes

The source readers were instructed to inspect original images **before** draft records and reported all 70/70 and 71/71 window records respectively (the physical original PDF359 appears in both windows). The source's 1647 page images were verified independently against the original complete scan and their raw reviews remain unedited at \`independent_review/OPUS_A_INITIAL.md\` and \`OPUS_B_INITIAL.md\`. Their finding severities are source-fidelity labels, not empirical measures. Corrections are preserved within R2138–R2299 and the prior 129-unit input snapshot is kept for diff-based replay.

The largest substantive repairs were **Moon-derived vs radical eighth house**, **fifth not sixth** in cattle recovery, **Moon or its house lord** in distinct role/house clauses, **the opposite direction of Moon's news vs remorse**, **the word Infortune crossing original pages 363–364**, **Mars as the sole aspecting planet** in a cattle-impoundment harm clause, and a p330 erratum that says **OR rather than FOR**. Additional original headings and alternative significators were recovered rather than silently merged. The original source also distinguishes custody from imprisonment and voluntary from forced return, which cannot be used to infer present legal or moral conclusions.

Each edited source unit is a normalized **paraphrase**, not a diplomatic transcription. The late-seventeenth-century source's grammar and occasional conflicting rules are **retained in an uncertainty register**, not smoothed into one modern algorithm. No real lost goods, animals, fugitives, third-party motives, predictions or clinical outcomes were independently verified. [Independent source readers A/B; \`PHASE1_RULES_DRAFT.json\`; \`UNRESOLVED.json\`]

"""
s=s.replace(marker,addition+marker)
p.write_text(s)
n=B/"SOURCE_FIRST_NOTES.md"
notes=n.read_text()
notes+="\n## 2026-10-13 first independent original-image reviews, source repair\n\n"
notes+=("- Fresh original-image window A reviewed PDF353–359 and 70 draft records, 7 major and 15 moderate material findings; window B reviewed PDF359–364 and 71 records, 9 high and 18 medium findings. The original initial outputs are retained and hash-checked.\n"
 "- Restored the Moon-derived eighth from the Moon, radical eighth fallback, p325 second/FIFTH/eleventh recovery, p330 'OR' erratum, opposite news/regret lunar directions, and all B-reported additional headings/conditional units.\n"
 "- The next physical PDF364 contains some phase1 body then the separate thief-and-theft heading opening phase2; do not count a source paragraph in both phases.\n"
 "- Phase1 after repairs holds 162 reference-only normalized source units; all Chapter L beyond the p330 thief divider remains untouched and OPEN.\n")
n.write_text(notes)
print("Report reconciled against both frozen original image-first reviewers.",
      "length",len(s),"review_finding_total",49)
