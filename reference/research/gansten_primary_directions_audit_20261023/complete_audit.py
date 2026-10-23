"""Complete the existing audit without changing its technical specifications."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "baseline"


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Expected one occurrence: {old[:90]!r}")
    return text.replace(old, new, 1)


def load_table(name: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = (BASE / name).read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("index,"))
    reader = csv.DictReader(lines[start:])
    return list(reader.fieldnames or []), list(reader)


def save_table(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (ROOT / name).open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


report = (BASE / "GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md").read_text()
original_report = report
report = replace_once(
    report,
    "**Appendix correction revision, 23 October 2026:** the former cross-reference-error conclusion is withdrawn. Earlier Kindle observations and the reported print contents are now kept separate below. No fresh Kindle reinspection succeeded in this revision; the software appendix has not been read. The mathematical sections are preserved unchanged.",
    "**Completion revision, 23 October 2026:** fresh Kindle inspection confirms the tables as Appendix II at displayed p. 161, immediately after the formula appendix and before the Glossary. The software survey described for the published book was not found in this accessible Kindle edition. The earlier blanket Appendix III error conclusion remains withdrawn. This completes the available-edition reading audit, with the unavailable software survey and independent historical/software validation explicitly excluded. Sections 1–6, the numerical inputs and all D01–D62 records are preserved.",
)
report = replace_once(report, "| Copyright | Page iv in the earlier Kindle reading | Public bibliographic comparison added; no second physical edition inspected |", "| Copyright | Page iv, freshly reinspected | Confirms the 2009 publication and Solar Fire Deluxe v6.0 chart credit; no second physical edition inspected |")
report = replace_once(report, "| Bounds/year tables | Earlier Kindle reading recorded label II at p. 161; reported print contents label this III at p. 171 | No fresh Kindle heading check; individual numeric cells not audited, transcribed or independently verified |", "| Bounds/year tables | Fresh heading and table-structure inspection: Appendix II, displayed p. 161 | Individual numeric cells not transcribed or independently verified; reported print counterpart remains III at p. 171 |")
report = replace_once(report, "| Software appendix | Reported print Appendix II, p. 161; author and publisher confirm software reviews exist | Original appendix unread; Kindle inclusion, relocation, numbering and transitions remain unresolved |", "| Software appendix | No survey entry in Kindle front Contents/navigation; sequential 160→161→163 transition checked; whole-book searches completed | Survey not found in the accessible Kindle edition and not read; print survey text and publisher explanation remain unavailable |")
report = replace_once(report, "| Symbols/front-matter lists and index | Not systematically examined | No claim to have audited every front-matter or index entry |", "| Symbols/front Contents/index | Symbols x, Contents xi, and index 177–183 inspected in this completion pass | Navigation and terminology coverage checked; every index link was not individually followed, and index references do not establish new algorithms |")

start = report.index("## 0A. Appendix-edition correction and software evidence")
middle = report.index("### Useful software details from legitimate external documentation", start)
end = report.index("## 1. Technical foundations", middle)
external = report[middle:end]
external = external[:external.index("### Remaining action and correction history")]
external = external.replace("### Sources checked in this revision", "### External sources retained from the prior correction; E01–E02 reopened in the completion")
new_appendix = """## 0A. Appendix-edition reconciliation and software evidence

### Result and scope

Fresh inspection of the purchased Kindle edition resolves the earlier access gap. Its own front Contents at displayed xi, its navigation panel, and the actual heading at displayed 161 identify the terms-and-years material as **Appendix II**. Formula Appendix I ends at displayed 160; the next reader screen is that table appendix; advancing once more reaches the Glossary at displayed 163. No intervening software survey was displayed. The heading at 161 and both table structures were visually inspected; their numerical cells were not copied or independently audited.

The strongest supported conclusion is that **the software survey is not present in the accessible Kindle reading sequence or its listed contents**. This is an edition-specific observation, not proof of the publisher's intent, an explanation of the conversion history, or a claim about every print or digital edition. The original print contents reported earlier remain separate evidence. No physical print copy or primary print contents image was inspected in this completion pass.

