import logging
from unittest.mock import MagicMock, patch

import httpx2
import openai
import pytest
from pydantic import SecretStr

from app.core.config import Settings
from app.core.exceptions import AiInsightsUnavailableError
from app.schemas.ai_insights import AdInsightsResponse, AiCampaignInsight
from app.services.insights.openai_provider import UNAVAILABLE_MESSAGE, OpenAIInsightsProvider
from tests.insight_factories import flat_timeline, make_context

FAKE_KEY = "sk-test-not-a-real-key-1234"


def live_settings() -> Settings:
    return Settings(ai_provider="openai", openai_api_key=SecretStr(FAKE_KEY))


def build_provider(client: MagicMock) -> OpenAIInsightsProvider:
    with patch("app.services.insights.openai_provider.OpenAI", return_value=client):
        return OpenAIInsightsProvider(live_settings())


def test_analyze_returns_structured_insight_labelled_as_openai() -> None:
    parsed = AiCampaignInsight(
        summary="The selected ad outperforms campaign CTR.",
        strengths=["CTR is above the campaign benchmark."],
        risks=["No audience comments are available."],
        recommended_next_experiment="Test an alternative headline.",
        hypothesis="A clearer headline will improve CTR.",
        metrics_to_measure=["CTR", "Engagement rate"],
    )
    client = MagicMock()
    client.responses.parse.return_value = MagicMock(output_parsed=parsed)

    result = build_provider(client).analyze(make_context(flat_timeline(4, 1_000, 2.0, 3.0)))

    assert result == AdInsightsResponse(
        **parsed.model_dump(),
        provider="openai",
        model="gpt-4o-mini",
    )
    client.responses.parse.assert_called_once()
    assert client.responses.parse.call_args.kwargs["text_format"] is AiCampaignInsight


def test_client_receives_key_from_settings_without_retries() -> None:
    with patch("app.services.insights.openai_provider.OpenAI") as openai_mock:
        OpenAIInsightsProvider(live_settings())

    kwargs = openai_mock.call_args.kwargs
    assert kwargs["api_key"] == FAKE_KEY
    assert kwargs["max_retries"] == 0


@pytest.mark.parametrize("key", [None, SecretStr(""), SecretStr("   ")])
def test_init_requires_api_key(key: SecretStr | None) -> None:
    with pytest.raises(AiInsightsUnavailableError, match="OpenAI API key is not configured"):
        OpenAIInsightsProvider(Settings(ai_provider="openai", openai_api_key=key))


def test_analyze_raises_when_response_is_not_parsed() -> None:
    client = MagicMock()
    client.responses.parse.return_value = MagicMock(output_parsed=None)

    with pytest.raises(
        AiInsightsUnavailableError,
        match="OpenAI did not return a structured analysis",
    ):
        build_provider(client).analyze(make_context(flat_timeline(4, 0, 0, 0)))


def test_api_errors_are_wrapped_without_leaking_details(
    caplog: pytest.LogCaptureFixture,
) -> None:
    request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
    error = openai.AuthenticationError(
        message=f"Incorrect API key provided: {FAKE_KEY}",
        response=httpx2.Response(401, request=request),
        body=None,
    )
    client = MagicMock()
    client.responses.parse.side_effect = error

    with caplog.at_level(logging.WARNING), pytest.raises(AiInsightsUnavailableError) as exc_info:
        build_provider(client).analyze(make_context(flat_timeline(4, 1_000, 2.0, 3.0)))

    assert str(exc_info.value) == UNAVAILABLE_MESSAGE
    assert FAKE_KEY not in caplog.text
    assert "AuthenticationError" in caplog.text
    assert "status=401" in caplog.text


def test_connection_errors_are_wrapped() -> None:
    request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
    client = MagicMock()
    client.responses.parse.side_effect = openai.APIConnectionError(request=request)

    with pytest.raises(AiInsightsUnavailableError, match=UNAVAILABLE_MESSAGE):
        build_provider(client).analyze(make_context(flat_timeline(4, 1_000, 2.0, 3.0)))


def test_settings_repr_does_not_expose_key() -> None:
    settings = live_settings()

    assert FAKE_KEY not in repr(settings)
    assert FAKE_KEY not in str(settings.model_dump())
