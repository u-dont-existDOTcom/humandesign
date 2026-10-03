# Blind triage adjudication cases v1

Evaluate each synthetic case under this rule: ask only if the named route's behavioral distinction remains materially unresolved, context supports the question, and the source has not already answered it. Missing coverage alone is not enough. Unknown may remain unknown.

## Route authority

**G19** asks what matters when deciding what to do after a promised move-help commitment runs long and consumes personal time; retain only decision factors in that competing-commitment scene.

**G20** asks what the respondent would most want an unexpected amount equal to one month of ordinary living costs to do for them, with basic needs covered and no repayment obligation; retain only the intended function of that amount.

**M05** asks what the respondent would make of a familiar bus/car route suddenly taking a road that route normally never uses; retain the meaning they give the deviation without assuming danger or intuition.

**M09** asks what would matter in deciding whether to move from a simple familiar offline planning app to a more complex app with shared reminders and better search; retain only properties actually weighed.

**G23** asks what first catches attention on arrival at a casual shared meal where people are getting things ready and nobody assigned a job; retain only what catches attention in that setting.

## Cases

- **H1 / G19:** “When plans run longer than expected, I usually look at what is most urgent before I decide what to do next.”
- **H2 / G19:** “If I'd promised to help with a move and it was eating into time I had reserved for myself, I'd check how much my friend still truly needed me, how much personal time I'd lose, and renegotiate a shorter commitment if they could manage.”
- **H3 / M05:** “If a route I know suddenly used a road it never uses, I'd first assume there may be a detour or traffic issue and check the map. I wouldn't automatically take it as danger.”
- **H4 / M05:** “I tend to notice unusual things quickly, especially when something changes.”
- **H5 / M09:** “I value simple familiar tools. I'd switch if I regularly needed to coordinate shared reminders with other people, but better search alone wouldn't be worth the extra complexity and migration.”
- **H6 / G20:** “Extra money like that would be nice; I'd be glad to have it.”
- **H7 / G23:** “At a shared meal I first notice practical things that are unfinished — whether something needs carrying or serving, or whether someone is waiting for a place to sit.”

## Required adjudication output

For H1–H7 return:
- `decision`: `review_ready` or `clarification_needed`
- `route_id` only when clarification is needed
- one concise reason
- confidence: high / medium / low

Do not inspect or infer any implementation result.
