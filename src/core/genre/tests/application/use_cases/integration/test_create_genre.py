import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.infra.in_memory_genre_repositry import InMemoryGenreRepository


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
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository([movie_category, documentary_category])


class TestCreateGenre:
    def test_create_genre_with_categories(
        self, movie_category, documentary_category, category_repository
    ):

        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(genre_repository, category_repository)

        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id},
        )

        output = use_case.execute(input)

        assert output.id
        assert isinstance(output.id, uuid.UUID)
        assert isinstance(output, CreateGenre.Output)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_without_categories(self):

        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(genre_repository, InMemoryCategoryRepository())

        input = CreateGenre.Input(
            name="Action",
            categories=set(),
        )

        output = use_case.execute(input)

        assert output.id
        assert isinstance(output.id, uuid.UUID)
        assert isinstance(output, CreateGenre.Output)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre
        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True

    def test_when_categories_not_exist_then_raise_related_categories_not_found(
        self, category_repository
    ):

        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(genre_repository, category_repository)

        input = CreateGenre.Input(
            name="Action",
            categories={uuid.uuid4(), uuid.uuid4()},
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)
