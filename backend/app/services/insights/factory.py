from app.core.config import Settings
from app.core.exceptions import AiInsightsUnavailableError
from app.schemas.ai_insights import InsightsProviderStatus
from app.services.insights.base import InsightsProvider
from app.services.insights.demo_provider import DemoInsightsProvider
from app.services.insights.openai_provider import OpenAIInsightsProvider


def create_insights_provider(settings: Settings) -> InsightsProvider:
    """Return the configured provider.

    Live AI is opt-in: it requires ``AI_PROVIDER=openai`` *and* an API key. An
    explicit ``openai`` selection without a key fails loudly instead of quietly
    serving demo content in its place.
    """
    if settings.ai_provider == "openai":
        if not settings.has_openai_api_key:
            raise AiInsightsUnavailableError(
                "Live AI is enabled (AI_PROVIDER=openai) but OPENAI_API_KEY is not configured"
            )
        return OpenAIInsightsProvider(settings)

    return DemoInsightsProvider()


def get_provider_status(settings: Settings) -> InsightsProviderStatus:
    if settings.ai_provider == "openai":
        return InsightsProviderStatus(
            provider="openai",
            is_live=settings.has_openai_api_key,
            model=settings.openai_model,
        )

    return InsightsProviderStatus(provider="demo", is_live=False, model=None)
