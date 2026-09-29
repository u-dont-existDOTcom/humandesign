# Pro decision after the Correlation archive audit

Date: 2026-09-29

Gate: `empirical-astrology-post-correlation-pro-gate-v1-20260929`

Reviewed evidence: `9566ceb1d3578b6a181568e23422f7c913ad351c`

Scientific model retained: `literature_model_v1.0.0-wave3b-reaffirmed-20260928`

Prospective protocol retained: `same-hospital-personality-protocol-v1b-20260928`

## Decision

**Reaffirm the scientific model and prospective protocol; correct the evidence rationale and cohort accounting; activate no astrology feature. Preserve the implementation-acceptance and prospective-launch holds.**

This is a new, append-only Pro decision record, not a new fitted model. Full-text access materially improves what can be adjudicated. It removes “abstract only” as the reason to defer several candidates, establishes a real new-person test of planetary dominance, reveals a specific shared-chart problem in that test's target construction, and confirms numerical inconsistencies in the southern-hemisphere paper. None of these changes supplies an independently measured, reproducible chart-to-personality mapping for the frozen model.

This decision is narrower than “astrology has been disproved.” It also does not mean “the positive studies are just multiple testing.” The most interesting new-person result remains statistically unusual under its published assumptions after a nine-endpoint correction. The unresolved question is whether those assumptions test the claimed human association rather than agreement inside a chart-conditioned measurement system.

The machine-readable authority is `reference/empirical_astrology/literature_model_v1b_post_correlation_gate.json`. It supersedes conflicting historical source identities, access claims, overlap labels and candidate rationales only. Historical decisions, model bytes, executable specifications and results remain unchanged. In particular, the old v1b `REG-001` identification of the inversion paper is no longer operative; preserving that file as history is not endorsement of its superseded citation.

## Review boundary and evidential units

All 25 requested articles and both adjacent sources were reviewed through the supplied complete-source audit and the 27-entry repository packet. All 25 distinct issue/author-copy PDF fingerprints were checked against the owner's archive and matched. The 27 article entries correspond to 28 appended extraction rows because Daigno's two cohorts have separate rows. The complete extraction registry has 90 rows. These are document-management counts, **not independent-study or independent-person counts**.

This review additionally reopened the dominance training methods, all nine replication table cells, the replication participant roster, the inversion methods and southern roster, and the inversion arithmetic/orientation examples. The decisive tables were visually inspected as rendered original pages; their problems are not inferred from unreliable OCR. Most older-study detail remains grounded in the evidence worker's full-text audit, not a claimed second exhaustive extraction of every table in all 27 articles.

No owner-known outcomes, prospective responses, secret answer keys or person-level development results were examined. No new human associations were estimated. The accompanying arithmetic is a calculation from printed aggregate numbers, not a reconstruction of the studies' individual records. A small synthetic counterexample tests a logical inference, not astrology. Paid originals and full-issue extracted text remain outside Git.

The article-by-article dispositions, partial cohort graph and reproducible arithmetic accompany this decision. The supplied audit's favorable and unfavorable results remain attached to each source; this decision does not replace that ledger with a selection of convenient examples.

## 1. Robustness: what the recovered originals actually establish

### Planetary dominance: real new-person evidence, but a chart-conditioned target

Godbout and Coron's replication paper reports 61 people different from the 189 used to build the seven-factor model. It describes a surname-A Astro-Databank selection, AA/A records, exclusion of rounded full-hour times, and the same biography-analysis procedure as the training study. This deserves credit as a **new-person test of an inherited pipeline**. Neither common authors nor common software, by itself, cancels that credit. The 2024 comparison uses the original 189 plus these same 61, however, so it is not a third sample. [Sources: Correlation 36(1), 2023, pp.49–53; 35(2), 2023, pp.11–25; archive audit items 22–23.]

