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


def test_get_summary_calculates_rate_from_aggregated_totals() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=10,
        ),
        MetricRecord(
            date=date(2026, 3, 16),
            ad_id="ad-2",
            platform=Platform.META,
            impressions=900,
            clicks=45,
            engagements=90,
        ),
    ]

    summary = CampaignService().get_summary(metrics)

    assert summary.ctr == 5.5
    assert summary.engagement_rate == 10.0


def test_get_timeline_aggregates_metrics_by_date() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=20,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.META,
            impressions=300,
            clicks=30,
            engagements=60,
        ),
    ]

    timeline = CampaignService().get_timeline(metrics)

    assert len(timeline) == 1

    point = timeline[0]

    assert point.date == date(2026, 3, 9)
    assert point.impressions == 400
    assert point.clicks == 40
    assert point.engagements == 80
    assert point.ctr == 10.0
    assert point.engagement_rate == 20.0


def test_get_timeline_returns_points_in_chronological_order() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 16),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=20,
        ),
        MetricRecord(
            date=date(2026, 3, 2),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=200,
            clicks=20,
            engagements=40,
        ),
    ]

    timeline = CampaignService().get_timeline(metrics)

    assert [point.date for point in timeline] == [
        date(2026, 3, 2),
        date(2026, 3, 16),
    ]


def test_get_timeline_calculates_rate_from_aggregated_totals() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=10,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.META,
            impressions=900,
            clicks=45,
            engagements=90,
        ),
    ]

    timeline = CampaignService().get_timeline(metrics)

    assert timeline[0].ctr == 5.5
    assert timeline[0].engagement_rate == 10.0


def test_get_timeline_returns_empty_list_when_no_metrics() -> None:
    timeline = CampaignService().get_timeline([])

    assert timeline == []


def test_get_platform_summary_aggregates_metrics_by_platform() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-3",
            platform=Platform.META,
            impressions=500,
            clicks=25,
            engagements=50,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=20,
        ),
        MetricRecord(
            date=date(2026, 3, 16),
            ad_id="ad-2",
            platform=Platform.GOOGLE,
            impressions=300,
            clicks=30,
            engagements=60,
        ),
    ]

    summaries = CampaignService().get_platform_summary(metrics)

    assert [summary.platform for summary in summaries] == [
        Platform.GOOGLE,
        Platform.META,
    ]

    google = summaries[0]

    assert google.impressions == 400
    assert google.clicks == 40
    assert google.engagements == 80
    assert google.ctr == 10.0
    assert google.engagement_rate == 20.0

    meta = summaries[1]

    assert meta.impressions == 500
    assert meta.clicks == 25
    assert meta.engagements == 50
    assert meta.ctr == 5.0
    assert meta.engagement_rate == 10.0


def test_get_platform_summary_returns_empty_list_when_no_metrics() -> None:
    summaries = CampaignService().get_platform_summary([])

    assert summaries == []
