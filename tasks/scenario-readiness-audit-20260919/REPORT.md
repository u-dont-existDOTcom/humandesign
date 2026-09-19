# Scenario-first survey — readiness audit

19 September 2026 · final text-only design: **scenario-bank-v5.1-20260919**

## Judgment

**I judge this revised design ready for a saved, one-question-at-a-time owner pilot.** I have no remaining identified material wording, context-binding or interview-flow defect that I would ask the owner to debug before trying it.

This is my substantive design judgment after reviewing the actual questions and proposed continuations. It is not an independent evaluation, a promise that every possible answer has been anticipated, or a certification of the deployed app. The owner pilot remains paused. No app change, inference call, VM wake, recruitment or chart scoring occurred.

## What changed in the review method

Earlier passes mainly repaired individual questions and their coverage labels. This pass reviewed the complete interaction contract: the exact scene, what one answer establishes, which next question is justified, what should be skipped, what happens after a topic change or correction, and what stopping preserves. The criterion was a useful and faithful conversation, not a longer list of questions or another high coverage count.

The frozen input was the 75-entry v4 bank at repository commit `81b20fee050d1400d39c9f099093e9829e1d51dd`; the attached source bank matches the canonical manifest. Every inherited entry has an individual audit row. All 73 inherited information identifiers have an explicit narrow interpretation and an example of an unsupported extension. All examples are fictional and were authored/reviewed in this same Chat context.

## Material repairs

### Comparisons now compare the same response task

The old new-group scene asked what the person would do, but the invitation follow-up asked which role they would accept. That changed both the situation and the response task. The revision uses the same shared-meal setting and asks what they would do in both conditions. A difference is retained as a conditional self-report, not evidence for a global trait or psychological mechanism.

Workload variants reset from the stated baseline rather than accidentally accumulating prior conditions. Variants that stipulate joining a project or intending to finish are visibly hypothetical; they cannot rewrite an earlier refusal into biography.

### A plausible action no longer supplies its reason

A bare agreement gets one open reason question. An already-given reason is retained, not re-asked or replaced with suspected guilt. Negotiation gets an action-matched follow-up rather than a yes/no template. A feeling such as “bad” is clarified before it becomes guilt, sympathy or obligation.

The shared-meal noticing question cannot establish responsibility merely because the respondent noticed food or another person. Two optional help-specific prompts distinguish felt responsibility and limits when a real helping choice is under discussion. They are not follow-ups to every friendly decision.

### Several questions no longer make the desired behavior inevitable

The promised-task question now asks what happens rather than what keeps the person following through. The after-decision question no longer assumes an opposite pull persists. Recovery asks what happens after stopping rather than assuming that a known technique restores energy. A rich answer can eliminate the need for those probes.

### Emotion, motivation and bodily information are not collapsed

Disappointment when a friend cancels does not establish resistance to novelty. A separate optional comparison addresses familiar versus new activities without relying on disappointment. Concern for an anxious person does not automatically mean the respondent's mood changed. Affection does not answer sexual desire.

For bodily responses, within-choice duration, cross-choice occurrence and perceived usefulness are distinct. Explicit no sensation blocks sensation-specific probes. Generic decision clarity remains available independently. When an answer already describes duration and an exhaustion exception, the next useful probe—if needed—is only about usefulness outside that exception, not a repetition of the whole topic.

### Follow-ups now have an exact conversational referent

The final artifact removes the obsolete single-parent field that coexisted with the newer context-reference field. A follow-up must bind to the particular scene and answer, not to the most recent message by position. After a topic change, the question names the earlier scene in its actual delivered wording. It is insufficient to record the intended referent only in an internal note.

The 32-branch challenge set includes a delayed question about tension after an argument, after a resources discussion intervened. The repaired delivered question explicitly names the argument. It cannot accidentally become a question about feelings around money.

### The interview does not consume every available question

