from datetime import date

from pydantic import BaseModel, Field

from app.models.domain import Platform


class AdSummary(BaseModel):
    ad_id: str
    title: str
    image: str
    total_impressions: int = Field(ge=0)
    total_clicks: int = Field(ge=0)
    total_engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)


class AdTimelinePoint(BaseModel):
    date: date
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)


class AdPlatformSummary(BaseModel):
    platform: Platform
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)


class AdComment(BaseModel):
    date: date
    platform: Platform
    comment: str


class AdDetail(BaseModel):
    ad_id: str
    title: str
    body: str
    image: str
    total_impressions: int = Field(ge=0)
    total_clicks: int = Field(ge=0)
    total_engagements: int = Field(ge=0)
    ctr: float = Field(ge=0)
    engagement_rate: float = Field(ge=0)
    timeline: list[AdTimelinePoint]
    platforms: list[AdPlatformSummary]
    comments: list[AdComment]
