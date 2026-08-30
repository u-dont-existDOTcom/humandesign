"""Resume or aggregate the fixture-granular qualified real-engine replay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.natal_time.replay import (
    ReplayValidationError,
    current_repository_commit,
    load_replay_context,
    run_replay,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-commit")
    parser.add_argument("--output-root", type=Path, default=Path("state/replay"))
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    repository_commit = args.repository_commit or current_repository_commit(root)
    try:
        context = load_replay_context(root, repository_commit)
        index = run_replay(
            context,
            args.output_root,
            aggregate_only=args.aggregate_only,
        )
    except ReplayValidationError as exc:
        parser.error(str(exc))
    print(json.dumps(index, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
