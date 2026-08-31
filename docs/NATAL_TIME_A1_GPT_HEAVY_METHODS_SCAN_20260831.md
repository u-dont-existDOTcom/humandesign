# A1/GPT-heavy semantic-authority, role, and custody methods scan

Status: bounded checkpoint-13 methods scan; architecture evidence only

This scan began only after commit `5091d16fd22e78ed2147b4de839bbd8e99e00e0c` froze the
source-free conception. It examines the generic problems of human semantic authorship under heavy
AI assistance, contribution attribution, qualitative reflexivity, source fidelity, automation
bias, isolated automated judgment, provenance, dual roles, and post-selection revision. It does
not search for constructs, instruments, target-domain mappings, human-facing language, or a real
eligibility outcome.

## Decision-level synthesis

The mature reusable pieces are structural rather than substantive:

- identify human and nonhuman actor roles and disclose exactly what each did;
- preserve original recordings or bytes, derivatives, uncertainty, and review history;
- represent entities, activities, agents, derivations, access, generation, and invalidation as
  separately identifiable provenance events;
- define and differentiate human-AI roles, knowledge limits, oversight, and test boundaries;
- require every AI-produced semantic derivative to remain visibly non-authoritative until the
  human source accepts the exact derivative; and
- commit independent judgments before reconciliation so later discussion cannot rewrite the
  originals.

No source validates the complete proposed workflow. Evidence about LLM judging and annotation is
task-specific and mixed. In unrelated tasks, LLM judges have shown useful agreement while also
showing position, verbosity, self-enhancement, shared-model, and reasoning biases. Text-annotation
studies range from strong performance against crowd workers to substantial, unpredictable
task/model variation. Therefore two GPT runs are a custody and single-run-risk control, not proof
of validity or independent models.

Human approval is also not a magic validity step. Automation-bias evidence shows that warnings or
responsibility instructions can increase checking without necessarily improving objective
decisions. The architecture must preserve source support and force explicit semantic authority;
it cannot infer fidelity merely from a checked box.

## Method-family decisions

Each family has exactly one checkpoint-13 disposition. These choices authorize only metadata and
custody architecture; they do not select a future prompt, model, threshold, evidence standard,
reconciliation rule, or human procedure.

| Method family | Disposition | Bounded use or reason |
|---|---|---|
| Contributor-role taxonomy | `ADAPT` | Keep conceptualization, processing, validation, writing, and supervision contributions distinct; add context/run identity needed here. |
| AI-use disclosure and human responsibility | `ADAPT` | Record the tool purpose and retain human responsibility without mislabeling GPT as the human semantic source. |
| Qualitative reporting and reflexivity | `ADAPT` | Record dual roles, derivation, recording, validation, and limitations; reporting guidance is not a validity guarantee. |
| Original recording and transcript preservation | `REUSE_DIRECTLY` | Preserve the original, audit the transcript, document changes, and never let a derivative replace the source. |
| Source offsets, timestamps, and uncertainty | `ADAPT` | Bind extracted units to exact locations and preserve uncertainty; no recording format is selected. |
| Entity/activity/agent provenance graph | `REUSE_DIRECTLY` | Reuse typed identities, derivation, generation, usage, event order, and consistency constraints. |
| Cryptographic content binding and version identity | `ADAPT` | Use content hashes and immutable version identities; do not claim that integrity proves semantic truth. |
| Documented human-AI roles and oversight | `ADAPT` | Define role permissions, knowledge limits, oversight, test context, and lifecycle review. |
| Non-leading cognitive facilitation | `ADAPT` | Preserve nondirective, source-bound probing as a future design family; no human-facing wording or procedure is selected. |
| Source-grounded factuality diagnostics | `ADAPT` | Atomic/source-support and QA/entailment checks may later diagnose support, but cannot replace human semantic fidelity. |
| Warning-only or responsibility-only automation-bias control | `REJECT_INCOMPATIBLE` | Empirical evidence does not support treating warnings or responsibility instructions as sufficient. |
| Source-linked human acceptance receipts | `COMPOSE` | Combine immutable source lineage, explicit derivative identity, and a typed human decision without treating opaque summary approval as evidence. |
| Multiple sealed initial GPT runs | `ADAPT` | Preserve separately initialized, separately committed judgments and later reconciliation; do not claim independent models. |
| Multi-model jury as a required configuration | `UNRESOLVED` | Diverse-model panels can reduce intra-model bias in studied evaluation tasks, but no configuration is selected or validated here. |
| Reconciliation that overwrites initial judgments | `REJECT_INCOMPATIBLE` | Consensus cannot erase sealed first judgments or disagreement. |
| Raw-origin and clean-conception two-freeze gate | `COMPOSE` | Combine source preservation, non-authoritative derivatives, human decisions, and protected-access gating. |
| Exact versus near-duplicate handling | `COMPOSE` | Exact matches may be flagged mechanically without deletion; possible semantic equivalence remains a non-binding flag. |
| Post-selection revision prevention | `ADAPT` | Freeze the independent package before later results and label any later work as a new, non-clean branch. |
| Owner/author dual-role conflict controls | `COMPOSE` | Separate event roles, preserve adjudication authority, prohibit owner override, and disclose the single-author limit. |

