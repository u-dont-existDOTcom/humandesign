# Empirical Astrology — Wave 1.5 Normalization and Wave 2 Full-Text Plan

Date: 2026-09-28

## Purpose

Wave 1 produced 1,248 feature-level records across 10 worker files. Before retrieving large numbers of original papers, normalize and deduplicate the corpus so repeated publications, reanalyses, and reused datasets are not mistaken for independent evidence.

Do not alter the original Wave 1 worker files. All new work must go to worker-specific Wave 1.5 / Wave 2 files.

---

# WAVE 1.5 — NORMALIZATION / DEDUPLICATION

Use 6 workers.

Recommended model: **GPT-5.6 Sol, High** for all six workers.
Use **Extra High only for N06**, where conflicting records and study-family adjudication require more reasoning.

Do not use GPT-5.6 Pro yet.

## N01 — Normalize W01-W02
Inputs:
- data/empirical_astrology/wave1/worker_01_studies.jsonl
- data/empirical_astrology/wave1/worker_02_studies.jsonl

Outputs:
- data/empirical_astrology/wave1_5/n01_normalized.jsonl
- notes/empirical_astrology/wave1_5/n01_report.md

Task:
- normalize citation strings
- split bundled citations where possible
- infer canonical source-document identity only when supported
- assign provisional source_document_id
- assign provisional dataset_id / study_family_id
- preserve all original content
- flag suspected duplicates/reanalyses/reused cohorts
- do not collapse records yet

## N02 — Normalize W03-W04
Same task, inputs W03-W04.

Outputs:
- n02_normalized.jsonl
- n02_report.md

## N03 — Normalize W05-W06
Same task, inputs W05-W06.

## N04 — Normalize W07-W08
Same task, inputs W07-W08.

## N05 — Normalize W09-W10
Same task, inputs W09-W10.

## N06 — Cross-worker deduplication and conflict map
Recommended model: **GPT-5.6 Sol, Extra High**

Inputs:
- all 10 Wave 1 worker files
- N01-N05 normalized outputs

Outputs:
- data/empirical_astrology/wave1_5/master_source_registry.jsonl
- data/empirical_astrology/wave1_5/master_dataset_registry.jsonl
- data/empirical_astrology/wave1_5/cross_worker_duplicate_map.jsonl
- notes/empirical_astrology/wave1_5/n06_conflict_report.md

Task:
- reconcile source_document_id collisions
- reconcile dataset_id / cohort reuse across workers
- identify Chapter 7 / Chapter 8 duplicate coverage
- identify multiple papers using the same cohort
- distinguish replication vs reanalysis vs commentary
- flag contradictory extraction or bibliographic uncertainty
- do not delete any records
- do not synthesize astrology conclusions yet

## Universal Wave 1.5 worker prompt

Read:
- tasks/EMPIRICAL_ASTROLOGY_WAVE1_5_AND_WAVE2_PLAN_20260928.md
- tasks/EMPIRICAL_ASTROLOGY_PARALLEL_WAVE1_20260928.md
- AGENTS.md

You are Worker NXX. Execute only your assigned Wave 1.5 task.

Do not edit any Wave 1 file. Preserve all original extracted claims. Normalize identity and provenance, not scientific conclusions. Write only your assigned output files. Commit your completed output on a worker-specific branch and publish through the GitHub connector/API if shell push lacks credentials.

Continue until the full assigned input is exhausted. Final response: report commit SHA, output counts, unresolved identity conflicts, and any high-risk duplicate families.

---

# WAVE 2 — ORIGINAL FULL-TEXT RETRIEVAL / EXTRACTION

Launch only after N06 has produced the canonical source and dataset registries.

Use up to 10 workers in parallel.

Default model: **GPT-5.6 Sol, High**.
Upgrade to **Extra High** when:
- reconstructing complicated statistical analyses;
- adjudicating competing reanalyses;
- tracking overlapping Gauquelin datasets;
- evaluating multiplicity or control-generation methods;
- converting old scanned tables into precise feature definitions.

Use **GPT-5.6 Pro only for final synthesis / algorithm architecture**, not routine paper extraction.

