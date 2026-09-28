# Empirical Astrology Corpus — Parallel Wave 1

Date: 2026-09-28

## Decision

Use 10 extraction workers in parallel, with this chat/repo acting as coordinator. This corpus is not a 1–2-tab job: Chapter 7 alone contains more than 700 individual studies over roughly 558 pages, and Chapter 8 synthesizes more than 400 studies. The first wave should divide the backbone by non-overlapping page ranges so workers cannot duplicate or overwrite each other.

Each worker MUST write only to its own output files. Do not edit shared master files. A later coordinator pass will deduplicate and merge.

## Source

Dean, Mather, Nias & Smit (2022), *Understanding Astrology: A critical review of a thousand empirical studies 1900–2020*.

Free PDFs:
- UA-2: https://astrology-and-science.com/UA-2.pdf — Chapter 7 pp.197–494.
- UA-3: https://astrology-and-science.com/UA-3.pdf — Chapter 7 pp.495–754.
- UA-4: https://astrology-and-science.com/UA-4.pdf — Chapter 8 onward, pp.755–948.

UA reports that Chapter 7 summarizes >700 individual studies and Chapter 8 provides overviews of >400 studies. The whole book reviews roughly 1,000 empirical studies; these counts overlap and are not counts of unique independent datasets.

## Worker assignments

1. W01 Signs: book pp.197–272.
2. W02 Application Issues A: pp.273–329.
3. W03 Application Issues B: pp.330–386.
4. W04 Conferences/Surveys + early Events: pp.387–450.
5. W05 later Events + Gauquelin Topics: pp.451–526.
6. W06 Personality A: pp.527–572.
7. W07 Personality B: pp.573–618.
8. W08 Research Issues A: pp.619–685.
9. W09 Research Issues B + Chapter 7 summary: pp.686–754.
10. W10 Chapter 8 synthesis: pp.755–862. This worker extracts cross-study conclusions and, especially, every cited study/result that is not already clearly represented by Chapter 7. It must flag overlaps rather than silently duplicate them.

## Required output per worker

Write two files:
- `data/empirical_astrology/wave1/worker_XX_studies.jsonl`
- `notes/empirical_astrology/wave1/worker_XX_report.md`

Do not touch another worker's files.

### JSONL record schema

One JSON object per study or feature-level result. Use null when unavailable.

Fields:
- record_id
- worker_id
- ua_section_id
- ua_book_pages
- citation_raw
- authors
- year
- title
- source
- source_type
- study_family
- dataset_name_or_description
- likely_dataset_reuse
- sample_n
- population
- birth_data_source
- birth_time_quality
- predictor_family
- predictor_exact
- predictor_definition
- outcome_family
- outcome_exact
- statistical_method
- multiplicity_handling
- effect_size
- p_value_or_interval
- sufficient_statistics
- original_reported_result
- result_direction: positive | null | opposite | mixed | unclear | nonempirical
- ua_interpretation
- ua_criticism
- replication_or_reanalysis_refs
- algorithmic_relevance
- candidate_feature_or_constraint
- full_text_priority: A | B | C | D
- full_text_status
- primary_source_url_if_given
- extraction_notes

A paper with multiple independently testable predictors/outcomes should generate multiple feature-level records where the text permits it.

### Priority rules

A — original full text mandatory before algorithm use:
- potential algorithm feature;
- strong/interesting positive;
- important null that could exclude a major feature family;
- replication/reanalysis;
- influential controversy;
- technical definition needed to reproduce result.

B — useful original if accessible:
- moderator, secondary feature, modest/isolated effect, useful technical detail.

C — summary adequate for current phase:
- peripheral/redundant empirical result with low algorithmic information.

D — nonempirical/out of scope.

### Extraction discipline

1. Preserve the original study's reported finding separately from Dean et al.'s interpretation.
2. Do not convert the review authors' criticism into the original result.
3. Extract negative/null findings as carefully as positive findings.
4. Record exact N, orbs, angular sectors, aspect definitions, house/sign definitions, effect sizes, p-values, and raw counts whenever printed.
5. Flag likely reuse of Gauquelin, Astro-Databank, Eysenck/Dean, or other recurring datasets.
6. Do not infer missing statistics.
7. Do not decide whether astrology is true.
8. Do not create an optimized algorithm yet.
9. Commit output to the humandesign repository when the assigned range is complete.
10. In the worker report, give counts: study-level sources, feature-level records, A/B/C/D totals, positive/null/opposite/mixed totals, likely reused datasets, and the top 10 original sources that coordinator should retrieve next.

## Worker prompt template

You are Worker WXX in the empirical-astrology corpus project. Work only on the assigned book-page range above. Read the full assigned range of *Understanding Astrology* directly, not search snippets. Extract every empirical study and every algorithmically meaningful feature-level result into the specified JSONL schema. Preserve original reported results separately from the review authors' interpretation. Capture positive, null, mixed and opposite findings equally. Record exact quantitative details whenever available. Write only your two worker-specific files and commit them to u-dont-existDOTcom/humandesign. Do not edit shared/master files. Continue until the entire assigned page range is exhausted; do not stop after interesting examples. Your final chat response should report the commit SHA and extraction counts.

## Coordinator merge after Wave 1

After all ten commits:
1. inspect every worker output;
2. normalize citations;
3. deduplicate source documents;
4. create study-family/dataset IDs;
5. merge feature records;
6. identify conflicts between Chapter 7 and Chapter 8;
7. generate the A/B/C/D full-text acquisition queue;
8. then launch Wave 2, partitioned by source family rather than book pages:
   - Correlation Evidence List and full archive;
   - 91 specialist-journal studies;
   - Gauquelin primary/replication chain;
   - personality/aspect/orb originals;
   - astrologer matching/blind-test originals;
   - relationship/synastry originals;
   - time-twin originals;
   - post-2020 empirical literature;
   - dataset/reuse audit;
   - full-text acquisition/DOI/open-copy resolver.

Wave 2 should not begin until Wave 1 gives us canonical citations and priorities.
