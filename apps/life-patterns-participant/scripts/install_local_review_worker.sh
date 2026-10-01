#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-https://life-patterns-participant-production.up.railway.app}"
TOKEN_FILE="${2:-$HOME/.config/life-patterns/review-worker-token}"
DEST="${LIFE_PATTERNS_REVIEW_WORKER_HOME:-$HOME/.local/share/life-patterns-review-worker}"
UNIT_DIR="$HOME/.config/systemd/user"
UNIT="$UNIT_DIR/life-patterns-review-worker.service"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

test -f "$TOKEN_FILE" || { echo "Missing worker token file: $TOKEN_FILE" >&2; exit 2; }
test "$(stat -c '%a' "$TOKEN_FILE")" = "600" || {
  echo "Worker token file must have mode 600." >&2
  exit 2
}

rm -rf "$DEST/stage"
mkdir -p "$DEST/stage/authority" "$UNIT_DIR"
cp -a "$REPO_ROOT/apps/life-patterns-participant/participant" "$DEST/stage/"
cp "$REPO_ROOT/apps/life-patterns-participant/scripts/gpt_review_worker.py" "$DEST/stage/"
cp "$REPO_ROOT/apps/life-patterns-participant/requirements.txt" "$DEST/stage/"
cp "$REPO_ROOT/tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md" "$DEST/stage/authority/"
cp "$REPO_ROOT/tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json" "$DEST/stage/authority/"
cp "$REPO_ROOT/tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json" "$DEST/stage/authority/"
cp "$REPO_ROOT/tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md" "$DEST/stage/authority/"

if [[ ! -x "$DEST/venv/bin/python" ]]; then
  python3 -m venv "$DEST/venv"
  "$DEST/venv/bin/pip" install --quiet -r "$DEST/stage/requirements.txt"
fi

rm -rf "$DEST/current"
mv "$DEST/stage" "$DEST/current"

cat > "$UNIT" <<EOF
[Unit]
Description=Life Patterns local Codex review worker
After=network-online.target

[Service]
Type=simple
Environment=PYTHONPATH=$DEST/current
ExecStart=$DEST/venv/bin/python $DEST/current/gpt_review_worker.py --base-url $BASE_URL --token-file $TOKEN_FILE --authority-dir $DEST/current/authority
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now life-patterns-review-worker.service
systemctl --user --no-pager --full status life-patterns-review-worker.service | sed -n '1,18p'
