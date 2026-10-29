from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.core.config import AiProviderName, Settings, get_settings
from app.dependencies import get_insights_provider
from app.main import app
from app.schemas.ai_insights import AdInsightsResponse, AiInsightContext, InsightProviderName

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.clear()


def use_settings(ai_provider: AiProviderName, openai_api_key: SecretStr | None = None) -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        ai_provider=ai_provider,
        openai_api_key=openai_api_key,
    )


def test_get_ads_returns_ad_performance_summaries() -> None:
    response = client.get("/api/v1/ads")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 7

    first_ad = data[0]

    assert set(first_ad) == {
        "ad_id",
        "title",
        "image",
        "total_impressions",
        "total_clicks",
        "total_engagements",
        "ctr",
        "engagement_rate",
    }


def test_get_ad_returns_detailed_analytics() -> None:
    response = client.get("/api/v1/ads/global_contractors")

    assert response.status_code == 200

    data = response.json()

    assert data["ad_id"] == "global_contractors"
    assert data["title"] == "Pay contractors anywhere"
    assert data["image"] == "global_contractors.svg"

    assert data["total_impressions"] == 253754
    assert data["total_clicks"] == 3102
    assert data["total_engagements"] == 4507
    assert data["ctr"] == pytest.approx(3102 / 253754 * 100)
    assert data["engagement_rate"] == pytest.approx(4507 / 253754 * 100)

    assert len(data["timeline"]) == 10
    assert [item["platform"] for item in data["platforms"]] == ["LinkedIn", "Meta"]
    assert len(data["comments"]) == 6


def test_get_ad_returns_404_when_ad_does_not_exist() -> None:
    response = client.get("/api/v1/ads/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ad 'does-not-exist' was not found",
    }


def test_generate_ad_insights_returns_404_when_ad_does_not_exist() -> None:
    use_settings(ai_provider="demo")

    response = client.post("/api/v1/ads/does-not-exist/insights")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ad 'does-not-exist' was not found",
    }


def test_generate_ad_insights_uses_demo_provider_without_api_key() -> None:
    use_settings(ai_provider="demo", openai_api_key=None)

    response = client.post("/api/v1/ads/global_contractors/insights")

    assert response.status_code == 200

    data = response.json()

    assert data["provider"] == "demo"
    assert data["model"] is None
    assert "LinkedIn" in data["summary"]
    assert data["recommended_next_experiment"]
    assert data["hypothesis"]
    assert data["metrics_to_measure"]


def test_demo_insights_differ_between_ads() -> None:
    use_settings(ai_provider="demo")

    first = client.post("/api/v1/ads/payroll_in_minutes/insights").json()
    second = client.post("/api/v1/ads/compliance_checklist/insights").json()

    assert first["summary"] != second["summary"]
    assert first["recommended_next_experiment"] != second["recommended_next_experiment"]


def test_generate_ad_insights_returns_503_when_live_ai_has_no_key() -> None:
    use_settings(ai_provider="openai", openai_api_key=None)

    response = client.post("/api/v1/ads/global_contractors/insights")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Live AI is enabled (AI_PROVIDER=openai) but OPENAI_API_KEY is not configured",
    }


def test_generate_ad_insights_returns_provider_metadata_from_live_provider() -> None:
    class FakeLiveProvider:
        name: InsightProviderName = "openai"
        model: str | None = "test-model"

        def analyze(self, context: AiInsightContext) -> AdInsightsResponse:
            return AdInsightsResponse(
                summary=f"Live analysis of {context.selected_ad.ad_id}",
                strengths=[],
                risks=[],
                recommended_next_experiment="Test something.",
                hypothesis="Something will improve.",
                metrics_to_measure=["CTR"],
                provider=self.name,
                model=self.model,
            )

    app.dependency_overrides[get_insights_provider] = FakeLiveProvider

    response = client.post("/api/v1/ads/global_contractors/insights")

    assert response.status_code == 200
    assert response.json()["provider"] == "openai"
    assert response.json()["model"] == "test-model"
    assert response.json()["summary"] == "Live analysis of global_contractors"
