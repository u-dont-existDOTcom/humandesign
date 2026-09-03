# Life Patterns Neutral Measurement Bridge — v1 Design Specification

Status: design/specification only. No production bridge, model scoring, birth-data use, participant recruitment, merge, or deployment authorization.

Independent pre-scan conception:

- `state/LIFE-PATTERNS-MEASUREMENT-BRIDGE-INDEPENDENT-CONCEPTION-2026-09-03.md`

## Existing-work scan and explicit build decision

The bridge is a measurement instrument, not a serialization convenience. Existing psychometrics, qualitative coding, ontology engineering, within-person measurement, annotation tooling, and selective-classification work solve major parts of the problem. v1 therefore composes those foundations and invents only the project-specific theory-blind bridge boundary.

### 1. Construct validity — reuse/adapt

Use the modern unified validity framework represented by the *Standards for Educational and Psychological Testing* and Messick's validity work.

Validity belongs to the **interpretation/use of coded observables**, not to an observable merely because coders agree. For every proposed neutral observable, maintain a validity argument with evidence relevant to:

- content/construct representation;
- response/coding process;
- internal structure where a multi-item or aggregated construct exists;
- relations with external variables or independently measured constructs where available;
- generalizability/invariance across relevant contexts, modes, languages, and populations;
- consequences of using the coded value in model comparison.

References:

- AERA, APA & NCME, *Standards for Educational and Psychological Testing* (2014): https://www.aera.net/publications/books/standards-for-educational-psychological-testing-2014-edition
- Messick (1995), DOI `10.1037/0003-066X.50.9.741`
- Downing (2003), DOI `10.1046/j.1365-2923.2003.01594.x`

**Decision:** do not call coder agreement "validation." Reliability is one component of a broader observable-by-observable validity program.

### 2. Ontology engineering — reuse/adapt before invention

Do not invent all behavioral concepts under project-local names.

Existing sources to inspect for every candidate observable:

- **Human Behaviour Ontology (HBO)** — broad behavior entities, explicit literature-driven ontology development, review, inter-rater reliability and refinement. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10594800/
- **Behaviour Change Intervention Ontology / Behaviour Change Ontology ecosystem** — methodological precedent for systematic ontology development and annotation workflows: https://www.behaviourchange.net/
- **Cognitive Atlas** — reusable cognitive concepts/tasks and explicit assertions: https://www.cognitiveatlas.org/
- **PhenX Toolkit** — expert-selected standard phenotype/exposure measurement protocols and data dictionaries: https://www.phenxtoolkit.org/
- other established domain measures discovered during construct-specific review.

For each Life Patterns observable, record:

- whether an established term/protocol already solves it;
- external identifier/IRI/DOI when reused;
- exact reason for adapting rather than directly reusing;
- project-local definition only for the unresolved remainder.

Follow the OBO Foundry engineering principles where applicable:

- stable unique identifiers;
- explicit scope;
- textual definitions;
- reuse of established terms;
- documented relations;
- versioned immutable releases;
- do not silently change the meaning of a released identifier.

References:

- OBO Foundry principles: https://obofoundry.org/principles/fp-000-summary.html
- OBO versioning: https://obofoundry.org/principles/fp-004-versioning.html
- Noy & McGuinness, *Ontology Development 101*: https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html

**Decision:** build a small versioned Life Patterns neutral ontology as a **composition and extension layer**, not a replacement for existing ontologies.

### 3. Codebook development — reuse/adapt

For every categorical/ordinal observable, the released codebook must include at minimum:

- stable observable ID;
- display label;
- precise definition;
- unit of analysis: episode, context, life phase, or person-level aggregate;
- allowed values;
- inclusion criteria;
- exclusion criteria;
- positive examples;
- near-miss/negative examples;
- ambiguous examples;
- required source evidence;
- explicit missing / insufficient / not-applicable behavior;
- aggregation rule if an episode-level code contributes to a person-level summary;
- external ontology/protocol cross-references;
- theory-contamination handling;
- version provenance.

MacQueen et al.'s team-based codebook work is the baseline pattern for explicit definitions and systematic team coding. HBO/BCIO's staged ontology-development process provides a stronger domain-specific precedent for literature identification, expert review, annotation and refinement.

References:

