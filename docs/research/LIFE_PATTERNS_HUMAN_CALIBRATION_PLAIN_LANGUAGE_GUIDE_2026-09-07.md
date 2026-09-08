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

> Given only this specific episode or repeated-series report and this neutral observable definition, what does the evidence actually support?

Depending on the frozen schema, that may mean deciding that the observable is supported/observed, insufficiently evidenced, not applicable, or assigning the appropriate permitted behavioral value and recording exact supporting/counterevidence.

The purpose is to measure whether a competent blind human applies the neutral coding system similarly to the automated coder, and to expose ambiguous or unreliable codes.

## The auditor should not edit JSON directly

The verified private handoff is a machine interchange artifact, not an appropriate default user interface. The substantive task is human judgment; JSON/JSONL exists so the result can be deterministically validated and frozen.

Before an auditor is asked to complete the first pass, provide a theory-neutral local/offline annotation interface that renders the same frozen evidence and rules in ordinary form controls and exports the unchanged response contract. The interface must not alter packet bytes, codebook semantics, selected units, allowed values, or blinding. Requirements are recorded in `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_REQUIREMENTS_2026-09-08.md`.

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

## How to interpret statements such as “I always X”

A behavioral self-report such as **“I always X” is evidence**. The system should not throw it away.

What it establishes is narrower than the literal wording may suggest:

- it is direct evidence that the narrator **reports/perceives X as recurrent**;
- it is not, by itself, a bounded **episode-level observation**;
- it does not prove the literal universal claim that X happened on every possible opportunity;
- it does not establish a numerical occurrence count unless multiple opportunities/instances are also supported;
- when the source provides a sufficiently bounded repeated-series report with exact participant text and recurrence information, the separate **series evidence** layer can code that recurrence.

This is why the codebook separates narrator claims, episodes, and repeated-series evidence. The rule “a global claim is not behavioral proof” should be read as **“do not silently convert one generalized sentence into one or more invented concrete episodes or a proven universal frequency.”** It does not mean the sentence is evidentially worthless.

There is also an important difference between:

- **behavioral recurrence:** “I always checked the door before leaving”; and
- **trait interpretation:** “I am always cautious.”

The first directly reports a recurring behavior. The second mostly reports the narrator's interpretation/label and needs behavioral content before it can support a behavioral code.

## What the human receives

The exported private bundle contains the preselected calibration packets, the embedded frozen instructions/manual, response schemas, blank response templates, and an unfilled independence/exposure attestation.

The human should receive the bundle privately because the packets may contain participant text. Private participant evidence must not be committed to the public repository.

## What the interface must ultimately export

The human-facing UI should produce completed working copies equivalent to:

- `episode_responses.blank.jsonl` -> completed episode-response JSONL;
- `series_responses.blank.jsonl` -> completed series-response JSONL;
- `auditor_attestation.blank.json` -> completed attestation.

The auditor should not need to understand or hand-edit those formats.

For each assigned unit, the human:

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
