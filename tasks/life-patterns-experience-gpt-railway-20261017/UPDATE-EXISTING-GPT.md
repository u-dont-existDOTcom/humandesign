# Update the original Life Patterns Custom GPT in place — experience v2

**Owner-only GPT editor step.** This cumulative update builds on the October 17 early Railway review package. It does not create a second GPT, reset existing Actions or credential, change a saved review ID, or alter earlier respondents.

1. Open the **existing** Life Patterns Custom GPT editor, not a new GPT.
2. In the resulting ZIP, replace its **Instructions** with the entire file named INSTRUCTIONS-life-patterns-voice-interviewer-v2.md. This is under the strict 8,000-character limit.
3. Retain the original eight Knowledge files, and add the two new files: knowledge/EXPERIENCE-MEANING-OPTIONAL-v2.md and knowledge/experience-meaning-v2.json. The package contains all ten complete Knowledge files, so replacing with the complete set is also safe.
4. Replace the *existing* Action schema with ACTION-life-patterns-submission-openapi.yaml, version 1.9.0. Keep the exact same Action URL and **existing private bearer secret**. Do not remove/recreate the Action credential.
5. Save the same GPT in place. Verify the optional interview prompt and the Action schema include the optional experience_record_json parameter. A participant choosing Railway should complete the experience module on Railway; do not ask it twice in GPT.
6. If the Railway deployment is not yet v1.9.0, do not activate the GPT update ahead of the receiving backend. This package has no private participant answers.

**Behavior:** After independently reviewing the primary answers and freezing CF003, the GPT offers up to four core experience questions and up to four participant-selected topics, with separate consent and usual versus peak intensity. Optional results travel as a *third, separate, unscored* record in the same final submission call. A participant declining the module submits the original two records unchanged.

**Research boundary:** This module is post-review exploratory; it is not part of the original blind validation. Old records and unrelated Railway environment changes must remain intact.
