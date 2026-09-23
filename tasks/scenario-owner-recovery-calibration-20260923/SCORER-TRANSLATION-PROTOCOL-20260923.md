# Post-freeze scorer translation protocol — 2026-09-23

Status: **frozen method before the survey-instantiated candidate ranking is opened**.

## Boundary

The target-blind neutral measurement is already frozen at 79 participant answers. The private final neutral profile SHA-256 is `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`.

Only this post-freeze stage may receive scorer-specific semantics. Nothing in translation or scoring may feed backward into the neutral profile, question selection, coding, or adjudication. Raw participant answers and participant-specific findings remain outside Git.

## Behavioral-confidence translation

Use the pre-existing V3 behavioral-confidence classes only:

- `1.00`: repeated, specific, stable, or explicitly emphasized across contexts/time;
- `0.75`: clear and specific but based on fewer contexts or less repetition;
- `0.50`: moderately supported, context-sensitive, or somewhat interpretive;
- `0.25`: weak, tentative, generic, or newly reported without corroboration;
- `0.00`: unknown / do not score.

Confidence is confidence that the scorer-specific behavioral claim is established by the frozen neutral evidence. It is not confidence in Human Design, astrology, a chart candidate, or a historical winner.

Two independent target-aware translators receive only the frozen neutral profile, the relevant pre-existing crosswalk/scorer semantics, and this confidence rubric. They receive no birth tuple, chart state, candidate identity, candidate score/rank, recovery result, or the other translator's output. Disagreements are adjudicated before scoring.

## V1.1 merged HD + Western translation

Use only the frozen `historical_merged_cluster_crosswalk` and the historical V1.1 cluster semantics. For each of the 19 historical clusters freeze the translated behavioral confidence and bounded evidence rationale before any V1.1 search.

The translated confidence replaces the historical cluster behavioral-confidence term. HD/Western feature definitions, salience/directness tuples, `rho=0.25`, `cap_multiplier=1.25`, contradiction definitions, astronomy, Philadelphia-house convention, universe, and ranking/refinement procedure remain historical/frozen.

The original one-off V1.1 scanner is absent from Git and was not recovered from local session logs, old worktrees, shell history, dangling Git objects, GitHub issues/PRs, or Actions artifacts/logs. Therefore a reconstructed scorer must first reproduce the frozen historical V1.1 scores/ranks before it may score the new translation. Until that occurs, the V1.1 recovery result is **technically unresolved**, never approximated into pass/fail.

## Clean V4.3 / NetInformation translation

Use only the frozen `clean_v36_information_crosswalk`, the frozen V4.3 base mapping plus its pre-ranking v2 overlay, and exclude all mappings flagged `post_selection=true` from the primary comparison.

The crosswalk contains the 19 clean informative observables identified by the pre-existing holistic-information audit. It does not instantiate the old target's additional Type/center core fields.

### Selector rule

For each positive crosswalk observable:

- if the observable exactly matches a frozen mapping ID, select that mapping only (the three distinct profile observables use this form);
- otherwise select all candidate-unexposed mappings in the named dependency cluster.

`CONTRADICTION:X` selects the pre-existing contradiction cluster `X`. Unknown selectors fail closed. No mapping or contradiction may be invented.

### Confidence rule — CAP

A pre-search review compared two candidate rules. The final frozen rule is:

`derived_pathway_confidence = min(frozen_pathway_confidence, translated_behavioral_confidence)`

This **CAP** rule requires no undocumented factorization of the historical pathway confidence. A proportional-rescaling rule was rejected because it would assume, without repository evidence, that within-observable confidence ratios are reusable pure mapping-confidence factors.

All frozen non-confidence mechanics remain unchanged: predicate, salience, directness, flexibility, prevalence parents/backoff, contradiction severity, and dependency clustering.

An observable with translated confidence `0.00` is omitted entirely before candidate matching, state-signature construction, and duration tie-breaking. Zero means absence of usable evidence, not a negative match.

### CoreFit and score-equivalent interval policy

The historical target-specific `CoreFit` block is not instantiated by the 19-observable owner crosswalk. Importing it would leak old target assumptions into the new survey run. For this survey-instantiated comparison:

- CoreFit is a constant zero for every candidate;
- ranking otherwise remains NetInformation descending, meaningful contradictions ascending, DetailedSupport descending, then stable duration descending;
- adjacent exact states merge only when their active survey-scoring mapping/contradiction signature is identical. Historical Type/Authority/center/profile fields that are not active survey evidence may not split the stable-duration tie-break interval.

This is labeled **survey-instantiated clean V4.3/NetInformation crosswalk run**, not the untouched historical V4.3 audit.

## Freeze-before-search receipts

The private dual-translation freeze was completed before opening the new survey-instantiated ranking. Public Git records only non-private hashes and method metadata.

Frozen private inputs:

- V1.1 translated behavioral input SHA-256: `dbb92b270c2720cabed823e61ddc735dced579628c33f12df540e38b172d147d`
- V4.3 translated behavioral input SHA-256: `093ce072cc8c4342185d0a70667fbcef04564d34c1edf3f364f4b72955c19894`
- V4.3 CAP-derived translated model SHA-256: `fe5fdae912063bbe56d53ec40e199faa8fb25a0261ff34f64320eedf7ff2d4b9`
- CAP-method review SHA-256: `74557c3d51e055ae0ba42dcdb34964a2531dd5fc49f98c959ffa3d3db79650ab`

The historical V4.3 engine was separately rerun unchanged before the survey-derived search and reproduced the published clean and post-selection results. Historical-reproduction log SHA-256: `2e090745d96a636280125fe9c1eb3b1799f02543d088949e0edd84a9d2ca3369`.
