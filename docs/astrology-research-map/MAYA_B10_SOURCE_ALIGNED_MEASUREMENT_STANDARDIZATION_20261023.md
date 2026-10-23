# B10 — Source-faithful Chuen craft measurement using existing research standards

**23 October 2026 · a usable pre-review instrument, not an active, frozen or completed human experiment.**

## Why the prior Chuen study design needed an actual change

The B07–B09 original-source audit demonstrated a **real colonial Yucatec birth-day claim** associating **Chuen** with skilled making, carpentry and weaving. Barrera Vásquez's earlier translation (reported in Thompson's *Maya Hieroglyphic Writing*, 1950, p80) and Bolles's later Kaua/Chan Cah/Pérez edited Yucatec columns support the *historical lexical sense*, **not** the truth that contemporary people born on this day have those occupations. Likewise, the B04/B05 1722 **Highland K'iche'** 5×52 calendrical almanac is **not** the same natal source, and traditional birth-day turnover remains unverified in modern Yucatán.

B09 suggested that a single question about **total paid+unpaid craft hours over the past 12 months** should be the primary observable. That is more precise than generic artistic personality but still problematic: the historical source says **an artisan/occupation/skill**, while the question asks for *stylized estimated hours* far into the past. Time-use validation literature reports both systematic and random recall errors in stylized estimates, and UN statistical guidelines favor shorter recall intervals/diaries when appropriate. The previous B09 version was **unfrozen and had no respondents**, so evaluating alternative measures now does not create post-outcome fitting.

