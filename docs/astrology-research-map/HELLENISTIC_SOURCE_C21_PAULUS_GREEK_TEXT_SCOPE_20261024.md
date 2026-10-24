# C21 — Greek Paulus: sect-light scope, the seven-distinct rule and degree fractions

**Research date: 24 October 2026.** **Main objective OPEN:** reconstruct Hellenistic source-defined methods faithfully, preserving contradictions, for eventual independently blinded human comparison. This batch is **direct Greek textual/source-interpretation research**, **0 human predictive validations**, and **no production scorer changes**. Continues from C20; does not repeat earlier manuscript/papyrus acquisition.

## What is newly checked against actual Greek

Directly accessed the **Eulogikon digital Greek body of Paulus Alexandrinus, *Eisagogika* (“Elements of Astrology”)**, including the site's downloadable Markdown. The HTML returned 200, **245,014 bytes / SHA-256 `ee00fd3c669cee1484b355b2b2ec04544f69bf159046d6d914fade0e51cd29cc`**; Markdown returned 200, **181,883 bytes / SHA-256 `78b9da9d8fdf9187c969ebb4cd3b46151f9831d8e68d238274962f0e8696a263`**. The webpage's own front matter says text modified **2026-10-23** and has a separate internal content hash. URLs:

- `https://eulogikon.org/works/paul-alexandria-astrology-sum-aa`
- `https://eulogikon.org/works/paul-alexandria-astrology-sum-aa.md`

**Source authority boundary:** this is a readable modern digital edition/transcription of the *Greek body*, NOT a newly recovered late-antique papyrus, NOT independent collation of the three physical 14th–16th-century witnesses, and **not** Boer's actual printed 1958 Greek critical apparatus. No complete source text copied into Git. Four tiny direct phrases and our interpretations are stored in [the C21 evidence register](PAULUS_C21_GREEK_SECT_LIGHT_CLAUSES_V1.json).

### Chapter 5, by-sign monomoiria

The passage directs allotment in **Chaldean planetary order**, starting with the planet whose domicile the sign is, then advancing one planet per **ordinal** degree. Its ending explicitly counts the remaining **arcminutes as belonging to one degree**. This supports the previously frozen C04 interpretation that a longitude of **0°35′** occupies the **first** ordinal degree, while **2°35′** is in the **third**, not second. It does not make the truncated-completed-degree comparison used in Tolsa's 2017 *Valens* table identical to this source method. The prior C20 Berlin four candidate degrees **2, 9, 16, 23** remain mathematically reproduced, unchanged and *editorially reconstructed*, not papyrus values.

### Chapter 32, by-trigon monomoiria — important scope distinction

The subject of the ancient instructions is the **light of the sect**, **Sun for day** and **Moon for night**. The text instructs beginning with the sect's first triplicity lord of that light and distributing successive degrees while avoiding a second assignment to a planet before the starting planet's cycle condition is satisfied. This agrees in principle with C05's *seven-distinct-planet narrative interpretation*, which skips the duplicated Venus in the four trigon ruler pairs. Chapter 32 describes its *subjoined chart* as **diurnal** and explicitly says the order of rulers changes for nighttime births, with fire trigon opening **Jupiter then Sun** at night.

**Crucial limitation:** the instruction is **NOT** that chapter-32 trigon monomoiriai automatically apply to any chosen planet, Ascendant, Midheaven, or other chart point. Earlier C04/C05/Tolsa comparisons that test those labels against the trigon rule are *comparative historical exploratory exercises*, not direct validated executions of chapter 32 in its declared light-of-sect setting. They are not deleted or marked impossible; their applied-scope distinction is now explicit.

The old C05 daytime narrative remains **34/120** different from the Greenbaum corrected daytime table. The directly photographed Munich, Florence and Vatican *diagram-family* readings still contradict seven-distinct-planet narrative in many individual cells, including duplicate Venus and the changed water-column phase. **Literal manuscript tables are not “repaired” to conform to the prose, and the prose is not overwritten by those tables.** Determining which historical recension/notation is earliest still requires actual Boer 1958 chapter-32 printed apparatus and independent manuscript genealogy.

Another vital negative: Eulogikon's modern Markdown displays **the four trigon sign-group headings** of the canonical table, but **no legibly transcribed 30×4 per-degree planetary cell grid** between that heading and its next prose sentence. This is a limitation of *that digital rendering*, not evidence that Paulus's ancient or Boer printed tables contained no cells. It cannot settle the existing 34 source disagreements.

### Chapter 33, Ascendant recovery: several methods, not one unique rule

The adjacent Greek passage discusses using the *light of sect's trigon monomoiria* to infer an Ascendant degree, but explicitly names **other approaches**—including Moon's planetary bounds and earlier syzygies. This establishes a **historical plurality of Ascendant inference procedures**. It does **not** independently establish the missing Libra Ascendant of Berlin P. Berol. 21347, nor the extra hypothetical **Saturn Egyptian term** needed to favor the C20 editorial **2°35′** conjecture over 9°35′, 16°35′ and 23°35′. That four-element uncertainty remains.

## Reproducible technical enforcement (research only)

The new [sect-light-only wrapper](paulus_c21_luminary_scope.py) reuses unchanged C04/C05 frozen code without adding a new astronomical engine. Its chapter-32 research API requires `sect=day, luminary=Sun` or `sect=night, luminary=Moon`; it refuses unrecognized sect and mismatched/arbitrary luminary (including `Ascendant`). It accepts an **explicit ordinal degree 1–30** rather than silently imposing chapter 5's arcminute handling on chapter 32, for which the exact same rounding convention is not explicitly established by this passage.

The C21 regression fixtures check source hashes, short exact Greek clauses, chapter 5 physical intervals, chapter 32 diurnal/nocturnal first-ruler examples, all-seven-distinct narrative assignments, the unreconciled **Cancer/day degree-8** triple reading (*narrative Venus; corrected Greenbaum Mars; photographed manuscript family Mercury*), unchanged 34/120 manuscript/table disagreements, and no human data or production rule promotion.

**Important interpretation:** This does not prove the manuscript-table family is wrong, nor the original author's intended chart, nor predictive astrology. The numbers are merely source-aware implementation checks. Existing Oxford P.Oxy.4277 **1 of 3** calculation matches and two failures are unchanged.

## Next source work

1. **Boer's actual printed 1958 chapter-32 apparatus/diurnal diagram**: direct compare the Greek narrative's no-duplicate rule to printed table, marginal sigla and the three handwritten copies; the current Eulogikon text does not supply the cells.
2. **Boer 1962 attributed commentator's Greek diagrams** and alternative Paris Z/Y codices; test whether their textual genealogy actually differs from Florence/Vatican/Munich rather than counting dependent copies as independent votes.
3. **Original Jones 1999 vol II pp421–427** to independently distinguish damaged glyphs from editorial restorations in P.Oxy. 4277. Authenticated original Oxford photos are already known and need not be fetched again. Maintain C20 Berlin editorial reconstruction as four options.

No biographies, production predictions, purchased Gansten Kindle extraction using Work, or source-image redistribution.
