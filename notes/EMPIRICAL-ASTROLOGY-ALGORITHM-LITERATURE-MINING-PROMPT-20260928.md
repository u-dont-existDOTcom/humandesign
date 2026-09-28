SYSTEMATIC EMPIRICAL ASTROLOGY LITERATURE-MINING PLAN FOR AN EVIDENCE-OPTIMIZED ASTRO ALGORITHM

Purpose
-------
This is NOT primarily a review of whether astrology "works," and it is NOT a review focused on time twins, aspect orbs, or any single astrological claim.

The goal is to design and, where feasible in this research run, begin executing a comprehensive literature-mining program that recovers the MOST USEFUL EMPIRICAL INFORMATION accumulated across decades of scientific/statistical astrology research, so that it can later be translated into candidate features, weights, interactions, priors, exclusions, and testable rules for an optimized astrology algorithm.

The desired output is an empirical "feature atlas" for astrology: What chart variables have actually been tested? Which specific configurations showed signals? Which failed? Under what populations/outcomes/definitions? What effect sizes, directions, thresholds, orbs, angular sectors, house systems, aspect families, interactions, nonlinearities, and boundary conditions were reported? Which results replicated? Which datasets were reused? Which apparently positive rules are likely artifacts? Which neglected findings deserve clean prospective replication?

Do not assume traditional astrology is correct. Do not assume it is false. Treat the historical literature as a noisy model-development corpus from which we want to extract potentially predictive structure while controlling aggressively for publication bias, multiple testing, post-hoc fitting, dataset reuse, and methodological weaknesses.

PART 1 — BUILD A NEAR-COMPLETE SOURCE MAP

Systematically identify empirical/statistical astrology research from database inception to 2026.

Search journal archives issue-by-issue where possible, not merely via keyword search. In particular, inventory the complete empirical contents of specialist research venues such as:
- Correlation / Journal of Research into Astrology
- Astrological Association research publications and research conference proceedings
- Journal of Scientific Exploration where relevant
- mainstream psychology, personality, statistics, sociology, medicine/epidemiology, astronomy, and social-science journals that published empirical astrology studies
- dissertations and theses
- Gauquelin publications/data monographs and later reanalyses
- CURA and serious archival research collections
- books/chapters containing original datasets or analyses
- conference proceedings and technical reports
- non-English empirical literature where discoverable
- skeptical/critical publications when they contain original analyses or reanalyses
- astrology-sympathetic publications when they contain actual quantitative data

Do not limit retrieval to famous studies. Citation-chain backward and forward from every major empirical research program and prolific empirical author. Identify authors/research groups whose work forms a series and trace the entire series.

For every potentially useful paper, locate the FULL TEXT whenever legally accessible. Search publisher pages, institutional repositories, author pages, Internet Archive/Google Books where lawful, ResearchGate/Academia author copies, thesis repositories, journal archives, DOI mirrors, and cited later reproductions. If full text cannot be obtained, record exactly what is missing and how to obtain it.

Create a "full-text acquisition queue" prioritized by likely algorithmic value, not fame.

PART 2 — DO NOT ORGANIZE THE REVIEW AROUND "POSITIVE VS NULL"

Organize the literature around ASTROLOGICAL FEATURES AND PREDICTIVE TARGETS.

Build a taxonomy broad enough to capture, at minimum:

A. Natal astronomical/chart features
- planets/luminaries by sign
- planets/luminaries by house
- Ascendant, MC, DSC, IC and angular distance
- Gauquelin sectors and alternative sector definitions
- conjunctions, oppositions, squares, trines, sextiles
- minor aspects
- exact continuous angular separation rather than categorical aspects
- orb width / tightness
- applying vs separating
- aspect strength functions
- aspect patterns/configurations (T-squares, grand trines, stellia, etc.) where empirically studied
- angular aspects to ASC/MC
- planetary prominence/dominance
- retrogradation
- declination, parallels/contra-parallels if studied
- latitude or other 3-D geometry if studied
- midpoints
- harmonics
- dignities/debilities/rulership/dispositors/receptions if empirically studied
- house rulership relationships
- elements/modalities/polarities
- Moon phase / Sun-Moon geometry
- lunar nodes
- asteroids or other bodies only where there is real empirical work
- fixed stars only where empirically studied
- combinations/interactions among the above

B. Timing/dynamic features
- transits
- progressions
- solar arcs
- returns
- directions
- age/event timing
- whether effects depend on natal configuration, orb, applying/separating status, angularity, etc.

C. Relationship features
- synastry aspects
- house overlays
- composite/Davison or other relationship charts if empirically studied
- attraction, marriage, divorce, relationship duration, interpersonal similarity/difference
- family/parent-child patterns

