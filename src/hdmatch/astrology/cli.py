"""Command-line entrypoint for research-only birth-derived primary-direction timelines.

Example (with official Swiss .se1 files already downloaded):
  PYTHONPATH=src python -m hdmatch.astrology.cli \
    --utc 2000-01-01T12:00:00Z --latitude 45 --longitude-east 0 \
    --ephemeris-dir /absolute/path/to/ephe --output /tmp/timeline.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from .aspect_timeline import (
    AspectProfile,
    AspectTimeline,
    SignificatorProjection,
    generate_aspect_timeline,
)
from .geometry import GeometryMethod
from .sky import snapshot_from_swiss_files
from .timeline import TimeKey, Timeline, generate_timeline


def parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("--utc requires a timezone offset, e.g. 2000-01-01T12:00:00Z")
    return dt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Research-only conjunction primary directions with strict SWIEPH"
    )
    parser.add_argument(
        "--utc", required=True, help="ISO 8601 birth instant with explicit offset, e.g. ...Z"
    )
    parser.add_argument(
        "--latitude",
        type=float,
        required=True,
        help="geographic north-positive latitude in degrees",
    )
    parser.add_argument(
        "--longitude-east",
        type=float,
        required=True,
        help="east-positive geographic longitude in degrees",
    )
    parser.add_argument(
        "--ephemeris-dir",
        type=Path,
        required=True,
        help="directory containing official sepl_18.se1 and semo_18.se1",
    )
    parser.add_argument(
        "--method", choices=["all"] + [m.value for m in GeometryMethod], default="all"
    )
    parser.add_argument(
        "--key",
        choices=[x.value for x in TimeKey],
        default=TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR.value,
    )
    parser.add_argument("--max-age", type=float, default=100.0)
    parser.add_argument(
        "--profile",
        choices=["body_conjunctions", *(item.value for item in AspectProfile)],
        default="body_conjunctions",
        help=(
            "bodily conjunctions (legacy default), zodiacal promissor rays, "
            "or mundane semi-arc phase aspects"
        ),
    )
    parser.add_argument(
        "--significator-projection",
        choices=[x.value for x in SignificatorProjection],
        default=SignificatorProjection.RETAIN_BODILY.value,
        help="project the fixed planetary significator to beta=0 only for zodiacal ray profile",
    )
    parser.add_argument("--output", default="-", help="JSON output path or '-' for stdout")
    args = parser.parse_args(argv)
    try:
        sky = snapshot_from_swiss_files(
            parse_utc(args.utc),
            latitude_deg=args.latitude,
            longitude_east_deg=args.longitude_east,
            ephemeris_directory=args.ephemeris_dir,
        )
        methods = tuple(GeometryMethod) if args.method == "all" else (GeometryMethod(args.method),)
        timeline: Timeline | AspectTimeline
        if args.profile == "body_conjunctions":
            if args.significator_projection != SignificatorProjection.RETAIN_BODILY.value:
                raise ValueError(
                    "bodily conjunction profile does not support significator projection"
                )
            timeline = generate_timeline(
                sky, methods=methods, time_key=TimeKey(args.key), max_age_years=args.max_age
            )
        else:
            profile = AspectProfile(args.profile)
            selected_methods = (
                None
                if profile is AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC and args.method == "all"
                else methods
            )
            timeline = generate_aspect_timeline(
                sky,
                profile=profile,
                methods=selected_methods,
                significator_projection=SignificatorProjection(args.significator_projection),
                time_key=TimeKey(args.key),
                max_age_years=args.max_age,
            )
    except (ValueError, RuntimeError, OverflowError) as exc:
        parser.exit(status=2, message=f"primary-direction calculation failed: {exc}\n")
    json_text = json.dumps(timeline.to_dict(), ensure_ascii=False, indent=2) + "\n"
    if args.output == "-":
        sys.stdout.write(json_text)
    else:
        path = Path(args.output)
        if path.exists():
            parser.exit(2, message=f"refusing to overwrite output file: {path}\n")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json_text, encoding="utf-8")
        print(f"saved {len(timeline.directions)} research-only contacts to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
