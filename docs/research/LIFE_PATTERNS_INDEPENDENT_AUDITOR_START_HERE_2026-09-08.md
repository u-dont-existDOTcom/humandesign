# Independent Behavioral Calibration — Auditor Start Here

Status: theory-neutral operating guide for the existing frozen development calibration bundle. This guide does not change the codebook, selected units, packets, schemas, prompts, or scientific gates.

## What you are doing

You are independently applying a frozen behavioral coding manual to a small set of autobiographical evidence. You are not evaluating a personality theory, diagnosing the narrator, judging the narrator, inferring hidden motives, or trying to agree with another coder.

Your first pass must be completed without seeing any automated coder output, consensus, expected answer, external-model mapping, participant birth/chart material, or target-model result.

Do not use ChatGPT, another LLM, an automated coder, or an external annotation assistant to complete this first pass.

## What is in the private ZIP

The ZIP contains:

- `README.md` — controlling bundle instructions;
- 6 episode packets under `packets/episode/`;
- 2 repeated-series packets under `packets/series/`;
- `episode_responses.blank.jsonl` — 44 preselected episode-observable rows;
- `series_responses.blank.jsonl` — 22 preselected series-observable rows;
- response schemas for those two files;
- `auditor_attestation.blank.json` — the independence/exposure declaration;
- a public-safe receipt that binds the frozen package.

The packet files and schemas are read-only source material. Do not edit them.

## Before coding

1. Keep the whole bundle private.
2. Read `README.md` first.
3. Confirm that you have not seen automated answers or external target-model outputs for these cases.
4. If you already have relevant exposure, do not hide it. Record it honestly in the attestation so the coordinator can decide whether your pass is eligible.
5. Make working copies of the two blank JSONL files and the blank attestation. Preserve the originals unchanged.

## How to code each assigned row

Each row already contains the task ID, evidence ID, observable ID, corpus binding, and fixed schema constants. Preserve those values exactly.

Find the matching task and observable in the supplied packet. Read the exact source segments and the embedded frozen manual. Then code only what the evidence supports.

The evidence state is one of:

- `observed` — the evidence meets the observable's minimum requirements;
- `insufficient` — the relevant situation may be present but the supplied evidence is not enough to code a substantive value;
- `not_applicable` — the observable's prerequisite circumstance is affirmatively absent from the bounded evidence.

Do not force an `observed` value merely because a behavior seems plausible.

### If the state is `observed`

For episode rows, an observed response must include:

- one or more permitted `coded_values`;
- a `value_relation` (`single`, `ordered_sequence`, or `unordered_multiple` as appropriate);
- at least one exact `supporting_source_segment_id` from the assigned task.

For repeated-series rows, an observed response additionally requires a defensible `minimum_reported_occurrences` of at least 2.

If the selected value is a frozen non-action value, the full four-part non-action gate must be established: awareness, opportunity, reasonable feasibility, and established non-action. If any part is missing, do not code substantive non-action.

If the value is the frozen Other-Specified option, provide a concrete `other_specified_description`.

### If the state is `insufficient` or `not_applicable`

Do not supply substantive coded values, a value relation, a recurrence count, a non-action assertion, or an Other-Specified description. Use missingness flags and notes where they help explain why the evidence cannot be coded.

## Important evidence rules

- Exact source segments are primary evidence. Transfer summaries are orientation only.
- Preserve counterevidence and exceptions.
- Sequence is not the same as mixedness: if behavior changes within one episode, preserve the ordered sequence.
- Temporal order does not prove causation. Record influence only when the narrator explicitly states it.
- A global narrator claim such as “I always...” is not by itself behavioral proof.
- Silence or non-mention is normally insufficient evidence, not proof of non-action.
- Do not optimize for agreement with what you imagine another coder would choose.

## Questions and ambiguity

If a case is genuinely ambiguous under the frozen manual, use the permitted insufficient/missingness path or record a concise note. Do not ask the participant/project owner how a particular case “should” be coded during the first pass. Substantive clarifications belong after the first pass is frozen.

## Completion requirement

Complete every assigned unit exactly once:

- 44 episode rows;
- 22 repeated-series rows;
- total: 66 rows.

Then complete `auditor_attestation.blank.json` honestly, including the actual completion time in UTC.

Return the completed working copies and completed attestation to the coordinator. Preserve your first-pass files unchanged after submission. Do not view automated labels or discuss disagreements until the coordinator confirms that your first pass has been frozen.
