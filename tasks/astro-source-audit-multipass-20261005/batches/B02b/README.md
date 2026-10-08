# Lilly planetary descriptions — reproducible source-reference packet

Read REPORT.md for the findings and CONVERSATION_HANDOFF.md to continue in a new chat.

PLANETS.json retains the seven planet catalogues. RULES.json gives 139 paragraph/category-level records with source page anchors. TABLE_AUDIT.json preserves conflicting numbered-degree assignments and the separately labelled later summary-table comparison. UNRESOLVED.json gives twenty retained questions. No original source book is included.

The helper and its unittest module use only the Python standard library. From this directory run:

```sh
python3 -m unittest discover -s . -p 'test_lilly_planet_reference.py' -v
```

build_reference_data.py deterministically regenerates PLANETS.json, RULES.json and TABLE_AUDIT.json in the repository layout; it contains the curated analyst transcription, not an independent extraction engine. The other metadata and reports are independently authored artifacts. Neither a successful regeneration nor tests validate the source's predictive claims.
