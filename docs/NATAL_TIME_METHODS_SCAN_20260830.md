# Natal-time inference bounded methods scan — 2026-08-30

## Status and boundary

This documentation-only scan satisfies the bounded literature task authorized by ChatGPT Pro checkpoint 2. It began after the independent conception was frozen in `docs/NATAL_TIME_INDEPENDENT_CONCEPTION_SNAPSHOT_20260830.md`. It does not select or implement a ranking target, likelihood, prior, weight, score, threshold, questionnaire item, stopping rule, calibration rule, cohort size, or participant-facing label.

The scan is a targeted methods review, not a systematic review or a claim of literature exhaustiveness. It asks which established methods can constrain a later supervised design and which apparent analogies do not transfer. The status labels below mean:

- **Directly reusable** — a methodological constraint can be adopted without defining natal-inference semantics.
- **Needs adaptation** — the method is relevant, but its estimand, assumptions, sample structure, or output does not directly match one person's chart-state candidates.
- **Incompatible as a direct method** — using the method as-is would answer a different question, manufacture unsupported meaning, or violate the frozen design.
- **Unresolved** — evidence is insufficient to select among scientifically different alternatives.
- **Strongest established baseline** — the minimum comparison a future bespoke component would have to improve upon in independent validation.

## Overall finding

The bounded scan did not identify a peer-reviewed method that validates Human Design or astrological birth-time rectification from natal self-report, nor one that directly turns a single person's chart-distinct intervals into defensible probabilities. The strongest directly reusable foundation is therefore the one already implemented: keep every engine-distinct interval in an unordered, no-pruning candidate set; preserve evidence lineage; blind behavioral collection to candidate identity; freeze every adaptive choice before evaluation; and require future bespoke inference to beat ordinary non-HD and null baselines on untouched participants.

