"""Resume or aggregate the fixture-granular qualified real-engine replay."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from hdmatch.natal_time.replay import (
    ReplayContext,
    ReplayExpectation,
    ReplayValidationError,
    current_repository_commit,
    load_replay_context,
    real_engine_fixture_executor,
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
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    repository_commit = args.repository_commit or current_repository_commit(root)
    try:
        context = load_replay_context(root, repository_commit)

        def reporting_executor(
            replay_context: ReplayContext,
            expectations: tuple[ReplayExpectation, ...],
        ) -> Sequence[Mapping[str, Any]]:
            name = expectations[0].source_fixture_name
            print(f"REAL_ENGINE_REPLAY_START:{name}", file=sys.stderr, flush=True)
            receipts = real_engine_fixture_executor(replay_context, expectations)
            print(f"REAL_ENGINE_REPLAY_DONE:{name}", file=sys.stderr, flush=True)
            return receipts

        index = run_replay(
            context,
            args.output_root,
            executor=reporting_executor,
            aggregate_only=args.aggregate_only,
        )
    except ReplayValidationError as exc:
        parser.error(str(exc))
    print(json.dumps(index, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
