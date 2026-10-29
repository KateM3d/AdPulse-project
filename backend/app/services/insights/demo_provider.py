"""Deterministic, rule-based insights for running AdPulse without an LLM.

Nothing here calls an external service. The output is derived purely from the
supplied metrics, and every response is labelled with ``provider="demo"`` so
clients can present it as sample content rather than model output.
"""

from dataclasses import dataclass
from enum import StrEnum

from app.schemas.ai_insights import AdInsightsResponse, AiInsightContext, InsightProviderName
from app.schemas.analytics import PlatformSummary, TimelinePoint
from app.services.metrics import calculate_rate

MIN_WEEKS_FOR_TREND = 4
TREND_THRESHOLD = 0.2
PLATFORM_GAP_RATIO = 1.8
OUTPERFORM_INDEX = 1.2
UNDERPERFORM_INDEX = 0.8
ENGAGEMENT_LEAD_INDEX = 1.1
CLICK_LAG_INDEX = 0.9


class InsightPattern(StrEnum):
    NO_DELIVERY = "no_delivery"
    LIMITED_DATA = "limited_data"
    DECLINING = "declining"
    RECOVERING = "recovering"
    PLATFORM_GAP = "platform_gap"
    ENGAGEMENT_WITHOUT_CLICKS = "engagement_without_clicks"
    OUTPERFORMING = "outperforming"
    UNDERPERFORMING = "underperforming"
    ON_BENCHMARK = "on_benchmark"


@dataclass(frozen=True)
class PerformanceSignals:
    ctr: float
    engagement_rate: float
    benchmark_ctr: float
    benchmark_engagement_rate: float
    impressions: int
    active_weeks: int
    early_ctr: float
    late_ctr: float
    best_platform: PlatformSummary | None
    worst_platform: PlatformSummary | None
    comment_count: int

    @property
    def ctr_index(self) -> float:
        return _index(self.ctr, self.benchmark_ctr)

    @property
    def engagement_index(self) -> float:
        return _index(self.engagement_rate, self.benchmark_engagement_rate)

    @property
    def has_trend(self) -> bool:
        return self.active_weeks >= MIN_WEEKS_FOR_TREND and self.early_ctr > 0

    @property
    def ctr_trend(self) -> float:
        if not self.has_trend:
            return 0.0
        return (self.late_ctr - self.early_ctr) / self.early_ctr

    @property
    def platform_ratio(self) -> float:
        if self.best_platform is None or self.worst_platform is None:
            return 1.0
        if self.worst_platform.ctr == 0:
            return float("inf") if self.best_platform.ctr > 0 else 1.0
        return self.best_platform.ctr / self.worst_platform.ctr


def _index(value: float, benchmark: float) -> float:
    if benchmark == 0:
        return 1.0
    return value / benchmark


def _period_ctr(points: list[TimelinePoint]) -> float:
    return calculate_rate(
        sum(point.clicks for point in points),
        sum(point.impressions for point in points),
    )


def extract_signals(context: AiInsightContext) -> PerformanceSignals:
    ad = context.selected_ad
    benchmarks = context.campaign_benchmarks

    timeline = sorted(ad.timeline, key=lambda point: point.date)
    midpoint = len(timeline) // 2

    delivering_platforms = sorted(
        (platform for platform in ad.platforms if platform.impressions > 0),
        key=lambda platform: (platform.ctr, platform.platform),
    )
    has_comparison = len(delivering_platforms) >= 2

    return PerformanceSignals(
        ctr=ad.ctr,
        engagement_rate=ad.engagement_rate,
        benchmark_ctr=benchmarks.ctr,
        benchmark_engagement_rate=benchmarks.engagement_rate,
        impressions=ad.total_impressions,
        active_weeks=len(timeline),
        early_ctr=_period_ctr(timeline[:midpoint]),
        late_ctr=_period_ctr(timeline[midpoint:]),
        best_platform=delivering_platforms[-1] if has_comparison else None,
        worst_platform=delivering_platforms[0] if has_comparison else None,
        comment_count=len(ad.comments),
    )


def classify(signals: PerformanceSignals) -> InsightPattern:
    if signals.impressions == 0:
        return InsightPattern.NO_DELIVERY
    if signals.active_weeks < MIN_WEEKS_FOR_TREND:
        return InsightPattern.LIMITED_DATA
    if signals.ctr_trend <= -TREND_THRESHOLD:
        return InsightPattern.DECLINING
    if signals.ctr_trend >= TREND_THRESHOLD:
        return InsightPattern.RECOVERING
    if signals.platform_ratio >= PLATFORM_GAP_RATIO:
        return InsightPattern.PLATFORM_GAP
    if signals.engagement_index >= ENGAGEMENT_LEAD_INDEX and signals.ctr_index <= CLICK_LAG_INDEX:
        return InsightPattern.ENGAGEMENT_WITHOUT_CLICKS
    if signals.ctr_index >= OUTPERFORM_INDEX and signals.engagement_index >= 1:
        return InsightPattern.OUTPERFORMING
    if signals.ctr_index <= UNDERPERFORM_INDEX and signals.engagement_index < 1:
        return InsightPattern.UNDERPERFORMING
    return InsightPattern.ON_BENCHMARK


