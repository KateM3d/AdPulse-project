import logging

from openai import APIStatusError, OpenAI, OpenAIError

from app.core.config import Settings
from app.core.exceptions import AiInsightsUnavailableError
from app.schemas.ai_insights import (
    AdInsightsResponse,
    AiCampaignInsight,
    AiInsightContext,
    InsightProviderName,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an AI campaign performance analyst.

Analyze only the supplied campaign data.
Treat the supplied data as the only source of truth.

Do not invent or assume:
- metrics or benchmarks
- campaign context
- audience characteristics
- business goals
- causal relationships
- facts that are not present in the input

If the supplied data is insufficient to support a conclusion, say so rather
than filling the gap with an assumption.

Compare the selected ad with the supplied campaign-level benchmarks.
Consider:
- overall performance
- platform-level performance
- timeline trends
- ad title and copy
- audience comments

Treat audience comments as qualitative signals only.
Describe what individual comments suggest, but do not generalize them to the
broader audience or use them as evidence of overall audience sentiment.

Clearly distinguish observations supported by the data from interpretations.

Do not infer causes from performance patterns alone.
For example, do not attribute changes to audience fatigue, creative fatigue,
seasonality, targeting, competition, or other external factors unless the
supplied data explicitly supports that explanation.
Describe unsupported causes as unknown.

Your goal is decision support, not generic marketing advice.

Recommend exactly one practical next experiment that is directly motivated by
the supplied evidence.

The experiment should:
- change one main variable where possible
- be specific enough to test
- include a clear hypothesis
- identify the metrics that should determine whether it worked

Keep the analysis concise and actionable.

Return:
- a concise performance summary
- strengths supported by the data
- risks supported by the data
- one practical next experiment
- a testable hypothesis
- the metrics that should be measured
"""

UNAVAILABLE_MESSAGE = "Live AI insights are temporarily unavailable"


class OpenAIInsightsProvider:
    name: InsightProviderName = "openai"

    def __init__(self, settings: Settings) -> None:
        if settings.openai_api_key is None or not settings.has_openai_api_key:
            raise AiInsightsUnavailableError("OpenAI API key is not configured")

        self.model: str | None = settings.openai_model
        self._model = settings.openai_model
        self._client = OpenAI(
            api_key=settings.openai_api_key.get_secret_value().strip(),
            max_retries=0,
            timeout=settings.openai_timeout_seconds,
        )

    def analyze(self, context: AiInsightContext) -> AdInsightsResponse:
        try:
            response = self._client.responses.parse(
                model=self._model,
                instructions=SYSTEM_PROMPT,
                input=context.model_dump_json(),
                text_format=AiCampaignInsight,
            )
        except OpenAIError as exc:
            # Log only the error type and status; provider messages can echo request details.
            status = exc.status_code if isinstance(exc, APIStatusError) else None
            logger.warning("OpenAI request failed: %s (status=%s)", type(exc).__name__, status)
            raise AiInsightsUnavailableError(UNAVAILABLE_MESSAGE) from exc

        result = response.output_parsed

        if result is None:
            raise AiInsightsUnavailableError("OpenAI did not return a structured analysis")

        return AdInsightsResponse(
            **result.model_dump(),
            provider=self.name,
            model=self._model,
        )