There are 79 bank entries: the 75 reviewed entries plus four optional routes for responsibility, limits on help, novelty, and weakening closeness beyond contact frequency. Thirty inherited question texts were revised. There is no required 79-question survey and no claim that calling prompts optional proves a shorter interview.

The protocol requires a reason why the next answer could change the description. An empty category alone is not a reason. Supplied reasons, conditions and comparisons are reused across the conversation at their actual scope. Unknown, inapplicable and declined answers remain distinct; they neither earn coverage credit nor invite endless retries.

## What was challenged

The 32 authored dialogue branches cover bare answers, full answers, mixed motives, negotiated responses, conditional responses, ambiguous feelings, absent versus unknown signals, already-decided choices, nonadjacent references, no retreat need, declined romance, elected role substitution, corrections, answer-plus-stop messages, normative-plus-personal clauses, repeated confusion, counterfactual participation, respondent-added assumptions, affection versus desire, no identified skill, and scoped refusal to discuss repair.

Each branch includes the actual question, fictional reply, proposed next utterance, narrow retained information, rejected continuation and review rationale. These are direct examples of the proposed behavior, not a test that simply counts author-assigned labels. Static checks verify their IDs, provenance fields and internal consistency; **the judgments about meaning are mine**, not an automated semantic score.

A confirmation pass found and repaired four additional issues: competing parent-reference fields; an antecedent recorded in commentary but not sufficiently specified in delivered wording; a still-useful narrower question hidden by a generally rich signal answer; and an opportunity prompt that had lost its scene cue. Those changes are recorded in ITERATION-LOG.json. Historical fictional transcripts and their old labels were not rewritten to manufacture success.

## Evidence and source limits

All 73 identifiers are reviewed as information-planning aids. The evidence guide deliberately includes examples that support only part of a compound identifier, such as physical affection without sexual desire. That is a correct partial record, not a failing person and not a completed whole field. A scenario supplies no observation count, and a source quotation does not validate an overbroad interpretation.

The method reuses the already-established question-evaluation approach. CDC/NCHS describes open probes into how an answer was reached and findings grounded in respondents' experiences. GOV.UK guidance supports asking only needed questions, permitting genuine uncertainty and reusing information. Neither validates this particular instrument or requires importing form navigation into the conversational flow.

Verified primary guidance, 19 September 2026:
- CDC/NCHS, Cognitive Interviewing: https://www.cdc.gov/nchs/ccqder/question-evaluation/cognitive-interviewing.html
- GOV.UK Design System, Question pages: https://design-system.service.gov.uk/patterns/question-pages/

This is a bounded continuation of the same research-informed design, not a new psychometric framework or a new mandatory validation campaign. The remaining uncertainty is actual user and runtime performance. Filling a behavioral checklist still does not prove full AstroHD chart or birth-time recovery; those remain separately governed outcomes.

## Privacy and continuation

The owner-device private archive remains outside the public repository and outside Railway. The current audit request was appended as design feedback, and the portable export was read back. No pilot answer has been fabricated. The per-turn requirement to save exact questions, exact answers, evidence mode, corrections and verification remains in force. The helper is not background monitoring and no automatic Railway synchronization is claimed.

Design files and public verification belong in humandesign. Personal content and content-derived hashes do not. When the owner resumes, the next task is the saved Chat pilot using this revised protocol, not more basic questionnaire repair. This report does not itself resume it.

## Reading and reproduction

Start with INTERVIEW-PROTOCOL.md and SCENARIO-BANK-v5.md. NODE-AUDIT.json contains the individual 79-entry review. EVIDENCE-REVIEW.json contains 73 scoped interpretation examples. DIALOGUE-CHALLENGES.md presents the 32 actual proposed branches. VERIFICATION.json reports executed static checks; it is not an independent human-validity certificate.

The packet includes the frozen input bank and source requirement list. `python3 check_design.py` checks the artifact relationships without contacting any service. The two build scripts reconstruct the bank and dialogue examples; do not run them over an existing frozen folder unless intentionally creating a new candidate revision.
