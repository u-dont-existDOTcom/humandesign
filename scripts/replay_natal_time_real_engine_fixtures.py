"""Resume or aggregate the fixture-granular qualified real-engine replay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from hdmatch.natal_time.replay import (
    ReplayValidationError,
    current_repository_commit,
    load_replay_context,
    run_replay,
    verify_production_source,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-commit")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"),
    )
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    repository_commit = args.repository_commit or current_repository_commit(root)
    output_root = args.output_root if args.output_root.is_absolute() else root / args.output_root
    try:
        source_verification = verify_production_source(
            root, repository_commit, output_root
        )
        context = load_replay_context(
            root,
            repository_commit,
            source_verification=source_verification,
        )

        def report(stage: str, name: str) -> None:
            print(
                f"REAL_ENGINE_REPLAY_{stage.upper()}:{name}",
                file=sys.stderr,
                flush=True,
            )

        index = run_replay(
            context,
            output_root,
            aggregate_only=args.aggregate_only,
            progress=report,
        )
    except ReplayValidationError as exc:
        parser.error(str(exc))
    print(json.dumps(index, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
