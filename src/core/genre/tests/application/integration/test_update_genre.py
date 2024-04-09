import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import (
    GenreDoesNotExistsException,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repositry import InMemoryGenreRepository


class TestUpdateGenre:
    def test_when_genre_does_not_exist_then_raise_genre_not_found_exception(self):
        genre = Genre(
            name="Action",
            categories=set(),
        )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository()
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(
            id=uuid.uuid4(), name="Action", is_active=True, category_ids=set()
        )

        with pytest.raises(GenreDoesNotExistsException):
            use_case.execute(input)

    def test_genre_with_invalid_data_then_raise_invalid_genre_exception(self):
        genre = Genre(
            name="Action",
            categories=set(),
        )
        repository = InMemoryGenreRepository([genre])
        use_case = UpdateGenre(repository, InMemoryCategoryRepository())  # type: ignore

        input = UpdateGenre.Input(id=genre.id, name="")

        with pytest.raises(InvalidGenreData):
            use_case.execute(input)

    def test_genre_with_invalid_category_then_raise_invalid_genre_exception(self):
        genre = Genre(
            name="Action",
            categories=set(),
        )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository([Category(name="Action")])
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(id=genre.id, name="Action", category_ids={uuid.uuid4()})  # type: ignore

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_update_genre_add_one_valid_category(self):
        category_documentary = Category(name="Documentary")
        category_drama = Category(name="Drama")
        genre = Genre(
            name="Action",
            categories={category_documentary.id, category_drama.id},
        )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository(
            [
                Category(name="Action"),
                Category(name="Documentary"),
                Category(name="Drama"),
            ]
        )
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(id=genre.id, name="Action", category_ids={category_repository.get_by_name("Action").id, category_repository.get_by_name("Drama").id, category_repository.get_by_name("Documentary").id})  # type: ignore

        use_case.execute(input)

        assert len(genre.categories) == 3

    def test_update_genre_remove_one_valid_category(self):
        category_documentary = Category(name="Documentary")
        category_drama = Category(name="Drama")
        category_action = Category(name="Action")
        genre = Genre(
            name="Action",
            categories={category_documentary.id, category_drama.id, category_action.id},
        )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository(
            [
                Category(name="Documentary"),
                Category(name="Drama"),
            ]
        )
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(id=genre.id, name="Romance", is_active=False, category_ids={category_repository.get_by_name("Documentary").id, category_repository.get_by_name("Drama").id})  # type: ignore

        use_case.execute(input)

        assert len(genre.categories) == 2
        assert genre.name == "Romance"
        assert genre.is_active is False
