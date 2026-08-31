from pathlib import Path

import pytest

from app.core.exceptions import DataLoadingError
from app.repositories.comments_repository import CommentsRepository


def test_get_all_returns_validated_comments(tmp_path: Path) -> None:
    file_path = tmp_path / "comments.csv"
    file_path.write_text(
        "date,ad_id,platform,comment\n2026-03-02,ad-1,LinkedIn,Very interesting concept\n",
        encoding="utf-8",
    )

    repository = CommentsRepository(file_path)

    comments = repository.get_all()

    assert len(comments) == 1
    assert comments[0].ad_id == "ad-1"
    assert comments[0].platform == "LinkedIn"
    assert comments[0].comment == "Very interesting concept"


def test_get_all_rejects_invalid_comment_data(tmp_path: Path) -> None:
    file_path = tmp_path / "comments.csv"
    file_path.write_text(
        "date,ad_id,platform,comment\n2026-03-02,ad-1,TikTok,Very interesting concept\n",
        encoding="utf-8",
    )

    repository = CommentsRepository(file_path)

    with pytest.raises(
        DataLoadingError,
        match="Invalid comment data",
    ):
        repository.get_all()
