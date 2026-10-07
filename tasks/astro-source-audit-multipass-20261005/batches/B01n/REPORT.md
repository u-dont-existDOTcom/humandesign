# Astrology source audit: Ptolemy's complete natal timing chapter

Batch B01n, 2026-10-07. Source: Ptolemy, *Tetrabiblos*, Robbins's 1940 English translation in the supplied 1964 reprint. Targeted comparisons use Holden's published 2009 Rhetorius translation. This is historical source analysis, not a personal reading or a new validated prediction model.

## Recovery and completed scope

The interrupted IV.9 batch had already been committed and published at `fc9b500a21842d1c8f940d8465822f4b0c8b6396`. It contained 59 records and a recorded 473-test full checkpoint. It was recovered, not re-extracted or counted twice.

This increment reads and extracts all of English IV.10, including both transmitted endings and the relevant English explanatory notes. The scope begins at the IV.10 heading on PDF461/printed437 and ends with the two conclusions and notes on PDF483/printed459. Twelve English main pages and two relevant facing-note pages were inspected. The preceding IV.9 material and the following index are excluded. Greek and the complete critical apparatus were not independently translated or collated.

| Measure | Result |
|---|---:|
| New Ptolemy source records | **78** |
| Cumulative Ptolemy records | **708** |
| Sections read/extracted | **48 of 61** |
| English Book I | **24 of 24** |
| English Book III | **14 of 14** |
| English Book IV, including both endings | **10 of 10** |
| General age rows / topical origins / ingress levels | **7 / 5 / 4** |
| New targeted Rhetorius comparisons | **3**, bringing the total to **20** |
| Unresolved issues in this batch | **22** |

All thirteen Book II chapters and the remaining multi-source audit remain open. Records, table rows and tests are not independent human observations or predictive successes.

## 1. Five simultaneous timelines, not one good-or-bad period

For particular timing Ptolemy explicitly uses all the principal prorogations rather than the single selection used in the length-of-life enquiry. His origin/topic assignments are:

| Origin | Topic in this passage |
|---|---|
| Ascendant | Body and journeys abroad |
| Lot of Fortune | Property |
| Moon | Affections of the soul and marriage |
| Sun | Dignities and glory |
| Midheaven | Actions, friendships, children and other conduct of life |

He explains why: a person can lose a relative and receive an inheritance, become ill while gaining promotion, or have children amid misfortune. Simultaneously favorable or unfavorable outcomes across everything are possible, but exceptional in this account (PDF473–475/printed449–451).

Our methodological implication is to preserve these output dimensions rather than score a date as generically good or bad. The Moon's timing role does not erase Mercury's role in the earlier character enquiry; these are different questions and layers.

## 2. A multi-timescale method, with different jobs at each scale

The chapter distinguishes general time rulers, annual rulers, monthly/daily places and planetary ingresses. General rulers carry greater authority; partial rulers assist or deter; ingresses affect increase or diminution. Particularly emphasized are Saturn for general places, Jupiter for annual places, Sun/Mars/Venus/Mercury for monthly places, and Moon for daily places (PDF477–479/printed453–455).

This is not simply a list of slow-to-fast transits. The general procedure uses directions, term participation and the original natal connection to the topic. An ingress has to be interpreted with those relationships and the relevant aspects. The source says particularly, not exclusively; the table does not prohibit a planet at every other scale.

The compilation specification now connects these stages explicitly. It is a source specification, not a deployed full timing engine, and it does not validate or retune the previously fitted Hale or Joel timing candidates.

## 3. The monthly and daily numbers must not be silently modernized

The adopted text gives one year per sign, then **28 days per sign** for monthly counting and **2 1/3 days per sign** for daily counting, starting from the corresponding annual/monthly places. Robbins's note preserves the alternatives of 30 days and 2 1/2 days, with different evidentiary status: he reports no manuscript support for the 30-day proposal but two manuscripts for 2 1/2 (PDF477/printed453).