def _pct(value: float) -> str:
    return f"{value:.2f}%"


def _relative(index: float) -> str:
    change = (index - 1) * 100
    direction = "above" if change >= 0 else "below"
    return f"{abs(change):.0f}% {direction}"


def _strengths(signals: PerformanceSignals) -> list[str]:
    strengths: list[str] = []

    if signals.impressions and signals.ctr_index >= 1:
        strengths.append(
            f"CTR of {_pct(signals.ctr)} is {_relative(signals.ctr_index)} "
            f"the campaign average of {_pct(signals.benchmark_ctr)}."
        )
    if signals.impressions and signals.engagement_index >= 1:
        strengths.append(
            f"Engagement rate of {_pct(signals.engagement_rate)} is "
            f"{_relative(signals.engagement_index)} the campaign average of "
            f"{_pct(signals.benchmark_engagement_rate)}."
        )
    if signals.best_platform is not None:
        strengths.append(
            f"{signals.best_platform.platform} is the strongest platform for this ad "
            f"at {_pct(signals.best_platform.ctr)} CTR."
        )
    if signals.ctr_trend >= TREND_THRESHOLD:
        strengths.append(
            f"CTR improved from {_pct(signals.early_ctr)} in the first half of the "
            f"flight to {_pct(signals.late_ctr)} in the second half."
        )

    if not strengths and signals.impressions:
        strengths.append(
            f"The ad delivered {signals.impressions:,} impressions across "
            f"{signals.active_weeks} active week(s), giving a usable baseline."
        )

    return strengths


def _risks(signals: PerformanceSignals) -> list[str]:
    risks: list[str] = []

    if signals.impressions == 0:
        return ["The ad has no recorded impressions, so performance cannot be assessed."]

    if signals.ctr_index < 1:
        risks.append(
            f"CTR of {_pct(signals.ctr)} is {_relative(signals.ctr_index)} "
            f"the campaign average of {_pct(signals.benchmark_ctr)}."
        )
    if signals.engagement_index < 1:
        risks.append(
            f"Engagement rate of {_pct(signals.engagement_rate)} is "
            f"{_relative(signals.engagement_index)} the campaign average."
        )
    if signals.ctr_trend <= -TREND_THRESHOLD:
        risks.append(
            f"CTR fell from {_pct(signals.early_ctr)} in the first half of the flight "
            f"to {_pct(signals.late_ctr)} in the second half. The data does not show why."
        )
    if signals.worst_platform is not None and signals.platform_ratio >= PLATFORM_GAP_RATIO:
        risks.append(
            f"{signals.worst_platform.platform} CTR is only "
            f"{_pct(signals.worst_platform.ctr)}, absorbing "
            f"{signals.worst_platform.impressions:,} impressions."
        )
    if signals.active_weeks < MIN_WEEKS_FOR_TREND:
        risks.append(
            f"Only {signals.active_weeks} week(s) of data are available, "
            "which is too few to separate trend from noise."
        )
    if signals.comment_count == 0:
        risks.append("No audience comments are available, so there is no qualitative signal.")

    if not risks:
        risks.append("No material risks stand out in the available data.")

    return risks


@dataclass(frozen=True)
class _Recommendation:
    summary: str
    experiment: str
    hypothesis: str
    metrics: list[str]


