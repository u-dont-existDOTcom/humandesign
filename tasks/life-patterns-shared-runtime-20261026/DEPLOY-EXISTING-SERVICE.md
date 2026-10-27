# Activate the prepared shared-topics release

The code is merged and verified. Current public Action remains **1.9.0**. Railway account/service reads work, but the source-change calls in this session were interrupted without a receipt. This file is an exact release handoff, not a success claim.

## Existing target

- Project: `humandesign-relationship` (`97658d58-84ab-40c8-ab1d-1be06600c4b5`).
- Service: `life-patterns-participant` (`30746eb8-07c9-42e7-8825-152124b9337d`).
- Environment: `production` (`b9916074-da51-46a1-8d7d-fd618b3c3d2a`).
- Repository: `u-dont-existDOTcom/humandesign`.
- Prepared branch: `deploy/life-patterns-shared-topics-v110-20261027`.
- Exact commit: `9cf9527075a39b3f30e9bbb698cf5e56740bbe96`.

Use the existing service's source connection to pin that exact commit. The prepared commit already selects `apps/life-patterns-participant/Dockerfile`. It is the merged, tested application plus the same participant-only Railway configuration as the previous deployment. The canonical research branch's root configuration belongs to the separate relationship application.

The corresponding existing-service connector operation is:

```json
{
  "projectId": "97658d58-84ab-40c8-ab1d-1be06600c4b5",
  "serviceId": "30746eb8-07c9-42e7-8825-152124b9337d",
  "repo": "u-dont-existDOTcom/humandesign",
  "branch": "deploy/life-patterns-shared-topics-v110-20261027",
  "commitSha": "9cf9527075a39b3f30e9bbb698cf5e56740bbe96"
}
```

Before retrying, inspect the current source, deployments, environment inventory and staged changes. An interrupted operation may have completed after its response was lost. The last observed state is in LIVE-DEPLOYMENT-RECEIPT.json. Keep the existing `/data` volume, one replica, database and keys. No new infrastructure or credential rotation is needed. The source operation is service-wide across environments; the last inventory contained only production. Do not accept unrelated staged changes.

## Confirm activation

Require a terminal successful deployment for the exact commit above. Then read:

- `https://life-patterns-participant-production.up.railway.app/healthz`: status ok, shared supplement available, unchanged main question-policy identity.
- `https://life-patterns-participant-production.up.railway.app/action-openapi.yaml`: version `1.10.0`, exact bytes matching the published `action-openapi-v1.10.yaml`.
- `/assets/shared-evidence.js`, `/assets/experience.js`, `/assets/finish.js` and `/finish`: exact published asset bytes, privacy headers retained.
- Unauthenticated finish state, GPT review and admin record routes must still reject access. Use nonexistent IDs and no credentials; no respondent record is needed.

The old known source `7de212f027e14c198fb58dc91d11df3068d58e56` on `deploy/life-patterns-experience-v19-20261018` is the rollback reference. This release introduces no database migration.

After live verification, install `Life-Patterns-GPT-Shared-Topics-v1.10-2026-10-26.zip` into the existing private GPT using its UPDATE-EXISTING-GPT.md. Replace Instructions and Action, replace one Knowledge guide and add two Knowledge files. There are thirteen Knowledge files in the complete set. Retain the existing private bearer configuration. Do not upload intake metadata, researcher provenance or participant records as Knowledge.
