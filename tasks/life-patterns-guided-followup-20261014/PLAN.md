# Guided context follow-ups — October 14

Goal: On opening an owner-private offline V3 pilot, automatically prompt the eight requested context clarifications one at a time, without choosing question IDs. Generic pilot auto-starts immediately after importing an existing 25-question JSON export. Previously recorded answers and unusual-behavior records remain unchanged; no data is sent to a server.

Target routes: TF1-G01, TF1-G02, TF1-G16, TF1-G23, TF1-M05, TF1-G20, TF1-M01, TF1-M03.

Controls: Next, Previous, Skip for now, no stable default, resume unfinished, explicit export. Already completed or skipped items do not get reasked automatically. Show existing answers as context.

Delivery: Reversible source and HTML update; separate private prefilled owner HTML so no manual import needed. No live GPT or study submission changes.

Acceptance: 25 answers restored, eight automatic prompts, answer/skip/resume/export preserve source, file-only browser with no external requests and mobile-accessible interface; only synthetic test fixtures committed.
