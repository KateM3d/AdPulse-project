from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.ai_insights import InsightsProviderStatus
from app.services.insights.factory import get_provider_status

router = APIRouter(prefix="/insights")


@router.get(
    "/provider",
    response_model=InsightsProviderStatus,
    summary="Get the active insights provider",
    description=(
        "Reports whether insights come from the deterministic demo provider "
        "or a live LLM. Never exposes credentials."
    ),
)
def get_insights_provider_status(
    settings: Annotated[Settings, Depends(get_settings)],
) -> InsightsProviderStatus:
    return get_provider_status(settings)
