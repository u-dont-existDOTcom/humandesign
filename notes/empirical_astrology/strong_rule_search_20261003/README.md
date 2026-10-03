# Strong-rule search: findings and limits

## Answer

The expanded search found strong-looking fits to the development data, but no stable strong astrology/numerology classifier. The previous additive pilot did not test all interacting rules or the rich, birth-time-aware individual-reading method. Its negative results must not be broadened into a rejection of every such method.

This extension used the same 82 offender/control pairs, not 82 new people. The labels mean membership in the existing serial-killer-biography and Nobel-laureate datasets. They do not establish current imprisonment for every case, actual happiness for controls, or individual dangerousness.

## What was actually run

The earlier four 53-pair AUCs reproduced exactly: calendar 0.5315058739765041; date numerology 0.4848700605197579; date-only astrology 0.5873976504093984; combined 0.50124599501602. Their balanced accuracies also reproduced. The earlier quoted permutation p-values were not replayed: their implementations and raw draws were absent from the saved script. No new claim rests on those p-values.

The new search allowed conditional combinations with decision trees. It considered 12 depth/leaf-size settings inside each training fold, rather than selecting rules using held-out outcomes. Five outer folds kept each pre-existing pair together; three inner folds selected settings. The full 82-pair comparison was repeated with three predetermined splits. A fixed 128-tree random forest supplied a second nonlinear diagnostic. Repetitions reuse the same people and are not independent cohorts.

Feature families contained 76 birth-date numerology variables; 78 displayed-name numerology variables; 271 six-planet variables; 526 nine-planet variables; and up to 680 combined variables. Astronomy included signs, major aspects at two fixed orbs, retrograde indicators and simple sign dignities. Name analysis used the recorded display spelling under cyclic and Chaldean letter encodings, not verified full birth names.

Missing birth times were not invented. There are no houses, Ascendant, Midheaven or Moon-based features. Planetary variables average nine samples over a conservative 50-hour possible-UTC envelope for an unspecified local birth time and offset. These samples are not an exact interval-boundary calculation. The ephemeris explicitly requested and returned Moshier (flags 260); this is an exploratory noncanonical calculation, not Swiss-production or V4.3 compliance.

## Performance on people excluded from each fit

Mean AUC over the three outer-split repetitions; chance AUC is 0.50. These are internal exploratory comparisons, not untouched external validation.

| Inputs | Selected compact trees | Fixed random forest |
|---|---:|---:|
| Birth-date numerology | 0.483 | 0.533 |
| Displayed-name numerology | 0.555 | 0.594 |
| Six-planet expanded astrology | 0.516 | 0.478 |
| Nine-planet expanded astrology | 0.525 | 0.605 |
| Date numerology + nine planets | 0.549 | 0.610 |
| Date + name numerology + nine planets | 0.576 | 0.632 |
| Calendar nuisance baseline | 0.568 | 0.564 |
| Name-format nuisance baseline | 0.670 | 0.688 |

For the combined inputs, mean held-out balanced accuracy was 55.7% for selected compact trees and 60.0% for the fixed forest. A single depth-three tree fitted to the entire dataset reached 76.2% balanced accuracy and AUC 0.812 on those same training people. That full-data tree is not the same object as the fold-specific selected trees. Unrestricted trees could fit the combined data perfectly; that is memorization evidence, not validation.

## The strongest apparent result and its checks

The predeclared 53-pair sensitivity subset (birth years within five years) produced AUC 0.753 and balanced accuracy 72.6% for the combined tree search on one split. Because this was the strongest result, it received explicitly post-result diagnostics, not a new claim of confirmation.

On the other two predeclared seeds its AUC fell to 0.651 and 0.648, and balanced accuracy to 60.4% and 58.5%. Thus reporting only 0.753 would substantially exaggerate stability.

Replacing the letter-number tables with ten arbitrary encodings, preserving each table's distribution of letter values, produced AUCs ranging from 0.577 to 0.720 on that same subset/split. This is a diagnostic warning about name structure and model search, not a formal corrected p-value or proof that all numerology effects are absent.

Ten independently redrawn same-birth-year random-calendar panels gave mean forest AUC 0.504 for six-planet astrology, 0.503 for nine-planet astrology, and 0.486 for date numerology plus nine planets. Random dates are not real happy-person controls and do not model country-specific birth seasonality. These panels specifically check whether a date-pattern signal persists when birth years are identical within pairs.

## Two measurable cohort problems

Of the 63 pairs with different birth years, the offender was younger in 62 and the control in one. There were 19 birth-year ties. A rule choosing the later-born person therefore identifies 62/63 of unequal-year pairs without astrology. This conditional pair-ranking rate is NOT a single-person AUC or accuracy over all 164 records.

There were 23 control names containing initials and zero offender names containing initials. Name formatting alone yielded stronger aggregate discrimination than the esoteric feature families in this search. It demonstrates a source-convention difference; it does not prove that every contribution from name numerology is explained by that difference.

## Individual readings versus cohort classification

These are not yet equivalent tests. Full individual readings can use exact birth times, complete names and rich traits; this cohort lacks comparable information. Recognizing a personality pattern and classifying murder versus Nobel recognition also ask different questions. Even a genuinely useful personality model need not predict that particular life-outcome contrast.

However, perceived accuracy and discriminative accuracy are different. A reading can fit its intended person well yet also fit several other people well. Interpretive flexibility, information leakage, selective attention and chance are possible explanations to test, not established diagnoses of the owner's experiences. Genuine interactions are also a possibility; this search gave some explicit interaction learners an opportunity to find them.

A method that consistently identifies individuals should create an aggregate advantage when correct readings are compared with matched decoy readings. That does not require all offenders to share one sign or number. The closer follow-up is therefore to preserve the individual-reading method, conceal identities and feedback, freeze outputs, and measure correct-person versus shuffled-person matching. Do not substitute a shallow zodiac-frequency test for that claim.

## Status and recovery

No predictive model is promoted. No participant was recruited, no individual-risk assessment was made, and no production code was changed. The scientific parent remains open; this bounded exploratory search is complete. The unresolved need is a genuinely independent, adequately matched cohort with reliable names/times, or a controlled test of the exact individual-reading method. Merely trying more symbols on these same people is not new validation.

`PROTOCOL.md` was committed before the new model results. `search_rules.py` is the primary run; `check_candidate.py` contains the post-result diagnostic; `audit_baseline.py` replays the earlier algorithm. Input projection, fold rules, held-out scores, manifests, feature cache, results and execution logs accompany the report. Independent cross-family methodological review was not run; deterministic and cross-runtime checks are separate from such review.

Reproduce with the pinned dependencies in `requirements.txt`:

    python audit_baseline.py
    python search_rules.py human
    python search_rules.py calendar_null
    python check_candidate.py

The source input is the pre-existing repository CSV, blob fca43841a83f6efcfe4d1dde66d6887335954c3c. The derived five-column projection SHA-256 is b47abae2747943169efced12ffd84f5d61b92e0a4213e08dc0af3e5197b9565d. It was independently regenerated byte-for-byte from that CSV on the owner-authorized computer.

## Methodological sources

Friedman and Popescu (2008), Predictive learning via rule ensembles: https://arxiv.org/abs/0811.1679

Cawley and Talbot (2010), On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation: https://www.jmlr.org/papers/v11/cawley10a.html

Scikit-learn decision-tree documentation: https://scikit-learn.org/stable/modules/tree.html

Forer (1949), The fallacy of personal validation; a classroom demonstration of gullibility (relevant background, not a diagnosis of these cases): https://pubmed.ncbi.nlm.nih.gov/18110193/
