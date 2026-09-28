# Empirical Astrology End-to-End Evidence Report

Date: 2026-09-28

Branch: `worker/empirical-astrology-end-to-end`

Status: complete development-evidence pass; not prospective validation

## Executive conclusion

The end-to-end pass reached normalization, publication-level deduplication, dataset-lineage reconciliation, complete A-priority acquisition triage, original-full-text reading, feature-level extraction, 2021–2026 screening, candidate/constraint registries, and an implementable development specification.

The dominant result is constraint, not a validated feature set. The most rigorous blinded tests, large administrative relationship datasets and large modern personality datasets are null at practically useful scales. Several positive claims remain scientifically interesting, but none is both precisely reconstructable and independently replicated strongly enough to receive a nonzero production weight. The next algorithm should therefore be a prospective hypothesis-discrimination instrument: theory-neutral primary design, tightly limited preregistered secondary moderators, complete provenance, and untouched held-out replication.

## 1. Corpus and evidence counts

| Measure | Final count | Interpretation |
|---|---:|---|
| Wave 1 feature records processed | **1,248** | Every source row preserved verbatim inside the normalized record with worker/file/line/hash provenance |
| Unique source documents | **913** | 901 Wave 1-origin canonical publications plus 12 targeted additions; feature-specific titles from the same physical publication collapsed |
| Empirical source documents | **795** | Commentary/review-only documents separately flagged |
| Canonical dataset/cohort units | **965** | Conservative operational units; uncertain units remain separate rather than being over-merged |
| Likely independent replication relations identifiable | **69** | Identifiable from the corpus; not all are high quality or confirmatory |
| Original/fullest texts retrieved and read | **14** | 13 A-priority originals/reanalyses plus one C-priority synthetic preprint used only as a negative evidence-class constraint |
| Primary feature-level extraction rows | **49** | All required fields present; secondary syntheses labelled, not presented as primary results |
| Actively resolved sources | **577** | Every final A source (502), 74 highest-value B sources, and the already-obtained 2026 preprint |
| Still missing or unverified among active targets | **563** | Includes abstract/landing/PDF candidates that were not actually read |
| Missing A-priority full texts | **489** | Durable source-by-source continuation queue created |
| Queue A / B / C / D | **502 / 220 / 92 / 99** | 913 canonical source documents total |
| Candidate-feature registry rows | **8** | None assigned a nonzero production weight |
| Negative-constraint registry rows | **15** | Design, feature, accounting and safety constraints |
| Verified publication-alias groups collapsed | **25** | 36 inflated source identities removed while retaining all feature rows |
| Chapter 7/8 reconciliation relations | **28** | Includes direct same-source, explicit cross-reference, likely-duplicate and alias relations; eight final source documents directly span both chapters |

The full-text “missing” count is a count of actively searched targets, not a claim that all 913 sources should have been indiscriminately acquired. Lower-priority C/D commentary and low-information historical papers were intentionally not all retrieved.

## 2. What was produced

### Master data

- `normalized_feature_records.jsonl`: all 1,248 original records plus canonical source/dataset/family IDs, original line hash and preserved direction.
- `source_registry.jsonl`: publication-level identities, empirical/review roles, priorities, chapter coverage, conflicts and current additions.
- `dataset_registry.jsonl`: cohort units, source reuse, sample/population/time-quality metadata and independence notes.
- `duplicate_reanalysis_map.jsonl`: same-publication aliases, same-cohort publications, reanalyses, independent-replication relations and Chapter 7/8 reconciliation.
- `fulltext_queue.jsonl` and `fulltext_queue.md`: complete A/B/C/D queue ordered by information value, not positivity.

### Original-source layer

- `fulltext_manifest.jsonl`: 577 acquisition records with exact citation, URL, status, provenance, role, inspected sections and read-copy hash where applicable.
- `missing_fulltexts.md`: all 563 unresolved targets with candidate URLs/statuses and a clear legal-access boundary.
- `primary_feature_extractions.jsonl`: 49 exact claims from read originals, including nulls, raw counts, p/Bayes information, operational definitions, lineage and risk notes.

### Decision layer

- `evidence_map.md`: programme-by-programme synthesis with dataset independence and feature status.
- `candidate_feature_registry.jsonl`: eight reconstructable or potentially reconstructable hypotheses.
- `negative_constraint_registry.jsonl`: fifteen exclusions and mandatory design controls.
- `literature_derived_algorithm_spec.md`: the prospective development algorithm, astronomical feature contract, controls, ablations and held-out criteria.

No original Wave 1 file was edited.

## 3. Normalization and canonicalization results

Wave 1 preserved direction exactly: no null, opposite, mixed or nonempirical label was rewritten to make a narrative cleaner. Missing statistics remain missing. Canonical fields were filled only where a citation, DOI, URL or retrieved original supported them.

