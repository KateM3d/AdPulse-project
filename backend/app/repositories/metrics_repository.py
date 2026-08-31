from pathlib import Path

from pydantic import ValidationError

from app.core.exceptions import DataLoadingError
from app.models.domain import MetricRecord
from app.repositories.csv_loader import load_csv_rows


class MetricsRepository:
    REQUIRED_COLUMNS = {
        "date",
        "ad_id",
        "platform",
        "impressions",
        "clicks",
        "engagements",
    }

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_all(self) -> list[MetricRecord]:
        rows = load_csv_rows(
            self._file_path,
            required_columns=self.REQUIRED_COLUMNS,
        )

        metrics: list[MetricRecord] = []

        for row_number, row in enumerate(rows, start=2):
            try:
                metrics.append(MetricRecord.model_validate(row))
            except ValidationError as exc:
                raise DataLoadingError(
                    f"Invalid metric data in {self._file_path.name} at row {row_number}"
                ) from exc

        return metrics
