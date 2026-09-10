# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-R05-FACET-OVERLAP-AND-ABSENCE-SEMANTICS-DEFECT-2026-09-10.md`
4. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt`
5. `state/LIFE-PATTERNS-HUMAN-UI-DIRECT-CHOICE-CORRECTION-2026-09-09.md`
6. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-DIRECT-CHOICE-VERIFIED-2026-09-09.json`
7. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
8. `state/LIFE-PATTERNS-HUMAN-UI-HUMAN-FIRST-CORRECTION-2026-09-09.md`
9. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
10. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
11. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
12. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
13. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
14. `state/CURRENT-STATE.md`
15. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 correction, private v2 freeze, and several rounds of owner-led human-interface simplification are complete. **However, human calibration is newly blocked before collection by a theory-neutral subcode-overlap / absence-semantics audit.**

No qualifying independent human first-pass annotations have been collected. No automated Life Patterns coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Newly discovered R05 problem

Owner review of the direct-choice UI exposed that NBM-R05 is being displayed as one flat behavior list even though the frozen reconciled codebook explicitly defines **two different facets**:

- option-set construction: `R05-O1..R05-O6`;
- choice resolution: `R05-R1..R05-R9`.

Some values across those facets are therefore expected to co-occur. The human should not be forced to infer this architecture from one undifferentiated list.

More importantly, `R05-O2` is worded:

> accepts one/default option **without searching for alternatives**

This is a hybrid value: affirmative acceptance/default-selection behavior plus an absence-of-search condition. It can plausibly overlap with:

- `R05-R1` — selects without reported comparison / first acceptable option;
- `R05-R4` — follows an explicit rule, prior commitment, or default.

The frozen compact non-action registry includes `R05-O2` because the **absence-of-search clause** requires evidence that search did not occur. That does **not** mean accepting the default is itself “did not act.” The current generic human gate wrongly collapses the whole hybrid value into “did not act” language and asks generic absence questions without naming the absent action.

This is now treated as a possible substantive measurement defect, not merely a UI-copy defect.

## Exact next gate

Run:

`state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt`

in a **fresh target-theory-blind context** using only:

1. the exact reconciled neutral codebook;
2. the compact non-action classification;
3. the frozen ambiguity-resolution amendment;
4. the original non-action-classification prompt for semantics of the registry label.

The audit must review **all 22 observables**, not just R05, for:

- explicit/implicit multi-facet structure;
- overlapping/nested/near-duplicate subcodes;
- hybrid affirmative+absence codes;
- exact absent action/proposition required by every non-action gate;
- response-contract limitations for co-occurring facets/sequences;
- measurement-level double-count/redundancy risk.

Preserve the raw audit JSONL + summary before theory-exposed review.

### Disposition after audit

- If findings are presentation-only: repair the UI so facets are explicit and every absence-dependent gate names the precise absent action.
- If the current response contract cannot represent facet/co-occurrence/sequence structure cleanly: make a new versioned response contract before collection.
- If frozen subcodes themselves overlap too much for reliable blind coding: perform a new **theory-blind versioned codebook clarification/revision**, preserving all historical artifacts unchanged, then regenerate dependent package/handoff/UI.

Do not use target-model information to resolve these issues.

## Why current auditor kits are suspended

All current private auditor kits were built before this overlap/absence audit. They remain historical owner-review artifacts only and must **not** be given to an independent auditor for new collection until the new gate is cleared.

The direct-choice UI corrections remain useful design constraints:

- ask the substantive human question directly;
- derive machine states behind the scenes;
- hide machine IDs;
- one-source provenance automatic;
- no optional research-data busywork;
- multi-behavior order asked only after multiple behaviors are actually selected;
- errors tell the human what to do.

But those interface improvements cannot compensate for unresolved measurement overlap or incorrectly scoped absence semantics.

## Recurrence correction remains controlling

- generalized behavioral self-report is direct **reported recurrence** evidence;
- confirming anecdotes selected after a recurrence claim are not independent frequency evidence;
- scope/denominator, exceptions, exception frequency, and temporal/context boundaries are preferred follow-ups;
- no fabricated occurrence floor is required.

## Hard boundaries

- no current auditor kit may be used for new human collection pending the overlap/absence audit;
- no theory-exposed substantive neutral-codebook repair;
- no automated Life Patterns coding before the eventual revised independent human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
