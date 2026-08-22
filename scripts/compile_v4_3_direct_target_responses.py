#!/usr/bin/env python3
"""Generate or verify the canonical V3.6 direct-target response artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from hdmatch.experiments.canonical import canonical_json_bytes
from hdmatch.model.v4_3_profile_mapping import (
    BEST_CURRENT_COMPILED_PATH,
    BEST_CURRENT_SOURCE_PATH,
    LESS_CONTAMINATED_COMPILED_PATH,
    LESS_CONTAMINATED_SOURCE_PATH,
)
from hdmatch.model.v4_3_responses import (
    BEST_CURRENT_RESPONSE_PATH,
    LESS_CONTAMINATED_RESPONSE_PATH,
    compile_v4_3_direct_target_responses,
    verify_v4_3_direct_target_responses,
    write_v4_3_direct_target_responses_new,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    variants = (
        (
            "less_contaminated",
            LESS_CONTAMINATED_COMPILED_PATH,
            LESS_CONTAMINATED_SOURCE_PATH,
            LESS_CONTAMINATED_RESPONSE_PATH,
        ),
        (
            "best_current_descriptive",
            BEST_CURRENT_COMPILED_PATH,
            BEST_CURRENT_SOURCE_PATH,
            BEST_CURRENT_RESPONSE_PATH,
        ),
    )
    for variant, compiled, source, output in variants:
        artifact = compile_v4_3_direct_target_responses(
            repository_root=root,
            mapping_library_path=root / compiled,
            mapping_source_library_path=root / source,
            variant=variant,
        )
        output_path = root / output
        if args.write:
            write_v4_3_direct_target_responses_new(output_path, artifact)
        else:
            if output_path.read_bytes() != canonical_json_bytes(artifact):
                raise ValueError(f"tracked direct-target response bytes differ: {output}")
            verify_v4_3_direct_target_responses(
                output_path,
                repository_root=root,
                mapping_library_path=root / compiled,
                mapping_source_library_path=root / source,
            )
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
