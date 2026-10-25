# G35 handoff — Gene Keys official source audit and HD-geometry crosswalk

**25 October 2026. ROOT OUTCOME OPEN:** historical and modern natal chart traditions source-reconstructed, then frozen as specifically falsifiable behavior/event predictions **before** consenting untouched humans answer, compared against chart-decoy and nonastrology baselines with negative/tie reporting. **0 real Gene Keys predictive or contemplative intervention validations**. Gene Keys belongs as an HD-derived *interpretive* lane, not as an independent 17th astronomical datapoint.

## Bootstrap and approved branch isolation

Read current default `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`, then `humandesign/AGENTS.md`; [G35 complete report](GENEKEYS_G35_OFFICIAL_SOURCE_CROSSWALK_AND_TEST_PLAN_20261025.md), [source/testing registry](GENEKEYS_G35_SOURCE_STATUS_AND_TEST_PLAN_V1.json), [six synthetic crosswalks](GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json) and this document.

G35 child branch `research/astro-genekeys-g35-source-crosswalk-20261025`, worktree `/home/joel/development-worktrees/humandesign/astro-genekeys-g35-20261025`, descends from verified **Hellenistic C34 synthetic-freeze** accepted commit `bc43c5404f8b185103fd5e8c0b413a7b00bf0679`. The root `participant-session-v1` is a separate exclusive writer; **do not alter its active-task lock, production scorer, human intake or other current writer’s state**. All new code/registries under `docs/astrology-research-map/`, read-only references to existing `src/hdmatch/chart`. No user/other real personal DOB or responses, subscriptions, paywalled books, health/relationship predictions or unverifiable metaphysics promoted.

## Actual G35 results

- Primary Gene Keys official sources directly examined: https://genekeys.com/resource/astrology/ ; https://genekeys.com/how-to-read-your-profile/ ; https://genekeys.com/docs/what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/ ; https://genekeys.com/docs/whats-a-pre-natal-design-unconscious-planet-why-88-degrees/ ; https://genekeys.com/audios-more-information/ . These support **11 core Golden Path spheres** and official natal/design planet mapping; **three extra** Creativity, Relating, Stability separately documented. Activation sequence 4, Venus 6, Pearl 4 referenced spheres but only **11 distinct** because repeated Purpose, Vocation, Life’s Work/Brand.
- A Gene Key is the **same key number as the corresponding incumbent Human Design Rave gate**, each 5.625° and six lines of 0.9375°. New `genekeys_g35_source_crosswalk.py` strictly consumes existing `GateActivation` and `ChartComputation` plus verified local Swiss-source metadata. It checks gate/line labels vs physical longitude, all required natal/design planets, duplicates, genuine 180° Sun–Earth opposition, mirrored partner lines; outputs sphere→numeric key/line and sequences **without any copyrighted 64-key text or asserted interpretation of persons**.
- Actual public solar reference checks from Gene Keys Pulse: **2020-01-06 GK54** and **2026-10-15 GK32, Oct20 GK50, Oct26 GK28** all match the incumbent Swiss/Rave chart gate numbers for 12:00 UTC. This is limited wheel corroboration, not verified official full profile parity.
- **Source ambiguity:** official help's title asks *Why 88 degrees?* while its explanation calls the prenatal time **about 88 days before birth**. The incumbent Human Design root solver uses exact **88° solar arc**, which is not exactly 88 calendar days. The six strictly **synthetic** 2020–2021 research profiles compare both conventions: calendar-time differences **0.19–3.56 days**, different numeric prenatal Gene Keys **1–4 of eight planet labels**, different lines **3–7**. Sun/Earth pairs are redundant, not independent. Do **NOT** select “whichever looks right” from human biographies, or claim the official Free Profile calculator exactly matches our HD root without a reference output.
- Official Gene Keys positions reused from HD should **not** count as an independent new natal sample. What is potentially distinct is Richard Rudd’s Shadow/Gift/Siddhi contemplation/Golden Path interpretation. The 64 complete primary interpretive essays **were not ingested** and no frozen personality/behavior mapping exists. No human predictions, accuracy, trials or biological frequencies verified.
- Two possible real human experiments are DIFFERENT: (A) prospective blinded Gene Keys interpretive predictions above matched Human Design interpretation and chart-decoy/natural baselines, **only after source→behavior mapping frozen**; (B) randomized Gene Keys contemplation vs an attention-matched reflective-control intervention (tests usefulness, NOT natal chart validity). Both remain **not started** and are not compulsory extra gates for finishing the Hellenistic C34 subtask.

