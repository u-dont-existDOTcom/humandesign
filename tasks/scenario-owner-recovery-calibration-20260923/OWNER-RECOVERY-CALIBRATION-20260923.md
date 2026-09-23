# Scenario survey owner birth-recovery calibration — 2026-09-23

Status: target-theory-blind measurement calibration in progress.

## Purpose

Test whether the completed owner scenario interview preserves enough behavior-only information to satisfy the pre-existing owner AstroHD recoverability regression. This is a development regression, not untouched validation or population evidence.

The calibration must not turn a failed measurement into a success by adapting questions after inspecting the owner's birth target.

## Privacy boundary

Raw answers, private event identifiers/locators, neutral coder outputs, and any participant-specific profile stay outside public Git. Public artifacts may record only method, cryptographic hashes, aggregate coverage, and final pass/fail diagnostics that do not reproduce raw answers.

## Frozen measurement

- participant-answer records: 68
- source private-export SHA-256: `a0eb46e17d44644c5b4f7c7d6e9a177a2a9ee8da9c7340f37292413108258784`
- private measurement-freeze SHA-256: `7a6398de3c591e7dd8cc907b90c7312171452e6c13624a96e3f01826d6944863`
- target-blind minimal measurement packet SHA-256: `ce596c0cf1b18d9f2a924b34ab914a941c91b8f6da5414f0b045e2c354cf337a`
- neutral facet-contract SHA-256: `605212e814429b23c87dbcf4279e297dc4d436831521e741534bdb4222c3cd57`
- interview-protocol SHA-256: `b5b148303e6db77af5c5ab137d208bdd3d8b4f785142fe479d51cb7ee9c26248`

The private measurement packet contains no birth data, chart data, target-model mapping, candidate score/rank, or historical recovery result.

## Stage A — neutral coding

Two fresh independent GPT-5.6 Sol xhigh coding contexts receive only:

1. the frozen minimal measurement packet;
2. the neutral 73-facet contract;
3. the interview protocol.

They must code literal participant evidence into `sufficient`, `partial`, `unknown`, `inapplicable`, or `unassessed`, preserving conditions and design-invalidated answers. They cannot see any birth/chart/model/recovery information.

Material disagreements are adjudicated in a third fresh target-blind context before any target-aware mapping is exposed.

## Stage B — target-blind calibration gaps

Before opening the historical AstroHD crosswalk, a fresh gap-planning context may propose only repaired neutral v7 questions needed to resolve material evidence gaps. It sees neutral requirements and coding only, never the birth target or historical target mapping.

If additional answers are collected, append them privately, create a new immutable measurement freeze/version, and repeat Stage A. Do not silently mutate v1.

## Stage C — post-freeze historical mapping

Only after the final neutral profile is frozen may a separate target-aware process receive the historical owner crosswalk. It maps supported neutral evidence into the historical score-bearing behavioral constructs without viewing the true birth tuple or previous candidate rankings.

Mappings/confidences/scoring inputs are frozen and hashed before search/reveal.

## Stage D — recovery test

Primary legacy regression gate is the pre-existing `astrohd-v1.1-v3.6-century-hourly-plus-leading-minute-refinement` owner benchmark:

- correct birth date must be the top distinct refined neighborhood;
- exact recorded moment rank against the hourly universe must be <= 2;
- absolute refined local peak offset must be <= 11 minutes;
- coverage alone cannot pass.

The historical one-off V1.1 scan implementation is not present in Git. Therefore any reconstructed legacy scorer must first reproduce the historical frozen result from the frozen historical model before it is permitted to score the new profile. If exact reproduction cannot be established, the legacy gate remains technically unresolved rather than being approximated into a pass.

The legacy recoverability gate is primary for **survey adequacy** because it is the pre-existing owner benchmark that localized the known birth target tightly using the merged HD + Western scorer: correct date/top refined neighborhood, exact recorded moment rank <= 2 in the hourly universe, and local refined peak within 11 minutes. This benchmark and the later V4.3 audit are not the same scoring system. Using a V4.3 variant already known not to recover the exact owner moment as the sole survey gate would confound a measurement failure with a model failure.

A separate current V4.3-style diagnostic may also be run, but its status must be preserved exactly:

- cleaner candidate-unexposed V4.3-style variant: a 2013 interval is rank 1 and a correct-date 1985 interval is rank 2;
- best-current descriptive variant including the two candidate-exposed Moon/Mars carrier refinements: a correct-date 1985 interval is rank 1;
- the V4.3 rank-1 1985 interval does not contain the exact recorded birth moment, so it must not be described as better exact-time recovery than the older merged V1.1 benchmark;
- the freeze preserves those historical before/after results and their contamination status; it does **not** make V4.3 the final model or prohibit improvement;
- any mapping/weight change learned from this owner case must be a new explicit post-ranking model version/revision. The owner may be used as development data for that revision, but the same owner result cannot then be claimed as independent confirmation of it.

After the v7-calibrated neutral profile is frozen, V4.3 diagnostics may be rerun if the implementation is available. A miss by the cleaner pre-selection variant alone is not evidence that the survey failed, because that variant already had a known owner rank-2 model miss before this survey calibration.

## Decision rule

- If neutral coding shows material calibration gaps, fill only those gaps target-blind before target-aware scoring.
- If the frozen post-freeze profile passes the declared legacy gate, the owner development recoverability regression passes.
- If it fails, the survey/mapping/scoring chain requires further development; do not tune the same frozen test after reveal and relabel it independent.
