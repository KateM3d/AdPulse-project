from app.core.config import get_settings
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.data_validator import validate_ad_relationships
from app.repositories.metrics_repository import MetricsRepository


def test_bundled_data_loads_successfully() -> None:
    settings = get_settings()

    ads = AdRepository(settings.data_dir / "ad_set.csv").get_all()
    metrics = MetricsRepository(settings.data_dir / "metrics.csv").get_all()
    comments = CommentsRepository(settings.data_dir / "comments.csv").get_all()

    validate_ad_relationships(ads, metrics, comments)

    assert len(ads) == 7
    assert len(metrics) == 113
    assert len(comments) == 37
