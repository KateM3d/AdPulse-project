from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.core.config import Settings, get_settings
from app.main import app

client = TestClient(app)


def test_provider_status_defaults_to_demo() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(_env_file=None)  # type: ignore[call-arg]

    try:
        response = client.get("/api/v1/insights/provider")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"provider": "demo", "is_live": False, "model": None}


def test_provider_status_never_exposes_the_api_key() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        ai_provider="openai",
        openai_api_key=SecretStr("sk-test-secret"),
    )

    try:
        response = client.get("/api/v1/insights/provider")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["provider"] == "openai"
    assert response.json()["is_live"] is True
    assert "sk-test-secret" not in response.text
