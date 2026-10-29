import pytest

from app.core.config import get_settings
from app.models.domain import Platform
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.metrics_repository import MetricsRepository
from app.schemas.ai_insights import AiInsightContext
from app.services.ad_service import AdService
from app.services.campaign_service import CampaignService
from app.services.insights.demo_provider import (
    DemoInsightsProvider,
    InsightPattern,
    classify,
    extract_signals,
)
from tests.insight_factories import (
    flat_timeline,
    make_context,
    platform_summary,
    timeline_point,
)


def pattern_of(context: AiInsightContext) -> InsightPattern:
    return classify(extract_signals(context))


def test_no_delivery() -> None:
    context = make_context(flat_timeline(6, 0, 0, 0), platforms=[])

    assert pattern_of(context) is InsightPattern.NO_DELIVERY


def test_limited_data_when_fewer_than_four_weeks() -> None:
    context = make_context(flat_timeline(3, 10_000, 3.0, 5.0))

    assert pattern_of(context) is InsightPattern.LIMITED_DATA


def test_declining_ctr() -> None:
    timeline = [
        timeline_point(0, 10_000, 200, 300),
        timeline_point(1, 10_000, 190, 300),
        timeline_point(2, 10_000, 100, 200),
        timeline_point(3, 10_000, 90, 200),
    ]

    assert pattern_of(make_context(timeline)) is InsightPattern.DECLINING


def test_recovering_ctr() -> None:
    timeline = [
        timeline_point(0, 10_000, 60, 150),
        timeline_point(1, 10_000, 70, 150),
        timeline_point(2, 10_000, 120, 250),
        timeline_point(3, 10_000, 130, 250),
    ]

    assert pattern_of(make_context(timeline)) is InsightPattern.RECOVERING


def test_platform_gap() -> None:
    timeline = flat_timeline(6, 20_000, 1.2, 2.0)
    platforms = [
        platform_summary(Platform.LINKEDIN, 60_000, 1_200, 1_800),
        platform_summary(Platform.META, 60_000, 240, 600),
    ]

    assert pattern_of(make_context(timeline, platforms)) is InsightPattern.PLATFORM_GAP


def test_engagement_without_clicks() -> None:
    context = make_context(flat_timeline(6, 10_000, 0.6, 3.0))

    assert pattern_of(context) is InsightPattern.ENGAGEMENT_WITHOUT_CLICKS


def test_outperforming() -> None:
    context = make_context(flat_timeline(6, 10_000, 1.8, 2.5))

    assert pattern_of(context) is InsightPattern.OUTPERFORMING


def test_underperforming() -> None:
    context = make_context(flat_timeline(6, 10_000, 0.5, 1.0))

    assert pattern_of(context) is InsightPattern.UNDERPERFORMING


def test_on_benchmark() -> None:
    context = make_context(flat_timeline(6, 10_000, 1.0, 2.0))

    assert pattern_of(context) is InsightPattern.ON_BENCHMARK


def test_zero_benchmarks_do_not_divide_by_zero() -> None:
    context = make_context(flat_timeline(6, 10_000, 1.0, 2.0))
    context.campaign_benchmarks.ctr = 0.0
    context.campaign_benchmarks.engagement_rate = 0.0

    result = DemoInsightsProvider().analyze(context)

    assert result.summary


def test_analyze_is_deterministic() -> None:
    context = make_context(flat_timeline(6, 10_000, 0.6, 3.0))
    provider = DemoInsightsProvider()

    assert provider.analyze(context) == provider.analyze(context)


def test_analyze_labels_output_as_demo() -> None:
    result = DemoInsightsProvider().analyze(make_context(flat_timeline(6, 10_000, 1.8, 2.5)))

    assert result.provider == "demo"
    assert result.model is None


def test_analyze_uses_actual_metrics_in_text() -> None:
    timeline = flat_timeline(6, 20_000, 1.2, 2.0)
    platforms = [
        platform_summary(Platform.LINKEDIN, 60_000, 1_200, 1_800),
        platform_summary(Platform.META, 60_000, 240, 600),
    ]

    result = DemoInsightsProvider().analyze(make_context(timeline, platforms))

    assert "LinkedIn" in result.summary
    assert "2.00%" in result.summary
    assert "0.40%" in result.summary
    assert "Meta" in result.recommended_next_experiment
    assert "CTR on LinkedIn" in result.metrics_to_measure


@pytest.mark.parametrize(
    "context",
    [
        make_context(flat_timeline(6, 0, 0, 0), platforms=[]),
        make_context(flat_timeline(2, 10_000, 1.0, 2.0)),
        make_context(flat_timeline(6, 10_000, 1.0, 2.0)),
        make_context(flat_timeline(6, 10_000, 0.5, 1.0)),
    ],
)
def test_analyze_always_returns_complete_insight(context: AiInsightContext) -> None:
    result = DemoInsightsProvider().analyze(context)

    assert result.summary
    assert result.recommended_next_experiment
    assert result.hypothesis
    assert result.risks
    assert result.metrics_to_measure


def test_bundled_demo_ads_produce_distinct_insights() -> None:
    settings = get_settings()
    ads = AdRepository(settings.data_dir / "ad_set.csv").get_all()
    metrics = MetricsRepository(settings.data_dir / "metrics.csv").get_all()
    comments = CommentsRepository(settings.data_dir / "comments.csv").get_all()
    benchmarks = CampaignService().get_summary(metrics)
    provider = DemoInsightsProvider()

    patterns: dict[str, InsightPattern] = {}
    summaries: set[str] = set()

    for ad in ads:
        context = AiInsightContext(
            selected_ad=AdService().get_ad_detail(ad=ad, metrics=metrics, comments=comments),
            campaign_benchmarks=benchmarks,
        )
        patterns[ad.ad_id] = pattern_of(context)
        summaries.add(provider.analyze(context).summary)

    assert patterns == {
        "payroll_in_minutes": InsightPattern.OUTPERFORMING,
        "global_contractors": InsightPattern.PLATFORM_GAP,
        "payday_peace_of_mind": InsightPattern.ENGAGEMENT_WITHOUT_CLICKS,
        "compliance_checklist": InsightPattern.DECLINING,
        "founder_story": InsightPattern.LIMITED_DATA,
        "benefits_bundle": InsightPattern.UNDERPERFORMING,
        "switch_in_a_day": InsightPattern.RECOVERING,
    }
    assert len(summaries) == len(ads)