| Material | Reviewer-reported print start | Fresh Kindle observation |
|---|---|---|
| Formula appendix | I, 147 | Appendix I; its final Fortune discussion displayed at 160 |
| Software survey | II, 161 | No survey entry or intervening section found |
| Terms and planetary years | III, 171 | Appendix II heading and tables at 161 |
| Glossary | 173 | Directly reached after the tables at 163 |
| Bibliography | 181 | Earlier complete reading at 171–175 retained |
| Index | Not independently verified for print | Navigation opens at 177; continuation inspected through final Z entries at 183; subsequent publisher advertising inspected separately |

The downstream ten-page shift is consistent with the absent survey, but remains a comparison with reported print anchors. Do not add ten to every Kindle reference or call the retained Appendix III references errors in the printed book. A fresh whole-book search for Appendix III returns three matches at displayed 28, 119 and 131. This adds the main-text reference at 119 to the two endnote references previously recorded; the newly located main-text label was visually confirmed on a screen whose footer begins at 118. Clicking that highlighted label did not navigate; no hyperlink destination is inferred, and the two endnote occurrences were not separately clicked.

### Whole-book search and positive control

| Reader search | Result actually returned | Meaning |
|---|---|---|
| software | Six results: displayed 43, 53, 57, 84 twice, and 148 | Main-text/formula references; no software-survey result |
| Janus | Zero results | Bounded negative search result, not proof by itself |
| Solar Fire | One result at displayed iv | Freshly opened: chart-production credit, not a software review |

The copyright page credits Solar Fire Deluxe v6.0 for charts unless otherwise stated. That identifies a chart-generation build mentioned by the source; it does not disclose direction settings, certify the correctness of its calculations, establish the reviewed program list, or reproduce the missing survey. The positive search matches, actual section boundaries and contents list together provide substantially better evidence than an empty query alone.

The symbols page at x and the index from 177 through 183 were also inspected as navigation/terminology checks. They do not supply the absent software survey or an additional executable rule. Every individual index target was not opened.

### What is complete and what remains separate

The technical audit of the material accessible in this purchased Kindle edition is complete. The original software survey remains **unread/unavailable in this edition**, rather than silently replaced by modern documentation. Its exact historical recommendations require a legitimate copy containing that section. The author and publisher pages E01–E02 were reopened in this pass and still describe software reviews; neither page explains the observed Kindle layout. Q25 now closes the Kindle-access/layout component while retaining the print-text/provenance component. Q26 remains the separate executable-software reproduction task.

"""
new_appendix += external.replace("The two synthetic cases and 135 phase checks remain the arithmetic baseline", "The two synthetic cases were rerun successfully in this completion pass; the 135 phase checks remain a previously reported baseline")
new_appendix += """### Correction history

The earlier blanket Appendix III error inference was withdrawn in the prior correction. This completion now verifies the earlier Kindle Appendix II observation with live contents, headings, sequential transitions and in-book searches. It does not reinstate a print-error allegation. The Appendix I §4a local subtraction-label observation remains unchanged. The complete previous audit is retained as the baseline; revisions affect coverage, edition reconciliation and their dependent metadata, not the mathematical specifications or historical disagreement records.

"""
report = report[:start] + new_appendix + report[end:]
report = replace_once(report, "The earlier conclusion about the two “Appendix III” references is withdrawn. [Ch. 2 note 3, p. 28; Ch. 9 note 14, p. 130.] That label agrees with the reported print contents. The prior Kindle label II/p. 161 remains an earlier observation requiring fresh checking; it does not establish an authorial or print-edition error. See §0A for the edition evidence and remaining gap.", "The earlier conclusion about the “Appendix III” references remains withdrawn; fresh search returns three instances, at displayed 28, 119 and 131. [Ch. 2 note 3, p. 28; Ch. 9 note 14, p. 130.] That label agrees with the reported print contents. Fresh Kindle inspection now confirms Appendix II at displayed p. 161, with no software survey found in its contents or sequential appendix transition. This establishes a Kindle/print-layout difference against the reported print anchors, not an authorial or print-edition error. See §0A.")
report = replace_once(report, "No existing repository or source audit was modified, and no empirical comparison was performed.", "The completed audit and companion indexes are saved in humandesign. Existing Lilly/Ptolemy source audits, production mappings and scoring code were not changed. No empirical comparison or external software-engine validation was performed.")
report += """
## 9. Completion verification

