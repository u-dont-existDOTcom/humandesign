# AstroHD V4.3 freeze clarification — 2026-09-23

Owner concern: if AstroHD V4.3 still did not rank the known owner birth target first, a vague "frozen model" rule must not block legitimate model repair.

## Exact status

The repository preserves two different V4.3-style owner results:

1. **Cleaner candidate-unexposed variant:** 2013 rank 1; actual 1985 state rank 2.
2. **Best-current descriptive variant:** after two carrier refinements were added with the 1985 candidate already exposed, the actual 1985 state ranks 1.

Therefore "V4.3 ranks the owner #2" and "V4.3 ranks the owner #1" are both incomplete shorthand unless the contamination/version status is named.

## What is frozen

The historical audit result and its pre/post-selection provenance are frozen. This prevents retroactively rewriting the cleaner rank-2 result after seeing the answer. It does **not** prohibit improving AstroHD.

Any improvement learned from this owner case must be versioned as a new explicit post-ranking revision/model version. The owner case is valid development/training evidence for that revision, but its fitted result is not independent validation.

## Why survey calibration uses the legacy recovery gate first

The current task is to test whether the repaired survey captures enough information. The historical legacy owner recovery is the known scorer that previously recovered the target. The cleaner V4.3 variant is already known to rank the owner #2, so using it as the sole survey pass/fail criterion would mix two unknowns: survey quality and model quality.

After the neutral v7 profile is frozen, run the historical recovery gate first. V4.3 diagnostics remain useful separately. If a future best-current model fails the frozen owner profile, that opens a versioned model/crosswalk development problem; it does not justify mutating the historical V4.3 audit in place.
