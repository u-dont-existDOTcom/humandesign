# Current state — Railway participant app repaired after first real Venice smoke

Read tasks/ACTIVE-TASK.json, apps/life-patterns-participant/README.md, and tasks/participant-railway-venice-20260927/FIRST-REAL-VENICE-ACTIVATION-20260928.json.

The owner ran the manual activation helper. This resolved the earlier uncertainty about Venice: the authenticated gateway smoke passed on GPT-5.6 Sol with XHigh. The participant service was enabled temporarily and reached a successful Railway deployment.

The real participant smoke then failed before showing its first question. Its saved synthetic session contains zero participant turns and three telemetry rows: two real Venice Plan calls (both GPT-5.6 Sol / XHigh) followed by question_or_evidence_admission_not_resolved; no semantic Admission call occurred. This narrows the failure to deterministic validation of the model-proposed empty-record opening, not Venice connectivity.

The repair is deliberately narrow: when there are no participant turns, imported source records, or evidence, the app now uses the frozen survey bank's first self-contained route A0 as the canonical opening without an LLM planning call. Venice remains adaptive after the participant supplies the first behavioral answer. The full 79-route bank remains a menu, not a quota, and no short survey was substituted. Focused app tests remain green.

The first activation helper also exposed a rollback transport bug: Railway CLI rejects setting an empty stdin variable. The repaired helper uses railway variable delete when the previous participant gateway variable was absent. After the failed run, the supervising chat explicitly restored PARTICIPANT_LIVE_ENABLED=0, cleared the participant gateway token, and redeployed. Health now reports both participant_enabled=false and provider_configured=false.

The repaired participant app (4105789f29d8278677686f73df0bece7c603a882) is deployed successfully as Railway deployment a3c900d3-0d67-478f-a36d-36f086346297, but remains disabled. The repaired activation helper is in later branch commit 81a055577a1c39eecce0d353b95e24d2cca2ad1a and is copied into ~/Téléchargements/Life-Patterns-Venice-Activation/.

No real participant record has been moved into the Railway app. The existing owner service remains unchanged. Existing unrelated Railway staged changes remain outside this task.

Next action is a human-side rerun of the repaired activation helper. Success requires: deterministic A0 opening; exact synthetic answer persistence; a real Venice planning call and independent semantic-admission call after that answer; a frozen synthetic export; and generated private researcher/participant links. Failure must restore the disabled state automatically.
