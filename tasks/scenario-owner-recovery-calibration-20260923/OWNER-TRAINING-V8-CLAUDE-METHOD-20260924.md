# Owner-trained scenario survey v8 — Claude Opus 5.5 development method — 2026-09-24

Status: **TARGET-AWARE OWNER TRAINING / DEVELOPMENT, NOT VALIDATION**.

## Owner correction

The owner explicitly rejected treating the 79-answer freeze as a terminal measurement boundary. The actual development goal is to make the survey/recovery method work on the known owner case first. The prior frozen run remains an immutable audit snapshot only; it is not a reason to stop improving the survey.

## Training target

Known development target:

- recorded birth: 1985-01-29 10:25 UTC, Philadelphia;
- persistent competing date neighborhood: 2013-01-28/29;
- earlier same-date 1985 intervals remain relevant for time discrimination.

Because the target and competitors are now deliberately exposed to the designer, all changes produced in this phase are owner-trained/post-selection development evidence. They may improve the product but cannot later be counted as independent confirmation on this owner case.

## Goal

Use Claude Opus 5.5 at max effort as a target-aware survey designer/debugger to identify the smallest set of **real behavioral distinctions** needed to:

1. distinguish the recorded 1985 date neighborhood from the persistent 2013 competitor; then
2. distinguish the recorded 10:25 time neighborhood from other 1985 intervals.

The designer may inspect the complete existing private answer history, neutral profile, survey-v7 bank/protocol, Survey-v2 field vocabulary/dependency map, and exact structural field differences among the training target and competitors.

## Constraints on proposed survey fixes

A proposed discriminator is admissible only if:

- it has a plausible participant-observable behavioral meaning independent of the known target;
- the question can be phrased without Human Design/astrology/chart jargon;
- at least two plausible ordinary-life answers exist;
- the answer is not nearly forced, tautological, or merely a restatement of availability/feasibility;
- it does not ask the owner to endorse a flattering/general identity label;
- it does not infer a hidden structural mechanism from behavior unless the mechanism makes a separately measurable behavioral prediction;
- existing answers are checked first so we do not re-ask a distinction already answered;
- question wording must pass the existing final rendered-question admission checks plus expected information gain.

The designer may reject chart differences that do not yield defensible behavioral predictions.

## Required Claude output

Claude must return:

1. diagnosis of which existing survey distinctions failed to separate the target from 2013 and why;
2. ranked candidate behavioral discriminators for **date recovery** and **time recovery**;
3. for each candidate: source structural/Survey-v2 field difference, behavioral hypothesis, existing-answer status, risk of target overfit, and expected discriminating value;
4. exact proposed scenario question(s) only for the smallest high-value set;
5. explicit admission check for each question;
6. proposed v8 facet/contract semantics and scoring direction for development;
7. a stop rule: ask one question at a time, recalculate training-case separation, and stop adding questions once the target is sufficiently separated for this development stage.

Claude may use the target to select constructs, but it must not fabricate the owner's answer or choose wording that signals which answer is desired.
