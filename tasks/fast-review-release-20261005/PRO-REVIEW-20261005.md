# Pro review — Life Patterns fast clarification pipeline

Date: 2026-10-05
Decision: **Review accepted after repairs, for controlled integration. Not deployed.**

## Authority and review boundary

The owner instructed: “insetad of claude you can use this pro pass now to check it”. This replaces the pending Claude check for this task. There is no remaining requirement to wait for that provider's quota reset before acting on this review.

This is an owner-authorized Pro code/requirements review with executable checks. It is not a cross-family check or an untouched blind review: the owner supplied the development history. The application-model tests used the existing isolated `gpt-5.6-sol` / `xhigh` configuration. They are software-development evidence, not validation of Human Design, astrology, or human prediction.

Reviewed baseline: `2bc0365b532d0347c5243aa798ffd35a059eb15f`.
Repaired code and frozen test packet: `a39228f89c12a3a03742efd5b067a7477dffadc2`.
Review branch: `pro/gap-triage-review-20261005`.

The review request is complete. The parent product outcome remains open: the faster clarification stage is not yet connected to the live reviewer or Custom GPT. The inherited experiment's no-live-change boundary remains intact.

## What the review found

The earlier statement that only the Claude quota remained was too strong. The published code had concrete defects that the historical green tests had not excluded. Six new contract probes reproduced five defect classes before any repair:

| Defect | Consequence | Repair |
|---|---|---|
| Omission recovery could bypass independent admission and reverse an answered/low-information rejection. | A local omission detector could cause a redundant question even when a distant answer resolved the issue. | Recovered candidates now require a separate complete-source gap-admission call. A detector cannot override an existing independent veto in the same pass. |
| A gap could remain the selected question after both wording checks rejected it. | The summary could recommend clarification despite an empty usable-question map. | Gap approval and ready-to-ask wording are separate. Selection uses only final approved questions; exhausted wording repair is an explicit failure state. |
| Deferred or unresolved review could be presented or scored as ready. | Missing work could disappear behind a successful no-question result. | Pending, unresolved, wording-failed, and ready outcomes stay distinct. The replay no longer maps every non-clarification result to ready. |
| More than four presentations of one route exceeded the audit's binding limit. | A valid long record could crash the audit. | Caller-owned bindings preserve all route presentations, within the existing 1,000-turn import bound. |
| A valid paraphrased antecedent could remove an unasked dependent route before semantic review. | A useful follow-up could be impossible to select merely because its preceding question lacked a canonical ID. | The fast menu permits semantic-context candidates, but still requires actual answered antecedents and independent contextual-equivalence admission. Menu membership never proves eligibility. |

The omission repair also preserves the admitted source/context bindings through question rendering. Previously rejected work is not silently rehabilitated by a weaker detector. Excess omission candidates remain explicitly pending rather than being mistaken for completed review.

One old unit test explicitly expected omission recovery to override admission. Its assertion was corrected to preserve admission authority; the bypass was not retained merely to keep that historical test green.

## Verification actually performed

- **Six new Pro contract regressions:** failed at the baseline, passed after repair.
- **Focused shadow tests:** 44 passed, including those six regressions.
- **Full participant suite:** 160 passed in 22.88 seconds. This includes the focused tests; the totals are not additive.
- **Affected-file Ruff checks:** passed.
- **Six new semantic cases:** all expected decisions and usable route sets matched in one application-model run per case. Targets were frozen before execution; the code was unchanged during the run.

Unlike the earlier small-route replays, the new semantic cases did not hide unrelated bank entries. All 78 eligible route cards were visible, and the normal import path handled source IDs and corrections.

| Synthetic case | Expected and observed result | Semantic time |
|---|---|---:|
| Complete factors and already-described negotiation preference | No clarification | 18.029 s |
| An unidentified purpose for unexpected money | Clarify the money-purpose route | 33.030 s |
| Paraphrased meal-cost antecedent with explicitly unsettled persistence | Clarify negotiation preference | 34.027 s |
| A procedural answer resolved by a distant later answer | No clarification | 17.014 s |
| Explicit correction plus an inability/skip response | No clarification | 17.014 s |
| Two independent gaps, including conflicting answers to the same scene | Both clarifications | 41.026 s |

These are Pro-authored requirement probes, not an independent population sample. They demonstrate the tested behavior, not a universal error rate or broad statistical non-inferiority. Generated wording was also inspected; it remained tied to the supplied source and route tasks.

## The repaired 81-turn benchmark

The private owner record was processed without copying its text into repository reports.

- Behavioral turns: **81**.
- Eligible route cards: **78**.
- Application model setting: **gpt-5.6-sol, xhigh**.
- Semantic time until a usable first clarification batch: **114.164 seconds (1 minute 54.2 seconds)**.
- Ready questions: **3**; no wording rejections.
- Full final review/evidence synthesis completed: **false**.
- Broad omission audit: **pending**, deliberately outside the first-batch path after independent gap admission.

| Stage | Seconds |
|---|---:|
| Gap-spec triage | 75.142 |
| Independent gap admission | 14.008 |
| Question rendering | 14.007 |
| Wording review | 11.007 |
| **Total** | **114.164** |

The preceding implementation's reported run was 112.159 seconds. This repaired run preserves the approximately two-minute first-batch result without lowering the configured reasoning effort. It does not establish that every interview, no-question path, or full final synthesis will finish within three minutes.

## Integration disposition

**The Pro review replaces the pending Claude gate and is accepted after the repairs above.** The unchanged original candidate should not be promoted; use the repaired code identified here.

This is approval to proceed with controlled integration of the first-clarification stage, not a claim that production is already ready. The live Engine, review worker, HTTP API and Custom GPT files are unchanged relative to the reviewed baseline. No service was deployed, no GPT installation bundle was generated, and no participant submission/freeze was performed.

The existing live API still exposes one clarification at a time. The small-batch shadow result does not by itself implement local question batching, one batch-answer Action, durable deferred-audit scheduling, or final synthesis. Those remain application integration work, not another Claude-review prerequisite.

The integration contract is saved alongside this report as `PRO-INTEGRATION-CONTRACT-20261005.md`. It retains the existing information-based stopping rule and source/consent boundaries; there is no new lifetime clarification cap.

## Evidence and recovery

All evidence is in `tasks/clarification-triage-shadow-20261003/` on the review branch:

- `PRO-REGRESSION-BEFORE-20261005.txt` and `PRO-CONTEXT-MENU-BEFORE-20261005.txt`: pre-repair failures.
- `PRO-PARTICIPANT-SUITE-20261005.txt`: full suite result.
- `PRO-SEMANTIC-CASES-20261005.json`, `PRO-SEMANTIC-EXPECTED-20261005.json`, `PRO-SEMANTIC-MANIFEST-20261005.json`: frozen synthetic cases, targets and code binding.
- `PRO-SEMANTIC-RESULTS-20261005.jsonl` and `PRO-SEMANTIC-EVALUATION-20261005.json`: actual full-bank results and evaluation.
- `PRO-SEMANTIC-SYNTHETIC-TRACE-20261005.jsonl`: explicitly synthetic structured outputs only, not private owner source or provider prompts.
- `PRO-OWNER-SCALE-20261005.json`: privacy-safe 81-turn timing receipt.

The current checkpoint supersedes earlier task-local instructions to wait for Claude, but preserves those historical reports as evidence. It does not promote unrelated research branches or alter any frozen scoring model.
