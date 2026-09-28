# Empirical Astrology Corpus: GPT Execution Plan

Date: 2026-09-28

## Goal

Mine the empirical astrology literature for algorithmically useful findings: exact predictors, outcomes, effect directions/sizes, boundary conditions, replications, failures, and technical definitions that can become candidate features or negative constraints in the HumanDesign/astro research harness.

This is an execution plan for GPT-assisted work in this repository. It does not depend on the Deep Research app.

## What the corpus actually looks like

The best backbone is *Understanding Astrology* (Dean, Mather, Nias & Smit, 2022), available free as four PDFs. It is 948/952 pages, >650,000 words, and claims coverage of roughly 1,000 empirical studies from 1900-2020, with >4,000 references. Its Individual Studies section runs approximately pp.197-753 and is already organized into signs, application issues, conferences/surveys, events, Gauquelin topics, personality, and research issues. It also says 210 conference/website studies are discussed but not counted in the final 1,000 unless reviewed elsewhere.

This book is a discovery/index layer, not an authority layer. Its conclusions are contested in *Correlation*, so any finding we might encode in an algorithm must be checked against the original study and substantive critiques/reanalyses.

A second backbone is the complete *Correlation* contents index (1968 onward). The Astrological Association provides a 46-page contents index through 2025 and the Correlation site lists 2026 issues. The journal currently publishes twice yearly. Full issue PDFs are generally part of the Correlation digital archive subscription, although some individual issue PDFs/articles are publicly indexed.

Historical specialist research also includes:
- *Astro-Psychological Problems* (APP), 1982-1995.
- *Astrologie in Onderzoek* / precursors (AinO), 1977-2003.
- *Kosmos* / ISAR research material, especially 1978-1995.
- NCGR Research Journal / Syzygy and related research issues.

The astrology-and-science archive has detailed abstracts of 91 selected studies from Correlation, APP, AinO, and Kosmos and estimates the underlying four-journal source material at about 4.6 million words. Its 2007 academic-database bibliography contained 1,674 astrology-related references, of which it estimated about 10% were purely empirical. These overlap substantially with the 2022 book and must be deduplicated.

Therefore 1,000 studies does NOT mean 1,000 independent journal articles. Some papers contain several studies; some records are books, chapters, theses, conference reports, unpublished work, replications, or reanalyses; and many share datasets. The first task is to measure the actual number of unique source documents and independent datasets.

## Execution strategy

### Pass 1 — Build the master study inventory from the 2022 backbone

Read the four *Understanding Astrology* PDFs directly, especially pp.197-753 and pp.755-862. For each individual study create a structured record with citation/source/year, study family/dataset, sample and birth-data quality, exact predictor, exact outcome, exact astrological definition, reported effect and direction, reviewer criticism, replication/reanalysis references, whether original full text is needed, and algorithmic relevance.

Do not accept the book's verdict as the result. Keep the authors' reported result separate from the secondary review's interpretation.

Expected size: approximately 1,000 study records plus some additional conference/website records.

### Pass 2 — Independent positive-evidence and specialist-journal crosswalk

Independently extract Correlation's 63-study Evidence List (2020, updated in 2022), the 91-study Correlation/APP/AinO/Kosmos abstract collection, complete Correlation TOCs through 2026, NCGR/Syzygy research-journal TOCs, Journal of Scientific Exploration astrology/Gauquelin papers, and other specialist empirical sources discovered in references. Crosswalk these against Pass 1 so the inventory is not controlled by the framing or omissions of one review team.

### Pass 3 — Post-2020 update

Search 2021-2026 for empirical work not in the 2022 book: Correlation, NCGR/Syzygy, Journal of Scientific Exploration, mainstream psychology/medical/social-science databases, theses/preprints, and citation chains from major authors.

### Pass 4 — Triage for full-text retrieval

Assign each record:
- A — MUST READ ORIGINAL: potential algorithm feature, important null, major replication/reanalysis, or contested influential result.
- B — READ IF AVAILABLE: potential moderator/secondary feature, useful technical detail, or weak/isolated signal.
- C — SUMMARY SUFFICIENT FOR NOW: low algorithmic value, redundant report, or peripheral exploratory result.
- D — OUT OF SCOPE: not empirical or not relevant to the model.

Do not use a finding as an algorithmic prior/weight unless the original/fullest primary source has been checked.

### Pass 5 — Full-text extraction

