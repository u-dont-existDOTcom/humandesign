"""FastAPI application exposing only deterministic, currently supported services.

The normative run endpoints remain present but fail closed with structured 501
responses.  Run storage, profile freezing, holdout release, answer-key reveal,
and experiment orchestration belong to the CLI-first experiment layer and are
not emulated here.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI

from hdmatch import __version__
from hdmatch.api.errors import (
    ERROR_RESPONSES,
    ApiProblem,
    domain_problem,
    engine_problem,
    install_error_handlers,
)
from hdmatch.api.models import (
    ChartComponentMetadata,
    ChartRecord,
    ChartRequest,
    ComponentHealth,
    DateAggregationRequest,
    DateAggregationResponse,
    HealthResponse,
    ModelMetadataResponse,
    NextQuestionRequest,
    NextQuestionResponse,
    QuestionUtilityResponse,
    StateIntervalsRequest,
    StateIntervalsResponse,
    SymbolicModelMetadata,
    SymbolicScoreRequest,
    SymbolicScoreResponse,
)
from hdmatch.api.serialization import (
    chart_record,
    engine_metadata,
    ephemeris_metadata,
    state_interval_record,
)
from hdmatch.api.unresolved import register_unresolved_run_routes
from hdmatch.chart.boundaries import build_chart_state_intervals
from hdmatch.chart.calculator import CHART_ENGINE_VERSION, calculate_chart
from hdmatch.chart.design_moment import DesignMomentError
from hdmatch.chart.ephemeris import EphemerisError, EphemerisProvider
from hdmatch.chart.timezone import timezone_database_version
from hdmatch.model.mapping_library import MappingLibrary, MappingStatus
from hdmatch.model.symbolic_score import score_symbolic
from hdmatch.search import aggregate_dates, select_next_question


@dataclass(frozen=True, slots=True)
class ApiDependencies:
    """Public, non-secret dependencies injected when constructing the service."""

    ephemeris_provider: EphemerisProvider | None = None
    mapping_library: MappingLibrary | None = None
    code_commit: str = "unknown"


def create_app(dependencies: ApiDependencies | None = None) -> FastAPI:
    """Build an application without acquiring any answer-key capability."""

    deps = dependencies or ApiDependencies()
    service = FastAPI(
        title="Human Design Reverse-Matching Search API",
        version=__version__,
        description=(
            "Deterministic chart/model primitives. Stateful blind-run operations "
            "remain unresolved and fail closed."
        ),
    )
    install_error_handlers(service)

    @service.get(
        "/health",
        response_model=HealthResponse,
        responses=ERROR_RESPONSES,
        operation_id="getHealth",
    )
    @service.get(
        "/v1/health",
        response_model=HealthResponse,
        responses=ERROR_RESPONSES,
        include_in_schema=False,
    )
    async def health() -> HealthResponse:
        return HealthResponse(
            api_version=__version__,
            chart_engine=ComponentHealth(
                status="ready" if deps.ephemeris_provider is not None else "unconfigured",
                detail=(
                    "deterministic ephemeris provider is configured"
                    if deps.ephemeris_provider is not None
                    else "inject a strict ephemeris provider to enable chart endpoints"
                ),
            ),
            symbolic_model=ComponentHealth(
                status="ready" if deps.mapping_library is not None else "unconfigured",
                detail=(
                    "frozen mapping library is configured"
                    if deps.mapping_library is not None
                    else "inject a frozen mapping library to enable symbolic scoring"
                ),
            ),
        )

    @service.get(
        "/v1/model/metadata",
        response_model=ModelMetadataResponse,
        responses=ERROR_RESPONSES,
        operation_id="getModelMetadata",
    )
    async def model_metadata() -> ModelMetadataResponse:
        provider_metadata = (
            ephemeris_metadata(deps.ephemeris_provider.metadata)
            if deps.ephemeris_provider is not None
            else None
        )
        library = deps.mapping_library
        symbolic = SymbolicModelMetadata(status="unconfigured")
        if library is not None:
            symbolic = SymbolicModelMetadata(
                status="ready",
                model_version=library.model_version,
                mapping_library_sha256=library.sha256(),
                question_bank_version=library.question_bank_version,
                frozen_mapping_count=len(library.frozen_mappings),
                unresolved_mapping_count=sum(
                    mapping.status is MappingStatus.UNRESOLVED for mapping in library.mappings
                ),
            )
        return ModelMetadataResponse(
            api_version=__version__,
            code_commit=deps.code_commit,
            chart=ChartComponentMetadata(
                status="ready" if provider_metadata is not None else "unconfigured",
                chart_engine_version=CHART_ENGINE_VERSION,
                timezone_database_version=timezone_database_version(),
                ephemeris=provider_metadata,
            ),
            symbolic=symbolic,
            unavailable_capabilities=(
                "stateful_run_storage",
                "profile_freezing",
                "bounded_candidate_ranking",
                "global_scored_search",
                "holdout_release",
                "robustness_orchestration",
                "final_report_reveal",
                "advanced_color_tone_base",
                "independent_engine_verification",
            ),
        )

    @service.post(
        "/v1/chart",
        response_model=ChartRecord,
        responses=ERROR_RESPONSES,
        operation_id="calculateChart",
    )
    async def chart(request: ChartRequest) -> ChartRecord:
        provider = _require_provider(deps)
        try:
            computation = calculate_chart(
                provider,
                request.birth_utc,
                design_time_tolerance_seconds=request.design_time_tolerance_seconds,
                design_arc_tolerance_degrees=request.design_arc_tolerance_degrees,
            )
        except ValueError as exc:
            raise domain_problem(exc) from exc
        except (DesignMomentError, EphemerisError) as exc:
            raise engine_problem(exc) from exc
        return chart_record(computation)

    @service.post(
        "/v1/chart/state-intervals",
        response_model=StateIntervalsResponse,
        responses=ERROR_RESPONSES,
        operation_id="calculateChartStateIntervals",
    )
    async def state_intervals(request: StateIntervalsRequest) -> StateIntervalsResponse:
        provider = _require_provider(deps)
        try:
            intervals = build_chart_state_intervals(
                provider,
                request.range_start_utc,
                request.range_end_utc,
                root_tolerance_seconds=request.boundary_tolerance_seconds,
            )
            records = tuple(
                state_interval_record(
                    provider,
                    interval,
                    root_tolerance_seconds=request.boundary_tolerance_seconds,
                )
                for interval in intervals
            )
            representative = calculate_chart(
                provider,
                request.range_start_utc + (request.range_end_utc - request.range_start_utc) / 2,
                design_time_tolerance_seconds=request.boundary_tolerance_seconds,
            )
        except ValueError as exc:
            raise domain_problem(exc) from exc
        except (DesignMomentError, EphemerisError) as exc:
            raise engine_problem(exc) from exc
        return StateIntervalsResponse(
            range_start_utc=request.range_start_utc,
            range_end_utc=request.range_end_utc,
            intervals=records,
            engine_metadata=engine_metadata(representative),
        )

    @service.post(
        "/v1/model/symbolic-score",
        response_model=SymbolicScoreResponse,
        responses=ERROR_RESPONSES,
        operation_id="scoreSymbolicModel",
    )
    async def symbolic_score(request: SymbolicScoreRequest) -> SymbolicScoreResponse:
        library = _require_mapping_library(deps)
        try:
            result = score_symbolic(
                request.chart_features,
                request.responses,
                library,
                request.prevalence_by_anchor,
            )
        except (KeyError, ValueError) as exc:
            raise domain_problem(exc) from exc
        return SymbolicScoreResponse(
            model_version=library.model_version,
            mapping_library_sha256=library.sha256(),
            score=result,
        )

    @service.post(
        "/v1/search/date-aggregation",
        response_model=DateAggregationResponse,
        responses=ERROR_RESPONSES,
        operation_id="aggregateDateScores",
    )
    async def date_aggregation(request: DateAggregationRequest) -> DateAggregationResponse:
        try:
            results = aggregate_dates(
                request.states,
                request.scores,
                request.mode,
                request.threshold_rubric_bits,
            )
        except ValueError as exc:
            raise domain_problem(exc) from exc
        return DateAggregationResponse(results=results)

    @service.post(
        "/v1/search/next-question",
        response_model=NextQuestionResponse,
        responses=ERROR_RESPONSES,
        operation_id="selectNextQuestion",
    )
    async def next_question(request: NextQuestionRequest) -> NextQuestionResponse:
        try:
            selected = select_next_question(
                request.candidate_weights,
                request.likelihoods_by_question,
                request.expected_reliability,
                request.burden,
            )
        except ValueError as exc:
            raise domain_problem(exc) from exc
        response = None
        if selected is not None:
            response = QuestionUtilityResponse(
                question_id=selected.question_id,
                expected_information_gain=selected.expected_information_gain,
                adjusted_utility=selected.adjusted_utility,
                expected_reliability=selected.expected_reliability,
                burden=selected.burden,
            )
        return NextQuestionResponse(selection=response)

    register_unresolved_run_routes(service)
    return service


def _require_provider(dependencies: ApiDependencies) -> EphemerisProvider:
    provider = dependencies.ephemeris_provider
    if provider is None:
        raise ApiProblem(
            503,
            "EPHEMERIS_NOT_CONFIGURED",
            "a strict deterministic ephemeris provider is required for this endpoint",
        )
    return provider


def _require_mapping_library(dependencies: ApiDependencies) -> MappingLibrary:
    library = dependencies.mapping_library
    if library is None:
        raise ApiProblem(
            503,
            "MAPPING_LIBRARY_NOT_CONFIGURED",
            "a frozen mapping library is required for symbolic scoring",
        )
    return library


app = create_app()
