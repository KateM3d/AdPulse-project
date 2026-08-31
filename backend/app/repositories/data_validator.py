from app.core.exceptions import DataLoadingError
from app.models.domain import Ad, Comment, MetricRecord


def validate_ad_relationships(
    ads: list[Ad],
    metrics: list[MetricRecord],
    comments: list[Comment],
) -> None:
    ad_ids = {ad.ad_id for ad in ads}

    unknown_metric_ad_ids = {metric.ad_id for metric in metrics if metric.ad_id not in ad_ids}

    unknown_comment_ad_ids = {comment.ad_id for comment in comments if comment.ad_id not in ad_ids}

    if unknown_metric_ad_ids:
        unknown = ", ".join(sorted(unknown_metric_ad_ids))
        raise DataLoadingError(f"Metrics reference unknown ad IDs: {unknown}")

    if unknown_comment_ad_ids:
        unknown = ", ".join(sorted(unknown_comment_ad_ids))
        raise DataLoadingError(f"Comments reference unknown ad IDs: {unknown}")
