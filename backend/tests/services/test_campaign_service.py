from datetime import date

from app.models.domain import MetricRecord, Platform
from app.services.campaign_service import CampaignService


def test_get_summary_aggregates_campaign_metrics() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 2),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=1000,
            clicks=20,
            engagements=30,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.META,
            impressions=2000,
            clicks=40,
            engagements=60,
        ),
    ]

    summary = CampaignService().get_summary(metrics)

    assert summary.total_impressions == 3000
    assert summary.total_clicks == 60
    assert summary.total_engagements == 90
    assert summary.ctr == 2.0
    assert summary.engagement_rate == 3.0
    assert summary.start_date == date(2026, 3, 2)
    assert summary.end_date == date(2026, 3, 9)


def test_get_summary_handles_empty_metrics() -> None:
    summary = CampaignService().get_summary([])

    assert summary.total_impressions == 0
    assert summary.total_clicks == 0
    assert summary.total_engagements == 0
    assert summary.ctr == 0.0
    assert summary.engagement_rate == 0.0
    assert summary.start_date is None
    assert summary.end_date is None
