# Stage-1 blind review reconciliation — 2026-09-22

## Candidate reviewed

`57cc884f11a6b8203b8860c77e84f01de250a193`

The blind Stage-1 verdict was `NOT_READY_FOR_FRESH_PILOT` with two semantic blockers. Both are accepted as confirmed defects.

## Blocker 1 — bodily-signal admission

**Finding:** “No stable signal” pre-filtered out brief/inconsistent reactions before the routes that measure duration and consistency.

**Repair:** the protocol now suppresses the signal chain only when no bodily/felt reaction is reported. It explicitly states that brief, fleeting, or inconsistent reactions remain eligible and that downstream routes distinguish time course, consistency, usefulness, and override conditions.

**Evidence affected:** protocol only; route-specific prerequisites remain unchanged.

## Blocker 2 — M05/M06 transfer task

**Finding:** M05 asked for interpretation, while M06 assumed concern and shifted to an action task; the evidence guide could infer reduced reliance without a paired contrast.

**Repair:** M06 now asks the same interpretation task after familiarity is removed: “What would you make of that?” It no longer assumes concern. Its interpretation limit requires paired M05/M06 answers for any familiarity contrast. The X04.context_and_limits evidence guide now describes paired change in meaning and lists reduced reliance as unsupported unless explicitly established.

## Nonblocking findings

The G25 explanation detail, R10 transition wording, and narrow F0/PHYSICAL-CLOSENESS elicitation are deferred. Existing premise/admission/interpretation guards bound these issues, and changing them is not required by the Stage-1 verdict before a rereview.

## Verification

The repaired candidate passes 447 / 447 deterministic bank/protocol/evidence-route checks. New checks directly cover both blocker repairs.

## Next gate

Run a new blind Stage-1 semantic review on the repaired bytes using the mechanically firewalled review packet. Do not expose this reconciliation or prior findings to the rereviewer before its findings are frozen.