- MacQueen et al. (1998), DOI `10.1177/1525822X980100020301`
- Michie et al./HBCP ontology-development series; HBO methods as above.

**Decision:** adapt these workflows. Do not derive the codebook by looking at which wording makes HD/astrology score better.

### 4. Episode/context preservation — reuse/adapt within-person measurement literature

Do not force rich evidence into one global trait value before it is scientifically justified.

Fleeson's density-distribution work demonstrates large, meaningful within-person behavioral variability alongside stable individual differences. Experience Sampling / Ecological Momentary Assessment literature likewise emphasizes temporal/contextual measurement and limitations of global retrospective reports.

References:

- Fleeson (2001), DOI `10.1037/0022-3514.80.6.1011`
- Shiffman, Stone & Hufford (2008), DOI `10.1146/annurev.clinpsy.3.022806.091415`
- Stone et al./EMA methodological review, DOI `10.1146/annurev-clinpsy-080921-083128`

**Decision:** primary coding unit is the episode/context. Person-level summaries are derived views with frozen aggregation rules. Preserve within-person heterogeneity, counterexamples and life-phase changes.

The present retrospective interview is **not** an EMA design. EMA is a future prospective benchmark/validation layer, not a label to apply to current data.

### 5. Inter-rater reliability — reuse with multiple diagnostics

Do not choose a single reliability coefficient by habit.

Development-corpus coding should report:

- raw/percent agreement;
- per-class prevalence;
- confusion matrices;
- Krippendorff's alpha appropriate to the measurement scale when multiple raters/missing data make it suitable;
- Gwet AC1/AC2 or another justified sensitivity statistic when prevalence/marginal distributions make kappa-style chance correction unstable;
- per-observable disagreement/error analysis.

Cohen's kappa has known dependence on marginal/prevalence structure; the literature debates how problematic that is. Therefore no single threshold from one coefficient determines validity or release automatically.

References:

- Krippendorff, *Content Analysis* / alpha methodology
- O'Connor & Joffe (2020), DOI `10.1177/1609406919899220`
- Zec et al. (2017), DOI `10.2174/1874434601711010211`
- Vach (2005), DOI `10.1016/j.jclinepi.2004.02.021`

**Decision:** benchmark against trained independent human coders and report a reliability profile, not a magic kappa cutoff.

### 6. Measurement invariance — reuse/adapt

Do not assume the same code has the same meaning across language, culture, input modality, or time merely because the JSON schema is identical.

Track at minimum:

- interview language;
- typed vs voice input;
- translation/transcription path when applicable;
- relevant cultural/context metadata only when ethically collected and scientifically justified;
- life phase/time context.

Before strong cross-group comparisons, evaluate whether the observable/codebook is functioning equivalently enough for the intended inference.

Reference:

- Putnick & Bornstein (2016), DOI `10.1016/j.dr.2016.06.004`

**Decision:** measurement-invariance evidence is a later validation gate; v1 must at least retain the metadata needed to detect non-invariance.

### 7. LLM annotation — experiment only, never assumed ground truth

Evidence is mixed and task-dependent.

Positive evidence:

- Gilardi, Alizadeh & Kubli (2023), DOI `10.1073/pnas.2305016120`, found ChatGPT highly effective on several well-defined text-annotation tasks relative to crowd workers.

Counterevidence / limitations:

- Felkner, Thompson & May (ACL 2024), DOI `10.18653/v1/2024.acl-long.760`, found GPT-3.5 unacceptable as a substitute for relevant human annotators on a sensitive fairness-benchmark coding task.
- Wang et al. (ACL 2024), DOI `10.18653/v1/2024.acl-long.511`, document evaluator bias.
- Hu et al. (ACL 2024), DOI `10.18653/v1/2024.acl-long.516`, show LLM evaluators can confuse distinct evaluation criteria.

**Decision:** trained-human coding is the reference baseline. A frozen LLM coder may be adopted only observable-by-observable after it is benchmarked on a separate human-coded development set and its error/abstention behavior is acceptable. Model success against HD/astrology is never a criterion for approving the coder.

### 8. Abstention / insufficient evidence — reuse selective-classification principle

A coder that is forced to assign every construct will fabricate measurement certainty.

Selective classification / reject-option literature formalizes the tradeoff between coverage and error when a classifier may abstain on ambiguous cases.

References:

- Chow (1970), DOI `10.1109/TIT.1970.1054406`
- Hendrickx et al. (2021), *Machine Learning with a Reject Option: A Survey*, arXiv `2107.11277`

**Decision:** `insufficient`/abstain is a first-class correct output. For automated coders, report risk/error as a function of retained coverage rather than optimizing raw coverage alone.

### 9. Annotation tooling — reuse mature tools for development; do not build a custom coder UI yet

Mature annotation systems already support codebooks/guidelines, multiple annotators, model suggestions and exports:

- Argilla: https://docs.argilla.io/
- doccano: https://doccano.github.io/doccano/
- Label Studio: https://labelstud.io/

**Decision:** do not spend PR #24 engineering effort on a bespoke annotation platform. Export the development corpus/codebook in a tool-neutral JSONL/CSV-compatible representation and pilot with an existing annotation tool. Pick a concrete tool when the first human-coding pilot is ready; Argilla is a strong candidate because it explicitly separates model suggestions from human responses, while doccano is a mature lightweight open-source alternative.

## Architecture after scan

The two-stage architecture from the independent conception survives, but is tightened.

### Stage A — one shared neutral measurement instrument

`behavioral freeze -> released neutral ontology/codebook -> episode-level coded evidence`

Stage A is shared across candidate model families and is completely blind to:

- birth data;
- chart state;
- candidate dates/times;
- model family output;
- prediction direction;
- rank/fit;
- whether a given code would help or hurt any model.

This is the principal anti-leakage boundary.

### Stage B — thin declarative model adapters

`neutral coded evidence -> predeclared model-specific score inputs`

A model adapter may:

- select declared neutral observable IDs;
- apply a frozen deterministic mapping/aggregation rule;
- apply the manifest's frozen missing/uncertain/rejected policy.

A model adapter may **not**:

- reread raw narrative;
- run a model-aware LLM interpretation;
- invent a missing neutral construct for one participant;
- alter Stage-A codes after seeing model outputs.

If a model requires an unmeasured construct, that is a prospective measurement gap, not permission for post-hoc translation.

## Neutral ontology release object

A released ontology/codebook artifact must be immutable and content-addressed.

Candidate top-level fields:

- `schema_version`;
- `ontology_id`;
- `ontology_version`;
- `ontology_sha256`;
- release status: `development`, `candidate`, `frozen_for_validation`;
- scope statement;
- source/reuse registry;
- observable definitions;
- relations between observables where needed;
- coding-procedure identity;
- aggregation-policy identity;
- theory-contamination policy identity;
- release date;
- provenance/source commit.

Released observable IDs never silently change meaning. Material semantic changes receive a new observable ID or explicitly versioned successor relationship.

## Observable schema

Each neutral observable definition should contain:

- `observable_id`;
- `label`;
- `definition`;
- `unit_of_analysis`;
- `value_type`;
- allowed values/range;
- explicit `insufficient` and `not_applicable` semantics;
- inclusion criteria;
- exclusion criteria;
- evidence requirements;
- positive examples;
- negative/near-miss examples;
- ambiguity examples;
- contextual qualifiers allowed/required;
- participant-review provenance policy;
- theory-language contamination policy;
- external cross-references;
- origin status: `reused`, `adapted`, or `project_specific`;
- validity status;
- reliability status;
- release notes.

## Coded episode record

Primary coded record is episode-level.

Required fields:

- behavioral `freeze_sha256`;
- ontology/codebook SHA-256;
- coding-procedure SHA-256;
- coder ID/type/version/hash;
- episode ID;
- source-turn IDs/hashes;
- observable ID;
- code state: `observed`, `contradicted`, `mixed`, `insufficient`, `not_applicable`;
- coded value when applicable;
- confidence/uncertainty field defined by the coding procedure;
- exact supporting evidence references;
- exact counterevidence references;
- context/domain/life-phase qualifiers;
- input modality/language metadata;
- theory-exposure flag when relevant;
- participant-edited-source provenance;
- timestamp/run receipt.

No free-text model interpretation enters the scoreable field.

## Person-level derived evidence

Any person-level value is a derived artifact over episode codes and must bind a frozen aggregation policy.

The default should preserve distributions/conditional profiles rather than collapse immediately to a binary trait.

Examples of permissible derived forms:

- prevalence across applicable episodes;
- distribution across ordinal states;
- context-conditioned prevalence;
- within-person heterogeneity estimate;
- evidence count and effective coverage;
- temporal/life-phase partitions.

A model that can consume only a binary value must define in its Stage-B adapter how that richer shared evidence is reduced, and the reduction must be frozen before target scoring.

## Reliability development protocol

### Development corpus

Use only development cases for bridge construction and reliability work. Owner data and anyone whose evidence materially shaped the ontology/codebook remain development data.

Sample episodes across:

- major evidence domains;
- short/long narratives;
- typed/voice transcripts;
- clear and ambiguous cases;
- positive/negative/mixed/insufficient states;
- counterexamples;
- theory-exposed language where ethically available;
- languages/cultural contexts actually intended for early deployment.

### Human coding baseline

At least two independent trained coders for development reliability slices, blinded to all birth/model information.

Coder training uses the released candidate codebook. Disagreements are preserved before adjudication.

Report per observable:

- sample size;
- class distribution;
- raw agreement;
- confusion matrix;
- scale-appropriate Krippendorff alpha where appropriate;
- sensitivity agreement statistic where prevalence is extreme;
- abstention/insufficient rate;
- adjudication rate;
- error taxonomy.

No fixed universal release threshold is declared in this spec. Thresholds must be chosen with observable consequences, prevalence, ambiguity and intended model use in view and then frozen prospectively.

### LLM candidate coder

Only after human baseline exists:

1. freeze exact model/version/prompt/schema/examples/settings;
2. code the held-out human-development slice without birth/model information;
3. compare against human reference and human-human disagreement;
4. measure classwise errors and abstention, not only aggregate accuracy;
5. inspect systematic subgroup/modality/language errors;
6. either reject, restrict to specific observables, route uncertain cases to humans, or accept for a new version;
7. do not inspect model-tournament success during this decision.

## Construct-validity program

Reliability alone is insufficient. For each major observable family maintain a validation ledger covering applicable evidence sources:

- **content:** literature/ontology/measure rationale and expert review;
- **response/coding process:** whether interview evidence and coder behavior actually instantiate the intended construct;
- **internal structure:** where composites/aggregates are claimed;
- **external relations:** convergence/discriminant evidence against independent measures where scientifically meaningful;
- **generalizability/invariance:** modality/language/culture/time/context;
- **consequences:** whether coding/aggregation creates systematic bias, false certainty, or model favoritism.

Model accuracy is downstream criterion evidence at most; it must never be the sole evidence that the measurement bridge is valid.

## Immediate implementation boundary

Implement next, before any actual model adapter:

1. immutable Pydantic/JSON schema for ontology releases and coded episode records;
2. external-source/reuse registry fields;
3. stable version/hash validation using `hdmatch.experiments.canonical`;
4. explicit missing/insufficient/not-applicable state machine;
5. provenance validation that every scoreable code points to evidence inside the same behavioral freeze;
6. deterministic person-level aggregation interface that preserves coverage and heterogeneity;
7. validation-report schema for human-human and human-automated reliability results;
8. **template/example observables only**, clearly non-authoritative and synthetic until construct-specific literature review is complete;
9. tool-neutral annotation export/import contract;
10. tests for hash integrity, ontology versioning, provenance, missingness, model blindness, and aggregation semantics.

Do **not** yet implement:

- the substantive HD/astrology target ontology by intuition;
- a production LLM coder;
- a model-specific narrative-reading bridge;
- birth/model access in the coding path;
- participant-facing model execution;
- a claim that the bridge is validated.

## Acceptance criteria for the framework milestone

1. The coding framework can represent rich episode-level evidence without forcing a value when evidence is insufficient.
2. Every coded observable is pinned to one released ontology definition and exact source evidence inside one behavioral freeze.
3. Released ontology artifacts are immutable/content-addressed and old versions remain interpretable.
4. External reused/adapted concepts retain source identifiers/provenance.
5. Person-level aggregation explicitly reports evidence coverage and heterogeneity.
6. No model family, chart, birth input, rank or prediction can enter Stage A.
7. Stage B remains declarative and cannot reread raw narrative.
8. Human reliability results and automated-coder reliability results share one auditable report contract.
9. Synthetic framework fixtures cannot be mistaken for a validated substantive ontology.
10. CI/Ruff/mypy remain green.