This B10 increment applies a bounded established-work scan rather than devising a new craft typology. Important primary references: [ILO's ISCO-08 official occupation classification](https://isco.ilo.org/en/isco-08/), [Luxembourg Social Security's published ISCO-08 unit-code list](https://ccss.public.lu/en/codes-citp.html), [U.S. Bureau of Labor Statistics ATUS coding methodology](https://www.bls.gov/tus/lexicons.htm), [UN Statistics Division time-use guidelines](https://unstats.un.org/UNSDWebsite/demographic-social/time-use/guidelines/II/), and [COSMIN content-validity methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC5891557/) (Terwee et al. 2018, DOI 10.1007/s11136-018-1829-0). Original measurement-error study: [Kan & Pudney, *Measurement Error in Stylized and Diary Data on Time Use*, 2008](https://doi.org/10.1111/j.1467-9531.2008.00197.x). These references guide *measurement methodology*, not natal astrology.

## A much more defensible short list of measurement options

| Candidate | Construct | Measurement | Source fidelity / principal limitation |
|---|---|---|---|
| **C1 – preferred for source fidelity** | Skilled craft-maker **work/occupation** | Describe work tasks; reviewer blind to birthday assigns **narrow occupational units** | Closest to carpenter/weaver, but biased by paid-work access and misses unpaid subsistence crafts |
| **C2 – alternative** | Practiced physical craft-making | **Frequency over 4 weeks** (0/1/2–3/4–7/8+ occasions), paid/unpaid separately | Concrete behavior with lower recall burden, but misses seasonal episodes and skill without current opportunity |
| **C3 – previously proposed B09 primary** | Approximate yearly making-hours | Six ordered time bins spanning 0 to over 100 hours | Indirect proxy and vulnerable to annual recall error; **do not promote without review** |
| **C4 – supporting measurement** | Observed activities | Seven consecutive days of brief diary entries, paid vs unpaid separated | Reduces recall delay; may undercapture episodic artisan practice |

This is a **pre-outcome comparison**. No selection has yet been frozen as confirmatory. A reasonable default is **C1 if the source's occupational identity is the intended effect**, with C2 and C4 as clearly secondary sensitivity/reliability checks. A content reviewer may instead select C2 if occupational status turns into a proxy for opportunity, but must record that decision *before any person’s scored chart–response linkage*. Do not combine different outcomes, source epithets, four calendar variants, Men/Caban traits and old participant profiles into one flexible success criterion.

### The task-code crosswalk is deliberately narrow

The official **ISCO-08 Major Group 7** is **far too broad** to count wholesale as a historical Chuen prediction. We therefore propose *one investigator-defined subset* of **unit** occupations: **7115** carpenters and joiners; **7314** potters; **7317** wood and basketry handicrafts; **7318** textiles/leather handicrafts; **7522** cabinet-makers; **7531** tailors and dressmakers; **7533** sewing and embroidery workers. These match actual object making and specific historical weaving/woodworker examples. The ILO has **not** endorsed an "ISCO Chuen" instrument.

The code must be assigned by a person who can inspect *tasks*, ideally with an independent second reviewer blinded to whether a chart classifies the respondent as Chuen. It must **not** be inferred from the mere word "creative", hobby interest, demographic labels, or the investigator seeing natal data. An industrial automatic loom operator, a cashier in a craft store, a cook doing routine household chores and a digital artist are not automatically the same as a trained carpenter or traditional weaver. An unpaid apprentice may have real skill but cannot simply be passed through a job-only classifier as if formally occupational; report this separately pending a source-aligned rule.

[Machine-readable COSMIN/ISCO/ATUS/UN evidence and measurement candidate matrix](MAYA_B10_ESTABLISHED_CRAFT_MEASURES_AND_DECISION_MATRIX.json).

### A real content-review packet rather than another generic suggestion

[Open the self-contained cognitive-review protocol](MAYA_B10_CRAFT_QUESTION_COGNITIVE_REVIEW_PACKET.md) for a blinded evaluator. It gives two neutral candidate questions (occupational tasks and 4-week crafting frequency), paid/unpaid variants, respondent think-aloud prompts, a seven-day diary check, French/English interpretation questions, and three content-validity domains: **relevance, comprehensiveness, and comprehensibility**. Its 3–6 development-reviewer suggestion is **not** a regulatory minimum and is not an untouched astrology validation sample.

Any misunderstandings or translation changes can be used to improve this **development** instrument. The source-aligned **one** primary measure, frozen calendar date rule (declared reconstructed GMT584283, not guaranteed living traditional count), coefficient policy, birth-time uncertainty handling, decoys, missingness, statistical test, subgroup/comparison strategy, and private enrollment/consent must be fixed *before* true scored participants. The existing `humandesign` forward-blind protocol already governs source–prediction–answer–reveal separation: do **not** fork a new production HD V4.3 scorer.

### Anonymous work-task code example tests

To make the codebook executable without mixing private birth records, B10 adds a [manually supplied ISCO-unit coding preflight](maya_b10_occupation_coder_preflight.py). It is **not** an NLP occupational classifier, a public participant-score service or a chart prediction engine. Given only a blinded, preverified four-digit occupation code, reviewer verification state, and whether tasks were paid/self-employed/unpaid, it emits candidate core-match / core-nonmatch / **abstain** flags. It **rejects identity and birth fields** and abstains on uncertain occupational or unpaid classifications instead of converting missing/unpaid data into "not a craft worker".

The [13 entirely synthetic role fixtures](MAYA_B10_ANONYMOUS_CODING_FIXTURES_V1.json) cover paid carpentry, textiles, cabinet-making, pottery, embroidery, craft-store cashier, industrial loom operator, digital art, food preparation, unpaid subsistence weaving, apprenticeships, ambiguous roles, and no records. Tests explicitly show that a **wrongly assigned** ISCO code could produce a false core-role flag—hence the need for independent coding, not algorithmic overconfidence. This codebook does **not** assign roles based on any real human respondent or make a source-derived natal prediction.

## Scientific readiness and next exact steps

**Measurement options available:** yes, with direct external standards and source warrants.

**Finished true content-validity tests by independent adults:** zero. **Selected/frozen main human outcome:** no. **New recruited respondents:** zero. **Actual forward-blind human effect estimates:** zero. **Any production natal model promotion:** zero.

The next authorized in-scope operation after this source increment is to **perform** the small, no-DOB cognitive-review exercise and obtain a recorded answer about whether C1 craft occupation or C2 recent practice is the more intelligible/source-faithful single target. That is a human observation we cannot manufacture. The rest of the necessary study—private birth-data normalization, exact historical reconstruction, one frozen null/decoy policy, and ethical recruitment—must proceed before a result can be called predictive. This Maya lane need not block a prepared forward-blind experiment in any other astrology school.

**Reproduction:** `python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -q`, original B09 **166** source-only/method checks + B10 **10** new source/ISCO scope/negative tests = **176**. These are not 176 human births or 176 validated astrological predictions.
