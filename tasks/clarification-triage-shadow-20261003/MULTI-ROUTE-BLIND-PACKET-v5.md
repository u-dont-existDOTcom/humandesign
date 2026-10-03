# Fresh multi-route blind adjudication v5 — 2026-10-03

This packet is frozen before any v5 shadow replay. Judge only the source and route contract below; do not inspect implementation output.

Rule: A clarification is eligible only when it is context-supported, not already answered, and its answer could materially change an unresolved behavioral distinction, condition, contradiction, or interpretation. Missing coverage alone is not enough. Unknown may remain unknown. A narrow missing-piece follow-up is allowed when source itself exposes a material unresolved condition or decision boundary. Independent useful questions may be returned together, maximum three.

Route meanings:
- **M05**: on a familiar route, driver takes a road the route normally never uses; ask what the respondent makes of that cue. Do not assume danger or intuition.
- **M09**: familiar/simple/offline planning app versus more complex new app with shared reminders/better search and ~1 hour migration; ask what matters in deciding whether to switch.
- **M11**: friend-meal exchange where respondent offers several hours cooking/organising and friend says paying for all ingredients is too much; ask what respondent says next.
- **PREFER-EXCHANGE**: only after a bound M11 antecedent; ask how much respondent usually wants to keep negotiating toward a mutually acceptable arrangement in that exact exchange.
- **G19**: promised help for a friend's move runs long into personal time; ask what matters in deciding what to do.
- **G20**: basic needs covered, unexpected extra money equal to one month ordinary living costs, no repayment; ask what respondent most wants it to do.
- **G23**: casual shared meal with familiar people, no assigned job; ask what catches attention first.

Cases K1–K7 are in the accompanying frozen JSON. For each case return:
- decision: review_ready or clarification_needed
- ordered route_ids (empty if ready)
- route_type for each asked route: canonical or missing_piece_followup
- one concise reason
- confidence high/medium/low

Do not discuss implementations, benchmarks, or prior evaluations.