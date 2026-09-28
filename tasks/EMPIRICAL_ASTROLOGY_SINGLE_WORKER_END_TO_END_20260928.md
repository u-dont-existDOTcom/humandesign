# Empirical Astrology — Single-Worker End-to-End Literature Mining Task

Date: 2026-09-28

## Model / thinking level

Use **GPT-5.6 Sol, Extra High**.

Do not use Deep Research.
Do not split this task into subworkers.
Do not stop after normalization, after a few example papers, or after producing another plan.

This is an execution task.

## Goal

Starting from the completed Wave 1 corpus already merged into `main`, turn the 1,248 extracted feature-level records into a cleaned empirical evidence base and then retrieve/read the highest-value original studies needed to identify candidate features, negative constraints, replications, and unresolved gaps for an optimized astrology algorithm.

Historical literature is DEVELOPMENT evidence only. Do not claim prospective validation.

## Inputs

Read first:

- `AGENTS.md`
- `tasks/EMPIRICAL_ASTROLOGY_PARALLEL_WAVE1_20260928.md`
- all 10 files:
  - `data/empirical_astrology/wave1/worker_01_studies.jsonl`
  - ...
  - `data/empirical_astrology/wave1/worker_10_studies.jsonl`
- all 10 worker reports:
  - `notes/empirical_astrology/wave1/worker_01_report.md`
  - ...
  - `notes/empirical_astrology/wave1/worker_10_report.md`

Also use the Wave 1 coordinator/recovery notes only as provenance context, not as scientific evidence.

## Phase 1 — Normalize all 1,248 Wave 1 records

Do not edit any Wave 1 file.

Create:

- `data/empirical_astrology/master/normalized_feature_records.jsonl`
- `data/empirical_astrology/master/source_registry.jsonl`
- `data/empirical_astrology/master/dataset_registry.jsonl`
- `data/empirical_astrology/master/duplicate_reanalysis_map.jsonl`

For every Wave 1 record:

1. preserve the original record and worker provenance;
2. normalize author names, year, title, source/journal, volume/issue/pages/DOI/URL where recoverable;
3. assign a canonical `source_document_id`;
4. assign a canonical `dataset_id` where the underlying cohort/sample can be identified;
5. assign a `study_family_id` for repeated research programmes;
6. identify:
   - exact duplicate coverage;
   - Chapter 7 / Chapter 8 duplicate coverage;
   - later reanalysis of the same data;
   - repeated publication of the same cohort;
   - independent replication;
   - commentary/review only;
7. preserve positive/null/opposite/mixed direction exactly as originally extracted;
8. never infer missing statistics.

The source registry must distinguish:
- unique source document count;
- empirical source document count;
- unique dataset/cohort count;
- genuinely independent replication count where identifiable;
- uncertain identity conflicts.

## Phase 2 — Build a ranked original-source acquisition queue

Create:

- `data/empirical_astrology/master/fulltext_queue.jsonl`
- `notes/empirical_astrology/master/fulltext_queue.md`

Rank every source A/B/C/D using algorithmic information value, not whether it is positive.

Priority A includes:
- strong/interesting positive findings that could become algorithm features;
- important nulls that could eliminate a major feature family;
- major replications or failed replications;
- major controversies/reanalyses;
- sources needed to reconstruct an exact technical rule;
- high-dimensional scans;
- orb/aspect/angularity work;
- Gauquelin primary/replication work;
- time-twin work;
- astrologer-blind matching;
- personality/sign-confound work;
- synastry/relationship work;
- profession/eminence studies;
- prediction/transit/rectification studies;
- computational/ML studies.

Do not acquire every old paper indiscriminately.

## Phase 3 — Retrieve original full texts

For every A-priority source, and then the highest-value B sources if time permits, actively search for the original/fullest primary text.

Search in this order:

1. publisher/journal open full text;
2. author/institutional repository;
3. legitimate journal/archive copy;
4. thesis/dissertation repository;
5. existing Project/Library files if already available;
6. otherwise mark missing.

Do not purchase anything.
Do not ask the user to obtain material until you have exhausted publicly/legal accessible copies.

When a PDF is used, inspect the PDF itself, not search snippets.

Create:

- `data/empirical_astrology/fulltexts/fulltext_manifest.jsonl`
- `notes/empirical_astrology/fulltexts/missing_fulltexts.md`

For each source record:
- canonical source_document_id;
- exact citation;
- access URL;
- full-text status;
- file/source provenance;
- whether primary, reanalysis, replication, or secondary;
- pages/sections actually inspected;
- missing-material note where relevant.

## Phase 4 — Extract originals at feature level

Create:

- `data/empirical_astrology/fulltexts/primary_feature_extractions.jsonl`

For every retrieved original paper, extract all algorithmically meaningful tested claims, not just the significant ones.

Required fields:

- source_document_id
- dataset_id
- study_family_id
- citation
- sample_n
- population
- birth-data source and precision
- inclusion/exclusion rules
- exact predictor family
- exact predictor definition
- zodiac/reference frame
- house system
- aspect definition
- orb definition
- applying/separating handling
- angularity/sector definition
- exact outcome
- measurement instrument
- statistical method
- multiplicity handling
- effect size
- uncertainty / CI
- p-value / Bayes factor
- raw counts / sufficient statistics when available
- whether hypothesis was a priori / exploratory / post-hoc / unclear
- original author conclusion
- replication/reanalysis relation
- methodological risk notes
- algorithmic candidate or negative constraint
- whether independent of earlier datasets

If a paper tested 60 aspects, preserve the tested feature family sufficiently to know what was actually examined. Where detailed row-level extraction is practical and useful, produce multiple records.

Do not let a paper's abstract substitute for the methods/results when the full text is available.

## Phase 5 — Trace the major empirical research programmes

At minimum, make sure the original-source layer adequately covers these programmes where sources are retrievable:

### Gauquelin / planetary sectors
- primary Gauquelin profession/eminence work;
- replications;
- Ertel analyses/reanalyses;
- heredity work;
- control-generation disputes;
- sector definitions;
- dataset reuse.

### Personality / signs / self-attribution
- Mayo–White–Eysenck;
- Smithers–Cooper;
- Niehenke;
- Bourque;
- Steyn;
- sign-knowledge/self-attribution controls.

### Aspects / orb / angularity / harmonics
- Startup;
- Tarvainen;
- Addey;
- Vail/Pottenger;
- continuous angular separation;
- tight versus wide;
- applying versus separating;
- angularity interactions.

### Whole-chart / blind astrologer matching
- Carlson;
- Dean;
- McGrew & McFall;
- Heukelom;
- Indiana/Mull;
- chart-to-biography matching;
- client-authentic-vs-control reading tests.

### Time twins
- Roberts & Greengrass;
- French et al.;
- Dean & Kelly;
- NCDS;
- Steyn;
- Fuzeau-Braesch where relevant.

### Relationships / synastry
- Ruis;
- van de moortel;
- Gauquelin couple datasets;
- marriage/divorce registries;
- Voas;
- aspect-frequency relationship work.

### Vocation / profession / eminence
- doctor/clergy/professional samples;
- politician/artist/scientist/commander studies;
- Gauquelin derivatives;
- degree-area occupation studies.

### Prediction / transits / rectification
- transits;
- progressions;
- mundane prediction;
- horary;
- rectification;
- prenatal epoch;
- prospective prediction contests;
- development-vs-holdout failures.

### High-dimensional / computational astrology
- McDonough;
- Bergen;
- Godbout;
- Dean IRT;
- automated chart matching;
- ML/statistical scans;
- multiplicity and control-generator studies.

### Post-2020 update
Search 2021–2026:
- Correlation;
- NCGR / Syzygy;
- Journal of Scientific Exploration;
- theses;
- preprints;
- other relevant empirical sources.