For A papers extract exact hypotheses; all tested predictors/outcomes, not only significant ones; sample construction; birth-time source/precision; chart calculation details; aspect/orb/house/angle definitions; statistical method; multiplicity; sufficient statistics/effect size; subgrouping; data reuse; robustness checks; author's stated result; our methodological assessment; and replication status. A single paper may yield many feature-level rows.

### Pass 6 — Build the evidence graph

Connect feature -> outcome -> study -> dataset -> replication/reanalysis -> result. This prevents multiple papers using the same Gauquelin or Astro-Databank sample from masquerading as independent replication.

### Pass 7 — Produce the development feature registry

Every candidate rule ends as replicated_candidate, promising_requires_replication, interaction_only_candidate, definition_uncertain, likely_confounded, negative_constraint, or insufficient_evidence. No literature-derived feature enters untouched validation automatically.

## Full-text acquisition

Yes, additional full texts will be needed.

Already readily accessible: *Understanding Astrology* 2022 (free four-part PDF); some Correlation issues/articles; some APP scans; many mainstream papers through open copies/repositories; and some NCGR issues.

Likely bottlenecks: the complete Correlation archive (official site says PDFs of all past editions are available to subscribers); older APP/AinO/Kosmos issues; older books/monographs and theses; mainstream paywalled articles without repository copies; and NCGR/Syzygy issues that are member-only or sold individually.

Acquisition order: public/legal full text -> author/repository copy -> existing Project/Library files -> journal subscription/library access supplied by user -> interlibrary/author request for high-value unresolved sources. Triage first; do not buy every source.

## Time estimate using GPT rather than human manual reading

These are active-work estimates, not promises of unattended/background completion.

Inventory/triage:
- Parse the 2022 review into ~1,000 study records: 6-12 GPT/tool hours.
- Crosswalk Correlation + 91-study specialist set + post-2020 material: 4-8 hours.
- Deduplication/study-family linking and first priority pass: 4-8 hours.
- First usable evidence map: roughly 14-28 active hours.

High-value full-text layer: planning assumption 150-250 papers/chapters deserve A-level original-source checking after deduplication. At roughly 5-10 minutes of tool/reasoning time per ordinary paper, with longer treatment for major controversies: ~15-30 hours for 150 sources or ~25-50 hours for 250 sources. Retrieval delays are separate.

Near-exhaustive full-text audit: if we ultimately deep-extract every retrievable primary document rather than only the algorithmically relevant subset, use a planning range of ~60-120+ active GPT/tool hours after acquisition. Revise this after Pass 1 tells us how many unique documents sit behind the ~1,000 study records.

This is realistically a multi-session project measured in days/weeks of active work, but not the 10-12 human-team weeks proposed by the previous Deep Research output.

## First milestone

Do not acquire hundreds of PDFs yet. First ingest the four free *Understanding Astrology* PDFs; turn the individual-study sections into a machine-readable inventory; crosswalk the 63-study pro-astrology Evidence List; crosswalk the 91 selected specialist-journal studies; add Correlation 2021-2026 and NCGR/Syzygy; and produce the A/B/C/D full-text queue. Only then will we know exactly how many full texts are worth obtaining.

## Mission Control

The currently exposed Mission Control connector in this chat is supervisory/read-only (binding, challenge, and liveness lookups); it does not expose a generic action for launching literature-review workers. Therefore the actual corpus work should be executed by GPT with web/academic retrieval and persisted in this repository. If Mission Control supplies a bound supervisory request, use it to supervise/verify the relevant batch, but do not block the literature pipeline waiting for it.

## Sources used to size the project

- Dean, Mather, Nias & Smit (2022), *Understanding Astrology*: https://www.astrology-and-science.com/U-aino3.htm
- Correlation current/previous issues: https://correlationjournal.com/correlation-issues/
- Astrological Association Correlation archive/subscription: https://www.astrologicalassociation.com/product/correlation/
- Correlation complete contents index: https://www.astrologicalassociation.com/wp-content/uploads/2025/11/correlationindex.pdf
- 91-study specialist-journal abstracts: https://www.astrology-and-science.com/d-rese2.htm
- Academic reference alert: https://www.astrology-and-science.com/u-refs2.htm
- Correlation 32(2) 2020 Evidence List: https://www.astrologicalassociation.com/wp-content/uploads/2021/05/c20203202-1.pdf
- NCGR publications/research journal archive: https://ncgrastrology.org/publications-2/