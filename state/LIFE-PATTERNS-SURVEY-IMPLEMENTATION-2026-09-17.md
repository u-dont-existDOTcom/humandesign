# Approved survey implementation — 2026-09-17

Status: **IMPLEMENTED AND DEPLOYED TO THE EXISTING OWNER PROTOTYPE; HOSTED CI PASSED.** The remaining product boundary is a short owner natural-use evaluation. This is not a merge, public release, scientific-validity claim, or a claim that every generated question is good.

## What changed

**Reliable continuity.** One explicit workflow now controls the current phase and pending action. Mutations are revision-bound, single-flight and idempotent, with transactional rollback. Failed answers retain their draft and operation identity. A lost acknowledgement can be reconciled without submitting the answer twice. Error/retry controls are visible. A failed restoration preserves the old checkpoint instead of silently starting and saving a fresh interview over it. Old accepted patterns do not override a later awaiting-answer state. Pause survives a late response and refresh; Resume is explicit. Normal answer drafts survive opening, submitting or leaving a saved-pattern correction.

**Question selection and source fidelity.** Every current model route receives shared source-bound conversation, operative evidence, pattern status and corrections. Final question admission runs after runtime fallback/refinement, not merely on an earlier candidate. Cross-area selection can report no worthwhile next question while preserving incomplete coverage. A fallible formulation review distinguishes an endorsed direct report, a plausible new inference requiring judgment, and unsupported or context-only material. Direct self-knowledge need not be surprising or rare. Scope, conditions, time, negation and speaker attribution matter; an exact substring alone does not establish endorsement. The configured model/provider is unchanged.

**A coherent interface and result.** The deployed surface is one template and one renderer, replacing the inherited HTML patch chain. There is one labeled textbox, compact approximate coverage progress, no fabricated time estimate, persistent Finish for now, explicit Resume, a stable Your patterns collection with source context, and separate summary/backup/research exports. Reduced-motion preferences are respected. Saved-pattern corrections are append-only annotations: the original historical adjudication is preserved, while the current item becomes disputed and is exported as unresolved. This is not automatic acceptance of replacement wording or a new adjudication of the old proposal.

**Reproducible recovery and export.** Already-open old tabs retain the raw recovery-read contract and receive an explicit refresh boundary for obsolete mutation routes. The research export includes the exact source archive, blueprint/build identifiers, current statuses and unresolved corrections even when zero patterns were accepted. It is an immutable development record, not validation. Older transcript reconstruction remains non-scientific. Private narrative was not committed to Git.

## Exact verification and deployment

| Boundary | Verified result |
|---|---|
| Application commit | `aace9ac3a40f1a8dfd6244ab714a86563d0132c8` |
| Application tree | `140b813e37b9ab1262b18341d27050f8656452a0`; uploaded bytes matched the locally verified tree |
| CI-only compatibility follow-up | `4e727ac7b33c83f99221751196d5dc0d90a0dbd5`; no application-source change |
| Hosted CI | Run `35258133276`: **SUCCESS**; Python/test/lint/typecheck job and actual browser job both passed |
| Hosted browser job | Job `105326790223`: **13 scenarios passed**, zero page errors, zero model calls; runner-installed sandboxed Google Chrome |
| Local full suite | **815 passed, 7 skipped**, one Starlette/httpx deprecation warning, 10.92 seconds |
| Local browser suite | **13 scenarios passed**, zero page errors, zero live model calls |
| Lint | `ruff check src tests --ignore E501,I001`: PASS, preserving the repository's existing exclusions |
| Strict typing | `mypy src/hdmatch`: PASS across **207 source files** |
| Diff and task preflight | PASS |
| Railway owner prototype | Deployment `03e306da-08c8-497a-993b-fd72c4ef2a1c`: **SUCCESS**, source application commit above |
| Live health | `/healthz`: HTTP **200**, build `survey-flow-2026-09-17.1`, exact application commit reported |
| Live page identity | Checked 2026-09-17 18:23 UTC: HTTP **200**, 30,613 bytes; SHA-256 `73476297122d61934a4489cea8fce16f4cf2c67d66c892c630874e89448fd718`; byte-for-byte equal to the verified candidate HTML |

Local skips were four historical-commit checks unavailable in the shallow checkout and three official-ephemeris-file smoke cases. The isolated VPS Python environment omitted the unrelated pyswisseph build because no compiler was present; hosted CI installed the complete checked-in lock. No system packages or global machine policies were changed.

The first hosted browser attempt, run `35257645705`, failed before executing tests because the downloaded Chrome binary lacked a usable sandbox under the runner's AppArmor restrictions. The Python/lint/typecheck job passed. The CI-only correction selected the runner-installed Chrome with its existing sandbox support; it did **not** add `--no-sandbox` or weaken host policy. The subsequent browser run executed and passed all 13 cases. This was an infrastructure failure and repair, not evidence of inferior application semantics.

Browser cases cover original-checkpoint preservation, visible next-question retry, failed-answer draft retention, lost acknowledgement, overlapping sends, pause during delayed generation/reload/resume, historical acceptance versus the newer question, stable patterns and append-only correction, preservation of the ordinary answer draft, inference judgment and automatic continuation, no-worthwhile-question without false completion, zero-pattern export metadata, and responsive/reduced-motion/label checks.

Responsive checks covered 320, 375, 414, 768, 1024 and 1440 CSS pixels. Native mobile keyboards, full zoom/contrast/screen-reader conformance and real-model latency/quality were not certified. The new hosted browser job now tests actual UI behavior rather than treating the existence of an HTML string as proof of a working transition.

## Preserved authority and remaining work

Owner approval is recorded in `tasks/LIFE-PATTERNS-SURVEY-APPROVED-IMPLEMENTATION-2026-09-17.md`. The accepted v2 evidence contract and 23-dimension neutral blueprint are unchanged. No birth target, chart, expected direction, scoring map or candidate rank enters runtime elicitation. No arbitrary episode/counterexample quota was added.

The existing passwordless owner-development service and configured model/provider were reused. No new service, access-policy change, external participant collection, paid evaluation campaign, public release or merge occurred. The development pull request remains draft/open/unmerged.

Next: refresh the existing interview and conduct a short owner test of question usefulness, remembered context, saved pattern accuracy and correction burden. These judgments remain open despite green deterministic tests. A new frozen interview and the separately authorized owner-self historical AstroHD recovery regression are later scientific/product evidence boundaries, not completed by this implementation.

Evidence: `artifacts/life-patterns/survey-implementation-2026-09-17/browser-regressions.json` and `deployment-receipt.json` in the same directory. Final local test-efficiency receipt reports 96.86 seconds of tests across the measured 3,723.57-second interval (2.6%); 12 focused/affected and three full runs, zero mutation runs and zero forced unchanged-green reruns. Full checkpoints were repeated only after a substantive legacy-correction fix or the required owner-state prose repair. Transport/setup activity is not counted as direct product improvement.

**There was never a completion policy.** Preserve the owner correction in `state/OWNER-CORRECTION-2026-09-02.md`; do not invent additional mandatory scientific-completeness gates from task bookkeeping.