The first deterministic pass produced 937 apparent source documents. Original-text inspection and bibliographic reconciliation showed that several were feature-specific titles for one physical publication. Examples include:

- five Lu et al. study rows → one 2020 JPSP article, while its distinct study datasets remain distinct;
- seven Dean–Kelly outcome rows → one 2003 JCS publication and one NCDS cohort;
- two Carlson feature rows → one 1985 Nature paper;
- two Startup aspect rows → one 1984 thesis cohort; the 1985 article remains a separate publication but the same dataset;
- two Rajopadhye rows → one 2021 article;
- repeated thesis/article feature titles for Niehenke, Noblitt, Gaynor, Blackmore, Martindale and others.

Twenty-five verified alias groups removed 36 false source identities, yielding 901 Wave 1-origin documents. Twelve targeted current/reanalysis sources were added, giving 913 final documents.

The 965 dataset/cohort units are deliberately conservative. Some are outcome-specific subsets of a larger cohort and low-certainty historical identities cannot be safely merged without originals. Each carries an identity-certainty field. This avoids the more damaging error of declaring distinct samples identical, while reuse relations identify known shared cohorts.

## 4. Chapter 7 / Chapter 8 reconciliation

Chapter 8 frequently summarizes or re-labels Chapter 7 material. Reconciliation used four auditable mechanisms:

1. exact or near-exact publication canonicalization;
2. explicit Chapter 8 references back to a Chapter 7 section;
3. conservative author/year/title links for Wave 1 rows already flagged as reuse;
4. original-text publication alias verification.

The relation map contains 28 Chapter 7/8-flagged relations. Eight final source documents directly contain both chapter coverages; the remaining relations preserve cross-source references where the abbreviated Chapter 8 citation was insufficient for a destructive merge. Chapter repetition is never counted as replication.

## 5. Full-text acquisition outcome

Every final A-priority source was run through the public/legal resolver; the next 74 B sources were also attempted. Search order followed publisher/journal, author/institutional repository, legitimate archive, dissertation repository and existing project links. No purchase or access-control bypass was used.

Fourteen fullest available texts were read:

1. Carlson 1985, double-blind matching;
2. McGrew–McFall 1990, Indiana chart matching;
3. Bhandary et al. 2018, Vedic mental-illness judgments;
4. Helgertz–Scott 2020, Swedish marriage/divorce registers;
5. Lu et al. 2020, stereotypes, personality and discrimination;
6. Mayo–White–Eysenck 1978, signs and personality;
7. Voas 2007, ten million marriages;
8. Oshop–Foss 2015, Twitter prominence and Vedic karakas;
9. Rajopadhye et al. 2021, 68 Vedic rule aggregates;
10. Startup 1984, complete 338-page thesis;
11. Ertel–Irving 1997, Mars-effect selection reanalysis;
12. Dean–Kelly 2003, NCDS time twins and matching synthesis;
13. French–Leadbetter–Dean 1997, complete public HTML reanalysis;
14. Samantaray et al. 2026, synthetic ML demonstration.

PDFs were searched and extracted locally; relevant scan/table/method pages were visually inspected. Read-copy SHA-256 values and exact inspected sections are in the manifest. Read copies were not committed merely to inflate deliverables or redistribute source files.

The remaining 563 targets were not collapsed into a generic “unavailable” label. Their status distinguishes no candidate, unverified landing/registry candidate, unverified PDF candidate, abstract-only, and issue-index-only.

## 6. Most promising candidate signals

“Promising” here means worth a clean prospective test, not likely true and not production-ready.

### 6.1 Vedic AtmaKaraka–PutraKaraka kendra rule

Oshop–Foss reported 60/84 selected high-profile Twitter users versus 3025/5460=55.4029% in permuted charts, Fisher one-sided p=.00205; secondary follower regressions were p=.043 and p=.017. The exact rule is reconstructable: sidereal Lahiri, mean nodes, highest- and sixth-highest within-sign degree, kendra relation in D1 or D9. It is one selected cohort with severe coverage/ascertainment risks and no independent replication. Status: `promising_requires_replication`.

### 6.2 Applying versus separating orb asymmetry

A 2022 publisher abstract reports no consistent tight-versus-wide effect across four >50,000-chart applications but suggests applying aspects can use maximum orbs 1–2° wider than separating aspects. Exact outcomes and controls are unavailable. Status: `promising_requires_replication`, allowed only as a secondary interaction after the full text is recovered.

### 6.3 Adjusted planetary dominance

A 2023 abstract describes an independent N=61 biography replication with p=3.2e-05, r=.51. Exact scoring, biography labels, blinding, semantic pipeline and multiplicity are unavailable. Status: `definition_uncertain`; no implementation until reconstructed from the original.

