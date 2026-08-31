import csv
from pathlib import Path

from app.core.exceptions import DataLoadingError


def load_csv_rows(
    file_path: Path,
    required_columns: set[str],
) -> list[dict[str, str]]:
    if not file_path.exists():
        raise DataLoadingError(f"Data file not found: {file_path}")

    try:
        with file_path.open(encoding="utf-8-sig", newline="") as file:
            sample = file.read(2048)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;")
                reader = csv.DictReader(file, dialect=dialect)
            except csv.Error:
                reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise DataLoadingError(f"CSV file has no header: {file_path}")

            columns = set(reader.fieldnames)
            missing_columns = required_columns - columns

            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise DataLoadingError(f"Missing required columns in {file_path.name}: {missing}")

            rows: list[dict[str, str]] = []

            for raw_row in reader:
                row = {
                    key: value
                    for key, value in raw_row.items()
                    if key and not key.startswith("Unnamed:")
                }
                rows.append(row)

            return rows

    except OSError as exc:
        raise DataLoadingError(f"Failed to load CSV file: {file_path}") from exc
