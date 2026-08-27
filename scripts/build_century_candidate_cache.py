#!/usr/bin/env python3
"""Compatibility entry point for the structural century-cache builder.

The original implementation resolved every line transition for every body and was
far too expensive for a 100-year production universe.  Keep this filename working,
but route all builds through the single v2 structural implementation so there is no
second cache semantics to accidentally invoke.
"""

from build_century_candidate_cache_fast import main


if __name__ == "__main__":
    main()