def _recommend(pattern: InsightPattern, signals: PerformanceSignals) -> _Recommendation:
    best = signals.best_platform
    worst = signals.worst_platform

    match pattern:
        case InsightPattern.NO_DELIVERY:
            return _Recommendation(
                summary="This ad has not delivered any impressions yet, so there is nothing "
                "to evaluate.",
                experiment="Confirm the ad is approved and eligible to serve, then relaunch "
                "it on a single platform with a fixed weekly budget.",
                hypothesis="If the ad is eligible and funded, it will collect enough "
                "impressions within one week to establish a CTR baseline.",
                metrics=["Impressions", "CTR"],
            )
        case InsightPattern.LIMITED_DATA:
            return _Recommendation(
                summary=f"This ad has only {signals.active_weeks} week(s) of delivery. Early "
                f"CTR is {_pct(signals.ctr)} against a campaign average of "
                f"{_pct(signals.benchmark_ctr)}, but the sample is too small to draw "
                "conclusions.",
                experiment="Keep the creative and budget unchanged for at least two more "
                "weeks before testing variations.",
                hypothesis="With four or more weeks of data, the ad's CTR will settle within "
                "a stable range that can be compared fairly with the rest of the campaign.",
                metrics=["Weekly CTR", "Weekly engagement rate", "Impressions"],
            )
        case InsightPattern.DECLINING:
            return _Recommendation(
                summary=f"CTR dropped from {_pct(signals.early_ctr)} to "
                f"{_pct(signals.late_ctr)} between the first and second half of the "
                "flight. The data shows the decline but not its cause.",
                experiment="Run a refreshed version of the creative (new headline and visual, "
                "same offer) against the current version with an even budget split.",
                hypothesis="If the decline is tied to the current creative, the refreshed "
                "version will restore CTR to at least the first-half level.",
                metrics=["CTR by variant", "Week-over-week CTR change", "Engagement rate"],
            )
        case InsightPattern.RECOVERING:
            return _Recommendation(
                summary=f"CTR rose from {_pct(signals.early_ctr)} in the first half of the "
                f"flight to {_pct(signals.late_ctr)} in the second half, overtaking its "
                "earlier performance.",
                experiment="Shift 20% of budget from lower-performing ads to this ad for "
                "two weeks while keeping the current creative unchanged.",
                hypothesis="If the improvement is durable, CTR will stay at or above "
                f"{_pct(signals.late_ctr)} at the higher spend level.",
                metrics=["CTR at increased spend", "Clicks", "Engagement rate"],
            )
        case InsightPattern.PLATFORM_GAP:
            assert best is not None and worst is not None
            return _Recommendation(
                summary=f"Performance depends heavily on platform: {best.platform} reaches "
                f"{_pct(best.ctr)} CTR while {worst.platform} reaches only "
                f"{_pct(worst.ctr)}.",
                experiment=f"Move half of the {worst.platform} budget to {best.platform} "
                "for two weeks and compare blended results with the previous period.",
                hypothesis=f"Reallocating spend toward {best.platform} will raise the ad's "
                "blended CTR without reducing total clicks.",
                metrics=[
                    f"CTR on {best.platform}",
                    f"CTR on {worst.platform}",
                    "Blended CTR",
                    "Total clicks",
                ],
            )
        case InsightPattern.ENGAGEMENT_WITHOUT_CLICKS:
            return _Recommendation(
                summary=f"The ad earns attention but not clicks: engagement rate is "
                f"{_pct(signals.engagement_rate)} ({_relative(signals.engagement_index)} "
                f"average) while CTR is {_pct(signals.ctr)} "
                f"({_relative(signals.ctr_index)} average).",
                experiment="Test a variant with an explicit call to action and a concrete "
                "next step (for example, pricing or a demo) while keeping the visual.",
                hypothesis="A clearer call to action will convert existing engagement into "
                "clicks and lift CTR toward the campaign average.",
                metrics=["CTR by variant", "Engagement rate by variant", "Clicks"],
            )
        case InsightPattern.OUTPERFORMING:
            return _Recommendation(
                summary=f"This is one of the campaign's strongest ads: CTR of "
                f"{_pct(signals.ctr)} is {_relative(signals.ctr_index)} the campaign "
                "average, with engagement also above average.",
                experiment="Increase this ad's budget by 25% for two weeks and track whether "
                "efficiency holds at higher volume.",
                hypothesis="CTR will remain at least 20% above the campaign average as spend "
                "increases.",
                metrics=["CTR at increased spend", "Impressions", "Clicks"],
            )
        case InsightPattern.UNDERPERFORMING:
            return _Recommendation(
                summary=f"The ad trails the campaign on both measures: CTR of "
                f"{_pct(signals.ctr)} and engagement rate of "
                f"{_pct(signals.engagement_rate)} are below average.",
                experiment="Test a rewritten headline that names one specific, concrete "
                "benefit, keeping the visual and audience unchanged.",
                hypothesis="A more specific message will lift CTR to at least the campaign "
                f"average of {_pct(signals.benchmark_ctr)}.",
                metrics=["CTR by variant", "Engagement rate by variant"],
            )
        case InsightPattern.ON_BENCHMARK:
            return _Recommendation(
                summary=f"The ad performs close to the campaign average, with CTR of "
                f"{_pct(signals.ctr)} versus {_pct(signals.benchmark_ctr)}.",
                experiment="Run a headline A/B test with one alternative focused on the "
                "primary customer benefit.",
                hypothesis="A benefit-led headline will lift CTR by at least 10% relative to "
                "the current version.",
                metrics=["CTR by variant", "Engagement rate by variant"],
            )


class DemoInsightsProvider:
    name: InsightProviderName = "demo"
    model: str | None = None

    def analyze(self, context: AiInsightContext) -> AdInsightsResponse:
        signals = extract_signals(context)
        pattern = classify(signals)
        recommendation = _recommend(pattern, signals)

        return AdInsightsResponse(
            summary=recommendation.summary,
            strengths=_strengths(signals),
            risks=_risks(signals),
            recommended_next_experiment=recommendation.experiment,
            hypothesis=recommendation.hypothesis,
            metrics_to_measure=recommendation.metrics,
            provider=self.name,
            model=self.model,
        )
