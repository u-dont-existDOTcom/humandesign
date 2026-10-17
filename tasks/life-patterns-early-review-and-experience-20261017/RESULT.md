# Early Railway review and experiential chart-domain audit — 2026-10-17

## Owner outcome A: end endless GPT review check-ins

The v1.7.0 ready-only finishing link forced participants to stay in GPT through an indeterminate number of independent review rounds. This did **not** satisfy the owner's objective of a finite participant-facing experience.

Changed v1.8.0 behavior: after the consented source is submitted and Railway issues a saved review ID, the existing GPT offers a one-time secure Railway portal link **immediately**, whether status is queued, processing, clarification_needed, paused/blocked or ready. The old interview, answer sources, review ID, encrypted /data volume and old seven GPT Action routes are retained. The browser (separate HttpOnly/SameSite cookie) shows independent stage, actual answered/skipped counts and exact admitted questions. It rechecks status while open; the participant does not need to recontact the GPT. There is no fabricated global future question count or worker-time promise.

The portal now handles both fast-batch and legacy single-question review formats. It uses the existing source-bound encrypted storage method; each batch/answer is exact, explicitly skippable, and idempotent. The source/worker rejects new questions after the participant explicitly chooses **Stop further questions**. The server records that choice and preserves all prior answers plus skips for already admitted questions, invalidates any in-flight reviewer lease and requests an independent evidence-only final synthesis (including legacy reviews). This does not fabricate instant readiness: independent processing may remain queued, fail or require recovery. Only actual status ready permits source-quoted evidence confirmation, three separately frozen CF003 questions and transactional encrypted final submission.

## Owner outcome B: missing chart domains

The previous V7 bank has 79 named question records arranged in 29 existing situational families. It is not a full source-first chart trait inventory; its focus on choices, collaboration, workload, romance and routine problem solving fails to sample large parts of what traditional natal astrological authors discuss. Source check: Ptolemy III.13-14 explicitly includes the mind, emotional/sensory qualities and religious/philosophical dispositions; Lilly's ninth house describes religious matters, dreams and visions, and Book III includes natal ninth-house religious/journey judgements. These are **historical interpretive claims**, not statistically proven chart predictors.

**First chart-domain gap ledger:** `CHART-DOMAIN-V7-RECONCILIATION-v0.json` identifies 26 candidate domains; 9 absent, 7 proxy only, 7 partial, 2 directly sampled, one not appropriate for a routine personality survey. Some highly relevant overlooked fields: subjective meaning and search for it, awe/surprise, sudden insight versus gradual change, religion and worldview, dreams/visions, perceived guidance, meaningful coincidences with retrospective appraisal, creativity, family roots, vocation, and foreign-cultural experiences. A travel *planning scenario* is not actual travel history; deciding if one volunteer project is worthwhile is not equivalent to lifetime sense of meaning. Traditional house conventions do **not** directly prove that exact synchronicity or awe frequency follows from a particular planet/house.

`EXPERIENCE-MEANING-PILOT-v0.json` contains eight neutral noncompulsory prompts, with a default four-item optional path. Self report distinguishes frequency, intensity, meaning assignment, later reassessment, changes over time, personal presence of meaning and social-world contribution. There is **no new astrology mapping, birth prediction, updated accepted scoring, or compulsory repeat interviewing of existing participants**. The candidate must be piloted for participant comprehension and independent discriminant/retest value; only a future frozen a priori astrological prediction against controls could test actual predictive ability.

This is a **first source-anchored inventory**, not a comprehensive chapter-by-chapter audit of Lilly III, Ptolemy, Dariot, Hellenistic, Jyotish and retained book-study sources. Future complete atlas needs source-rule provenance, feature-direction prediction and ethically appropriate outcome type for each claimed domain, without using already inspected owner's or development participants' charts to design seemingly successful mappings. Source matrix preserves these explicit limits.

## Tests and release boundary

- Full participant app: 256 tests passed.
- Root repository: 1,089 tests passed, 6 astronomy/ephemeris fixtures skipped where production SWIEPH not installed in that run.
- Dedicated browser synthetic end-to-end: FAST batch answer, participant decline-further-questions, and LEGACY single question all reached existing secure ready confirmation, three CF003 answers and encrypted receipt without ChatGPT checks; no external browser requests or injected HTML execution.
- Privacy: No participant identities, sources, target DOBs, review IDs, Bearer credentials or final record content in git/release packages.
- Reproducible action v1.8.0 and cumulative same-GPT update (7,944 strict Instructions characters, eight knowledge files). A separate experimental domain audit is **not** included in the live GPT's behavior rules.

Publication and Railway production rollout are separately tracked. The private ChatGPT GPT editor can be updated **only** after copying these files into its existing configuration and clicking Update. A new source release does not mutate that private editor or any participant's current review.
