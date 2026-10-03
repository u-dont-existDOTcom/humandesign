# Plugin migration assessment — 2026-10-02

## Owner question
Should the Life Patterns participant surface move from a Custom GPT to a plugin now, and would a plugin remove the current Action/handoff UX problems?

## Current platform facts
- OpenAI schedules standard Custom GPT retirement for 2026-12-11. Migration uses the latest published GPT version; the migrated plugin starts private and does not automatically install itself or preserve the GPT's existing audience/sharing.
- GPT custom Actions do not migrate automatically. Life Patterns therefore needs a replacement integration (available app or custom MCP) before the plugin can replace the current Railway Action.
- Plugin users generally install the plugin. Installation can trigger app setup/authorization. Included apps/actions remain subject to provider/workspace permissions and action approvals.
- ChatGPT Scheduled tasks explicitly do **not** support Custom GPTs, so the current GPT cannot reliably wake itself later or send a completion notification when Railway finishes.
- Plugins can participate in ChatGPT automation when their connected apps expose supported task/event capabilities, but event-triggered tasks currently depend on Work, eligible plans/workspaces and supported app events. That makes notification a useful plugin enhancement, not a universal participant requirement.

Official references:
- https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt

## Product decision for this pilot
The plugin is the required long-term destination, but migration is not the immediate fix for the owner-observed approval-card or lost-review-handle bugs.

Keep the current GPT operational for the present owner test while applying the Action-approval/review-handoff hotfix. In parallel, build a private plugin parity prototype and rebuild the Railway integration through the supported plugin app/MCP path. Do not switch participant links until the plugin reproduces source recovery, independent-review handoff, file delivery, and the participant-facing permission explanation.

## Why
- Moving immediately would add an install/setup step while the current participant workflow is still being debugged.
- A plugin does not remove action approval requirements by itself.
- Migrating before the replacement integration exists would break the independent-review/final-submission path because the current custom Action does not transfer.
- A parallel private prototype preserves the working test surface and gives time to measure the real install/approval friction before public migration.
- For the present GPT, the best low-friction fallback is an explicit check-back interval plus automatic status checking on any ordinary continuation message. For the plugin prototype, test an optional review-ready event/notification path and an interactive status surface so eligible users do not have to poll manually. Keep the ordinary check-back flow as the cross-plan fallback.

## Non-goal
This note does not authorize plugin publication, public sharing, or a production cutover. Those are separate owner-visible release actions after parity testing.


## Review-endgame UX target — 2026-10-03

The current GPT fallback is now bounded: one slow independent pass may return at most one clarification; after the participant answers or skips it, a finalization-only delta pass runs from the already reviewed state and cannot open another behavioral clarification. This removes indefinite clarification loops while retaining independent admission of the clarification answer.

For the plugin prototype, improve further rather than reproducing chat polling:
- render a persistent **Review in progress** status surface that can refresh from Railway without the participant repeatedly asking;
- show the next expected check time / elapsed state directly in that surface;
- when supported by the user's ChatGPT plan/app-event path, offer an optional review-ready notification;
- keep ordinary return-to-chat checking as the universal fallback, so installation or notification permission is not required for completion.

Do not make proactive notification a scientific or completion prerequisite. It is a UX enhancement layered over the same durable review state.
