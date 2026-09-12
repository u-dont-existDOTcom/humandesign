# Life Patterns recurrence evidence policy v2 — 2026-09-08

Status: **development candidate** for the next versioned Life Patterns measurement stack. Theory-blind and target-blind. This file does not overwrite the reconciled v1 codebook or any v1 package/calibration artifact.

## Purpose

Correct the episode-centric treatment of recurrence before any human calibration or automated coding is collected.

The governing distinction is:

> A detailed example can increase **specificity** without increasing **independent support for frequency**.

## Evidence roles

Every recurrence-relevant statement must retain its evidence role. Do not silently substitute one role for another.

### R1 — generalized behavioral recurrence self-report

Examples: `I always X`, `I usually X`, `that happens every day`, `I sometimes X`, `this has been common throughout my life`.

This is direct evidence that the narrator reports a recurring behavior at the stated strength/scope. It is not zero evidence and does not require a confirming anecdote to become usable recurrence self-report.

It is **not** automatically:

- a literal verified universal;
- an independently observed opportunity-level rate;
- a set of fabricated episodes;
- a numerical occurrence count.

### R2 — bounded concrete episode

A bounded incident can establish what happened in that instance and clarify sequence, prerequisites, opportunity, feasibility, consequences, or meaning.

A concrete episode selected because the participant already said `I always X` is **not independent frequency evidence for the recurrence claim**. It may still be useful for interpretation or as a counterexample.

### R3 — exception / counterexample

A reported exception can qualify or falsify a strong recurrence claim and identify boundary conditions. It may be represented as a generalized exception statement or a concrete exception episode.

Do not require a concrete exception episode if the boundary condition and approximate exception frequency are already clear.

### R4 — sampled opportunity observation

Prospective diary/event sampling, structured/random opportunity sampling, or a bounded exhaustive opportunity set can support inference about opportunity-level frequency because the sampling frame makes observed opportunities informative.

### R5 — external behavioral record

Logs, records, passive measurements, or independent observations can provide a different evidence class from participant self-report. Preserve provenance and measurement limitations.

### R6 — trait/interpretive label

Examples: `I am cautious`, `I am spontaneous`, `I am generous`.

A trait label is not equivalent to a behavioral recurrence statement unless behavioral content is supplied.

### R7 — causal explanation

Examples: `I do X because Y`, `Y makes me do X`.

Preserve as narrator-stated explanation/influence. Do not upgrade it into objective causation.

## Recurrence self-report representation

When exact source text supports a generalized behavioral recurrence claim, record the following without requiring an episode:

1. **behavioral value(s)** under the applicable neutral observable;
2. **reported recurrence strength**;
3. **scope/opportunity class** when supported;
4. **life period/context** when supported;
5. **exception status and exception frequency** when supported;
6. **evidence basis**;
7. exact supporting source-segment provenance;
8. uncertainty/missingness where relevant.

### Reported recurrence strength

Use the smallest supported category; do not invent numeric precision:

- `universal_language` — participant uses language such as always/every time for the stated scope;
- `near_universal` — almost always / nearly every time;
- `usually` — participant indicates more often than not / usually;
- `often` — participant says often/frequently/common without a stronger quantifier;
- `sometimes` — participant explicitly reports intermittent occurrence;
- `rarely` — participant reports infrequent recurrence;
- `repeated_unquantified` — repeated/recurrently, but strength cannot be placed above;
- `bounded_rate_or_count` — an explicit rate/count over a defined period/opportunity set is supplied;
- `context_conditional` — recurrence strength is explicitly conditional on a context and no single cross-context strength is appropriate;
- `changed_over_time` — a material temporal change prevents one stable recurrence strength from representing the whole stated period;
- `unclear` — recurrence is asserted but the strength cannot be classified reliably.

These categories describe **reported recurrence**, not externally verified true frequency.

## Exception representation

Use:

- `exceptions_explicitly_denied` — participant explicitly says there are no exceptions in the stated scope;
- `exceptions_reported` — one or more exceptions/boundaries are reported;
- `exceptions_not_probed_or_unknown` — the source does not establish exception status.

Where supported, preserve an exception-frequency class:

- `none_reported`;
- `almost_never`;
- `sometimes`;
- `often`;
- `context_dependent`;
- `rough_rate_or_count`;
- `unknown`.

Do **not** infer `exceptions_explicitly_denied` merely from the word `always`. Ordinary-language `always` is retained as `universal_language`; exception status remains separate unless the source establishes it.

## Frequency evidence basis

Every recurrence annotation must identify its basis:

