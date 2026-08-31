from pathlib import Path

from pydantic import ValidationError

from app.core.exceptions import DataLoadingError
from app.models.domain import Ad
from app.repositories.csv_loader import load_csv_rows


class AdRepository:
    REQUIRED_COLUMNS = {"ad_id", "title", "body", "image"}

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_all(self) -> list[Ad]:
        rows = load_csv_rows(
            self._file_path,
            required_columns=self.REQUIRED_COLUMNS,
        )

        ads: list[Ad] = []

        for row_number, row in enumerate(rows, start=2):
            try:
                ads.append(Ad.model_validate(row))
            except ValidationError as exc:
                raise DataLoadingError(
                    f"Invalid ad data in {self._file_path.name} at row {row_number}"
                ) from exc

        return ads
