from collections import defaultdict
from datetime import date

from app.models.domain import MetricRecord, Platform
from app.schemas.analytics import PlatformSummary, TimelinePoint
from app.schemas.campaign import CampaignSummary
from app.services.metrics import calculate_rate


class CampaignService:
    def get_summary(
        self,
        metrics: list[MetricRecord],
    ) -> CampaignSummary:
        total_impressions = sum(metric.impressions for metric in metrics)
        total_clicks = sum(metric.clicks for metric in metrics)
        total_engagements = sum(metric.engagements for metric in metrics)

        dates = [metric.date for metric in metrics]

        return CampaignSummary(
            total_impressions=total_impressions,
            total_clicks=total_clicks,
            total_engagements=total_engagements,
            ctr=calculate_rate(total_clicks, total_impressions),
            engagement_rate=calculate_rate(
                total_engagements,
                total_impressions,
            ),
            start_date=min(dates) if dates else None,
            end_date=max(dates) if dates else None,
        )

    def get_timeline(
        self,
        metrics: list[MetricRecord],
    ) -> list[TimelinePoint]:
        grouped: dict[date, dict[str, int]] = defaultdict(
            lambda: {
                "impressions": 0,
                "clicks": 0,
                "engagements": 0,
            }
        )

        for metric in metrics:
            grouped[metric.date]["impressions"] += metric.impressions
            grouped[metric.date]["clicks"] += metric.clicks
            grouped[metric.date]["engagements"] += metric.engagements

        return [
            TimelinePoint(
                date=metric_date,
                impressions=values["impressions"],
                clicks=values["clicks"],
                engagements=values["engagements"],
                ctr=calculate_rate(
                    values["clicks"],
                    values["impressions"],
                ),
                engagement_rate=calculate_rate(
                    values["engagements"],
                    values["impressions"],
                ),
            )
            for metric_date, values in sorted(grouped.items())
        ]

    def get_platform_summary(
        self,
        metrics: list[MetricRecord],
    ) -> list[PlatformSummary]:
        grouped: dict[Platform, dict[str, int]] = defaultdict(
            lambda: {
                "impressions": 0,
                "clicks": 0,
                "engagements": 0,
            }
        )

        for metric in metrics:
            grouped[metric.platform]["impressions"] += metric.impressions
            grouped[metric.platform]["clicks"] += metric.clicks
            grouped[metric.platform]["engagements"] += metric.engagements

        return [
            PlatformSummary(
                platform=platform,
                impressions=values["impressions"],
                clicks=values["clicks"],
                engagements=values["engagements"],
                ctr=calculate_rate(
                    values["clicks"],
                    values["impressions"],
                ),
                engagement_rate=calculate_rate(
                    values["engagements"],
                    values["impressions"],
                ),
            )
            for platform, values in sorted(
                grouped.items(),
                key=lambda item: item[0].value,
            )
        ]
