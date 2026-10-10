"""Package the published B02i core and its declared companions.

Adapted from B02h/build_delivery_packet.py. Build only after the root producer
has created MANIFEST.json and SOURCE_PUBLICATION_RECEIPT.json. This program
builds local deliverables; it does not publish, distribute, or verify an owner
copy. Actual archive extraction, standalone testing and delivery have separate
receipts. The full report is copied byte-for-byte from the manifested core.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent
BATCH = "B02i"
TASK = PurePosixPath("tasks/astro-source-audit-multipass-20261005")
BATCH_PATH = TASK / "batches" / BATCH
LILLY_INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PTOLEMY_INDEX = TASK / "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
STATE = PurePosixPath("state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02i.md")
COMPANION = TASK / "batches/B02f/lilly_presence_ship_reference.py"
REPORT = "Astrology-Lilly-Property-Treasure-20261010.md"
ZIP = "Astrology-Lilly-Property-Treasure-Records-20261010.zip"
HANDOFF = "Astrology-Lilly-Handoff-B02i-20261010.md"
ORIGINAL_PDF = "Lilly-1647-Christian-Astrology-I-III.pdf"
STANDALONE_COMMAND = "python3 -B -m unittest discover -s B02i -p 'test_*.py' -v"
ZIP_TIMESTAMP = (2026, 10, 10, 0, 0, 0)

VERIFY = '''"""Verify the files listed in this packet's content manifest."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "PACKET_CONTENTS.json").read_text())
seen = set()
for row in manifest["files"]:
    relative = PurePosixPath(row["path"])
    if relative.is_absolute() or ".." in relative.parts or str(relative) in seen:
        raise ValueError("Invalid or duplicate packet path: " + str(relative))
    seen.add(str(relative))
    path = root.joinpath(*relative.parts)
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    if len(data) != row["bytes"]:
        raise ValueError("Byte count differs: " + str(relative))
    if hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise ValueError("SHA256 differs: " + str(relative))
print(json.dumps({"status": "PASS", "verified_files": len(seen),
                  "source_revision": manifest["source_revision"],
                  "verification_scope": "Listed packet bytes only; not predictive accuracy or owner delivery"}))
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or ".." in path.parts or "\\" in value:
        raise ValueError(f"Expected a repository-relative POSIX path: {value}")
    if path.name == ORIGINAL_PDF:
        raise ValueError("The retained original PDF is outside the delivery packet")
    return path


def verified_manifest_bytes(repo, rows):
    """Read each declared input once and retain the exact verified bytes."""
    result = {}
    for row in rows:
        relative = relative_path(row["path"])
        key = str(relative)
        if key in result:
            raise ValueError(f"Duplicate core manifest path: {key}")
        path = repo.joinpath(*relative.parts)
        data = path.read_bytes()
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            raise ValueError(f"Manifest mismatch: {key}")
        result[key] = data
    return result


def core_json(core, path):
    key = str(path)
    if key not in core:
        raise ValueError(f"Required published-core input is absent from MANIFEST.json: {key}")
    return json.loads(core[key])