Add new sources to the same registries and extraction format.

## Phase 6 — Produce the evidence map

Create:

- `notes/empirical_astrology/master/evidence_map.md`
- `data/empirical_astrology/master/candidate_feature_registry.jsonl`
- `data/empirical_astrology/master/negative_constraint_registry.jsonl`

For each major feature family, summarize:

- what has actually been tested;
- positive findings;
- null/opposite findings;
- effect sizes;
- exact definitions;
- moderator/boundary conditions;
- independent replications;
- failed replications;
- dataset overlap;
- multiple-testing risk;
- confounds;
- whether it deserves prospective testing.

Candidate statuses:

- `replicated_candidate`
- `promising_requires_replication`
- `interaction_only_candidate`
- `definition_uncertain`
- `likely_confounded`
- `negative_constraint`
- `insufficient_evidence`

Do not produce one arbitrary overall truth score.

## Phase 7 — Translate the literature into an algorithm-development specification

Create:

- `notes/empirical_astrology/master/literature_derived_algorithm_spec.md`

This is a DEVELOPMENT specification, not a validated model.

For every proposed candidate feature:

- exact astronomical calculation;
- exact predictor definition;
- exact outcome domain it was reported to relate to;
- evidence source(s);
- dataset independence;
- effect direction;
- effect size where usable;
- whether weight can be evidence-derived or must be learned;
- dependencies/redundancies;
- required interaction terms;
- required ablation;
- required held-out prospective test.

Explicitly include the current protocol decision:

- primary same-hospital / near-time-birth personality test remains theory-neutral;
- aspect/orb tightness and angularity are preregistered secondary moderators;
- specific aspect-to-trait mappings must be frozen before outcomes;
- held-out replication is required.

## Phase 8 — Final report

Create:

- `notes/empirical_astrology/master/END_TO_END_REPORT_20260928.md`

Report:

1. total Wave 1 feature records processed;
2. unique source documents;
3. empirical source documents;
4. unique datasets/cohorts;
5. likely independent replications;
6. number of full texts retrieved;
7. number still missing;
8. A/B/C/D queue counts;
9. most promising candidate signals;
10. strongest negative constraints;
11. highest-value unresolved claims;
12. dataset-reuse problems;
13. post-2020 additions;
14. what should enter the next algorithm version;
15. what should explicitly NOT enter it;
16. what prospective experiments would most efficiently discriminate among the remaining hypotheses.

## Quality rules

- Never count multiple papers on the same cohort as independent replication.
- Never treat a review author's conclusion as the primary result.
- Never convert a missing statistic into an estimate unless explicitly marked as an approximate derivation and mathematically justified.
- Never optimize on the user's known chart or known life events.
- Never use historical development evidence as untouched validation.
- Preserve null and failed results.
- Distinguish exploratory discovery from confirmatory testing.
- Distinguish statistical significance from practical predictive value.
- Treat prior astrology knowledge/self-attribution as a confound wherever relevant.
- Treat astronomical prevalence/base rates and control construction as part of the model.
- Correct for multiplicity conceptually and quantitatively wherever the source permits.
- Do not stop merely because some full texts are missing. Continue with all available material and produce a missing-source queue.

## Git / publication rules

Save all work in `u-dont-existDOTcom/humandesign`.

Do not edit the original Wave 1 files.

Work on a dedicated branch:
`worker/empirical-astrology-end-to-end`

If shell Git lacks credentials, use the connected GitHub connector/API.

Commit/publish the completed outputs and verify remote contents.

## Final worker response

Report:
- remote branch;
- final commit SHA;
- counts for normalized records, unique sources, unique datasets, full texts retrieved, missing A-priority texts, candidate features, negative constraints;
- major unresolved methodological conflicts;
- confirmation that the task reached the end-to-end report and did not stop at planning or partial extraction.
