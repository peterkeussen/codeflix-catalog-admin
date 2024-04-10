import uuid
from operator import ge

import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoCategoryRepository
from src.django_project.genre_app.models import Genre as GenreORM
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_orm = GenreORM.objects.first()
        assert genre_orm.id == genre.id
        assert genre_orm.name == genre.name
        assert genre_orm.is_active == genre.is_active

    def test_saves_genre_with_categories(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoCategoryRepository()

        category = Category(id=uuid.uuid4(), name="Action")
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)

        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_orm = GenreORM.objects.first()
        assert genre_orm.id == genre.id
        assert genre_orm.name == genre.name
        assert genre_orm.is_active == genre.is_active
        assert genre_orm.categories.count() == 1

        related_category = genre_orm.categories.get()
        assert related_category.id == category.id
        assert related_category.name == category.name
