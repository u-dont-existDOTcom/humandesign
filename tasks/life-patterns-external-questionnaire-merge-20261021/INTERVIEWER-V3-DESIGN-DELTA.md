# Adaptive Life Patterns v3 — interviewer delta from an external questionnaire

**Status:** Research instrument candidate, not active in the existing GPT or Railway service. Works *alongside* the frozen V7, 25 TF1 tendency questions, eight optional EM questions, and the 23 candidate topics; does not invalidate or recode earlier completed responses.

## What this changes

The external questionnaire's best contribution is to insist on **observable real-life history**, clear time frames, and a response/evidence note. The main mistake is confusing an externally chosen yes/no *forecast outcome* (e.g. meeting an arbitrary hours or money threshold) with someone's enduring psychological tendency.

Adopt the independent evidence layers:

| Layer | What the interviewer asks | What may legitimately be inferred |
| --- | --- | --- |
| Habitual tendency | What usually happens across actual opportunities in a defined phase (e.g. last 2–3 years)? | First-person recurrence and conditionality, not objective trait truth |
| Actual activity/event | What did you really study, create, lead, teach, leave or change? Approximately when? | The stated event or duration, not automatic personality |
| Ability/preference/opportunity | Could you do it, would you choose it, and were there chances? | Three distinct reported dimensions |
| External observer comment | What did another person actually say and in what situation? | A sourced reported observation, not validated assessment |
| Independently frozen future outcome | What happened after the entire prospectively specified window elapsed? | An outcome evaluated separately after the fact, never a current survey answer |

## Rules for the original GPT interviewer and future Railway candidate

1. Begin with the current interview's ordinary-life question, one at a time. Before asking additional material, inspect the person's **already existing original answers** for the *same* construct, time frame and dimension. Do not ask merely to fill a questionnaire quota or turn a broader answer into five repeated "independent" responses.
2. If relevant but unresolved, offer a short participant-chosen topical menu from the existing 23 optional candidates, not an automatic 23-question sequence; at most five chosen topics total. The external survey suggests **seven possible microprobes** after a related answer, and at most two per session if they genuinely clarify an important distinction.
3. For a recurring tendency, ask the **usual pattern** plus *opportunities/exposure* and exceptions. Ordinary frequency words are acceptable; percentages are entirely optional. A story about one latest episode is a factual example, not a sufficient general personality measurement.
4. Use identifiable **recall periods** for reported life history and approximate dates only if actually useful; never reveal DOB-derived ages or chart-selected forecast windows to a blinded participant. Do not force exact ages, income, days, hours or event counts.
5. **Work** includes contract, self-employed, informal, volunteer, community service, teaching, independent research, and paid work. Ask compensation separately from type/duration/activity. Distinguish income *received* from meaningful work or competence.
6. Allow respondent-generated categories and complete preferences: "depends on the people and purpose", other, two tied priorities, none, no opportunities, unclear, not applicable and decline are **valid and sufficient**. Never override them with an A/B answer.
7. Separate making things creatively, technical craft, artistic appreciation, how much they spend on aesthetics, and what is rewarding to them. Money spent is influenced by financial and housing opportunity; it is **not** a beauty preference meter.
8. Separate **what another person commented** from the person's own recurring report; do not collapse high standards, detail, critique and perfectionism into a single composite.
9. Preserve "missing/unclear" as its own observed state and leave future forecast items **FUTURE_PENDING**. Never convert either to "no". Preserve the full exact original choice and clarification note in the source archive.
10. For chart experiments, freeze each intended chart predicate, expected response/outcome, question wording and non-astrology baseline **before** independent participant collection. The author's printed freeze label is not verifiable without the frozen file and timestamp provenance. No stored owner response provides untouched validation of the development model.

## Seven new conditional probes

The seven entries in `CONDITIONAL-MICROPROBES-v1.json` cover evidence/reasoning when disagreeing, third-party feedback, freely chosen reflective solitude, voluntary group departure, held leadership versus leadership preference, open-ended partner priorities (ties allowed), and project persistence relative to actual started-project opportunities. They are **conditional** and are not seven new mandatory questions.

The question origins and distinct existing survey areas are traceable through `EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json`. The executable additive instrument is `LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json`, constructed deterministically from the 23 previously accepted research candidates **without changing their question wording**. The original 25 TF1 and eight EM questions remain pinned and untouched.

## Explicitly rejected source designs

- Mandatory hard cutoffs about paid work, training hours, counts of readers, social groups, or household decoration spending for stable personality traits.
- Forced one-to-one/group A/B answers and restricted five-item partner priority rankings.
- Treating absence of a salary/job title as the absence of actual teaching, coordinating, writing or earning activity.
- Treating one long argument, group departure, abandoned project, or move as repeated psychological disposition.
- Counting overlapping relocation or study events as multiple independent corroborations.
- Repeating a known choice to engineer support for a chart-based prediction.
- Treating a five-item future forecast without elapsed windows or the underlying frozen key as a completed personality test or proof of astrological success.

**Release boundary:** This guide and its JSON are a *candidate research instrument*, not production deployment. The existing live GPT and Railway Action v1.9 require a separate versioned update and a pilot check before enabling new questions; the present user asked to integrate the best design features, not to rewrite or score historical records retroactively.
