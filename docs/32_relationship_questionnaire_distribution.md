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

## Participant incentive: satisfy curiosity after the freeze

The survey should not feel like unpaid data collection. Completion should unlock a useful personalized reveal.

### Reward 1 — Relationship fingerprint

Immediately after the participant reviews and freezes their answers, show a plain-language profile derived from their own responses, not from astrology. This can be genuinely interesting even if the symbolic model ultimately fails.

The reveal should summarize the relationship as a multidimensional pattern rather than one compatibility score, for example:

- attraction and sexual desire in each direction;
- whether love and `in love`/Eros were reciprocal or asymmetric;
- sexual chemistry versus libido mismatch or habituation;
- intellectual compatibility versus intellectual stimulation/self-expansion;
- shared interests and mystical/spiritual resonance;
- psychological intimacy/confiding versus emotional readability;
- playful drama versus serious conflict;
- repair/recovery style;
- autonomy, engulfment, jealousy, and how these change with closeness or threat;
- practical future fit;
- strongest relationship assets;
- strongest mismatches or tradeoffs;
- important unknowns where the participant did not have enough evidence.

The value proposition is not `we will tell you whether you are compatible`. It is closer to:

> See the actual shape of your relationship — including differences between love, attraction, sex, intellectual fit, emotional ease, autonomy, and long-term life fit that ordinary compatibility tests collapse together.

Where both partners participate independently, an optional paired reveal can compare their two fingerprints after both have frozen responses and both consent to the comparison. It should distinguish disagreement from asymmetry rather than deciding which partner is correct.

### Reward 2 — Blind Astro/HD prediction reveal

If the participant supplies the necessary birth data and the study mode includes symbolic prediction, reveal the frozen model only **after** the response record is sealed.

The result should be presented as a prediction audit, not fortune-telling:

- `Predicted strongly and matched`;
- `Predicted weakly / ambiguous`;
- `Predicted and missed`;
- `Not predicted by this model`;
- `Could not score because birth time or response evidence was insufficient`.

Then show the main chart features behind each frozen prediction in ordinary language. Participants should be able to see surprising hits **and** obvious failures. Do not hide misses behind new post-hoc interpretations.

The curiosity hook is therefore:

> Before you see the astrology/Human Design reading, describe the relationship. Then see what the chart predicted without being allowed to change its answer after hearing yours.

This is more interesting than a conventional astrology reading because the participant gets to test whether it actually knew anything.

### Reward 3 — Optional comparison against ordinary relationship science

A stronger later version can show three columns after completion:

1. **What you reported** — the relationship fingerprint;
2. **What established relationship constructs would emphasize** — e.g. desire discrepancy, responsiveness, autonomy, conflict/repair, commitment;
3. **What Astro/HD predicted before seeing your answers**.

This makes the experience educational even for a participant who is skeptical of astrology. It also prevents the symbolic result from being the only source of perceived value.

### Curiosity-preserving UX

Before completion, the UI may say things such as:

- `Your answers will build a relationship fingerprint.`
- `At the end, you'll see which dimensions were unusually strong, asymmetric, or context-dependent.`
- `If you provide birth data, you'll also see what the frozen Astro/HD model predicted before your answers were compared with it.`

Do **not** reveal which current question maps to which chart feature, what answer is expected, or partial prediction results while the questionnaire is still running.

A progress screen can tease completed dimensions without revealing their values, for example:

- `Love & attraction mapped`
- `Sexual pattern mapped`
- `Mind & communication mapped`
- `Emotional/autonomy pattern mapped`
- `Practical future fit mapped`

This gives a sense of accumulating insight without contaminating later answers.

## Two deployment modes

### Development phenotype capture

Use when collecting additional development relationships before looking at their charts.

Flow:

1. participant opens public link;
2. app asks the six frozen core relationship anchors in order;
3. after each answer, the backend records which phenotype axes remain unresolved or which neutral applicability flags were triggered;
4. `select_next_capture_question` chooses only relevant follow-ups;
5. raw answers and the completed phenotype record are frozen;
6. show the non-astrological relationship fingerprint;
7. birth/chart data may be inspected only after the phenotype freeze if the experiment requires chart-blind development;
8. if applicable, reveal the later Astro/HD audit as a separate layer.

No chart prediction is needed to run this mode.

### Validation / rectification

Use only after a model version and candidate prediction matrix have been independently frozen.

Flow:

1. create/freeze candidate charts and their predicted response likelihoods outside the participant UI;
2. participant begins the survey without seeing those predictions;
3. the backend passes only anonymous candidate weights and unanswered-question likelihood matrices into `select_next_validation_question`;
4. selection uses the existing repository rule: expected information gain × expected reliability − burden;
5. participant prose is classified separately under the blind relationship classifier protocol;
6. raw answers, classifications, and predictions are independently frozen before scoring/reveal;
7. show the relationship fingerprint first;
8. then show the frozen prediction audit and misses.

The selector must not receive birth metadata, true-candidate identity, candidate rank, participant prose, or classifier rationale.

## Hosting recommendation

For an initial public pilot, use a small hosted web application rather than Google Forms/Typeform-style static forms. Static conditional branching can hide/show questions, but it cannot faithfully implement the repository's candidate-blind expected-information-gain selection without reproducing substantial backend logic elsewhere.

A lightweight hosted app needs only:

- responsive participant UI;
- session store/database;
- the checked-in questionnaire JSON/rubric registry;
- the relationship questionnaire routing module;
- an API layer around session creation, answer submission, next-question selection, pause/resume, and final freeze;
- a relationship-fingerprint renderer;
- an optional post-freeze Astro/HD audit renderer;
- administrative export of de-identified response packages.

A platform such as Replit is suitable for a fast pilot because it can host the UI, backend, and database under one public URL. For later formal research, the same repository code can be deployed to a more controlled host without changing questionnaire semantics.

## Share channels

Once deployed, distribution is simply the public survey URL. It can be shared through direct message, email, WhatsApp/Signal, social posts, participant-recruitment communities, or a QR code. Recruitment text should describe the survey generically as relationship research and should not disclose which chart features predict which answers.

The public hook should emphasize the participant payoff, for example:

> Map the real shape of one important relationship, then see what a blinded Astro/HD model predicted correctly — and what it got wrong.

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

1. short intro explaining the two rewards: relationship fingerprint and optional blind chart reveal;
2. consent;
3. relationship context;
4. one large prompt at a time;
5. optional examples/probes shown only when needed;
6. visible progress described broadly (`Core questions`, then `A few follow-ups`) rather than displaying scored domains;
7. save after every answer;
8. final review screen where participants may correct wording before freeze;
9. freeze answers;
10. show personalized relationship fingerprint;
11. if eligible, show frozen Astro/HD prediction audit;
12. completion receipt/session code.

Do not expose hidden classifier labels, chart predictions, candidate counts, EIG values, or which question was chosen because it discriminates among charts before the freeze.

## Minimal viable pilot

The fastest participant-worthy pilot is:

- development-capture mode;
- six core anchors plus adaptive phenotype follow-ups;
- pseudonymous session ID;
- SQLite/Postgres-style persistent storage;
- raw-answer JSON export;
- an attractive personalized relationship-fingerprint result page;
- no astrology shown until answers are frozen;
- chart data entered/revealed only after phenotype completion when chart-blind capture is desired.

The **result page is not optional for public recruitment**: it is the primary participant incentive.

After that UX works reliably, add validation mode with frozen candidate prediction packages, answer-blind EIG selection, and the post-freeze Astro/HD hit/miss reveal.
