# Blind rereview reconciliation — candidate 73c52ee — 2026-09-22

Reviewed candidate: `73c52eef27b8a1af4bc17b0ea33563cdf137592a`

Blind verdict: `NOT_READY_FOR_FRESH_PILOT`; `semantic_change_required=true`.

## Confirmed blockers and repairs

1. **M04 stipulated continued intention while claiming evidence about will versus available energy.** The stipulation is removed. M04 now holds the bounded M03 task/time/obligations constant, introduces unusual tiredness and mistakes, and asks only what that tiredness changes about the respondent's intention to finish. Evidence credit is limited to the answer-originated change or non-change in intention; execution/capacity are not inferred.

2. **R08 left weekly recovery ambiguous and used a near-forced extreme workload.** R08 now uses the same work modality and ordinary conditions for four weeks at about 8.5 hours/day, six days/week, explicitly includes one full no-work day each week for normal rest/personal activity, and explicitly excludes additional vacation/recovery periods. The endpoint is the end of the sixth workday of week four. The workload is intentionally less extreme so materially different energy trajectories remain plausible.

## Adopted nonblocking cleanup

- `M05`/`X04.cue_form` now describe respondent-assigned meaning to a stimulus-presented route deviation rather than implying the respondent independently reported/detected the cue.
- `OWNERSHIP` now uses a concrete access-equivalent laptop scenario that removes hidden availability, software-access, privacy, and cost differences.
- The interview protocol now states explicitly that the target internal state itself must remain answer-originated, and that multi-day/week workload routes must specify nonwork-day recovery assumptions.
- The exploratory sensory-conflict item now has protocol-level defense in depth: exploratory routes cannot fill canonical evidence or reopen a naturally stopped canonical interview.

## Verification

The repaired candidate passes 483 / 483 deterministic checks, including direct regression assertions for both blockers and the adopted semantic boundaries.

## Next gate

Commit the exact repaired bytes and run another fresh mechanically firewalled GPT-5.6 Sol xhigh semantic review. Do not expose any prior review findings, reconciliation, rationale, audits, verification verdicts, or private participant material before findings freeze.
