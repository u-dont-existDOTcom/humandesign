# Astrology forward- and reverse-blind validation — scientific readiness draft, 20 October 2026

**STATUS: DESIGN DRAFT ONLY. NOT preregistered, recruitment-ready, a locked model or a report of human predictive results.** Existing real human astrology prediction trials in this project: **zero**. This draft is intended to make the next step empirically meaningful rather than merely increasing original-source annotations. All actual participant data must remain private and out of the public HumanDesign source-history repository.

## Scope and analysis hierarchy

Three distinct astrological source/model families are under investigation: historical Western Lilly/Ptolemy, Chinese Zi Wei Dou Shu, and Chinese BaZi. They differ in calendar, time, chart and interpretation rules; **do not retrospectively select the tradition that best matches each person**. A future combined model must have weights/conventions frozen on development-only data before being evaluated on entirely new participants; cross-system post-hoc ensemble scoring cannot rescue negative results.

Separate four types of evidence:

1. **Original-text history**: the old text literally says a particular thing, with source SHA/folio/edition and contextual qualifications. A historical rule is not a validated characteristic of anyone.
2. **Chart-engine mathematics**: a defined birth timestamp/longitude/zone/calendar choice leads to reproducible stars and houses, verified against independently produced date/calendar/geometry oracles. Software agreement is not yet empirical psychology.
3. **Forward-blind human predictive validity**: before observing responses, a frozen chosen chart and original selected behavior mapping predicts nonleading questionnaire answers better than declared controls, on untouched people.
4. **Reverse-blind chart matching**: an already frozen response profile identifies its true chart among independently computed matched alternatives better than predeclared chance/permutation expectations. This is a secondary distinct claim; don't infer it from forward prediction alone.

## Existing verified results and limits

The current Chinese historical source index documents BaZi210 and ZiWei586 claims. The fourteen principal Zi Wei star Life-palace descriptions are text-covered, and four auxiliary star descriptions follow, but many original auxiliary star/house/time rules remain OPEN. A separate Chinese source-engine lane reproduced 14 major-star placements for 312 synthetic charts only when incompatible leap-month conventions were explicitly harmonized; 120 raw leap-convention mismatches were preserved. Another Chinese dual-calendar audit has 30 mismatches in an exhaustive 1901–2100 two-software comparison, including 2057 dates, and only ten original official HKO modern date records.

The Western engine reproduces some original printed historical geometric inputs: a known Lilly merchant natal chart's seven zodiac signs if the written 1616 date is interpreted Julian, four Regiomontanus house cusps within about eight arcminutes given printed right ascension; however natal Mercury/Venus original-vs-modern longitude discrepancies and actual historical clock/birthplace remain unresolved. An old solar return's daily motion closely matches the modern ephemeris while its absolute noon longitude differs. None constitutes a real-person behavioral test.

The HumanDesign repository's existing forward-blind infrastructure guidance at `docs/20_forward_blind_prospective_validation.md`, `docs/05_blinding_and_secrets.md`, `docs/10_metrics.md` can inform the experimental process, but its HD gate/line scoring definitions are **not** astrology source mappings, nor can its model-compliance tests establish astrological readiness.

## Minimal viable source-limited forward pilot (not yet approved)

The fastest scientifically useful first test need not wait for every 17th-century chapter to be transcribed, **provided** a bounded, honest source-limited model can be frozen. The model name must disclose exactly which text/conventions are included. A Chinese source-limited model could use only original principal-star Life-palace configurations with independently verified natal calendar rules for a narrow, specifically defined modern cohort. A Western source-limited model could similarly restrict to original-source-verified natal planetary and Regiomontanus rules, withholding historic timing, local-meridian or interpretive claims that cannot yet be computed reproducibly. **Neither is ready today**: birth-date conventions and outcome mapping remain open.

Choose only one primary confirmatory family or preregister multiplicity-adjusted co-primary comparisons. Freeze before a participant's scored answers:

- exact software commit, source-note IDs and printed-era uncertainty; stellar positions/calendar type, source witness/ephemeris SHA and returned provenance flags;
- accepted birthplace/recorded clock provenance, IANA TZ, DST fold, birth-time uncertainty and inclusion rules (reject undefined, 2057 disputed or near solar-hour boundary cases rather than pick an appealing chart);
- exact source-rule resolution hierarchy including conflicting positive and negative indications, branch precedence, how many features per participant, which conditional wording and whether a skipped chart/question is scored;
- exact chart features, mapping to participant-observable behavior questions, dependencies, option directions, questionnaire bank, response choices and randomized option order;
- independent chart decoys, class/age/geographic nuisance-matched panels, random seed and nonastrological baseline training/controls;
- primary metric and unit, e.g. per-question proper log score **only** if probabilities are calibrated without validation people, plus secondary chart-rank percentile and predeclared permutation null;
- timestamped cryptographic input/chart/model/prediction package and locked response-independent randomization and analysis script.

Never infer standardized effect size from a retrospectively fitted known merchant or from synthetic calendar agreement.

## Eligibility, blinding, consent and data integrity

Recruit *new, untouched* adults with independently supplied full DOB, birth time evidence and birthplace. An owner or known case whose chart/answers have already informed the rules (including previously examined owner and Hale) may serve as development examples, **not** untouched final validation. Predeclare whether people familiar with astrology can be included, separately record familiarity before testing, and do not tell participants their chart or predicted traits before response freeze. Birth location/time and sensitive responses must remain outside the public repo; store only blinded pseudonymous hashes/aggregate reports where permitted and anonymization genuinely holds. Explicit voluntary consent must cover birth data, storage, response collection and later interpretation/reveal.

Use nonleading behavior-first items that assess ordinary habits/experiences on defined time intervals. Do not test source-era discriminatory or medical/mortality assertions as if reliable diagnoses, social worth or advisories. Source statements with 'or', reversals, benevolent mitigations or vague temporal conditions must be either precisely operationalized **in advance**, separately marked as hypotheses with statistical multiplicity, or excluded from scored primary analysis.

## Primary evaluation and negative controls

Preferred **forward-blind** primary metric: difference against a frozen nonastrological baseline in cross-validated/holdout average proper score for predicted response distributions. Avoid calling raw symbolic support scores calibrated probabilities. If no justified probabilities exist, lock a categorical/rank-based metric instead with a declared null and ties. Secondary **reverse** evaluation on exactly the same withheld cohort can use an N×N chart-to-response score matrix with true-chart rank, matched decoy ranks, and chart-label permutation to estimate the null; the chart/response pairings cannot be tuned after reveal. Decoys must be fixed before responses; broad panels are reported in addition, not chosen later because they look better. Report misses, excluded uncertain birth-time cases, missing responses, version deviations, all model families tried and all predeclared score variants. No retrospective 'not-self', 'wrong school', invalid moral category or convenient Cazimi interpretation can justify excluding a miss after observing an outcome.

Before any final test, decide sample size with an explicit pre-data simulation/power and precision goal, familywise hypotheses, interim-analysis rule (ideally none), significance/CI and minimum worthwhile effect threshold. Do **not** invent a sample size from the existing source registry's 15k historical annotation count. A pilot can estimate response quality and prevalence but its participants become development data, not a fresh untouched confirmatory cohort once responses are inspected.

## Current go/no-go

Machine-readable `READINESS_GATES_V1.json` deliberately marks **10 blocking gates** across input accuracy, model freeze, chart computation, questionnaire mapping, calibrated scoring, decoys, consent, pre-response data freeze, untouched cohort and predeclared evaluation. No scored human study is authorized as completed/ready here. Synthetic tests and historical source work can continue independently. This is a review plan, NOT a signed or registered scientific preregistration, nor evidence a participant has consented.

**Next highest-value development action:** choose a specific bounded source-limited astrology model, close its natal-time/calendar scope on synthetic and independently authenticated input cases, and map a *small* preselected subset of source rules to behavior-first questions without having any new people's answers. Then freeze a synthetic-only full participant flow and negative-control permutation scorer. Owner choice and consent gates occur before real data.
