#!/usr/bin/env python3
"""Independent text and registry integrity for Henning's 27/28-mansion and
2;30 year-change commentary issues, without inventing Sanskrit readings.
"""
from pathlib import Path
from subprocess import run
import json

R=Path(__file__).resolve().parent
d=json.loads((R/"batches/T67/HENNING_NAME_AND_YEAR_CHANGE_SOURCE_CONFLICTS_V1.json")
             .read_text(encoding="utf-8"))
notes=d["notes"]
assert d["note_count"]==4
assert [x["id"] for x in notes]==[f"TIB-R{i:04d}" for i in range(592,596)]
assert all(x["source_id"]=="TIB-HENNING-2007" and x["human_validated"] is False
           and x["anchor"] for x in notes)
a=notes[0]["relevant_counts"]
assert a["mansions_in_syllable_source"]*a["letters_each"]==a["labeled_quadrants"]==112
assert a["zodiac_signs"]*a["quadrants_per_sign"]==a["zodiac_quadrants"]==108
assert a["labeled_quadrants"]!=a["zodiac_quadrants"]
b=notes[1]
assert len(b["source_visible_named_groups"])==24
assert len(set(b["source_visible_named_groups"]))==24
assert b["source_claimed_group_count"]==28
assert b["printed_group_count"]==24
assert d["validated_human_results"]==d["model_promotions"]==0
parent=run(["python3",str(R/"verify_t62_t66_planetary.py")],
           capture_output=True,text=True,check=True)
assert "49 new source notes" in parent.stdout
print("T67 SOURCE DISCREPANCIES PASS: 4 new notes TIB-R0592–0595,")
print("  112 vs 108 quadrants; 24 listed vs nominal28 quartets;")
print("  2;30 year change contested among different commentators;")
print("  T62–T66 1995 source-planet arithmetic and prior T01–T61 suites PASS.")
