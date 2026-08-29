FROM python:3.12-slim

WORKDIR /app

COPY . /app

# pyswisseph does not currently publish a compatible wheel for this image, so build
# its extension from source, then remove the compiler toolchain from the runtime image.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir '.[api,ephemeris]' && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/* /root/.cache/pip

ARG SWISSEPH_COMMIT=3fd0f956d73898b91cc4f67cf18b21af656d1342
RUN mkdir -p /opt/swisseph && python - <<'PY'
import hashlib
import os
import urllib.request
from pathlib import Path

commit = os.environ.get("SWISSEPH_COMMIT") or "3fd0f956d73898b91cc4f67cf18b21af656d1342"
root = Path("/opt/swisseph")
files = {
    "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
}
for name, expected in files.items():
    url = f"https://raw.githubusercontent.com/aloistr/swisseph/{commit}/ephe/{name}"
    data = urllib.request.urlopen(url, timeout=60).read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SystemExit(f"Swiss Ephemeris hash mismatch for {name}: {actual}")
    (root / name).write_bytes(data)
PY

ENV PYTHONUNBUFFERED=1
ENV HDMATCH_EPHEMERIS_PATH=/opt/swisseph

CMD ["/bin/sh", "-c", "exec python -m uvicorn hdmatch.api.relationship_launch_app:create_relationship_launch_app_from_env --factory --host 0.0.0.0 --port ${PORT:-8000}"]
