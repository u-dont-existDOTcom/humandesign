# Primary directions: Lilly 1647 source-visible dignity components

**25 October 2026 — research checkpoint.** This supporting Western research lane is NOT the owner’s ultimate goal. The root goal remains **OPEN**: compute historically differentiated Western, Hellenistic, Jyotish, Chinese and other astrology rules, freeze them, then test concrete chart-derived predictions on genuinely untouched, prospective human data against controls. No human natal data or event outcomes were examined here.

## What was recovered

Six original first-edition pages of William Lilly's *Christian Astrology* (London 1647, printed pp.101–105 and 115) are now preserved in `original_1647_pages/` with SHA-256 provenance. They contain the five positive essential dignities and three adverse conditions, an exact 12-sign degree table, and a broader positional/accidental score sheet. See `DIGNITY_SOURCE_EVIDENCE.md` for author text versus research interpretation. The older original direction-effect pages 654–655 and 670 are preserved in earlier checkpoint branches.

The program models *only separately checkable components*, rather than silently converting them to a full natal strength judgment.

| Lilly source-visible factor | Isolated tabular points |
| --- | ---: |
| Domicile | +5 |
| Exaltation | +4 |
| Correct day/night triplicity ruler | +3 |
| Correct degree-based term/bound ruler | +2 |
| Correct ten-degree face ruler | +1 |
| Detriment | −5 |
| Fall | −4 |
| Peregrine (no positive essential dignity) | −5 |

Each sign’s five successive terms and three faces are transcribed from Lilly **p.104**. The day/night triplicity distinction uses the nativity's geometric solar horizon, a clearly named modern astronomical implementation rather than an unverified historical sunrise/sect convention. The source specifically requires the watery triplicity to belong to Mars in either sect. The source’s table calls itself Ptolemaic, but that description is **not** permission to substitute differently transmitted Ptolemaic bound tables.

The **accidental house-only** score is reported separately, using mathematical Swiss Placidus position: houses 1/10 +5; 4/7/11 +4; 2/5 +3; 9 +2; 3 +1; 6/8 −2; 12 −5 (first-edition p.115). This reconstructed house assignment is not automatically the full Argolus/Lilly direction algorithm.


## Frozen synthetic comparison: exact earlier 96 charts and 216 contacts

The source contract and six source scans were **committed and pushed before** recalculating the 96 existing synthetic natal skies. This is the same month × latitude panel with existing frozen input plan `948a1289b5f891c7f7870632ad116fb16ea6409d1bed575483c07c9901fbc0d0`. There is no new sampling, event history, source-rule fitting or hit selection.

| Output | Observed |
| --- | ---: |
| Synthetic charts re-examined | 96 |
| Classical planetary essential+house rows | 672 (96 × 7) |
| Previously declared direction contacts with promissor components attached | 216 |
| Day / night charts by modern solar horizon | 48 / 48 |
| Favorable Midheaven–Jupiter *aspect* contacts | 47 |
| Of those 47, Jupiter in domicile or exaltation | 10 |
| Of those 47, Jupiter in an angular house | 18 |
| Complete Lilly 'Jupiter strong in radix' determinations | **0** |
| Real-world outcomes / human predictive validations | **0** |

The 10 and 18 refer to different components and are **not** independent tests of astrology, not conditional event probabilities, and cannot be used to choose retrospectively which rules count. Each of the 47 was already present in the 216-contact diagnostic before this evaluation. Exact per-chart sign, face, term, sect, visible positive and negative factors, house placement and source-rule contact are retained in the CSV and JSON outputs.

## Why full historical natal strength remains unresolved

Lilly p.115 explicitly includes receptions by house/exaltation as alternative ways to obtain dignity points. His broader accidental table includes speed, direct/retrograde planetary motion, combustion, solar beams, aspects, and fixed-star contacts. The currently reconstructed source fields do **not** contain all those conditions.

At original pp.654–655 the effects of a direction depend on BOTH natal significator and promissor, and Lilly allows a direction to manifest little or nothing. The significator is often the *Ascendant or Midheaven angle*, for which scoring a planetary ecliptic dignity is not an equivalent judgment. The original favorable Jupiter–Midheaven aspect at p.670 is conditional on Jupiter's strength, but no complete, unique source-backed cutpoint has been established for this experiment. Thus every computed `full_natal_strength` remains **null/unresolved**, despite positive or negative partial factors.

**Full 1647 Argolus direction conventions, particularly the historical sense of direct/converse, remain unresolved**. Neither the p.104 dignity table nor the current Swiss house calculation authenticates the prior diagnostic's shortest-signed-arc, one-degree-per-year method. No individual birth-time rectification, recommendations, or human outcomes are attempted.


## Reproducibility and remaining work

- `DIGNITY_PRE_FREEZE_CONTRACT.json`: frozen input cohort, named source fields, exclusions and prohibited interpretation changes.
- `DIGNITY_SOURCE_EVIDENCE.md` and `original_1647_pages/`: six original public-domain Lilly source images with page identifiers, not a modern paraphrase disguised as primary evidence.
- `src/hdmatch/astrology/lilly_essential_dignity.py`: typed, pure essential-table calculation and separate source-visible house-position components; does **not** overwrite the existing primary-direction engine.
- `tests/unit/test_lilly_essential_dignity.py`: boundary, sect, historical numerical example, original sign table, positivity/debility, uncertain full strength and Swiss integration checks.
- `build_source_visible_dignities.py`: reads ONLY the frozen prior 96 inputs and previously calculated 216 source-rule contact keys, verifies Swiss source-file hashes/flags, and emits the reports below.
- `PARTIAL_DIGNITIES_PLANET_ROWS.csv`: 672 planet rows, including empty/unknown complete-strength verdicts.
- `PARTIAL_DIGNITIES_CONTACT_CROSSWALK.json`: 216 links to the unchanged prior direction contacts; no new age/window choices.
- `PARTIAL_DIGNITIES_SUMMARY.json`: per-planet partial-score histograms, house and sect counts, conditional-Jupiter components, and explicit zero complete verdicts.
- `verify_dignity_replay.py`: recomputes all 96 charts and requires all three report files to reproduce **byte-for-byte**; `DIGNITY_REPLAY_VERIFICATION.json` records that evidence.

The correct next study-design step is not to label high partial scores as confirmed predictions. Source-defined reception/accidental and direction-orientation variants must first be completed or declared unresolved, then outcomes, opportunity denominators, birth-time uncertainty intervals, competing astrology rulebooks and null controls must be frozen. Only genuinely untouched human observations can test predictive validity. This research subtask contributes source features, *not* a substitute finish line.

The 96-chart panel is nonrepresentative and already a DEVELOPMENT engineering dataset. Do not adjust the score or cutoff to make known cases look better, and do not reinterpret negative/missing indicators as support.

The project-level next empirical test options and unresolved acceptance conditions are detailed in `NEXT_EMPIRICAL_GATE.md`. It is an open study-design handoff, not a preregistered or completed human trial.
