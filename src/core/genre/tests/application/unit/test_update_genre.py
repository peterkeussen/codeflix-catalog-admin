import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreDoesNotExistsException
from src.core.genre.application.use_cases.update_genre import UpdateGenre
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
def action_category() -> Category:
    return Category(
        name="Action",
    )


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category, action_category
) -> GenreRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [
        movie_category,
        documentary_category,
        action_category,
    ]

    return repository


@pytest.fixture
def mock_empyt_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []

    return repository


class TestUpdateGenre:
    def test_genre_update_when_genre_does_not_exist_then_raise_genre_not_found_exception(
        self, mock_empyt_category_repository, mock_genre_repository
    ):
        use_case = UpdateGenre(mock_genre_repository, mock_empyt_category_repository)

        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Action",
            is_active=True,
            category_ids=set(),
        )

        with pytest.raises(GenreDoesNotExistsException):
            use_case.execute(input)
