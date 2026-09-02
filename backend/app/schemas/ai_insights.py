from pydantic import BaseModel, Field

from app.schemas.ad import AdDetail
from app.schemas.campaign import CampaignSummary


class AiInsightContext(BaseModel):
    selected_ad: AdDetail
    campaign_benchmarks: CampaignSummary


class AiCampaignInsight(BaseModel):
    summary: str = Field(min_length=1)
    strengths: list[str]
    risks: list[str]
    recommended_next_experiment: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    metrics_to_measure: list[str]
