from app.models.domain import MetricRecord
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
