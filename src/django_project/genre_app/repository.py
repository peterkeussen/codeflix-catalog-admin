from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre):
        with transaction.atomic():
            genre_orm = GenreORM.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_orm.categories.set(genre.categories)

    def get_by_id(self, genre_id) -> Genre | None:
        try:
            genre_orm = GenreORM.objects.get(id=genre_id)
            return Genre(
                id=genre_orm.id,
                name=genre_orm.name,
                is_active=genre_orm.is_active,
                categories=set(genre_orm.categories.values_list("id", flat=True)),
            )
        except GenreORM.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Genre | None:
        try:
            genre_orm = GenreORM.objects.get(name=name)
            return Genre(
                id=genre_orm.id,
                name=genre_orm.name,
                is_active=genre_orm.is_active,
                categories=set(genre_orm.categories.values_list("id", flat=True)),
            )
        except GenreORM.DoesNotExist:
            return None

    def delete(self, genre: Genre) -> None:
        GenreORM.objects.get(id=genre.id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_orm = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None
        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
                # categories=set(genre.categories),
            )
            genre_orm.categories.set(genre.categories)

    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre_orm.id,
                name=genre_orm.name,
                is_active=genre_orm.is_active,
                categories=set(genre_orm.categories.values_list("id", flat=True)),
            )
            for genre_orm in GenreORM.objects.all()
        ]
