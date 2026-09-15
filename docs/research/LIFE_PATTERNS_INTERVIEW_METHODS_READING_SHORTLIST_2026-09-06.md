# Life Patterns: complementary interviewing and measurement books

Date: 2026-09-06
Status: bounded existing-work scan and reading recommendation, not an interview release or implementation change.

## Recommendation

Prioritize Herbert J. Rubin and Irene S. Rubin, *Qualitative Interviewing: The Art of Hearing Data*, third edition. Next prioritize Gordon B. Willis, *Cognitive Interviewing: A Tool for Improving Questionnaire Design*. These address different needs: conducting a useful responsive research conversation, and testing how respondents understand and answer questions.

Use the other references below for specific gaps rather than adding every book's recommendations to the runtime prompt. No participant needs to repeat a completed interview because of this reading list.

## Scope and evidence boundary

This assessment checked publisher descriptions, tables of contents, and available chapter summaries. It is not a full-text review of these five books and does not establish their effectiveness for an AI interviewer or the validity of this project's measurements. Project applications below are recommendations, not claims made by the books about Life Patterns or AstroHD.

The starting design remains pattern-first, age-aware, source-grounded, attentive to participant autonomy, and separate from directional behavior-change coaching. The existing MI assessment is retained. Choice after the scan: adapt established interviewing and measurement methods; do not invent another ontology or scoring framework here.

PR #24 was read at head `845ad42482e1777b0ed1f7e5052303ad3f133184` before this additive documentation change. The existing MI applicability memo was read at that commit. No runtime, deployment, codebook, private interview, or frozen source is changed.

## Ranked references

### 1. Qualitative Interviewing: The Art of Hearing Data — Herbert J. Rubin and Irene S. Rubin, third edition

Verified scope: responsive qualitative interviewing; conversational partnerships; interview structure; main questions, probes and follow-up questions; analysis and reporting. The publisher describes an iterative relationship between design, data gathering and analysis. [1]

Project use: improve movement from a broad reported pattern to a participant-specific process or distinction, without repetitive questioning or substituting the interviewer's interpretation. Assess the difference between opening a topic, clarifying an existing answer and following a newly raised issue.

Targeted reading: chapters 6–10, especially chapters 9 and 10 on main questions/probes and follow-ups.

Boundary: iterative development is useful before measurement freeze. It does not authorize revising a confirmatory instrument after inspecting target-model fit. A book recommendation is not evidence that the AI applies these skills successfully.

### 2. Cognitive Interviewing: A Tool for Improving Questionnaire Design — Gordon B. Willis

Verified scope: questionnaire development and pretesting; think-aloud and verbal probing; concurrent versus retrospective interviewing; proactive/reactive probes; analysis and documentation of findings; avoiding probing pitfalls and artificial problems. [2]

Project use: distinguish unclear wording, retrieval difficulty, overbroad scope, redundant questioning and mismatched assumptions. Treat a complaint about a question as data about the instrument before treating it as a participant problem.

Boundary: cognitive interviewing evaluates the questions. It is not a reason to ask every production participant to explain their thinking about every question. We should use targeted pretesting/debriefing rather than add a second interview inside the first. It cannot alone establish population discrimination or construct validity.

### 3. The Psychology of Survey Response — Roger Tourangeau, Lance J. Rips and Kenneth Rasinski

Verified scope: comprehension, memory, dates/durations, factual estimates, context effects, response formatting, sensitive-topic reporting and collection mode. Chapter 3's available summary explicitly warns about the accuracy costs of demanding difficult memory retrieval. [3]

Project use: inform the distinction between reported recurring experience, a particular recollection, estimated frequency and present interpretation. Review whether a question asks for precision the participant cannot reasonably supply.

Boundary: neither a general pattern statement nor a vivid episode should automatically outrank the other for every purpose. Specific project evidence rules require their own justification; these references do not make adult retrospective childhood reports contemporaneous observations.

### 4. Calendar and Time Diary Methods in Life Course Research — edited by Robert F. Belli, Frank P. Stafford and Duane F. Alwin

