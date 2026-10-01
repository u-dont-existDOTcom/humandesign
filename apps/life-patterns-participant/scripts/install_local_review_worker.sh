#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-https://life-patterns-participant-production.up.railway.app}"
TOKEN_FILE="${2:-$HOME/.config/life-patterns/review-worker-token}"
DEST="${LIFE_PATTERNS_REVIEW_WORKER_HOME:-$HOME/.local/share/life-patterns-review-worker}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"
CODEX="$(command -v codex)"
command -v bwrap >/dev/null
[[ "$BASE_URL" == https://life-patterns-participant-production.up.railway.app ]] || exit 2
[[ -f "$TOKEN_FILE" && "$(stat -c '%a' "$TOKEN_FILE")" == 600 ]] || { echo 'Private mode-600 worker token is required.' >&2; exit 2; }
mkdir -p "$DEST" "$HOME/.config/systemd/user"
chmod 700 "$DEST"
STAGE="$(mktemp -d "$DEST/release.XXXXXX")"
mkdir -p "$STAGE/authority"
cp -a "$REPO_ROOT/apps/life-patterns-participant/participant" "$STAGE/"
find "$STAGE" -type d -name __pycache__ -prune -exec rm -r {} +
cp "$REPO_ROOT/apps/life-patterns-participant/scripts/gpt_review_worker.py" "$STAGE/"
cp "$REPO_ROOT/apps/life-patterns-participant/requirements.txt" "$STAGE/"
for FILE in INTERVIEW-PROTOCOL-v6.md interviewer-bank-v7.json EVIDENCE-GUIDE-v7.json; do
  cp "$REPO_ROOT/tasks/scenario-survey-v7-redesign-20260922/$FILE" "$STAGE/authority/"
done
cp "$REPO_ROOT/tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md" "$STAGE/authority/"
if [[ ! -x "$DEST/venv/bin/python" ]]; then
  python3 -m venv "$DEST/venv"
fi
"$DEST/venv/bin/pip" install --quiet -r "$STAGE/requirements.txt"
# Stop only our named worker, preserving encrypted pending state between versions.
systemctl --user stop life-patterns-review-worker.service 2>/dev/null || true
if [[ -d "$DEST/current" && ! -L "$DEST/current" ]]; then
  mv "$DEST/current" "$DEST/previous-legacy"
fi
ln -s "$STAGE" "$DEST/current.new"
mv -Tf "$DEST/current.new" "$DEST/current"
cat > "$HOME/.config/systemd/user/life-patterns-review-worker.service" <<EOF
[Unit]
Description=Life Patterns development review worker (ChatGPT subscription)
After=network-online.target
[Service]
Type=simple
WorkingDirectory=$DEST/current
Environment=PYTHONPATH=$DEST/current
Environment=PATH=$(dirname "$CODEX"):/usr/local/bin:/usr/bin:/bin
ExecStart=$DEST/venv/bin/python $DEST/current/gpt_review_worker.py --base-url $BASE_URL --token-file $TOKEN_FILE --authority-dir $DEST/current/authority
UMask=0077
Restart=on-failure
RestartSec=10
KillMode=control-group
TimeoutStopSec=15
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now life-patterns-review-worker.service
systemctl --user is-active life-patterns-review-worker.service
