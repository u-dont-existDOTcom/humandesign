# Astrology source audit: marriage and children

Date: 2026-10-06. Batch B01k. Source: Ptolemy, *Tetrabiblos*, F. E. Robbins's 1940 translation, supplied 1964 reprint. Bounded comparison: Rhetorius, James Holden's published 2009 translation, supplied PDF and owner OCR.

## Completed scope

The full English text of IV.5 (marriage) and IV.6 (children), together with the relevant English notes, is read and extracted. The span starts at the marriage heading on PDF417/printed393 and ends before friends/enemies on PDF437/printed413. All eleven English pages were visually inspected; five English-note starts on facing pages were also checked. Greek text and the complete critical apparatus were not independently translated or collated.

| Measure | Result |
|---|---:|
| IV.5 source records | 73 |
| IV.6 source records | 20 |
| New source records | **93** |
| Cumulative Ptolemy source records | **500** |
| Ptolemy chapters/sections read | **44 of 61** |
| Conditional spouse-description rows | **10** |
| Continuity/quality combinations | **4** |
| New targeted Rhetorius comparisons | **3** |

Books I and III remain complete. Six of ten Book IV sections are now read. Four Book IV sections and all thirteen Book II sections remain unaudited. Counts describe source records and data representations, not independent predictions or successful human trials.

## 1. The same word can require different astronomy

In IV.5, Ptolemy explicitly gives different meanings to eastern quadrants for the Sun and Moon. The solar definition refers to the portions preceding the rising and setting signs. The lunar definition refers to the phases from new Moon to quarter and from full Moon to the next quarter (PDF421/printed397).

Consequently, putting the Moon into the same natal-house quadrant calculation as the Sun would not reproduce this passage. The bounded reference helper classifies directed lunar elongation only. It refuses to apply that formula to the Sun and leaves exact new/full/quarter boundaries unresolved because their ownership is not specified. It does not turn phase labels into a marriage prediction for anyone.

The corresponding age claims also preserve a disjunction: marrying young **or** marrying someone younger; marrying late **or** marrying someone older. The chapter does not provide a numerical age threshold (PDF417-421/printed393-397).

## 2. Endurance and relationship quality are explicitly separate

The chapter first describes cross-chart trines/sextiles between luminaries as generally supporting lasting marriage, with special emphasis on the husband's Moon and wife's Sun. Then benefic or malefic testimony modifies the quality of the relationship. The resulting source combinations are (PDF421-423/printed397-399):

| Luminary relation | Further testimony | Source description |
|---|---|---|
| Harmonious | Benefic | Lasting baseline, with pleasantness, agreement and benefit |
| Harmonious | Malefic | Quarrelsome, unpleasant and unprofitable; not here reclassified as divorce |
| Inharmonious | Benefic | Not completely terminated; renewals and recollections preserve kindness and affection |
| Inharmonious | Malefic | Divorce with abuse and violence |

These are historical claims, not a validated compatibility or relationship-safety model. Their methodological value is that continuity, affection, conflict, benefit and separation must not be collapsed into one good/bad score. Mixed testimony is not resolved by selecting the most flattering cell: the helper retains both supports and marks the mixture unresolved.

## 3. A description of the partner is not a description of the native

The opening spouse-description method uses the native's Moon to describe a wife and the native's Sun to describe a husband within the source's historical male/female framework. Later, the enquiry changes: Mars is used for the male native's own disposition toward love, Venus for the female native's (PDF419-421 and429-431).

The ten spouse-description rows now preserve both the enquiry and the subject being described. They cannot be retrieved as a generic description of the native. This is a source-specific role distinction, not a modern gender-identity classifier.

The Venus-Saturn passages further show why context matters. One spouse-description branch concerns sexual sluggishness; another concerns thrift and family affection. In the later other-union enquiry, Venus with Saturn is described as producing pleasant, firm unions, while adding Mars brings instability, harm and jealousy (PDF419,421,425). These are not faithfully represented by one universally positive or negative Venus-Saturn rule.

## 4. The children chapter does not begin with a generic fifth-house rule

