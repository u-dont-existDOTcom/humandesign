# Constructed conversation cases — second pass

These are author-reviewed expectations, not independent respondents or NLP test results. Exact source text outranks labels. The typed-state unit tests exercise control paths only after a human/Chat has supplied the semantic state.

| Case | Response or situation | Appropriate next behavior | Not supported |
|---|---|---|---|
| 01 | “Yes, I'd go.” | Ask “What would make you say yes?” when motive is useful and missing. | Guilt, enjoyment, duty, or general self-sacrifice. |
| 02 | “Yes, because I enjoy seeing them.” | Keep action and enjoyment; no repeated why probe. | Hidden guilt or responsibility. |
| 03 | “I'd go, but I'd feel guilty if I didn't.” | If needed, ask “What would you feel guilty about?” | A unique cause of guilt. |
| 04 | “I'd feel bad for them.” | Clarify the person's intended feeling or reason only if still ambiguous. | Self-blame, empathy subtype, or obligation by default. |
| 05 | “I'd like to see them, but I also feel I should.” | Preserve both motives; do not force one winner. | One exclusively causal motive. |
| 06 | “I'd say later.” | An open reason probe can clarify the delay. | Autonomy as a general trait. |
| 07 | “Which friend? That changes my answer.” | Repair the relationship premise or retain the stated conditionality. | Indecision or failure to answer. |
| 08 | “I don't know.” | Keep unknown; offer a fitting scene or change topic rather than manufacture motive. | A negative trait or sufficient evidence. |
| 09 | “If I answered yes, would you ask why?” | Store design feedback; keep the pilot paused. | An actual yes response. |
| 10 | “Actually, I would go because I want company, not because of guilt.” | Append correction; supersede the unsupported guilt interpretation. | Continued use of the withdrawn motive. |
| 11 | “Nothing bodily comes to mind.” | Distinguish no reaction from unsure; do not ask how reliable that nonexistent signal is. | A concealed bodily authority. |
| 12 | “There is a tense feeling, but I don't know whether it tells me anything.” | Capture reaction plus uncertain usefulness; no trust score. | Reliable guidance. |
| 13 | “I decide tomorrow after checking the details.” | Ask about clarity over time only if relevant and not already explained. | Delayed clarity caused by time alone. |
| 14 | “I return to the task after interruptions.” | Keep resumption; depth and duration remain unknown. | Sustained stationary focus. |
| 15 | “I stop when I make mistakes.” | Keep stopping cue; ask restoration only if depletion/recovery is relevant and missing. | Successful recovery. |
| 16 | “My response has not changed.” | Do not ask what learning made it different. | Developmental improvement. |
| 17 | “My trust would stay the same.” | Do not force a repair/reliance-again question. | Broken trust. |
| 18 | “I don't want to discuss relationships.” | Stop this topic; do not relabel privacy as absence of intimacy. | Romantic or sexual orientation. |
| 19 | “I would not join that project.” | A later investment scenario is allowed only as an explicit, welcome hypothetical variant. | A month of actual prior investment. |
| 20 | “I'd choose better light.” | Keep preferred condition; ask functional effect only if useful. | Demonstrated improved concentration. |
| 21 | “More money would buy tools.” | Keep practical purpose; status and ownership motives remain unknown. | Lack of interest in recognition. |
| 22 | “I'd move the meal earlier so they could come.” | Keep accommodation; do not infer persuasion ability from a proposal. | Measured effectiveness. |
| 23 | “I have no current partner, but I can answer from a past relationship.” | Record the past frame and retain it in follow-ups. | A current partner or unchanged present preference. |
| 24 | A quoted answer is exact but its label claims more than it says. | Reject the excess interpretation even though the source pointer is valid. | Semantic correctness from hash or quote matching. |
