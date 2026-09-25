# Life Patterns v2 — owner long-thread resilience repair — 2026-09-16

## Owner consumer-seam finding

A long owner interview exposed a compound product failure. The participant experienced repeated semantic questions, a progress display that remained at zero throughout the active thread, no updated final synthesis after refinement, and a failure when accepting the displayed synthesis. Because the development runtime stored the hidden ledger only in process memory, the failure also created a reasonable data-loss concern.

No private interview narrative is stored here. This receipt preserves only abstract product findings and repair behavior.

## Verified generating conditions

### 1. Semantic repetition from a short planner window

The normal interviewer planner received only a short tail of recent conversation and the refinement planner received a similarly short tail. In a long thread, early questions and answers therefore fell outside the model-visible planning window. The interviewer could then ask a semantically equivalent observer-view or scope question again despite the participant having already answered it.

### 2. Progress was adjudication-gated

The browser aggregate coverage state advanced only after a pattern received participant adjudication. Evidence accumulated during a long unsettled thread was not returned to the client as progress evidence, so the participant-visible indicator could remain at 0% while substantial material had already been supplied.

### 3. Refinement could not lawfully emit a final synthesis

The refinement contract explicitly prohibited `surface_hypothesis`. Once a thread entered refinement, the model could ask another question or state that no high-value question remained, but could not produce the updated synthesis that the participant needed to judge.

### 4. A tentative proposal could outlive its supporting fact

The runtime committed a tentative model synthesis into `pattern_proposals` before participant adjudication. Subsequent participant correction could supersede one of that proposal's supporting facts while the original proposal remained active. Final v2 validation correctly rejected that stale proposal because its grounding no longer referred only to operative evidence.

### 5. Process-memory storage lacked participant-controlled recovery

The development runtime intentionally did not persist private interview narrative to Git or Railway storage, but the browser also kept no local recovery copy. A container restart therefore removed the exact server-side hidden ledger with no participant-controlled fallback.

## Repair candidate

Current implementation:

- `src/hdmatch/api/life_patterns_v2_owner_resilient.py`
- `src/hdmatch/api/life_patterns_v2_owner_resilient_ui.py`
- `tests/unit/test_life_patterns_v2_owner_resilient.py`

Behavioral changes:

1. normal and refinement planners receive up to the practical full thread window (80 turns) rather than the prior short tail;
2. the interviewer is explicitly told that semantic rewording of an answered question is still repetition and that one pattern thread must not expand merely to consume every adjacent standardized dimension;
3. when refinement has no more decision-changing question, it may and should return a new `surface_hypothesis` grounded only in current operative facts, so the participant receives an actual final tentative synthesis;
4. model-generated syntheses remain ephemeral working drafts until participant adjudication; only the currently displayed draft is materialized into the v2 record immediately before participant judgment, preventing later fact corrections from stranding a durable stale proposal;
5. a bounded coverage assessment is attached periodically during an active thread so the browser can update its approximate completion horizon before pattern adjudication;
6. progress refresh is auxiliary: failure to refresh the estimate cannot fail an otherwise successful interview turn;
7. the browser stores a bounded visible-turn recovery copy in local storage and offers a local download. This is recovery-only and is explicitly not the scientific measurement freeze.

The target-theory-blind runtime boundary and accepted v2 semantic substrate are unchanged.

## Recovery boundary for the failed owner session

The exact prior hidden evidence ledger is not guaranteed recoverable after the in-memory service restarts. The owner supplied the visible transcript back to the supervising chat, so the visible conversation itself can be preserved privately and used as development recovery material without committing it to the repository. It must not be represented as the final fresh pre-scoring measurement freeze.

## Verification boundary

The repair is not accepted merely because local logic is plausible. Required evidence is:

- regression coverage for full-thread memory, updated-synthesis refinement, current-fact rebinding, successful adjudication, in-thread progress delivery, and browser-local recovery UI;
- GitHub CI green for tests, Ruff, and strict mypy on the exact candidate head;
- Railway deployment success and `/healthz` HTTP 200 on the exact application head;
- owner consumer-seam retest confirming that a long thread no longer repeats established questions, progress moves before final adjudication, refinement ends in an actual synthesis, and acceptance succeeds after participant corrections.