- `generalized_self_report`;
- `bounded_rate_or_count_self_report`;
- `sampled_opportunities`;
- `external_record_or_observation`;
- `mixed_basis`.

For the current v8/v8.1 development transfer, exact-source repeated-series material is ordinarily `generalized_self_report` unless the exact source itself supplies a bounded rate/count. Transfer summaries cannot silently upgrade the basis.

## Episode-frequency firewall

The following are hard rules for v2:

1. A confirming episode elicited or volunteered as an example of an already asserted recurrence pattern does not increase recurrence-frequency strength by count.
2. Multiple self-selected confirming examples do not become representative merely because there are several.
3. Episode observations remain valid episode-level evidence for the neutral behavioral value.
4. A genuine counterexample can qualify the recurrence claim.
5. Only an explicit sampling frame can make a collection of episodes support opportunity-level frequency estimation.
6. Do not create a recurrence score by adding `number of confirming episodes + series claim`.

## Exception-first interview probing

When a participant supplies a generalized recurrence statement and clarification is needed, default to:

1. **scope/denominator** — what class of opportunities/situations does the quantifier apply to?
2. **boundary conditions** — are there conditions where the behavior changes or does not occur?
3. **exception frequency** — within the relevant opportunity class, how often does the rule fail?
4. **temporal change** — has this pattern or its boundaries changed across a relevant life period?
5. **incident only if informative** — request a specific incident only if it resolves meaning, sequence, prerequisites, boundary conditions, exceptions, consequences, mechanism, or comes from a valid sampling design.

Do not force fake numeric precision. Natural responses such as never, almost never, sometimes, context-dependent, or a rough fraction/count are acceptable when that is the participant’s available resolution.

## Person-level aggregation

Person-level recurrence summaries must keep frequency evidence separate from episode existence evidence.

A summary may say, for example:

- participant reports `universal_language` for behavior X within scope Y;
- exception status is unknown because it was not probed;
- one concrete episode illustrates the process but is **not counted as independent frequency support**;
- one counterexample defines condition Z;
- no sampled opportunity data are available.

Do not collapse those facts into a pseudo-precise frequency score.

## Coding-state semantics

For repeated-series evidence, `observed` means:

> the exact supplied source supports a report of the specified behavioral value recurring within a defined or interpretable scope.

It does **not** mean the true objective opportunity-level frequency has been independently verified.

A minimum numerical occurrence count is **not required** for `observed` generalized recurrence self-report. A count/rate is required only when the annotation explicitly claims a bounded count/rate.

Use `insufficient` when the exact source does not support the behavioral value/recurrence distinction required by the observable. Use `not_applicable` only when the observable prerequisite is affirmatively absent.

## Exact-source requirement for current development transfer

The v8/v8.1 transfer contains both exact participant fragments and interviewer summaries. For coding:

- exact participant source segments are primary;
- recurrence language, rough counts, exceptions, and behavior summaries from transfer fields are orientation unless independently supported by exact source text;
- summary-only series remain ineligible for blind coding;
- no summary field can manufacture an exception, count, or recurrence strength absent from exact source.

## Non-action

If a recurring value is a substantive non-action code, each claimed recurrence still depends on the frozen non-action semantics. Do not infer recurring refusal/delay/avoidance from silence. The relevant source must support awareness, opportunity, reasonable feasibility, and established non-action for the behavioral claim being coded.

## Human/automated calibration

The human and automated coders must receive the same v2 recurrence definitions and the same exact selected evidence, while remaining isolated from each other’s labels and all target-model information.

Calibration should compare:

- evidence state;
- neutral behavioral value(s);
- recurrence-strength category when observed;
- exception status/category when applicable;
- evidence basis;
- source-citation validity.

Agreement on these fields is measurement reliability evidence only. It does not establish objective frequency accuracy, construct validity, predictive validity, or target-theory truth.

## Versioning / supersession

The reconciled v1 codebook, v1 development manual, v1 package `LPKG-18170B8D3EEC8423A523`, v1 calibration `LPCA-5B3E6CFCCE49807050DF`, and regenerated v1 human handoff remain immutable historical development artifacts.

This policy is a **new v2 development candidate**. Before any v2 human first pass:

1. bind this policy into a new development coding manual/stack;
2. create versioned repeated-series task/response contracts that encode the firewall above;
3. regenerate a new content-addressed development package and human calibration handoff from the exact recovered source bytes;
4. verify the human-facing UI exports the exact v2 contract;
5. freeze the v2 artifacts before labels exist.

No target-model outputs may be used to revise this policy.
