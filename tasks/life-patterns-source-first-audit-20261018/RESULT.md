# Why the Life Patterns survey missed other astrological chart domains

**2026-10-18 · Source-first questionnaire audit v2 · Survey design, not predictive validation**

## Decision

The owner identified a real omission. Earlier development completed **some** source-to-survey audits, but not the full requested source-inventory-to-measurement acceptance. The accepted first pass checked 17 anchors from Ptolemy's natal soul chapter and Lilly's *introductory horary house-topic* discussion, followed by nine Ptolemy Book IV life-domain summaries. It then delivered the owner's eight experience questions and a live completion flow. That did **not** answer whether the *other* astrological subjects were covered.

This audit resumes that neglected objective without allowing the separate full-book transcription lane to take over the questionnaire. It compares the original V7 79-route bank, TF1's 25 question bank, the eight recently released EMv2 items, and the separately versioned historical-rule claims. Source correspondence is **not** predictive accuracy; no chart rule or stored participant answer is updated here.

## What the expanded evidence actually covers

| Source boundary | Documentary entries included | Evidence strength |
| --- | ---: | --- |
| Ptolemy, *Tetrabiblos* III.13 natal soul/character | 15 | 13 earlier passage anchors and two new directly checked passage topics (Mars initiative; Mars–Venus playfulness); no validated personal predictions |
| Ptolemy, *Tetrabiblos* IV.2–10 natal life history | 9 | Source-level chapter descriptions, NOT fully extracted conditional natal algorithms |
| Lilly, *Christian Astrology* Book III, original 1647 natal table of contents | 29 | Original contents headings only; no warranted individual rule inference |
| Lilly, Book III natal religion and dreams | 31 | Two textual witnesses; committed v1 retains unresolved astrological glyphs, not scored |
| Lilly, introductory house-topic text | 4 | *Horary/house topic*, not proof of a natal claim |
| Varāhamihira, *Brihat Jataka* XV.1–4 | 4 | Online Sanskrit with secondary English; verse-level descriptions about ascetic initiation/renunciation, some translation uncertainty |
| **Total** | **92** | **Documentary records, not 92 independent testable predictions** |

The resulting crosswalk contains **46 normalized human/outcome domains**. Of these, 32 have at least one related historically attested source record in the **bounded sources above**; 14 are explicitly marked modern extrapolations or other survey constructs. For the full 46-domain set the historical V7 classification is **18 absent, nine partial, 13 proxy-only, six not routine participant questions**. These are authored construct-level judgements, not psychometrically verified coverage rates. Among the 32 source-attested areas, six are outside an ordinary personality interview, and **13 participant-facing historical topics are absent from V7, TF1 and all eight EMv2 items**.

No prior source is interpreted to claim a calibrated *frequency of awe*, *rate of being surprised*, *synchronicity frequency*, *life's subjective meaning score* or *how much higher guidance one feels*. The eight EM questions capture first-person experiences that are **only adjacent to** some classical concepts. This is precisely why the source audit must not be retroactively read as confirming those mappings.

### The 13 previously omitted attested areas

1. Actual religious/spiritual orientation (different from perceived divine guidance).
2. Actual spiritual/religious/ritual practice (different from conviction or awe).
3. **Deliberate renunciation or religious initiation** (from *Brihat Jataka* XV; separate from ordinary spiritual practice).
4. Major changes/conversion in philosophical or religious commitments.
5. Interest in mysteries, divination, hidden matters and methods for deciding what is true.
6. Actual dream content and emotional tone.
7. Dream recall, remembered significance and practices of dream interpretation.
8. Making things creatively rather than solely valuing them.
9. Actual appreciation or involvement with music/beauty/art.
10. Ordinary playfulness, dancing/humor or spontaneous enjoyment.
11. Actual long-term relations with siblings and kin.
12. Parents, household roots and belonging to home or place (the *belonging* outcome itself is a modern extrapolation from a household topic).
13. Actual parenting/offspring or caregiving roles, when relevant; never a fertility prediction.