Published double-blind natal-chart matching studies are not birth-time-rectification studies and do not directly test Human Design. They are nevertheless relevant adverse evidence for treating natal-description matching as established: Carlson tested natal-chart personality descriptions under a double-blind protocol, and Wyman and Vyse found that participants could identify their psychometric profile above chance but not their computer-generated astrological summary ([Carlson 1985](https://doi.org/10.1038/318419a0); [Wyman and Vyse 2008](https://pubmed.ncbi.nlm.nih.gov/18649494/)). Accordingly, traditional rectification practice cannot serve as validation, a prior, or a performance baseline without new blinded out-of-sample evidence.

## Method matrix

| Topic | Established result or constraint | Transfer status | Project implication without selecting semantics | Key source |
| --- | --- | --- | --- | --- |
| Birth-time rectification / natal matching | The located controlled literature tests whether people or astrologers can match natal descriptions, not whether behavior recovers an unknown birth time. Results do not establish such recovery. | **Incompatible as a validated direct method; unresolved as a new empirical hypothesis** | Do not encode rectification lore as a likelihood, prior, rule, or truth label. Any later recovery model is bespoke and must be evaluated blind against declared nulls. | [Carlson 1985](https://doi.org/10.1038/318419a0); [Wyman and Vyse 2008](https://pubmed.ncbi.nlm.nih.gov/18649494/) |
| Uncertain input / interval censoring | Turnbull gives a nonparametric distribution estimate for a population sample observed through grouping, censoring, or truncation. | **Needs adaptation; incompatible for assigning one-person candidate probabilities directly** | Evidence can legitimately define a set or interval of possible inputs. A population censoring estimator does not, by itself, order one person's times or imply uniform mass within a remembered window. | [Turnbull 1976](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1976.tb01597.x) |
| Prior sensitivity | Bayesian conclusions can depend materially on partially specified or misspecified priors; robust Bayesian analysis evaluates ranges or sensitivity rather than hiding the dependence. | **Needs adaptation** | If a future supervised design selects Bayesian inference, it must expose the prior family and report sensitivity. No date, clock-time, duration, source-quality, or chart-state prior is selected here. | [Berger 1990](https://www.sciencedirect.com/science/article/abs/pii/037837589090079A) |
| Probability calibration | Discrimination and calibration are different. Predictions that rank correctly can still be misleading as probabilities, especially after overfitting or population shift. | **Directly reusable as a prohibition; needs adaptation for a future estimator** | Raw chart scores, interval ranks, vote fractions, and duration fractions are not probabilities. Any probability claim requires a separately frozen calibrator and untouched validation data with appropriate diagnostics. | [Van Calster et al. 2019](https://doi.org/10.1186/s12916-019-1466-7) |
| Remembered dates and weekdays | People often reconstruct event dates from within-week information, event sequences, and landmarks rather than retrieving an exact stored date. Confidence and dating strategy may be informative but are not documentary verification. | **Directly reusable for evidence-state design; needs adaptation for inference** | Preserve the independently remembered weekday and dating basis as evidence metadata. Do not auto-correct a date, call agreement verification, or convert confidence/landmarks into weights without separate validation. | [Thompson, Skowronski, and Betz 1993](https://pubmed.ncbi.nlm.nih.gov/8316097/); [Rubinova et al. 2022](https://doi.org/10.1037/mac0000065) |
| Data leakage / double dipping | Selecting, weighting, or sorting on data and then evaluating on the same non-independent data can distort estimates and invalidate inference. | **Directly reusable** | Keep date answers, candidate features, relationship evidence, documented true time, and post-reveal clarifications out of the blind natal-response collector and evaluator. Exploratory relationship-assisted rectification disqualifies that relationship as validation evidence. | [Kriegeskorte et al. 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2841687/) |
| Nested validation and participant grouping | Error estimated with the same cross-validation loop used for tuning is biased; all training choices must occur inside an inner loop and final error in an outer loop or untouched test set. | **Directly reusable** | Split by participant, not answer, probe, relationship, interval, or repeated observation. Feature selection, item selection, model family choice, tuning, calibration, and stopping choices all belong inside development folds. | [Varma and Simon 2006](https://doi.org/10.1186/1471-2105-7-91) |
| Selective / post-selection inference | Ordinary inferential guarantees fail after data-driven model selection unless selection is accounted for; universal protection can be conservative. | **Needs adaptation; directly reusable as a claim boundary** | Post-hoc construct or subgroup discovery remains exploratory. A selected model may be frozen for a new cohort, but success on the data that selected it is not untouched confirmation. | [Berk et al. 2013](https://arxiv.org/abs/1306.1059) |
| Abstention / reject option | Classification can trade coverage for error through an explicit reject option. The optimal rule depends on the loss model and calibrated class information. | **Needs adaptation** | A future system should be allowed to return an unresolved set instead of forced precision. No reject threshold, loss, or participant wording is selected because those require a supervised scientific and product decision plus calibration evidence. | [Chow 1970](https://research.ibm.com/publications/on-optimum-recognition-error-and-reject-tradeoff) |
| Conformal / set-valued prediction | Under the applicable exchangeability and calibration-data conditions, conformal methods can produce prediction sets with marginal coverage, including adaptive sets for unordered labels. | **Needs adaptation; currently unresolved at the expected sample scale** | Set-valued output is conceptually aligned with non-fabricated precision, but a guarantee would require a fixed target, exchangeable untouched calibration participants, participant-level grouping, and enough data. Deterministic candidate completeness is not conformal coverage. | [Romano, Sesia, and Candes 2020](https://papers.nips.cc/paper/2020/hash/244edd7e85dc81602b7615cd705545f5-Abstract.html); [Angelopoulos and Bates 2023](https://arxiv.org/abs/2107.07511) |
| Questionnaire internal consistency | Coefficient alpha depends on assumptions that are frequently violated and is not a general certificate of construct validity or unidimensionality. | **Needs adaptation; alpha-alone use is incompatible** | Evaluate the reliability of each intended construct and response process rather than optimizing alpha. Redundant probes cannot be counted as independent evidence merely because they correlate. No item set or reliability cutoff is selected. | [McNeish 2018](https://pubmed.ncbi.nlm.nih.gov/28557467/) |
| Rater / classifier agreement | Intraclass-correlation forms answer different reliability questions depending on the rater model and whether absolute agreement or consistency is intended. | **Needs adaptation** | Human or LLM coding agreement needs a predeclared unit, rater population, target, and agreement definition. Repeated outputs for one participant are clustered, not independent validation cases. | [Shrout and Fleiss 1979](https://pubmed.ncbi.nlm.nih.gov/18839484/) |
| Privacy-preserving outcome ledger | Removing direct identifiers does not automatically make a release safe; quasi-identifiers, linkage, release context, and repeated releases require risk governance and review. | **Directly reusable for governance; specific privacy mechanism unresolved** | Keep participant-level dates, places, intervals, chart sequences, narratives, and deterministic personal-data hashes private. A future public ledger should prefer non-identifying aggregates or synthetic releases and undergo disclosure review. Tiny-cohort differential privacy is not selected and may have unacceptable utility without an explicit privacy budget and release model. | [NIST SP 800-188](https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance); [NIST Privacy Framework](https://www.nist.gov/privacy-framework) |

## Strongest established baselines for future supervised work

These are comparison obligations, not selections of a model or scoring rule.

1. **Deterministic no-inference baseline:** return the complete unordered set of engine-distinct intervals for every operative date. A proposed inferential layer must never lose the documented true interval because of an enumerator defect or an unstated bucket.
2. **No-pruning behavioral baseline:** after collecting answers, retain the same complete unordered set. A bespoke method must demonstrate improvement over doing nothing inferentially.
3. **Ordinary-information baselines:** compare any date/time recovery signal with declared calendar, month/season, timezone/location, cohort, demographic-if-collected, response-style, and source-quality baselines. These controls must receive the same tuning opportunity as the AstroHD model.
4. **Null chart baselines:** compare with random or permuted participant-to-chart assignment, plausible mismatched charts, and date-only candidate structure. Permutation occurs at participant level and preserves the relevant clustering.
5. **Blinded matching baseline:** conceal candidate identity and the true time from the response collector, coder, adaptive selector, and evaluator until their outputs are frozen. Traditional or model-generated natal interpretations do not count as evidence unless they outperform blinded alternatives out of sample.
6. **Untouched-participant validation:** development, calibration, and final validation roles stay distinct. All adaptive choices are repeated inside participant-level training folds; the final claim uses participants not involved in mapping, item, model, threshold, subgroup, or calibrator selection.
7. **Abstention/set baseline:** compare forced single-window output with the complete candidate set and, only after separate calibration, any set-valued or abstaining method. Coverage, set width, and rejection rate must be reported separately from ranking performance.

## Transfer constraints by project surface

### Evidence intake

The existing immutable source lineage and server-side weekday lock are supported by the temporal-memory evidence: remembered date components may be reconstructed from landmarks and sequences. This supports preserving how an answer was obtained; it does not establish a correction rule. Documentary evidence, independently verified evidence, participant-reported evidence, memory, confidence, and calendar concordance must remain distinct.

### Candidate generation

Classical interval censoring supports representing uncertainty as a set rather than choosing an arbitrary point. It does not justify uniform time mass, duration weighting, or a population distribution for an individual. The deterministic chart-engine partition therefore remains separate from statistical inference.

### Model development and evaluation

Nested validation and anti-circularity results transfer directly. If probes, constructs, feature mappings, models, priors, calibrators, or stopping policies are learned, that entire process is training. Repeated answers, candidate intervals, two partners, and multiple relationships from one person cannot cross participant-level folds. A later claim must also distinguish descriptive matching, date recovery, time-window recovery, and downstream relationship prediction.

### Uncertainty output

Ranking, calibrated probability, conformal coverage, and abstention are different outputs. A rank is not a probability; a candidate-complete set is not a confidence set; conformal marginal coverage is not per-person certainty; an abstention threshold is not scientifically neutral. Selecting any of these semantics remains blocked pending a new Pro supervision checkpoint.

### Public evidence accumulation

The current synthetic allowlist is safer than publishing detailed deidentified participant rows. Exact birth facts, rare timezone histories, chart-state sequences, relationship linkages, and deterministic hashes can be quasi-identifying in combination. A future ledger needs a declared release purpose, threat model, aggregation rules, disclosure review, revision/version policy, and separation between private audit records and public evidence. This scan does not select differential privacy, k-anonymity, suppression levels, or release thresholds.

## Unresolved questions returned to supervision

- What target, if any, should a later natal model predict: exact engine interval, equivalence class, candidate set, pairwise ordering, or another predeclared object?
- Is the feasible participant count sufficient for separate development, calibration, and untouched validation, especially for participant-level conformal or abstention guarantees?
- Which self-report constructs have test-retest, inter-rater, and predictive reliability adequate for out-of-sample use?
- What non-HD baselines can be measured without collecting privacy-expanding demographics or revealing calendar information?
- If priors are considered, which external population evidence could justify them, and what sensitivity family would be mandatory?
- What public aggregation granularity remains useful after small-cell and linkage-risk review?
- Does any blinded natal signal exist after the strongest ordinary-information and permutation controls? If not, the correct scientific output is the deterministic unresolved candidate set.

No question above is answered by the deterministic conformance work, and none authorizes inferential implementation.
