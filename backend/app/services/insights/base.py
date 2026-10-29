from typing import Protocol

from app.schemas.ai_insights import AdInsightsResponse, AiInsightContext, InsightProviderName


class InsightsProvider(Protocol):
    name: InsightProviderName
    model: str | None

    def analyze(self, context: AiInsightContext) -> AdInsightsResponse: ...