The existing original Python reproducibility kernel was executed again during this completion pass. It returned the three example-1 arcs 42.17434402835047°, 42.20081504892782° and 46.449117851278395°, and the two example-2 horizon arcs 10.653324067373134° and 5.5081832727086635°. Its ratio and altitude assertions passed. A further comparison against the displayed rounded values uses a 1e-8° tolerance. These are same-agent arithmetic checks on invented inputs; no production engine, historical chart, independent program or predictive result is certified.

Preservation checks retain sections 1–6 byte-for-byte as text, retain all 62 D-records, and retain every figure/method record and its identifier. Only the documented edition/coverage fields and the newly observed copyright-page software credit change. CSV exports normalize Library's tabular read representation into valid CSV and retain all parsed fields and rows; they are not claimed byte-identical to the original CSV files. A separate verification receipt records the checks and remaining limits.

**Next research boundary:** independently implement and compare the declared geometries, signs, quadrants and time keys; reconcile historical witnesses separately. Neither step is relabeled as a completed part of this reading audit.
"""
(ROOT / "GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md").write_text(report)

questions = (BASE / "GANSTEN_OPEN_QUESTIONS.md").read_text()
questions = questions.replace("No existing research repository was modified.", "This completion saves the audit in humandesign; existing historical-source audits and production mappings were not changed.")
qstart = questions.index("## Appendix correction status")
qend = questions.index("## P0", qstart)
questions = questions[:qstart] + """## Available-edition audit completed — 23 October 2026

Fresh Kindle inspection confirms the front Contents at xi, symbols at x, Appendix II tables at 161, direct formula/table/glossary transitions at 160→161→163, and index coverage at 177–183. Whole-book searches returned software: six main-text/formula hits; Janus: zero; Solar Fire: one copyright-page chart-software credit for Deluxe v6.0. No software survey was found in the accessible Kindle edition. The author/publisher descriptions still advertise software reviews, but no original print survey or publisher explanation was obtained.

The Appendix III search also returns three matches (28, 119, 131), rather than only the two previously listed endnotes; the main-text match was visually confirmed. Q25 is closed for Kindle layout/access and open only for the unavailable print-software text/provenance. The table-cell, original-witness and external-engine questions below are separate research tasks; they are not hidden unread chapters. The original numerical kernel was rerun successfully. No independent engine comparison, global direction-engine certification, or predictive validation occurred.

