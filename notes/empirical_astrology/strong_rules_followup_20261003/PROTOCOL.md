# Stronger-rule follow-up: exploratory protocol

## Owner outcome and status
The owner wants a numerology/astrology ruleset with a large, useful separation, rather than weak isolated-number signals, and an explanation of why individual readings appear more striking than group comparisons. Parent outcome remains OPEN. This bounded pass expands and actually executes the rule search; it does not redefine success as a completed audit. No deployment, individual criminal-risk scoring, or conclusions about a person's dangerousness are authorized.

## Source and recovery
Source branch head: 04748c0a25d38d4d34c61147a919f229de69e9a0. Original paired_cohort.csv Git blob: fca43841a83f6efcfe4d1dde66d6887335954c3c. Original run_analysis.py blob: ccfb677972b83ffd08be2926c83ae289d640bf9e. Both were retrieved byte-for-byte; the original <=5-year AUCs reproduce exactly. The 82 pairs contain 62 offender birth years later than their assigned control, 19 equal, and 1 earlier. Control names have initials in 23/82 records, versus 0/82 offender names. These are dataset/source artifacts, not astrological findings.

All these people and outcomes were previously exposed. Every new score is internal DEVELOPMENT evidence, even with properly nested cross-validation. No fresh external test cohort exists in this pass. Cohort labels/status/DOBs remain source-reported, not individually reverified. Nobel achievement is not subjective happiness; that original requested outcome remains unmeasured.

## Method frozen before stronger-model fitting
1. Retain original 82 pairs as an audit arm. Construct a separate maximum-size, without-replacement matching from the same two pools requiring identical birth year and sex agreement where offender sex is recorded. Unknown offender sex remains explicitly unknown and eligible, never inferred from names. Resolve ties deterministically without numerology/astrology features. This reduces the known age artifact but cannot remove geography, education, selection, or name-reporting bias.
2. Numerology families: DOB-based component-reduction and straight digit-sum variants; Pythagorean listed-name expression, vowels and consonants (Y consonant), 11/22/33 preserved; combined date+listed-name features. Normalize Latin diacritics deterministically and never invent expanded initials or birth names. Listed-name results are NOT birth-name numerology validation.
3. Astrology: geocentric tropical Sun/Mercury/Venus/Mars/Jupiter/Saturn/Uranus/Neptune/Pluto positions and major pairwise aspects (0/60/90/120/180 degrees), retrograde and sign/element/modality features. Average features over nine equally spaced reference times spanning -14 to +36 hours relative to UTC midnight of the recorded date. This conservative reference envelope covers possible UTC instants for an unspecified local date; averaging is a modelling convention, not an inferred birth-time probability. No Moon, houses, angles, or exact-time dignity rules. Explicit Moshier flags and returned-mode verification; reduced experimental model, NOT canonical V4.3 or the existing six-rule personal model.
4. Fuse astrology with both numerology families. Search interpretable depth-2/depth-4 trees, depth-2/depth-3 gradient boosting, an RBF support-vector model, and an ExtraTrees ensemble, with fixed parameters in the executable. No outcome-guided changes to this search space after results.
5. Use three repetitions of five-fold outer evaluation. All fitting, feature-family and model selection happen only inside the outer training data, using three inner folds. Keep pairs together; for the exactly matched arm group all people from the same birth year together. Report the selection procedure's outer results, all family results, and apparent in-sample fit separately. Never select the strongest outer score and call it an unbiased final result.
6. Conventional controls: birth year alone and name-format features alone. Include an unrestricted tree and shuffled-label fitting as memorization diagnostics, not proposed valid models. A large fitted score without large held-out separation is not the requested strong signal.
7. If practical, apply the same predeclared date-only search to independently redrawn same-birth-year calendar controls. These are null/calendar checks, not happier people and not additional independent cases.

## Large-effect working benchmark
Assistant-selected operational benchmark, not a universal scientific threshold: at least 75% held-out balanced accuracy and/or AUC >=0.80, with meaningful coverage. This avoids elevating a tiny nominal p-value into the owner's desired effect. A score crossing it is a candidate, not validation; confound checks and a genuinely new cohort remain necessary. Weak residual findings are logged, not promoted as the next priority. No exhaustive absence claim follows from a bounded unsuccessful search.

## Activated controls and enforcement
- Current UDA AGENTS.md and LESSON-INDEX.md loaded this turn. Reproducibility: exact source blobs and baseline replay before causal comparison.
- Task-time lesson activation: owner correction changes goal from weak-number replication to richer large-effect search; executable configuration must match this protocol.
- Research-before-reinvention: COMPOSE established tree/ensemble/SVM models and nested CV, not invent a new scoring ideology. Primary sources: scikit-learn nested-CV and ensemble documentation; Cawley and Talbot, JMLR 2010, On Over-fitting in Model Selection.
- Person/group separation and honest uncertainty: no synthetic or in-sample success as human validation; names and outcomes excluded from astro feature generation.
- Parallel write isolation: this branch only, additive artifacts; no merges, production edits or alteration of prior historical files.
- Delivery: save code, aggregates, data/input hashes, executed logs and a recovery note; provide a usable report rather than repository identifiers alone.

## Prior-work sources
https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html
https://www.jmlr.org/papers/v11/cawley10a.html
https://scikit-learn.org/stable/modules/ensemble.html

## Unfinished boundary
Birth-time-dependent astrology and verified full-birth-name numerology require better inputs. The individual-reading discrepancy requires blinded own-profile-versus-decoy comparisons using the SAME reading protocol; broad outcome labels are not a substitute for that test. Do not diagnose the owner's experiences as bias without testing them.
