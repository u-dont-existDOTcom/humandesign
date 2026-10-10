# Lilly: wealth, its means, timing and continuation

Source audit B02g — 10 October 2026

## Result and scope

The complete second-house section of William Lilly's *Christian Astrology*, Book II, is now read and extracted: Chapter XXVII begins midway through PDF 201, after the previously completed self-question paragraph; Chapter XXVIII ends on PDF 221 immediately before the third-house heading. This batch adds **122 source records**, taking Lilly's cumulative inventory from **774 to 896**, and the combined Ptolemy/Lilly inventory from **1,840 to 1,962**. The wider source-complete, multi-author audit remains open. [Evidence: `RULES.json`, `SECTION_COVERAGE.json`, cumulative extraction indexes.]

The 122 rows comprise 69 XXVII records and 53 XXVIII additions. The separate reader supplied 54 XXVIII candidates; its case-introduction row was merged into the already extracted XXVII introduction, so the same passage is not counted twice. There is **one selected historical case**, **32 preserved unresolved items**, and **seven comparisons with retained source records**. Unresolved items include author discretion and missing outcome evidence as well as textual uncertainties; 32 is not a count of printing mistakes. [Evidence: `XXVIII_EXTRACTED.json`, `HISTORICAL_CASES.json`, `UNRESOLVED.json`, `CROSS_SOURCE_COMPARISONS.json`.]

The original 894-page witness matches the previously registered SHA256:

`2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`

The primary reader checked all 21 relevant original page images, PDF 201–221, alongside the existing text. A separate XXVII checker read 201–211 before reviewing its candidate records; a separate XXVIII reader read 211–222, with 222 used to establish the following chapter boundary. No new OCR was used. The raw PDF, full text and page images remain outside the repository. Page references below identify this exact witness. [Evidence: `READING_RECEIPT.json` and the separate reading/review receipts in `review/`.]

## 1. The question selects the applicable houses

Lilly distinguishes three questions that could otherwise be compressed into a generic wealth enquiry. [XXVII, PDF 201 and 207–209; R775, R819–R832.]

| Question | Querent and own money | Other party and that party's money | Source condition |
|---|---|---|---|
| General prospect of wealth | First and second houses | No particular donor assigned | No named person from whom fortune is expected |
| Recovery, borrowing or pledged goods from another person | First and second | Seventh and eighth | Ordinary comparable parties |
| Payment, wages or gain from a much superior person | First and second | Tenth and eleventh | Querent is much inferior to the expected payer |

The Moon and Ascendant lord also signify the querent. The eighth is the second counted from the seventh; the eleventh is the second counted from the tenth. These are explicit relationship-dependent frames. The reference helper requires the caller to name a frame; it does not inspect a chart and choose whichever frame produces a favourable answer. [Same passages; `QUERY_FRAMES.json`, `lilly_wealth_reference.py`.]

The general means-of-wealth discussion is itself conditional. Lilly first requires a judgement that subsistence or riches are promised, then examines the planet actually helping to bring them. His later enquiry into the cause of insufficient fortune belongs to an adverse judgement. Listing every helpful channel and every obstruction together would erase that distinction. All twelve house channels have been retained with their occupational, relationship and sign qualifications, including the sixth-house occupancy condition, Cancer/Pisces in the ninth-house sea-voyage clause, and Virgo's grain association distinct from the twelfth-house cattle signs. [XXVII, PDF 202–207; R792–R818.]

Fortune and both lunar nodes receive planetary aspects but do not themselves emit rays in this passage. A symmetric longitude calculation therefore does not make their interpretive roles symmetric. [XXVII, PDF 201; R777.]

## 2. Natural character, office, condition and reception remain separate

A malefic can signify acquisition when its dignity, helpful contacts or placement support that role. Conversely, Jupiter and Venus can obstruct when afflicted or serving as the obstructing significator. In the example, Mars retains its difficult qualities while acting as second lord, seventh lord and Fortune's dispositor. Lilly uses it for both performance and timing, while preserving labour and obstruction. [XXVII, PDF 206–207; XXVIII, PDF 216–217; R816–R817, R864–R874.]

