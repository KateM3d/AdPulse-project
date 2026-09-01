from collections import defaultdict
from datetime import date

from app.models.domain import Ad, Comment, MetricRecord, Platform
from app.schemas.ad import AdComment, AdDetail, AdSummary
from app.schemas.analytics import PlatformSummary, TimelinePoint
from app.services.metrics import calculate_rate


class AdService:
    def get_ad_summaries(
        self,
        ads: list[Ad],
        metrics: list[MetricRecord],
    ) -> list[AdSummary]:
        metrics_by_ad: dict[str, list[MetricRecord]] = {}

        for metric in metrics:
            metrics_by_ad.setdefault(metric.ad_id, []).append(metric)

        summaries: list[AdSummary] = []

        for ad in ads:
            ad_metrics = metrics_by_ad.get(ad.ad_id, [])

            total_impressions = sum(metric.impressions for metric in ad_metrics)
            total_clicks = sum(metric.clicks for metric in ad_metrics)
            total_engagements = sum(metric.engagements for metric in ad_metrics)

            summaries.append(
                AdSummary(
                    ad_id=ad.ad_id,
                    title=ad.title,
                    image=ad.image,
                    total_impressions=total_impressions,
                    total_clicks=total_clicks,
                    total_engagements=total_engagements,
                    ctr=calculate_rate(
                        total_clicks,
                        total_impressions,
                    ),
                    engagement_rate=calculate_rate(
                        total_engagements,
                        total_impressions,
                    ),
                )
            )

        return summaries

    def get_ad_timeline(
        self,
        ad_id: str,
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
            if metric.ad_id != ad_id:
                continue

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

    def get_ad_platform_summary(
        self,
        ad_id: str,
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
            if metric.ad_id != ad_id:
                continue

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

    def get_ad_detail(
        self,
        ad: Ad,
        metrics: list[MetricRecord],
        comments: list[Comment],
    ) -> AdDetail:
        ad_metrics = [metric for metric in metrics if metric.ad_id == ad.ad_id]
        ad_comments = [comment for comment in comments if comment.ad_id == ad.ad_id]

        total_impressions = sum(metric.impressions for metric in ad_metrics)
        total_clicks = sum(metric.clicks for metric in ad_metrics)
        total_engagements = sum(metric.engagements for metric in ad_metrics)

        return AdDetail(
            ad_id=ad.ad_id,
            title=ad.title,
            body=ad.body,
            image=ad.image,
            total_impressions=total_impressions,
            total_clicks=total_clicks,
            total_engagements=total_engagements,
            ctr=calculate_rate(
                total_clicks,
                total_impressions,
            ),
            engagement_rate=calculate_rate(
                total_engagements,
                total_impressions,
            ),
            timeline=self.get_ad_timeline(ad.ad_id, metrics),
            platforms=self.get_ad_platform_summary(ad.ad_id, metrics),
            comments=[
                AdComment(
                    date=comment.date,
                    platform=comment.platform,
                    comment=comment.comment,
                )
                for comment in sorted(
                    ad_comments,
                    key=lambda item: item.date,
                )
            ],
        )
