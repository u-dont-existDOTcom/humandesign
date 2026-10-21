# Tibetan astrology source research — exact continuation after T67 (21 October 2026)

## Owner root outcome (OPEN)

User originally said: "ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system", with repeated subsequent "continue". This commits to studying all needed open Tibetan astrology source material and user-supplied Gyurme Dorje (White Beryl + Moonbeams), Philippe Cornu (Tibetan Astrology) and Edward Henning (Kālacakra and the Tibetan Calendar), integrating authentic rules with current Western Lilly/Ptolemy, Chinese BaZi/Zi Wei, Indian Jyotish; independently compute natal and timing rules; freeze them and perform prospective blinded human forward/reverse tests versus chart decoys and non-astrological baseline. Source annotation/documentary counts are NOT scientific success. Do not return only a handoff or ask routine questions when user says continue; execute actual next source/engine work, save incremental checkpoints in **humandesign**.

## Versioned accepted parent and active branch

Accepted previous Tibetan T57–T61 branch: `research/astro-tibetan-t57-almanac-janson-20261021`, exact `645e8e9e9128d5f1c0c8d3602573020625bff37e`. Previously accepted **542** source annotations R0001–R0542 and tested almanac/Phugpa/Tsurphu civil-day engine, **zero** validated human predictive tests.

Current isolated branch: `research/astro-tibetan-t62-henning-originals-planets-20261021`; exact final remote HEAD MUST be fetched fresh. A confirmed intermediate work commit is `bba3d46d0a21ffedf40aa1b7c26fbdb10e36a963`; later commits in this branch are expected for integration/handoff.

**Storage/checkout operational caveat:** `/mnt/hdd` archive disk is near full (less than 1 GB available). Do NOT add another full checkout or delete unrelated worktrees. The accepted local working tree uses `/tmp/hd-tibetan-t57-20261021` on root disk, cone-mode **sparse-checkout only** of `tasks/astro-tibetan-primary-sources-20261021`. This scope does not imply other source files were deleted; verify branch compare via remote. Its sparse state is clean once current files committed. Central GitHub repository visible via `/home/joel/humandesign` and connector. User's source PDF remains attached in current conversation/Library; no source PDF or copyrighted scan in Git.

## Work finished in this session

**Total new historic-documentary records: 53, current cumulative `595`**, all source-only:
- `batches/T62/HENNING_KALACAKRA_TRANSLATION_16_NOTES_V1.json`: TIB-R0543–0558 (16), Chapter V calendrical source passage, version-typed translation vs Henning modern inference.
- `batches/T63/HENNING_KALACAKRA_TRANSLATION_16_NOTES_V1.json`: TIB-R0559–0574 (16), planetary, Rahu, script-syllable and nonfatalistic Mūlatantra passage as QUOTED within Vimalaprabhā. Its actual original Mūlatantra manuscript not separately found.
- `batches/T64/JANSON_PLANET_APPENDIX_16_NOTES_V1.json`: TIB-R0575–0590 (16), Janson 2014 Appendix D.1–D.6 (five planets and lunar nodes).
- `batches/T66/PLANETARY_SOLAR_EPOCH_CONFLICT_V1.json`: TIB-R0591 (1), Janson D.9 literal rational vs own mixed-radix discrepancy.
- `batches/T67/HENNING_NAME_AND_YEAR_CHANGE_SOURCE_CONFLICTS_V1.json`: TIB-R0592–0595 (4), literal 28/27 lunar mansion discrepancy, published 24-versus-28 syllable groups, Sanskrit/Tibetan variants, and conflicting 2;30 year-change interpretations.
- `batches/T65/planetary_phugpa_E1927.py`: **source-faithful mathematical tool only, no additional source annotations**. Original Python Fraction implementation of traditional Phugpa E1927 Mercury/Venus/Mars/Jupiter/Saturn true slow+fast model; selectable **two explicit** solar epoch source representations, Rahu E1927/E1987 6900 lunar-day model. Does not compute observed sky and does not validate any participant's life.
- `verify_t62_t66_planetary.py`: test verifies first 49 unique new IDs, source constants, printed 1995 planetary example (including physically inspected Henning PDF p83), both source epoch variants, lunar node epoch parity, unsupported-policy rejection and all prior Tibetan tests.
- `verify_t67_original_source_discrepancies.py`: test verifies R0592–0595, 112 vs108, 24 printed vs28 nominal source categories, and chains all prior focused tests.
- `CROSS_LANE_INTEGRATION_T62_T67.md`: full source/provenance/test and cross-cultural dependence report. This file is exact handoff.

