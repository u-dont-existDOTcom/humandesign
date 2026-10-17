# Lilly Book III: natal chart-domain census versus the Life Patterns survey

**Source:** William Lilly, *Christian Astrology* (London, 1647), original archive item `b30338724`, *Contents of the third Book*, approximate printed pp.489–742 and later worked example. **Audit date:** 2026-10-17. **Evidence class:** original printed *table of contents*, transcribed by the archive's imperfect OCR. **Not a test of astrology's predictive accuracy.**

## Direct answer to the owner's question

The existing Life Patterns V7 questionnaire was developed primarily around choices and interpersonal scenarios. The original natal text is organized around a much wider set of **intellectual and behavioral dispositions, observed life circumstances, relationship histories, religious orientation and dreams, and prediction/timing methods**. The mismatch is systematic. Asking people what they *would* do in a group setting cannot, on its own, measure how their actual life has unfolded or what their most intense subjective experiences feel like.

The original 1647 scanned-volume OCR was retrieved and its complete byte stream verified against the already accepted independent Lilly Book III witness hash:
`7c08b55359c41049c5d43901b8da869a326f8eb852e4a30603a4b698533626aa` (2,005,702 bytes). The original Book III table of contents is located between decoded text-character offsets **86275 and 96952**. All **29** grouped rows in `LILLY3-NATAL-DOMAIN-CENSUS-v1.json` carry an actual original OCR anchor, an exact text excerpt, the anchor's reproducible offset, the printed-page indication, and a conservative V7 coverage disposition.

The inventory is **29 major source-topic groups, not all individual subheadings or fully extracted chart rules**. The original OCR interleaves columns, corrupts planet glyphs and sometimes prints page numbers incorrectly. This audit is therefore suitable for **finding missing measured subjects**, but **not** for constructing or testing a chart predicate before checking the original folios and full clauses.

## Coverage results

| Relation to existing V7 questions | Book III contents topics | Meaning |
|---|---:|---|
| No direct V7 question | **6** | Siblings, parents and family, historical domestic help/livestock, children, religious orientation, dreams |
| Only an indirect scenario proxy | **6** | Actual fortune, wealth, marriage history, travel history, honors/status, occupation |
| Partially sampled as behavior | **4** | Manners, understanding, real friendships, conflicts/enmity |
| Outside a behavior-only survey | **2** | Complexion/physical constitution; stature/appearance |
| Inappropriate as compulsory personality assessment | **4** | Longevity, illness, captivity, mortality/violent death |
| Astrological technique rather than a human trait | **7** | Birth-time rectification, preliminary natal methods, lord of geniture, directions, profections, revolutions, transits and worked examples |

The classifications are **researcher-coded coverage**, not inter-rater-validated psychometric statistics. “Proxy” means a nearby V7 scene involves a related action; it is **not** a measurement of the stated real-life outcome. “Not a participant trait” does not mean the astrological *method* is useless; it means asking a person how often they experience a calculation technique would be a category error.

## Additional topics the original chart tradition names

**Mind and habitual character** (original printed pp.532–545): Lilly lists complexion/temperament, manners, and the native's understanding. V7 has some relevant scenes about coping, relationship behavior, learning and reasoning, but cannot be treated as a comprehensive measure of intellect or lifelong personality. The earlier Ptolemy III.13 ledger separately lists religion, intellectual/philosophical interests, divination and dreams.

**Actual life and relationships** (pp.551–648): Original contents include wealth and how obtained, actual siblings and relations with parents, marriage and children, journeys, public dignity, vocation, friendship quality, conflict and captivity. These are different from a scenario probe about using extra money, booking a trip, joining a group, or deciding when to rest. Some historical categories are culturally obsolete or intrusive and would require separate sensitive opt-in if ever studied.

**Spiritual orientation and dreams** (pp.611–614): Book III *explicitly* has natal sections for a person's religion and dreams. These were already extracted in the accepted independent chapters CXLII–CXLIII source study (31 provisional source units) and are cross-referenced here, **not counted as new predictions**. It separately recorded that Lilly denied stellar compulsion of the person's actual religion and that planetary signs must be checked against facsimile images.

**Timing methods** (pp.651–742): Directions, annual profections, revolutions, and transits occupy extensive space. These are calculation and forecasting mechanisms, not respondents' reported personality traits. Their life-event claims require accurate occurrence windows and chart calculations to test prospectively, not more generic opinion questions.

**Body/health and high-stakes events:** Original topics include physical stature, bodily illness, longevity, imprisonment, and types of death. Cataloguing their historical presence does **not** justify asking respondents invasive questions or using a natal chart for medical or mortality advice. Those claims may be documented historically while excluded from ordinary personality assessments.

## Where awe, wonder, synchronicity and personal meaning fit

This broader contents audit supports the owner's diagnosis of **missing first-person experience** but does not magically supply precise frequencies and chart rules for it. The historical religion/dream sections, and Ptolemy's discussion of mysteries, omens and philosophy, offer **adjacent source subjects**. The checked Lilly Book III contents do **not** label separate headings for the daily frequency of awe, how often someone is shocked by themselves, synchronicity noticing, or the strength of existential meaning. That is a statement about this particular *contents section*, not a claim that no astrology writer ever discussed those experiences.

Keep the neutral **optional** experience-and-meaning pilot (four short starting prompts; eight domains available) and optional religion/dream pilot outside the current GPT and existing interviews. Pilot comprehension and response variation first; do not convert self-report into a desired chart match. A related source term is not an empirical validation or a license to assign chart points.

## What a complete astrology-aligned instrument would need

There are at least **three different target classes**, each requiring different measurement and validation:

1. **Disposition and phenomenology:** habitual character, awe, surprise, meaning, dream recall, interest in learning or divination. Use nonleading, optional first-person questions, with frequency, intensity, real-life context, developmental change and unknowns distinguished.
2. **Life events and biography:** actual career, relationships, family, travel and dated transitions. When voluntarily reported, preserve source quality, timing and non-disclosure. External events cannot be inferred from hypothetical scenario answers.
3. **Astrological calculational or forecasting rules:** rectification, significators, direction/profection/return systems. These require source-authenticated equations, planetary glyph checks, birth-time uncertainty, prospective event predictions and matched null models, **not** respondent questions about the rule names.

Sensitive medical/violence/mortality topics should remain historical-source records rather than personality predictions.

The **next source work** is chapter-body rule-level extraction and original page-image corroboration of the actual predicates, beginning with high-value, ethically measurable domains such as understanding, character, profession, creativity and worldview. Compare astrology-derived predictions against non-astrological baselines on people whose birth data and answers were not used to devise those rules. A person whose story inspired a question is a **development participant**, not an untouched validation win.

## Source and scope references

- Lilly original Wellcome volume, 1647: https://wellcomecollection.org/works/s7z7c46y
- Original public OCR witness, Internet Archive: https://archive.org/download/b30338724/b30338724_djvu.txt
- Previously accepted natal religion/dream rule index: `tasks/lilly-book3-religion-dreams-coverage-20261017/`
- Previously accepted Ptolemy III.13/IV and Lilly house-topic audit: `tasks/astrology-phenomenology-source-anchors-20261017/`
- Original neutral 79-question V7 bank: `tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json`

**Scientific boundary:** No natal chart was calculated, no ASTROHD/HD mapping changed, no participant response was accessed, and no live questionnaire was modified.
