"""Frozen symbolic behavioral model and scoring primitives."""

from hdmatch.model.compiler import CompilationResult, compile_mapping_artifacts
from hdmatch.model.mapping_library import MappingLibrary, load_mapping_library
from hdmatch.model.reliability import effective_confidence
from hdmatch.model.symbolic_score import SymbolicScore, score_symbolic
from hdmatch.model.v4_3_compiler import (
    compile_mapping_library_v2,
    compile_mapping_library_v2_file,
)
from hdmatch.model.v4_3_mapping import (
    MappingLibrarySourceV2,
    MappingLibraryV2,
    load_mapping_library_source_v2,
    load_mapping_library_v2,
    require_mapping_feature_coverage,
)

__all__ = [
    "CompilationResult",
    "MappingLibrary",
    "MappingLibrarySourceV2",
    "MappingLibraryV2",
    "SymbolicScore",
    "compile_mapping_artifacts",
    "compile_mapping_library_v2",
    "compile_mapping_library_v2_file",
    "effective_confidence",
    "load_mapping_library",
    "load_mapping_library_source_v2",
    "load_mapping_library_v2",
    "require_mapping_feature_coverage",
    "score_symbolic",
]