**Important checked results**:
1. Henning original book, user PDF SHA256 `3fa6c44d4c25c4c69937e9575c0653265e1e77bb1b6923a19ef69ec10f539fd5`. Chapter V physical PDF pp231–314/printed211–294 read in relevant source windows; Chapter II PDF pp77–107/printed57–87 worked 1 March 1995 model. Rare manuscript/Sanskrit original NOT checked.
2. Janson D.9 `s0'=25;9,20,0,97440 (27,60,60,6,149209)` equals exactly `1−458672/6714405`, but published rational fraction prints `1−458772/6714405` (difference about **19.3 arcseconds**). Henning printed p63/one-based PDF83 **visually** says **458672**, with the same 24806-day step. Issue TIB-CONFLICT-012. Both algorithm policies retained; none chosen on human fit.
3. Five planets under supported Henning/Janson mixed radix 458672 in 1995-03-01:
   - Mercury final 20;49,16
   - Venus 19;38,58
   - Mars 8;58,24
   - Jupiter 17;45,33
   - Saturn 23;14,23
   - mean Sun 22;45,37; general day **24806**. This reproduces Henning text to three mixed-radix terms (source model, not physical sky ephemeris).
4. A Kālacakra `Mūlatantra` quotation embedded within Vimalaprabhā (Henning PDF269/printed249) explicitly denies that identical birth instants guarantee identical outcomes and emphasizes actions. Henning's potential-vs-behavior reading is his interpretation. Neither is empirical validation and neither permits posthoc rescues.
5. Henning PDF268/printed248: 28×4=112 mansion-syllable quadrants, but 12×9=108 for signs; translation actually enumerates 24 quartets, source missing four named group mappings. Different Sanskrit/Tibetan versions and White Beryl authority noted but originals not checked. Year-change correction 2;30 is disputed among Bu-ston, Lochen Dharmaśrī, Khedrupje; Henning considers none satisfactory.
6. Source/production separation: no real human astrological predictive tests, no newly promoted natal/planet model, no actual modern sky observation parity, no medical/mortality or ritual advice.

## Test commands

```bash
task=/tmp/hd-tibetan-t57-20261021/tasks/astro-tibetan-primary-sources-20261021
python3 "$task/verify_t67_original_source_discrepancies.py"
# chains verify_t62_t66_planetary.py -> verify_t61_henning_caption.py -> all accepted earlier Tibetan suites.
```

Before owner delivery, **fetch exact current remote branch**, verify source ID sequence 543–595 plus old 542 (595 nonduplicated), source SHA, tests and no source modifications outside Tibetan lane. Commit all generated docs/tests and push branch, then verify remote. Use zero-click local `~/Téléchargements/` for report, handoff, code when local device available; avoid GitHub branch navigation.

## Next authorized executable frontier, no repetition

**Next new historical source note TIB-R0596.** Prioritize:
1. Extend Henning Chapter V primary-translation reading into remaining untranslated/variant astronomical references or read Henning Chapter VI original source numerical variant evaluations; compare with Janson Appendix D and **independent modern astronomical ephemeris** as a *separate* mathematical/physical approximation check (do not conflate Janson+Henning shared derivation with two unrelated traditions).
2. Independently locate and read Sanskrit Vimalaprabhā / original Tibetan sources for the source conflicts (#012–015); maintain variant provenance, do not invent missing syllables.
3. Finish the still-unread parts of user-supplied Cornu and Henning volumes and the large open-access Erlewine manual and additional Janson appendices, then formalize distinct measurable Tibetan astrologic rule families, source-dependent overlap with Chinese/BaZi and Jyotish.
4. Once full chart policy is source-grounded and engineering parity demonstrated, freeze and prospectively score blinded real-human cases vs matched decoy and non-astrology baselines. Retain all misses, source negative results, unresolved branches. **ROOT PROJECT OPEN.**

No further routine owner confirmation is needed for authorized reading, source code and isolated research commits; no paid operations or outreach/publishing/production promotion.
