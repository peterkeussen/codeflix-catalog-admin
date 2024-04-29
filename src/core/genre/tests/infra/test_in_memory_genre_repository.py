from src.core.genre.infra.in_memory_genre_repositry import InMemoryGenreRepository
from src.django_project.genre_app.models import Genre


class TestCreateGenre:
    def test_create_genre(self) -> None:
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        assert len(genre_repository.genres) == 1
        assert genre_repository.get_by_id(genre.id)

        assert genre_repository.get_by_name("Action")


class TestListGenre:
    def test_list_genre(self) -> None:
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        assert len(genre_repository.list()) == 1


class TestDeleteGenre:
    def test_delete_genre(self) -> None:
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        genre_repository.delete(genre.id)

        assert len(genre_repository.list()) == 0


class TestUpdateGenre:
    def test_update_genre(self) -> None:
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        genre.name = "Action 2"
        genre_repository.update(genre)

        assert genre_repository.get_by_name("Action 2")


class TestGetGenre:
    def test_get_genre(self) -> None:
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        assert genre_repository.get_by_id(genre.id)
        assert genre_repository.get_by_name("Action")
