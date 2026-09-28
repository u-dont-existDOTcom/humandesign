# Empirical Astrology Evidence Map

Date: 2026-09-28

Scope: 1,248 Wave 1 feature records, publication-level canonicalization, targeted original-source retrieval, and a 2021–2026 update.

## How to read this map

This is a development evidence map, not a verdict score and not prospective validation. The unit of independent evidence is a cohort or dataset—not a feature row, chapter mention, paper, or later reanalysis. Exact provenance is in `normalized_feature_records.jsonl`; document identities are in `source_registry.jsonl`; dataset reuse is in `dataset_registry.jsonl` and `duplicate_reanalysis_map.jsonl`; originals actually read are in `fulltext_manifest.jsonl` and `primary_feature_extractions.jsonl`.

The normalized corpus contains 1,248 preserved Wave 1 records, 913 canonical source documents after current additions and verified publication-alias collapse, 795 empirical source documents, and 965 conservative dataset/cohort units. The last figure is intentionally conservative: low-certainty units remain separate rather than being silently merged. Sixty-nine likely independent replication relations are identifiable; they are not all high-quality or confirmatory.

Evidence labels used below:

- **Original read**: methods/results inspected in a legal public full text.
- **Review-derived**: retained from Wave 1 with its original direction, but not promoted to primary evidence.
- **Abstract-only**: useful for the acquisition queue and hypothesis registry, not for a weight or a primary extraction.
- **Independent**: a distinct cohort, not merely a second paper or reanalysis.

## Executive evidence map

| Feature family | Strongest positive or suggestive result | Strongest null/opposite result | Independence and reuse | Main risk | Development status |
|---|---|---|---|---|---|
| Sun signs → personality | Mayo–White–Eysenck N=2,324 reported small polarity/water-sign effects | Lu et al. N=173,709: four traits null, raw extraversion disappears after season control, all B10<.001 | Independent modern cohort; historical positive not replicated under knowledge controls | Self-selection, astrology knowledge, season | `negative_constraint` |
| Sun signs → relationships | No stable original signal | Voas adjusted N=9,500,773 and Helgertz–Scott N=66,063 marriages: no practical compatibility pattern | Two independent national datasets | Census imputation and huge-N significance | `negative_constraint` |
| Whole-chart blind matching | No verified replicated signal | Carlson Part 2 0.34 vs 1/3; Indiana astrologers 0–3/23; meta-summary ES=.051, p=.66 | Carlson independent; McGrew/McFall and Mull reuse one 23-case cohort | Instrument adequacy; reader variance | `negative_constraint` |
| Time twins | Original Roberts–Greengrass claim did not survive reanalysis | NCDS N=2,101 mean serial r=-.003; reanalysis r=-.001 | NCDS independent; French et al. reuses Roberts–Greengrass | Post-hoc bins/models; broad composite test | `negative_constraint` for broad similarity |
| Aspects/orbs/harmonics | 2022 abstract suggests applying orb may exceed separating by 1–2° | Startup N=911: four aspect studies negative; continuous scan 3/32, family p=.21 | Startup one cohort; 2022 exact datasets unverified | Multiplicity, flexible orbs, correlated features | `interaction_only_candidate` |
| Gauquelin sectors | Long programme reports profession/eminence excesses | Replication/reanalysis chain is disputed and eligibility/control definitions move | Extensive cohort and publication reuse; later analyses often not independent | Selection, eminence thresholds, sector/control generation | `definition_uncertain` |
| Vedic karaka kendra | Oshop–Foss 60/84 vs 55.40% permuted, p≈.002 | No independent frozen replication located | One selected Twitter dataset | Coverage/selection, flexibility, no preregistration | `promising_requires_replication` |
| Vedic rule aggregates | None in the retrieved celebrity test | Rajopadhye et al. 742 vs 509: none of 68 parameters separated groups as predicted | One cohort; related programme papers are distinct datasets when shown | 68 correlated tests, incomplete orbs | `negative_constraint` for that rule set |
| Vedic clinical judgment | Bhandary et al. reported sensitivity/specificity ≈77–82% | Current-illness inter-rater κ=-.111; precise symptom/onset performance weak | One unreplicated cohort | Reader confounded with chart subset, recruitment, time quality | `likely_confounded`; high-stakes exclusion |
| Computational biography matching | 2023 abstract claims independent N=61, r=.51 | Dean simulation/review concerns and no auditable full method in this pass | Independence claimed, not verified from full text | Semantic leakage, tuning, abstract-only | `definition_uncertain` |
| Hemisphere sign inversion | 2026 abstract N=141 reports large north/south contrast | No full-text audit or independent replication | One dataset in abstract | Public-figure selection, pipeline tuning | `promising_requires_replication` |
| Violence/Mars aspects | 2026 abstract claims two cohorts, h=.144/.191 | Methods, controls, orbs, birth quality and multiplicity unavailable | Two cohorts claimed, not full-text verified | Stigma/high stakes, ascertainment, abstract-only | `likely_confounded`; excluded |
| Primary directions/fatality | No verified positive original in this pass | 2026 abstract N=400, Monte Carlo p=.11, powered for RR=1.15 | One modern dataset claimed | Abstract-only and high stakes | `negative_constraint` pending full text |

