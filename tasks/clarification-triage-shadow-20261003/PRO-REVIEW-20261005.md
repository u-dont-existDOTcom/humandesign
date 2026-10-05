# Pro review — fast clarification pipeline — 2026-10-05

## Authority and scope
Owner: “insetad of claude you can use this pro pass now to check it”. This replaces the pending Claude check for this task. It does not claim cross-family review or an untouched blind context: the owner supplied the development history.

Reviewed base: `2bc0365b532d0347c5243aa798ffd35a059eb15f`. Parent outcome remains OPEN: faster useful end-of-interview clarification, source fidelity, independent admission, information-based stopping, fewer wait/approval cycles.

Current lane: decision/review with reversible shadow repairs. Live deployment and GPT configuration remain unchanged during the review.

## Active checks
- Exact current source, frozen behavioral instrument; no birth/chart data or scoring rules enter model packets.
- Approved gap is distinct from ready-to-ask wording; both are required before question delivery.
- Every recovered question must pass complete-source independent admission; omission detection alone is not authorization.
- No-question, unresolved, and pending-review states remain distinct.
- Source text, filenames, IDs, prompts and raw model outputs remain outside committed benchmark telemetry; synthetic fixtures are labelled synthetic.
- Isolated branch, preserve baseline, reproduce failures before repair, run focused tests then participant suite, publish and read back exact artifacts.

## Review status
IN_PROGRESS. No acceptance based on historical green labels alone.

## Initial findings frozen before repair
1. HIGH — The matched-source omission detector directly authorized recovered routes and could overrule `already_answered` / `low_information_gain` rejection without a fresh full-source admission. Its local context can omit a distant resolving answer. Reproduced by two deterministic contract tests.
2. HIGH — A gap whose question failed both wording checks remained the selected/recommended question despite an empty `final_questions` map. Reproduced.
3. HIGH — A deferred omission check could coexist with reported `review_ready`; replay collapsed unresolved outcomes into ready. Reproduced for the summary; replay branch inspected.
4. MEDIUM — Five source turns mapped to one route exceeded a four-reference binding limit and crashed the audit. Reproduced.
5. HIGH — Unasked dependent routes can be removed before semantic review when a valid antecedent is paraphrased without a canonical ID; lower-confidence matching happens too late, after menu exclusion. Additional regression queued before repair.

The five original Pro contract probes failed at the reviewed base. These are deterministic engineering failures, not measured frequencies of application-model mistakes.
