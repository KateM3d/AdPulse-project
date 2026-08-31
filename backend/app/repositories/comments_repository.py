from pathlib import Path

from pydantic import ValidationError

from app.core.exceptions import DataLoadingError
from app.models.domain import Comment
from app.repositories.csv_loader import load_csv_rows


class CommentsRepository:
    REQUIRED_COLUMNS = {
        "date",
        "ad_id",
        "platform",
        "comment",
    }

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_all(self) -> list[Comment]:
        rows = load_csv_rows(
            self._file_path,
            required_columns=self.REQUIRED_COLUMNS,
        )

        comments: list[Comment] = []

        for row_number, row in enumerate(rows, start=2):
            try:
                comments.append(Comment.model_validate(row))
            except ValidationError as exc:
                raise DataLoadingError(
                    f"Invalid comment data in {self._file_path.name} at row {row_number}"
                ) from exc

        return comments