The training original makes the central measurement issue more precise than the handoff's general reference to semantic leakage. Its “biographical dominance” is **not a label constructed from biography alone**. For each person, Mastro takes that person's chart, produces ten alternative portraits by tripling each candidate planet in turn, and ranks those portraits by their match to the person's extracted biography words. The target therefore depends on both chart and biography. The compact seven-factor predictor is another function of the same chart. [Source: 35(2), 2023, printed pp.17–21, especially the target construction on pp.17–18 and normalization on p.21.]

Write the prediction as `f(C)` and the target as `g(C,B)`, where `C` is the chart and `B` the biography. Agreement between them can reflect biography-specific information, but it can also reflect their shared dependence on `C`. Shuffling already-finished target labels across people breaks that shared-chart structure. It does not, by itself, answer whether the genuine biography matches its own chart better than an appropriately comparable wrong biography.

A counterexample establishes the inference gap: suppose `g(C,B)` always selects the chart's most prominent planet, regardless of `B`, and `f(C)` does the same. Their agreement is perfect on new people despite zero biography information. Shuffling finished labels makes agreement fall toward chance; swapping biographies and regenerating `g` does not. This is a logical counterexample to the adequacy of output-only shuffling, **not a claim that the published software has exactly this defect or that its entire signal is artificial**.

The minimal direct audit is to preserve each chart, reassign appropriately comparable biographies, regenerate the ten chart-conditioned targets, and score the frozen predictor against them. Person-level profiles, candidate/tie handling and complete software are needed. A separately measured trait endpoint is needed before this becomes evidence for a chart-to-personality map rather than an internal dominance target. No such result is available in this packet.

The 2023 and 2026 pipelines must also remain distinct. The 2023 target uses extracted/cleaned published biographies; ChatGPT's illustrated prose comparison is not evidence that it generated those primary labels. The 2026 inversion paper does generate its primary biographical nouns by prompting ChatGPT with the person's name. The scoring denominators differ, too: total portrait score in the 2023 target versus the number of astrological words in the 2026 chart score. They are not interchangeable replications of one measurement.

### Southern-hemisphere inversion: the aggregate statistic is not the unresolved arithmetic

The direct source is Godbout and Brun, *Correlation* **38(1), issue dated 2026, pp.39–56**. Preserve the discrepancy that the publisher abstract labels it 2025. The 2024 **37(1), pp.73–84** article concerns German zodiac-book sales and is not this test. [Sources: archive audit items 24 and adjacent comparator; direct original.]

The inversion paper reports 48 of 68 southern subjects and 26 of 73 northern subjects favoring inversion. Those counts give the reported strong north–south contrast under the stated two-proportion calculation. Recomputing that arithmetic does not establish that the 141 underlying decisions were correctly generated.

| Example in the original | Non-inverted score | Inverted score | Printed difference | Inverted minus non-inverted |
|---|---:|---:|---:|---:|
| Allende, Table 1, p.47 | .9989 | .9425 | +.0456 | **−.0564** |
| Anitta, Table 1, p.47 | .3616 | .9617 | +.0201 | **+.6001** |
| Musk, Table 4, p.50 | .3170 | .3329 | +.1108 | **+.0159** |

Figure 6 on p.49 labels the June-28 Sun Capricorn in the non-inverted column and Cancer in the inverted column, while the next page's prose identifies Capricorn as inverted. This is an internal orientation contradiction even before an independent ephemeris calculation.

These failures require the full original/inverted score pairs, denominators, tie rules, chart orientation and executable settings. They do **not** justify silently correcting the headline by one case, assuming a global column reversal, assuming harmless typesetting, or declaring the aggregate effect false. The appropriate result is **reported contrast, reproduction unresolved**.

Even after correction, a 50/50 success probability does not follow merely from comparing two chart versions. Different lexical outputs and word-count normalizations can favor one version under nonmatching biographies. The northern group is useful but unmatched in ascertainment, geography, history and biography construction. A defensible semantic null and identity-independent measurement remain necessary. Both reported latitude-distance failures must remain visible.

The paired inversion is a test of a **combined expert-system transformation**, not an isolated causal effect of zodiac signs. The paper's joint sign/aspect vocabulary and retained midpoints do not make that paired transformation meaningless; they limit what a positive result would mean. [Source: direct original, pp.42–50.]

