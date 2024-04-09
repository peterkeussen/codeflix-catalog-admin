import uuid
from unittest.mock import create_autospec

import pytest

from core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    GenreDoesNotExistsException,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def mock_category_repository() -> GenreRepository:
    return create_autospec(CategoryRepository)


class TestUpdateGenre:
    def test_genre_update_when_genre_exists_then_update(
        self, mock_genre_repository, mock_category_repository
    ):
        movie = Category(name="Movie")
        documentary = Category(name="Documentary")
        genre = Genre(
            name="Action", is_active=True, categories={movie.id, documentary.id}
        )
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            is_active=False,
            category_ids={movie.id},
        )

        use_case.execute(input)

        assert genre.is_active is False
        assert genre.categories == {movie.id}
        assert mock_genre_repository.update.call_count == 1

    def test_genre_update_when_genre_does_not_exist_then_not_found_exception(
        self, mock_genre_repository, mock_category_repository
    ):
        mock_genre_repository.get_by_id.return_value = None
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Action",
            is_active=False,
            category_ids=set(),
        )

        with pytest.raises(GenreDoesNotExistsException):
            use_case.execute(input)

    def test_when_genre_with_invalid_data_then_raise_invalid_genre_exception(
        self, mock_genre_repository, mock_category_repository
    ):
        genre = Genre(
            name="Action",
            categories=set(),
        )
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        input = UpdateGenre.Input(id=genre.id, name="")

        with pytest.raises(InvalidGenreData):
            use_case.execute(input)

    def test_when_genre_with_invalid_category_then_raise_invalid_genre_exception(
        self, mock_genre_repository, mock_category_repository
    ):
        genre = Genre(
            name="Action",
            categories=set(),
        )
        mock_genre_repository.get_by_id.return_value = genre
        mock_category_repository.get_by_id.return_value = None
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        input = UpdateGenre.Input(id=genre.id, name="Action", category_ids={uuid.uuid4()})  # type: ignore

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)