## Evidence by problem

### Attribution and human responsibility

The current CRediT resource describes fourteen standardized contributor roles and supports granular
contribution reporting. Current ICMJE guidance requires disclosure of which AI tool was used and
for what purpose, does not treat AI as an author, and retains human responsibility for accuracy,
integrity, originality, attribution, and confidentiality. These sources support explicit actor and
activity metadata, not a claim that a disclosure alone proves clean human origin.

### Qualitative reporting, source preservation, and reflexivity

The COREQ abstract identifies research-team/reflexivity, recording, theme derivation, respondent
validation, and supporting quotations as reporting domains. The SRQR abstract supports transparent
reporting through twenty-one standards. Neither complete article was lawfully available through
the bounded full-text route, so only abstract-level claims are used.

Oral History Association guidance is more directly operational for custody: preserve original
recordings, review first-draft transcripts for accuracy, disclose differences from the original,
record processing steps, and give the human source an opportunity to review. Census cognitive-
interviewing guidance supports think-aloud work and nondirective probes, while emphasizing that
technique depends on the testing objective. This makes neutral facilitation a future method-design
problem, not executable language for this checkpoint.

### Provenance, integrity, and role governance

W3C PROV supplies the most directly reusable conceptual structure: entities, activities, agents,
generation, usage, attribution, association, derivation, event ordering, typing, and consistency.
C2PA separately demonstrates content-bound manifests and versioned claims, while explicitly
distinguishing verifiable provenance from a value judgment about truth. NIST AI RMF requires clear
human-AI roles, knowledge limits, oversight, lifecycle documentation, scientific-integrity and
construct-validation considerations, context-matched testing, and preserved limitations. These
sources justify closed metadata, hashes, event ordering, and explicit role access, but not the
scientific validity of the eventual process.

### GPT judging, annotation, and fidelity diagnostics

Zheng et al. report useful LLM-judge agreement in their evaluated conversational preference tasks
and document position, verbosity, self-enhancement, and reasoning biases. Verga et al. report that
a panel of diverse smaller models outperformed one large judge across their studied settings and
reduced intra-model bias, but this does not establish a required configuration for eligibility
adjudication. Gilardi et al. found strong ChatGPT performance on several political text-annotation
tasks; a later PNAS Nexus study found significant and unpredictable task/model variation and urged
caution. The only defensible transfer is task-specific testing and precise run/model provenance.

FActScore and QAFactEval show that source-support can be decomposed into atomic or question-based
checks. They are diagnostic precedents for source linkage, not validated measures of whether a
human considers a paraphrase faithful to intended meaning.

### Automation bias and post-selection change

The complete open text of Kupfer et al. was read and method-audited through AskRigor. In a
simulated personnel task with ninety-three mainly student participants, increased verification
correlated with better objective decisions. A system-error warning increased verification but did
not improve objective decision quality; a responsibility instruction did not improve either.
The study cannot validate this workflow and has limited population/task transportability.