**Other meaningful deficits are not technically wholly absent, but were represented mostly by adjacent hypothetical choices**: real occupation/vocation; wealth fluctuations; public recognition and authority; marriage and long-term relationships; relocation/foreign travel; major phases and dated life events; durable friendship/conflict. The earlier hypothetical questions about a trip, a windfall, recognition, social planning or work energy do not recover those histories.

## The chart mapping itself also fails a source-fidelity check

The project's separate CF003 mapping assigns ten planetary labels to ten development-stage behavioral meanings. Its source record explicitly says nine meanings descend from the project's prior Human Design role lineage, and one Sun-purpose construct is an added development proxy. **This is not the same as translating Lilly/Ptolemy/Varāhamihira natal predicates.** The chart and measurement sides are both incomplete.

A few examples:

| Current CF003 role | Checked classical passage treats instead/additionally | Assessment |
| --- | --- | --- |
| **Venus = values, ethics, boundaries** | Ptolemy explicitly discusses creative, aesthetic, pleasant-dream and affection qualities for particular Venus configurations | Substantial narrowing; art and beauty not measured by the Venus ethics target |
| **Moon = recurring motivational pressure** | Ptolemy starts with the Moon in assessing the sensory/emotional qualities of the soul alongside Mercury | Different construct emphasis |
| **Mercury = speech and messages repeatedly expressed** | Ptolemy includes inquiry, reason, learning, calculations and invention | Communication captures only part |
| **Jupiter = opportunity/growth principles** | Ptolemy also presents reverence, religion and generosity | Partial overlap with major omitted subjects |
| **Mars = assertion/direct action** | Ptolemy combines Mars with Venus for playfulness and artistry in a particular qualified configuration | Some direct overlap, but single-planet roles miss joint conditions |
| **Pluto / Uranus / Neptune** | Not planets in the checked ancient/1647 seven-planet clauses | Requires separate modern-source mapping; not evidence that all modern outer-planet astrology is wrong |

The full **ten-role** audit is in `CF003-PLANET-MAPPING-GAPS-v1.json`. The original natal claims often depend on **combinations, aspects, essential dignity, chart houses/house rulers, lots and timing**, not a single planet-to-personality-label assignment. The questionnaire can be improved now, but any attempt to score its new answers using these classical rules requires **separately frozen chart conditions and independent tests**. Existing CF003 mappings and scores have not been changed.

## Prioritized new survey design

The attached `ADAPTIVE-QUESTION-CANDIDATES-v1.json` contains **16** brief, neutral topic candidates. None is compulsory or currently in the deployed GPT/Railway questionnaire. The participant should select the topics they find relevant and unanswered, **up to five optional topics in one session**, with previous-source de-duplication. Never ask all sixteen merely to reach exhaustive coverage.

Highest-value offerings based on **distinct measurement value**, not the number of historical statements:

| Candidate topic | Initial question (shortened here) | Unique distinction |
| --- | --- | --- |
| **DREAM** | How often do you remember dreams in a typical recent month? | Recall vs content vs assigned meaning |
| **BELIEF** | What spiritual, religious, philosophical or secular practices, if any, recur in your life? | Practice vs belief vs felt guidance |
| **RENUNCIATION** | Have you ever deliberately withdrawn from worldly goals/status or adopted a more ascetic life? | Vows/retreat/actual life phase vs spiritual experience |
| **BELIEF_CHANGE** | Have your important convictions been stable, gradually revised or suddenly transformed? | Long-term worldview vs single insight |
| **ART** | How often do you **make** things creatively; separately, how often does art/music/beauty matter? | Production vs appreciation |
| **MYSTERY** | How often do you investigate hidden or philosophical questions? | Interests/practices vs belief in coincidences |
| **TIMELINE** | What up to three turning points divide your life into a before and after, roughly when? | Actual events vs inner change and date confidence |
| **VOCATION** | What work or calling have you actually pursued across your life? | Life role vs hypothetical work energy |
| **HOME** | Where and with whom, if anywhere, do you feel belonging or home? | Actual family/place belonging vs group-role preference |

