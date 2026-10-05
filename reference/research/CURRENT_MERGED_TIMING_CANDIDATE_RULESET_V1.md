# Current merged timing candidate ruleset

Status: CURRENT DEVELOPMENT REGISTRY.

Owner rule: whenever a timing ruleset produces a very strong match, add the exact rule to the merged candidate registry rather than leaving it only in chat or a one-off experiment.

Canonical registry:
- reference/research/current_merged_timing_candidate_ruleset_v1.json

Retention requirements:
- preserve exact executable parameters or an exact frozen source reference;
- record whether the motivating outcome was known before the rule was created;
- retain false positives, ties, misses, and unchanged transfer tests;
- never retune an existing rule after a transfer miss; create a new version;
- keep endpoint-specific rules separate from generic timing rules;
- a strong retrospective fit earns retention, not validation.

Current candidates:
1. daily_three_family_angle_activation_v1 — generic high-activation-day candidate. It uniquely matched Hale's September 23, 2026 event date in the motivating post-outcome case, but missed Joel's June 5, 2002 family-loss date when transferred unchanged; it instead flagged April 8-9, 2002.
2. father_loss_v4_sudden — endpoint-specific development candidate. It placed June 5, 2002 in the top-score state but did not uniquely localize the day and retains earlier false positives.

The registry is cumulative: future strong rulesets are appended with their evidence and limitations instead of replacing earlier candidates.
