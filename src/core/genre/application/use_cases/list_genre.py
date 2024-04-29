from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class ListGenreInput:
    order_by: str = "name"
    ordering: str = "asc"
    current_page: int = 1
    page_size: int = 10


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


@dataclass
class ListGenreOutputMeta:
    current_page: int = 1
    page_size: int = 10
    total: int = 0


T = TypeVar("T")


@dataclass
class ListGenreOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListGenreOutputMeta = field(default_factory=ListGenreOutputMeta)


@dataclass
class ListGenreResponse(ListGenreOutput[GenreOutput]):
    pass


class ListGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.genre_repository = repository

    def execute(self, request: ListGenreInput) -> ListGenreResponse:
        genres = self.genre_repository.list()

        sorted_genres = sorted(
            [
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ],
            key=lambda genre: getattr(genre, request.order_by),
            reverse=False if request.ordering == "asc" else True,
        )

        page_offset = (request.current_page - 1) * request.page_size
        genres_page = sorted_genres[page_offset : page_offset + request.page_size]

        return ListGenreResponse(
            data=genres_page,
            meta=ListGenreOutputMeta(
                current_page=request.current_page,
                page_size=request.page_size,
                total=len(sorted_genres),
            ),
        )
