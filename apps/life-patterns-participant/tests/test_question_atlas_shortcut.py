"""The local question guide must link real files and not copy source data."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def atlas_installer():
    path = Path(__file__).resolve().parents[1] / "scripts/install_question_atlas_shortcut.py"
    spec = importlib.util.spec_from_file_location("atlas_installer_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_installer_links_all_researcher_files_without_copying_content(tmp_path):
    module = atlas_installer()
    downloads = tmp_path / "Downloads"
    applications = tmp_path / "applications"
    documents = [
        downloads / module.ATLAS_FOLDER / module.ATLAS_NAME,
        downloads / module.ANSWERS_NAME,
        downloads / module.ATLAS_FOLDER / module.MAPPING_NAME,
    ]
    for i, file in enumerate(documents):
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("PRIVATE_FIXTURE_" + str(i))
    index, desktop = module.make_guide(downloads, applications)
    contents = index.read_text()
    for file in documents:
        assert file.exists()
        assert file.name in contents or module.MAPPING_NAME in contents
    assert contents.count("<article>") == 3
    assert "79 historical" in contents
    assert "25 current" in contents
    assert "diagnostic tests" in contents
    assert "PRIVATE_FIXTURE" not in contents
    assert index.stat().st_mode & 0o777 == 0o600
    assert "Terminal=false" in desktop.read_text()
    assert "Life Patterns Questions and Interpretations" in desktop.read_text()
    assert desktop.stat().st_mode & 0o777 == 0o644


def test_missing_researcher_source_does_not_claim_installed(tmp_path):
    module = atlas_installer()
    with pytest.raises(FileNotFoundError):
        module.make_guide(tmp_path / "empty", tmp_path / "applications")
    assert not (tmp_path / "applications" / module.DESKTOP_NAME).exists()
