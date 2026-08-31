from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class Platform(StrEnum):
    GOOGLE = "Google"
    LINKEDIN = "LinkedIn"
    META = "Meta"


class Ad(BaseModel):
    ad_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    image: str = Field(min_length=1)


class MetricRecord(BaseModel):
    date: date
    ad_id: str = Field(min_length=1)
    platform: Platform
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    engagements: int = Field(ge=0)


class Comment(BaseModel):
    date: date
    ad_id: str = Field(min_length=1)
    platform: Platform
    comment: str = Field(min_length=1)
