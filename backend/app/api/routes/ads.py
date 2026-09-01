from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.exceptions import AdNotFoundError
from app.dependencies import (
    get_ad_repository,
    get_comments_repository,
    get_metrics_repository,
)
from app.repositories.ad_repository import AdRepository
from app.repositories.comments_repository import CommentsRepository
from app.repositories.metrics_repository import MetricsRepository
from app.schemas.ad import AdDetail, AdSummary
from app.services.ad_service import AdService

router = APIRouter(prefix="/ads")


@router.get(
    "",
    response_model=list[AdSummary],
    summary="List ad performance summaries",
    description=("Returns performance summaries for all ads in the campaign."),
)
def get_ads(
    ad_repository: Annotated[
        AdRepository,
        Depends(get_ad_repository),
    ],
    metrics_repository: Annotated[
        MetricsRepository,
        Depends(get_metrics_repository),
    ],
) -> list[AdSummary]:
    ads = ad_repository.get_all()
    metrics = metrics_repository.get_all()

    return AdService().get_ad_summaries(ads, metrics)


@router.get(
    "/{ad_id}",
    response_model=AdDetail,
    summary="Get detailed ad analytics",
    description=(
        "Returns ad content, aggregated performance, timeline, "
        "platform breakdown, and associated comments."
    ),
    responses={
        404: {
            "description": "Ad not found",
        },
    },
)
def get_ad(
    ad_id: str,
    ad_repository: Annotated[
        AdRepository,
        Depends(get_ad_repository),
    ],
    metrics_repository: Annotated[
        MetricsRepository,
        Depends(get_metrics_repository),
    ],
    comments_repository: Annotated[
        CommentsRepository,
        Depends(get_comments_repository),
    ],
) -> AdDetail:
    ad = ad_repository.get_by_id(ad_id)

    if ad is None:
        raise AdNotFoundError(ad_id)

    metrics = metrics_repository.get_all()
    comments = comments_repository.get_all()

    return AdService().get_ad_detail(
        ad=ad,
        metrics=metrics,
        comments=comments,
    )