def checked_count(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid nonnegative count for {label}")
    return value


def load_counts(core):
    """Use final manifested inputs rather than freezing today's provisional totals."""
    rules = core_json(core, BATCH_PATH / "RULES.json")
    unresolved = core_json(core, BATCH_PATH / "UNRESOLVED.json")
    tests = core_json(core, BATCH_PATH / "TEST_RUN_SUMMARY.json")
    chart_table = core_json(core, BATCH_PATH / "WORKED_NUMERIC_TABLES.json")
    lilly = core_json(core, LILLY_INDEX)
    ptolemy = core_json(core, PTOLEMY_INDEX)
    reading = core_json(core, BATCH_PATH / "READING_RECEIPT.json")

    record_count = len(rules["rules"])
    if checked_count(rules["records_count"], "source records") != record_count:
        raise ValueError("RULES.json record count differs from its inventory")
    general = checked_count(rules["general_records_count"], "general records")
    narrative = checked_count(rules["worked_example_records_count"], "narrative records")
    if general + narrative != record_count:
        raise ValueError("General and worked narrative counts do not sum to the inventory")
    identifiers = [row["id"] for row in rules["rules"]]
    if len(set(identifiers)) != record_count or not identifiers:
        raise ValueError("The source inventory must contain unique, nonempty IDs")
    numbers = []
    for identifier in identifiers:
        match = re.search(r"\.R(\d+)$", identifier)
        if not match:
            raise ValueError(f"Source record lacks an R-number: {identifier}")
        numbers.append(int(match.group(1)))
    if len(set(numbers)) != record_count:
        raise ValueError("Source R-numbers are not unique")
    numbers.sort()
    if numbers == list(range(numbers[0], numbers[-1] + 1)):
        record_range = f"R{numbers[0]}–R{numbers[-1]}"
    else:
        record_range = f"R{numbers[0]} through R{numbers[-1]}; see RULES.json for the admitted IDs"

    open_issues = len(unresolved["issues"])
    resolved = len(unresolved["resolved_readings"])
    if unresolved["issues_count"] != open_issues or unresolved["resolved_readings_count"] != resolved:
        raise ValueError("UNRESOLVED.json counts differ from its separate issue lists")
    new_tests = checked_count(tests["new_distinct_tests"], "new tests")
    retained_tests = checked_count(tests["retained_distinct_tests"], "retained tests")
    total_tests = checked_count(tests["total_distinct_tests"], "all focused tests")
    if new_tests + retained_tests != total_tests:
        raise ValueError("Focused test subtotals do not add to the declared total")
    if tests["status"] != "PASS" or any(run["exit_code"] != 0 for run in tests["runs"]):
        raise ValueError("The published focused test summary does not report a passing run")
    if tests["subtests_or_reruns_counted_as_additional"] is not False:
        raise ValueError("Focused counts must not add subtests or reruns")

    chart_count = len(chart_table["charts"])
    if chart_table["actual_chart_count"] != chart_count:
        raise ValueError("Chart count differs from the actual figure list")
    coordinate_entries = 0
    for chart in chart_table["charts"]:
        entries = len(chart["house_cusps"]) + len(chart["bodies_and_points"])
        if chart["entry_count"] != entries:
            raise ValueError("A chart's coordinate count differs from its entries")
        coordinate_entries += entries
    lilly_count = checked_count(lilly["records_count"], "cumulative Lilly records")
    ptolemy_count = checked_count(ptolemy["source_records"], "retained Ptolemy records")
    source_hash = rules["source_sha256"]
    if lilly["source_sha256"] != source_hash or reading["source_sha256"] != source_hash:
        raise ValueError("Source hash differs across the admitted batch inputs")
    return {
        "source_records": record_count, "record_range": record_range,
        "general_records": general, "narrative_records": narrative,
        "lilly_records": lilly_count, "ptolemy_records": ptolemy_count,
        "combined_records": lilly_count + ptolemy_count,
        "unresolved": open_issues, "source_resolved": resolved,
        "new_tests": new_tests, "retained_tests": retained_tests, "focused_tests": total_tests,
        "charts": chart_count, "coordinate_entries": coordinate_entries,
        "source_id": rules["source_id"], "source_sha256": source_hash,
        "source_identity_receipt": reading["identity_verification"],
        "count_sources": ["B02i/RULES.json", "B02i/UNRESOLVED.json", "B02i/TEST_RUN_SUMMARY.json",
                          "B02i/WORKED_NUMERIC_TABLES.json", "context/" + LILLY_INDEX.name,
                          "context/" + PTOLEMY_INDEX.name],
    }


def make_handoff(commit, counts):
    return f'''# Continue Lilly source audit after the fourth-house block

The fourth-house source span is complete: **PDF236 / printed202**, beginning with its heading and full preamble, through **the final XXXVIII paragraph above the horizontal divider on PDF256 / printed222**. Chapters XXXII–XXXVIII and all intervening unnumbered material are included. The source-publication receipt identifies immutable source revision `{commit}` for this packet.

## Exact next reading

Resume **PDF256 / printed222 below the horizontal divider**, at **“Of the fifth House, and its Questions.”** Include that heading, then **Chapter XXXIX, “If one shall have Children, yea or no?”**, and its opening question-context paragraph. Do not restart at the already completed fourth-house paragraph or skip the fifth-house introduction.

## What this batch preserves

- {counts['source_records']:,} new source records, {counts['record_range']}: {counts['general_records']:,} general, methodological or illustrative records and {counts['narrative_records']:,} records in the worked purchase narrative.
- {counts['lilly_records']:,} cumulative Lilly records plus {counts['ptolemy_records']:,} retained Ptolemy records: {counts['combined_records']:,} source records in the two inventories.
- {counts['unresolved']:,} unresolved textual, implementation or evidence limits, with {counts['source_resolved']:,} source-resolved readings tracked separately. These are not counts of demonstrated author errors.
- {counts['charts']:,} actual chart with {counts['coordinate_entries']:,} cusp, planet, node and Fortune entries. Printed omissions and inferred sign labels remain explicit.
- The source-stage focused summary reports {counts['focused_tests']:,} distinct passing tests: {counts['new_tests']:,} new and {counts['retained_tests']:,} retained. The included standalone new suite has {counts['new_tests']:,}; retained projects are not duplicated wholesale.

These are inventory and engineering counts. A source record may hold several branches, a qualification, an illustration or a retrospective report; the inventory is not a count of independent predictions or observed cases. Counts above are loaded from the final manifested records, issue ledger, numeric table, test summary and index snapshots.

## Use the delivered files

Read `{REPORT}` for the complete report. It is byte-identical to the published core's `B02i/AUDIT_REPORT.md`. Extract `{ZIP}`, read `B02i/README.md`, and run these commands from the extracted packet root:

```bash
python3 verify_packet.py
{STANDALONE_COMMAND}
```

The supported standalone suite uses the Python standard library. Its unchanged computational companion, `B02f/lilly_presence_ship_reference.py`, is included. To reproduce the static checks, run `python3 -B B02i/lilly_fourth_house_arithmetic.py`; this writes `B02i/ARITHMETIC_CHECKS.json`. Repository-production generators require the full repository and are not the packet's supported reading interface.

The packet includes every core-manifest file, original reader notes and candidates, admitted records, issue and case ledgers, numeric inputs, code, source-stage test receipts, included review records and retained comparison excerpts. Both index snapshots and the dated continuation state are under `context/`. `PACKET_CONTENTS.json` lists the included files with byte counts and SHA-256 hashes; it excludes itself from its recursive hash list. The packet does not contain the whole cumulative corpus or the original PDF.

## Preserve context, outcomes and unknowns

Keep the goods owner and question type explicit. The mislaid-object procedure begins with a restricted indoor/non-stolen context, and its named sign slots can share the same physical body. Purchase, land assessment and rental assign different meanings to the same houses. Preserve their conditions, alternatives and undefined ties; do not turn the literal rain-sign list or ordinal treasure-depth comparison into a different numerical model.

The father's-estate discussion distinguishes present requests, future provision and the father's will. Treasure presence, material identity, acquisition, location and depth are different questions. Specifying a mineral before the question is prior information. Narrative memories of success, theological explanations and illustrative examples retain their stated evidential limits.

The purchase narrative begins with an already formed intention and a known money-recall restriction. Negotiation, the later rival, assistance, the loan, agreement, and payment/sealing are dependent episodes within the same enquiry. Agreement and completion have different dates. Financial disadvantage and satisfaction are different outcomes. Bodily-mark reports are retrospective; durability and lifetime lease expectations lack confirming endpoints in the admitted pages.

Keep the printed Fortune value separate from the retained-profile calculation and preserve the unresolved discrepancy. Missing cusp minutes remain null. Mercury's geometric sector and possible cusp influence are separate; the Sun's local seller assignment and later lordship wording are retained without changing the chart. Static separations do not supply historical contact dates, an ephemeris, a global orb rule or a universal degree-to-time conversion.

## Source recovery and continuation

Retained original: `{ORIGINAL_PDF}`; source `{counts['source_id']}`; SHA-256 `{counts['source_sha256']}`. The B02i source identity receipt states: {counts['source_identity_receipt']} Reuse that retained original. The packager does not rehash or include it and does not substitute a modern edition.

Canonical index: `tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json`. Dated checkpoint: `state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02i.md`. Batch: `tasks/astro-source-audit-multipass-20261005/batches/B02i/`.

Load current owner, project and source-provenance instructions before continuing. Earlier batches, earlier dated states, participant inputs, fitted models and prediction freezes stay unchanged. Do not replay historical restricted payloads at `state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md`, task `CURRENT_PASS.json` or `PASS_PLAN.json`. This saved source-sized boundary does not close the wider multi-author audit.

## Publication, packet checks and delivery are separate stages

`B02i/SOURCE_PUBLICATION_RECEIPT.json` identifies the recorded remote source revision. Building this ZIP creates local deliverables; it is not a distribution-publication receipt, an extracted-packet test receipt or proof of an owner copy in Downloads. Those later actions need their actual process/readback receipts. The requested owner destination is the OS-designated Downloads folder.

No background continuation, runtime-model promotion, independent event corroboration or empirical predictive accuracy is established by this packet.
'''


def packet_destination(relative):
    """Preserve the batch subtree and the proven context/companion layout."""
    if relative.is_relative_to(BATCH_PATH):
        return PurePosixPath(BATCH) / relative.relative_to(BATCH_PATH)
    if relative == COMPANION:
        return PurePosixPath("B02f/lilly_presence_ship_reference.py")
    return PurePosixPath("context") / relative.name


def main():
    required_stage_files = [ROOT / "MANIFEST.json", ROOT / "SOURCE_PUBLICATION_RECEIPT.json"]
    missing = [path.name for path in required_stage_files if not path.is_file()]
    if missing:
        raise SystemExit("Published-source stage is incomplete; no packet built. Required: " + ", ".join(missing))
    manifest_bytes = (ROOT / "MANIFEST.json").read_bytes()
    publication_bytes = (ROOT / "SOURCE_PUBLICATION_RECEIPT.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    publication = json.loads(publication_bytes)
    commit = publication.get("remote_source_commit")
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-fA-F]{40}", commit) is None:
        raise ValueError("SOURCE_PUBLICATION_RECEIPT requires remote_source_commit as a full commit SHA")
    if manifest.get("batch") != BATCH or manifest.get("stage") != "IMMUTABLE_VERIFIED_SOURCE_CORE":
        raise ValueError("The required B02i immutable source-core manifest is not present")
    repo = ROOT.parents[3]
    core = verified_manifest_bytes(repo, manifest["files"])
    for path in (LILLY_INDEX, PTOLEMY_INDEX, STATE, BATCH_PATH / "AUDIT_REPORT.md", BATCH_PATH / "README.md"):
        if str(path) not in core:
            raise ValueError(f"Required core or continuation companion is not manifested: {path}")
    counts = load_counts(core)
    report_bytes = core[str(BATCH_PATH / "AUDIT_REPORT.md")]
    if manifest["report_sha256"] != digest(report_bytes):
        raise ValueError("Manifest report SHA does not match the exact core report")
    if manifest["source_record_count"] != counts["source_records"] or manifest["source_sha256"] != counts["source_sha256"]:
        raise ValueError("Manifest source identity/count differs from admitted records")
    companions = {row["path"]: row for row in manifest["unchanged_computational_companions"]}
    if str(COMPANION) not in companions:
        raise ValueError("The retained B02f computational companion must be declared and hashed")
    companion_bytes = verified_manifest_bytes(repo, [companions[str(COMPANION)]])[str(COMPANION)]

    # No output is created before the published core and required inputs pass.
    out = ROOT / "deliverables"
    out.mkdir(exist_ok=True)
    (out / REPORT).write_bytes(report_bytes)
    handoff_bytes = make_handoff(commit, counts).encode("utf-8")
    (out / HANDOFF).write_bytes(handoff_bytes)
    with tempfile.TemporaryDirectory() as folder:
        packet = Path(folder)
        destinations = {}
        def put(relative, data, origin):
            relative = relative_path(str(relative))
            key = str(relative)
            if key in destinations:
                if destinations[key]["sha256"] == digest(data):
                    return
                raise ValueError(f"Different inputs collide at packet path: {key}")
            destination = packet.joinpath(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            destinations[key] = {"path": key, "bytes": len(data), "sha256": digest(data), "source": origin}

        for path, data in sorted(core.items()):
            put(packet_destination(PurePosixPath(path)), data, path)
        put(PurePosixPath(BATCH) / "MANIFEST.json", manifest_bytes, "source-stage manifest")
        put(PurePosixPath(BATCH) / "SOURCE_PUBLICATION_RECEIPT.json", publication_bytes, "recorded source-publication receipt")
        put(PurePosixPath("B02f/lilly_presence_ship_reference.py"), companion_bytes, str(COMPANION))
        put(PurePosixPath(HANDOFF), handoff_bytes, "generated owner handoff")
        put(PurePosixPath("verify_packet.py"), VERIFY.encode("utf-8"), "packet byte verifier")
        read_me = f'''# Lilly fourth-house packet

Start with `B02i/AUDIT_REPORT.md` and `B02i/README.md`.

From this packet root run:

```bash
python3 verify_packet.py
{STANDALONE_COMMAND}
```

The supported standalone new suite has {counts['new_tests']:,} tests and uses the Python standard library. The reported repository-wide focused subset has {counts['focused_tests']:,} distinct tests, including {counts['retained_tests']:,} retained tests whose projects are not duplicated wholesale here. Source-stage test receipts are included; actual extracted-packet execution has its own later receipt.

Both source-index snapshots and the dated continuation state are under `context/`. The required unchanged helper is under `B02f/`. The complete new batch and declared comparison companions are included; the whole cumulative corpus and retained original PDF are not. Evidence ledgers retain source-repository paths as provenance.

The next reading begins with the fifth-house heading and Chapter XXXIX below the divider on PDF256 / printed222, including the opening paragraph. Source completion, remote-source publication, archive verification and owner delivery are distinct stages. These materials do not establish predictive accuracy.
'''
        put(PurePosixPath("READ_ME.md"), read_me.encode("utf-8"), "packet reading instructions")
        contents = {
            "source_revision": commit,
            "source_manifest_sha256": digest(manifest_bytes),
            "source_publication_receipt_sha256": digest(publication_bytes),
            "stage": "LOCAL_PACKET_FROM_RECORDED_PUBLISHED_SOURCE",
            "counts": counts,
            "files": [destinations[key] for key in sorted(destinations)],
            "self_excluded": "PACKET_CONTENTS.json is excluded from its own recursive hash list.",
            "actual_extracted_archive_execution_recorded_here": False,
            "owner_delivery_verified": False,
        }
        (packet / "PACKET_CONTENTS.json").write_text(json.dumps(contents, indent=2, ensure_ascii=False) + "\n")
        with zipfile.ZipFile(out / ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(packet.rglob("*")):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(packet).as_posix(), date_time=ZIP_TIMESTAMP)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.create_system = 3
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    if (out / REPORT).read_bytes() != report_bytes:
        raise ValueError("Delivered report differs from the manifested core report")
    rows = [{"filename": name, "path": "deliverables/" + name,
             "bytes": (out / name).stat().st_size, "sha256": sha(out / name)}
            for name in (REPORT, ZIP, HANDOFF)]
    deliverables_manifest = {
        "source_revision": commit,
        "source_manifest_sha256": digest(manifest_bytes),
        "source_publication_receipt_sha256": digest(publication_bytes),
        "stage": "LOCAL_DELIVERABLES_BUILT_FROM_RECORDED_PUBLISHED_SOURCE",
        "files": rows, "counts": counts,
        "owner_destination": "OS-designated Downloads",
        "report_matches_core": True,
        "report_copy_method": "exact manifested AUDIT_REPORT.md bytes; no re-rendering or normalization",
        "actual_archive_reextraction_verified": False,
        "standalone_packet_test_run_recorded_here": False,
        "distribution_published_by_this_program": False,
        "owner_delivery_verified": False,
        "next_stage": "Root records actual archive verification, distribution publication and owner-copy readback separately",
    }
    (ROOT / "DELIVERABLES_MANIFEST.json").write_text(json.dumps(deliverables_manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"source_revision": commit, "stage": deliverables_manifest["stage"],
                      "files": rows, "report_matches_core": True, "owner_delivery_verified": False}))


if __name__ == "__main__":
    main()
