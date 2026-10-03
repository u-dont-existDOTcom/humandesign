# Multi-route blind adjudication v3 — 2026-10-03

## Boundary

Development-only synthetic cases J1–J5. No participant source was disclosed.

The evaluator packet contained:
- the information-based clarification rule;
- only the relevant frozen route wording/interpretation limits;
- synthetic case source;
- route IDs in scope.

The evaluator packet withheld:
- shadow or legacy outputs;
- benchmark timings;
- producer rationale;
- prior adjudicator conclusions;
- repair history.

## First adjudicator

Fresh Claude Sonnet, high effort.

- J1: `review_ready` — high.
- J2: clarify `M09` canonical — high.
- J3: clarify `M05`, then `G20`, both canonical — high.
- J4: clarify `M05` canonical — high.
- J5: clarify `PREFER-EXCHANGE` via missing-piece follow-up — medium.

These labels were frozen before the first J1–J5 shadow replay.

## Second adjudicator

Fresh Claude Opus, xhigh effort, given the same original blind J1–J5 packet and no implementation outputs.

- J1: `review_ready` — high.
- J2: clarify `M09` canonical — high.
- J3: clarify `M05` canonical; leave `G20` unknown because it is missing coverage only — medium.
- J4: clarify `M05` canonical — medium-high.
- J5: clarify `PREFER-EXCHANGE` via missing-piece follow-up — medium.

A separate earlier fresh Opus adjudication of J2/J3, also blind to implementation output, had judged J2 `review_ready` and J3 `M05` only. Therefore J2 is evaluator-unstable even within the same model family/context reset.

## Frozen scoring disposition

Do not tune the model to force one side of a genuine adjudication dispute.

- J1, J4, J5: scored normally; evaluator agreement is adequate for this bounded experiment.
- J2: unscored/disputed. The question is whether a generic familiarity/complexity preference leaves enough material information gain for the full M09 tradeoff. Fresh adjudications disagree.
- J3: require `M05`; permit `G20` either present or absent. M05 is stable consensus. G20 is disputed because one evaluator treated the untouched resource-purpose route as missing coverage only.

This disposition was chosen from evaluator disagreement, not to excuse a particular shadow output.

## Interpretation

The v3 packet is useful precisely because it reveals the boundary between “material unresolved distinction” and “missing coverage.” That boundary should stay explicit and auditable rather than being converted into hidden prompt tuning.

Promotion still requires broader records and repeated stability; this adjudication only defines which J1–J5 outcomes are fair hard targets.