The new helper uses exact rational arithmetic. Twelve daily steps of 7/3 days equal 28 days; twelve monthly steps of 28 days equal 336 days. These arithmetic facts do not authorize inserting an undocumented annual reset, stretching 336 into a civil year, or quietly substituting the alternative 30-and-5/2 convention.

The epoch, inclusive/exclusive counting and reset convention are not completely settled by the passage. Helpers therefore require an explicitly supplied epoch and a declared zero-based half-open counting policy. That policy is an implementation choice, not attributed to Ptolemy. No actual date is forecast.

## 4. General planetary ages are not individualized chart evidence

The sequence is Moon about4 years, Mercury10 more, Venus8, Sun19, Mars15, Jupiter12, then Saturn for the remainder. Nominal cumulative divisions are 0–4, 4–14, 14–22, 22–41, 41–56, 56–68 and68 onward. The first boundary is approximate, so the table does not assert exact birthday transitions (PDF465–471/printed441–447).

The text expressly distinguishes this general age analogy from particular differences in nativities. Consequently, finding a conventional life-stage description appropriate for someone of that age does not establish that their individual chart was correctly identified.

Rhetorius46 instead organizes ages around the angles. Rhetorius49's least-year table agrees with four of these stage lengths but gives Moon25, Mercury20 and Saturn30 for its own planetary-period purpose. The same word period must not make these schemes interchangeable (Rhetorius PDF29,32–33/printed26,29–30).

The opening country-level examples also remain identified as historical stereotypes. They have not been converted into modern population, identity or character classifiers.

## 5. Repeated roles intensify the source judgement without creating independent evidence

Ptolemy says the same planet governing both time and ingress concentrates the result, favorable or unfavorable, especially if it also had original natal rulership of the matter. The helper preserves that role interaction and its unspecified magnitude. It adds no independent confirmations and assigns no probability (PDF481/printed457).

Similarly, all relevant planets and favorable as well as unfavorable major aspects participate in the general directions. Direct presence/aspect at the degree has priority; only known absence permits the nearest-preceding fallback. Term rulers share the rulership, but the passage does not supply a numerical share or a complete tie-breaking scheme (PDF475/printed451).

## 6. Both endings deliberately leave the detailed event synthesis incomplete

The Parisinus2425 conclusion leaves a complete particular account to judgement of temperaments. The other ending also omits the detailed enumeration and invokes skilled combination. Robbins identifies the latter with the Paraphrase and treats the original ending as a textual question (PDF481–483/printed457–459).

Thus completing the English natal books does not uncover a completely specified deterministic forecasting algorithm. Unresolved judgement, geometry and calendar choices must become explicit, versioned implementation decisions before outcomes are consulted—not new exceptions discovered to rescue a miss.

## Verification and storage

**150 checks passed in this turn's container:** 86 new bounded reference tests plus 64 adjacent B01l regression checks. The previous full-repository checkpoint of473 passing tests remains historical evidence; it was not rerun or added to150 and presented as a fresh result.

The new tests cover all age/origin/ingress rows, rational boundaries, distinct rate conventions, explicit epochs, known-absent versus unknown selection, tied carriers, origin-specific temporal measures, three-valued conditions, role dependence and source/coverage links. They do not establish astronomical qualification, independent semantic review or predictive validity.

The authorized desktop connection became unavailable during delivery. Publication therefore uses the working GitHub route with a hashed, self-contained source-audit archive and readable recovery files. The archive contains the complete new structured records, code, tests and a guarded checkpoint-update script. No raw book, OCR text or page image is included. The full desktop regression run and automatic placement in the computer's Downloads folder remain unperformed; the downloadable packet is the usable delivery. Historical models and previous source batches are unchanged.

## Next saved reading boundary

**B01o: English II.1–II.2**, starting at PDF141/printed117, with II.2 at PDF145/printed121, stopping before II.3 on PDF153/printed129. These headings are located only. First restore the archived batch and reconcile the progress mirrors when execution access is available; do not repeat IV.9 or IV.10. Book II's mundane/ethnographic claims remain historical source material, not modern demographic inference. The parent multi-pass audit remains OPEN; no background work after delivery is promised.
