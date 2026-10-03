# Strong-rule search: development protocol

Owner request: prioritize a ruleset giving strong signals, rather than pursuing very weak effects; explain apparent individual-reading accuracy versus group performance. Parent task remains OPEN. This is an exploratory extension, not a new untouched validation cohort.

## Source and audit

Use the existing 82 pairs from `notes/empirical_astrology/murderer_birth_pattern_pilot_20261003/paired_cohort.csv`, source blob `fca43841a83f6efcfe4d1dde66d6887335954c3c`. Container transport is unavailable, so a five-column name/date projection was transcribed from the connector output. Projection SHA256: `b47abae2747943169efced12ffd84f5d61b92e0a4213e08dc0af3e5197b9565d`. All four earlier 53-pair AUCs and balanced accuracies have already reproduced exactly from this projection. The earlier permutation p-values were not reproduced; their implementations/raw draws were not in the saved script. No unsupported execution claims are inherited.

Audit found 62 case-younger pairs, one control-younger pair, and 19 birth-year ties. Nobel prize recognition is not a happiness measurement. Current prison status and exact DOBs remain incompletely source-verified. These are dataset labels, not risk assessments.

## Independent conception and reuse

An additive model can miss interacting rules. Compare compact decision trees, which make conjunctions and disjunctions explicit, with a fixed nonlinear tree ensemble. Reuse scikit-learn implementations rather than inventing a new rule learner. Decision-sufficient sources: scikit-learn tree documentation; Friedman and Popescu (2008), Predictive learning via rule ensembles; Cawley and Talbot (2010), model-selection bias. Disposition: COMPOSE established tools into an exploratory diagnostic.

## Registered exploratory search (before new performance results)

Feature families: birth-date numerology; six-planet non-lunar astrology expanded with signs, major aspects and simple sign dignities; nine-planet expansion; displayed-name numerology under two explicit letter mappings; combined birth-date and displayed-name features. Calendar/birth year and name-format features are non-esoteric confound baselines. Display names are not asserted to be canonical birth names.

Numerology includes the earlier component-preserving 11/22/33 reduction, straight digit-sum sensitivity, birthday and attitude reductions. Name mappings are Latin cyclic 1..9 and conventional Chaldean groups; diacritics removed, Y consonant, full spelling as recorded. Name-formats/initials are tested separately because the two source datasets format names differently.

Astronomy: explicitly requested Moshier via pyswisseph, returned engine checked; exploratory date-only diagnostic, not canonical Swiss/V4.3. No Moon, houses, Ascendant, MC or birth-time claims. Nine equally spaced samples from UTC midnight minus 14 hours through plus 36 hours represent a conservative unknown-local-time envelope. Average sign/aspect indicators across these samples; major aspects 0,60,90,120,180 degrees, with fixed 3- and 6-degree orbs. No post-result feature changes.

Primary human comparison: all 82 pre-existing pairs, with pair-grouped 5-fold outer CV and 3-fold inner CV selecting tree max depth from 1,2,3,4 and leaf size from 4,8,12. Repeat with three predetermined seeds 20261003,20261017,20261031. All preprocessing/selection using labels stays inside training folds. Report whole-data fitting separately, never as validation. Fixed random forest (128 trees, depth 4, leaf size 6) provides an additional nonlinear check, without result-driven tuning. Record balanced accuracy and AUC, not only p-values.

Sensitivity: existing 53 pairs with <=5-year gaps; birth-year-only and name-format baselines; ten independently redrawn same-year random-date panels for date-only arms. Random dates are calendar controls, not real happier people. Any age or source-format difference is a confound, not an astrological effect. Repeated CV is internal exploratory evidence, not fresh replication.

Working definition of a large candidate: held-out AUC around 0.75 or higher with balanced accuracy around 0.70 or higher, stable across splits and not explained by the confound checks. These are analyst-chosen descriptive guideposts, not owner-imposed hard gates. A smaller result is not forbidden; it is simply not the strong signal requested. A rare high-purity subgroup must disclose coverage and independent test counts.

## Active obligations

Preserve target and allow development fitting; do not equate fitting with validation. Verify actual calculations; distinguish planned, attempted and executed. Do not convert the limited feature search into a verdict on every possible astrology system. Do not diagnose the owner's individual experiences as bias without tests. Store code, inputs/provenance, raw held-out predictions, metrics and limitations in this isolated branch. No model promotion, production deployment, individual criminality prediction, new paid services or participant recruitment is authorized here.

## Intended interpretation of the individual/group gap

Compare the same reading method against shuffled-person readings, with the reader blind to names, biographies and feedback; freeze predictions before evaluation. A high apparent fit to one person is distinct from discriminating that person from matched alternatives. Existing individual cases are development evidence unless their blindness/freeze/control conditions are documented. Both genuine interactions and interpretive flexibility remain possibilities to distinguish, not assumptions to declare settled.
