# Fresh respondent pilot launch — scenario survey v7

Status: **READY_FOR_FRESH_PILOT**

Reviewed survey commit: `1d79a4d6f620f59699ff9a0c21e6441d7cd8017f`

Before running the pilot, verify the question bank, protocol, evidence guide, and source-requirements hashes against `BLIND-REREVIEW-FIREWALL-1D79A4D-READY.json`. A later state-only commit is acceptable only if those survey bytes are unchanged.

## Freshness requirement

Use a respondent who did **not** complete the owner live pilot and has not been shown the v7 bank, repair history, target-model mappings, chart-derived predictions, fit scores, or expected answers.

Run the interview in a fresh interviewer context that has access to the bank/protocol/evidence contract but not to target-theory outputs or prior participant answers.

## Privacy

Raw participant answers, exact transcript text, private identifiers, and content-derived hashes stay outside public Git.

Create a new private per-pilot archive outside every Git ancestor. Save:
- exact rendered question;
- exact participant answer;
- route/version binding;
- answer kind and narrow interpretation;
- process/design feedback as a separate event;
- corrections append-only rather than overwriting prior answers.

Public Git may receive only non-private design findings, counts, and review/state artifacts.

## Interview procedure

1. Apply `INTERVIEW-PROTOCOL-v6.md` before every question.
2. Treat `interviewer-bank-v7.json` as a menu, not a quota.
3. Ask one response task at a time.
4. Preserve “it depends” conditions rather than forcing a global trait.
5. If only one piece is missing, acknowledge what was supplied and ask only that piece.
6. Suppress tautological, redundant, mirror, antecedent-missing, premise-insufficient, or low-information routes.
7. Do not use the exploratory sensory-conflict item during canonical interviewing. If used later, label it explicitly exploratory and give it no canonical evidence credit.
8. Stop naturally when no remaining route is both admissible and expected to add a useful nonredundant distinction.

## During-pilot design defect capture

Treat these as design feedback, not respondent-trait evidence:
- “this is obvious” / mirror or tautology;
- missing premise or hidden determinant;
- uncertainty caused by scene ambiguity;
- question already answered;
- question asks the wrong target (action versus mood, motive versus behavior, etc.);
- respondent must invent workload, motive, relationship, cost, recovery, or another determinant;
- canonical route feels forced despite global admission guards.

Do not repair the live question repeatedly after one clarification. Preserve unknown/inapplicable and move on when needed.

## Pilot completion

After natural stop:
- freeze the private transcript;
- record participant-answer count and route coverage privately;
- publish only a non-private design checkpoint;
- review whether any new defect class requires redesign;
- do not score the participant against chart/birth data during the usability/semantic pilot.

A clean fresh pilot is evidence that the redesigned interview is usable enough for the next validation stage. It is not psychometric validation or evidence that AstroHD is true.
