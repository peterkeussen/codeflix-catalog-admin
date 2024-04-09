import uuid
from os import name
from typing import Any
from unittest.mock import create_autospec

import pytest

from src.core.genre.application.exceptions import GenreDoesNotExistsException
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository():
    return create_autospec(GenreRepository)


class TestDeleteGenre:
    def test_delete_genre_repository(
        self,
        mock_genre_repository,
    ):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(mock_genre_repository)

        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        mock_genre_repository.delete.assert_called_once_with(genre.id)

    def test_delete_genre_does_not_exist_then_raise_not_found(
        self,
        mock_genre_repository,
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = DeleteGenre(mock_genre_repository)

        with pytest.raises(
            GenreDoesNotExistsException, match="Genre id .* does not exists"
        ):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))