## Programme 1 — Gauquelin planetary sectors, profession and eminence

### What was tested

The programme uses diurnal planetary sectors—especially “key sectors” near rising/culminating regions—to compare eminent occupational groups with controls. It includes primary Gauquelin samples, athlete/profession replications, heredity claims, CSICOP and CFEPP tests, Ertel’s eminence analyses, demographic/control-generation critiques, and repeated publication of the same records.

### Evidence and chain

Wave 1 retains both reported positive sector excesses and null/opposite replications. The retrieved Ertel–Irving 1997 reanalysis (`SRC-POST-ERTELIRVING1997`) does not add a cohort. It compares the same historical programmes and reports:

- published Gauquelin athletes N=2,888 versus unpublished N=1,503, with an unpublished-subset selection index IMQ=1.31, p<.01;
- CSICOP N=408, IMQ=1.58 and a combined p=.01 under their selection analysis;
- no equivalent CFEPP selection-index result, with interpretation depending on low-eminence admissions.

The authors explicitly avoid a firm causal conclusion. The primary result of this chain is therefore methodological: sector boundaries, eligibility, eminence, publication status, demographic matching and control generation can change the apparent effect. Multiple papers using Gauquelin, CSICOP or CFEPP records are not independent replications.

### Decision

No sector receives an evidence-derived weight. A future test would require independent civil records, a fixed eminence rubric, a fixed sector definition, a demographic/hospital/time-preserving control generator, preregistration, and a held-out cohort. Status: `definition_uncertain` plus a hard reuse/control constraint.

## Programme 2 — Personality, signs and self-attribution

### Historical positive

Mayo, White and Eysenck (`SRC-8E12AA0FDD738B`, original read) studied 2,324 adults who had written to an astrologer. Odd signs showed higher extraversion (MSR=20.83, p=.0001) and water signs higher neuroticism (MSR=4.492, p=.0113). Differences were small—roughly one scale point against SDs around 4–5—and the sample was selected for astrology interest. Smithers–Cooper, Niehenke, Bourque, Steyn and other Wave 1 entries form the later knowledge-control and replication chain; their distinct cohorts remain separate in the dataset registry.

### Modern independent null and causal confound

Lu et al. 2020 (`SRC-7E9F58D3B36681`, original read) separates social stereotypes from actual traits:

- Study 7, N=173,709: agreeableness p=.84, conscientiousness p=.06, stability p=.98, openness p=.35; all B10<.001. Raw extraversion p=.002 disappears after season control (p=.26). Believer subgroup N=17,373 is also null.
- Study 8, N=32,878 employees: recent performance F=.73, p=.71, B10<.001; five-period average F=.42, p=.95, B10<.001.
- Preregistered Study 6, N=351 HR professionals: a Virgo label reduced hireability (d=-.29, p=.006) and perceived agreeableness (d=-.37).

This is an important distinction: astrology labels can change judgments and behavior even when signs do not predict the underlying trait. The causal social effect is a confound, not celestial validation.

### Decision

Sun-sign personality and employment main effects are hard exclusions. Belief, sign knowledge, prior readings and rater exposure must be measured or blinded. Season of birth remains a conventional covariate, not an astrology feature.

## Programme 3 — Aspects, orbs, angularity and harmonics

### Startup programme

Startup’s 1984 thesis (`SRC-11C6F771BA7D21`, original read) used one N=911 cohort, 32 planetary pairs and ten EPQ/16PF dimensions. It contains four distinct analyses, not four independent replications:

1. astrologer-specified aspect-to-trait directions: no overall support;
2. hard versus soft versus no-aspect MANOVA: null;
3. attempted 108th-harmonic replication for four Sun–planet pairs: null;
4. continuous separation in 24 bins of 15°: 3 of 32 MANOVAs p<.05; probability of at least three by chance=.21.

The 1985 journal article is a republication of the same cohort. Addey, Vail/Pottenger, Niehenke, Tarvainen and other aspect sources remain in the full queue and registry; unavailable originals retain their Wave 1 direction only.

### Recent orb claim

Tarvainen 2022 (`SRC-POST-TARVAINEN2022`) reports in a publisher abstract that four applications totaling more than 50,000 charts do not consistently favor tight over wide aspects, while applying aspects appear to tolerate maximum orbs about 1–2° wider than separating aspects. The full methods/results were not publicly available, so the exact aspect set, outcomes, control construction and multiplicity cannot be audited.

### Decision

Generic aspect, hard/soft, harmonic and continuous-separation main effects receive zero prior weight. Tightness, applying/separating status and angularity may appear only as preregistered secondary interaction terms attached to a pre-frozen aspect-to-trait mapping. They cannot define the primary endpoint.

## Programme 4 — Whole-chart and blind astrologer matching

### Carlson

Carlson 1985 (`SRC-3B14ACC2E29EF7`, original read) includes two parts in one publication. Part 1 is not decisive because subjects could not reliably recognize even their own CPI profile. Part 2 is the stronger test: 116 returned astrologer matches, correct first choice 0.34±.044 against chance 0.33 and the astrologers’ predicted minimum 0.50. Second/third choices were 0.40/0.25. Weight and confidence did not improve accuracy.

### Indiana/Mull/McGrew–McFall

McGrew and McFall 1990 (`SRC-6F54505EC903CC`, original read) used 23 richly documented cases with birth times verified to ten minutes, six expert astrologers, and one nonastrologer. Astrologers scored 0–3 correct, median 1; the control scored 3. Mean pairwise agreement was 1.4/23 and accuracy–confidence r=.03. The Mull and McGrew/McFall publications use the same 23-case cohort and count once.

### Broader synthesis

Dean and Kelly (`SRC-EA6A69D470403A`, original read) report a heterogeneous 40+ test synthesis of about 700 astrologers and 1,150 charts: mean ES=.051, p=.66; client reading discrimination across ten studies: ES=.002; inter-astrologer agreement across 25 studies: .101. These are secondary syntheses and are labelled as such in extraction records.

### Decision

No human reader score, intuition score or confidence weight enters the algorithm. Any future chart matcher must be mechanical, frozen, blind, calibrated against a chance/control generator and replicated on a held-out cohort.

## Programme 5 — Time twins

### Roberts–Greengrass chain

French, Leadbetter and Dean 1997 (`SRC-8809CD680770F5`, complete public HTML read) reanalysed the same 128 subjects/six dates and roughly 1,400 pairs used by Roberts–Greengrass. The mean correlation between birth interval and E/P/N/L difference was -.001. Equal-sized bins removed the claimed closest-pair trend. The highlighted p=.003 regression was post hoc; one result among nine plausible regressions was not persuasive. This is a reanalysis, not a replication.

### NCDS independent cohort

