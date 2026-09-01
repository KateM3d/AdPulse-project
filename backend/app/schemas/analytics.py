from datetime import date

from pydantic import BaseModel, Field

from app.models.domain import Platform


class TimelinePoint(BaseModel):
    date: date
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)


class PlatformSummary(BaseModel):
    platform: Platform
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)
