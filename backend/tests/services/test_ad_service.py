from datetime import date

from app.models.domain import Ad, Comment, MetricRecord, Platform
from app.services.ad_service import AdService


def test_get_ad_summaries_aggregates_metrics_by_ad() -> None:
    ads = [
        Ad(
            ad_id="ad-1",
            title="First ad",
            body="First body",
            image="first.png",
        ),
        Ad(
            ad_id="ad-2",
            title="Second ad",
            body="Second body",
            image="second.png",
        ),
    ]

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
            date=date(2026, 3, 16),
            ad_id="ad-1",
            platform=Platform.META,
            impressions=300,
            clicks=15,
            engagements=30,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.LINKEDIN,
            impressions=500,
            clicks=25,
            engagements=50,
        ),
    ]

    summaries = AdService().get_ad_summaries(ads, metrics)

    assert len(summaries) == 2

    first = summaries[0]

    assert first.ad_id == "ad-1"
    assert first.title == "First ad"
    assert first.image == "first.png"
    assert first.total_impressions == 400
    assert first.total_clicks == 25
    assert first.total_engagements == 50
    assert first.ctr == 6.25
    assert first.engagement_rate == 12.5

    second = summaries[1]

    assert second.ad_id == "ad-2"
    assert second.total_impressions == 500
    assert second.total_clicks == 25
    assert second.total_engagements == 50
    assert second.ctr == 5.0
    assert second.engagement_rate == 10.0


def test_get_ad_summaries_includes_ad_without_metrics() -> None:
    ads = [
        Ad(
            ad_id="ad-1",
            title="First ad",
            body="First body",
            image="first.png",
        )
    ]

    summaries = AdService().get_ad_summaries(ads, [])

    assert len(summaries) == 1

    summary = summaries[0]

    assert summary.ad_id == "ad-1"
    assert summary.total_impressions == 0
    assert summary.total_clicks == 0
    assert summary.total_engagements == 0
    assert summary.ctr == 0.0
    assert summary.engagement_rate == 0.0


def test_get_ad_timeline_aggregates_only_requested_ad() -> None:
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
            ad_id="ad-1",
            platform=Platform.META,
            impressions=300,
            clicks=15,
            engagements=30,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.GOOGLE,
            impressions=1000,
            clicks=500,
            engagements=500,
        ),
    ]

    timeline = AdService().get_ad_timeline("ad-1", metrics)

    assert len(timeline) == 1

    point = timeline[0]

    assert point.date == date(2026, 3, 9)
    assert point.impressions == 400
    assert point.clicks == 25
    assert point.engagements == 50
    assert point.ctr == 6.25
    assert point.engagement_rate == 12.5


def test_get_ad_timeline_returns_empty_list_when_ad_has_no_metrics() -> None:
    timeline = AdService().get_ad_timeline("missing-ad", [])

    assert timeline == []


def test_get_ad_platform_summary_aggregates_only_requested_ad() -> None:
    metrics = [
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.META,
            impressions=300,
            clicks=15,
            engagements=30,
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
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=5,
            engagements=10,
        ),
        MetricRecord(
            date=date(2026, 3, 9),
            ad_id="ad-2",
            platform=Platform.GOOGLE,
            impressions=1000,
            clicks=500,
            engagements=500,
        ),
    ]

    summaries = AdService().get_ad_platform_summary("ad-1", metrics)

    assert [summary.platform for summary in summaries] == [
        Platform.GOOGLE,
        Platform.META,
    ]

    google = summaries[0]

    assert google.impressions == 200
    assert google.clicks == 15
    assert google.engagements == 30
    assert google.ctr == 7.5
    assert google.engagement_rate == 15.0

    meta = summaries[1]

    assert meta.impressions == 300
    assert meta.clicks == 15
    assert meta.engagements == 30
    assert meta.ctr == 5.0
    assert meta.engagement_rate == 10.0


def test_get_ad_detail_combines_ad_metrics_and_comments() -> None:
    ad = Ad(
        ad_id="ad-1",
        title="First ad",
        body="First body",
        image="first.png",
    )

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
            date=date(2026, 3, 16),
            ad_id="ad-1",
            platform=Platform.META,
            impressions=300,
            clicks=15,
            engagements=30,
        ),
    ]

    comments = [
        Comment(
            date=date(2026, 3, 16),
            ad_id="ad-1",
            platform=Platform.META,
            comment="Second comment",
        ),
        Comment(
            date=date(2026, 3, 12),
            ad_id="ad-2",
            platform=Platform.GOOGLE,
            comment="Other ad comment",
        ),
        Comment(
            date=date(2026, 3, 9),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            comment="First comment",
        ),
    ]

    detail = AdService().get_ad_detail(
        ad=ad,
        metrics=metrics,
        comments=comments,
    )

    assert detail.ad_id == "ad-1"
    assert detail.title == "First ad"
    assert detail.body == "First body"
    assert detail.image == "first.png"

    assert detail.total_impressions == 400
    assert detail.total_clicks == 25
    assert detail.total_engagements == 50
    assert detail.ctr == 6.25
    assert detail.engagement_rate == 12.5

    assert len(detail.timeline) == 2
    assert [point.date for point in detail.timeline] == [
        date(2026, 3, 9),
        date(2026, 3, 16),
    ]

    assert len(detail.platforms) == 2

    assert [comment.comment for comment in detail.comments] == [
        "First comment",
        "Second comment",
    ]


def test_get_ad_detail_handles_ad_without_metrics_or_comments() -> None:
    ad = Ad(
        ad_id="ad-1",
        title="First ad",
        body="First body",
        image="first.png",
    )

    detail = AdService().get_ad_detail(
        ad=ad,
        metrics=[],
        comments=[],
    )

    assert detail.ad_id == "ad-1"
    assert detail.total_impressions == 0
    assert detail.total_clicks == 0
    assert detail.total_engagements == 0
    assert detail.ctr == 0.0
    assert detail.engagement_rate == 0.0
    assert detail.timeline == []
    assert detail.platforms == []
    assert detail.comments == []
