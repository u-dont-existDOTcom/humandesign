# Life Patterns — first-person experience pilot v1

**2026-10-17. Status:** Optional, separately versioned, offline development instrument. Not live, not psychometrically validated, and **not used to score astrology, Human Design, diagnoses or earlier interviews**.

## Original owner outcome and corrected scope

The owner wants to understand why the survey missed awe, sudden personal revelations, surprising people/world/self, predictability, perceived higher guidance, synchronicities, and felt meaning—and what other important human experiences it has overlooked. Improve actual survey coverage **before** pursuing further historical astrology research. The completed Ptolemy/Lilly source audits provide context only and cannot turn a candidate construct into a tested chart prediction.

## Current instrument comparison

The historical V7 bank contains 79 question/route entries primarily about plausible behavior in scenes. The active tendency-first v1 has 25 direct-behavior items; the 25-item V3 scaffold is not activated. Neither bank adequately samples the eight original felt-experience domains. The separate domain ledger crosswalks these banks and names other uncovered first-person areas. Its categories are qualitative judgments, not exhaustive source-corpus coverage or proof of predictive validity.

## Pilot interaction and admission

1. Obtain **separate opt-in**. In the offline version, participants are informed that the page has no server connection or autosave. It is not an invitation to redo the full interview.
2. Check any prior interview evidence (if authorized). Only skip a new item as **ALREADY_COVERED** when the source directly answers that item's *specific question and time period*, with an actual source reference. A nearby scenario, source-topic label or speculative chart claim is not sufficient.
3. Start with EM01 self-surprise, EM03 awe, EM04 sudden realization, EM08 personal/social meaning. These are four cards; EM08 has **two separate response fields** rather than conflating meaning with worldly impact.
4. After those, offer four other topics in a neutral menu. EM02 surprise about people/world, EM05 life predictability, EM06 perceived guidance and EM07 meaningful coincidences are participant-selected. Do not infer absence of an experience from not selecting its topic. Selection is never evidence of high frequency.
5. Ask one direct question per card. Positive-frequency answers can open one **optional** intensity/context clarification. A report of never, uncertainty, refusal, or sufficient earlier evidence is complete; do not manufacture a follow-up.
6. Keep frequency, felt strength, valence/meaning, later reappraisal, action change, personal meaning and perceived impact distinct. The past year is the primary recall frame; present meaning is a current-state report. Earlier-life differences may be volunteered without forcing a retrospective timeline.
7. Preserve answer states: NOT_ASKED, ANSWERED, NEVER, UNKNOWN, SKIPPED, ALREADY_COVERED. No response counts toward a chart score; no imputed zero or personality trait for unknown, missing or skipped data. Don't code religious skepticism as a lack of awe, or a vivid coincidence as proof of external guidance.
8. Permit editing and exporting. Offline exports contain no birth data by default. Never upload, merge into prior respondent records or promote to production automatically.

## Additional neglected human-experience domains

The ledger identifies dream experiences, creativity/aesthetics, play/humor, family and home identity, worldview and spiritual practice, identity change, community belonging, cultural exploration, ordinary sensory life and actual turning points. **None** is a compulsory new question yet. The first next-module candidates are dreams, creativity, family/home (fully optional), and playfulness. Decisions to include them should be based on distinct measurement value and participant burden—not merely because astrologers discuss a related topic. Medical/trauma/death forecasts are outside routine personality interviewing.

## Evidence plan and constraints

Use **adapt/experiment** rather than reinvent scales: research context already identifies AWE-S (awe experience), MLQ (presence/search of meaning), and DSES (daily spiritual experience). The custom wording is not any validated scale, nor a composite of their licensed items. Against the minimal baseline of the eight old prompts, test readability, neutral wording, participant burden and whether the split constructs are distinguishable. Next test response variability and repeatability with new, separately consented development volunteers; defer any chart predictions until pre-registration and an independent untouched cohort. No live Railway credentials, participant records, private responses or production Action schema were accessed or modified by this task.

## Reproducible checks

- python3 -m pytest tests/unit/test_life_patterns_experience_pilot_v1.py -q
- python3 tasks/life-patterns-experience-pilot-20261017/build_offline_pilot.py
- Browser sanity check: opt-in, four default cards, no question duplication, optional topic menu, never/unknown/skip, edit answers, export and import, no network/autosave.
- A passing structure test means functional implementation, **not** validation of these constructs or of astrology.

The owner-only Custom GPT editor upgrade to Railway v1.8 remains a separate human action. This pilot does not change it.