### Tightness, applying status, sectors and case-ascertained findings

Tarvainen's 2022 paper brings four applications into view, not four new independently concordant tests of one fixed modifier. The mathematician and theologian data are reused and date-only; the two parental analyses concern paired spouses. Tightness is not consistent across the examples, and the female applying/separating comparison reverses the male direction. This does not support a universal tighter-is-stronger coefficient or a transferable one-/two-degree applying allowance. [Audit items 12–15 and 21.]

The older Gauquelin aspect null and Ertel aspect-window null are relevant negatives for the settings they tested, not proofs that all aspects are inert and not new confirmations of sectors. The 1995 time-precision direction contradicts the proposed monotonic precision improvement; it does not identify why. Dean's trait-expectancy critique shows why repeated mentions cannot stand in for independent persons. Brady's strong firstborn nodding result must travel with its failed Gauquelin-family comparison. [Audit items 2, 4, 6, 8–9.]

Daigno's Mercury–Mars conjunction result is present in two case-ascertained sources and meets the paper's stated eight-test threshold. That is positive aggregate evidence worth retaining. It does not fix event-denominator dependence, unmatched calendar-day controls, case ascertainment, noon-imputed dates or failed temporal subsets. Ruis 2012 reuses the 2008 people; Currey reuses Press's cases and controls. None earns a personality feature, clinical rule or forensic inference. [Audit items 10–11, 19, 25.]

No case-level cluster-adjusted confidence interval can be honestly reconstructed from the supplied aggregate counts alone. Missing such an analysis is not an estimated null result.

## 2. Ablations: distinguish informative comparisons from fresh confirmation

The selected house-cusp shift in 2021, the 2013/2015/2022 orb curves, and the 2024 twelve-model dominance comparison describe performance on reused or outcome-inspected records. They can identify candidate settings and diagnose sensitivity; they do not validate their selected settings on untouched people. The same applies to a favorable subgroup found after a pooled or predeclared family fails.

Conversely, finding one unsuccessful endpoint does not automatically cancel a different predeclared successful endpoint. The dominance paper's rank-three/three-try failure must be reported, but the remaining results are not erased by a rule that all nine had to succeed unless that conjunction was actually the declared target. The frozen prospective A/B study is different: its contract explicitly requires **both** cohorts to pass, so either failure prevents the replicated-success label.

No executable astrology feature is present in v1b. Removing one is therefore `NOT_APPLICABLE_NO_INCLUDED_FEATURE`, not an estimated zero, a failed ablation, or an additional piece of corroboration. Aspect/orb tightness, applying status and angularity remain inactive secondary templates.

## 3. Nulls and leakage: the necessary replay, not an unnecessarily expensive substitute

For dominance, the wrong-biography audit must preserve the shared chart while regenerating every target stage affected by the biography reassignment. Shuffling finished targets is not equivalent. The original 189-person shuffled expectation cannot simply be assumed to calibrate the 61-person sample's actual rank, tie, vocabulary and candidate distribution.

There are two different inferential tasks. A **development whole-search test** reruns feature screening, coefficient selection, endpoint selection and all affected coding decisions inside each null replicate. A **genuinely untouched test of a frozen model** keeps its previously fixed coefficients and definitions fixed. Charging all training searches again to such a validation is not necessary merely because training occurred; verifying the freeze and accounting for choices actually made on the validation data is necessary.

Likewise, “full pipeline” does not mean paying to regenerate an unchanged stochastic GPT profile in every permutation. A profile genuinely frozen independently of the reassigned chart may be conditioned on. Stages influenced by the randomized assignment must be rerun. If names, chart facts, geography or adaptive prompting influenced target generation, that dependency must be modeled or removed; a finished-profile permutation cannot prove the absence of identity/world-knowledge leakage. Masked independent biographies or independently collected traits address a different, necessary measurement question.

