from datetime import date, timedelta

from app.models.domain import Platform
from app.schemas.ad import AdComment, AdDetail
from app.schemas.ai_insights import AiInsightContext
from app.schemas.analytics import PlatformSummary, TimelinePoint
from app.schemas.campaign import CampaignSummary
from app.services.metrics import calculate_rate

BENCHMARK_CTR = 1.0
BENCHMARK_ENGAGEMENT_RATE = 2.0


def timeline_point(week: int, impressions: int, clicks: int, engagements: int) -> TimelinePoint:
    return TimelinePoint(
        date=date(2026, 3, 2) + timedelta(weeks=week),
        impressions=impressions,
        clicks=clicks,
        engagements=engagements,
        ctr=calculate_rate(clicks, impressions),
        engagement_rate=calculate_rate(engagements, impressions),
    )


def platform_summary(
    platform: Platform, impressions: int, clicks: int, engagements: int
) -> PlatformSummary:
    return PlatformSummary(
        platform=platform,
        impressions=impressions,
        clicks=clicks,
        engagements=engagements,
        ctr=calculate_rate(clicks, impressions),
        engagement_rate=calculate_rate(engagements, impressions),
    )


def make_context(
    timeline: list[TimelinePoint],
    platforms: list[PlatformSummary] | None = None,
    comments: list[AdComment] | None = None,
) -> AiInsightContext:
    """Build a context whose totals are derived from the timeline, like the real services."""
    impressions = sum(point.impressions for point in timeline)
    clicks = sum(point.clicks for point in timeline)
    engagements = sum(point.engagements for point in timeline)

    if platforms is None:
        platforms = [platform_summary(Platform.LINKEDIN, impressions, clicks, engagements)]

    return AiInsightContext(
        selected_ad=AdDetail(
            ad_id="test-ad",
            title="Test ad",
            body="Test body",
            image="test.svg",
            total_impressions=impressions,
            total_clicks=clicks,
            total_engagements=engagements,
            ctr=calculate_rate(clicks, impressions),
            engagement_rate=calculate_rate(engagements, impressions),
            timeline=timeline,
            platforms=platforms,
            comments=comments or [],
        ),
        campaign_benchmarks=CampaignSummary(
            total_impressions=100_000,
            total_clicks=round(100_000 * BENCHMARK_CTR / 100),
            total_engagements=round(100_000 * BENCHMARK_ENGAGEMENT_RATE / 100),
            ctr=BENCHMARK_CTR,
            engagement_rate=BENCHMARK_ENGAGEMENT_RATE,
            start_date=date(2026, 3, 2),
            end_date=date(2026, 5, 4),
        ),
    )


def flat_timeline(
    weeks: int, impressions: int, ctr: float, engagement_rate: float
) -> list[TimelinePoint]:
    return [
        timeline_point(
            week,
            impressions,
            round(impressions * ctr / 100),
            round(impressions * engagement_rate / 100),
        )
        for week in range(weeks)
    ]
