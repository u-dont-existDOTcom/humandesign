# Independent Behavioral Calibration — Start Here

You will use one private HTML file. It works entirely on your computer and does not use AI or send the stories anywhere.

## What you are deciding

Each screen shows:

1. **one piece of the narrator's story**, and
2. **one specific behavior question** about that story.

Answer only that question. **The story does not have to match the question.** A No answer is normal and useful.

- **Yes — clearly shown**: the exact quote clearly shows the behavior asked about.
- **No — does not fit**: the required situation is absent. Do not reinterpret the story to make it fit.
- **Can't tell**: the behavior might fit, but the exact quote is not clear enough to decide reliably.

Here, **narrator** means the person whose story you are coding.

Example: if the question asks whether the narrator **sought or used someone else's help**, a story where the narrator **offered help to somebody else** is No. Direction matters.

## If you answer Yes

Choose the behavior that the exact quote shows.

Source citation is bookkeeping, not a second behavioral judgment:

- if the unit contains **one exact quote**, the interface saves that quote automatically as the source for your Yes answer; there is no extra citation checkbox to answer;
- if there are **several exact quotes**, select only the quote(s) you actually relied on for the behavior you chose;
- an optional collapsed control lets you mark a quote that genuinely contains an exception, limitation, or conflicting detail. Most units need nothing there.

You do **not** need to interpret internal source identifiers such as `EP-002-SEG-01`. Those are stable machine provenance keys used only in the exported data. Human-facing source choices show `Exact quote`, `Exact quote 1`, etc. plus the actual quote text.

You do not need to understand internal R16-a / R16-b style codes either. They are identifiers for the exported data.

Open **Formal definition and coding rules** only when the plain question is not enough to decide.

Optional context, uncertainty, and influence fields are secondary. For influence, record it only when the narrator explicitly says something affected **the behavior you selected on this screen**. It is not a general question about who influenced whom in the story.

## Repeated-pattern screens

A statement such as “I always X,” “I usually X,” or “I sometimes X” is evidence that the narrator reports X as recurring. Do not demand a confirming anecdote or invent a count.

Keep exceptions separate. “Always” by itself does not prove the narrator explicitly denied every exception.

## Independence requirement

This first pass must be completed before you see any automated answers, automated consensus, target-model results/mappings, birth/chart information, or expected answers. Do not use ChatGPT or another AI to make the coding judgments.

If you have already seen disqualifying information, say so honestly in the attestation.

## Using the file

Open:

`Life-Patterns-Human-Calibration-V2-PLAIN-READABLE-SOURCES.html`

Expected SHA-256:

`f5889d34d6160a44fc902263fd68a7b3d13404418127967400221334ae8379f3`

The page should say **Bundle verified**. If it does not, stop and report the technical problem.

There are 66 selected units: 44 story episodes and 22 repeated-pattern units. Use **Download progress** if you need to stop and continue later.

When all 66 are complete, finish the independence attestation and prepare the final exports. Return these three files unchanged:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Do not inspect automated results until the coordinator confirms your first pass has been frozen.
