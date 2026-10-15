"""Recovery-source and GPT update reproducibility, without real participant data."""

from __future__ import annotations

import importlib.util
import json
import stat
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-gpt-completed-resume-20261015"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def module(name: str):
    f = TASK / name
    spec = importlib.util.spec_from_file_location(f.stem, f)
    assert spec and spec.loader
    object_ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(object_)
    return object_


def synthetic_docx(
    path: Path,
    *,
    skip_number: bool = False,
    edited: bool = True,
    birth_info: bool = False,
    missing_answer: bool = False,
):
    root = ET.Element(W + "document")
    body = ET.SubElement(root, W + "body")

    def add(text: str, style: str = "Normal"):
        p = ET.SubElement(body, W + "p")
        pp = ET.SubElement(p, W + "pPr")
        ET.SubElement(pp, W + "pStyle", {W + "val": style})
        r = ET.SubElement(p, W + "r")
        t = ET.SubElement(r, W + "t")
        t.text = text

    add("Behavioral Patterns Research Interview", "Title")
    add("Answers are lightly edited for spelling." if edited else "No editorial note supplied")
    add("1. Ordinary behavior", "Heading1")
    add("1. How do you respond?", "Question")
    add("It depends on what actually happens.", "Answer")
    add("3. How often?" if skip_number else "2. How often?", "Question")
    if not missing_answer:
        add("Usually after work; no role taken.", "Answer")
    if birth_info:
        add("Date of birth: TEST", "Normal")
    with zipfile.ZipFile(path, "w") as doc:
        doc.writestr("word/document.xml", ET.tostring(root, encoding="utf-8"))


def test_source_only_import_does_not_infer_missing_consent_or_ids(tmp_path):
    parser = module("extract_edited_interview.py")
    docx = tmp_path / "edited.docx"
    synthetic_docx(docx)
    report = parser.extract(docx, expected=2)
    assert report["question_and_answer_count"] == 2
    assert report["source_kind"] == "lightly_edited_interview_document_not_verbatim_chat"
    assert report["consent"]["research_use_consented"] is None
    assert report["original_interviewer_birth_blinding"] == "unknown_from_this_document"
    assert report["turns"][0]["question_text"] == "How do you respond?"
    assert report["turns"][1]["answer_text"] == "Usually after work; no role taken."
    assert all(row["canonical_question_id"] is None for row in report["turns"])
    out = tmp_path / "source-private.json"
    parser.write_private(out, report)
    assert json.loads(out.read_text()) == report
    assert stat.S_IMODE(out.stat().st_mode) == 0o600
    with pytest.raises(FileExistsError):
        parser.write_private(out, report)


@pytest.mark.parametrize(
    "changes",
    [
        {"skip_number": True},
        {"edited": False},
        {"birth_info": True},
        {"missing_answer": True},
    ],
)
def test_source_parser_rejects_fabrication_leakage_or_missing(tmp_path, changes):
    parser = module("extract_edited_interview.py")
    docx = tmp_path / "bad.docx"
    synthetic_docx(docx, **changes)
    with pytest.raises(ValueError):
        parser.extract(docx, expected=2)


def test_unexpected_question_count_fails_closed(tmp_path):
    parser = module("extract_edited_interview.py")
    path = tmp_path / "two.docx"
    synthetic_docx(path)
    with pytest.raises(ValueError, match="count mismatch"):
        parser.extract(path, expected=96)


def test_gpt_packet_stays_under_8000_chars_and_cumulative_action_unchanged():
    builder = module("build_update.py")
    files = builder.components()
    text = files[builder.INSTRUCTIONS].decode()
    assert "COMPLETED-INTERVIEW-CONTINUATION-v1.md" in text
    assert "startLifePatternsReview" in text
    assert "fast-batch-v1" in text
    assert len(text.replace("\n", "\r\n")) <= 8000
    knowledge = sorted(k for k in files if k.startswith("knowledge/"))
    assert len(knowledge) == 8
    guide = files["knowledge/COMPLETED-INTERVIEW-CONTINUATION-v1.md"].decode()
    assert "independent birth-blind review" in guide
    assert "do not conduct the new 25-question TF1 main survey" in guide
    assert "lightly edited" in guide
    assert "role-entry" in guide
    assert "three real-life examples" in guide
    assert all(not name.endswith((".docx", ".source-only.json")) for name in files)
    assert all("/PRIVATE-" not in name for name in files)

    with zipfile.ZipFile(builder.BASE) as base:
        assert files[builder.ACTION] == base.read(builder.ACTION)
        for name in builder.REPLACED_FILES:
            assert files["knowledge/" + name] == base.read("knowledge/" + name)
    binary = builder.archive_bytes(files)
    assert builder.OUT.is_file() and builder.OUT.read_bytes() == binary
    manifest = json.loads(files["UPDATE-MANIFEST.json"])
    assert manifest["action_schema_version"] == "1.6.0"
    assert manifest["knowledge_file_count"] == 8
    assert manifest["same_gpt_same_action_and_credential"]
    assert manifest["participant_text_or_credentials_in_package"] is False
    assert all(builder.sha(files[k]) == v for k, v in manifest["files"].items())


def test_explicit_auth_and_saved_originals_before_new_review():
    guide = (TASK / "COMPLETED-INTERVIEW-CONTINUATION-v1.md").read_text()
    assert "A previous participant's file is never a global GPT Knowledge upload" in guide
    assert "confirm" in guide and "research" in guide and "consent" in guide
    assert "If there is a valid prior" in guide
    assert "do not ask it" in guide
    assert "Do not fabricate" in guide or "Do not recode" in guide


def test_owner_delivery_installs_readable_cumulative_files_and_refuses_drift(tmp_path):
    builder = module("build_update.py")
    installer = module("install_owner_files.py")
    result = installer.install(tmp_path)
    assert result["verified_update_zip_in_downloads"]
    assert result["gpt_editor_updated"] is False
    assert result["knowledge_files"] == 8
    directory = tmp_path / installer.FOLDER
    assert (directory / builder.INSTRUCTIONS).is_file()
    assert (directory / "UPDATE-EXISTING-GPT.md").is_file()
    assert (directory / "knowledge/COMPLETED-INTERVIEW-CONTINUATION-v1.md").is_file()
    assert installer.digest(tmp_path / builder.OUT.name) == installer.digest(builder.OUT)
    assert installer.install(tmp_path) == result  # exact idempotent recheck
    (directory / "knowledge/COMPLETED-INTERVIEW-CONTINUATION-v1.md").write_text("tamper")
    with pytest.raises(ValueError, match="conflict"):
        installer.install(tmp_path)
