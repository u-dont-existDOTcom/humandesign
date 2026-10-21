# External GPT questionnaire — answer preservation and survey design integration

**2026-10-21. Research candidate + private owner data merge.** The attached source was an OpenDocument Drawing with 31 numbered questions and seven pages. The user explicitly identifies the responses as their own, though the questions originated from another person's GPT. We did not receive independently verified frozen prediction files.

## Personal survey: completed and exact

The user's latest verified existing personal stack, containing the V3.3 25-item interview and three unusual-behavior records, the separate 84-turn primary interview, three CF003 answers and eight lived-experience answers, remains embedded **unchanged** inside the newly generated private self-survey master. The external form was appended as another clearly identified source: 26 historical answers, of which **21 have a substantive selected choice (17 affirmative, four negative)** and five have an explicitly selected missing/unclear option; the five future outcomes are unanswered. No missing or future item was converted to a false answer. Source evidence notes and reference windows are preserved.

The exact private archive, its original SHA-256 and the ODG raw source digest were checked on the authorized owner computer. This public repository intentionally does **not** include those private content hashes or participant answer texts. An apparently related 96-turn interview was checked against its declared source and conclusively identified as a different person's record; it was excluded. This is a source-stack merge, not a new combined/averaged personality scale. Older answers and newly appended answers are not guaranteed independent even if the topics overlap.

**Private recipient folder:** the owner computer's Downloads / Life-Patterns-External-C-Import-20261021, with restricted permissions. It contains (1) the lossless machine-readable combined master, (2) 31-item source extract, (3) a human-readable full 31-answer appendix. No original files were overwritten or private responses pushed to GitHub.

## Source audit: all 31 question designs reviewed

Each original item Q01–Q31 has a typed, source-bound disposition and reason in `EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json`. Counts:

| Research design disposition | Number |
| --- | ---: |
| Adapt as observable actual activity or life history | 15 |
| Offer a narrowly conditional question only if unanswered | 7 |
| Reject arbitrary aesthetic spending as personality proxy | 1 |
| Reject forced either/or social choice | 1 |
| Link overlapping events without counting them twice | 2 |
| Preserve future forecast in a separate outcome-evaluation lane | 5 |
| **Total** | **31** |

### Strongest features to adopt

1. **Actual reported activity as well as preferences:** education, vocational history, leadership, teaching, creative output, meditation and long-term relationships can be asked as things that happened, not only hypotheticals.
2. **Useful recall periods and exposure denominators:** count how often a situation occurred, rather than claiming an absolute cut-off equals a durable trait.
3. **Continuity and change over time:** identify sustained and changing patterns without leaking dates derived from a participant's birth chart.
4. **Verbatim respondent clarification:** preserve exact meaning when the person's scope differs from the author's boxes; never turn “depends” or “unclear” into a “no”.
5. **Independent third-party descriptions as separate provenance:** specific other-person feedback is useful context, not an automatically confirmed self-trait.
6. **Prospective future outcomes isolated:** preserve future items as pending and do not count them as responses or empirical predictive hits without a separately frozen, independently verified score key and elapsed window.

### Weak design features rejected or repaired

The original source imposes several absolute hour/count/money and paid-work thresholds which may be sensible *operational outcomes* for a preregistered future prediction but are weak generic **personality** measurements. It conflates salary with doing productive work, home decor spending with aesthetic taste, and one incident with a repeated tendency. Some categories do not fit informal work, creators, self-employment or ambiguously classified activities. A forced one-to-one-versus-group choice ignores the role of actual participants and reasons. A forced five-attribute relationship priority ranking can hide all the respondent's own qualities, ties and real ordering. Overlapping dated moves or education may be one piece of evidence repeated in different reference windows. The external document's claimed freeze time alone cannot establish real preregistration or verify its predictive performance.

## Revised version: actual research instrument, not just recommendations

Built a full `LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json`:
- **All 23 earlier optional topic questions preserved literally**, with their full previous prompt and follow-up, source hashes, eligibility rules, precise evidence class and answer recording dimensions.
- **Seven optional conditional microprobes** for observed evidence/reasoning, externally given feedback, chosen reflective solitude, voluntary group departure, leadership preference versus actual roles, self-authored partner priorities, and project completion/change/abandonment relative to started projects. They only appear when a prior answer genuinely leaves a relevant issue unresolved.
- Current eight EM experience questions and 25 TF1 direct questions are pinned by hash and otherwise unchanged.
- Cumulative admission defaults: zero compulsory new questions, at most five participant-selected optional topic questions and at most two conditional follow-ups per sitting; valid states include CONTEXT_DEPENDENT, NO_OPPORTUNITIES, UNCERTAIN, SKIPPED, NOT_APPLICABLE, NEVER and ALREADY_COVERED.
- The five previously unobserved future items are excluded from the live survey question pool. They belong to an evaluator-only future-outcome lane.

The practical interviewer version is `INTERVIEWER-V3-DESIGN-DELTA.md`. The human-review matrix is `ITEM-DISPOSITION-SOURCE.psv` and the machine matrix is `EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json`; all deliberately omit identifying dates, respondent notes and marked choices.

### Why no live deployment in this task

The user's self answers are **development data**. Incorporating an external prediction questionnaire directly into the frozen model, an active ChatGPT GPT Action or the production Railway interface would change validation conditions before its effectiveness and burden were checked. A separately versioned additive research instrument answers the requested design integration, while keeping the existing live interview intact. Pilot its actual quality and duplicate-question avoidance first; any subsequent GPT/Railway deployment needs ordinary controlled versioning, not retrospective chart-score repairs. No claim of astrological predictive validity was made.

## Files

Public, generic: PLAN.md, RESULT.md, INTERVIEWER-V3-DESIGN-DELTA.md, ITEM-DISPOSITION-SOURCE.psv, CONDITIONAL-MICROPROBES-v1.json, LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json, EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json, build_adaptive_survey_v3.py, merge_owner_personal_results.py, render_private_personal_import.py, verification tests and machine receipt.

Private, on owner laptop: exact combined master, exact 31 extracted responses and a readable 31-response appendix. Only this private destination contains the actual identifying reference windows and original response notes.