Verified scope: event-history calendars, time diaries, life-course applications, computerized instruments and data-quality/reliability/validity assessment. The contents include chapter 3 on the rationale for calendar interviewing, chapter 9 on global versus episodic reports of hedonic experience, and chapters 15–16 on evaluation and timeline-data quality. [4]

Project use: examine a light-touch life-period scaffold for placing reported patterns and changes using participant-supplied life landmarks. This is a candidate adaptation, not a validated new protocol. Preserve uncertain ranges and separate supplied anchors from inferred dates.

Boundary: do not demand a complete life calendar, impose a developmental cutoff, choose ages using target predictions, or extrapolate findings on hedonic experience to personality measurement without evidence. Retrospective age-tagged data are not a prospective longitudinal study.

### 5. Scale Development: Theory and Applications — Robert F. DeVellis and Carolyn T. Thorpe, fifth edition

Verified scope: reliability, validity, item development/evaluation, optimizing instrument length, distinctions between scales and indices, factor analysis and item response theory. [5]

Project use: later measurement evaluation of the concern that some questions contribute little information. Examine clarity, observable variability, redundancy, reproducibility and retained coverage rather than choosing questions because they sound interesting or elicit unusual answers.

Boundary: the current multi-label episode codebook is not automatically a unidimensional reflective scale. Do not apply coefficient alpha or factor-analysis assumptions to all heterogeneous codes by default. Clear conversational wording, variation between respondents, coder reliability and external-model validity are distinct targets. This is a later-stage reference rather than the first book for conversational conduct.

## Adjacent reference considered

Robert S. Weiss, *Learning From Strangers: The Art and Method of Qualitative Interview Studies*, is a credible alternative to Rubin and Rubin for practitioner examples of successful/unsuccessful interviews and the complete qualitative interview-study process. It is not a priority additional purchase/read because it overlaps the first recommendation. [6]

## Proposed application, not performed in this turn

Begin with targeted reading of Rubin and Rubin and Willis. Use authorized existing development excerpts or clearly synthetic examples to compare proposed interviewer responses against the present implementation on source fidelity, useful clarification, repetition, correction uptake and burden. Counterfactual rewritten turns are not observed participant outcomes. Evaluate future real interactions separately before claiming that the changes improve accuracy or shorten interviews.

Preserve participant narratives privately. Do not upload them, book files or copyrighted chapters to the public repository. No new personality constructs, scoring weights, model comparisons or interview prompts are introduced by this memo.

## Verified publisher sources

[1] SAGE, third-edition description and contents: https://www.sagepub.com/shop/buy-a-book/qualitative-interviewing-3-234196 ; responsive-interviewing description: https://in.sagepub.com/en-in/sas/node/53455

[2] SAGE, description and detailed contents: https://www.sagepub.com/shop/buy-a-book/cognitive-interviewing-1-225856

[3] Cambridge University Press, description: https://www.cambridge.org/core/books/psychology-of-survey-response/46DE3D6F7C1399BCDC78D9441C630372 ; chapter 3 summary: https://www.cambridge.org/core/books/abs/psychology-of-survey-response/role-of-memory-in-survey-responding/A693DF1AA1D1E4ECADF74CF37BA63C7D ; contents: https://www.cambridge.org/core/books/abs/psychology-of-survey-response/contents/470BC1CDEAE907B90CAC1DBB2A002E84

[4] SAGE, edited-volume description and contents: https://www.sagepub.com/shop/buy-a-book/calendar-and-time-diary-methods-in-life-course-research-1-229475 ; chapter 9 authors and title: https://methods.sagepub.com/book/edvol/embed/calendar-and-time-diary/chpt/global-episodic-reports-hedonic-experience

[5] SAGE, fifth-edition description and detailed contents: https://us2.sagepub.com/en-us/nam/scale-development/book269114

[6] Simon & Schuster / Free Press, official description: https://www.simonandschuster.com/books/Learning-From-Strangers/Robert-S-Weiss/9780684823126
