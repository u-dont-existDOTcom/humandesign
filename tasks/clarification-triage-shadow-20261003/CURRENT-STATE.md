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
- Current hardened lean contract: **112.023 s** total (GapTriage 72.012 s + GapAdmission 40.011 s), with complete 81-turn source, xhigh reasoning and no source truncation.
- Legacy successful initial Plan+Admission: ~488.155 s. Lean shadow is about **4.36x faster**.
- The lean shadow's selected route was **M11**, matching the actual legacy review's first canonical clarification route on this owner case.
- Focused lean shadow tests: **14 passed**.

## Approval / streaming finding

Current official OpenAI app-permission documentation confirms that eligible connected apps/accounts may offer **Always allow** or **Allow low-risk actions**, but current GPT Actions help does not restate the old consequential-flag guarantee. Historical Actions documentation said `x-openai-isConsequential: false` exposes **Always allow**. The experimental schema therefore marks **only the read-only review-status GET** explicitly nonconsequential for a private UI probe. All participant-data or state-changing POSTs remain consequential.

Do not add per-answer Custom GPT writes yet. First exploit the ~4.36x triage speedup and clarification batching. If persistent permission is verified privately, a separate append-only encrypted checkpoint endpoint becomes a reasonable Custom-GPT experiment; the plugin remains the better long-term place for batched/incremental ingestion.

## Open quality gate

Before promotion:
1. build synthetic/development replay cases for answered gaps, true unresolved gaps, unsupported premises, conditions/corrections, dependent follow-ups and review-ready records;
2. compare legacy and shadow route/question decisions under blind adjudication;
3. require zero admitted redundant questions and no material loss of useful clarifications;
4. only then move evidence synthesis off the critical path or wire triage into live behavior.

Remote experiment head verified: `e40a685800396adbb3dbb85ceb323f1107f40d04`. Do not merge this experiment merely from the owner-case latency result.
