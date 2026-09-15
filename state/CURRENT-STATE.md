# Current state

## Life Patterns — 2026-09-15

Active task: `life-patterns-v2-standardized-coverage-owner-retest` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Only abstract product findings and synthetic regressions are preserved.

## Product strategy status

Direct owner testing has progressively replaced several failed participant-facing strategies: surfaced fact/paraphrase review, quota-driven multi-episode/counterexample interrogation, recurrence-as-sufficient-pattern logic, and synthesis/refinement paths that could overreach or repeat themselves.

The current product principle is **target-aware instrument design / target-blind runtime execution**. Development may intentionally collect neutral behavioral dimensions useful for later astrology / Human Design analysis and InnerSignal, while the runtime interviewer receives no participant chart, expected answer direction, target-model mapping, candidate score, or hidden theory label.

The current interviewer retains:

- person-specificity admission: generic high-base-rate regularities are not promoted to Life Patterns;
- adaptive burden control: no arbitrary episode or counterexample quota;
- familiar-observer / self and inner / outer triangulation when informative;
- dedicated non-repetitive `Keep trying to pin it down` reasoning;
- participant authority over person-level synthesis;
- explicit preproposal versus postproposal evidence timing.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-ADAPTIVE-STOPPING-REPAIR-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-PERSON-SPECIFICITY-GATE-2026-09-15.md`
- `state/LIFE-PATTERNS-v2-OWNER-OBSERVER-TRIANGULATION-AND-REFINEMENT-REPAIR-2026-09-15.md`

## Owner methodological correction: optional probes are not enough

The owner correctly identified that a loose menu of possible high-information questions is not, by itself, standardized scientific measurement. Participant-led conversation alone can leave important behavioral domains unobserved for reasons unrelated to the participant's actual traits.

The deployed development candidate therefore adds a **versioned required-domain coverage checklist** while preserving adaptive conversational wording.

The checklist standardizes:

1. required constructs/domains;
2. coverage status semantics;
3. evidence citation/provenance requirements;
4. explicit missingness;
5. when a domain still needs further measurement;
6. canonical neutral screeners for under-covered domains;
7. blueprint version/hash for later freezing.

It does **not** require every participant to receive identical follow-up sentences or repeat information already supplied. Natural participant-led evidence can satisfy a required domain.

Coverage statuses are `unassessed`, `partial`, `sufficient`, `unknown`, `inapplicable`, and `declined`. Only `sufficient`, `unknown`, `inapplicable`, and `declined` close a domain. Silence never becomes absence or a terminal missingness state. `partial`/`sufficient` coverage must cite valid operative hidden-ledger fact IDs.

Coverage assessment is interview-routing/process metadata, not a chart score or validation result.

Receipt:

`state/LIFE-PATTERNS-v2-OWNER-STANDARDIZED-COVERAGE-BLUEPRINT-2026-09-15.md`

## Development coverage blueprint v1

Version: `life-patterns-required-coverage-v1`.

Current top-level required domains:

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

The browser aggregates coverage across completed pattern threads. `Continue required coverage` opens the next still-`unassessed`/`partial` domain with a canonical neutral screener. `Finish for now` remains available and explicitly reports incomplete coverage instead of pretending completion.

Cross-cutting questions such as self-vs-observer, inner-vs-outer, automatic-vs-deliberate, baseline-vs-triggered, timing/threshold/duration/recovery, context stability, developmental change, and coexisting modes remain **adaptive discriminators inside the required checklist**, not separate mandatory questions for every domain.

### Domain partition is not yet a final validation freeze

The existing behavior-first HD question bank was cross-checked after this correction. It confirms the need for required coverage and spans body/signal access, decision timing, social entry/recognition, energy/recovery, learning/expertise, resources/ambition/status, conflict/relationships, developmental chronology, emotional permeability/baseline, pressure, expression, environment/direction, fear, original contribution, persuasion, purpose, and related constructs.

Therefore the current 10-domain partition is a reversible development candidate. Before untouched validation, it must be explicitly crosswalked against the behavior-first question bank and later astrology/HD behavioral target surface. Broad buckets may need splitting—for example body-signal access/state-dependence versus environment, and resources/status/security versus sensory/physical conditions. Any validation run must freeze a declared coverage blueprint version/hash before collection.

## Password removal

At the owner's explicit request, the development surface is now **passwordless**.

`src/hdmatch/api/life_patterns_v2_owner_deployed_app.py` installs Basic Auth only when `HDMATCH_OWNER_BASIC_PASSWORD` is non-empty. Railway's Basic Auth username/password variables were set to empty strings and the redeployed service started successfully.

This intentionally broadens access to anyone who has or discovers the development URL and may expose runtime model usage/cost. It does **not** authorize external participant recruitment/collection, target-model scoring, publication, or representation as a validated public study.

## Verification / deployment

Passwordless wrapper head: `e6cb6e0f20c98ade58a283695508e4f0fc7f94fa`.

Standardized coverage application head: `5b2b2a0526685155079dc7e280c9ac975490ef68`.

Coverage regression/test head: `c916051dd3d4c114e85aeeb304abb8a34e236b19`.

GitHub Actions run `34920921980`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

Railway deployment `71bbefbe-06e0-432c-b904-c60904de4932`: **SUCCESS**. Application startup completed and `/healthz` returned HTTP `200`.

The health contract now describes a development surface and declares standardized required coverage, blueprint version/hash, adaptive wording with fixed domains, person-specificity, observer triangulation, and target-theory blindness. The stale `owner_only=true` health claim is not used on the standardized app.

## Current gate

Strategy: **SEMI-STRUCTURED STANDARDIZED COVERAGE + TARGET-AWARE DESIGN / TARGET-BLIND RUNTIME — OWNER RETEST REQUIRED**.

Next owner evidence:

1. Refresh/reopen the browser and confirm there is no password prompt.
2. Run a natural participant-led pattern and adjudicate it.
3. Inspect the required-coverage count, then choose `Continue required coverage`.
4. Confirm previously covered domains are skipped and the next genuinely under-covered domain receives a neutral screener.
5. Confirm `unknown`, `inapplicable`, and `declined` terminate the domain rather than trigger repeated probing.
6. Confirm `Finish for now` reports incomplete coverage rather than claiming completeness.
7. Judge whether the current broad domain partition is useful enough for further development; before validation freeze, perform the explicit behavior-question-bank / astrology-HD coverage crosswalk and split materially overbroad domains.

Still unauthorized: external participant collection/recruitment, automated participant coding, target-model activity, merge/release, publication, production expansion, and unapproved spending.

**There was never a completion policy.**