## F01 — Gauquelin / planetary-sector research
Priority:
- primary Gauquelin papers/books/data
- Ertel replications/reanalyses
- heredity/profession/eminence datasets
- control construction and sector definitions

Model: Sol Extra High

## F02 — Personality / Sun-sign / self-attribution
Priority:
- Mayo-White-Eysenck
- Smithers-Cooper
- Niehenke
- Steyn
- Bourque
- sign-knowledge confound studies

Model: Sol High

## F03 — Aspects / orb / angularity / harmonics
Priority:
- Startup
- Tarvainen
- Addey
- Pottenger/Vail
- exact continuous-angle studies
- applying/separating
- angularity interactions

Model: Sol Extra High

## F04 — Whole-chart matching / astrologer blind tests
Priority:
- Carlson
- Dean
- McGrew & McFall
- Indiana / Mull
- Heukelom
- chart-vs-biography / client matching

Model: Sol Extra High

## F05 — Time twins / same-time births
Priority:
- Roberts & Greengrass
- French et al.
- Dean & Kelly
- NCDS 2,101-person analyses
- Steyn time-twin subset
- Fuzeau-Braesch twins where relevant

Model: Sol High

## F06 — Relationships / synastry
Priority:
- Ruis
- van de moortel
- Gauquelin couples
- marriage/divorce registry studies
- Voas
- relationship aspect-frequency work

Model: Sol High

## F07 — Vocational / profession / eminence
Priority:
- doctor/clergy/profession datasets
- commander / politician / artist / scientist studies
- Gauquelin profession derivatives
- occupation-degree studies

Model: Sol High

## F08 — Prediction / transits / event timing / rectification
Priority:
- transits
- horary
- mundane prediction
- rectification
- prenatal epoch
- prospective prediction contests
- development-vs-holdout failures

Model: Sol High

## F09 — High-dimensional / computational astrology
Priority:
- McDonough AstroDataBank scan
- Bergen
- Godbout
- Dean IRT
- machine learning / automated chart matching
- multiplicity and control-generator studies

Model: Sol Extra High

## F10 — Post-2020 and specialist-journal update
Priority:
- Correlation 2021-2026
- NCGR / Syzygy
- Journal of Scientific Exploration
- theses/preprints
- empirical studies not covered by Understanding Astrology

Model: Sol High

## Required full-text worker outputs

Each worker writes:
- data/empirical_astrology/wave2/fXX_primary_extractions.jsonl
- notes/empirical_astrology/wave2/fXX_report.md
- notes/empirical_astrology/wave2/fXX_missing_fulltexts.md

For every original paper:
- canonical citation and source_document_id
- full-text URL / access status
- dataset_id
- exact sample construction
- birth data provenance and precision
- exact predictor definitions
- exact outcome definitions
- all tested hypotheses, not only significant ones
- statistical method
- multiplicity correction
- exact effect sizes / counts / p-values / CIs where available
- original author conclusion
- replication/reanalysis links
- methodological risk notes
- algorithmic candidate / negative-constraint note
- whether result is confirmatory, exploratory, post-hoc, or unclear
- whether it is independent of earlier datasets

Do not infer missing numbers.

## Full-text acquisition policy

Search in this order:
1. publisher / journal open full text
2. author / institutional repository
3. legitimate archive / thesis repository
4. existing Project/Library files
5. flag as missing

Do not purchase anything automatically.
Do not use secondary summaries as substitutes where the paper is marked A-priority and the original can plausibly be found.

---

# FINAL SYNTHESIS AFTER WAVE 2

Only after Wave 2 is merged:

Use **GPT-5.6 Pro** or **GPT-5.6 Sol Extra High**.

Produce:
- canonical empirical feature registry
- replicated vs nonreplicated evidence map
- negative-constraint registry
- dataset-independence graph
- effect-size summary where comparable
- proposed literature-derived candidate astro model
- ablation plan
- prospective preregistration
- untouched validation plan

Historical literature remains DEVELOPMENT evidence only. It cannot be used to claim prospective validation.
