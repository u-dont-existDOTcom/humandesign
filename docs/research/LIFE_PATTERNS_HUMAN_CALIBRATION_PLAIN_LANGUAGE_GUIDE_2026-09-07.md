# Life Patterns Human Calibration — Plain-Language Guide

Status: explanatory guide for the existing development-only blind human calibration workflow. This guide does not alter the frozen coding manual, schemas, selected units, prompts, or scientific gates.

## The most important distinction

**The independent human is not auditing the scoring of the owner's Survey-v2 answers.**

There are two separate measurement systems in this repository:

1. **Survey-v2 / natal reverse matching** — a frozen questionnaire/classifier/scoring system intended to test whether human narrative can identify or rank birth-derived Human Design states.
2. **Life Patterns neutral coding** — a theory-blind behavioral measurement system that converts autobiographical episodes into neutral behavioral observables before any Human Design target-model comparison.

The current `44 episode units + 22 series units` human-calibration bundle belongs to **#2, Life Patterns neutral coding**.

## What the independent human is actually checking

The automated Life Patterns coder reads selected autobiographical evidence and applies the frozen neutral behavioral codebook. The independent human is given the **same selected evidence and the same neutral coding rules, but not the automated answers**.

They independently answer questions of the form:

> Given only this specific episode and this neutral observable definition, what does the evidence actually support?

Depending on the frozen schema, that may mean deciding that the observable is supported/observed, insufficiently evidenced, not applicable, or assigning the appropriate permitted behavioral value and recording exact supporting/counterevidence.

The purpose is to measure whether a competent blind human applies the neutral coding system similarly to the automated coder, and to expose ambiguous or unreliable codes.

## What they are NOT doing

They are not:

- deciding whether Human Design is true;
- seeing the owner's natal chart or birth data;
- judging whether a Survey-v2 answer matches the owner's chart;
- checking the Survey-v2 ranking or scoring formula;
- deciding whether the automated coder is "correct because it agrees with HD";
- interpreting personality, hidden motives, morality, diagnosis, or spiritual meaning;
- rewriting the participant's stories;
- changing the frozen codebook during the first pass.

## Why an independent human is needed

Three or more isolated automated coding passes can tell us whether the automated coder is self-consistent. They cannot by themselves establish that the coding procedure corresponds to how an independent human would apply the measurement definitions.

The human calibration therefore supplies a different error check:

**frozen autobiographical evidence -> frozen neutral rules -> independent human labels**

versus

**the same frozen autobiographical evidence -> the same frozen neutral rules -> automated consensus labels**

Agreement and disagreement are then measured. Neither side is automatically treated as ground truth. Disagreement can reveal unclear definitions, insufficient evidence, unstable automated coding, or a human mistake that needs adjudication after the first pass is frozen.

## What the human receives

The exported private bundle contains the preselected calibration packets, the embedded frozen instructions/manual, response schemas, blank response templates, and an unfilled independence/exposure attestation.

The human should receive the bundle privately because the packets may contain participant text. Private participant evidence must not be committed to the public repository.

## What the human fills in

The human works from copies of the blank templates and completes every assigned unit exactly once:

- `episode_responses.blank.jsonl` -> completed episode-response JSONL;
- `series_responses.blank.jsonl` -> completed series-response JSONL;
- `auditor_attestation.blank.json` -> completed attestation.

Exact filenames used for a returned completed bundle may be chosen operationally, but the original blank files and frozen packets should be preserved unchanged.

For each assigned row, the human:

1. keeps the supplied task/evidence/observable identities unchanged;
2. reads only the supplied source evidence and frozen coding instructions;
3. selects only values permitted by the supplied schema/manual;
4. records exact source support and counterevidence where required;
5. uses insufficient/not-applicable states when the rules require them rather than guessing;
6. completes all selected units;
7. freezes the first-pass output before seeing automated labels or consensus.

## Blinding requirement

Before and during the first pass, the human must not have access to:

- automated coding outputs for these units;
- automated consensus;
- expected answers;
- Human Design/chart/birth information for the task;
- target-model mappings, scores, rankings or reveal results.

If they have already seen relevant project-specific target information, that exposure must be disclosed in the attestation so eligibility can be assessed rather than silently ignored.

## What happens after they finish

The coordinator validates that the response files:

- cover exactly the preselected units;
- contain no duplicates or missing units;
- obey the frozen schemas and codebook/procedure bindings;
- preserve the first-pass output rather than rewriting it to match the automated coder.

Only after the independent first pass is frozen may the human labels be compared with automated consensus.

## Relationship to Survey-v2

Survey-v2 has its own separate classifier and scoring reliability problem. A human reviewer could be used in a future Survey-v2 measurement study, but that is **not what this Life Patterns calibration bundle is for**.

If the participant whose autobiographical Life Patterns episodes are being coded is also the owner who previously answered Survey-v2, that does not merge the two pipelines. The Life Patterns human still codes only the neutral behavioral evidence under the Life Patterns codebook and never audits the Survey-v2 score.
