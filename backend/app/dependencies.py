from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.metrics_repository import MetricsRepository
from app.services.insights.base import InsightsProvider
from app.services.insights.factory import create_insights_provider


def get_ad_repository() -> AdRepository:
    settings = get_settings()
    return AdRepository(settings.data_dir / "ad_set.csv")


def get_metrics_repository() -> MetricsRepository:
    settings = get_settings()
    return MetricsRepository(settings.data_dir / "metrics.csv")


def get_comments_repository() -> CommentsRepository:
    settings = get_settings()
    return CommentsRepository(settings.data_dir / "comments.csv")


def get_insights_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> InsightsProvider:
    return create_insights_provider(settings)
