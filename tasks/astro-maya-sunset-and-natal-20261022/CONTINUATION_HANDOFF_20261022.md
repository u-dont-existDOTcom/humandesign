# Astrology source-reader handoff — Maya sunset/Noj cross-community batch

**Date:** 2026-10-22. **Parent empirical owner outcome OPEN:** read sources across multiple traditions, calculate reproducible birth features, and actually test frozen falsifiable chart-to-human predictions against untouched participants and matched non-astrology baselines. No source annotation/engineering pass fulfills the last step.

## Branch and preserved baselines

Current isolated worktree on owner's laptop:
owner-local isolated sparse checkout (available from the new GitHub research branch)
branch `research/astro-maya-sunset-and-natal-audit-20261022`, based on accepted preceding source branch `research/astro-maya-tedlock-madrid-witness-20261022` at `d72cf205f7494fa49012c822752f018c3b66df60`. Prior 16-tradition reconciliation, 11 historical dependency edges and **one canonical Mermaid map** left intact; no prior accepted SHA-pinned reconciliation outputs touched.

## Original literature checked and evidence distinction

1. Read Guatemalan government original Spanish 2016 119-page source by **Alejandro Garay and Igor Xoyón**, *Armonización de los calendarios mayas*, printed pp 39–44, 58 and 86: https://mcd.gob.gt/wp-content/uploads/2017/02/Armonizacion-Maya.pdf. Original PDF retained privately on authorized owner machine; SHA-256 `16950ebf88f4bb7f0e94315e516aefdf1e99ae3cc3652e78948a2da96454fdf2`. These are author/ethnographic/epigraphic calendrical claims, **not a natal truth**.
2. Original Komon Tohil/Zunil three-page living K'iche' daykeeper PDF SHA-256 `eb02e1359329e7e4fcd90527f7f38539940f78e190c60f2dae2ea525eae0fbe7`; kept private, linked and accurately quoted in limited labels only.
3. Barbara Tedlock's *Time and the Highland Maya*, original owner EPUB prior verified SHA `95c88db1d7310e2b247a7ed5b8f15136abb27064ed49b3c3a33949ce7e607081`, expanded reading printed p53, p110–130, p133–146, not full book.
4. Contrasting modern scholarship: Cano Contreras et al. (2020), *Estudios de Cultura Maya* 56, DOI `10.19130/iifl.ecm.2020.56.2.0007`: practices have regional/specialist variation.

## New material that is actually reproducible

- `docs/astrology-research-map/MAYA_SUNSET_AND_NATAL_COMMUNITY_AUDIT_20261022.md` — owner-readable research report. Clearly distinguishes sacred Cholq'ij **after sunset** and solar Ab' **at dawn** in Garay/Xoyón's documented argument, as distinct from Gregorian midnight, and says source's workshop **>90% agrees with celebrating yearbearer on 5 K'ayab', NOT with day-clock sunset**.
- `docs/astrology-research-map/MAYA_SUNSET_BOUNDARY_SOURCE_WITNESSES_V1.json` — 14 source-labelled day/phase records (8 civil dates), 2016 book SHA, 2020 scholarly limit, source classes and explicit human-zero counters. Some are author-generated examples/derived next days, not 14 independent observations.
- `docs/astrology-research-map/maya_sunset_boundary_sensitivity.py` — standalone **unscored** date-only sensitivity. Inputs: Gregorian civil `date`, *externally observed* `before_sunset`/`after_sunset`/`unknown`, declared GMT 584283 or 584285. `unknown` returns both signs and ABSTAIN. Does not calculate astronomical sunset, Haab, Long Count, personality, or birthplace offsets. All statuses ineligible for human scoring until birth-clock policy supported.
- `docs/astrology-research-map/MAYA_MOMOSTENANGO_ZUNIL_NATAL_DOMAIN_CROSSWALK_V1.json` — **20/20** natal day-name pairs with historic Momostenango and present-day Zunil page anchors and discordant candidate source domains; no hidden assumption of a single universal Maya natal-personality rule. Tedlock/Momostenango Noj **innovative thinker** is NOT a duplicate of Zunil No’j natal prudence; Zunil Imox explicitly has creativity. Tedlock Toj illness/debt vs Zunil Toj mediation/self-teaching conflict; sexual/clinical stigma quarantined.
- `test_maya_sunset_boundary_sensitivity.py` 10 new date/source/abstention/phase and safety scope tests; `test_maya_natal_community_crosswalk.py` 5 new source-variant preservation tests. **61/61** map-focused tests passed (46 existing + 15 new).
- Updated `docs/astrology-research-map/README.md` and owner guide with newest evidence and URLs. Original one canonical map source unchanged.

## Actual scientific implication and remaining decisions

**Important:** The Noj task remains **NOT_FROZEN** and source-local to Tedlock/Momostenango, not a cross-community prediction. A preliminary normal-power calculation at fixed prevalence ~1/20 suggests an unscreened cohort of **1,836** for detecting standardized `d=0.3` with two-sided alpha=.05, 80% power and no multiple comparisons/attrition. This is a hypothetical design input, not a measured effect or recruitment authorization. Prefer an existing mechanically mature chart tradition for earliest untouched prospective cohort if this single candidate is impractical.

Next safe permitted reading: check independent Momostenango and Zunil current practitioner policy on *birth-specific* day-change (not just ritual start); record era and daylight/dusk time uncertainty. Select and freeze **one source-specified nonstigmatizing measure**, content-check proxy, lock questionnaire, chart/decoy, source/hash and comparator before untouched consented participants. Literature-based claims that day names influence a baby's character have **NOT** been tested as evidence in humans.

## Completion status

Source-reading increment may be accepted if tests and publication push readback pass; overall owner outcome **OPEN**; 0 actual human forward/reverse blind validations; 0 production astrology rule promotions. No booked participants, no changed HD V4.3 engine. Avoid duplicating old sibling readers, or treating a source-derived result from the same formula as genuinely independent truth.

Run:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -v
```
Then check `git diff --check` and original/added file hashes and cold-extracted ZIP test. Owner ZIP should be placed in `~/Téléchargements`; do not distribute copyrighted originals.
