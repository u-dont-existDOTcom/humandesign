"""Replay B02r's distinct original-source tests during normal CI."""
import json
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1] / "tasks/astro-source-audit-multipass-20261005/batches/B02r"


def test_lilly_xlviii_and_43_horary_aphorisms():
    result = subprocess.run(
        [sys.executable, str(B / "run_verification.py")],
        cwd=B,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads((B / "TEST_RUN_SUMMARY.json").read_text())
    assert summary["successful"], summary
    assert summary["distinct_test_count"] >= 69, summary
    assert summary["failures"] == summary["errors"] == 0
