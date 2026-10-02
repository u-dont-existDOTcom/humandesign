# Plugin migration assessment — 2026-10-02

## Owner question
Should the Life Patterns participant surface move from a Custom GPT to a plugin now, and would a plugin remove the current Action/handoff UX problems?

## Current platform facts
- OpenAI schedules standard Custom GPT retirement for 2026-12-11. Migration uses the latest published GPT version; the migrated plugin starts private and does not automatically install itself or preserve the GPT's existing audience/sharing.
- GPT custom Actions do not migrate automatically. Life Patterns therefore needs a replacement integration (available app or custom MCP) before the plugin can replace the current Railway Action.
- Plugin users generally install the plugin. Installation can trigger app setup/authorization. Included apps/actions remain subject to provider/workspace permissions and action approvals.

Official references:
- https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt

## Product decision for this pilot
The plugin is the required long-term destination, but migration is not the immediate fix for the owner-observed approval-card or lost-review-handle bugs.

Keep the current GPT operational for the present owner test while applying the Action-approval/review-handoff hotfix. In parallel, build a private plugin parity prototype and rebuild the Railway integration through the supported plugin app/MCP path. Do not switch participant links until the plugin reproduces source recovery, independent-review handoff, file delivery, and the participant-facing permission explanation.

## Why
- Moving immediately would add an install/setup step while the current participant workflow is still being debugged.
- A plugin does not remove action approval requirements by itself.
- Migrating before the replacement integration exists would break the independent-review/final-submission path because the current custom Action does not transfer.
- A parallel private prototype preserves the working test surface and gives time to measure the real install/approval friction before public migration.

## Non-goal
This note does not authorize plugin publication, public sharing, or a production cutover. Those are separate owner-visible release actions after parity testing.
