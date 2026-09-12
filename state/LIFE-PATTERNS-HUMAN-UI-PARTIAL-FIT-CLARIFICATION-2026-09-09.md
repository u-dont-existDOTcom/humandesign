# Life Patterns human calibration — partial-fit clarification

Status: owner-led pre-collection UI/method clarification. No independent human first pass has begun.

## Problem found

The human-facing state buttons were phrased as a fit rating:

- Yes — clearly shown
- No — does not fit
- Can't tell

That naturally creates the question: **where is “partially”?**

The underlying frozen response states are not actually a three-point fit scale. They are three different measurement conditions:

- `observed`: the exact source contains enough evidence to choose one or more substantive behavioral values for the observable;
- `not_applicable`: the prerequisite situation for the observable is affirmatively absent;
- `insufficient`: the observable may be relevant, but the exact source is too incomplete/unclear to support a reliable substantive behavioral code.

A generic fourth state called `partial` would collapse distinct situations and make coder agreement less interpretable.

## Controlling human rule

Do **not** add an undefined “Partially” state to the frozen response contract.

Instead present the actual decision:

1. **Enough information to code** → `observed`
2. **Doesn't apply** → `not_applicable`
3. **Not enough information** → `insufficient`

Explicitly tell the human:

> This is not a fit scale. If some pieces fit but there is not enough exact evidence to choose a listed behavior reliably, choose **Not enough information**.

## Cases that might otherwise be called “partial”

### Some prerequisites/evidence are present, but not enough to choose a behavior

Use **Not enough information** (`insufficient`).

### The source clearly shows more than one behavioral response

Use **Enough information to code** and select every clearly supported behavior; then answer the conditional sequence question if multiple behaviors are selected.

### A listed behavioral value is only partly supported

Do not select it merely because part of its wording fits. Use another fully supported listed value, Other Specified if its frozen rule is satisfied, or **Not enough information** when the source cannot support a defensible code.

### The broad situation clearly does not occur

Use **Doesn't apply** (`not_applicable`), not partial or insufficient.

## Scientific boundary

This clarification changes human-facing wording only. It does not change:

- the 44 episode + 22 repeated-series selected units;
- exact private source evidence;
- the `observed / insufficient / not_applicable` response contract;
- behavioral subcodes;
- recurrence semantics;
- target-model blindness;
- calibration chronology.

No automated labels, target-model outputs, or post-hoc fit information were used to make this clarification.
