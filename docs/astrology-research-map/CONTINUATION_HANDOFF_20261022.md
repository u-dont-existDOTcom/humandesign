# HumanDesign cross-tradition map + Maya source-first research — continuation handoff

22 October 2026. **OWNER SCIENTIFIC ASTROLOGY GOAL REMAINS OPEN.** Continue source-grounded Western/Ptolemy/Lilly, Indian Jyotish, Chinese BaZi/Zi Wei, Tibetan, newly added Maya and source-independent traditions; compute authentic natal/chart rules with explicit calendar/clock policies; freeze source-justified, falsifiable question outcomes and matched chart/time/nonastrology baselines before collecting real answers from untouched consenting humans. No source-annotation, chart-engine software parity or synthetic score is evidence of actual real-person predictive accuracy.

## Saved map — what was absent and what now exists

Before this iteration the repository had an HD-only `ARCHITECTURE.md`, a useful HD `reference/core/MAPPING_V2_EVIDENCE_PROTOCOL.md`, existing survey/answer mapping library, individual Chinese/Jyotish/Tibetan source inventories and some domain crosswalks. **It had no single cross-tradition source-to-question dependency map** showing original tradition provenance, ritual-versus-natal distinction, chart-feature calculation, chosen observer question and human test denominator.

This isolated research branch `research/astro-mesoamerica-source-map-20261022` (fork of accepted prior book-status branch c0d63a1e520b9420206e3aaa59199207d99621f3) adds that missing operational map without overwriting main/other research branches:
- `docs/astrology-research-map/README.md`: living one-screen Mermaid source→trait→chart→predeclared outcome→prospective human experiment overview plus specific evaluation/gate flow, cross-domain alignment notes.
- `WORKFLOW.mmd`, `SOURCE_TO_TEST_GATES.mmd`, `TRADITION_DEPENDENCIES.mmd`: three editable source-controlled diagrams (overview, inference gate, 13-node historically-dependent lineage).
- `TRADITION_COVERAGE_V1.json`: **16** source-family/risk/priority statuses and **11** source-dependency links, from Modern HD/Greek/Arabic/Babylonian to Indian, Chinese, Tibetan, K'iche'/codex Maya, Nahua and quarantined modern Dreamspell; explicit 0 human validations. Literary source cross-tradition agreement is *not* independent scientific confirmation if direct historical borrowing is plausible.
- `CLAIM_TRACE_SCHEMA_V1.json`: model-neutral source↔exact-claim↔chart-policy↔observable/negation↔null↔decoy↔actual-human-evidence schema. `CLAIM_TRACE_EXAMPLE_MAYA_E_V1.json` demonstrates a source-only E/Eb' travel disposition, intentionally missing K'iche' epoch, calibrated direction, respondent instrument and confirmatory pre-freeze.
- Root `ARCHITECTURE.md` has an explicit one-line link to this *new map*, without modifying canonical HD V4.3 scorer, personality question survey, participant data, relationship model or production code.

## Maya books and free first reading

Ranked primary source catalog `MAYA_SOURCE_CATALOG_V1.json` has **11** named evidence references, their rights/access/authority and usefulness; readable plan `MAYA_READING_AND_RESEARCH_PLAN.md`. The most important:
1. **Komon Tohil, K'iche' Zunil daykeepers**, Smithsonian living-source original “The Meaning of the Days in the Maya Sacred Calendar,” free original 3-page PDF **read all three pages**. We preserved **20** literal K'iche'/Yucatec day-name correspondences, original page positions and **seven exploratory, quarantined** behavior/outcome candidate claims in `MAYA_FIRST_SOURCE_WITNESS_V1.json`. No source claims were added to runtime or misrepresented as human results.
2. **Barbara Tedlock, Time and the Highland Maya**: most important scholarly K'iche' daykeeper ethnography, 1992 revised, buy/borrow; no full legitimate free copy confirmed. Ancient vs contemporary regional practice distinctions essential.
3. **Dresden Codex** institutional original facsimile free via SLUB/FAMSI; ancient Maya Venus/eclipse/ritual/astronomical source, NOT necessarily natal personality source; **Harvey & Victoria Bricker, Astronomy in the Maya Codices** essential critical companion (2011, 907 pages, no free complete full text verified).
4. Aveni *Skywatchers*, David Stuart *The Order of Days*, Vail+Aveni *The Madrid Codex* and scholarship on GMT584283 calendar correlation as meaningful second-tier sources. **Kenneth Johnson's modern Maya horoscope presentation and Argüelles Dreamspell must be separate modern hypotheses, not attributed uncritically to classic codices.**

