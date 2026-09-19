# Life Patterns — LLM-Primary, Human-Calibrated Coding Protocol

Status: **owner-approved development protocol** superseding full-corpus dual-human coding as the default Life Patterns development path.

Date: 2026-09-04

Canonical codebook candidate:

- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

The earlier `LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md` remains a valid stricter all-human benchmark route, but it is no longer the required default development workflow.

## Why this protocol changed

The reconciled codebook is deliberately detailed and contains many prerequisite, missingness, sequence, and context distinctions. Requiring two humans to code the entire development corpus creates a realistic risk of attention fatigue, inconsistent application, and unsustainable labor. Exact human-human identity is not the scientific target; disagreement is itself evidence about codebook ambiguity.

Recent annotation-methods work also supports evaluating whether high-capability LLM annotators can substitute for humans after calibration on a smaller human-labeled subset rather than assuming humans must label the full corpus. This project therefore adopts an **LLM-primary / human-calibrated** development design.

This does not claim that an LLM is automatically correct because it is internally consistent. A consistently wrong automated coder remains wrong. Human auditing, disagreement analysis, theory blindness, frozen provenance, and later validation review remain required safeguards.

## Development roles

### Primary production coder

Use a high-capability target-theory-blind LLM as the primary production coder over the full development corpus.

Requirements:

- exact codebook version frozen;
- exact coding prompt/procedure frozen;
- no Human Design/AstroHD/astrology model mappings, birth data, chart outputs, candidate scores, or model-fit information in coding context;
- exact model/product identity and version recorded when available;
- exact output preserved;
- no access to prior coding pass outputs during an independent pass;
- no hidden repair using target-model information.

### Replicated LLM passes

For each development corpus version, run at least **three independent blinded coding passes** when operationally feasible.

They may use the same high-capability model in isolated fresh contexts; a second model family may additionally be used as a robustness audit, but is not required for the first development pass.

The passes are not treated as three independent human judges. They measure stochastic/model stability and expose ambiguous cases.

### Consensus rule

For categorical outputs:

- unanimous same value: `llm_consensus = unanimous`;
- majority same value with one dissent: `llm_consensus = majority`, preserving all raw outputs;
- no stable majority / incompatible applicability judgments: `llm_consensus = unresolved` and route to audit/adjudication rather than forcing a label.

For multi-step sequences, consensus must preserve ordering; set agreement alone is insufficient.

For prerequisite judgments and IE/NA, disagreement is never silently collapsed.

### Human calibration auditor

A theory-blind human auditor reviews a **strategically sampled subset**, not the whole corpus.

The auditor must not receive target-model information or LLM answers before producing the auditor's own first-pass coding.

The human sample should overrepresent:

- high-impact confusion pairs;
- non-action cases;
- IE vs NA cases;
- multi-step sequences;
- LLM pass disagreements;
- sparse observables where examples exist;
- a random slice of apparently easy unanimous LLM cases, so auditing does not look only at failures.

The auditor's role is to detect systematic LLM failure and codebook ambiguity, not to serve as an infallible gold standard.

## Human burden

The development workflow does **not** require two humans to code 60–100 episodes each before LLM coding can proceed.

A practical first pass may use one qualified blind human auditor on a smaller, information-rich subset. Sample size is chosen for development signal and feasibility, not to pretend to satisfy a formal LLM-replacement statistical test.

If later publication-grade evidence is needed to justify wholesale replacement of human annotators, the project may add a larger multi-human calibration subset and a formal alternative-annotator/equivalence analysis. That is a later validation decision, not a prerequisite for current development.

## Theory-exposed owner coding

A theory-exposed project owner may code episodes only as a **separate sensitivity analysis** after the blind LLM and human-auditor outputs for those episodes are frozen.

Owner coding:

- must not enter the blind calibration benchmark;
- must not be used to repair the codebook before blind outputs are frozen;
- may be compared afterward to quantify whether target-theory exposure materially shifts neutral coding.

## Human-auditor comparison

Report, at minimum:

- applicability agreement by observable;
- substantive-value agreement;
- IE/NA agreement;
- non-action prerequisite agreement;
- sequence agreement;
- confusion matrix where sample size allows;
- rate and nature of LLM unanimous cases rejected by the human auditor;
- rate and nature of LLM-disagreement cases where the human auditor selects one side versus a third interpretation;
- `other specified` rate;
- qualitative disagreement taxonomy.

Do not interpret the human as automatically correct. Every disagreement is inspected against the frozen operational definition and evidence span.

## Stability outputs for replicated LLM coding

Report separately:

- exact-pass agreement;
- per-observable agreement;
- applicability/prerequisite stability;
- IE/NA stability;
- sequence stability;
- context-modifier stability;
- unresolved rate;
- model-family disagreement if a second family is used;
- sensitivity to prompt version and model version, if either changes.

A high self-agreement rate does not establish construct validity.

## Development adjudication

Adjudication occurs only after raw independent outputs are frozen.

Order:

1. freeze every independent LLM pass;
2. freeze the blind human-auditor pass where applicable;
3. compute disagreement/stability reports;
4. adjudicate using the frozen codebook and source evidence only;
5. preserve original outputs alongside adjudicated development labels;
6. route recurrent ambiguity into a theory-blind v2 codebook revision.

No target-model result may be visible during adjudication or revision.

## Promotion beyond development

The project does **not** yet declare one universal route from this development protocol to final validation-candidate status.

Before confirmatory model scoring, choose and freeze one of these validation routes:

### Route A — conventional human benchmark

Use sufficient independent theory-blind human coding to establish the required external reliability evidence.

### Route B — statistically justified automated-annotator substitution

Use a prespecified human calibration design large enough to statistically test whether the frozen LLM annotator is an acceptable substitute for human annotators, with the exact method and decision criterion frozen before target-model results.

### Route C — explicit automated measurement instrument

Treat the frozen LLM coding pipeline itself as the measurement instrument, report test-retest/model stability plus independent human spot-audit evidence, and make no claim that its labels are a human gold standard. This route requires an explicit methods justification and must be preregistered before confirmatory model scoring.

Whichever route is chosen, model-fit results cannot be used to choose the route retrospectively.

## Current development assignment

- one owner-designated theory-blind human: `BLIND-HUMAN-AUDITOR-A`;
- theory-exposed owner: sensitivity coder only, not blind benchmark;
- primary automated coder: not yet pinned in this document;
- no second human is required to start the LLM-primary development pilot.

Human identities are kept outside the public research repository; repository receipts use pseudonymous coder IDs.

## Authorization boundary

This protocol authorizes methodology preparation only. It does not itself authorize:

- contacting the designated human auditor;
- spending money;
- exposing target-model information;
- running confirmatory target-model scoring;
- validation-candidate promotion;
- merging/deploying PR #24.
