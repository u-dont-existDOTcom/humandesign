# Owner-scale critical-path omission-audit experiment — 2026-10-04

## Change

A new shadow-only `defer_if_admitted` match-audit policy removes omission reconciliation from the immediate clarification-return path once at least one route-level gap has independently passed GapAdmission.

The full blocking behavior remains the default/control. Under the critical-path policy:
- if at least one gap spec is admitted, the current valid clarification batch can proceed and the match audit is marked deferred;
- if triage is review-ready or all proposed gaps are rejected, the match audit still runs before a no-question/stopping result can be returned;
- no model effort, clarification-count cap, admission rule, or wording gate is weakened.

## Focused verification

- Ruff passed.
- 32/32 shadow-triage tests passed.
- Tests explicitly verify that a valid admitted question defers the audit, while a would-be no-question result still performs omission audit and can recover an omitted route.

## Owner-scale benchmark

Same recovered 81-turn owner source, GPT-5.6 Sol xhigh.

Control full pipeline:
- total semantic time: 554.368s (9m14.4s);
- GapMatchAudit: 248.174s;
- match audit covered 54 pairs and 80/81 source turns.

Critical-path policy:
- total semantic time: **281.539s (4m41.5s)**;
- GapTriage: 168.521s;
- GapAdmission: 113.018s;
- GapMatchAudit: deferred, 0 blocking seconds;
- 54 audit pairs recorded as deferred;
- no wording render/review was needed in this run.

This is a **49.2% reduction** in semantic critical-path time versus the control, without lowering model effort.

The run admitted two immediate routes. Route identity differs from the earlier stochastic control run, so this benchmark is latency evidence rather than a same-sample quality comparison.

## Decision

The omission audit should not block an already-valid clarification batch. This is a useful improvement but it does not yet meet the 1–3 minute target. Remaining blocking cost is triage (~169s) plus admission (~113s).

Next experiment: reduce duplicated context on those two blocking calls while keeping exact participant source semantics and full route authority available at admission.