Dean and Kelly 2003 analysed 2,101 London births from 3–9 March 1958, mean adjacent separation 4.8 minutes and 73% within five minutes. Across 110 subject outcomes, mean serial r=-.003 (SD .028), with five p<.05 versus 5.5 expected. Sixteen mother controls averaged r=.001 (SD .029); subject-minus-control difference was in the wrong direction, p=.56. Sensitivity was about 0.00±.03.

### Decision

Broad natal-chart similarity is a negative constraint. The project’s proposed same-hospital/near-time personality experiment remains worthwhile because it is narrower, theory-neutral, locally controlled and prospective; it must not reinterpret the historical time-twin nulls as validation.

## Programme 6 — Relationships and synastry

### Large registry tests

Voas 2007 (`SRC-8F48C8A53D11D4`, original read) began with 10,317,673 England/Wales couples. An apparent excess of roughly 22,100 same-sign marriages was traced to same-birthday and first-of-month response/imputation errors. The adjusted 9,500,773-pair distribution was substantively random.

Helgertz and Scott 2020 (`SRC-8F28F7EAE4AD94`, original read) used 66,063 Swedish marriages for pairing and 46,326 unions/14,920 divorces for Cox models across six popular compatibility schemes. No pairing class differed even at p<.1. Representative hazard results were HR=.980 and HR=1.000. Isolated coefficients were small, inconsistent and non-ordinal.

### Synastry programme

Ruis, van de moortel, Gauquelin couple datasets, Westran and aspect-frequency studies are fully represented in the registries. Their reuse relations prevent Gauquelin-derived marriage papers from being counted as new couples. The 2021 Westran “1,300 cases” replication is in the update queue, but only an issue listing was public in this pass.

### Decision

Sun-sign compatibility is excluded. Full-chart synastry is not proven false by a Sun-sign test, but it has no transferable verified rule in the acquired originals and remains `insufficient_evidence` until exact, independent, multiplicity-controlled work is read and replicated.

## Programme 7 — Vocation, profession and eminence

This family contains doctors, clergy, scientists, artists, politicians, commanders, degree-area occupations, Gauquelin derivatives, McDonough scans and public-figure datasets. Publication count substantially overstates independent evidence because the same professional registries and Gauquelin records are repeatedly sliced by planet, occupation, eminence and method.

The strongest retrievable modern feature-level positive is Oshop–Foss 2015 (`SRC-33C6ABEB7839AE`): 60/84 high-profile Twitter users satisfied an AtmaKaraka–PutraKaraka kendra relation in D1 or D9 versus 3025/5460 (55.4029%) permuted, Fisher one-sided p=.00205. The cohort was selected through top-account coverage and timed-birth availability; no preregistration or independent replication was found. It is a frozen-form candidate, not a validated vocation feature.

Rajopadhye et al. 2021 (`SRC-79DD8AC42CC650`) tested 21 Vedic principles as 68 aggregate positive/negative parameters in 742 celebrities versus 509 ordinary charts. None separated the groups in the predicted direction. Orbs and some calculation details are insufficiently specified for reuse; the tested aggregate rule system is a negative constraint.

## Programme 8 — Prediction, transits, rectification and mundane claims

Wave 1 includes transits, progressions, horary, rectification, prenatal epoch, mundane events and prediction contests. Most high-value originals remained inaccessible and are explicitly queued. These claims are particularly exposed to post-hoc event windows, choice of significator, retroactive rectification, flexible start/end dates and development-on-test failure.

The 2026 Borealis publisher abstract (`SRC-POST-BOREALIS2026`) reports N=400 AA-quality AstroDataBank cases, fixed 180-day windows, Monte Carlo p=.11, and power for RR=1.15 for severe Morinus primary directions at violent death. It is a useful modern null but remains abstract-only. Prediction features do not enter the next algorithm.

## Programme 9 — High-dimensional and computational astrology

