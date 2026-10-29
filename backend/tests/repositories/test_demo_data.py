import csv
from collections import defaultdict
from datetime import date

from app.core.config import get_settings
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.data_validator import validate_ad_relationships
from app.repositories.metrics_repository import MetricsRepository
from app.services.ad_service import AdService
from app.services.campaign_service import CampaignService


def test_bundled_demo_data_loads_successfully() -> None:
    settings = get_settings()

    ads = AdRepository(settings.data_dir / "ad_set.csv").get_all()
    metrics = MetricsRepository(settings.data_dir / "metrics.csv").get_all()
    comments = CommentsRepository(settings.data_dir / "comments.csv").get_all()

    validate_ad_relationships(ads, metrics, comments)

    assert len(ads) == 7
    assert len(metrics) == 113
    assert len(comments) == 37


def test_demo_metrics_are_internally_consistent() -> None:
    metrics = MetricsRepository(get_settings().data_dir / "metrics.csv").get_all()

    for record in metrics:
        assert record.impressions > 0
        assert record.clicks <= record.impressions
        # Engagements include clicks.
        assert record.clicks <= record.engagements <= record.impressions

    keys = [(record.date, record.ad_id, record.platform) for record in metrics]
    assert len(keys) == len(set(keys)), "each ad/platform has at most one row per week"


def test_demo_comments_fall_within_each_ads_delivery() -> None:
    settings = get_settings()
    metrics = MetricsRepository(settings.data_dir / "metrics.csv").get_all()
    comments = CommentsRepository(settings.data_dir / "comments.csv").get_all()

    delivery: dict[str, set[str]] = defaultdict(set)
    first_date: dict[str, date] = {}
    for record in metrics:
        delivery[record.ad_id].add(record.platform)
        first_date[record.ad_id] = min(first_date.get(record.ad_id, record.date), record.date)

    for comment in comments:
        assert comment.platform in delivery[comment.ad_id]
        assert comment.date >= first_date[comment.ad_id]


def test_aggregates_match_independent_csv_totals() -> None:
    """Recompute totals straight from the CSV to guard the service-layer arithmetic."""
    settings = get_settings()

    with (settings.data_dir / "metrics.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    impressions = sum(int(row["impressions"]) for row in rows)
    clicks = sum(int(row["clicks"]) for row in rows)
    engagements = sum(int(row["engagements"]) for row in rows)

    metrics = MetricsRepository(settings.data_dir / "metrics.csv").get_all()
    summary = CampaignService().get_summary(metrics)

    assert summary.total_impressions == impressions == 1281840
    assert summary.total_clicks == clicks == 15220
    assert summary.total_engagements == engagements == 24666
    assert summary.ctr == clicks / impressions * 100
    assert summary.engagement_rate == engagements / impressions * 100

    ads = AdRepository(settings.data_dir / "ad_set.csv").get_all()
    ad_summaries = AdService().get_ad_summaries(ads, metrics)

    assert sum(ad.total_impressions for ad in ad_summaries) == impressions
    assert sum(ad.total_clicks for ad in ad_summaries) == clicks
    assert sum(ad.total_engagements for ad in ad_summaries) == engagements

    platforms = CampaignService().get_platform_summary(metrics)
    assert sum(platform.impressions for platform in platforms) == impressions

    timeline = CampaignService().get_timeline(metrics)
    assert sum(point.clicks for point in timeline) == clicks
