from unittest.mock import MagicMock, patch

from app.core.config import Settings
from app.core.exceptions import AiInsightsUnavailableError
from app.schemas.ad import AdDetail
from app.schemas.ai_insights import AiCampaignInsight, AiInsightContext
from app.schemas.campaign import CampaignSummary
from app.services.ai_insights_service import AiInsightsService


def test_analyze_returns_structured_insight() -> None:
    settings = Settings(openai_api_key="test-key")

    context = AiInsightContext(
        selected_ad=AdDetail(
            ad_id="test-ad",
            title="Test ad",
            body="Test body",
            image="test.png",
            total_impressions=1000,
            total_clicks=20,
            total_engagements=30,
            ctr=2.0,
            engagement_rate=3.0,
            timeline=[],
            platforms=[],
            comments=[],
        ),
        campaign_benchmarks=CampaignSummary(
            total_impressions=10000,
            total_clicks=150,
            total_engagements=220,
            ctr=1.5,
            engagement_rate=2.2,
            start_date=None,
            end_date=None,
        ),
    )

    expected = AiCampaignInsight(
        summary="The selected ad outperforms campaign CTR.",
        strengths=["CTR is above the campaign benchmark."],
        risks=["No audience comments are available."],
        recommended_next_experiment="Test an alternative headline.",
        hypothesis="A clearer headline will improve CTR.",
        metrics_to_measure=["CTR", "Engagement rate"],
    )

    mock_response = MagicMock()
    mock_response.output_parsed = expected

    with patch("app.services.ai_insights_service.OpenAI") as openai_mock:
        client = MagicMock()
        client.responses.parse.return_value = mock_response
        openai_mock.return_value = client

        service = AiInsightsService(settings)
        result = service.analyze(context)

    assert result == expected

    client.responses.parse.assert_called_once()


def test_init_requires_api_key() -> None:
    settings = Settings(openai_api_key=None)

    try:
        AiInsightsService(settings)
    except AiInsightsUnavailableError as error:
        assert str(error) == "OpenAI API key is not configured"
    else:
        raise AssertionError("Expected AiInsightsUnavailableError")


def test_analyze_raises_when_response_is_not_parsed() -> None:
    settings = Settings(openai_api_key="test-key")

    context = AiInsightContext(
        selected_ad=AdDetail(
            ad_id="test-ad",
            title="Test ad",
            body="Test body",
            image="test.png",
            total_impressions=0,
            total_clicks=0,
            total_engagements=0,
            ctr=0.0,
            engagement_rate=0.0,
            timeline=[],
            platforms=[],
            comments=[],
        ),
        campaign_benchmarks=CampaignSummary(
            total_impressions=0,
            total_clicks=0,
            total_engagements=0,
            ctr=0.0,
            engagement_rate=0.0,
            start_date=None,
            end_date=None,
        ),
    )

    mock_response = MagicMock()
    mock_response.output_parsed = None

    with patch("app.services.ai_insights_service.OpenAI") as openai_mock:
        client = MagicMock()
        client.responses.parse.return_value = mock_response
        openai_mock.return_value = client

        service = AiInsightsService(settings)

        try:
            service.analyze(context)
        except AiInsightsUnavailableError as error:
            assert str(error) == "OpenAI did not return a structured analysis"
        else:
            raise AssertionError("Expected AiInsightsUnavailableError")
