# Shadow clarification triage experiment — current state

- Task: `experiment-gap-triage-shadow-20261003`
- Branch: `experiment-gap-triage-shadow-20261003`
- Parent baseline: `2053e58`
- Status: development-only implementation is pushed and remotely verified; semantic benchmark and privacy-safe owner-case comparison complete; replay-set quality validation remains open
- Assurance lane: experiment only; privacy/no-live-change hard gates
- Authority: owner request plus `tasks/survey-owner-feedback-20261001/INDEPENDENT-REVIEW-LATENCY-REDESIGN-20261003.md`
- Completion command: `PYTHONPATH=apps/life-patterns-participant python -m pytest apps/life-patterns-participant/tests -q`

## Required outcome

Test whether clarification selection can be separated from full evidence synthesis without reducing reasoning effort or source fidelity. Do not connect this experiment to the live participant engine, review worker, HTTP API, deployment, or Custom GPT bundle until quality is shown non-inferior.

## Current implementation

1. `participant/shadow_triage.py` contains a source-complete GapTriage producer plus independent GapAdmission refuter. The lean producer returns only ranked questions/dependencies; it does not emit evidence, per-turn dispositions, route maps, source citations or defect prose.
2. Triage receives compact route authority; full interpretation/context controls are attached only for selected candidates in independent admission.
3. `scripts/benchmark_shadow_triage.py` runs private replays while persisting only privacy-safe aggregate/route metadata.
4. `tests/test_shadow_triage.py` covers full-source propagation, admission independence, no mutation, route/dependency/gate validation, review-ready/all-rejected outcomes, 81-turn-class input and privacy-safe output.
5. Production remains unchanged by this branch. The branch also contains a separate read-only `getLifePatternsReview` approval probe for testing whether current ChatGPT offers persistent **Always allow** on a nonconsequential status read.

## Semantic evidence

Private owner source is never committed.

- Prototype baseline repeats: ~70.3 s and ~121.4 s.
- Three planted semantic-redundancy variants: ~97.4–149.8 s; each planted equivalent answer suppressed its intended route despite no canonical route ID.
- Earlier hardened verbose contract: ~222.3 s.
- Hardened lean replay: **112.023 s** total (GapTriage 72.012 s + GapAdmission 40.011 s).
- A later semantic run of the final privacy-hardened benchmark contract took **222.314 s** (177.302 s + 45.012 s). Both retained all 81 behavioral source turns and xhigh reasoning.
- Legacy successful initial Plan+Admission: ~488.155 s. The hardened shadow is therefore about **2.20x–4.36x faster** on this owner case, with substantial stochastic/output-contract variance still to measure.
- Both the hardened shadow and the actual legacy review selected **M11** as the first canonical clarification route on this owner case.
- Focused shadow/action tests: **24 passed** after the current approval probe and triage changes.
- Seven targeted synthetic semantic outcomes now cover true unresolved `M11`, semantically redundant `M11`, antecedent-gated `PREFER-EXCHANGE`, missing-antecedent review-ready, correction-resolved review-ready, unsupported `WORK-RECOVERY` premise rejection, and an independently admitted two-question `M05` + `M11` batch. One initial synthetic wording was repaired because it accidentally answered the distinction it was supposed to leave unresolved.

## Approval / streaming finding

Current official OpenAI app-permission documentation confirms that eligible connected apps/accounts may offer **Always allow** or **Allow low-risk actions**, but current GPT Actions help does not restate the old consequential-flag guarantee. Historical Actions documentation said `x-openai-isConsequential: false` exposes **Always allow**. The experimental schema therefore marks **only the read-only review-status GET** explicitly nonconsequential for a private UI probe. All participant-data or state-changing POSTs remain consequential.

Do not add per-answer Custom GPT writes yet. First exploit the measured ~2.20x–4.36x triage speedup and clarification batching. If persistent permission is verified privately, a separate append-only encrypted checkpoint endpoint becomes a reasonable Custom-GPT experiment; the plugin remains the better long-term place for batched/incremental ingestion.

## Open quality gate

Before promotion:
1. add at least one genuinely dependent multi-question case where candidate 2 must wait for candidate 1's answer, plus broader development records rather than route-isolated fixtures;
2. compare legacy and shadow route/question decisions under blind adjudication on that broader development replay set;
3. require zero admitted redundant questions and no material loss of useful clarifications;
4. only then move evidence synthesis off the critical path or wire triage into live behavior.

Remote experiment head verified through the synthetic-quality benchmark commit. Do not merge this experiment merely from the owner-case latency result.
