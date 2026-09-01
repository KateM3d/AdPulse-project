from datetime import date

from pydantic import BaseModel, Field


class CampaignSummary(BaseModel):
    total_impressions: int = Field(ge=0)
    total_clicks: int = Field(ge=0)
    total_engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)
    start_date: date | None
    end_date: date | None
