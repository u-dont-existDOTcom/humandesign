# Murderer birth-pattern pilot — 2026-10-03

## Question

Can birth-date numerology and/or date-only astrology distinguish a cohort of convicted murderers with prison/life/death-sentence evidence from people with substantially more favorable public-life outcomes?

This is an exploratory case-control pilot. It is **not** a claim that astrology or numerology predicts criminality, and it must not be used to infer whether an individual is violent or dangerous.

## Cohorts

### Offender side

Source: `anurag-panda-dev/Serial-Killers-Dataset`, a Wikipedia-derived dataset with 494 serial-killer profiles and fields for date/place of birth, conviction/sentence information, categories, and source URLs.

The source supplied 332 records with day-precision dates of birth. A living + incarceration/life/death-sentence screen produced roughly 90 candidates. Obvious unsuitable records were then removed from the analyzed matched set, including collective-name records and known release-status false positives encountered during screening.

Final analyzed offender count: **82**.

Important limitation: the source's Wikipedia category fields can be historical. Therefore the cohort should be read as a high-confidence **incarceration/life/death-sentence evidence cohort**, not as a fully hand-audited census proving that every person was physically in prison on 2026-10-03.

### Positive-outcome comparison side

Source: `JeffersonConza/The_Nobel_Laureates`.

Nobel laureates were used as a **high-accomplishment public-life proxy** because they provide clean names, exact birth dates, sex, and birthplaces. They are not a measure of subjective happiness. Calling this a "happy people" cohort would overstate what the data say.

Controls were selected without using numerology or astrology: nearest unused birth year, same sex when offender sex was known. The sensitivity analysis used only **53 pairs with birth-year gap <=5 years**.

The exact rows used are in `paired_cohort.csv`.

## Feature policy

### Numerology

DOB-only features:
- Life Path, preserving master numbers 11/22/33;
- reduced birth day;
- month;
- reduced birth year;
- month+day attitude number;
- master-number flags;
- total birth-date digit sum.

Name numerology was excluded from this first pass because offender birth names, legal names, aliases, and transliterations are inconsistently documented. Using whatever name happened to be easiest to scrape would create avoidable bias.

### Astrology

Because exact birth times are unavailable for most subjects, the analysis deliberately excludes:
- Ascendant;
- Midheaven;
- houses;
- exact-time lunar claims.

The date-only feature set uses tropical ecliptic positions at 12:00 UT for:
- Sun;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;

plus compact element/modality counts. This is a coarse birth-date model, not a natal-chart model.

A specific mutable-sign count was also checked because prior serial-killer astrology work has claimed mutable-sign enrichment.

## Tests and results

### 1. Same-year calendar null

Each offender DOB was compared with random dates drawn from that same birth year. This asks a clean question: are the observed offender birthdays unusual relative to the calendar distribution they came from?

**Solar zodiac:** no signal. Omnibus Monte Carlo **p = 0.897**.

**Life Path:** borderline omnibus deviation, **p = 0.056**.

The two most conspicuous individual values were:
- Life Path 7: **15 observed vs ~9.1 expected**, raw p ~0.051;
- Life Path 33: **3 observed vs ~0.79 expected**, raw p ~0.039.

After correcting across the tested Life Path categories, both are **q ~0.303**. They are therefore not discoveries. They are only candidates that could be frozen before a new replication cohort is examined.

**Mutable planets:** no clear replication of a mutable-sign claim.
- mean mutable count across Sun/Mercury/Venus/Mars/Jupiter/Saturn: **2.146 observed vs 2.054 expected**, p ~0.433;
- people with >=4 of those six planets mutable: **13 observed vs 8.76 expected**, p ~0.132.

### 2. Out-of-sample offender vs same-year random-date classification

Across 100 independently redrawn same-year control sets, mean grouped cross-validated AUC:

| Feature family | Mean AUC |
|---|---:|
| Calendar-only | 0.467 |
| Numerology | 0.463 |
| Date-only astrology | **0.510** |
| Combined | 0.462 |

A useful discriminator should remain above chance out of sample. None did.

### 3. Offender vs Nobel high-accomplishment proxy

For the better matched subset of **53 pairs with <=5-year birth-year gap**, 5-fold pair-grouped L2 logistic regression produced:

| Feature family | CV AUC | Balanced accuracy | paired permutation p |
|---|---:|---:|---:|
| Calendar-only | 0.532 | 0.509 | 0.211 |
| Numerology | 0.485 | 0.519 | 0.586 |
| Date-only astrology | **0.587** | **0.557** | **0.096** |
| Combined | 0.501 | 0.528 | 0.522 |

The astrology-only bump is the strongest machine-learning result in this pilot, but it is still weak. It does not reach the usual p<0.05 threshold, several feature families were inspected, and adding numerology destroys rather than improves the separation.

## Prior-work cross-check

This direction has already been explored in public data:

- CUE's large birthday study analyzed **817 serial killers with day-precision DOBs** and reported no clear deviation from chance across its tested birthday/numerology/zodiac measures. It noted a few weak patterns but did not treat them as clear results.
- A separate public serial-killer zodiac analysis of roughly 300 cases likewise reports a null zodiac-distribution result.
- Jan Ruis's 2008 serial-killer birth-chart paper reported positive findings involving mutable signs, Moon aspects, and the 12th house, using 77 cases with known birth times plus a larger unknown-time sample. Those exact-time claims cannot be fairly tested in this dataset because the required birth times are mostly absent.

The present pilot therefore adds a matched-control/predictive check rather than treating raw zodiac frequency as sufficient evidence.

## Current conclusion

**No validated algorithm emerged.**

The strongest things worth carrying forward are narrow and pre-registrable:

1. Life Path 7 enrichment;
2. Life Path 33 enrichment;
3. the exact frozen date-only astrology feature set that produced AUC 0.587 in the <=5-year Nobel comparison.

Everything else should be treated as negative evidence.

The next scientifically useful step is not to add more symbols until something becomes significant. It is to freeze those three observations now and test them once on a **new independently sourced offender cohort plus exact-year-matched non-offender people**, without retuning. If they fail, they should be retired.

## Interpretation limits

- Public achievement is not subjective happiness.
- Serial killers are not representative of all murderers.
- Prison/status metadata is imperfect and should be hand-verified before a publication-quality analysis.
- Birth-year, sex, geography, socioeconomic background, and cohort effects can confound public-biography comparisons.
- Exact-time astrology cannot be inferred from date/place alone.
- A group-level statistical association, even if replicated later, would not justify labeling an individual dangerous from a birth date.

## Reproducibility

- Exact analyzed rows: `paired_cohort.csv`
- Machine-readable results: `results.json`
- Reproduction code: `run_analysis.py`
- Seed: `20261003`