D. Outcome domains
- validated personality/temperament measures
- behavior
- interests/values
- vocation/profession/eminence
- cognitive measures
- relationships
- life events
- creative/scientific/sport achievement
- demographic/social outcomes
- health/mortality studies only as evidence extraction, with NO clinical recommendations
- other objectively measured outcomes

E. Alternative astrological systems
Where empirical studies exist, include Western tropical, sidereal/Vedic, cosmobiology, harmonics, Gauquelin-derived approaches, and other systems. Keep systems separate unless evidence justifies combining them. The aim is to discover useful predictive variables, not to defend one tradition.

PART 3 — EXTRACT STUDIES AT FEATURE LEVEL, NOT JUST PAPER LEVEL

For each paper, extract every independently testable astrological claim/result into a structured record.

Minimum fields:
- full citation, DOI, URL, full-text status
- journal/source and whether peer reviewed
- authors/research group
- year/country
- dataset name/source
- whether dataset overlaps another paper
- sample size and effective independent N
- population/selection mechanism
- birth-data source and Rodden-like reliability if relevant
- exact birth-time precision/rounding
- outcome variable and measurement quality
- exact astrological predictor
- exact computational definition
- zodiac/reference frame
- house system
- aspect definition
- orb definition
- applying/separating handling
- angularity/sector definition
- any subgroup restriction
- whether predictor/outcome/hypothesis was specified a priori
- statistical test/model
- correction for multiple testing
- effect direction
- effect size and uncertainty where recoverable
- p value / Bayes factor where reported
- raw cell counts or sufficient statistics
- whether result was positive, null, opposite-direction, or mixed
- whether the same rule was tested elsewhere
- independent replication status
- reanalysis/criticism and outcome
- data availability
- code availability
- risk-of-bias notes
- "algorithmic usefulness" notes

Crucially, a paper reporting 40 tested chart factors should produce up to 40 feature-level records, not one row saying "positive" or "negative."

Extract numerical tables/figures where possible rather than relying on abstracts or authors' verbal conclusions.

PART 4 — RECOVER NEGATIVE INFORMATION AS AGGRESSIVELY AS POSITIVE INFORMATION

For algorithm design, failed rules are valuable because they tell us what to downweight or omit.

Therefore record:
- traditional rules repeatedly tested with no signal
- rules that worked only in one dataset
- rules that reverse direction across datasets
- effects that vanish under blinding, better controls, or correction
- effects attributable to astrology knowledge/self-attribution
- features that are redundant with season, geography, demographics, scheduled birth, or cohort effects
- results whose apparent significance came from flexible orb/threshold/subgroup searches

Do not simply label such papers "failures." Translate them into model constraints such as:
- candidate feature unsupported
- prior weight near zero
- interaction-only candidate
- requires specific population
- requires independent replication
- likely confounded
- definition unstable

PART 5 — IDENTIFY THE MOST PROMISING EMPIRICAL SIGNALS

After extraction, rank RESEARCH PRIORITY, not truth or astrological systems.

Identify candidate signals in tiers such as:
1. replicated by independent teams/datasets with reasonably sound methods
2. repeated within multiple datasets but not independently replicated
3. strong or intriguing isolated signal worth prospective replication
4. traditional claim with substantial null evidence
5. insufficiently tested claim

For every promising signal, answer:
- exactly what predictor produced it?
- exactly what outcome did it predict?
- what was the effect size?
- was the direction consistent?
- how sensitive was it to orb/cutoff/house system/sector definition?
- was it linear, thresholded, U-shaped, interaction-dependent, or subgroup-specific?
- was the signal discovered or confirmatory?
- has it replicated on genuinely independent data?
- what competing non-astrological explanation exists?
- can it be computed reproducibly from date/time/location?
- how should it enter a machine-readable candidate model?

Do NOT create a single arbitrary "evidence score" that hides these distinctions.

PART 6 — LOOK FOR COMBINATORIAL INFORMATION THAT INDIVIDUAL STUDIES MAY HAVE MISSED

Our eventual algorithm may outperform any one traditional rule if several weak but independent signals combine.

Search specifically for evidence about:
- interactions among planets/aspects/houses/angles
- whether angularity amplifies an aspect
- whether aspect tightness matters only for certain planets/outcomes
- whether effects are stronger for luminaries/personal planets
- whether configurations matter more than isolated placements
- whether applying/separating modifies effects
- whether chart features predict extremes better than population means
- nonlinear dose-response
- sex/gender, age, culture, profession, cohort, latitude, or birth-era moderators
- whether exact birth time adds incremental predictive value over date alone
- whether location adds incremental value over date/time
- whether different astrological systems encode overlapping astronomical information

Where the literature did not test interactions directly but provides sufficient statistics to motivate them, label them HYPOTHESIS-GENERATING, not established.

