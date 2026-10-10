# Idiosyncratic behaviors and answer scaffolds — Life Patterns design decision

**Status:** Prospective **development-only** changes. The real 25-question TF1 v1, historical v7, deployed GPT, and all existing respondent records are unchanged. The v3 answer choices are optional examples, not validated trait labels. No new birth-chart mapping is admitted.

## 1. Self-generated unusual-behavior inventory

**Why try this:** Open-ended self-generated examples can reveal meaningful within-person distinctions the existing question bank did not anticipate. Idiographic assessment and experience-sampling research study such individually relevant variables and behavioral context. This is a reasonable *discovery* instrument, but it is not established that uncommon self-reports contain more information about natal charts or that an inability to list them implies one's birth date is harder to identify.

**Proposed participant question**

> What are some specific things you do, like, notice, or handle differently from many people around you? Small everyday habits count. They need not be impressive or positive. If none come to mind, that is fine. Start with one to three, and continue only if you want.

After each useful example, capture exact observed behavior (not a trait adjective), typical frequency, context, social comparison group, what motivates it, meaningful contrary cases and how sure the person is that it is unusual. Limit follow-ups to one or two high-information questions per item. Offer prompts such as a routine, recurring shortcut, learning/organizing habit, social preference or reaction only when helpful. No quota: invite continuation toward 10–20 **if willing**, and permit zero, stopping or skipping.

**Interpretation constraint:** one person might describe repurposing a household tool. That action could reflect time-saving, convenience, resource scarcity, curiosity, learned habit, trial-and-error, or comfort with risks—not necessarily creativity, independence, intelligence, or nonconformity. A follow-up would seek why the choice was made, similar decisions, times the person followed official instructions, and whether any claimed efficiency was measured. Do not provide unsafe procedural instructions or assume a risky workaround is beneficial. The owner's original anecdote is not included in the public repository.

**Data quality measures:** self-described item count (spontaneous vs prompted separately), specificity, distinctiveness relative to a named reference group, stability on retest, novel domains not covered by the regular questionnaire, burden, and respondent comfort. Objective rarity requires comparison data. Self-estimated rarity is a *belief* and may be inaccurate. Unequal recall ability, modesty, culture, economic constraints, language fluency and opportunity must not be misinterpreted as innate chart uniqueness.

**Scientific hypothesis only:** after a separately preregistered chart-behavior mapping and blinded coder protocol, test whether this module adds out-of-sample birth-chart identification above the existing survey and matched non-astrological controls. Use identical candidate charts, decoy universe and held-out participants for with-module vs without-module scoring. Separately test whether inventory count predicts identification uncertainty; no assumed monotonic link. A rare behavior can uniquely identify a person socially without identifying their birth minute.

## 2. Scaffolds and multiple-choice examples

**Owner problem:** simply asking broad prompts often leaves people unable to generate a response, and an allegedly optional example is not offered when they most need it.

**Draft default:** show the direct question and 2–4 short, balanced, plausible answer *examples* immediately. Participants may tick one or several, mix them with their own language, say **Other — in my own words**, **Not sure / can't recall**, or **Prefer to skip**. A narrative response needs no option selection. Examples must cover materially different possibilities, including conditional responses, not merely “good” traits. Do not treat checkbox selection as objectively verified performance, a birth-chart feature, or independent corroboration. Avoid demanding examples after an already adequate answer.

**Voice adaptation:** read at most two or three short examples initially plus “or something else”; present all choices in the text interface. Do not enumerate a long list in audio and ask the person to remember it.

**Why not assume this is better:** example choices can improve comprehension and recall but also anchor participants, hide unanticipated answers, and contaminate reverse-match hypotheses. Pilot the same neutral question with open-only and example-supported presentations, randomized independently of birth data, and compare unanswered rate, source specificity, time to respond, correction count, examples copied verbatim, and participant understanding. Confirm any actual coding change against independently verified open responses.

## 3. TF1-A0: actual solitude enjoyment vs social invitations

**Original current v1:** “When your time is your own, do you usually protect uninterrupted time, look for company, or vary depending on who and what is involved?” The proposed v2 catalog copied this wording unchanged, although its heading misleadingly made it look like a new experimental question.

**Proposed v3 primary:** **“How much do you enjoy spending time alone?”** Examples: “I enjoy solitude and intentionally arrange time for it”; “I enjoy solitude when it happens, but rarely seek it out”; “I prefer company most of the time”; “It varies.” Other/unknown/skip always available.

**Two distinct, conditional follow-ups (only when useful and not already answered):**

- “Do you actively arrange time alone, or mostly enjoy it when it happens?” — deliberate time-making is **not** enjoyment.
- “When you are enjoying time alone and a friend invites you out, what normally decides whether you join them or stay?” — social acceptance/boundary is **not** enjoyment or proactively seeking solitude.

The original A0 question must not be treated as automatically equivalent to a direct solitude-enjoyment answer. Independent reviewer still decides what exact words support.

## 4. TF1-STATUS: split recognition from laptop ownership

**Cause:** the frozen historical v7 evidence facet `D19.status_ownership` jointly referenced two separate older question routes, `STATUS` (intrinsic reward of admiration) and `OWNERSHIP` (desire to own an access-equivalent laptop). The old question atlas naively displayed that combined facet under modern `TF1-STATUS`. It made an answer about recognition appear to support ownership motives.

**Display fix:** Current `TF1-STATUS` and proposed v2 `TF1-STATUS` no longer inherit the combined laptop facet. The atlas instead warns that the historical source mixed the two questions; it retains the actual historical entry for transparent provenance. The status question continues to measure only how intrinsically rewarding recognition feels and how that varies by relationship; no claim about ownership, power, status seeking, or invitation is permitted from it alone. `scoped_recognition_ownership_and_solitude-v0.json` records two distinct prospective researcher coding constructs without rewriting historical v7 or claiming scoring validity.

**Important:** Laptop ownership remains a separate historical answer that may be useful for research. It should not be deleted; it simply does not answer the recognition question.

## 5. What changes now and what remains pending

- Complete **25-route v3 candidate** with topic-specific answer-example paths, Other/unsure/skip and no forced-choice requirement. Only A0's question wording is changed relative to the existing v2 proposal; other earlier v2 wording revisions are inherited unmodified.
- Optional respondent-generated inventory module with open list and safe conditional follow-up rules.
- New prospective researcher facet-scoping and corrected, reproducible researcher atlas for STATUS and A0.
- Offline local pilot page where the owner can try response formats and inventory without sending any data. A local export is available only on user action.

**Not done:** no automatic interview deployment, no new finalized Human Design or AstroHD mapping, no correlation testing, no claim that distinctiveness aids DOB inference. Use new, previously untouched people and versioned source-to-target codebooks for any real validation.

## Prior work and methods

- COSMIN 2025 content-validity guidance: relevance, comprehensiveness and comprehensibility <https://pubmed.ncbi.nlm.nih.gov/40562250/>.
- COSMIN consensus methodology addresses **appropriateness of response options**, recall period and cognitive interviews <https://pmc.ncbi.nlm.nih.gov/articles/PMC5891557/>.
- Conner et al., 2009, *Experience Sampling Methods: A Modern Idiographic Approach to Personality Research* <https://pmc.ncbi.nlm.nih.gov/articles/PMC2773515/>.
- Haynes et al. (idiographic assessment conceptual/psychometric foundations) <https://pubmed.ncbi.nlm.nih.gov/19217703/>.

These sources support considering individually tailored behavioral elicitation and checking question comprehensibility. None establishes a causal or predictive relationship between behavioral distinctiveness and birth data.