Use nulls matched to the question and plausible exchangeability structure: language, era, profession, fame/biography length, geographic ascertainment and known person/family dependence. An arbitrary global birthday shuffle, generic equal-probability planet draw, or unmatched random word bag is not automatically valid. Random-word controls can be useful diagnostics when length and lexical frequencies are preserved, but they do not replace person-matched biography controls.

The accompanying reproduction specification states the minimum missing artifacts and these separate tests. It authorizes no new participant collection or external purchase/contact.

## 4. Multiplicity: a correction that does not erase the strongest signal

All nine dominance settings were visually transcribed from the original Tables 2–4. The following are deterministic recalculations of the **published** p-values:

| Maximum biography rank | Model tries | Successes/61 | Published p | Holm-adjusted p across nine |
|---:|---:|---:|---:|---:|
| 1 | 1 | 13 | .00372 | .01860 |
| 1 | 2 | 24 | .000152 | .001216 |
| 1 | 3 | 29 | .00274 | .01644 |
| 2 | 1 | 23 | .000961 | .006727 |
| 2 | 2 | 39 | .0000317 | **.0002853** |
| 2 | 3 | 43 | .00624 | .01872 |
| 3 | 1 | 29 | .00432 | .01860 |
| 3 | 2 | 42 | .0135 | .02700 |
| 3 | 3 | 47 | .182 | .18200 |

Eight of nine remain below .05 with Holm; six survive the simpler ninefold Bonferroni adjustment. An exact-binomial sensitivity treating each **rounded, training-derived** chance probability as a fixed constant also leaves eight below .05 after Holm; its smallest adjusted p is approximately .000643613. That sensitivity is not an independently validated binomial null. The original third-rank/third-try table has 47 observed versus 43.8 expected; contradictory nearby prose is not used as an alternative dataset.

Thus the disposition is not “nine tests explain it away.” Multiplicity corrections control their intended error family only when the individual p-values and null are valid. The shared-chart target, transferred chance probabilities and absent source-level replay are the substantive outstanding issues. Small p-values do not estimate the probability that astrology is true or that this target measures independent personality.

For the wider literature, count the actual endpoint, selection and reuse structure: 42→18→7 development selection, rank/try alternatives, twelve models, Brady's 338 comparisons, aspect/orb/house scans, Daigno's eight aspects and temporal subdivisions. Do not manufacture a precise universal correction by multiplying each p-value by the number of articles, and do not combine dependent selected p-values into a meta-analytic success claim without the required joint information.

## 5. Cohort reuse: a new directly verified overlap

The source-reported relationships include Dean's shared 1,198-person parent frame; repeated Gauquelin profession and family series; the exact 20,394-person ruler cohort in 2018/2021; Ruis's repeated 77+216; Press/Currey's repeated 311+311; and the dominance sequence 189 training → 61 new people → 250 reused people. These are linked analyses, not a succession of independent populations.

A further overlap was directly verified during this review: **Salvador Allende and Claudio Arrau** appear in both the 2023 replication's 61-person Table 1 and the 2026 inversion study's 68-person southern Figure 2. The handoff's suggestion that all 68 southern people are new relative to the earlier research is therefore too strong. At least two are reused. The 73 northern people are already known to be reused; their GPT word profiles are newly generated, which does not restore person independence. [Sources: 36(1), 2023, p.50; 38(1), 2026, p.42.]

The accompanying graph identifies these two person-level witnesses and distinguishes exact same-cohort, subset, partial, removed-duplicate and unknown intersections. It is **not a completed participant-level deduplication of every study**. The full 189/61/141 intersections, many historical profession/family edges, and Ruis-versus-Daigno/Wikidata intersections remain unavailable. Unknown overlap must not be silently coded as zero. The failure to obtain a complete graph is explicitly an unresolved evidence item, not a reason to invent an independent replication count.

## 6. Model/version adjudication