### 6.4 Southern Hemisphere sign inversion

A 2026 abstract reports N=141 and a large north/south difference under sign inversion (70.5% versus 35.6%, p≈1.62e-5, h≈.72). Public-figure selection and a tunable semantic pipeline make independent replication essential. Status: `promising_requires_replication`.

### 6.5 Gauquelin key sectors

The historical programme remains the largest claimed signal family, but it is not one stable feature and papers repeatedly reuse the same samples. Selection, eminence and control-generation disputes block an evidence weight. Status: `definition_uncertain`; only a completely independent preregistered programme replication can move it.

No candidate qualifies as a verified `replicated_candidate` for this project.

## 7. Strongest negative constraints

### 7.1 Sun-sign personality

Lu et al. N=173,709 found no sign effects on four Big Five traits, Bayes factors B10<.001; a raw extraversion association disappeared after season control. N=32,878 employee performance was also null. Historical Mayo effects are small and strongly exposed to self-selection/prior knowledge. Do not use Sun sign as a personality or employment feature.

### 7.2 Sun-sign relationships

Voas adjusted 9,500,773 England/Wales marriages after diagnosing a 22,100-pair response/imputation artifact. Helgertz–Scott independently analysed 66,063 Swedish marriages and 46,326 divorce histories. Neither supports a useful compatibility rule. Do not use Sun-sign love scores.

### 7.3 Whole-chart blind matching

Carlson Part 2 was 0.34 correct against chance 1/3; the Indiana astrologers scored 0–3/23, median 1, with confidence r=.03 and mean pair agreement 1.4/23. The broader synthesis reports ES=.051, p=.66. Do not use human-reader confidence, intuition or chart matching as a model weight.

### 7.4 Broad time-twin similarity

The NCDS N=2,101 cohort produced mean r=-.003 and 5/110 p<.05 versus 5.5 expected. The Roberts–Greengrass reanalysis produced r=-.001 and showed the claimed trend was sensitive to bins/models. Do not assume broad whole-chart similarity from close birth time.

### 7.5 Generic aspects/harmonics

Startup’s four analyses in N=911 did not support astrologer-specified aspect traits, hard/soft divisions, a 108th harmonic or continuous separation; 3/32 nominal results had family probability .21. Generic aspect weights are excluded. Tightness/angularity remain secondary moderators only.

### 7.6 Method and safety

Prior astrology knowledge can cause measurable discrimination (Virgo-label hireability d=-.29) without actual trait differences. Multiplicity, astronomical/demographic base rates, birth-time precision, low reader reliability, dataset reuse and development/validation separation are mandatory constraints. Clinical, violence, mortality and hiring scores are hard safety exclusions.

## 8. Major dataset-reuse problems

- **Gauquelin/CSICOP/CFEPP:** primary papers, replications and reanalyses often reuse athlete/profession records while changing inclusion, eminence or controls.
- **Roberts–Greengrass:** French et al. is a reanalysis of the same 128 people, not a replication.
- **NCDS:** many outcomes from one 2,101-person cohort are one cohort, not 110 studies.
- **Indiana/Mull/McGrew–McFall:** different publications report the same 23 cases.
- **Startup:** thesis chapters and the 1985 article reuse one N=911 cohort.
- **Lu et al.:** one publication contains multiple genuinely distinct studies; publication deduplication must not mistakenly merge their cohorts.
- **Rajopadhye programme:** celebrity, intelligence, longevity and relationship reports may be separate cohorts, but references within one paper do not add evidence until the original paper/dataset is identified.
- **Gauquelin marriage/synastry derivatives:** multiple feature papers can reuse the same couple registry.

The relation map encodes these distinctions so a future meta-analysis cannot weight papers as independent samples.

## 9. Post-2020 additions

Twelve targeted sources absent from the final Wave 1 canonical set were added to source, dataset, queue and manifest layers. They include 2021 synastry/SIDS/five-degree items, the 2022 orb paper, the 2023 adjusted-dominance replication, the 2024 twelve-model comparison, a 2025 Pluto/cancer item, and 2026 primary-directions, hemisphere, violence-aspect and ML papers.

Only the 2026 ML preprint was available as a full text in the current-source set; it is synthetic and does not count as real-world feature evidence. Four high-value Correlation claims had public abstracts with useful sample/effect statements, but none was converted into primary feature evidence. Remaining current items are in the missing queue.

## 10. Highest-value unresolved claims

In priority order:

