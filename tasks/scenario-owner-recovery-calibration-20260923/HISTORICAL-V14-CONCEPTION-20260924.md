# AstroHD V1.4 - cross-rulebook ensemble conception - 2026-09-24

Status: OWNER-CORRECTED ACTIVE DEVELOPMENT OBJECTIVE / TARGET-AWARE OWNER TRAINING / NOT VALIDATION.

## Owner correction

The intended objective is to combine externally pre-existing rules from multiple astrological rulebooks into one ensemble that can fit the owner development case without project-invented arbitrary feature weights.

The prior V1.3/V1.3b requirement that each whole tradition independently recover the birth neighborhood was an assistant-added anti-cherry-picking requirement. It is not part of V1.4.

## Core design

- Individual rules from Lilly, Ptolemy, Valens, Parashari/BPHS, Phaladeepika, and other pre-scoring admitted rulebooks may combine.
- Every rule preserves source/book/location/provenance and a target-blind mapping to neutral behavioral domains.
- Convergence may stack.
- Report raw-source stacking and lineage-deduplicated stacking separately.
- No project-authored astrology salience/directness weights.

## Combination arms

1. Equal-rule stacking: each satisfied supporting rule = +1; contradictory rule = -1; otherwise 0.
2. Lineage-deduplicated stacking: same, but substantially identical inherited rules count once per provenance lineage.
3. Source-native composition: preserve a book's native numerical scoring internally; normalize each source-model score to its empirical century percentile, center as 2p-1, then combine source models with equal source-model weight.

## Owner-trained sparse rule selection

The owner case is development data, so binary rule inclusion may be trained on it. Selection is mechanical rather than manual.

Using the frozen direct set (target, persistent 2013 comparator, eight same-date alternatives):
1. target must be strictly top under both equal-domain and frozen-confidence behavioral weighting;
2. among satisfying subsets, minimize selected rule count;
3. then maximize target margin;
4. exact ties use lexical rule_id order.

Rule weights are not fitted.

## Century evaluation

After a sparse direct solution is selected, run that unchanged subset over the 876,601-hour century universe. Report target/2013 ranks, global top candidates, recorded-date neighborhood, leave-one-rule/source/domain-out sensitivity, and raw-source versus lineage-deduplicated behavior. Do not alter the subset after century-rank reveal.

## Scientific boundary

A successful owner fit would show that a sparse ensemble of externally sourced astrology rules can recover this known case without invented numeric feature weights. It would not establish prediction on unseen people; that requires freezing the ensemble and testing fresh participants.

## Immediate next action

Build a machine-readable rule inventory from admitted rulebooks, map rule meanings to neutral behavioral domains in a target-blind semantic pass, freeze the inventory/search algorithm, run the sparse direct-set ensemble search, then century-rank the unchanged solution if one exists.