Kerr defines HARKing as presenting a result-informed post hoc hypothesis as if it were a priori.
The direct architecture implication is chronological truth: preserve pre-result versions and label
later revisions rather than rewriting history. It does not turn an exploratory later revision
into misconduct merely by existing; the failure is false representation of chronology.

## AskRigor protocol and applicability

The canonical Universal protocol was verified as version 20.5.15, revision 2026-08-24, SHA-256
`69c5186862ade61d6a97dc842b8c027324c7e2f3fd7147064a360049e0d25172`.
The Human Research Protocol was verified as version 20.5.23, revision 2026-08-24, SHA-256
`bf2adc1c4daea8241c47b2a111d4a19e6bf7427a6401ecf1b3ba75a58e046299`.
The scan is `DEVELOPMENT_DISCOVERY`, not validation or confirmation. Forum Signal is
`NOT_TRIGGERED`: this methods-architecture decision does not depend on first-person community
outcomes, and community reports cannot validate the workflow. The approved state is
`PREVIOUSLY_APPROVED` under the owner A1 ruling and Pro checkpoint-13 contract.

AskRigor full-text audit receipt for Kupfer et al.:

- source DOI: `10.3389/fpsyg.2023.1118723`;
- PMCID: `PMC10113449`;
- source-content SHA-256:
  `cce91b297b737cc1fc54bd1d310d12dd51457b09eb08c5a5b6085196a43f598e`;
- 89 of 89 source segments exhausted with synthesis lock passing; and
- validated study-method-audit SHA-256:
  `83e8a1c350ccbf6c1b76ac7ddf7c1ffcfca598445944109b7a7555e4c0d8ed56`.

## Limitations and assurance

- Evidence is drawn from adjacent tasks and standards, not this exact eligibility or authorship
  workflow.
- One human source cannot support cross-author convergence or robustness.
- Separate GPT runs can share training, model, prompt-family, provider, and systematic biases.
- Hashes prove byte identity, not truth, completeness, semantic fidelity, or absence of off-record
  exposure.
- Human acceptance can still be influenced by AI framing or owner incentives.
- Neutral facilitation, evidence packets, prompts, thresholds, model identity, and reconciliation
  rules remain unselected and unimplemented.

Operational alignment is `PASS` for the bounded scan. Scientific adequacy is `WARN`: the evidence
supports architecture and threat controls only. Release adequacy is `NOT_APPLICABLE`, release
permission is false, and no human process is ready to run.

## Core sources

- CRediT, current contributor-role resource: https://credit.niso.org/
- ICMJE, current AI recommendations: https://www.icmje.org/recommendations/browse/artificial-intelligence/
- Tong et al., COREQ: https://doi.org/10.1093/intqhc/mzm042
- O'Brien et al., SRQR: https://doi.org/10.1097/ACM.0000000000000388
- Oral History Association archive practices: https://oralhistory.org/archives-principles-and-best-practices-complete-manual/
- U.S. Census questionnaire testing methods: https://www.census.gov/about/policies/quality/standards/appendixa2.html
- W3C PROV constraints: https://www.w3.org/TR/prov-constraints/
- C2PA specifications: https://spec.c2pa.org/
- NIST AI RMF Core: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST Generative AI Profile: https://doi.org/10.6028/NIST.AI.600-1
- Zheng et al., LLM-as-a-judge: https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf
- Verga et al., panel of LLM evaluators: https://arxiv.org/abs/2404.18796
- Gilardi et al., text annotation: https://doi.org/10.1073/pnas.2305016120
- Reiss, chatbot annotation variability: https://doi.org/10.1093/pnasnexus/pgaf069
- Min et al., FActScore: https://aclanthology.org/2023.emnlp-main.741/
- Fabbri et al., QAFactEval: https://aclanthology.org/2022.naacl-main.187/
- Kupfer et al., automation bias: https://doi.org/10.3389/fpsyg.2023.1118723
- Kerr, HARKing: https://doi.org/10.1207/s15327957pspr0203_4

