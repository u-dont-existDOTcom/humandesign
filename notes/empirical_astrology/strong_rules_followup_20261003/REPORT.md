# Strong-rule search: findings and interpretation

**Date:** 3 October 2026. **Status:** completed exploratory computation and independent review; no strong predictive ruleset found. This is not an individual criminal-risk tool.

## Bottom line

A relatively short fitted decision tree correctly classified **80.5% of the 164 known records**, but the same tree-building procedure averaged only **52.2% balanced accuracy on held-out records**. An unrestricted tree achieved 100% on the real labels and on every one of ten shuffled-label datasets. Strong-looking fitted rules were easy to obtain; strong held-out discrimination was not.

The expanded search tested interactions, aspects, listed-name numerology, two DOB reduction conventions, and six nonlinear model configurations. None produced the requested large predictive effect. This does not establish that no possible astrological ruleset works, nor does it resolve the user's observation that individual readings appear striking.

## What was actually expanded

The first pilot was a limited date-only, predominantly additive analysis. It was not the full personal-reading method and did not test name numerology. Its negative result was therefore not a comprehensive test of the user's idea about combinations.

The new predeclared search offered **433 features**: 72 DOB-number indicators, 39 listed-name-number indicators, and 322 astronomical features. The latter include positions, sign/element/modality information, retrograde fractions and major pairwise aspects for nine astrological bodies. Two decision-tree depths, two gradient-boosting depths, a radial-basis support-vector model and an ExtraTrees ensemble were tested across five feature families.

Model selection occurred inside the training portion of each outer fold, using three inner folds. The outer evaluation used five folds repeated three times. Original pairs stayed together; the separately rematched arm kept all people from the same birth year together. Reported scores are internal development estimates: these people were already known to the project, not a fresh external validation sample. Repeating folds does not create more independent participants.

The working large-effect benchmark was at least 75% held-out balanced accuracy or AUC 0.80. This was an operational interpretation of the user's preference, not a universal scientific threshold or an excuse to promote a confounded result.

## Held-out results

The original pool contains **82 source-listed offenders and 82 Nobel-laureate controls**. A separate maximum-size rematching within those same pools produced **51 exact-birth-year pairs**, respecting sex agreement where offender sex was recorded. Sex remained unknown for 15 of those offenders. Geography and other life circumstances were not matched.

| Inputs supplied to the model search | Original 82 pairs | Exact-year-rematched 51 pairs |
|---|---:|---:|
| DOB numerology | 55.3% | 50.7% |
| Listed-name numerology | 46.7% | 44.4% |
| DOB + listed-name numerology | 47.8% | 49.3% |
| Expanded astrology including aspects | 55.5% | 47.1% |
| All three together | 53.0% | 48.4% |
| Training-only selection across all families | 54.5% | 45.8% |

These are mean outer-fold pooled **balanced accuracies**, with 50% the chance benchmark. Below-50 results are not a newly discovered reversed rule: any decision to reverse the rule must itself be selected inside training and tested independently. The study did not establish a useful inverse rule.

The rematched arm differs in sample composition and grouping as well as matching. Its lower scores cannot, by themselves, establish that birth-year confounding caused the entire original result.

Three random-calendar control redraws were also completed. They reuse the same offender cases and are not independent replications or samples of happy people. Their selected-pipeline balanced accuracies were 51.8%, 56.1% and 46.3%.

## The strong-looking fitted rule

A diagnostic tree, limited to at most four sequential decisions on each path, reached **80.5% apparent accuracy** and AUC 0.848 on all original records. This is not a universal four-clause rule: it is a branched tree with ten terminal leaves.

Refitting that exact depth-four procedure without allowing it to see each held-out test fold produced **52.2% average held-out balanced accuracy**, AUC 0.514. The full-data fitted tree itself has not been evaluated on a new external cohort.

The matched-sample version achieved 71.6% apparent accuracy and 45.1% held-out accuracy. With shuffled labels, depth-four trees averaged 73.2% apparent accuracy on the original pool and 78.7% on the smaller matched pool; some reached 84.1% and 91.2%, respectively. These are diagnostic simulations, not p-values for the real-label fitted tree. An unrestricted tree fitted all ten shuffled-label datasets perfectly in each arm.

Thus an impressive description of already-known cases is not the same observable result as an algorithm predicting withheld cases. Flexible model selection is a known source of optimistic estimates; nested evaluation separates fitting from evaluation [1,2].

## Important weaknesses in the original comparison

**Birth years were poorly balanced.** In 62 of the 82 original pairs the offender was born later, in 19 the years tied, and in only one the offender was born earlier. A trivial rule that selects the younger member of a pair reaches **87.2% pairwise accuracy when ties count half**. This assumes one member from each source cohort; it is not a standalone individual classifier and is not comparable to every other metric here. It demonstrates a sampling artifact, not astrology.

**Name representation differs.** Twenty-three control names contained initials, versus none of the offender names. A name-format-only baseline reached 65.2% held-out balanced accuracy in the original arm and 66.7% in the matched arm, exceeding all numerology/astrology families. The source difference is demonstrable; the experiment does not isolate how much of that baseline is attributable to initials alone.