1. exact Tarvainen 2022 applying/separating aspect definitions, outcomes and corrections;
2. Godbout–Coron adjusted planetary-dominance scoring, biography coding and pipeline-level permutations;
3. independent records and exact sector/control definitions across the Gauquelin chain;
4. Westran 2021 progressed-synastry N=1,300 cohort identity and preregistration status;
5. Daigno 2026 orbs, controls, record quality, multiplicity and cohort duplication;
6. Godbout–Brun 2026 semantic pipeline, trait labels and north/south sampling;
7. Addey/Vail/Pottenger exact astronomical baseline and harmonic/orb originals;
8. high-dimensional McDonough/Bergen discovery-versus-holdout histories;
9. exact independent replication status for occupation/eminence samples;
10. original methods for prediction, rectification, horary and transit claims now known mainly through reviews.

These are unresolved because of missing originals or definition/lineage uncertainty, not because their abstracts were negative or positive.

## 11. What should enter the next algorithm version

Only the research machinery and narrow prospective hypotheses should enter:

1. theory-neutral same-hospital/near-time birth distance as the primary predictor;
2. conventional site/date/time/cohort controls and a control generator preserving astronomical/demographic base rates;
3. one pre-frozen personality outcome and one pre-frozen similarity metric;
4. a very small pre-frozen aspect-to-trait mapping set;
5. continuous orb distance, applying/separating and angularity as secondary moderators only;
6. birth-time uncertainty propagation/exclusion;
7. belief/sign-knowledge/prior-reading measurement;
8. complete feature manifest, dataset lineage, multiplicity correction, nested selection, ablation and held-out replication.

Every literature-derived coefficient starts at zero. The Oshop–Foss rule can be reproduced in a separate prominence experiment, not smuggled into the personality model. Definition-uncertain recent claims stay blocked until their full texts and codebooks are recovered.

## 12. What must explicitly not enter

- Sun-sign personality or employment weights;
- Sun-sign relationship compatibility;
- human-reader confidence, intuition or client acceptance;
- generic hard/soft or aspect/no-aspect weights;
- a 108th-harmonic personality feature;
- uncorrected nominal discoveries from large scans;
- a broad “same chart means same person” score;
- Vedic clinical/violence/mortality/hiring features;
- the 21-rule/68-parameter celebrity aggregate;
- any feature whose only support is a review or abstract;
- any evidence multiplier based on number of papers rather than independent cohorts;
- any retrospective optimization on the user’s known chart or life events.

## 13. Most efficient prospective experiments

### Experiment A — same-hospital near-time personality

Primary test: whether personality-profile distance increases with birth-time distance inside hospital/date blocks. Use recorded times, one frozen instrument, cluster-aware estimation, locally preserving permutations and an untouched future cohort. This directly discriminates broad chart-similarity claims while minimizing demographic/time confounding.

### Experiment B — frozen aspect moderators

Before outcomes, freeze planet pairs, aspect angles, aspect-to-trait directions, orbs, applying/separating calculation and angularity distance. Treat all as a named secondary family. Compare no-astrology, time-distance, mapped-aspect, and moderator models; repeat feature selection under null permutations. Replicate without retuning.

### Experiment C — exact Oshop–Foss replication

Reproduce the original D1/D9 karaka count first. Then define a public-figure sampling frame before birth-time availability is checked, use coverage weighting, freeze Lahiri/node/navāṃśa settings, and test a second independent cohort. The primary result is the binary rule; follower regressions are secondary.

### Experiment D — recent computational-claim audit

After recovering the Godbout–Coron and hemisphere full texts, independently implement the complete semantic pipeline, blind trait coders to charts/hemisphere, run pipeline-level permutations and keep one cohort untouched. This efficiently tests whether the large abstract-reported effects survive leakage and tuning controls.

### Experiment E — clean Gauquelin programme replication

Use a new jurisdiction’s civil records, fixed occupations and eminence cutoffs, complete inclusion logs, exact sector geometry and preregistered demographic/time controls. Discovery and replication jurisdictions must be separate. This is expensive, so it ranks after Experiments A–D unless independent data access already exists.

## 14. Completion and limitations

This task did not stop at a plan, deduplication pass, example papers or a partial review. It produced every specified master/full-text/report artifact and continued despite inaccessible papers.

Limitations are explicit:

- 489 A-priority originals remain missing/unverified despite active public/legal resolution;
- many historical Wave 1 claims remain review-derived and must not be promoted to primary evidence;
- dataset identity is uncertain for some old or abbreviated citations;
- the current-source search is strongest for Correlation/JSE/public repositories and may miss non-indexed theses or society archives;
- the 69 independent-replication relations are corpus identifiers, not 69 successful replications;
- no historical result is prospective validation for this project.

The durable next step is not more retrospective scoring. It is recovery of the highest-value missing originals while the preregistered same-hospital/near-time experiment is implemented exactly as specified in `literature_derived_algorithm_spec.md`.
