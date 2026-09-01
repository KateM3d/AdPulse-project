from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_metrics_repository
from app.repositories.metrics_repository import MetricsRepository
from app.schemas.campaign import CampaignResponse
from app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaign")


@router.get(
    "",
    response_model=CampaignResponse,
    summary="Get campaign analytics",
    description=(
        "Returns the aggregated campaign summary, timeline, and platform-level performance."
    ),
)
def get_campaign(
    metrics_repository: Annotated[
        MetricsRepository,
        Depends(get_metrics_repository),
    ],
) -> CampaignResponse:
    metrics = metrics_repository.get_all()

    return CampaignService().get_campaign(metrics)