| Family | Current decision after the archive review |
|---|---|
| CF-001, prominence/karaka-kendra | Original-domain exploration only; no direct new exact replication in this batch. |
| CF-002, tightness/applying | Original-domain exploration only; no executable modifier or cross-domain transfer. |
| CF-003, adjusted dominance | Excluded from the personality model; retain the new-person result and prioritize source/null reproduction. |
| CF-004, southern inversion | Excluded; direct source now identified, aggregate reproduction and measurement unresolved. |
| CF-005, violence and related case series | Aggregate methodological audit only; categorical clinical/forensic/person-level exclusion retained. |
| CF-006, sectors | Profession/eminence exploration only; distinguish aspects, sectors and repeated cohorts. |
| CF-007, personality aspect/angular moderators | Secondary templates remain inactive; no exact trait mapping newly justified. |
| CF-008, clinical reader inference | Excluded; no responsive new exact validation in these 25 originals. |

The executable astrology feature list, aspect-to-trait map and moderator interaction list remain empty; astrology weights remain `{}` and the astrology coefficient vector has length zero. Full v1b remains identical to the theory-neutral model. No v1c science version is warranted by this packet.

A new **evidence gate** is warranted because source access, identity, mathematical checks, target construction and participant overlap changed. Updating those reasons is essential even when the inclusion decision remains the same. The machine-readable overrides make that distinction explicit rather than leaving obsolete “abstract only” text as the current justification.

## 7. Prospective specification and operational boundary

The exact v1b prospective specification is reaffirmed by path, version and SHA-256, not silently rewritten. It fixes the endpoint and scoring key, elapsed-time exposure and nuisance terms, birth-record quality, site/date matching and pair selection, independent cluster unit, multiplicity, exclusions, sample and conditional-power assumptions, seeds, software/freeze hashes, stopping, blinding, failure rules and the A/B conjunction. Operational identities and approvals still have to be supplied and independently checked; a scientific specification is not a completed launch package.

Each cohort remains 20 independent networks with 100 disjoint pairs per hospital/network, a fixed English IPIP-50 distance endpoint, the prescribed conventional controls, clustered inference and all fixed diagnostics/sensitivities. No favorable secondary result or pooled A+B analysis rescues a failed primary cohort. In the absence of data, status remains `NOT_EVALUATED`, not a measured zero or a failed hypothesis.

The prior specification already excludes multiple-birth records, limits participation to one person per known family/household/relationship component, matches delivery mode, includes clock-time nuisance terms, uses disjoint pairs and handles clustering at the independent-network level. Every eligible birth gap is at most 180 minutes. These protections were verified in the frozen specification; this is not a claim that their implementation has passed the outstanding Wave 4 checks.

Tarvainen's 2018 synthetic counterexample is relevant to sensitivity of one serial-correlation method under one injected pulse. It is not evidence from Dean's real participants and supplies no positive TN-001 estimate. Even a future replicated TN-001 association would not identify a celestial mechanism, validate astrology generally, establish a chart-to-trait map or justify individual predictions.

The pre-existing Wave 4 implementation findings W4-F01 through W4-F07 and the broader integration/feasibility requirements have **not been repaired or accepted by this archive review**. The previous gate remains controlling for implementation and launch. Its authorized mechanical repair and outcome-blind feasibility work can continue without feature search. No recruitment, scored outcome collection, owner-specific fitting, paid acquisition, external author contact or clinical/forensic use is authorized by this decision.

The nearest scientific follow-up is existing-source reproduction: recover the full dominance target/scoring exports and the inversion study's complete 141 score pairs/settings, then run the assignment-respecting nulls. This is more directly informative than a new adjustable personality survey or a new round of weights chosen from these studies. A future astrology-feature proposal must freeze the exact mapping before its outcomes and obtain genuinely untouched replication; it cannot borrow validation from the records used to choose it.

## Review and delivery record

Cross-family review status and reconciliation are recorded in `CORRELATION_CROSS_FAMILY_REVIEW_20260929.md` and the machine-readable gate. The review is an independent model-family interpretation check, not an independent participant study or a substitute for unavailable source data.

The validation receipt records protected hashes, article coverage, arithmetic replay, permitted-file scope and publication verification. This closes the requested **archive scientific-adjudication work package**. It does not close the broader research mission or claim operational readiness.
