from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
PORTABLE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_portable.py"
BASE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2.py"


def _load(path: Path, name: str) -> ModuleType:
    scripts_value = str(SCRIPTS)
    if scripts_value not in sys.path:
        sys.path.insert(0, scripts_value)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_portability_patch_updates_exact_checked_in_template() -> None:
    base = _load(BASE_SCRIPT, "life_patterns_ui_v2_base_portability_test")
    portable = _load(PORTABLE_SCRIPT, "life_patterns_ui_v2_portability_test")

    original = base._load_html_template()
    patched = portable.patch_html_for_portable_sha256(original)

    assert portable.STRICT_SHA256_JS in original
    assert portable.STRICT_SHA256_JS not in patched
    assert "function sha256Fallback" in patched
    assert "globalThis.crypto&&crypto.subtle" in patched
    assert "return sha256Fallback(bytes)" in patched
    assert len(patched) > len(original)


def test_portability_patch_fails_closed_on_template_drift() -> None:
    portable = _load(PORTABLE_SCRIPT, "life_patterns_ui_v2_portability_drift_test")

    with pytest.raises(ValueError, match="found 0"):
        portable.patch_html_for_portable_sha256("<html>no verifier here</html>")

    duplicated = portable.STRICT_SHA256_JS + portable.STRICT_SHA256_JS
    with pytest.raises(ValueError, match="found 2"):
        portable.patch_html_for_portable_sha256(duplicated)


def test_fallback_preserves_native_webcrypto_preference_and_standard_sha256_iv() -> None:
    portable = _load(PORTABLE_SCRIPT, "life_patterns_ui_v2_portability_constants_test")
    fallback = portable.PORTABLE_SHA256_JS

    assert "globalThis.crypto&&crypto.subtle" in fallback
    assert "crypto.subtle.digest(\"SHA-256\",bytes)" in fallback
    assert "1779033703,3144134277,1013904242,2773480762" in fallback
    assert "function sha256Fallback" in fallback