PART 7 — PUBLICATION BIAS AND THE SPECIALIST-JOURNAL QUESTION

Explicitly investigate the user's intuition: decades of specialist astrology journals presumably contain a mixture of positive, negative, and method-development results.

For each major specialist journal/venue:
- inventory empirical articles by year/issue as completely as possible
- classify result direction without relying solely on titles
- identify prolific authors and repeated datasets
- estimate how many papers are independent tests versus reanalyses/reuse
- identify null findings that are easy to overlook
- identify unusually strong positive findings
- look for editorial/publication bias, selective outcome reporting, and file-drawer discussion
- compare methodological quality over time

If feasible, create a journal-by-era evidence map. Do not infer publication bias merely because a journal is astrology-friendly; inspect what it actually published.

PART 8 — MAJOR RESEARCH PROGRAMS TO TRACE IN DEPTH

At minimum trace complete chains of original study -> criticism -> response -> replication/reanalysis for:
- Gauquelin and subsequent Mars/Jupiter/Saturn/angular-sector work
- Eysenck/Mayo and later personality work
- Carlson's Nature double-blind experiment and every substantive critique/reanalysis
- Startup's aspect/angular-separation work
- Fuzeau-Braesch twin research and Ertel/Dean exchange
- Roberts/Greengrass time twins, French/Leadbetter/Dean, Dean/Kelly
- Tarvainen's entire empirical series, not merely the 2022 orb paper
- Ertel's empirical/reanalysis work
- Suitbert Ertel / Geoffrey Dean / Ivan Kelly / Chris French research lines
- vocational/professional studies
- marriage/synastry studies
- any other research program with repeated quantitative work

But do not let these famous programs crowd out obscure empirical findings from the specialist journals.

PART 9 — PRODUCE AN ALGORITHM-READY EVIDENCE ATLAS

The final deliverable should include:

1. SOURCE MAP
A near-complete bibliography/inventory, grouped by feature family and research program, with full-text links/status.

2. FEATURE-LEVEL EVIDENCE TABLE
A structured table suitable for later conversion to CSV/JSON with one row per tested predictor/outcome claim.

3. REPLICATION GRAPH
Which papers reuse which datasets, which findings are genuine independent replications, and which are merely reanalyses.

4. ASTROLOGICAL FEATURE ATLAS
For every feature family (sign, house, aspect, angle, orb, etc.), summarize:
- evidence supporting
- evidence against
- effect directions
- effect sizes
- moderators
- computational definitions
- uncertainty
- most informative full texts

5. PROMISING SIGNALS DOSSIER
Detailed dossiers for the empirical findings most worth reproducing in our own code and testing prospectively.

6. NEGATIVE-CONSTRAINT DOSSIER
Rules/features with enough negative evidence that an optimized algorithm should initially omit/downweight them unless new data overturns that.

7. UNTESTED / UNDERTESTED HIGH-VALUE HYPOTHESES
Important traditional or mathematically plausible interactions that surprisingly lack good tests.

8. CANDIDATE ALGORITHM SPECIFICATION
Do NOT claim a validated astrology algorithm. Instead propose a development model whose candidate features/priors are derived from the literature. For each included feature state:
- evidence source
- exact calculation
- proposed initial weight or qualitative prior
- whether weight is evidence-derived or merely to be learned
- dependencies/redundancies
- required ablations
- required held-out tests

Prefer a modular architecture where features can be added/removed and tested incrementally.

9. VALIDATION PLAN
Explain how to learn from historical literature WITHOUT contaminating our untouched prospective human validation:
- literature is development evidence
- freeze a model version before new participant outcomes
- tune only on development datasets
- reserve untouched participants/cohorts/hospitals
- preregister primary outcomes
- report ablations: astrology model vs date-only vs time-only vs location-only vs season/demographic baselines
- test incremental value of each feature family
- use held-out replication for discovered interactions

10. PRIORITIZED FULL-TEXT READING/INGESTION QUEUE
Rank the papers/issues/books we should actually acquire and ingest into the humandesign research repository next, based on expected algorithmic information gain.

IMPORTANT ORIENTATION

The core question is:
"What useful predictive structure, if any, has the empirical astrology literature discovered that we can encode and test in a modern, optimized, blinded algorithm?"

It is NOT:
"Has astrology been proven?"
It is NOT:
"Do tight orbs work?"
It is NOT:
"Are time twins similar?"

Those are subquestions inside the larger evidence-mining project.

A null result is useful if it eliminates a feature. A positive result is useful only to the extent that its exact rule can be reconstructed and survives methodological scrutiny. A controversial result is useful if it yields a precise preregisterable hypothesis. The objective is to extract maximum model-building information from the entire empirical record while keeping development evidence strictly separate from untouched validation.