Free data/reference: Smithsonian Calendar System, original practitioner PDF and Smithsonian date converter; Dresden codex institutional original facsimile; open radiocarbon study on GMT Long Count↔Gregorian correlation.

## First Maya calendar tool (narrow evidence)

`docs/astrology-research-map/maya_calendar_reference.py` computes **date-only** lowland Long Count, 260-day Tzolk'in and 365-day Haab for declared proleptic Gregorian civil dates and **explicit correlation** 584283 or 584285, never selected after seeing personal outcomes. Fails closed on birthdays with time (datetimes), unsupported epochs, invalid correlation, and refuses generating any personality forecast. A K'iche' label is a **linguistic name correspondence only**, not an independently established living K'iche' day-count epoch.

`test_maya_calendar_reference.py` **12/12 green** checked 2012-12-20/21 and 2000-01-01 Smithsonian-style reference examples, 260/365/18,980-day calendar repeat, leap day, separate 584285, birth-hour exclusion. `test_research_map_integrity.py` **12/12 green** verifies 16 source families, 11 Maya references, 20 names, seven exploratory claims not scored, Mermaid maps and new schema/example, no human predictive validation and link in existing architecture. **Combined new 24/24 local focused tests PASS**. This is algorithmic reference-date consistency, **not K'iche' traditional continuity or scientific prediction**.

## Gaps and next actual research

**High priority additional systems not present as accepted full source-first reading:** Vettius Valens and Dorotheus (Hellenistic beyond Ptolemy), Rochberg *Babylonian Horoscopes* (free NYU/ISAW digital), medieval Arabic/Persian Abu Ma'shar and al-Biruni, living and historical Nahua/Aztec Tonalpohualli (Elizabeth Hill Boone *Cycles of Time and Meaning*, Codex Borgia) **distinct from Maya**, and a clearly labeled modern Western psychological astrology source (e.g. Robert Hand) if goal includes self-reported personality. Chinese Qi Men, Malagasy Vintana and other classes optional only when source/documented outcome relevance established; don't reflexively add an unlimited list.

Reading alone isn't the scientific objective: previous Lilly13,271+Ptolemy1,066, Chinese BaZi230+ZiWei1059, Indian five Jyotish432, Tibetan595 original-source annotations **do not equal real human predictive validations**. Best immediate next Maya frontiers are (a) pin independent Smithsonian/Maya published day-epoch anchors and Maya original codex folios, (b) read Tedlock and Brickers via library/authenticated source, (c) operationalize one or two nontrivial K'iche' daykeeper candidate claims into a context-aware question, with reverse controls and birth-date shuffle, but **do not use participant data/score until preregistered and culturally appropriate cohort/consent**.

## Durable state and guarantees

All new files live on the isolated `research/astro-mesoamerica-source-map-20261022` branch. No existing source registry, formal/production model, sex/health/medical/financial recommendation, survey answers, owner DOB, personal sample or default-main state touched by the research artifacts beyond a root HD-architecture pointer on this branch. No paid books were bought, and no modern copyrighted books copied to GitHub. Future reader should fetch exact current branch HEAD and these current files, run `python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -v`, reconcile accepted source branches without overwrites, preserve cross-lane condition differences.

**Real human blinded astrological predictive validations: 0; new production astrology rules: 0.** The core scientific parent goal remains OPEN. A visually coherent map is *not* proof the end-to-end human experiment is implemented.