The other **seven**, offered separately and with explicit opt-out, concern actual kinship, lasting bonds, foreign travel/migration, status, finances, parenting/caregiving, and playfulness. Sensitive health, death, incarceration, sexual and reproductive diagnoses are **not** added as routine questions simply because classical texts mention them. No chart-derived high-stakes recommendation is justified.

### Questionnaire method rather than sixteen extra demands

1. Preflight each optional domain against the participant's entire existing source; do not re-ask sufficiently covered facts.
2. Offer a short neutral topic chooser. A participant can pick none or stop at any point.
3. For subjective experiences, capture **frequency and typical versus peak strength** only when applicable. For real events, capture **what happened, approximately when, internal/external/both and recall confidence**, never force exact age/date.
4. Keep worldview disclosure, money history, family history and romance voluntary. Not relevant, never, declined and not asked are different.
5. Do not automatically interpret responses using natal predictions. Future chart-rule testing needs prospective hypotheses, independent samples and non-astrological comparison baselines.
6. Compare wording and burden to existing MADRE dream measurement, Creative Achievement Questionnaire and event-history calendars before adopting bespoke multi-item scales.

## What this pass does **not** finish

This is a reproducible **source-census and construct audit** against selected source-backed western natal texts plus the four-verse *Brihat Jataka* XV extension. It is **not** a full validated rule extraction of Lilly Book III, complete Hellenistic Valens/Dorotheus, Jyotish classics beyond this section, Dariot's full natal study, or modern psychological astrology. It cannot certify no further domains remain. Any comprehensive-all-traditions claim would be false without the book-lane corpus finishing and a subsequent source-linked rerun.

The proper next gate for a **live** questionnaire revision is pilot discrimination and burden of these candidates against existing answers. The separate original-source astrology extraction lane may later provide further attestations, but does not need to delay this questionnaire audit or convert every historical prediction into a compulsory user question. The audit file has no owner birth details, private participant answers or hidden score targets.

## Primary/source readings and prior-art references

- Ptolemy, *Tetrabiblos* III.13, actual natal mind/character, art, dreams, play and religious practices: https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/3D%2A.html
- Ptolemy, *Tetrabiblos* IV.2–10: https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/4A%2A.html (plus 4B, 4C).
- Lilly, 1647 *Christian Astrology* Wellcome original: https://wellcomecollection.org/works/s7z7c46y; pinned Book III natal TOC and religion/dream witnesses are exact-source-hash snapshots in this task.
- Varāhamihira, *Brihat Jataka* XV.1–4, online Sanskrit/translation with explicit ambiguities: https://vedicpupil.in/library/books/brihat-jataka/chapter-15; chapter index https://www.exoticindia.com/book/details/brihata-jatakam-of-varaha-mihira-nac247/
- Schredl et al., *Mannheim Dream questionnaire*: https://journals.ub.uni-heidelberg.de/index.php/IJoDR/article/view/16675
- Carson, Peterson & Higgins, *Creative Achievement Questionnaire*: https://doi.org/10.1207/s15326934crj1701_4
- Belli, *Event History Calendar* retrospective recall: https://pubmed.ncbi.nlm.nih.gov/9829098/

## Files and evidence of completion

- `SOURCE-TO-SURVEY-CROSSWALK-v2.json` — 92 source rows and 46 domain statuses, with version/claim-class tags.
- `CF003-PLANET-MAPPING-GAPS-v1.json` — all ten current planet/meaning mappings versus original text.
- `ADAPTIVE-QUESTION-CANDIDATES-v1.json` — sixteen optional, neutrally worded question candidates.
- `DOMAIN-REGISTRY-SOURCE.psv` — authored source/measurement comparison, explicit version.
- `input-snapshots/` — byte-checked Lilly natal contents and religion/dream candidate rules.
- `build_crosswalk.py` — deterministic source claim/coverage assembler and completeness assertions.
- `tests/unit/test_life_patterns_source_first_chart_audit_20261018.py` — source total, no chart scoring, evidence-class guard, candidate-domain link, ten planet-role checks.

**Status:** Survey-design research, not deployed, not scored, not a participant-result amendment.
