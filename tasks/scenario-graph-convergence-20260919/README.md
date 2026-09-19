# Scenario-first survey — converged graph review

Start with **REPORT.md** for the judgment or open **GRAPH-EXPLORER.html** for the offline graph. The HTML is read-only: it makes no network requests and captures no answers. Search or select a topic to inspect the actual questions. On a phone, diagrams scroll within their containers; the text panels remain readable.

The final full review required zero further substantive changes. This is an explicitly bounded design judgment, not proof of empirical validity, runtime performance or full AstroHD recovery. The pilot remains paused.

## Main artifacts

- INTERVIEW-PROTOCOL.md: conversational and privacy rules.
- REVIEWED-QUESTIONS.md and interviewer-bank-v6.json: all 79 available entries, not a fixed survey length.
- ROUTING-GRAPH.json and SCENARIO-GRAPH.md: source graph and Mermaid views. Edges distinguish context, advisory links and possible information; none awards evidence credit.
- EVIDENCE-GUIDE-v6.json: 73 narrow interpretation examples.
- DIALOGUE-CHECKS.md: 16 graph-focused authored examples; source-dialogues-v5.json preserves the 32 prior examples.
- CHANGES.json and FINDINGS.json: initial repairs, including repairs to the new audit model.
- FINAL-SWEEP.json and VERIFICATION.json: exact review scope, zero-change final pass and test limitations.

## Reproduction

`python3 test_graph.py` runs the explicit-state tests without network or inference. It does not interpret participant language. `python3 build_views.py` regenerates the HTML, SVG and Mermaid views from the JSON and requires Graphviz's `dot`. `python3 build_dialogue_checks.py` reproduces the authored examples.

`python3 rebuild_from_source.py` reproduces the data artifacts from the frozen files under source/. Run generators in a disposable copy when preserving an audited version. VIEW-CHECKS.json describes the separate browser check. No diagram is a deployed controller.

Personal records are held by the existing owner-private capture arrangement outside Git and Railway; this packet contains no actual participant answers. Design scope does not authorize app deployment or waking inference.
