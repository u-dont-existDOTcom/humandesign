#!/usr/bin/env python3
"""Create an offline derived-source packet from one exact committed revision.

Raw books/transcripts and private reviewer runtime logs are never included.
The optional acceptance receipt describes its own tested head, not the ZIP itself.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = "reference/research/numerology_v2_20261004/"
SELECTION = [
    "reference/research/NUMEROLOGY_BOOK_AUDIT_V2_20261004.md",
    "reference/research/numerology_method_registry_v2_20261004.json",
    "reference/research/NUMEROLOGY_METHODOLOGY_AUDIT_V1_20261003.md",
    "reference/research/numerology_method_registry_v1_20261003.json",
    BASE,
    "docs/24_numerology_methodology_policy.md",
    "notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md",
    "notes/JOEL_NAME_GOAL_COMPARISON_CORRECTION_20261003.md",
    "notes/NUMEROLOGY_SYSTEM_COMPARISON_20261003.md",
    "notes/NUMEROLOGY_NAME_LAYER_CORRECTION_20261003.md",
    "experiments/astrohd/chaldean_life_event_retrodiagnostic_20261003.json",
    "scripts/numerology_book_reference.py",
    "scripts/numerology_book_audit_verify.py",
    "scripts/numerology_book_audit_bundle.py",
    "tests/test_numerology_book_reference.py",
    "tests/test_numerology_book_audit_gate.py",
]


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--acceptance-receipt", type=Path)
    args = parser.parse_args()
    revision = git("rev-parse", "--verify", args.revision + "^{commit}").decode().strip()
    files = git("ls-tree", "-r", "--name-only", revision, "--", *SELECTION).decode().splitlines()
    data = {name: git("show", revision + ":" + name) for name in files}
    if not data or any(Path(name).suffix not in {".md", ".json", ".py"} for name in data):
        raise RuntimeError("Unexpected/missing packet files; only whitelisted derived text is permitted")
    frozen = json.loads(data[BASE + "freeze_manifest.json"])
    for name, expected in {**frozen["files"], **frozen["immutable_baseline_files"]}.items():
        if name not in data or blob(data[name]) != expected:
            raise RuntimeError("Frozen companion missing or changed: " + name)
    if args.acceptance_receipt:
        receipt = json.loads(args.acceptance_receipt.read_text())
        if receipt.get("status") != "PASS" or receipt.get("mode") != "committed_artifact_acceptance" or receipt.get("head") != revision:
            raise RuntimeError("Acceptance receipt does not certify the exact requested committed revision")
        data["verification/COMMITTED_ARTIFACT_ACCEPTANCE.json"] = args.acceptance_receipt.read_bytes()
    readme = f"""# Start here — Four-book numerology methodology audit

Source revision: {revision}
Repository: u-dont-existDOTcom/humandesign
Branch: research/six-rule-life-timing-20261001

Open **NUMEROLOGY_AUDIT_READER.html** for the integrated offline reader, or **SUMMARY.html** for the short conclusions. No internet, login, scripts, fonts or raw book downloads are needed to read these derived reports.

The canonical main audit is reference/research/NUMEROLOGY_BOOK_AUDIT_V2_20261004.md. The registry is reference/research/numerology_method_registry_v2_20261004.json. Full per-author specifications, the mandatory reconciliation, ambiguities, exact source freeze, arithmetic fixtures, independent closeout review and post-freeze empirical design are under reference/research/numerology_v2_20261004/.

The inherited V1 audit and registry are included because Cheiro V2 and the comparison depend on them. The policy and bounded historical annotations are included. Raw copyrighted books, complete transcripts, credentials, private reviewer logs and new participant data are not included. Original book hashes and page locators identify the supplied sources; this packet is an audit, not a substitute facsimile.

The source arithmetic and control regression tests run with Python 3.10 or later and the standard library:

```sh
python3 -m unittest discover -s tests -p 'test_numerology_book_*.py' -v
```

Run that command in the extracted packet directory. The full audit acceptance command additionally needs the actual Git checkout, task lock and history; an extracted ZIP is not a Git repository. Its exact-head acceptance result is included under verification/ when supplied at build time.

The source freeze does not make unresolved author instructions single-valued. SOURCE_RECONCILIATION.md controls its enumerated corrections. No author mixing, outcome-selected branch, retrospective rescue, empirical superiority or causal name-change claim is authorized. The proposed study has not launched; its separate operational prerequisites are listed explicitly.