**The outcome was not happiness.** Nobel selection documents an award, not subjective well-being. Offender labels, DOBs and current imprisonment were not individually reverified in this follow-up. The contrast remains source-listed offenders versus selected laureates, not a validated happiness outcome or a verified current-prison census.

## What this says about the individual/group discrepancy

The previous work changed both the prediction method and the target. A rich personal description, a symbolic life-timing interpretation and a binary offender-versus-laureate classifier are different tests. Even a hypothetical perfect predictor of one personality trait would not necessarily identify a complex life outcome.

Weak marginal associations do not logically exclude strong combinations. As a mathematical example, two binary inputs can individually be unrelated to a class while the rule "exactly one of them is present" determines it perfectly. That is why it was appropriate to try interactions. The present bounded interaction search did not find a stable large effect; it was not an exhaustive search of all traditions, features or possible models.

The astronomical model omits Moon, houses, angles and exact birth time. Name calculations use the listed public names, not independently verified full birth names. Therefore this is **not the same ruleset and input quality as the complete personal readings**. It would be an overstatement to say this experiment disproves those readings.

Conversely, a reading that feels accurate has not yet demonstrated that it fits its recipient better than equally well-written readings generated from other people's data. A true statement can be non-discriminating. This distinction appears in the original personal-validation literature [3], but it does not diagnose the user's particular experiences as bias.

The unresolved possibilities include a genuine person-specific effect missed by the coarse outcome, a mismatch between methods, broad applicability, and information/interpretation flexibility. These need different tests; they should not be silently traded off against one another. A trait-level success would not establish an ability to predict murder or happiness, and a negative outcome-label result does not settle trait-level matching.

## The next discrimination, prepared but not run

Use the exact personal-reading protocol that appears successful, freeze its rules before new participants, and compare each person's true-data reading with four matched decoy readings. Generate every reading without personality/history information or prior chats, conceal identifying birth/name/sign clues, equalize presentation, and ask for a first-choice ranking before any reveal. Record recognition of astrology/number clues separately.

One-in-five identification has a 20% chance benchmark when positions are randomized and ties are scored by a predeclared rule. Strong performance could therefore be visibly large rather than a weak significance result. Each participant contributes one primary observation; claims within a reading and repeated ratings are not independent extra people.

The companion **PERSONAL_READING_TEST.md** specifies the data boundaries and scoring. It has not been run, and no participant has been contacted. Fresh participant agreement and blinded ratings are needed; the present cohort does not supply them. This preserves the personal-reading question without pretending it has already been validated.

## Review and limitations

Claude Opus 5.5 independently examined the protocol, code and aggregate packet through a neutral Claude Code subscription session with no tools. The requested effort was max; the model identity was returned in model-usage metadata, while effective effort was not independently attested. The review agreed with the bounded no-strong-result conclusion and reported no material code error that changed it. It was not a second execution or a row-by-row source audit.

Review issues were retained: pooled AUC can mix score scales across models/folds, so this report emphasizes balanced accuracy and does not claim AUC confidence intervals or formal significance. The later depth-four permutation diagnostic was completed; all 164 source date strings have explicit day/month/year, allowed sex codes were checked, and code/input hashes match the actual result file. No sensitivity analysis establishes that this learner library could detect every genuinely strong but complicated effect. Approximate standard-error remarks in the reviewer text are not adopted as formal statistical evidence.

## Reproduction and provenance

The exact original <=5-year baseline AUCs were replayed before changing the method. Source cohort SHA-256: `c00416b688c70c5cc133690341ce7695006c5563e01d7b92a1239203e916cf11`. Executed expanded-search code SHA-256: `ce7c201de8173ecfce251f83ee35fd354a263eb9be774922d605ca51cf609c74`.

The astronomy calculation explicitly requested Moshier plus speed and verified returned flags 260. Positions/features were averaged across nine equally spaced reference instants spanning -14 to +36 UTC hours around the recorded date. This is a modelling convention for missing birth times, not an estimated distribution of actual birth times. It is a reduced experimental model, not canonical V4.3, the six-rule personal model, or a complete traditional natal reading.

Code, original inputs, matched-pair data, full results, fitting diagnostics, execution logs, review packet, review and reconciliation are included in the downloadable packet. See RUN.md. No production scoring model was changed and no model was deployed.

## Sources

[1] Cawley and Talbot (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*. https://www.jmlr.org/papers/v11/cawley10a.html

[2] scikit-learn, *Nested versus non-nested cross-validation*. https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html

[3] Forer (1949), *The fallacy of personal validation; a classroom demonstration of gullibility*. https://pubmed.ncbi.nlm.nih.gov/18110193/ . Original-paper text reprint: https://www.scribd.com/doc/17378132/The-Fallacy-of-Personal-Validation-a-Classroom-Demonstration-of-Gullibility . Cited for the distinction between personal applicability and discrimination, not as a diagnosis of these individual cases.
