# AstroHD V4.3 freeze clarification — 2026-09-23

Owner concern: if AstroHD V4.3 still did not rank the known owner birth target first, a vague "frozen model" rule must not block legitimate model repair.

## Exact status

The repository preserves two different V4.3-style owner results:

1. **Older V1.1 merged HD + Western benchmark:** correct date is the top refined neighborhood; exact recorded moment ranks #2 against the hourly century universe; refined local peak is +11 minutes.
2. **Cleaner candidate-unexposed V4.3 HD/NetInformation-style variant:** a 2013 interval ranks 1; a correct-date 1985 interval ranks 2.
3. **Best-current descriptive V4.3 variant:** after two carrier refinements were added with the 1985 candidate already exposed, a correct-date 1985 interval ranks 1. That rank-1 interval does not contain the exact recorded birth moment.

Therefore "V4.3 ranks the owner #2" and "V4.3 ranks the owner #1" are both incomplete shorthand, and describing the latter as better exact birth-time recovery is wrong. V1.1 and V4.3 also use different scoring architectures; the V1.1 benchmark is a merged HD + Western scan, whereas this V4.3 audit is the HD/NetInformation-style model.

## What is frozen

The historical audit result and its pre/post-selection provenance are frozen. This prevents retroactively rewriting the cleaner rank-2 result after seeing the answer. It does **not** prohibit improving AstroHD.

Any improvement learned from this owner case must be versioned as a new explicit post-ranking revision/model version. The owner case is valid development/training evidence for that revision, but its fitted result is not independent validation.

## Why survey calibration uses the legacy recovery gate first

The current task is to test whether the repaired survey captures enough information. The historical V1.1 merged benchmark is the known scorer that previously localized the target date/time neighborhood tightly. The cleaner V4.3 variant is already known to prefer a 2013 interval and the descriptive V4.3 rank-1 interval does not contain the exact recorded moment, so using V4.3 as the sole survey pass/fail criterion would mix two unknowns: survey quality and model quality.

After the neutral v7 profile is frozen, run the historical recovery gate first. V4.3 diagnostics remain useful separately. If a future best-current model fails the frozen owner profile, that opens a versioned model/crosswalk development problem; it does not justify mutating the historical V4.3 audit in place.
