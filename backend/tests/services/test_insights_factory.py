from unittest.mock import patch

import pytest
from pydantic import SecretStr

from app.core.config import Settings
from app.core.exceptions import AiInsightsUnavailableError
from app.services.insights.demo_provider import DemoInsightsProvider
from app.services.insights.factory import create_insights_provider, get_provider_status
from app.services.insights.openai_provider import OpenAIInsightsProvider

TEST_KEY = SecretStr("sk-test")


def test_demo_is_the_default_provider() -> None:
    settings = Settings(_env_file=None)  # type: ignore[call-arg]

    assert settings.ai_provider == "demo"
    assert isinstance(create_insights_provider(settings), DemoInsightsProvider)


def test_demo_provider_is_used_even_when_a_key_exists() -> None:
    settings = Settings(ai_provider="demo", openai_api_key=TEST_KEY)

    with patch("app.services.insights.openai_provider.OpenAI") as openai_mock:
        provider = create_insights_provider(settings)

    assert isinstance(provider, DemoInsightsProvider)
    openai_mock.assert_not_called()


def test_openai_provider_requires_explicit_selection_and_key() -> None:
    settings = Settings(ai_provider="openai", openai_api_key=TEST_KEY)

    with patch("app.services.insights.openai_provider.OpenAI"):
        provider = create_insights_provider(settings)

    assert isinstance(provider, OpenAIInsightsProvider)


@pytest.mark.parametrize("key", [None, SecretStr(""), SecretStr("  ")])
def test_openai_without_key_fails_instead_of_falling_back(key: SecretStr | None) -> None:
    settings = Settings(ai_provider="openai", openai_api_key=key)

    with pytest.raises(AiInsightsUnavailableError, match="OPENAI_API_KEY is not configured"):
        create_insights_provider(settings)


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ValueError):
        Settings(ai_provider="anthropic")  # type: ignore[arg-type]


def test_provider_status() -> None:
    assert get_provider_status(Settings(ai_provider="demo")).model_dump() == {
        "provider": "demo",
        "is_live": False,
        "model": None,
    }
    assert get_provider_status(
        Settings(ai_provider="openai", openai_api_key=TEST_KEY, openai_model="gpt-4o-mini")
    ).model_dump() == {"provider": "openai", "is_live": True, "model": "gpt-4o-mini"}
    assert get_provider_status(Settings(ai_provider="openai", openai_api_key=None)).is_live is False