Reception also has direction. A malefic **receiving** the querent's significators is not the same proposition as a malefic **being received**. Independent review found this direction blurred in two draft titles and one timing paraphrase; those were repaired. The source's ordinary recovery branch permits hardly-ever attainment or attainment with regrettable labour when reception is absent; the superior-payment branch uses a categorical denial. Neither has been substituted for the other. [XXVII, PDF 207–210; R821, R830–R833; `review/XXVII_CANDIDATE_FINDINGS.md`.]

The general hindrance discussion inside XXVIII gives a longer chain of conditions. Its records are linked as one required context so that a short rule cannot silently discard its exceptions. [XXVIII, PDF 218–220; R878–R892; `APPLICABILITY_AND_RELATIONS.json`.]

| Source situation | Qualification preserved |
|---|---|
| Ill-disposed evil contact without reception | Can prevent completion, including through an intermediary |
| Reception with an unfortunate contact | Can allow completion with weariness and solicitation, subject to later qualifications |
| Reception through square or opposition | Ill disposition can defeat it; the condition of the receiving and received planets matters |
| A well-disposed receiver | Reception through any aspect can perform the matter, including square/opposition |
| Sextile or trine without reception | Application, rather than separation, is expressly required |
| Translation to an impeded malefic | Fails unless that malefic is received in turn; the next receiver is not named |
| Malefic or unfortunate collector | Must receive both significators; receiving one is insufficient |

A particularly important passage allows another planet to interrupt the significators **before conjunction with the harmful planet**, thereby removing its harm and allowing completion. This prevents a universal classification of every abscission as either favourable or unfavourable: its effect depends on what contact is interrupted. [XXVIII, PDF 219; R884.]

Two sentences on PDF 219 remain difficult. One says that a planet receives relevant significators, then describes it as neither receiving nor received. Another omits an expected joining relation in an intermediary chain. Different senses of receiving may explain the first, but that is an interpretation. The source wording and unresolved status remain; no silent emendation becomes executable logic. [R882–R883; unresolved items U023–U024.]

## 3. The printed arithmetic reproduces, with a separate counting discrepancy

The calculation check uses the printed coordinates and the already retained geometry functions. It does not recalculate a historical sky. All seven antiscion entries and all seven opposite contra-antiscion entries reproduce. The seven planetary strength tallies and Fortune's separate tally also reproduce. [XXVIII, PDF 211–215; `WORKED_NUMERIC_TABLES.json`, `ARITHMETIC_CHECKS.json`.]

| Body or point | Fortitudes | Debilities | Net |
|---|---:|---:|---:|
| Saturn |6|14|−8|
| Jupiter |20|0|+20|
| Mars |21|12|+9|
| Sun |10|2|+8|
| Venus |23|5|+18|
| Mercury |18|5|+13|
| Moon |12|7|+5|
| Fortune |3|5|−2|

These totals do not exhaust Lilly's judgement. He describes Jupiter's platick square with Mars as some detriment without assigning it a numerical debit. Fortune is weak by its tally while receiving favourable fixed-sign and Mars-term testimony elsewhere. A correct sum is consequently not a complete wealth model. [XXVIII, PDF 213–216; R848, R854, R862.]

The motion list identifies **four swift planets**: Jupiter, Mars, Venus and Mercury. It explicitly calls Saturn, Sun and Moon slow. The later timing argument says **five** planets are swift. Both readings are visible in the original and remain in the data. The discrepancy check is expected to return false for agreement; a passing software test means the discrepancy was preserved. [XXVIII, PDF 212 and 217; R845, R872.]

Original-image checks also corrected readings that the text layer or earlier provisional summaries could mislead: Mars's daily motion is 35 arcminutes, Jupiter's stated mean 4′59″, the lunar transfer names Mercury rather than Jupiter, and the fixed-sign/Mars-terms clause refers to Fortune rather than Venus. The daily-motion values are source claims, not ephemeris-verified rates. [PDF 212,216–217; R845, R860, R862.]

## 4. Fortune is assigned across a boundary that exceeds five degrees

