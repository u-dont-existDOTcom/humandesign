# Survey V2 empirical robustness phase

## Claim boundary

The perfect-match century result is an **oracle structural-recoverability** result. It says that
the frozen questions and candidate-blind adaptive rule contain enough distinctions when every
predicted label is observed without error. It is not evidence that people exhibit the predicted
patterns or that a classifier can recover them reliably.

The noise audit is also synthetic. It measures how the frozen decoder behaves after controlled
wrong, ambiguous, Other, uncertain, mixed, and counterevidence classifications. It is an
engineering robustness result, not demonstrated human accuracy. Human accuracy requires a
prospective, blinded, person-split evaluation with all prediction and response packages frozen
before reveal.

## Frozen simulation contract

- Rescore the complete 288,938-state universe after every accepted answer.
- Select an adaptive field only from anonymous current score leaders and unanswered frozen field
  IDs, maximizing entropy with the frozen field order as the deterministic tie-break.
- The selector and stopping rule never receive birth metadata, the true-state identity, prose,
  classifier rationale, or candidate rank. Stop only when the score leader is unique or the frozen
  tie-breaker set is exhausted.
- A wrong or counterevidence answer is an explicit non-true frozen label. `Other`, uncertain, and
  ambiguous answers abstain and add no score. A mixed answer gives equal preregistered partial
  support to its two labels; it is not forced to one side.
- Report fractional top-1/top-5/top-10 credit under score ties, median true-state midrank, mean
  percentile, surviving leader count, true-state leader survival, and extra tie-breaker counts.
- Seeds, scenario definitions, candidate-universe hash, mapping hashes, software commit, and all
  per-shard outputs must be recorded in the machine-readable report.

The required scenario set is one wrong classification; 5%, 10%, and 20% wrong classifications;
5%, 10%, and 20% ambiguous classifications; and explicit Other, uncertain, mixed, and
counterevidence conditions. Scenario changes create a new audit version rather than overwriting a
frozen report.

## Classifier reliability

The frozen protocol in
`reference/core/survey_v2_classifier_reliability_protocol_v1.json` supports isolated same-model
repeats, cross-model repeats, and blinded human rerating. Agreement is diagnostic: it cannot alter
the current cohort's confirmatory scores. Post-reveal ratings and adjudications are retained but
excluded from confirmatory agreement and headline science.

## Redundancy

The probe registry in `reference/core/survey_v2_redundant_probes_v1.json` frames the same latent
construct in behaviorally different ways (life stages, settings, negative contrasts, and
counterevidence). All probes sharing a `latent_construct_id` form one dependency cluster. They can
estimate stability and reduce measurement error, but they contribute at most the structural bits
of that one latent construct. Regression tests enforce that duplicating a construct cannot inflate
the structural-information result.

No new astrology or Human Design structural domain should be added on the basis of this phase
unless a frozen robustness report identifies a specific failure and preregistered redundant probes
cannot repair it. Any such addition is a new model version for later untouched cohorts.
