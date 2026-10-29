from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.ad import AdDetail
from app.schemas.campaign import CampaignSummary

InsightProviderName = Literal["demo", "openai"]


class AiInsightContext(BaseModel):
    selected_ad: AdDetail
    campaign_benchmarks: CampaignSummary


class AiCampaignInsight(BaseModel):
    """Insight content. This is also the structured-output schema sent to the LLM."""

    summary: str = Field(min_length=1)
    strengths: list[str]
    risks: list[str]
    recommended_next_experiment: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    metrics_to_measure: list[str]


class AdInsightsResponse(AiCampaignInsight):
    """Insight content plus provenance, so clients never mistake demo output for an LLM."""

    provider: InsightProviderName
    model: str | None = None


class InsightsProviderStatus(BaseModel):
    provider: InsightProviderName
    is_live: bool
    model: str | None = None
