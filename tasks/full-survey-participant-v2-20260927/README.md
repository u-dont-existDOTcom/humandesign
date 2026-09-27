# Full Life Patterns participant V2 package

Date: 2026-09-27. Status: iteration candidate ready for participant use.

## What to distribute

Primary participant file: `Full-Life-Patterns-Survey-v2-2026-09-27.md`.

It is self-contained: the V2 controller plus the exact existing interview protocol, 79-route bank and 73-facet evidence guide are embedded. Participants do not need GitHub access. The same file handles a new interview, an existing old survey chat, or recovery from an attached response record.

Companion participant instructions: `START-HERE-FOR-PARTICIPANTS.txt`. For people already in an older survey chat, `UPGRADE-OLD-CHAT-MESSAGE.txt` provides the exact update message.

## What changed because of the first external participant run

- prevent broad thematic/ad-hoc question drift from silently receiving canonical evidence credit;
- preserve route identity and determining scene conditions at the actual rendered-question boundary;
- preserve earlier/current, relationship-context, first-reaction/later-response and baseline/confound distinctions;
- recover edited response records without pretending they are verbatim original transcripts;
- do not restart merely because original route IDs/JSON are missing;
- move neutral record review to the end of resumed questioning to reduce avoidable consistency priming;
- make ChatGPT create the JSON handoff and, when supported, a downloadable `life-patterns-participant-export.json` file;
- explicitly reject ChatGPT account-data export as the research handoff.

These are measurement/provenance/UX repairs. The canonical bank/evidence guide and astronomical model are unchanged. Asking more questions does not solve missing behavioral-to-chart interpretations; those remain separate model-development work.

## Privacy

No participant answers, names, birth data, or content-derived private hashes are stored in this public package. Participant-specific recovery packets are generated outside the repository from private input and delivered privately.

## Verification

Focused package tests verify the three authority blob identities, exact embedding, 79 bank routes, 73 evidence-guide facets, recovery preservation and V2 export/recovery instructions. These tests do not establish interviewer compliance in every model/chat or scientific validity.


## Claude independent review

Claude Opus 5.5 at max effort reviewed the public V2 package, builder, tests, original authority and branch diff. No private participant answers, birth data, chart data, targets or ranks were supplied. The first verdict was PASS_WITH_FIXES; the identified recovery/provenance/schema/route/export problems were repaired. One reconciliation pass returned PASS_WITH_MINOR_FIXES with no blocker. Every remaining participant-facing fix from that pass was then applied: exact imported-record preservation, correct route-card context semantics, split file/no-file closing messages, stop-reason/JSON consistency, and duplicate/null/path safety.

Final focused verification after those fixes: 15/15 V2 tests, 8/8 prior recovery tests, and 497/497 original survey checks. The package remains an Iteration candidate: these checks prove packaging/provenance invariants, not scientific validity or guaranteed compliance by every ChatGPT runtime. Live context/file behavior for the approximately 197 KB self-contained packet is the remaining empirical participant-use observation, not a pre-send blocker.
