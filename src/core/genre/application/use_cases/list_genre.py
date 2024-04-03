from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.genre_repository = repository

    @dataclass
    class Imput:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput]

    def execute(self, input: Imput) -> Output:
        genres = self.genre_repository.list()

        mapper_genres = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in genres
        ]

        return ListGenre.Output(data=mapper_genres)
