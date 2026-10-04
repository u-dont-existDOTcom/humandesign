# Fresh source-anchored multi-route blind packet v7 — 2026-10-04

Frozen before any v7 shadow replay. The synthetic cases were generated in a separate blind context instructed not to inspect implementation, prior validation cases, or expected outputs.

Governing rule:
- Ask only when the existing source itself exposes a materially unresolved behavioral distinction, contradiction, conditional boundary, or merely preliminary step whose downstream route-specific response remains unresolved.
- Missing route coverage alone is never a reason to ask; an unmentioned route can remain unknown.
- Semantically equivalent source can answer a route without a canonical route ID.
- Later corrections supersede corrected wording.
- If a source says “it depends on X” but does not say how X changes the response, a narrow missing-piece follow-up may be useful.
- If source says it cannot answer a distinction, repeating the same broad question is not useful.
- Multiple independent useful gaps may coexist and should all be selected up to three.
- A dependent follow-up must not be eligible before its antecedent is actually answered.
- For a broad canonical route asking what matters/means/catches attention, one concrete in-scope answer can be sufficient unless source itself exposes a material unresolved interpretation.

Route meanings:
- M05: familiar-route deviation; what meaning does the respondent make of it? Do not assume danger or intuition.
- M09: familiar/simple/offline planning app versus more complex app with shared reminders/better search and about one hour migration; what matters in deciding whether to switch?
- M11: two-person friend-meal exchange; respondent offers several hours cooking/organising and friend says paying for all ingredients is too much; what would respondent say next?
- PREFER-EXCHANGE: only after a bound M11 antecedent; how much does the respondent want to keep negotiating toward a mutually acceptable arrangement in that exact exchange?
- G19: promised help for a friend's move runs long into personal time; what matters in deciding what to do?
- G20: basic needs covered and unexpected extra money equal to one month ordinary living costs; what does respondent most want the money to do?
- G23: casual shared meal with familiar people and no assigned job; what tends to catch attention first?

Cases N1–N9 are frozen in `MULTI-ROUTE-CASES-v7.json`.
