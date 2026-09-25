# V1.5 live new-person pilot — operational receipt

Verified 2026-09-25. The participant-reviewed test is live at https://life-patterns-owner-production.up.railway.app/birth-test. The optional automatic interpretation service reached its configured provider but is blocked by `HTTP 429: credit_balance_exhausted`. No credit was purchased, no provider/model was substituted, and a successful live automatic interpretation is not claimed.

## What is now usable

The old fixed replay scorer did not read current survey answers. The new V1.5 path accepts current participant-confirmed behavioral interpretations and changes candidate scores under the same six astronomical clauses. The participant can answer nine original scenario-bank-v7 prompts, or import an existing interview, then review five explicit neutral interpretations. Direct manual confirmation is itself a self-report; it is not represented as evidence that an earlier scenario established a trait.

The birth date is not used to select or fit rules. Responses/profile, model/scorer/bridge identity and candidate panel are frozen first. Only afterward is the documented actual birth instant supplied for a rank comparison. Current answers can change the ranking; changing wording without changing the reviewed interpretation need not. Every edit invalidates the displayed old ranking and requires renewed review. Earlier frozen inputs/results are retained in the export. A delayed interpretation cannot overwrite subsequently edited answers. Subsequent edits after a ranking has been shown are labeled exploratory.

This is a candidate-panel test: 999 seeded century-random decoys plus the separately checked actual instant is the primary comparison. Secondary nested panels contain99 or9999 decoys. It is not an exhaustive century scan for a new participant or a calibrated probability. The original owner's full-century scan remains a distinct historical development result. Birth-time uncertainty and provenance are reported, not silently converted into exact-minute accuracy.

## Fixed astronomical source versus new behavioral hypothesis

The six astronomical clauses and their source/manifest hashes are unchanged. Five clause instances use criteria in Lilly's published strength/house/aspect table; one uses Phaladeepika's Venus directional-strength criterion. This does not mean Lilly invented every criterion or supplied five complete modern personality predictions.

The subset was selected using a known development birth target. The modern behavioral meanings and aggregation are additional modeling choices. V1.5 makes those meanings explicit rather than pretending that historical strength rules directly imply questionnaire answers. For a present clause, a supported affirmative interpretation contributes+1 and an explicitly opposing interpretation contributes-1; absent clauses, unknown/mixed evidence, and nonapplicability contribute0. No continuous astrology coefficient is fitted. The broad inherited work-energy-range label is not assigned an invented positive pole; Saturn retains its existing solitude/privacy connection.

Romantic connection affects up to three votes. Six votes are not six independent traits. The all-positive historical-signature baseline is displayed separately; when a person's interpretations yield the same positive signs, the app warns that their ranking equals that baseline. Many people may share a coarse profile. Smaller, source-checkable rules improve interpretability and falsifiability, not automatically out-of-sample validity. Selection from hundreds of rules still permits overfitting.

## Deployment and preservation

The research branch is `chat/v15-survey-decoder-20260925`. The deployed integration was deliberately narrowed to required files on the exact incumbent production commit, excluding unrelated research modifications. PR30 merged to the existing configured branch `codex/discover-life-patterns-mvp` at commit `3e82806d8877510ecc081ece69b9de1f74f4c76f`.

Railway deployment `2d60d3dd-2634-427c-a48f-62a36ee27350` is SUCCESS on that commit. No Railway source/start-command changes were required: the original deployment entrypoint mounts the additional route. Original interview, authentication, provider settings, domain and service were preserved. The unrelated staged environment patch was not committed by this work. No new paid service was created. Previous successful deployment remains the rollback.

Public root and /healthz returnedHTTP200. The live city lookup returnedHTTP200 and eight Philadelphia results. The /birth-test browser flow completed successfully against the actual Railway domain.

## Tests and actual consumer evidence

