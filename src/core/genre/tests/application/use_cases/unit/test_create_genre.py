import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(
        name="Movie",
    )


@pytest.fixture
def documentary_category() -> Category:
    return Category(
        name="Documentary",
    )


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category
) -> GenreRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]

    return repository


@pytest.fixture
def mock_empyt_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []

    return repository


class TestCreateGenre:
    def test_when_categories_not_exist_then_raise_related_categories_not_found(
        self, mock_empyt_category_repository, mock_genre_repository
    ):
        use_case = CreateGenre(mock_genre_repository, mock_empyt_category_repository)

        category_id = uuid.uuid4()

        input = CreateGenre.Input(
            name="Action",
            categories={category_id},
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        assert str(category_id) in str(exc_info.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):

        use_case = CreateGenre(
            mock_genre_repository, mock_category_repository_with_categories
        )

        input = CreateGenre.Input(
            name="",
            categories={movie_category.id},
        )

        with pytest.raises(InvalidGenreData, match="Name cannot be empty") as exc_info:
            use_case.execute(input)
        # OR
        assert "Name cannot be empty" in str(exc_info.value)

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        movie_category,
        documentary_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            mock_genre_repository, mock_category_repository_with_categories
        )

        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id},
        )

        output = use_case.execute(input)

        assert output.id
        assert isinstance(output.id, uuid.UUID)
        assert isinstance(output, CreateGenre.Output)
        mock_genre_repository.save.assert_called_once()
        mock_genre_repository.save.assert_called_with(
            Genre(
                id=output.id,
                name="Action",
                categories={movie_category.id, documentary_category.id},
            )
        )

    def test_create_genre_without_categories(
        self,
        mock_empyt_category_repository,
        mock_genre_repository,
    ):

        input = CreateGenre.Input(
            name="Action",
            categories=set(),
        )

        use_case = CreateGenre(mock_genre_repository, mock_empyt_category_repository)

        output = use_case.execute(input)

        assert output.id
        assert isinstance(output.id, uuid.UUID)
        assert isinstance(output, CreateGenre.Output)
        mock_genre_repository.save.assert_called_once()
        mock_genre_repository.save.assert_called_with(
            Genre(
                id=output.id,
                name="Action",
                categories=set(),
            )
        )

    def test_create_genre_with_invalid_categories(
        self,
        mock_empyt_category_repository,
        mock_genre_repository,
    ):

        input = CreateGenre.Input(
            name="Action",
            categories={uuid.uuid4()},
        )

        use_case = CreateGenre(mock_genre_repository, mock_empyt_category_repository)

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_create_genre_with_invalid_data_then_raise_invalid_genre_exception(
        self,
        mock_category_repository_with_categories,
        mock_genre_repository,
        movie_category,
        documentary_category,
    ):
        input = CreateGenre.Input(
            name="",
            categories={movie_category.id, documentary_category.id},
        )

        use_case = CreateGenre(
            mock_genre_repository, mock_category_repository_with_categories
        )

        with pytest.raises(InvalidGenreData, match="Name cannot be empty"):
            use_case.execute(input)