## Bounded next work aligned with original owner scientific outcome

1. **Public official calculator parity**: obtain a small lawful *synthetic* set from Gene Keys’ actual Free Profile output if its public authorized interface permits. Check 11 sphere Gate/Line outputs against the existing HD-derived crosswalk and resolve exact solar-design method. Otherwise retain `UNVERIFIED`, not a blocking new parent-science requirement.
2. **Source-to-behavior interpretations**: collect rights-respecting official Rudd primary descriptions for *selected* keys/lines and distinguish testable and untestable claims. Only preregister explicit, directionally scored behavior/outcome predictions that survive source paraphrase review. Do not reproduce full copyrighted book, invent explanatory genetics, or score generic resemblance as outcome success. Prefer breadth of the interpretive source before selection on life cases.
3. **Prospective comparison**: one independent participant cohort and one chart input may feed HD and Gene Keys separately as **dependent competing interpretation models**; never count their same gate position as two independent human predictions. The participant-session-v1 live branch is owner-locked and inaccessible as a validation playground; real consent, private custody, frozen predictions and outcomes require their own actual permissions. Keep human outcome **0** until undertaken.
4. Preserve **C34 Hellenistic source-only mock-freeze** and C33 Ptolemy marriage draft unchanged. No Gene Keys added to production V4.3 baseline; parent goal remains OPEN.

## Test/replay commands

Inside G35 worktree using installed project Python and pinned local source files:

```sh
PYTHONPATH=src /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_genekeys_g35_*.py' -v
PYTHONPATH=src:/tmp/c32-independent-erfa C32_IERS_C04_PINNED_FILE=/tmp/c32-eop-c04-mirror.txt /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py'
PYTHONPATH=src /home/joel/humandesign/.venv/bin/python docs/astrology-research-map/genekeys_g35_synthetic_profiles.py --ephemeris-dir /home/joel/humandesign/data/ephemeris --out /tmp/g35-synthetic-replay.json
```

The first group contains **23 new G35 tests**, verified focused before publication. C34 inherited Hellenistic suite had **367** tests. Verify exact final counts, identical synthetic JSON, SHA hashes, commit/push and clean worktree before announcing publication. No real human predictive results. The user’s original source completeness/empirical testing objective is still OPEN.


## Final accepted research checkpoint (verified)

**23/23 new Gene Keys G35 tests** and **367/367 inherited Hellenistic source/engineering tests** PASSED in the existing project Python + pinned Swiss/optional SOFA-IERS research environment; exit zero, **390 combined separate test cases**. Six actual synthetic chart crosswalks regenerated from the existing strict Swiss files were byte-identical to `GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json`; source-body digest `e5f47a5debd6101219a33929cbdace2fc7ddf17788ef08bb387c9a13f839a303`. No real chart, Shadow/Gift/Siddhi predictive behavior mapping, official Free Profile parity, live participants, randomized practice trial, production promotion or active exclusive task mutation occurred.

Source-level code rejects Sun/Earth opposition errors, wrong gate/line physical longitude, missing planet spheres, duplicate activations, a Python boolean masquerading as an integer gate, and any attempt to count shared HD positions as independent Gene Keys evidence. Keep this negative/unknown status when handing off.
