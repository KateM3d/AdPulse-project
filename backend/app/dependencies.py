from app.core.config import get_settings
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.metrics_repository import MetricsRepository


def get_ad_repository() -> AdRepository:
    settings = get_settings()
    return AdRepository(settings.data_dir / "ad_set.csv")


def get_metrics_repository() -> MetricsRepository:
    settings = get_settings()
    return MetricsRepository(settings.data_dir / "metrics.csv")


def get_comments_repository() -> CommentsRepository:
    settings = get_settings()
    return CommentsRepository(settings.data_dir / "comments.csv")
