from unicodedata import category
import uuid

import pytest
from core.category.infra.in_memory_category_repositry import InMemoryCategoryRepository
from core.genre.application.exceptions import GenreDoesNotExistsException, InvalidGenreData, RelatedCategoriesNotFound
from core.genre.application.use_cases.update_genre import UpdateGenre
from core.genre.domain.genre import Genre
from core.genre.infra.in_memory_genre_repositry import InMemoryGenreRepository
from django_project.category_app import repository
from django_project.category_app.models import Category
from django_project.category_app.tests.test_view import category_repository


class TestUpdateGenre:
    def test_when_genre_does_not_exist_then_raise_genre_not_found_exception(self):
        genre = Genre(
            name="Action",
            categories=set(),
            )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository()
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(id=uuid.uuid4(), name="Action", category_ids=set())

        with pytest.raises(GenreDoesNotExistsException):
            use_case.execute(input)
            
            
    def test_genre_with_invalid_data_then_raise_invalid_genre_exception(self):
        genre = Genre(
            name="Action",
            categories=set(),
            )
        repository = InMemoryGenreRepository([genre])
        use_case = UpdateGenre(repository, InMemoryCategoryRepository()) # type: ignore

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

        input = UpdateGenre.Input(id=genre.id, name="Action", category_ids={uuid.uuid4()}) # type: ignore

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)
            
    def test_update_genre_with_valid_category(self):
        genre = Genre(
            name="Action",
            categories=set(),
            )
        repository = InMemoryGenreRepository([genre])
        category_repository = InMemoryCategoryRepository([Category(name="Action")])
        use_case = UpdateGenre(repository, category_repository)

        input = UpdateGenre.Input(id=genre.id, name="Action", category_ids={category_repository.get_by_name("Action").id}) # type: ignore

        use_case.execute(input)