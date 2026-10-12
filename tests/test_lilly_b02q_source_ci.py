"""Run all forty-seven B02q source-fidelity tests in CI."""
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1] / "tasks/astro-source-audit-multipass-20261005/batches/B02q"


def test_b02q_source_verification():
    p = subprocess.run([sys.executable, str(B / "run_verification.py")], cwd=B,
                       capture_output=True, text=True, timeout=120, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
