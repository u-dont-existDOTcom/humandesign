# Gene Keys G39 — Delivered offline blinded stimulus-rating packets; NOT human manipulation validation

**25 October 2026. Original owner outcome OPEN:** The purpose remains to test specific source-defined natal-chart interpretations across Human Design/Gene Keys and other traditions against genuinely untouched consenting humans, with frozen chart predictions, source/analyst distinctions, chart decoys and credible nonastrological controls. G39 advances only the **quality assessment of G38’s researcher-written communication-style messages**. It does not collect an independent human rating, interpret anyone’s life, produce a successful Gene Keys prediction, or modify the live participant-session worker.

## What G38 already established and why this check was needed

G38 used the official Gene Keys [six “responds best to” Line descriptors](https://genekeys.com/how-to-read-your-profile/) as inspiration for a proposed communication-preference test. The publisher separately [qualifies that the wording of a Line changes with the Sphere/Sequence](https://genekeys.com/docs/why-do-i-have-different-line-keynotes-in-my-venus-or-pearl-sequence/). G38 deliberately selected **Life’s Work/natal Sun Line** as an *analyst choice*, generated four fictional scenarios × six message styles each with the exact same three event facts, and ran a synthetic chart Line → mock choice calculation. Its 120 fictional persons and 480 artificial choices, including mock permutation p=0.7115, are **software tests only**.

Even if the G38 scoring logic is sound, these four source-to-style assumptions remain unverified: people must perceive the messages as embodying the intended distinct communication styles; the messages must sound plausible; their facts must remain equally accessible; and wording/cognitive-effort differences must not trivially make one option preferable for everyone. In particular Line 2’s metaphorical “high frequency” and Line 4’s “romance” were only *partially approximated* by safe nonromantic messages. Passing code tests would not resolve those questions.

## What G39 actually built and executed

### Six finished, offline reviewer HTML files

The [G39 source-locked generator](genekeys_g39_blind_rating_packets.py) accepts only the **unchanged, byte-hashed** G38 final source bank/contract and G37 original Line descriptions, with exact input SHA256:

| Parent source | Required SHA-256 |
|---|---|
| G38 final 24-message bank | `fd3c880aa2cb84cd1f9c50eff0905f744d3b4d9bc22bf63f8ff825520976ecad` |
| G37 six official short Line descriptors | `2e53d6013037aeb40884df1da96390a27b7fbeb15828bb0a84342ddabd660b82` |
| G38 source-vs-analyst study contract | `3ff656246104e58700b2fd49f122fcb97077ccfc50bd1549b0d2e537c0358559` |

It generates **six** distinct pseudonymous, offline HTML files (R01–R06). Every file contains the same **24** fictional messages, with **four different scenarios** × **six source-inspired style versions**, in deterministic but different display order. Messages use non-revealing SHA-derived item IDs. Six published short Gene Keys Line descriptions appear as potential *classification labels* but no rater-visible message includes its intended source Line/label, a real chart, participant date or private answer. Categories and message orders vary by packet. The author-intended target labels reside **only in the separate researcher-key packet** [`GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json`](GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json), whose canonical body digest is `a8321ed8a7919fa5dd93fdfa7f45d4f91a2c7d7fb731c7c4a3f646d9243728a9`.

For each anonymous fictional prompt the local browser reviewer can choose among **six original source-style descriptors** or **“none / unclear”**; rate classification confidence 1–5; check the scenario’s three factual sentences (yes/no/unsure); and rate **naturalness** and **perceived interpersonal pressure** separately 1–5. Full reviewer instructions are [`GENEKEYS_G39_PUBLIC_RATER_INSTRUCTIONS.txt`](GENEKEYS_G39_PUBLIC_RATER_INSTRUCTIONS.txt). Ratings stay **only in in-memory browser state** until the reviewer deliberately clicks to export a JSON file. No background network calls, third-party scripts, analytics, cookies, localStorage or automatic upload are present. Closing the page discards responses. No personal birth, health, spirituality, relationship or demographic details are requested.

### Actual local Brave browser execution, then the separately coded scorer

The optional [real browser smoke test](genekeys_g39_browser_smoke.cjs) launched **Brave Chromium 156.0.8078.48**, opened two separate packet variants (R01 and R04), intentionally clicked the first “next” button with nothing selected (HTML required-field validation **correctly blocked** it), then submitted **24 fully artificial ratings** and clicked the actual **Export JSON** control. Both downloads were parseable JSON with **24 unique item codes each** and preserved naturalness, pressure, confidence and factual flags. The research [offline grader](genekeys_g39_rate_blind_packets.py), run as a separate command, read both exported JSON files, verified the frozen packet mapping and graded **48 artificial browser clicks** end to end.

That is real evidence the **file-based questionnaire software functions in the owner’s actual browser**, not evidence that an independent person reviewed the text. No actual human reviewer was contacted, recruited or administered a form. The [saved Brave browser smoke receipt](GENEKEYS_G39_ACTUAL_BRAVE_OFFLINE_BROWSER_SMOKE_V1.json) records the browser version, SHA256s of the original HTML and exported fake data, and the fact that **independent rater count remains zero**.

The first prepublication UI script mistakenly added literal backslash-plus-n to the researcher-key file; the separate Python scorer caught invalid JSON. This was corrected, and the actual Brave end-to-end export/scoring path was re-run. A subsequent refinement added naturalness and perceived-pressure ratings; the earlier **entirely synthetic and uncommitted** files are preserved only under `/tmp/g39-superseded-prepublication/`, never in the accepted repository checkpoint. No hidden human answers or trial version were modified.

### Synthetic grader controls, NOT independent ratings

[Three fixture controls](GENEKEYS_G39_SYNTHETIC_RATER_GRADER_RECEIPT_V1.json) were generated deliberately *from the secret researcher answer key* and evaluated by the same code:

| Fictitious six-reviewer responses (6×24) | Correct source labels |
|---|---:|
| Every fake rater chooses the keyed intended category | **144/144** |
| Every fake rater always chooses source-category 1 | **24/144** (16.7%) |
| Every fake rater chooses “none / unclear” | **0/144**, 144 abstentions |

The test score reports per-source-style confusion matrices, proportion classifiable (with unclear retained), confidence, perceived realism and pressure, factual inaccuracies, and pairwise inter-rater agreement. These are *descriptive language-manipulation measures*, **not** a hypothesis test for natal-chart accuracy or contemplative efficacy. With six equally represented authored categories, an indifferent single-category labeler scores **1/6** by construction. A perfect fixture scores 100% because it reads the answer key, not because the messages are independently recognizable.

## Negative finding in the completed mechanical wording audit

The independent [G39 lexical/length preflight](GENEKEYS_G39_STIMULUS_WORDING_CONFOUND_PREFLIGHT_V1.json) checks the G38 source bank without human perception:

- All **24/24** messages repeat their scenario’s same **three exact factual sentences once each**; factual-text equality is mechanically confirmed.
- **Eight of the 24 messages directly echo a defining word or phrase from their official source-category label:** four Line-3 “no pressure” prompts and four Line-5 “practical” prompts. This can inflate apparent correct labeling through lexical recognition.
- For each of four fictional scenarios, Line 1’s detailed/direct message averages **56.75 words**, Line 5’s practical/actionable message **29.75 words**, and other styles approximately 37.75–40.75. This length difference is partly deliberate, but creates a general readability/effort **confound** that cannot be called independent support for Gene Keys even if respondents prefer one variant.
- Line 2's source phrase “High Frequency with No Agenda,” Line 4’s “Integrity, Honesty, Softness & Romance,” and overlaps between Line 3 and Line 6 remain source-fidelity or discrimination risks. Mechanical exact-word tests cannot decide whether those constructs are faithfully conveyed.

G39 did **not** change the accepted G38 stimulus bank to conceal these flaws. Any proposed revised wording needs a dated next development version; once actual raters see stimuli, modifications must not turn *those same raters* into untouched confirmatory data.

## Real human-science boundary and honest next step

The six reviewer forms are an **opt-in language-manipulation check** only. The researcher-guide file [`GENEKEYS_G39_RESEARCHER_GUIDE.md`](GENEKEYS_G39_RESEARCHER_GUIDE.md) explains how to run the offline grader later on files that independent volunteers may choose to provide, without putting those responses into Git or the root `participant-session-v1` task. The researcher key and generators are in the project repository: a motivated future rater who searches the source repository can theoretically find target labels. Therefore these forms are **content-blind and locally private**, but they are **not adversarially double-blind nor externally notarized**. For a substantive later human trial, independently custody the scoring key and preserve a trusted pre-answer freeze.

The immediate missing observation is from actual **independent voluntary reviewers who did not write the messages**, judging whether source categories, naturalness, pressure and factual correctness are adequate. Do not fabricate a pass threshold, assume success from synthetic fixtures, or label the simulation of browser clicks as human review. Once the quality issues and source interpretation are independently addressed, genuine natal predictive validation would still require real participant consent, independent birth-time precision, frozen chart and behavioral model, matched full HD interpretation baseline, nonastrology population style controls, and response custody.

**STATUS: G39 offline reviewer/checker tools built and browser-tested; 0 real reviewers; 0 real natal predictive validations; no production or root participant-session task changes. Parent user goal remains OPEN.**


## Final owner delivery, scope and verified acceptance

The public instructions have been refined to be **unbranded**: reviewers see a neutral communication-style task, not the name of the astrological source. The reviewer ZIP deliberately contains only six offline HTML forms and a generic README; **no original source-to-Line labels, researcher answer key, generator, scoring scripts or natal hypotheses are enclosed**. The complementary researcher ZIP includes the six forms *plus* the private-intent classification key, original public source/version hashes, Python/JavaScript code, offline grader, artificial controls, this report and the continuation handoff. Do NOT distribute the researcher ZIP to independent reviewers.

The executable archive creator (genekeys_g39_deliver_separated_packages.py) runs on the authorized owner laptop, writes both archives **directly into the local French Downloads folder**, fixes ZIP metadata for reproducible hashes, refuses silent overwrites, verifies every compressed member by readback, excludes actual rater responses and writes an independent packaging receipt. The two filenames are:

- Anonymous-Message-Style-Review-Packets-G39-20261025.zip — **reviewer-safe, seven contents**, ready to offer voluntarily without sharing the study answer key.
- Gene-Keys-G39-Researcher-Scoring-Evidence-20261025.zip — **researcher-only, 25 contents** including scoring key and code; not reviewer-safe.

Exact final archive byte sizes/hashes and member lists are in GENEKEYS_G39_DELIVERY_MANIFEST_V1.json, produced after the final report was written. Neither ZIP contains real persons' ratings or birth information.

**Verified complete research-only test suite (executed, exit zero):**

- Focused Gene Keys G39 structural, source provenance, browser-export, lexical-bias, scoring/fixture and ZIP-separation tests: **25/25 PASS**.
- All cumulative Gene Keys G35–G39 source/engineering tests: **113/113 PASS** (88 inherited + 25 G39).
- Independent previously accepted Hellenistic C34 source/engineering tests: **367/367 PASS**, with pinned optional ERFA/IERS researcher inputs.
- **480 separate code/source test cases**, not 480 independent people, rated messages or astrology predictions. Actual independent style reviewers: **0**. Actual birth-based human predictive validations: **0**. Production scorer and exclusive participant-session task unchanged.

The only substantive next observation specific to G39 is optional participation by **independent consenting people unfamiliar with the scripts**, using the neutral reviewer ZIP and voluntarily returning their exported anonymous JSON. Software can score their classification/naturalness/pressure ratings without seeing natal charts. The current report intentionally sets **no after-the-fact pass threshold**. If the source classes aren't reasonably distinguishable or the wording sounds unnatural, preserve that negative result and move to a new development version—not a reinterpretation of the same reviewers as a confirmatory cohort. Gene Keys birth-based behavior prediction remains a separate downstream test with its own source, chart, privacy and consent requirements.