The chart prints Fortune at **Scorpio 0°10′** and the second cusp at **Scorpio 6°35′**, a difference of **6°25′**. Lilly explicitly acknowledges that Fortune is more than five degrees from the cusp, nevertheless assigns it second-house signification, and rejects first-house signification for this case. [XXVIII, PDF 211,214; R844, R854.]

The earlier retained visitor example excludes Mars from a following house because it is more than five degrees from its cusp. The current passage therefore matters when deciding whether a strict five-degree predicate could represent all Lilly house attributions. Both examples remain. This batch supplies no universal 6°25′ replacement threshold, and it does not alter the older reference function. [Retained B02f R714, PDF 188; current U021 and comparison C04.]

The same distinction appears more routinely for Venus: its printed position is 1°01′ before the eleventh cusp, yet Lilly treats it as on that cusp and uses the eleventh-house topic of friends. Geometric position between cusps and the source's attributed house are stored separately. [XXVIII, PDF 211,213,218; R851, R876; arithmetic output.]

## 5. Timing has several source methods and an explicit discretionary step

For the local distance-to-perfection method, Lilly's table is: [XXVII, PDF 209–210; R833–R835.]

| Houses of the selected significators | Symbolic unit per degree |
|---|---|
| Both cadent |Days|
| Both succedent |Weeks|
| Both angular |Months|
| Angular and succedent |Months|
| Succedent and cadent |Weeks|
| Angular and cadent |Months|

He then requires judgement about whether the business can actually be completed in the proposed unit and permits years instead of months for a long business. The text supplies no objective threshold. The helper returns only the named table's exact symbolic interval and carries the undefined override; it does not choose years, calculate a calendar date, or merge this table with the different timing scales retained from other questions. [Same passages; `TIMING_REFERENCES.json`, `lilly_wealth_reference.py`; comparison C02.]

Another route, attributed to some ancients, begins with two planets in the same sign **at the hour of the question**, then distinguishes the more ponderous Ascendant lord from the lighter one. The lighter-lord reception branch has following angular/domicile exceptions. The named joys here are zodiac signs—Saturn/Aquarius, Jupiter/Sagittarius, Mars/Scorpio, Venus/Libra and Mercury/Virgo—not a substitution of the separate mundane-house joy scheme. Lilly then distinguishes his own observation about single exaltation reception from domicile reception with benefic significators. [XXVII, PDF 210; R836–R841.]

In the worked case, the coordinates produce these distances: [XXVIII, PDF 211,217–218; R873, R875; arithmetic output.]

| Printed inputs | Calculated difference | Source interpretation |
|---|---:|---|
| Ascendant Libra 14°13′ to Mars Libra 16°12′ |1°59′|About two years; author reports a wife's portion at that time|
| Moon Leo 19°07′ to Venus Leo 25°34′ |6°27′|Later strong trade, reputation and friends about 1640, six years after the question|

The first distance is reasonably described as about two degrees; the second reproduces exactly. Neither calculation independently chooses the year unit. The six degrees27 minutes have not been converted into a spurious exact 6.45-year event date. Lilly himself says to mix art with reason for contingent timing. [PDF 217–218; R873–R877.]

## 6. Exact antiscia and a near contra-antiscion have different uses

Lilly says ordinary antiscia contribute little in the example because none meets an exact material cusp or planetary degree. He then uses Saturn's **near contra-antiscion** to Jupiter for kinship and servant cautions. The printed table gives Saturn's contra-antiscion at **Cancer 14°41′**, versus Jupiter at **Cancer 17°31′**: **2°50′ apart**. [XXVIII, PDF 215,220–221; R856, R894–R895.]

The distinction is retained without turning near into exact or assigning a new acceptable orb. His later warning about solar men who are friends also remains specific to that affliction; it does not retract the earlier proposition that other friends may help. No outcome confirmation is reported for those cautions in this section. [PDF 221; R895–R896.]

## 7. The reported evidence is narrower than all four questions

The case is selected and reported by Lilly retrospectively. He says the tradesman acquired a competent estate with labour and care up to the time of writing. He explicitly relays the man's report of wife-derived **money and land**, reports good trading, and places a wife's portion around the two-year interval. These are retained as reports, with their actual level of specificity. [PDF 211,216–217; R843, R863, R870, R873.]

