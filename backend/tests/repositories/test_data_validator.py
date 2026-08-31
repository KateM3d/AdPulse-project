from datetime import date

import pytest

from app.core.exceptions import DataLoadingError
from app.models.domain import Ad, Comment, MetricRecord, Platform
from app.repositories.data_validator import validate_ad_relationships


def test_validate_ad_relationships_accepts_valid_data() -> None:
    ads = [
        Ad(
            ad_id="ad-1",
            title="Ad",
            body="Body",
            image="ad.png",
        )
    ]

    metrics = [
        MetricRecord(
            date=date(2026, 3, 2),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=20,
        )
    ]

    comments = [
        Comment(
            date=date(2026, 3, 2),
            ad_id="ad-1",
            platform=Platform.GOOGLE,
            comment="Interesting",
        )
    ]

    validate_ad_relationships(ads, metrics, comments)


def test_validate_ad_relationships_rejects_unknown_metric_ad() -> None:
    ads = [
        Ad(
            ad_id="ad-1",
            title="Ad",
            body="Body",
            image="ad.png",
        )
    ]

    metrics = [
        MetricRecord(
            date=date(2026, 3, 2),
            ad_id="missing-ad",
            platform=Platform.GOOGLE,
            impressions=100,
            clicks=10,
            engagements=20,
        )
    ]

    with pytest.raises(
        DataLoadingError,
        match="Metrics reference unknown ad IDs",
    ):
        validate_ad_relationships(ads, metrics, [])


def test_validate_ad_relationships_rejects_unknown_comment_ad() -> None:
    ads = [
        Ad(
            ad_id="ad-1",
            title="Ad",
            body="Body",
            image="ad.png",
        )
    ]

    comments = [
        Comment(
            date=date(2026, 3, 2),
            ad_id="missing-ad",
            platform=Platform.META,
            comment="Interesting",
        )
    ]

    with pytest.raises(
        DataLoadingError,
        match="Comments reference unknown ad IDs",
    ):
        validate_ad_relationships(ads, [], comments)
