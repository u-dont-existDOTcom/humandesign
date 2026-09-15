# Life Patterns v2 standardized coverage blueprint — 2026-09-15

Status: **DEVELOPMENT CANDIDATE IMPLEMENTED / VERIFIED / DEPLOYED — OWNER PRODUCT RETEST REQUIRED**.

## Owner correction

The owner identified a methodological gap in the adaptive interviewer. A set of optional high-information probes is not by itself a scientific measurement design. If the instrument only follows whatever topics a participant volunteers, important behavior domains can remain systematically unobserved, and two participants can receive materially different measurement coverage for reasons unrelated to their actual behavior.

The owner also reaffirmed that the product is intentionally meant to collect person-specific evidence useful for later astrology / Human Design analysis and for InnerSignal. Target-theory blindness therefore must not be misread as target-indifferent measurement design.

No private interview transcript or identifying participant narrative is preserved in this receipt.

## Resolution: standardized constructs, adaptive probes

The current development architecture is a **semi-structured standardized interview**:

1. participant-led salient/idiosyncratic patterns come first;
2. a versioned required-domain checklist tracks what has and has not been measured;
3. naturally supplied evidence can satisfy a required domain without re-asking a canonical question;
4. under-covered required domains can be opened through a canonical neutral screener;
5. within a domain, follow-up wording remains adaptive and is admitted only when it can materially improve the domain characterization;
6. stopping/missingness is explicit rather than inferred from silence.

Thus the scientific checklist is the **required construct coverage plus status/evidence/provenance/stopping rules**, not a requirement to ask every participant the same literal sentence in the same order.

## Coverage statuses

Every required domain can be classified as:

- `unassessed` — no meaningful information;
- `partial` — relevant information exists, but not yet a stable person-specific characterization;
- `sufficient` — evidence supports a narrow person-specific characterization;
- `unknown` — the participant directly addressed the domain but cannot tell / does not know;
- `inapplicable` — the participant explicitly indicates the domain does not apply;
- `declined` — the participant explicitly refuses to answer.

Only `sufficient`, `unknown`, `inapplicable`, and `declined` count as coverage-complete. `unknown`, `inapplicable`, and `declined` are explicit missingness states, not negative behavioral evidence. Silence never becomes absence, inapplicability, or refusal.

For `partial` or `sufficient`, the coverage classifier must cite operative hidden-ledger fact IDs. Unsupported or unknown fact references are discarded; a `partial`/`sufficient` row with no valid cited fact is downgraded to `unassessed`.

Coverage assessment is process metadata used to route the interview. It is not an astrology/HD score, validation outcome, or independent behavioral observation.

## Development blueprint v1

Version: `life-patterns-required-coverage-v1`.

The current top-level required domains are:

1. decision and choice process;
2. energy, work, stopping, and recovery;
3. attention, cognition, learning, and work style;
4. emotional baseline and regulation;
5. relationships, conflict, trust, and boundaries;
6. social entry, recognition, groups, and roles;
7. communication and influence;
8. values, purpose, motivation, and salience;
9. environment, body, comfort, and security;
10. developmental continuity and change.

Each domain has a stable ID, definition, and canonical neutral screener. The complete blueprint is deterministically hashed and exposed by the development API. A later validation instrument must freeze a declared blueprint version/hash before scored collection.

## Adaptive discriminators are not the checklist

The existing cross-cutting discriminator menu remains useful *inside* these required domains: self-view vs familiar-observer view, inner vs outward presentation, baseline vs triggered state, automatic vs deliberate/learned response, context stability, timing/threshold/intensity/duration/recovery, developmental change, and coexisting modes.

Those discriminators are selected according to information gain; they are not each mandatory for every domain. For example, observer triangulation may be highly informative for a global claim such as emotional steadiness, while automatic-vs-deliberate response may matter more for conflict, persuasion, or decision behavior.

## Target-aware design / target-blind runtime

