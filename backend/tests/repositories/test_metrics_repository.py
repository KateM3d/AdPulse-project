from pathlib import Path

import pytest

from app.core.exceptions import DataLoadingError
from app.repositories.metrics_repository import MetricsRepository


def test_get_all_returns_validated_metrics(tmp_path: Path) -> None:
    file_path = tmp_path / "metrics.csv"
    file_path.write_text(
        "date,ad_id,platform,impressions,clicks,engagements\n2026-03-02,ad-1,Google,1000,25,40\n",
        encoding="utf-8",
    )

    repository = MetricsRepository(file_path)

    metrics = repository.get_all()

    assert len(metrics) == 1
    assert metrics[0].ad_id == "ad-1"
    assert metrics[0].platform == "Google"
    assert metrics[0].impressions == 1000
    assert metrics[0].clicks == 25
    assert metrics[0].engagements == 40


def test_get_all_rejects_invalid_metric_data(tmp_path: Path) -> None:
    file_path = tmp_path / "metrics.csv"
    file_path.write_text(
        "date,ad_id,platform,impressions,clicks,engagements\n2026-03-02,ad-1,Google,-1,25,40\n",
        encoding="utf-8",
    )

    repository = MetricsRepository(file_path)

    with pytest.raises(
        DataLoadingError,
        match="Invalid metric data",
    ):
        repository.get_all()
