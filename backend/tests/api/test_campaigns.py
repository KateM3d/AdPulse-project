from fastapi.testclient import TestClient

from app.core.exceptions import DataLoadingError
from app.dependencies import get_metrics_repository
from app.main import app
from app.repositories.metrics_repository import MetricsRepository

client = TestClient(app)


def test_get_campaign_returns_campaign_analytics() -> None:
    response = client.get("/api/v1/campaign")

    assert response.status_code == 200

    data = response.json()

    assert set(data) == {
        "summary",
        "timeline",
        "platforms",
    }

    assert data["summary"]["total_impressions"] == 1281840
    assert data["summary"]["total_clicks"] == 15220
    assert data["summary"]["total_engagements"] == 24666
    assert data["summary"]["start_date"] == "2026-03-02"
    assert data["summary"]["end_date"] == "2026-05-04"

    assert len(data["timeline"]) == 10
    assert len(data["platforms"]) == 3

    assert [item["platform"] for item in data["platforms"]] == [
        "Google",
        "LinkedIn",
        "Meta",
    ]

    assert isinstance(data["summary"]["ctr"], float)


def test_data_loading_error_returns_500() -> None:
    def raise_data_loading_error() -> MetricsRepository:
        raise DataLoadingError("metrics.csv is unreadable")

    app.dependency_overrides[get_metrics_repository] = raise_data_loading_error
    try:
        response = client.get("/api/v1/campaign")

        assert response.status_code == 500
        assert response.json() == {"detail": "metrics.csv is unreadable"}
    finally:
        app.dependency_overrides.clear()