""" + questions[qend:]
questions = re.sub(r"^\| Q25 \|.*$", "| Q25 | CLOSED: Kindle layout/access; OPEN: original print survey and editorial provenance | Fresh Kindle Contents xi, tables 161, transitions 160→161→163; searches software=6, Janus=0, Solar Fire=1 at iv; index 177–183 | Obtain a legitimate edition containing the software survey and any publisher explanation; preserve its exact edition/build context | Kindle structural question closed; original survey not read and exact print contents not independently inspected |", questions, flags=re.M)
questions = questions.replace("Bounds/year tables: earlier Kindle label II p. 161; reported print III p. 171", "Bounds/year tables: freshly confirmed Kindle Appendix II p. 161; reported print III p. 171")
(ROOT / "GANSTEN_OPEN_QUESTIONS.md").write_text(questions)

method_name = "GANSTEN_METHOD_COMPARISON.csv"
method_fields, methods = load_table(method_name)
for row in methods:
    if row["method_id"] == "P03":
        row["book_reference"] = "Ch.2 pp.11–26; Ch.6 pp.73–78; freshly confirmed Kindle Appendix II p.161; reported print III p.171; audit section0A"
        row["inspection_status"] = "Main discussions read; appendix heading and table structure freshly checked; numeric cells not transcribed/audited; software survey not found in accessible Kindle edition"
    elif row["method_id"] == "B05":
        row["book_reference"] += "; copyright iv"
        row["inspection_status"] += "; copyright freshly inspected: charts credited to Solar Fire Deluxe v6.0 unless otherwise stated"
        row["unresolved_ambiguity"] += "; chart-generation credit does not establish direction settings or missing software-review contents"
    elif row["method_id"] in {"S01", "S02"}:
        row["book_reference"] = row["book_reference"].replace("Original software appendix unread", "Original software survey not found in accessible Kindle edition; unread")
save_table(method_name, method_fields, methods)

figure_name = "GANSTEN_FIGURE_INDEX.csv"
figure_fields, figures = load_table(figure_name)
for row in figures:
    if row["item_id"] in {"T05", "T06"}:
        row["chapter_or_section"] = "Freshly verified Kindle Appendix II; reviewer-reported print III"
        row["inspection_status"] = "Heading and table structure freshly inspected at Kindle161; individual cells not transcribed or independently audited"
        row["coverage_limit"] = ("No complete numerical bounds data set delivered" if row["item_id"] == "T05" else "Planetary ruler years are not an arc-to-age key table") + "; original historical variants require checking; reported print171; Kindle layout resolved with software survey unavailable in this edition (section0A/Q25)"
save_table(figure_name, figure_fields, figures)

protected_before = original_report[original_report.index("## 1. Technical foundations"):original_report.index("## 7. Disagreement")]
protected_after = report[report.index("## 1. Technical foundations"):report.index("## 7. Disagreement")]
assert protected_before == protected_after
disagreements_before = re.findall(r"^\| D\d\d \|.*$", original_report, re.M)
disagreements_after = re.findall(r"^\| D\d\d \|.*$", report, re.M)
assert disagreements_before == disagreements_after and len(disagreements_after) == 62
assert len(methods) == 42 and len(figures) == 51
delta = {}
for name, fields, rows, key, allowed in [(method_name, method_fields, methods, "method_id", {"P03", "B05", "S01", "S02"}), (figure_name, figure_fields, figures, "item_id", {"T05", "T06"})]:
    before_fields, before_rows = load_table(name)
    assert fields == before_fields
    assert [r[key] for r in rows] == [r[key] for r in before_rows]
    changed = []
    for before, after in zip(before_rows, rows):
        if before != after:
            assert before[key] in allowed
            changed.append({"id": before[key], "fields": [f for f in fields if before[f] != after[f]]})
    delta[name] = changed
    with (ROOT / name).open(newline="") as handle:
        parsed = list(csv.DictReader(handle))
    assert parsed == rows

kernel = re.findall(r"~~~python\n(.*?)\n~~~", report, re.S)[0]
run = subprocess.run([sys.executable, "-c", kernel], capture_output=True, text=True, check=True)
values = [list(map(float, line.split())) for line in run.stdout.strip().splitlines()]
expected = [[42.1743440284,42.2008150489,46.4491178513], [0,122.1813977125,20.1509688608,10.6533240674,10.8086850434], [5,123.3491372283,25.0334590712,5.5081832727,5.5885109454]]
assert all(abs(a-b)<1e-8 for row, target in zip(values, expected) for a,b in zip(row,target))
verification = {"scope":"Available-edition reading audit and targeted preservation; same-agent verification", "protected_sections_1_to_6_identical":True,"all_62_disagreement_records_identical":True,"method_records":len(methods),"figure_records":len(figures),"csv_round_trip_passed":True,"changed_csv_records":delta,"kernel_exit_code":run.returncode,"kernel_stdout":run.stdout,"displayed_values_tolerance_degrees":1e-8,"displayed_values_passed":True,"independent_external_engine_comparison":"NOT RUN","historical_primary_witness_comparison":"NOT RUN","previous_135_phase_checks":"Prior audit claim retained; not rerun in this completion","predictive_validation":"NOT RUN","files":{n:{"bytes":(ROOT/n).stat().st_size,"sha256":hashlib.sha256((ROOT/n).read_bytes()).hexdigest()} for n in ["GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md","GANSTEN_OPEN_QUESTIONS.md",method_name,figure_name]}}
(ROOT / "VERIFICATION.json").write_text(json.dumps(verification,indent=2)+"\n")
print(json.dumps({k:v for k,v in verification.items() if k not in {"files","changed_csv_records","kernel_stdout"}},indent=2))
