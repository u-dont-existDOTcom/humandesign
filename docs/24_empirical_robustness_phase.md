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

## Exact indexed execution

The naïve scorer remains the correctness oracle. The accelerated scorer integer-encodes each
categorical outcome and builds an inverted candidate bitset for every feature/outcome pair. A
candidate is one bit in a Python arbitrary-precision integer. Match scores are accumulated with a
bit-sliced binary counter; mixed half-credit is represented exactly by scaling every score by two.
Exact score masks then provide the number above and tied with the true score, the current leader
set, candidate survival, and the stopping decision using integer `bit_count` operations.

Adaptive entropy is calculated from intersections of the current leader bitset with each frozen
outcome partition. The selection inputs and deterministic tie-break remain identical to the
reference implementation. The optimized layer does not receive birth metadata, the source-state
identity as a selection input, target rank, prose, or post-reveal evidence.

Preprocessing stores one candidate bit per feature across all outcome partitions, so partition
payload is linear in candidate count times feature count (plus Python object/index overhead). Each
ranking pass performs bit operations proportional to the number of answered features and the
packed bitset length, plus frozen adaptive questions. It does not allocate an N-by-N matrix.
This is an implementation-level speedup, not a claim that worst-case ranking is sublinear in the
candidate count. The tracked century report records observed runtime, peak process memory, and
unique transformed-answer signature counts.

Correctness is gated twice: exhaustive pathological small-universe tests compare every source and
scenario, including exact per-candidate score reconstruction; a deterministic real-cache audit
then compares reference and indexed engines over multiple subset sizes, scenarios, and seeds.

## Resumable execution and progress

The century runner writes `status.json` atomically while it initializes and after every configured
case interval. The status records the active scenario, completed and total cases, elapsed time, an
estimated remaining time, and the scenarios already complete. At scenario completion it writes a
content-hashed checkpoint and refreshes `partial-report.json`. A restart reuses a checkpoint only
when its scenario definition, frozen artifact hashes, candidate range, feature contract, scorer
version, and Git commit all match. A corrupt or stale checkpoint fails closed.

Use `--scenario SCENARIO_ID` to execute one frozen scenario, `--checkpoint-dir PATH` to choose the
durable checkpoint location, and `--progress-every N` to choose the status interval. Repeating
`--scenario` selects several scenarios. Resume is the default; `--no-resume` deliberately
recomputes them. CI uses one all-288,938-state job per frozen scenario, preventing one slow
scenario from hiding the status of the other eleven or exceeding a monolithic job timeout.

## Frozen century results

The content-hashed report at `state/SURVEY-V2-NOISE-AUDIT.json` covers all 288,938 candidates and
all twelve frozen scenarios at scorer commit `dd37aa4`. Top-k values use fractional credit for
ties. Every scenario has median true-state rank 1; that does not make these human-accuracy results.

| Scenario | Top 1 | Top 5 | Top 10 | Rank p90 | True state survives | Unique stop |
|---|---:|---:|---:|---:|---:|---:|
| Perfect answers | 100.000% | 100.000% | 100.000% | 1.0 | 100.000% | 100.000% |
| One wrong classification | 98.344% | 100.000% | 100.000% | 1.0 | 99.595% | 97.518% |
| Wrong 5% | 96.555% | 99.997% | 100.000% | 1.0 | 99.104% | 94.979% |
| Wrong 10% | 92.240% | 99.942% | 99.998% | 1.5 | 97.557% | 89.674% |
| Wrong 20% | 82.582% | 98.264% | 99.405% | 2.0 | 92.411% | 81.327% |
| Ambiguous 5% | 98.276% | 100.000% | 100.000% | 1.0 | 100.000% | 96.580% |
| Ambiguous 10% | 96.316% | 99.999% | 100.000% | 1.0 | 100.000% | 92.762% |
| Ambiguous 20% | 92.865% | 99.997% | 100.000% | 1.5 | 100.000% | 86.223% |
| Other 10% | 96.269% | 100.000% | 100.000% | 1.0 | 100.000% | 92.670% |
| Uncertain 10% | 96.363% | 100.000% | 100.000% | 1.0 | 100.000% | 92.860% |
| Mixed 10% | 99.948% | 100.000% | 100.000% | 1.0 | 100.000% | 99.896% |
| Counterevidence 10% | 92.171% | 99.937% | 99.998% | 1.5 | 97.521% | 89.612% |

The perfect-answer condition reproduces 100% unique rank-1 oracle recovery. Abstaining conditions
(`Other`, uncertain, and ambiguous) never eliminate the true state; explicit wrong or
counterevidence labels can. At 20% wrong answers, top-1 credit falls to 82.582%, while top-10
remains 99.405%. Mixed answers are substantially less damaging than forcing an uncertain response
to a wrong label.

Failure diagnostics consistently identify the personality-Moon and design-Moon constructs as the
largest per-perturbation risk, followed at higher corruption by channels and a small set of
baseline observables. This is a specific measurement-reliability failure inside frozen domains,
not evidence that the structural state space lacks a domain. The preregistered next action is to
evaluate behaviorally distinct redundant probes for those existing latent constructs. They remain
one dependency cluster each and cannot add structural bits. No new astrology or Human Design
domain is added in this version; that decision can be revisited only if prospective redundant
measurement fails under a new frozen protocol.

The indexed/reference equivalence report records 22,848 exact comparisons across pathological
small universes and deterministic real-cache subsets. The full report records a 3,437.7 MiB peak
process footprint. Scenario simulation time totals 890.5 minutes; because execution resumed from
checkpoints, the report's 549.1-minute wall time describes the final invocation rather than total
work across all invocations.
