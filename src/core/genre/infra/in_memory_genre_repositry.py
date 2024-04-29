from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: list[Genre] = None) -> None:  # type: ignore
        self.genres: list[Genre] = genres or []

    def save(self, genre: Genre) -> None:
        self.genres.append(genre)

    def get_by_id(self, genre_id: UUID) -> Genre | None:
        for genre in self.genres:
            if genre.id == genre_id:
                return genre
        return None

    def get_by_name(self, name: str) -> Genre | None:
        for genre in self.genres:
            if genre.name == name:
                return genre
        return None

    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        self.genres.remove(genre)  # type: ignore

    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id)
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(genre)

    def list(self) -> list[Genre]:
        return [genre for genre in self.genres]
