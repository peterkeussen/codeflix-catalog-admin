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
        raise NotImplementedError

    def get_by_name(self, name: str) -> Genre | None:
        raise NotImplementedError

    def delete(self, genre: Genre) -> None:
        raise NotImplementedError

    def update(self, genre: Genre) -> None:
        raise NotImplementedError

    def list(self) -> list[Genre]:
        raise NotImplementedError
