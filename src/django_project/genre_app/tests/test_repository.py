import uuid
from operator import ge

import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.models import Genre as GenreORM
from src.django_project.genre_app.repository import DjangoORMGenreRepository

@pytest.fixture
def genre() -> Genre:
    category_repository = DjangoORMCategoryRepository()
    category = Category(id=uuid.uuid4(), name="Action")
    category_repository.save(category)
    return Genre(name="Action", is_active=True, categories={category.id})

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
        category_repository = DjangoORMCategoryRepository()

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

@pytest.mark.django_db
class TestDelete:
    def test_deletes_genre_in_database(self, genre):
        repository = DjangoORMGenreRepository()
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        repository.delete(genre)
        assert GenreORM.objects.count() == 0
        
@pytest.mark.django_db
class TestUpdate:
    def test_updates_genre_in_database(self, genre):
        repository = DjangoORMGenreRepository()
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        genre.change_name("Comedy")
        repository.update(genre)
        assert GenreORM.objects.count() == 1
        genre_orm = GenreORM.objects.first()
        assert genre_orm.name == "Comedy"
        assert genre_orm.is_active == genre.is_active
        assert genre_orm.categories.count() == 1

        related_category = genre_orm.categories.get()
        assert {related_category.id} == genre.categories

        assert repository.get_by_id(genre.id) == genre

@pytest.mark.django_db
class TestList:
    def test_returns_all_genres(self, genre):
        repository = DjangoORMGenreRepository()
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        assert repository.list() == [genre]
        
@pytest.mark.django_db
class TestGetById:
    def test_returns_genre_by_id(self, genre):
        repository = DjangoORMGenreRepository()
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        assert repository.get_by_id(genre.id) == genre