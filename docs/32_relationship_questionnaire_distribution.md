# 32 — Relationship Questionnaire Distribution

Status: deployment/distribution guidance for the dynamic relationship questionnaire. This document does not alter the frozen questionnaire or scoring model.

## Recommended participant experience

Distribute the relationship questionnaire as a public web application with one question per screen.

Participants should not need to know Human Design, astrology, RRF, Love Styles, candidate charts, scoring, or which questions are adaptive. They should only see ordinary-language prompts about a relationship.

The public application should:

- generate a pseudonymous session ID;
- show a short consent/privacy notice;
- collect only the minimum relationship/birth metadata required by the declared study mode;
- ask one narrative question at a time;
- save the verbatim answer before selecting the next question;
- permit `I don't know`, `not applicable`, `mixed`, and context-dependent answers;
- support pause/resume through a private session token or link;
- never reveal predicted answer directions before response freeze;
- keep participant-facing data separate from chart-prediction/classifier internals;
- produce a frozen response record and hash before any reveal/evaluation step.

## Two deployment modes

### Development phenotype capture

Use when collecting additional development relationships before looking at their charts.

Flow:

1. participant opens public link;
2. app asks the six frozen core relationship anchors in order;
3. after each answer, the backend records which phenotype axes remain unresolved or which neutral applicability flags were triggered;
4. `select_next_capture_question` chooses only relevant follow-ups;
5. raw answers and the completed phenotype record are frozen;
6. birth/chart data may be inspected only after the phenotype freeze if the experiment requires chart-blind development.

No chart prediction is needed to run this mode.

### Validation / rectification

Use only after a model version and candidate prediction matrix have been independently frozen.

Flow:

1. create/freeze candidate charts and their predicted response likelihoods outside the participant UI;
2. participant begins the survey without seeing those predictions;
3. the backend passes only anonymous candidate weights and unanswered-question likelihood matrices into `select_next_validation_question`;
4. selection uses the existing repository rule: expected information gain × expected reliability − burden;
5. participant prose is classified separately under the blind relationship classifier protocol;
6. raw answers, classifications, and predictions are independently frozen before scoring/reveal.

The selector must not receive birth metadata, true-candidate identity, candidate rank, participant prose, or classifier rationale.

## Hosting recommendation

For an initial public pilot, use a small hosted web application rather than Google Forms/Typeform-style static forms. Static conditional branching can hide/show questions, but it cannot faithfully implement the repository's candidate-blind expected-information-gain selection without reproducing substantial backend logic elsewhere.

A lightweight hosted app needs only:

- responsive participant UI;
- session store/database;
- the checked-in questionnaire JSON/rubric registry;
- the relationship questionnaire routing module;
- an API layer around session creation, answer submission, next-question selection, pause/resume, and final freeze;
- administrative export of de-identified response packages.

A platform such as Replit is suitable for a fast pilot because it can host the UI, backend, and database under one public URL. For later formal research, the same repository code can be deployed to a more controlled host without changing questionnaire semantics.

## Share channels

Once deployed, distribution is simply the public survey URL. It can be shared through direct message, email, WhatsApp/Signal, social posts, participant-recruitment communities, or a QR code. Recruitment text should describe the survey generically as relationship research and should not disclose which chart features predict which answers.

## Consent and privacy

The public survey should clearly distinguish:

- the respondent's own data;
- information they provide about a partner;
- birth information;
- free-text relationship history.

Recommended defaults:

- pseudonymous participant IDs rather than names;
- optional contact information stored separately from survey content;
- explicit consent before saving relationship/birth data;
- an option to omit a partner's real name;
- no publication of raw third-party birth data or intimate narratives;
- separate researcher-only storage for answer-key/prediction packages;
- deletion/export path appropriate to the eventual study protocol.

## Suggested public UX

Keep the participant experience conversational rather than survey-like:

1. short intro and consent;
2. relationship context;
3. one large prompt at a time;
4. optional examples/probes shown only when needed;
5. visible progress described broadly (`Core questions`, then `A few follow-ups`) rather than displaying scored domains;
6. save after every answer;
7. final review screen where participants may correct wording before freeze;
8. completion receipt/session code.

Do not expose hidden classifier labels, chart predictions, candidate counts, EIG values, or which question was chosen because it discriminates among charts.

## Minimal viable pilot

The fastest scientifically usable pilot is:

- development-capture mode only;
- six core anchors plus adaptive phenotype follow-ups;
- pseudonymous session ID;
- SQLite/Postgres-style persistent storage;
- raw-answer JSON export;
- no astrology shown to participant;
- chart data entered/revealed only after phenotype completion when chart-blind capture is desired.

After that UX works reliably, add the validation mode with frozen candidate prediction packages and answer-blind EIG selection.