The chapter does not separately document the entire **about 1640** trade/reputation/friends cluster at that date. Nor does it supply full-lifetime follow-up for continued wealth. Lilly narrows continued riches to competent fortune without poverty or want; he does not claim an unchanging balance or unlimited growth. The fact that the man prospered while married cannot verify the counterfactual that he would have prospered without marriage. [PDF 216–220; R864, R875, R893; `HISTORICAL_CASES.json`.]

The eight evidence entries in the case file are eight distinct targets or cautions within **one** case. They are not eight independent successes. No predictive accuracy, probability or causal effect is estimated.

## 8. Source uncertainties and review results

All 32 unresolved items have page and record references. The principal groups are: unclear clause attachment/reception direction; incomplete synthesis and timing rules; the explicit swift-count discrepancy; the case-specific cusp exception; exact versus near contact tolerances; and limits of the reported outcomes. [Evidence: `UNRESOLVED.json`.]

There is also a small unresolved **reader disagreement** over the historical chart minute: the primary and XXVIII readers favour 00, while the independent XXVII checker sees a 6-like glyph. Both readings are retained and neither minute is used in any calculation. Calendar/UTC conventions and a compact chart-centre shorthand also remain unresolved. The printed longitudes, used directly for static arithmetic, do not depend on resolving those items. [PDF 211; `WORKED_NUMERIC_TABLES.json`, U016–U018, reconciliation receipts.]

The independent XXVII check found useful fidelity repairs to diagnostic alternatives, sixth-house occupancy, reception direction, and the query-time anchor. Those corrections were made in both relevant statements and titles. An unsupported draft forward attribution about a north-node/Saturn rule was removed, and the introduction's author-reported experience was retained. Original findings remain frozen beside the reconciliation; reviewer agreement is not substituted for source evidence. [Evidence: `review/XXVII_CANDIDATE_FINDINGS.md`, `review/XXVII_RECONCILIATION.md`, current R794, R796, R800, R818, R821, R830, R833, R836–R837, R843.]

Seven comparisons with earlier audit records keep question frames, timing profiles, Fortune algebra, cusp exceptions, long-ascension aspect valuation and evidence dependence distinct. The Ptolemy comparisons use retained audited records rather than a new read of that book. His retained Fortune formula has the same algebra, but the record also preserves Robbins's authenticity doubt; shared algebra does not merge natal and horary doctrine. [Evidence: `CROSS_SOURCE_COMPARISONS.json`; retained B01j R335–R339.]

## 9. What the tests establish

The actual focused run passed **121 tests: 28 new B02g, 31 retained B02f, 30 retained B02e and 32 retained methodology/index tests**. Pytest also reported 35 subtests in the new suite; these are not added to the 121 distinct test count. The runner was Python 3.12 with pytest 9.1.1 in a scratch-only dependency directory. Exact commands and outputs are saved in the four `TEST_*.txt` files.

The checks cover source-data identity and context links, preservation of uncertainty, question-frame contrasts, exact symbolic arithmetic, printed strength and antiscion reconciliation, and deterministic regeneration. They do not certify the author's predictions, complete interpretation of every ambiguous sentence, a modern historical sky, or the full HumanDesign application. No runtime model is promoted, no personal outcome is fitted, and no earlier source dataset or personal prediction freeze is changed. Use the separate publication and delivery receipts and the manifest to establish those transfers; source extraction and test results alone do not establish publication or delivery.

## Exact continuation point

Continue at **PDF 221, printed 187, below the horizontal rule: the third-house heading and its introductory paragraph**, then proceed to Chapter XXIX on PDF 222, printed 188. The heading concerns brethren, sisters, kindred and short journeys. These following pages were previewed only to establish the boundary; their rules have not yet been extracted. Do not restart the completed second-house paragraph or skip its following preamble. [Evidence: original PDF 221–222; `SECTION_COVERAGE.json`.]

The reference code and all source records remain historical research material. The completed boundary is this second-house batch; the broader multi-author audit and later predictive evaluation remain open.
