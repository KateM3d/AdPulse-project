import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    AdNotFoundError,
    AiInsightsUnavailableError,
    DataLoadingError,
)
from app.dependencies import (
    get_ad_repository,
    get_comments_repository,
    get_metrics_repository,
)
from app.repositories.data_validator import validate_ad_relationships

logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    ads = get_ad_repository().get_all()
    metrics = get_metrics_repository().get_all()
    comments = get_comments_repository().get_all()
    validate_ad_relationships(ads, metrics, comments)

    if settings.ai_provider == "openai" and not settings.has_openai_api_key:
        logger.warning("AI_PROVIDER=openai but OPENAI_API_KEY is empty; insights will return 503")

    yield


app = FastAPI(
    title="AdPulse API",
    description=(
        "AdPulse analytics API for exploring campaign performance, per-ad metrics, "
        "platform breakdowns, timelines, comments, and generated insights. "
        "All bundled campaign data is fictional demo content."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.exception_handler(AdNotFoundError)
async def ad_not_found_handler(
    _request: Request,
    exc: AdNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Ad '{exc.ad_id}' was not found",
        },
    )


@app.exception_handler(DataLoadingError)
async def data_loading_error_handler(
    _request: Request,
    exc: DataLoadingError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


@app.exception_handler(AiInsightsUnavailableError)
async def ai_insights_unavailable_handler(
    _request: Request,
    exc: AiInsightsUnavailableError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )
