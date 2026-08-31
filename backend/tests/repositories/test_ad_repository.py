from pathlib import Path

import pytest

from app.core.exceptions import DataLoadingError
from app.repositories.ad_repository import AdRepository


def test_get_all_returns_validated_ads(tmp_path: Path) -> None:
    file_path = tmp_path / "ad_set.csv"
    file_path.write_text(
        "ad_id,title,body,image\n"
        "ad-1,First Ad,First body,first.png\n"
        "ad-2,Second Ad,Second body,second.png\n",
        encoding="utf-8",
    )

    repository = AdRepository(file_path)

    ads = repository.get_all()

    assert len(ads) == 2

    assert ads[0].ad_id == "ad-1"
    assert ads[0].title == "First Ad"
    assert ads[0].body == "First body"
    assert ads[0].image == "first.png"

    assert ads[1].ad_id == "ad-2"


def test_get_all_rejects_invalid_ad_data(tmp_path: Path) -> None:
    file_path = tmp_path / "ad_set.csv"
    file_path.write_text(
        "ad_id,title,body,image\n,First Ad,First body,first.png\n",
        encoding="utf-8",
    )

    repository = AdRepository(file_path)

    with pytest.raises(
        DataLoadingError,
        match="Invalid ad data",
    ):
        repository.get_all()