Development may deliberately choose behavior domains because they are likely to be useful for later astrology / Human Design model comparison and for InnerSignal. The runtime interviewer still does **not** receive the participant's chart, expected answer direction, candidate ranking, target-model mapping, score, or hidden theory label.

The distinction is:

- target-aware **instrument design**;
- target-blind **participant execution**.

This prevents answer-key leakage without deliberately discarding predictive behavioral signal.

## Question-bank cross-check

The current HD behavior-first question bank was inspected after the owner correction. It supports the need for standardized domain coverage and contains constructs spanning body/signal access and override, decision timing, social entry/recognition, energy/recovery, learning and expertise, systems, resources/ambition/status, conflict/relationships, developmental chronology, emotional permeability/baseline, pressure, expression, environment/direction, fear, original contribution, persuasion, purpose, and other person-specific dynamics.

This cross-check also shows that the current 10-domain partition should **not yet be treated as the final validation taxonomy**. Before freezing an untouched validation instrument, development should test whether some broad buckets should be split—for example body-signal access/state-dependence versus environment, and resources/status/security versus sensory/physical conditions—and verify explicit crosswalk coverage against the behavior-first question bank and later astrology/HD target layers. That is a measurement-design refinement, not permission to tailor questions to a participant's known chart.

## Implemented behavior

Implementation: `src/hdmatch/api/life_patterns_v2_owner_coverage.py`.

The browser now aggregates coverage metadata across completed pattern threads. After a thread, the participant can choose **Continue required coverage**. The next required domain still marked `unassessed` or `partial` is opened with its canonical neutral screener in a fresh backend thread. Domains already `sufficient`, `unknown`, `inapplicable`, or `declined` are skipped.

`Finish for now` remains available. If required domains remain open, the summary explicitly reports incomplete coverage rather than pretending the interview is scientifically complete. This preserves voluntary stopping without collapsing missingness into a behavioral result.

The coverage classifier is target-theory-blind and uses the same hidden-ledger evidence/provenance boundary. Natural user-led material can cover several domains; the checklist therefore standardizes **coverage**, not conversational redundancy.

## Password removal

At the owner's explicit request, HTTP Basic authentication was removed from the live development surface.

`src/hdmatch/api/life_patterns_v2_owner_deployed_app.py` now installs Basic Auth middleware only when `HDMATCH_OWNER_BASIC_PASSWORD` is non-empty. Railway's `HDMATCH_OWNER_BASIC_PASSWORD` and `HDMATCH_OWNER_BASIC_USER` values were set to empty strings, and the resulting deployment succeeded.

The development URL is therefore intentionally unauthenticated. This broadens access to anyone who has or discovers the URL and can expose runtime model usage/cost. It does **not** authorize external participant recruitment/collection, target-model scoring, publication, merge/release, or representation of the prototype as a validated public study.

## Verification / deployment

Passwordless-capable wrapper head: `e6cb6e0f20c98ade58a283695508e4f0fc7f94fa`.

Standardized coverage implementation head: `5b2b2a0526685155079dc7e280c9ac975490ef68`.

Regression/test head: `c916051dd3d4c114e85aeeb304abb8a34e236b19`.

GitHub Actions run `34920921980`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

Railway deployment `71bbefbe-06e0-432c-b904-c60904de4932` from application head `5b2b2a0526685155079dc7e280c9ac975490ef68`: **SUCCESS**. Application startup completed and `/healthz` returned HTTP `200`.

No transcript persistence, request-body logging, target-model activity, chart-aware runtime routing, or new Railway service was added.

## Next decision-changing evidence

Owner browser testing should now answer two questions:

1. does the password prompt disappear after refresh/reopening the page;
2. does the required-coverage flow feel like a real semi-structured scientific interview rather than either free-form drift or a repetitive questionnaire?

For measurement architecture, the next development decision after that product test is whether to split/refine the current 10 broad domains before a validation freeze, using an explicit crosswalk to the existing behavior-first question bank and the later astrology/HD target-model behavioral surface.

**There was never a completion policy.**
