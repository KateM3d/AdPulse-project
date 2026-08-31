from pathlib import Path

import pytest

from app.core.exceptions import DataLoadingError
from app.repositories.csv_loader import load_csv_rows


def test_load_csv_rows(tmp_path: Path) -> None:
    file_path = tmp_path / "ads.csv"
    file_path.write_text(
        "ad_id,title\nad-1,Example Ad\n",
        encoding="utf-8",
    )

    rows = load_csv_rows(
        file_path,
        required_columns={"ad_id", "title"},
    )

    assert rows == [
        {
            "ad_id": "ad-1",
            "title": "Example Ad",
        }
    ]


def test_load_csv_rows_removes_exported_index_column(tmp_path: Path) -> None:
    file_path = tmp_path / "ads.csv"
    file_path.write_text(
        "Unnamed: 0,ad_id,title\n0,ad-1,Example Ad\n",
        encoding="utf-8",
    )

    rows = load_csv_rows(
        file_path,
        required_columns={"ad_id", "title"},
    )

    assert rows == [
        {
            "ad_id": "ad-1",
            "title": "Example Ad",
        }
    ]


def test_load_csv_rows_rejects_missing_required_columns(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "ads.csv"
    file_path.write_text(
        "ad_id\nad-1\n",
        encoding="utf-8",
    )

    with pytest.raises(DataLoadingError, match="Missing required columns"):
        load_csv_rows(
            file_path,
            required_columns={"ad_id", "title"},
        )


def test_load_csv_rows_rejects_missing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.csv"

    with pytest.raises(DataLoadingError, match="Data file not found"):
        load_csv_rows(
            file_path,
            required_columns={"ad_id"},
        )