IV.6 begins with planets connected with the Midheaven and its succedent, the Good Daemon, then uses the opposite places only in default of the primary planets (PDF433/printed409). Robbins identifies the Good Daemon as the eleventh place/house. The helper preserves primary-versus-fallback selection and does not mistake an unknown primary calculation for an empty result.

For this topic, the Moon, Jupiter and Venus are the giving group; the Sun, Mars and Saturn indicate few or no children; Mercury is common according to association and has an additional morning/evening modifier. Robbins reports the Anonymous's explanation that both sects here means donative/destructive groups, **not ordinary day/night sect** (PDF433-435/printed409-411). That gloss is separately attributed, not smuggled in as a new universal taxonomy.

The source also distinguishes complete childlessness from offspring who are born but subsequently suffer or do not endure. It separately treats number category, condition, status, affection toward parents, inheritance and relations among the children. These cannot be substituted for one another when scoring later predictions. The claims are historical, not fertility or medical guidance.

The concluding instruction uses the child-giving planet as a horoscope for a more particular enquiry. That is a changed reference within this method, not the child's independently observed natal chart (PDF437/printed413).

## 5. Ambiguity is preserved before implementation

Eighteen unresolved items are recorded. Particularly consequential ones include:

- Single-figure and application-count marriage clauses can support different number categories simultaneously; no priority is supplied.
- The adopted English plurality clause says bicorporeal **and** feminine, with a separate fecund-sign alternative. It has not been silently changed into an easier OR test (PDF433).
- A passion-with-restraint clause follows the male Mars-Saturn clause without expressly repeating Saturn, and precedes a no-Saturn clause. Its inherited scope matters (PDF429).
- In the female disposition sequence, Robbins adopts **Saturn** absent while Camerarius has **Jupiter**. A smoother interpretation is not permission to change the adopted text (PDF430-431).
- Leo and Virgo are examples of sterile places, not an asserted exhaustive universal list. The places/signs wording also has a transmission note (PDF432-433).

The historical descriptions of sexuality, coercion, social rank and family unions are preserved with their conditions and their source attribution. They are not converted into modern diagnoses, identity inferences or allegations about any actual person.

## 6. Rhetorius supplies a caution, not independent confirmation

In chapter104, Rhetorius discusses difficulty declaring exact numbers of siblings, marriages and children, recommends the safer category many, but then says he will still attempt the matter as far as possible. Holden also quotes a Byzantine epitomator's version separately (PDF140-141/printed152-153). Quoting only the hesitation would falsely turn this into a blanket rejection of numerical work.

Chapters105-106 use different qualified planetary groupings and a broader sterile-sign list in a **sibling** enquiry. Those are retained under that topic. They are neither independent empirical confirmation of IV.6 nor proof of a direct contradiction with Ptolemy's non-exhaustive examples for offspring. There are now eleven targeted comparisons across the audit; the full Rhetorius audit remains open.

## Verification and preservation

The isolated B01k suite passed **59 tests**. These check phase-reference geometry, exact-boundary abstention, all ten spouse rows, the four relationship cells, mixed/unknown testimony, primary/fallback selection, topic-specific planetary groups, AND/OR handling, conflicting clauses, input rejection and source/coverage integrity. They do not prove actual natal qualification, independent semantic review or predictive validity.

The combined integration suite passed **345 tests**: 59 new reference checks plus 286 retained checks. The exact command, exit code and measured test duration are saved in `VERIFICATION.json`.

All earlier source batches, runtime code, fitted astrology/numerology candidates and personal prediction freezes remain unchanged. Only four existing source-progress documents are advanced. Raw PDFs, complete OCR and page images stay outside Git. No new OCR or paid acquisition was performed.

## Next saved batch

**B01l: IV.7-IV.8**, friends/enemies and foreign travel. Start at PDF437/printed413; travel begins PDF447/printed423; stop before IV.9 on PDF451/printed427. These headings have been located, not counted as complete reading.

The parent source audit remains OPEN under the owner's multiple-pass plan. No unattended work is claimed after delivery.
