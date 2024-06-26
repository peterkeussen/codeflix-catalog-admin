from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.application.use_cases.exceptions import (
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre


class CreateGenre:
    def __init__(self, repository, category_repository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        is_active: bool = True
        categories: set[UUID] = field(default_factory=set)

    @dataclass
    class Output:
        id: UUID

    def execute(self, input_data: Input) -> Output:
        categories = {category.id for category in self.category_repository.list()}
        if not input_data.categories.issubset(categories):
            raise RelatedCategoriesNotFound(
                f"Related categories not found: {input_data.categories - categories}"
            )

        try:
            genre = Genre(
                name=input_data.name, is_active=True, categories=input_data.categories
            )
        except ValueError as error:
            raise InvalidGenreData(error) from error

        self.repository.save(genre)
        return CreateGenre.Output(id=genre.id)