PACKET_MANIFEST.json gives SHA-256 hashes of the payload files. It does not include itself. The separately recorded ZIP hash verifies the outer delivery object.
"""
    data["README_START_HERE.md"] = readme.encode()
    try:
        from markdown_it import MarkdownIt
        renderer = MarkdownIt("commonmark", {"html": False}).enable("table")
        render = renderer.render
    except ImportError:
        render = lambda text: "<pre>" + html.escape(text) + "</pre>"
    sections = [
        ("summary", "Conclusions and remaining limits", BASE + "AUDIT_COMPLETION_REPORT.md"),
        ("audit", "Complete audit and cross-system matrix", SELECTION[0]),
        ("reconciliation", "Mandatory source reconciliation", BASE + "SOURCE_RECONCILIATION.md"),
        ("cheiro", "Cheiro — V2 delta", BASE + "CHEIRO_CHALDEAN_V2.md"),
        ("campbell", "Campbell — Your Days Are Numbered", BASE + "CAMPBELL_YOUR_DAYS_V1.md"),
        ("jordan", "Jordan — The Romance in Your Name", BASE + "JORDAN_ROMANCE_NAME_V1.md"),
        ("divine", "Javane and Bunker — Divine Triangle", BASE + "JAVANE_BUNKER_DIVINE_TRIANGLE_V1.md"),
        ("design", "Post-freeze empirical comparison design", BASE + "EMPIRICAL_COMPARISON_DESIGN.md"),
        ("policy", "Methodology and versioning policy", "docs/24_numerology_methodology_policy.md"),
        ("review", "Independent closeout check", BASE + "CLOSEOUT_REVIEW.md"),
    ]
    style = """body{font:17px/1.65 system-ui,sans-serif;margin:0;color:#202938;background:#f6f7f9}main{max-width:1120px;margin:auto;padding:42px 26px}h1,h2,h3{line-height:1.25;color:#122236}h1{font-size:2rem}h2{margin-top:2em}p,li{max-width:94ch}nav{background:white;border:1px solid #dce2e8;border-radius:10px;padding:20px 28px}a{color:#174d80}section{background:white;padding:25px 30px;margin:28px 0;border:1px solid #dce2e8;border-radius:10px}table{border-collapse:collapse;font-size:14px;min-width:700px}td,th{padding:10px 12px;border:1px solid #d6dce4;vertical-align:top;text-align:left;min-width:125px}th{background:#eef2f6}.table-scroll{overflow:auto;margin:22px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f4f7;padding:15px;font-size:13px}code{overflow-wrap:anywhere}small{color:#586577}blockquote{border-left:4px solid #7b8c9e;padding-left:16px;margin-left:0}@media print{body{background:white}main{max-width:none;padding:0}section{border:0;padding:0;break-before:page}.table-scroll{overflow:visible}table{font-size:9px;min-width:0}td,th{min-width:0;padding:4px}}"""
    def document(chosen):
        toc = "".join(f'<li><a href="#{ident}">{html.escape(title)}</a></li>' for ident,title,_ in chosen)
        body = "".join(f'<section id="{ident}"><small>{html.escape(name)}</small>' + render(data[name].decode()) + '</section>' for ident,_,name in chosen)
        body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
        return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Numerology — Four-book methodology audit</title><style>{style}</style></head><body><main><h1>Four-book numerology methodology audit</h1><p>Separated author systems • source-first freeze • no owner-history refit</p><small>Source revision {revision}. Derived research packet, 4 October 2026.</small><nav><ol>{toc}</ol></nav>{body}</main></body></html>'.encode()
    data["NUMEROLOGY_AUDIT_READER.html"] = document(sections)
    data["SUMMARY.html"] = document(sections[:1])
    payload_manifest = {"schema_version":1,"source_revision":revision,"source_freeze_commit":"af2cbf287635a682d1cdb36597d5a9c47784743c","files":{name:hashlib.sha256(content).hexdigest() for name,content in sorted(data.items())},"raw_books_included":False,"html_has_scripts_or_external_assets":False}
    data["PACKET_MANIFEST.json"] = (json.dumps(payload_manifest,indent=2)+"\n").encode()
    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"Numerology-Four-Book-Audit-V2-20261004-{revision[:8]}.zip"
    if archive.exists():
        raise FileExistsError("Refusing to overwrite an existing delivery: " + str(archive))
    stamp = datetime.fromtimestamp(int(git("show", "-s", "--format=%ct", revision)), tz=timezone.utc)
    ztime = (stamp.year,stamp.month,stamp.day,stamp.hour,stamp.minute,stamp.second)
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,content in sorted(data.items()):
            info=zipfile.ZipInfo(name,ztime);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,content)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise RuntimeError("ZIP CRC verification failed")
        for name,digest in payload_manifest["files"].items():
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:
                raise RuntimeError("ZIP payload hash mismatch: "+name)
    standalone = output / f"Numerology-Audit-Reader-20261004-{revision[:8]}.html"
    standalone.write_bytes(data["NUMEROLOGY_AUDIT_READER.html"])
    summary = output / f"Numerology-Audit-Summary-20261004-{revision[:8]}.html"
    summary.write_bytes(data["SUMMARY.html"])
    print(json.dumps({"source_revision":revision,"archive_path":str(archive),"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"archive_bytes":archive.stat().st_size,"payload_file_count":len(data),"reader_path":str(standalone),"reader_sha256":hashlib.sha256(standalone.read_bytes()).hexdigest(),"summary_path":str(summary),"summary_sha256":hashlib.sha256(summary.read_bytes()).hexdigest(),"zip_crc_and_payload_hashes":"PASS","raw_books_included":False},indent=2))


if __name__ == "__main__":
    main()
