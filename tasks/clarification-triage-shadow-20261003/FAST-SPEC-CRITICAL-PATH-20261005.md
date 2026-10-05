# Fast spec-only clarification critical path — 2026-10-05

This development branch replaces question-producing GapTriage/GapAdmission on the first-batch critical path with small route-level GapSpecTriage/GapSpecAdmission outputs.

Key behavior:
- Triage returns only up to three route-level gap specs: route ID, exact source anchors, antecedent/context binding, one missing distinction, and dependencies. It does not draft participant-facing questions.
- Admission judges only whether each route-level gap exists; wording cannot erase a valid gap.
- A new self-contained canonical route can be materialized deterministically from the frozen bank. Repair/dependent questions are rendered only after gap admission and receive a wording-only adversarial check.
- Broad omission/match audit is deferred only after at least one gap has independently passed admission. If no gap is admitted, the audit still runs before returning no clarification and can recover an omission.
- Repair bindings keep both the prior route turn and required dependent context. Canonical context wins; high-precision lexical matches are next; model-supplied semantic context or a lower-confidence lexical context candidate is explicitly marked for independent semantic-equivalence admission rather than treated as proven.

Focused evidence:
- Ruff passed.
- 36/36 shadow-triage focused tests passed.
- Frozen v16 tuning cases Y1, Y2, Y4, Y7, Y8 and Y10 all passed across the post-repair runs. Latest context-candidate changes affect only dependent context binding; Y8 and Y10 were rerun afterward and passed.
- These v16 runs are tuning evidence only, not fresh promotion evidence.

Fresh cross-family validation remains blocked by the Claude Code weekly quota recorded on the v17 validation branch. The next independent measurement is owner-scale 81-turn latency on this fast-spec path.