- 28 exact-release affected tests passed, covering the answer-dependent decoder, original interview API and actual deployment-entrypoint authentication. Earlier broader V1.4/V1.5 affected run passed31 tests.
- Strict type checking passed across215 source files with narrow documented compatibility settings for retained hash-frozen historical code and the untyped Swiss extension. New V1.5 code remains strict.
- Changed active files passed scoped lint. Global repository lint is not claimed green:721 diagnostics were reproduced on the unchanged deployed baseline. Narrow frozen-source style exceptions preserve the historical scientific artifact hash. This does not certify unrelated code quality.
- Hosted unit/integration tests and the incumbent survey-browser check passed on the initial integration candidate; the repository-wide lint step retained baseline failures.
- The real headless browser test passed locally, on the exact production-based candidate and on the deployed website. On the live test, the synthetic all-positive case scored6; explicitly changing the sharing-understanding interpretation changed its score to4 under the same model. In this particular999-decoy fixture its rank stayedfirst, demonstrating that a score change need not move rank. A separate real-candidate test verified that different supported/contradicted profiles change candidate ordering without changing the model or panel.
- Live browser checks verified original frozen inputs were preserved, changed inputs invalidated old results, stale interpretation output was discarded, there were no page errors, and the390-pixel mobile viewport had no horizontal overflow.
- All probes used synthetic software fixtures or the existing known development instant. No new person's success or predictive validity is claimed.

## Automatic interpretation gate

The optional AI path is implemented and has source-exact quotation checks, neutral-definition-only structured payloads, basic obvious birth-key screening, and participant-review requirements. Mocked deterministic tests cover those interfaces, but they do not establish successful live provider execution.

The real live synthetic request reached the configured provider and returned `Owner Life Patterns model HTTP 429: credit_balance_exhausted`, exposed by the endpoint asHTTP422. A combined smoke-script request was blocked by the platform as indeterminate; it was not repeated unchanged. Independent browser verification and narrower explicit synthetic/read-only probes were admitted. One provider call was made, not a retry campaign. The provider's billing identity was not established from safe metadata; no secret values were read into this receipt. Replenishing or changing a paid/provider account remains an owner-controlled action. After any such action, successful live interpretation still needs verification; do not assume it is already proven.

The manual-review path is usable now and does not spend model credits. For the current test, skip the optional 'Suggest interpretations' button and have the participant review the five neutral statements directly. Existing raw-answer/profile snapshots remain unchanged.

## Data and evidence identities

Raw responses remain in the participant browser unless optional interpretation is explicitly requested. Rankings receive only the confirmed profile, birthplace and provenance hashes. Runtime result handles are unguessable and limited; the UI provides export and deletion. Export files contain private answers and should be shared only with participant permission. No real third-party response data were collected in this implementation task.

- Live-browser receipt SHA-256: `5dd5b37df52d100e568e4ef68ae9ec825542538dfb5eb2a8dced46c7ad92ff83`.
- New bridge SHA-256: `89b3766fcfd1c6935335bd13dba9ff812e7f3f7df1ec887e63512b2200c5e076`.
- New scorer SHA-256: `f0e4ac2887531c3ef206c612c0e3fa7dcb3ee30298a3b20bd4e0061c61cc19cb`.
- Unchanged V1.4d model SHA-256: `4bd0b02cc099142f932cc608e821d5db6539e1ec88a67c1d4f93f638d4cc0e83`.
- Unchanged V1.4 rule-module SHA-256: `0a7f3662891475c7b61efcd130c468f8e9c48b4d61e3c2072d4d0c054e9d87cc`.

## Completion boundary

Status: CORE_NEW_PERSON_TEST_LIVE_AND_VERIFIED / OPTIONAL_AUTO_INTERPRETER_CREDIT_BLOCKED / SCIENTIFIC_VALIDITY_UNESTABLISHED.

The immediate usable participant-reviewed test is delivered; automatic free-text interpretation is explicitly blocked rather than claimed complete. The next research input is a consenting new participant's first frozen result. Preserve misses and ties; do not silently refit the model on that person and call it validation. Future development revisions remain allowed when explicitly versioned. No background research work is claimed.
