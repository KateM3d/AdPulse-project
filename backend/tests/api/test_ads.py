from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app

client = TestClient(app)


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
    response = client.get(
        "/api/v1/ads/global_contractors",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ad_id"] == "global_contractors"
    assert data["title"] == ("Pay contractors anywhere")
    assert data["image"] == "global_contractors.svg"

    assert data["total_impressions"] == 253754
    assert data["total_clicks"] == 3102
    assert data["total_engagements"] == 4507

    assert len(data["timeline"]) == 10
    assert len(data["platforms"]) == 2
    assert len(data["comments"]) == 6


def test_get_ad_returns_404_when_ad_does_not_exist() -> None:
    response = client.get("/api/v1/ads/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ad 'does-not-exist' was not found",
    }


def test_generate_ad_insights_returns_404_when_ad_does_not_exist() -> None:
    response = client.post("/api/v1/ads/does-not-exist/insights")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ad 'does-not-exist' was not found",
    }


def test_generate_ad_insights_returns_503_when_api_key_missing() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(openai_api_key=None)

    try:
        response = client.post(
            "/api/v1/ads/global_contractors/insights",
        )

        assert response.status_code == 503
        assert response.json() == {
            "detail": "OpenAI API key is not configured",
        }
    finally:
        app.dependency_overrides.clear()
