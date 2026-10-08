# Question objections: live researcher inbox and versioned wording proposals

The owner's actual goal had two parts: question-quality complaints should reach the researcher, and objections should result in real question improvements rather than merely a rule that tells the reviewer not to overinterpret weak answers.

## Earlier gap and correction

The original 79-answer pilot was analyzed and generated important nonredundancy/information-gain safeguards. It **did not directly replace question wording based on the latest pilot**. New tendency-first prompts had separately replaced old scenes before this audit; the latest specific corrections were largely incorporated as model policy and a source-audited report. The service already preserved process feedback but lacked a researcher inbox. Describing those policies as “fixed questions” was too broad.

## Verified live return loop

The consented review request carries exact question critiques in the unchanged source alongside any separately captured behavioral response. The backend can also recognize a small number of explicit untagged objections, and extract independently classified process-feedback quotes. Researcher-only GET `/api/admin/question-feedback` reads retained reviews, clarification histories, final submissions and consented direct Railway sessions; no extra participant Action or permission card is required. The private `/admin` page displays the route, exact displayed question, safe feedback excerpt and a nonauthoritative issue category. The researcher can set New, Investigating, Revision proposed with a version ID, Resolved or Dismissed, persisted without editing participants' interview records. Feedback can be downloaded privately as JSON. The inbox is not a push notification or automatic issue/comment-to-code pipeline. Feedback supplied before consent or before any review transmission is not available to the service. The researcher must assess it.

The successful deployment uses a verified minimal archive of the merged implementation; Railway reports deployment `48b43d03-930a-4a37-8cfc-d4c704ee977d` SUCCESS. Live `/healthz` and `/admin` both return HTTP 200. Unauthenticated feedback GET returns HTTP 401; authenticated feedback, submissions and sessions GET all return HTTP 200 with 9 feedback items, 1 existing submission and 4 sessions at readback. No private source text, IDs or credentials are included in repository receipts. No human interview was mutated by the readback. Prior successful deployment is retained in Railway.

## Actual proposed question rewrites

Nine current TF1 question texts have been rewritten in `tendency-first-v2-development.json` with old/new wording in `QUESTION-REVISION-CROSSWALK.md`; three weak legacy optional probes are marked for retirement. This is a **not-active development candidate**, NOT a change to frozen v7 or the current version-pinned v1 survey. No participant was retroactively rescored and these rewrites have not been shown effective or predictive in a new cohort. A new prospective policy version, cognitive wording test and compatible old/new state routing would be needed before activation.

## Verification

- 215 participant application tests passed; 1,021 repository tests passed with six unrelated astronomy skips.
- Hosted verify and survey-browser checks passed, merge verified.
- Scoped changed-file lint passed with existing legacy exclusions; new feedback module mypy passed with dependencies skipped. Historic participant-wide strict typing debt is not claimed resolved.
- Protected admin route/auth and disposition tests passed; readback on live service passed.
- Cumulative existing-GPT ZIP and separate development question crosswalk are already in the researcher's OS Downloads directory.

## Remaining owner actions and explicit limits

To capture **new** critiques verbatim inside the private GPT on future interviews, apply the delivered cumulative Custom GPT editor packet. The backend inbox already works for records and complaints it can recover without that editor update. That edit must retain the existing action credential, GPT and saved reviews.

The nine proposed rewrites are not live questions. Researcher review and an independently versioned prospective activation remain optional work. The previous owner's real frozen-record final submission also remains separate and unconfirmed until a real receipt appears; the synthetic submission demonstration never proves the owner's records were stored.
