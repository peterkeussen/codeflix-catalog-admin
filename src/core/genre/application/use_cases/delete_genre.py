from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreDoesNotExistsException, GenreNotFoundException
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreDoesNotExistsException(f"Genre id {input.id} does not exists")
        self.repository.delete(input.id)  # type: ignore
