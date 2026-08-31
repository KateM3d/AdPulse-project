from datetime import date

import pytest
from pydantic import ValidationError

from app.models.domain import Ad, Comment, MetricRecord, Platform


def test_create_ad() -> None:
    ad = Ad(
        ad_id="example-ad",
        title="Example Ad",
        body="Example campaign copy",
        image="example.png",
    )

    assert ad.ad_id == "example-ad"
    assert ad.image == "example.png"


def test_ad_rejects_empty_ad_id() -> None:
    with pytest.raises(ValidationError):
        Ad(
            ad_id="",
            title="Example Ad",
            body="Example campaign copy",
            image="example.png",
        )


def test_create_metric_record() -> None:
    metric = MetricRecord(
        date=date(2026, 3, 2),
        ad_id="example-ad",
        platform=Platform.META,
        impressions=1000,
        clicks=50,
        engagements=75,
    )

    assert metric.platform == Platform.META
    assert metric.impressions == 1000


@pytest.mark.parametrize(
    "field",
    ["impressions", "clicks", "engagements"],
)
def test_metric_record_rejects_negative_metrics(field: str) -> None:
    data: dict[str, object] = {
        "date": date(2026, 3, 2),
        "ad_id": "example-ad",
        "platform": Platform.META,
        "impressions": 1000,
        "clicks": 50,
        "engagements": 75,
    }
    data[field] = -1

    with pytest.raises(ValidationError):
        MetricRecord.model_validate(data)


def test_metric_record_rejects_unknown_platform() -> None:
    with pytest.raises(ValidationError):
        MetricRecord.model_validate(
            {
                "date": date(2026, 3, 2),
                "ad_id": "example-ad",
                "platform": "TikTok",
                "impressions": 1000,
                "clicks": 50,
                "engagements": 75,
            }
        )


def test_create_comment() -> None:
    comment = Comment(
        date=date(2026, 3, 2),
        ad_id="example-ad",
        platform=Platform.LINKEDIN,
        comment="How long does it take to switch payroll providers?",
    )

    assert comment.comment == "How long does it take to switch payroll providers?"
