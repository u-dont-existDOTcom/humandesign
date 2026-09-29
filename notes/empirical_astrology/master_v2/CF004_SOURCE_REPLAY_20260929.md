# CF-004 source replay: southern hemisphere inversion

Date: 2026-09-29. Status: **published aggregate arithmetic replayed; 141 individual decisions and corrected semantic null source-blocked**. This is existing-source development analysis only. It changes no frozen decision, feature, weight, prospective specification or participant status.

## Sources and access check

- Vincent Godbout and Hubert Brun, “Should the Tropical Zodiac Signs Be Inverted to Their Opposites in the Southern Hemisphere?”, *Correlation* **38(1)**, PDF issue dated **2026**, pp. **39–56**; local original `/home/joel/Documents/astrology/correlations journal/2026 Vol 38 01c20263801.pdf`, SHA-256 `e3ad72ee69c213ebe79739c025c91357fd7c112eefc8468bbdb43911ee9e8e73`. The [publisher article page](https://correlationjournal.com/should-the-tropical-zodiac-signs-be-inverted-to-their-opposites-in-the-southern-hemisphere/) contains its abstract but no person-level download; the publisher's [abstract index](https://correlationjournal.com/abstracts/) dates it 2025, whereas the owner-held issue itself is dated 2026. Both dates remain in provenance.
- CF-003 replication roster: Godbout and Vital Coron, *Correlation* **36(1)**, 2023, pp.49–60, owner-held PDF `2023 Vol 36 01 c20233601.pdf`, SHA-256 `a4c0da056639aa0833dd96229a4efc3817395729b26c361875f24322f5092f44`, especially Table 1, p.50 (embedded raster image). Training parent: Godbout and Coron, *Correlation* **35(2)**, 2023, pp.11–29, PDF `2023 Vol 35 02 c20233502v2.pdf`, SHA-256 `780b8422d77059892b57c395d9cf3c2b40f828706b0c2ed51a7bcabb0b03aac6`, especially p.13.
- A recursive file inventory of the supplied `correlations journal` directory found PDFs only. `pdfdetach -list` showed zero embedded files in each of the three relevant PDFs. The inversion article's appendix/endnotes contain a survey, references and notes, **not** a score matrix or supplement. Searches of the publisher's article/issue/author pages and public source-index results found no score export. No purchase or author contact was made.

## Availability audit

| Input | Direct source availability | Replay result |
|---|---|---|
| 68 southern names; 73 northern names | Complete name rosters, Figures 2 and 1, pp.42 and 41 | 141 named subjects; individual birth-data source records/quality and exclusions not provided in a machine-readable table. |
| Paired original/inverted global scores | Three printed pairs only: Allende and Anitta in Table 1, p.47, Musk in Table 4, p.50 | **3/141** pairs present; **138/141 missing**. None of the printed differences agrees with its pair. |
| Word-score matrix and denominators | Figure 3 and Tables 1/4 print short snippets; one complete 151-item *trait list* for Greta Garbo in Figure 5 | No full 141 × 2 chart keyword scores, all matched words or denominator totals; the snippets cannot regenerate global scores. |
| Biography targets | Brief first-five southern snippets in Figure 4, 151 Garbo trait words in Figure 5 | No complete immutable 141-person French lists, prompts per person, model version snapshot, retries, edits or selection log. The published two prompts use **each named person's identity**, and request “exactly 150” while Garbo has 151. |
| Mastro transformation and software | Text says manual Ayanamsa 180°, planet-in-sign-plus-aspect and midpoints, houses excluded; no exact executable build or keyword-score export | The full fixed rule cannot be replayed from the article. Figure 6 orientation is self-contradictory. |
| Individual wins, ties, latitudes | Aggregate wins only: South 48/68, North 26/73; two latitude-distance tests stated null | No 141-person binary vector, tie/zero handling or latitude/score series. Preserve both failed latitude tests. |
| Conditional assignment-respecting null | No person-level chart/profile scoring exports or strata covariates | **Not run.** Do not substitute finished-score-label shuffling or a nominal 50/50 baseline. |

## Executable arithmetic replay

`python scripts/empirical_astrology/reproduce_cf004_20260929.py` uses only printed source numbers; standard-library calculations assert the three printed differences disagree and print structured JSON. For reported South 48/68 and North 26/73, pooled two-proportion **z=4.15518275**, one-sided normal **p=0.00001625138**, **Cohen's h=0.71618410**. Conditional on the paper's assumed 1/2 binomial baseline, its South 48/68 upper tail is **p=0.0004571954** and North non-inversion 47/73 upper tail is **p=0.009308876**. Those reproduce the headline rounded values and do not check how the 141 binary assignments were produced. The 1/2 null's validity is not established by this arithmetic.

| Person, original page | Non-inverted | Inverted | Printed difference | Inverted minus non-inverted | Pair implies |
|---|---:|---:|---:|---:|---|
| Allende, Table 1 p.47 | .9989 | .9425 | **+.0456** | **−.0564** | Non-inversion, contrary to prose calling both Table 1 examples positive. |
| Anitta, Table 1 p.47 | .3616 | .9617 | **+.0201** | **+.6001** | Inversion, with large discrepancy in magnitude. |
| Musk, Table 4 p.50 | .3170 | .3329 | **+.1108** | **+.0159** | Inversion, with large discrepancy in magnitude. |

Further exact source discrepancies: Figure 6, p.49, labels **Sun Capricorn non-inverted / Sun Cancer inverted** for the June 28 birth, but p.50 calls Capricorn the inverted Sun/Ascendant/Mercury; p.51's non-inverted example explicitly says Sun Cancer. The paper does not supply a corrected figure or orientable machine export. Table 4, p.50, prints Musk inverted *authority* score 7.9, whereas Table 5, p.51, prints 7.0 (spelled “Autority”). On p.48 the printed statement `0.705 / 0.365 = 1.98` is arithmetically false (≈1.932); the actual unrounded 48/68 divided by 26/73 is ≈1.982. None establishes which unprinted person-level scores, chart column or numerator was used in the headline. Neither a one-case correction nor a blanket swap of columns is defensible from these excerpts.

## Cohort intersections and boundaries

- The 2026 paper directly says its **73 northern charts** are reused from Godbout's 2020 Le Monde sample; the 2023 CF-003 training paper says its 189 included those same 73 plus 116 additional Astro-Databank subjects. Thus all 73 northern persons overlap the training sample, independently of their newly generated GPT word lists.
- The 2023 CF-003 replication Table 1 prints 61 new-person names; comparing that entire image roster against the inversion Figure 2 roster finds two direct exact-identity intersections: **Salvador Allende and Claudio Arrau**. No other exact name was observed in those two printed rosters; this does not resolve aliases, identity mistakes, biographical dependence or the missing full roster of 116 additional training people. In particular, the southern sample cannot be asserted disjoint from the 189-person training set.
- The 2024 twelve-model study uses the same 189+61 people, so overlapping Allende/Arrau are not a further independent replication. The 2023 and 2026 biography pipelines have different sources and denominators; they are not interchangeable targets.

## Exact missing inputs and next source boundary

Obtain an immutable source export with all 141 stable IDs/selection records, two chart versions and sign labels per person, Mastro executable build/corpus/settings, complete per-chart word scores and denominators, original biographical word lists with generation provenance, individual paired scores and ties. A corrected source version must carry provenance for the Allende, Anitta, Musk, Figure 6 and authority discrepancies. Only then can the 141 comparisons and latitude analyses be replayed without fitting. A conditional biography-assignment null additionally requires defensible exchangeability strata based on N/S ascertainment, era, language, fame, biography length and participant reuse, fixed **before** permutation, and recomputation of every scorer stage affected by reassigned biographies. Masked-identity or independent trait measurement is a separate sensitivity design. No such source-level replay or null has been claimed here.
