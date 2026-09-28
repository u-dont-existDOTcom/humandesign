# Cross-family review disposition

Date: 2026-09-28
Status: reviewer found errors in the initial candidate and again in the single reconciliation. No third review round was requested. The second review explicitly stated that a dark deployment with live inference disabled had no blocker. Every concrete live-inference blocker it identified was subsequently repaired and pinned with deterministic tests before deployment.

## Initial blocking findings — repaired

- Reviewer source no longer comes from the planner-selected subset. Independent admission reconstructs authoritative source from server state, including all pending turns, cited/antecedent/control turns, both directions of correction chains, source for amended evidence, route-related prior evidence, addressed-route sources, and all admitted evidence source during final review.
- Correction chains are followed both directions. Regression fixtures put the corrected original outside the four-turn recent window.
- Final-review correction has expanded source access and correction-related evidence/facet guidance.

## Reconciliation findings — repaired

- Correction facets: planner/reviewer guide now merges facets from correction-relevant admitted evidence, including review-only evidence. The reviewer also sees that evidence even when the proposal chooses not to amend it.
- Addressed-route gate: addressed-route support is required only when the bulk proposal actually contains addressed routes. Review context includes full route cards for addressed routes as well as the proposed next question. Admitted addressed-route mappings persist only after independent admission.
- Failed-call accounting: provider failures now emit Plan/Admission telemetry before propagation and therefore count toward the session model-call ceiling. Provider ValueError/TypeError becomes provider-invalid-structured-output rather than a plan-repair rejection.
- Review reserve: four semantic calls (two Plan+Admission attempts) are reserved for review correction; deterministic bookkeeping does not consume the semantic-call budget.
- Export coverage excludes quarantined and collection-metadata turns.
- Oversized bulk/review packets fail before provider invocation with operator-context-compaction-required.
- Mixed import/new-turn sequencing completes the entire import pass first and processes newer pending source before asking another question.
- Full-guide accidental fallback is prevented: None means full guide; an empty route set means an empty guide.
- Production factory remains Venice-only; Codex CLI is development-only.
- Experimental low completion-token caps remain disabled because Venice/XHigh truncation behavior was not paid-tested.

## Voice/import findings — repaired

- Voice instructions name per-turn keys: turn_id, question_text, answer_text, canonical_question_id and turn_role, with correction_of for corrections.
- Setup Q&A is metadata outside behavioral turns. Retrospective permission can be withdrawn mid-session.
- Final-review corrections are exported as ordered behavioral correction turns; pure confirmation stays in participant review.
- ChatGPT imports require explicit question/answer keys and preserve/remap correction links.
- Exact canonical wording can recover a route ID without upgrading edited/unverified wording provenance.
- GPT-authored evidence stays in the received source record but is never admitted as Railway evidence until independent Railway admission.
- Export labels source fidelity and evidence authority; collection-mode analysis separates collector-unverified from Railway-admitted evidence and explicitly compares whole pipelines rather than claiming voice/text equivalence.

## Evidence

- Final full participant-service suite: 79/79 PASS before the last reconciliation micro-tests; focused reconciliation suites also pass after the subsequent fixes.
- Final mobile browser smoke: PASS, synthetic provider only, no JavaScript errors.
- Final no-paid-API Codex development probe: GPT-5.6 Sol/XHigh planner chose fresh G23; independent admission approved first pass.
- Cost benchmark v3 is aggregate-only; participant text/identity are absent.
- Legacy deployable interviewer remains unchanged: current strict count 7,933 characters, so PR 42 compact text cannot be added without removing other existing rules. Core accuracy protections are present in the new voice collector and Railway prompts.

## Assurance boundary

The second Opus review explicitly found no blocker to deploying while live inference stays disabled. The current deployment step is therefore a dark/reversible cost-guard deployment only. Re-enabling production inference still requires resolving the Venice 402/credit condition and exercising the live provider path under the owner's spending authorization; no paid call is performed here.
