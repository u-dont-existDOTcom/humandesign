# C33 — Change the Hellenistic pilot from rare military campaigns to a more observable marriage-count claim

**25 October 2026. ORIGINAL OWNER GOAL OPEN:** reconstruct source-defined competing techniques across 16 astrology traditions, then measure whether frozen chart predictions contain information about untouched real people, with blinded survey/outcome collection, strong nonastrology baselines, chart decoys, and explicit negative cases. **No humans evaluated or recruited in C33.** This is not an astrology-success report, historical manuscript validation or deployment of a new scorer.

## 1. Military pilot feasibility: archival service records are not enough

The prior candidate C30, a Dorotheus verse quoted in Hephaistio II.19, computes a Lot of Expedition from **Asc + Moon − Saturn** and describes campaigns when it lands in four zodiac signs. C31 and C32 correctly established strict Swiss planetary provenance and high-precision independent IAU/ERFA and Earth-orientation agreement (up to **329 passing historical/engineering tests**), but this does not solve its human outcome ascertainment.

Read the **United States National Archives** directly, rather than assuming a historical archive would be a ready-made evaluation panel:

- [NARA request instructions](https://www.archives.gov/veterans/military-service-records): full military personnel records normally become publicly accessible **62 years after separation**; newer personnel files require authorization for material beyond public information.
- [NARA's own explanation of OMPF content](https://www.archives.gov/veterans/military-service-records/about-service-records): files contain duty and administrative assignments, but **do not contain detailed participation in specific battles or engagements**.
- Full original time-of-birth records and campaign-observation outcomes have not been linked for a representative, truly untouched cohort. Recruiting only known veterans or war participants would cause selection bias, while ordinary peacetime service cannot be reclassified as the predicted war-campaign outcome.

**Result:** C30 stays a historically attested, falsifiable *development* candidate but is **not the recommended first blinded recruitment target** in the present evidence/access environment. This is a feasibility disposition, not a disconfirmation of astrology or a claim that no war cohort could ever exist.

## 2. Better source-defined claim: Ptolemy's marriages

Read the original Greek of **Ptolemy, *Tetrabiblos* IV.5 §§2 and 4**, in the edited **Boll/Boer Greek text** at [Perseus](https://beta.perseus.tufts.edu/urn:cts:greekLit:tlg0363.tlg007.1st1K-grc1:4.5/) and the corresponding **1940 Robbins Loeb English** [on LacusCurtius](https://penelope.uchicago.edu/thayer/e/roman/texts/ptolemy/tetrabiblos/4b*.html). A separately recovered modern [Eulogikon digital Greek rendition](https://eulogikon.org/works/ptolemy-alexandria-tetrabiblos-phs-ai.md) (484,328 UTF-8 bytes; SHA256 `7d337a6314d3a68cca0bd310355e4737b393180e1b287415ee6eddfe34b9f630`) agrees in the relevant phrases.

The Greek source explicitly assigns the **Moon to its historical male-nativity branch** and the **Sun to its historical female-nativity branch**. The terms `ἐν δισώμῳ` (in a bicorporeal sign) and `πολυγάμους` (many marriages) occur in both. **Ptolemy, Book I.11** explicitly enumerates the four bicorporeal signs as **Gemini, Virgo, Sagittarius, and Pisces**. See [Ptolemy I.11](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1b*.html). This gives an observable category—having experienced more than one lawful marriage—without relying on the Ascendant or unresolved houses.

**Critical wording limitation:** IV.5 includes disjunctions: sign of one figure *or* application to one planet suggests one marriage; bicorporeal *or multiform* sign *or* application to several planets suggests multiple marriages. These alternatives can **coexist and even produce conflicting results**. We implemented **only the independently computable bicorporeal-sign sufficient positive subclause**, not the entire Ptolemaic marriage judgment. Outside those four signs the program states **NO AFFIRMATIVE CLAIM FROM THIS SUBRULE**, never the fabricated conclusion “one marriage.” Also, “lawful cohabitation” in the ancient setting is not perfectly equivalent to modern government-registered marriages; the observable modern translation must be fixed *before* test outcomes.

The four signs and branch-specific luminaries are now captured in the source-typed [C33 registry](HELLENISTIC_C33_MARRIAGE_RULE_AND_FEASIBILITY_V1.json), and [source-only classifier](hellenistic_c33_ptolemy_marriage_count.py). The code uses twelve exact tropical 30° bins with strict invalid-longitude rejection. **This is not an inference about any owner's life or third party.** The source uses a historical male/female binary; any modern cohort scope is separate and based on informed choice, not inferred identity.

## 3. Important feasibility advance: may not require an exact birth minute

The original source-positive Moon subclause depends on the **natal lunar sign**, not houses or an Ascendant. Consequently a documented birth-time uncertainty interval may still have the **same condition** throughout the whole interval.

C33 uses the **existing fail-closed Swiss Ephemeris `.se1` provider** for Moon/Sun. For any UTC birth window up to 48 h, it computes a midpoint physical longitude and a symmetric worst-case motion envelope from the **incumbent project's declared speed bound** (Moon 16°/day; Sun 1.1°/day). It then enumerates **every possible zodiac sign crossed** by the entire bound—not just endpoints. If the possible signs include both bicorporeal and other signs, it reports `TIME_INDETERMINATE`; the claimant must not select a conveniently favorable time.

**The speed bound is declared in the upstream implementation but has NOT been independently proved across the whole future historical cohort.** Hence current classifications are expressly *conditional* and not frozen human predictions. A scientific test can either independently validate a conservative bound across its intended date range or use complete interval event-solving with a second reference. Exact documented timezone/date and location-source conventions are also necessary to construct the correct UTC window.

Ran the full algorithm on **all 366 synthetic UTC days of leap-year 2020**, each **00:00–24:00 UTC**. There were *no real people, birth records, or marriage outcomes*.

| Source classifier outcome for this **synthetic UTC-day experiment** | Windows |
|---|---:|
| Source-positive bicorporeal condition throughout | **55** |
| No source-positive condition throughout | **186** |
| Crosses a possible positive/nonpositive sign boundary; unresolved | **125** |
| **Total windows** | **366** |

Thus **241/366 (65.8%)** of these dates could be conditionally classified **without a clock time** at the chosen source-declared speed bound, but 125 could not. This is not an estimate of the fraction of real humans with usable birth records; a UTC day is not necessarily the person's local civil birth date, sample birthdate distribution is not uniform, and the bound proof remains open. Among **conditionally classifiable** synthetic dates only **55/241 (22.8%)** have the positive branch; assuming a one-third exposed fraction after date-only filtering would misstate feasibility.

The full [366-row synthetic receipt](HELLENISTIC_C33_UTC_2020_SYNTHETIC_CLASSIFIER_V1.json) includes source-file SHA256s and all abstentions. The existing Swiss provider is reused; no astrology engine was rewritten or promoted.

## 4. Observable marriage history and power are more realistic than campaigns

The [US Census American Community Survey](https://data.census.gov/table/ACSDT1Y2024.B12505) directly tabulates **Number of Times Married** as a population-level outcome; the [Census marriage-history report](https://www.census.gov/newsroom/press-releases/2021/marriages-and-divorces.html) documents age/civil-status variation. Those public aggregate statistics do **NOT** supply individual natal birth times or matchable persons, and do **NOT** validate Ptolemy's hypothesis.

The proposed modern primary outcome is **at least two recognized marriages by attained age 50**, with the age threshold explicitly an **analyst-chosen follow-up cutoff, not written in Ptolemy**. Include never-married adults in the denominator, recruit without conditioning on marriage history, record the local legal/customary-union definition *before seeing outcomes*, and preserve incomplete information as unknown. The proposed historically scoped male Moon group is the *primary research lane*; the female Sun sign group is a separate secondary hypothesis especially susceptible to **birth-season confounding**, since Sun sign is almost a calendar-birth-month label. None of these are normative claims about modern gender identities, sexuality or relationship worth.

The [hypothetical sample-size worksheet](HELLENISTIC_C33_HYPOTHETICAL_POWER_V1.json) uses **normal-approximation two-proportion calculations** with arbitrary *assumed* event risks, two-sided alpha=0.05, nominal 80% power and exposed fractions. They are **not measured event rates, requirements, a preregistration, a forecast or a validated effect size**:

| Purely assumed example | Total sample size, unadjusted |
|---|---:|
| Military campaign: 1% vs 2%, 1/3 source-positive | **4,975** |
| Military campaign: 3% vs 4.5%, 1/3 source-positive | **5,513** |
| Multiple marriages: 15% vs 25%, 1/3 source-positive | **548** |
| Multiple marriages: 20% vs 25%, 1/3 source-positive | **2,435** |

As a **sensitivity to the synthetic date-only stable-window exposure fraction** 55/241 rather than 1/3, the hypothetical 15% versus 25% marriage case rises to **677**, and 20% versus 25% to **3,049**. These still **exclude** recruitment losses, actual confounding, missing marriage records, design-effect clustering, censoring and restrictive birth-quality screening. No observed difference was measured. Actual sample size can only be selected after a separately documented feasible cohort and prospectively chosen clinically/socially relevant difference.

## 5. Bounded next steps, without endlessly expanding source requirements

The candidate can be prepared as a **separate** human-study protocol without waiting for the C30 Ascendant/MC issue: select the complete positive-only clause and its contradictory-text warnings; verify source lunar sign stability from independently supplied birth date and timezone, with exact time only where necessary; freeze respondent pseudonyms, age/country/cultural eligibility, chart and data source hashes, question/outcome wording and primary effect/null before marriage-history answers are seen. Use a **strong nonastrological baseline** for birth decade, birthplace/region, birth season and marriage context. Use concealed response collection and person-level separation. Compare exposure groups without pretending the nonpositive lunar group is predicted to have exactly one marriage. Retain all negatives/unknowns.

[Unregistered blinded-study draft](HELLENISTIC_C33_BLINDED_MARRIAGE_COUNT_STUDY_DRAFT_V1.json) captures all of this. **No recruitment, owner personal biography or retrospective couple data used.** The active root `participant-session-v1` task and its scoring code are untouched. If the research protocol is later adopted, collecting informed human birth/intimacy/marital history data and freezing true predictions is a *separate*, actual authorized operation.

**Recommendation for the next Hellenistic continuation:** prioritize the **Ptolemy male-Moon marriage-count clause as a development-only prospective pilot**, retain Dorotheus's military-campaign source claim in the catalogue for a better suitable cohort, and move toward real consented blinded validation rather than collecting more Hellenistic manuscripts or fine-tuning source variants on known biographies. The broader 16-tradition owner objective is OPEN.


## Reproducibility and C33 verified status

- 2026-10-25: `PYTHONPATH=src:/tmp/c32-independent-erfa C32_IERS_C04_PINNED_FILE=/tmp/c32-eop-c04-mirror.txt /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c33_*.py'`: **18/18 new C33 tests passed**.
- Same pinned runtime, `-p 'test_hellenistic_*.py'`: **347/347 historical-source and research-engineering tests passed** (**329 inherited + 18 new**, no skips).
- Re-ran the complete 2020 date-only simulation from the two existing pinned Swiss ephemeris files; generated 366-row dataset and all hypothetical power scenarios were **byte-identical to their saved original JSON**. No user/other human birth chart data loaded.
- This verifies reproducible source registration, mathematical sign boundaries, provisional continuous-speed envelopes, status distinctions and hypothetical arithmetic. It **does not** prove the 16°/day historical bound, Ptolemy's actual predictive accuracy, modern marriage-law equivalence, a sampling design, or anything about the user.
- Human predictive validations **0**; production rule changes **0**; source versions/owner baseline and previous Hellenistic 329 historical-source cases unchanged.