McDonough, Bergen, Godbout, Dean IRT, automated matching and neural/statistical scans are represented at source/dataset level. Their central issue is not whether a classifier can be fit; it is whether feature discovery is separated from evaluation, labels are independent of astrology text, the control generator preserves astronomical prevalence, and the final pipeline survives a held-out cohort.

The 2023 Godbout–Coron abstract (`SRC-POST-GODBOUTCORON2023`) claims an independent N=61 adjusted planetary-dominance replication with p=3.2e-05 and r=.51. Exact feature construction, biography coding, blinding, semantic-label leakage and multiplicity were unavailable, so status is `definition_uncertain`.

Samantaray et al. 2026 (`SRC-POST-SAMANTARAY2026`, original read) is explicitly a humorous synthetic exercise. Its logistic regression, random forest and MLP operate on generated signs/traits and perform near chance. It is pipeline illustration, not empirical astrology evidence.

## Post-2020 update

The update searched current Correlation issue listings, publisher pages, JSE, preprints and public repositories. Twelve sources not already canonicalized in Wave 1 were added. The highest-value items are:

| Year | Source | Public evidence available | Current treatment |
|---:|---|---|---|
| 2021 | Westran, progressed synastry replication, 1,300 cases | Issue entry only | Missing-full-text queue |
| 2021 | Douglas, SIDS replication | Issue entry only | Missing-full-text queue; high-stakes exclusion |
| 2021 | Tarvainen, five-degree rule | Issue entry only | Missing-full-text queue |
| 2022 | Tarvainen, tight/wide and applying/separating aspects | Publisher abstract | Candidate only; no primary extraction |
| 2023 | Godbout–Coron, adjusted planetary dominance N=61 | Publisher abstract | Definition uncertain |
| 2024 | Godbout et al., twelve planetary-dominance models | Issue entry only | Missing-full-text queue |
| 2025 | Pluto and cancer | Issue entry only; author unresolved | Missing-full-text queue; high-stakes exclusion |
| 2026 | Borealis, primary directions and violent death N=400 | Publisher abstract | Negative constraint pending full text |
| 2026 | Godbout–Brun, Southern Hemisphere inversion N=141 | Publisher abstract | Promising but unverified |
| 2026 | Daigno, Mars/fast-planet aspects in two violence cohorts | Publisher abstract | Likely confounded; high-stakes exclusion |
| 2026 | Samantaray et al., ML and astrology | Full preprint | Synthetic; not validation |

No abstract-only claim has been converted into a primary extraction or model weight.

## Cross-cutting constraints

1. **Dataset reuse:** papers are not independent observations. Gauquelin, Roberts–Greengrass, NCDS, Indiana/Mull, Startup and multi-study Lu lineages are explicitly mapped.
2. **Multiplicity:** exact feature universes, interaction families and correction plans must be frozen before outcomes.
3. **Control generation:** calendar, hospital, time of day, latitude/longitude, cohort and astronomical prevalence must be preserved.
4. **Prior knowledge:** astrology belief, sign knowledge and prior chart readings can produce real social/behavioral effects without celestial validity.
5. **Birth precision:** a feature cannot be calculated more precisely than the source time supports.
6. **Reader variance:** low agreement prevents human labels from being treated as a stable algorithmic target.
7. **Practical effect:** huge samples can make negligible artifacts significant; calibration and out-of-sample prediction matter.
8. **High stakes:** clinical, violence, mortality and hiring inferences are excluded regardless of exploratory p-values.
9. **Development versus validation:** every literature-derived feature has been observed during development and therefore requires untouched prospective replication.

## What deserves prospective testing

Only three narrow avenues survive as testable development hypotheses:

1. a theory-neutral same-hospital/near-time personality design with local temporal controls;
2. tightness, applying/separating status and angularity as secondary moderators of mappings frozen before outcomes;
3. a small number of exactly reconstructed candidates—especially the Oshop–Foss kendra rule and, only after full-text recovery, recent planetary-dominance/hemisphere rules—run at zero prior weight in held-out data.

Everything else is either a negative constraint, definition-uncertain, confounded, missing its original, or too high-stakes for person-level use.
